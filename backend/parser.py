"""
LegalLens AI - Multimodal & Resilient File Parser.
Extracts clean text from PDF, Scanned PDF (OCR), Microsoft Word (.docx), and Plain Text (.txt).
Enforces strict 15MB file payload limit with zero-dependency XML/zlib fallbacks.
"""

import io
import zipfile
import xml.etree.ElementTree as ET
from typing import Optional

# Maximum payload size limit: 15 Megabytes
MAX_FILE_SIZE_BYTES = 15 * 1024 * 1024

try:
    import fitz  # PyMuPDF
except ImportError:
    fitz = None

try:
    import pytesseract
except ImportError:
    pytesseract = None

try:
    from PIL import Image
except ImportError:
    Image = None

try:
    import docx
except ImportError:
    docx = None


def extract_docx_xml_fallback(file_bytes: bytes) -> str:
    """Zero-dependency pure Python docx text extractor from OpenXML archive."""
    try:
        with zipfile.ZipFile(io.BytesIO(file_bytes)) as z:
            xml_content = z.read("word/document.xml")
            tree = ET.fromstring(xml_content)
            ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
            paragraphs = []
            for p in tree.iterfind('.//w:p', ns):
                texts = [node.text for node in p.iterfind('.//w:t', ns) if node.text]
                if texts:
                    paragraphs.append(''.join(texts))
            return '\n'.join(paragraphs)
    except Exception:
        return ""


def extract_text_from_file(file_bytes: bytes, filename: str) -> str:
    """
    Extracts text from PDF, DOCX, or TXT file bytes.
    Enforces 15MB limit and provides OCR fallback for scanned PDFs.
    """
    if len(file_bytes) > MAX_FILE_SIZE_BYTES:
        raise ValueError(f"Uploaded file '{filename}' exceeds maximum allowable size of 15MB ({len(file_bytes)} bytes).")

    ext = filename.lower().split('.')[-1] if '.' in filename else 'txt'

    ALLOWED_EXTENSIONS = {'txt', 'docx', 'pdf'}
    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError(f"Unsupported file format: '{ext}'. Please upload a PDF, DOCX, or TXT file.")

    if ext == 'txt':
        try:
            return file_bytes.decode('utf-8')
        except UnicodeDecodeError:
            return file_bytes.decode('latin-1', errors='ignore')

    elif ext == 'docx':
        if docx:
            try:
                doc = docx.Document(io.BytesIO(file_bytes))
                return "\n".join([para.text for para in doc.paragraphs if para.text])
            except Exception:
                return extract_docx_xml_fallback(file_bytes)
        return extract_docx_xml_fallback(file_bytes)

    elif ext == 'pdf':
        if fitz:
            try:
                doc = fitz.open(stream=file_bytes, filetype="pdf")
                text = ""
                for page in doc:
                    text += page.get_text("text") + "\n"

                # If text is extremely short, it may be a scanned document -> OCR
                if len(text.strip()) < 50 and pytesseract and Image:
                    ocr_text = ""
                    for page in doc:
                        pix = page.get_pixmap()
                        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                        try:
                            page_text = pytesseract.image_to_string(img)
                            ocr_text += page_text + "\n"
                        except Exception:
                            pass
                    if ocr_text.strip():
                        return ocr_text
                return text
            except Exception:
                pass

        # Fallback raw extraction
        try:
            return file_bytes.decode('utf-8', errors='ignore')
        except Exception:
            return ""

    return ""
