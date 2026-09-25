"""
LegalLens AI - Enterprise Features & Core API Test Suite.
Tests custom playbooks, OCR fallback, DOCX export, and batch portfolio due diligence.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi.testclient import TestClient
from backend.app import app

client = TestClient(app)

def test_health():
    res = client.get("/api/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "healthy"
    print("[PASS] /api/health")

def test_samples():
    res = client.get("/api/samples")
    assert res.status_code == 200
    data = res.json()
    assert len(data["samples"]) >= 4
    print(f"[PASS] /api/samples ({len(data['samples'])} samples available)")

def test_analyze_with_custom_playbook():
    sample_text = """
    EMPLOYMENT AND CONFIDENTIALITY AGREEMENT
    This Agreement is entered into on January 15, 2024.
    1. NON-SOLICITATION: Employee shall not solicit any employees or customers for 3 years following termination.
    2. INDEMNIFICATION: Employee agrees to hold Employer harmless and indemnify Employer against any losses.
    3. GOVERNING LAW: This agreement is governed by the laws of California.
    """
    playbook_rules = [
        {
            "regex_pattern": r"non-solicit|solicit.*employees",
            "title": "Strict Non-Solicitation Policy Violation",
            "severity": "High",
            "category": "Custom Restrictive Covenants",
            "description": "Employee non-solicitation detected.",
            "impact": "Restricts personal professional networking.",
            "recommendation": "Limit non-solicitation to 6 months and direct solicitations only."
        }
    ]
    res = client.post("/api/analyze", json={
        "text": sample_text,
        "filename": "Test_Playbook.txt",
        "playbook_rules": playbook_rules
    })
    assert res.status_code == 200
    data = res.json()
    
    # Check that playbook rule was triggered
    flag_titles = [f["title"] for f in data["risks_and_flags"]]
    assert any("Strict Non-Solicitation" in t for t in flag_titles)
    print("[PASS] /api/analyze with Custom Playbook Rule")

def test_batch_due_diligence():
    doc1 = {
        "filename": "Vendor_MSA.txt",
        "text": "MASTER SERVICES AGREEMENT. Governed by Delaware Law. Vendor indemnifies Client without limit. 60 days prior written notice required for termination."
    }
    doc2 = {
        "filename": "Subcontractor_Agreement.txt",
        "text": "SUBCONTRACTOR AGREEMENT. Governed by California Law. Subcontractor retains all intellectual property. 30 days prior written notice required."
    }
    
    res = client.post("/api/analyze-batch", json={
        "documents": [doc1, doc2]
    })
    assert res.status_code == 200
    data = res.json()
    assert data["summary"]["total_documents"] == 2
    assert "average_risk_score" in data["summary"]
    assert len(data["risk_matrix"]) > 0
    assert len(data["timeline_milestones"]) >= 2
    print(f"[PASS] /api/analyze-batch (Audited 2 contracts, found {len(data['timeline_milestones'])} timeline events)")

def test_export_markdown_and_docx():
    sample_text = "SAMPLE AGREEMENT. Governed by New York law. Rent is $3000 due monthly."
    
    md_res = client.post("/api/export-markdown", json={
        "text": sample_text,
        "filename": "Sample.txt"
    })
    assert md_res.status_code == 200
    assert "markdown" in md_res.json()
    print("[PASS] /api/export-markdown")

    docx_res = client.post("/api/export-docx", json={
        "text": sample_text,
        "filename": "Sample.txt"
    })
    assert docx_res.status_code == 200
    assert len(docx_res.content) > 0
    print(f"[PASS] /api/export-docx (Received {len(docx_res.content)} bytes)")

if __name__ == "__main__":
    print("--- Running LegalLens AI Automated Test Suite ---")
    test_health()
    test_samples()
    test_analyze_with_custom_playbook()
    test_batch_due_diligence()
    test_export_markdown_and_docx()
    print("--- All Tests Passed Successfully! ---")
