"""
LegalLens AI - Edge Cases, Unicode Robustness, and Fuzzing Test Suite.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi.testclient import TestClient
from backend.app import app
from backend.legal_engine import (
    analyze_document_text,
    extract_document_clauses,
    detect_document_metadata,
    generate_annotated_html
)
from backend.parser import extract_text_from_file

client = TestClient(app)

def test_empty_document_analysis():
    res = analyze_document_text("", "empty.txt")
    assert "risk_assessment" in res
    assert res["risk_assessment"]["score"] >= 10
    assert len(res["clauses"]) >= 0

def test_whitespace_only_document():
    res = analyze_document_text("   \n\t  \r\n   ", "spaces.txt")
    assert "risk_assessment" in res
    assert res["risk_assessment"]["score"] >= 10

def test_unicode_and_special_chars():
    unicode_text = """
    ⚖️ AGREEMENT FOR SERVICES ⚖️
    Party A (α-Corp, Tokyo 🇯🇵) hereby indemnifies and holds harmless Party B (β-Inc, München 🇩🇪).
    Payment Terms: Net-90 days with 18% compound interest per annum.
    Governing Law: Jurisdiction of Delaware law.
    """
    res = analyze_document_text(unicode_text, "unicode_contract.txt")
    assert res["risk_assessment"]["score"] > 0
    assert len(res["risks_and_flags"]) > 0
    assert "indemnif" in res["annotated_html"].lower()

def test_parser_unsupported_file_extension():
    try:
        extract_text_from_file(b"test data", "malicious.exe")
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "Unsupported file format" in str(e)

def test_parser_text_file_handling():
    content = b"Simple Employment Agreement. Non-compete for 12 months worldwide."
    extracted = extract_text_from_file(content, "agreement.txt")
    assert "Employment Agreement" in extracted

def test_detect_metadata_structure():
    text = "This Agreement is entered into between Acme Corp and Beta LLC on January 15, 2026 under the laws of Delaware."
    metadata = detect_document_metadata(text, "Contract.txt")
    assert "parties" in metadata
    assert "Delaware" in metadata["governing_law"]
    assert metadata["word_count"] > 0

def test_api_analyze_text_payload():
    payload = {
        "text": "The Contractor shall defend, indemnify, and hold harmless the Client against all damages in perpetuity.",
        "filename": "test_contract.txt"
    }
    res = client.post("/api/analyze", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "risk_assessment" in data
    assert "clauses" in data
    assert "annotated_html" in data
