"""
LegalLens AI - Security, Parser, and ReDoS Test Suite.
"""

import sys
import pytest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi.testclient import TestClient
from backend.app import app
from backend.parser import extract_text_from_file, MAX_FILE_SIZE_BYTES
from backend.legal_engine import safe_regex_search, analyze_document_text

client = TestClient(app)

def test_file_size_limit_rejection():
    # Attempting to parse bytes exceeding 15MB
    large_bytes = b"A" * (MAX_FILE_SIZE_BYTES + 1024)
    with pytest.raises(ValueError) as exc:
        extract_text_from_file(large_bytes, "Huge.txt")
    assert "exceeds maximum allowable size" in str(exc.value)

def test_redos_pattern_safety():
    # Long or nested dangerous regex patterns
    evil_pattern = "a" * 200 # Exceeds max_pattern_len
    res = safe_regex_search(evil_pattern, "sample text")
    assert res is None

def test_xss_sanitization_in_html():
    malicious_text = "<script>alert('xss')</script> This contract requires Net-90 payment."
    analysis = analyze_document_text(malicious_text, "Malicious.txt")
    assert "<script>" not in analysis["annotated_html"]
    assert "&lt;script&gt;" in analysis["annotated_html"]

def test_security_headers_enforced():
    res = client.get("/api/health")
    assert res.status_code == 200
    assert res.headers["X-Content-Type-Options"] == "nosniff"
    assert res.headers["X-Frame-Options"] == "DENY"
    assert "Content-Security-Policy" in res.headers
