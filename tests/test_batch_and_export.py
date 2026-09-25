"""
LegalLens AI - Batch Due Diligence & Document Export Test Suite.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi.testclient import TestClient
from backend.app import app

client = TestClient(app)

def test_batch_due_diligence_concurrent():
    doc1 = {"filename": "Vendor_A.txt", "text": "VENDOR AGREEMENT. Governed by Delaware law. Uncapped indemnity. 60 days prior written notice."}
    doc2 = {"filename": "Vendor_B.txt", "text": "CONTRACTOR AGREEMENT. Governed by Texas law. 30 days prior written notice."}
    
    res = client.post("/api/analyze-batch", json={"documents": [doc1, doc2]})
    assert res.status_code == 200
    data = res.json()
    assert data["summary"]["total_documents"] == 2
    assert len(data["risk_matrix"]) > 0
    assert len(data["timeline_milestones"]) >= 2
    assert len(data["cross_contract_conflicts"]) >= 1 # Delaware vs Texas jurisdiction fragmentation

def test_export_markdown_endpoint():
    res = client.post("/api/export-markdown", json={
        "text": "CONFIDENTIALITY AGREEMENT. Governed by California law.",
        "filename": "NDA.txt"
    })
    assert res.status_code == 200
    assert "markdown" in res.json()
    assert "LegalLens AI Briefing Report" in res.json()["markdown"]

def test_export_docx_endpoint():
    res = client.post("/api/export-docx", json={
        "text": "LEASE AGREEMENT. Rent is $2500.",
        "filename": "Lease.txt"
    })
    assert res.status_code == 200
    assert len(res.content) > 0

def test_suggested_questions_endpoint():
    res = client.get("/api/suggested-questions")
    assert res.status_code == 200
    data = res.json()
    assert "categories" in data
    assert len(data["categories"]) > 0

def test_sample_detail_endpoint():
    res = client.get("/api/samples/nda_mutual")
    assert res.status_code == 200
    data = res.json()
    assert data["id"] == "nda_mutual"
    assert "text" in data
    assert len(data["text"]) > 100
