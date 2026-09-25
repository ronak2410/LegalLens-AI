"""
LegalLens AI - Legal NLP & Grounded Q&A Test Suite.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi.testclient import TestClient
from backend.app import app
from backend.samples import SAMPLE_DOCUMENTS
from backend.legal_engine import analyze_document_text, extract_document_clauses
from backend.qa_engine import answer_document_question
from backend.comparator import compare_legal_documents

client = TestClient(app)

def test_samples_catalog():
    res = client.get("/api/samples")
    assert res.status_code == 200
    data = res.json()
    assert len(data["samples"]) == 4

def test_dynamic_clause_segmentation():
    sample_text = """
    AGREEMENT
    1. TERM OF SERVICE
    This agreement lasts 12 months.
    2. PAYMENT OBLIGATIONS
    Client pays $500 monthly.
    3. TERMINATION
    Either party may exit upon 30 days notice.
    """
    clauses = extract_document_clauses(sample_text)
    assert len(clauses) >= 3
    assert clauses[0]["clause_id"] == "Clause 1"

def test_legal_analysis_novel_contract():
    novel_text = """
    CONSULTING AGREEMENT
    Dated August 1, 2026. Between Alpha Corp and Beta LLC.
    1. INDEMNITY: Consultant agrees to hold harmless and indemnify Client from and against any and all claims without limit.
    2. IP ASSIGNMENT: Consultant assigns all rights in all pre-existing tools and background code in perpetuity worldwide.
    3. GOVERNING LAW: Governed by laws of Texas.
    """
    analysis = analyze_document_text(novel_text, "Novel.txt")
    assert analysis["risk_assessment"]["level"] == "High"
    assert analysis["risk_assessment"]["score"] >= 60
    assert len(analysis["risks_and_flags"]) >= 2
    assert len(analysis["redlines"]) >= 1

def test_grounded_qa_citation():
    lease_text = SAMPLE_DOCUMENTS["residential_lease"]["text"]
    res = answer_document_question("Can I terminate the lease early?", lease_text, "Residential Lease")
    assert res["is_grounded"] is True
    assert "Clause" in res["citation"] or "Early Termination" in res["citation"]
    assert len(res["excerpt"]) > 0

def test_grounded_qa_out_of_scope_refusal():
    lease_text = SAMPLE_DOCUMENTS["residential_lease"]["text"]
    res = answer_document_question("What is the recipe for baking chocolate cake?", lease_text, "Residential Lease")
    assert res["is_grounded"] is False
    assert "unrelated" in res["answer"].lower() or "not contain" in res["answer"].lower()

def test_comparator_delta():
    docA = "STANDARD TERMS. Net-30 payment. Mutual 30 days notice."
    docB = "ONE-SIDED TERMS. Net-90 payment. Consultant indemnifies without limit. 24 months non-compete."
    comp = compare_legal_documents(docA, docB, "Doc A", "Doc B")
    assert comp["score_delta"] > 0
    assert "Higher Risk" in comp["risk_shift_title"]
