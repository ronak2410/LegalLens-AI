"""
LegalLens AI - Side-by-Side Legal Document Comparator.
Performs semantic and risk comparison between two contract drafts or versions,
calculates the risk score delta, and highlights favorable/unfavorable clause shifts.
"""

from typing import Dict, Any
from backend.legal_engine import analyze_document_text

def compare_legal_documents(doc1_text: str, doc2_text: str, doc1_name: str = "Document A", doc2_name: str = "Document B") -> Dict[str, Any]:
    """
    Compares two contracts side-by-side and returns a structured comparison matrix.
    """
    analysis1 = analyze_document_text(doc1_text, doc1_name)
    analysis2 = analyze_document_text(doc2_text, doc2_name)
    
    score1 = analysis1["risk_assessment"]["score"]
    score2 = analysis2["risk_assessment"]["score"]
    delta = score2 - score1
    
    if delta > 15:
        risk_shift_title = f"Substantially Higher Risk in {doc2_name} (+{delta} pts)"
        risk_shift_badge = "unfavorable"
        risk_shift_summary = f"{doc1_name} carries {analysis1['risk_assessment']['level']} risk ({score1}/100) whereas {doc2_name} introduces {analysis2['risk_assessment']['level']} risk ({score2}/100) with new unilateral obligations."
    elif delta < -15:
        risk_shift_title = f"Significantly More Protective in {doc2_name} ({delta} pts)"
        risk_shift_badge = "favorable"
        risk_shift_summary = f"{doc2_name} reduces risk from {score1}/100 down to {score2}/100 with more balanced terms."
    else:
        risk_shift_title = f"Comparable Risk Profile ({delta:+d} pts)"
        risk_shift_badge = "neutral"
        risk_shift_summary = f"Both documents share similar risk exposure ({score1}/100 vs {score2}/100)."

    # Standardized Category Matrix
    categories = [
        ("Financial & Payment", "payment"),
        ("Liability & Indemnity", "liability"),
        ("Term & Termination", "termination"),
        ("Intellectual Property", "ip"),
        ("Restrictive Covenants", "covenant"),
        ("Dispute Resolution", "dispute")
    ]
    
    matrix = []
    for cat_label, cat_key in categories:
        flags1 = [f["title"] for f in analysis1["risks_and_flags"] if cat_key in f["category"].lower()]
        flags2 = [f["title"] for f in analysis2["risks_and_flags"] if cat_key in f["category"].lower()]
        
        status = "Identical"
        if len(flags2) > len(flags1):
            status = "Unfavorable Shift"
        elif len(flags1) > len(flags2):
            status = "Favorable Protection"
        elif flags1 != flags2 and (flags1 or flags2):
            status = "Modified Terms"
            
        matrix.append({
            "category": cat_label,
            "doc1_summary": "; ".join(flags1) if flags1 else "Standard / No major flags",
            "doc2_summary": "; ".join(flags2) if flags2 else "Standard / No major flags",
            "status": status
        })

    return {
        "doc1_name": doc1_name,
        "doc2_name": doc2_name,
        "doc1_score": score1,
        "doc2_score": score2,
        "score_delta": delta,
        "risk_shift_title": risk_shift_title,
        "risk_shift_badge": risk_shift_badge,
        "risk_shift_summary": risk_shift_summary,
        "comparison_matrix": matrix
    }
