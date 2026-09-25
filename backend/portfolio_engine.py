"""
LegalLens AI - Concurrent Portfolio Due Diligence Engine.
Concurrently analyzes contract batches, detects cross-document contradictions,
compiles risk heatmaps, extracts unified timelines, and generates consolidated action checklists.
"""

import re
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict, Any, Optional
from backend.legal_engine import analyze_document_text

def analyze_single_doc(item: Dict[str, Any], playbook_rules: Optional[List[Dict[str, Any]]]) -> Dict[str, Any]:
    text = item.get("text", "")
    filename = item.get("filename", "Contract.txt")
    res = analyze_document_text(text, filename, playbook_rules)
    res["filename"] = filename
    return res

def analyze_portfolio_documents(documents: List[Dict[str, Any]], playbook_rules: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
    """
    Analyzes multiple contracts concurrently as a single due diligence portfolio.
    """
    if not documents:
        return {}

    # Run analysis concurrently across threads for high efficiency
    with ThreadPoolExecutor(max_workers=min(len(documents), 8)) as executor:
        individual_analyses = list(executor.map(lambda d: analyze_single_doc(d, playbook_rules), documents))

    total_score = 0
    risk_distribution = {"Critical": 0, "High": 0, "Medium": 0, "Low": 0}
    all_categories = {}
    unified_timeline = []
    unified_checklist = []
    jurisdictions = []
    
    for analysis in individual_analyses:
        meta = analysis.get("metadata", {})
        risk = analysis.get("risk_assessment", {})
        filename = analysis.get("filename", "Contract")
        doc_title = meta.get("title", filename)
        
        # Risk aggregation
        score = risk.get("score", 0)
        total_score += score
        level = risk.get("level", "Low")
        if level in risk_distribution:
            risk_distribution[level] += 1
            
        # Jurisdiction aggregation
        law = meta.get("governing_law")
        if law and law != "Not explicitly stated":
            jurisdictions.append({"contract": doc_title, "law": law})
            
        # Timeline extraction
        effective = meta.get("effective_date")
        if effective and effective != "Not specified":
            unified_timeline.append({
                "contract": doc_title,
                "event": "Contract Effective Date",
                "date_detail": effective,
                "type": "effective",
                "urgency": "Info"
            })
            
        # Scan for notice windows
        for cl in analysis.get("clauses", []):
            cl_body = cl.get("body", "")
            notice_match = re.search(r'(\d+)\s+(?:days?|calendar days?)\s+prior\s+(?:written\s+)?notice', cl_body, re.I)
            if notice_match:
                days = notice_match.group(1)
                unified_timeline.append({
                    "contract": doc_title,
                    "event": f"Termination / Non-Renewal Notice Deadline ({days} days prior)",
                    "date_detail": f"{days} days advance notice required before expiration/renewal",
                    "type": "renewal_deadline",
                    "urgency": "Action Required" if int(days) >= 30 else "Standard"
                })
                break
                
        # Checklist items
        for chk in analysis.get("checklist", []):
            unified_checklist.append({
                "contract": doc_title,
                "label": chk.get("label"),
                "priority": chk.get("priority", "Medium"),
                "category": chk.get("category", "General")
            })
            
        # Category heatmap
        for flag in analysis.get("risks_and_flags", []):
            cat = flag.get("category", "General Risk")
            if cat not in all_categories:
                all_categories[cat] = {
                    "total_flags": 0,
                    "critical_high_count": 0,
                    "affected_contracts": set(),
                    "flags": []
                }
            all_categories[cat]["total_flags"] += 1
            if flag.get("severity") in ["Critical", "High"]:
                all_categories[cat]["critical_high_count"] += 1
            all_categories[cat]["affected_contracts"].add(doc_title)
            all_categories[cat]["flags"].append({
                "contract": doc_title,
                "title": flag.get("title"),
                "severity": flag.get("severity"),
                "impact": flag.get("impact"),
                "recommendation": flag.get("recommendation")
            })

    doc_count = len(documents)
    avg_score = round(total_score / max(doc_count, 1), 1)
    
    if avg_score >= 60:
        portfolio_status = "High Risk Exposure"
        portfolio_badge = "critical"
    elif avg_score >= 35:
        portfolio_status = "Moderate Risk Exposure"
        portfolio_badge = "warning"
    else:
        portfolio_status = "Healthy / Low Risk Exposure"
        portfolio_badge = "healthy"
        
    # Cross-document Conflict Detection
    conflicts = []
    unique_laws = {j["law"] for j in jurisdictions}
    if len(unique_laws) > 1:
        conflicts.append({
            "type": "Jurisdictional Fragmentation",
            "description": f"Portfolio spans {len(unique_laws)} distinct governing laws ({', '.join(unique_laws)}), increasing multi-jurisdictional compliance and litigation complexity.",
            "severity": "Medium",
            "impacted_contracts": [j["contract"] for j in jurisdictions]
        })
        
    indemnity_heavy = [doc["metadata"]["title"] for doc in individual_analyses if any("indemn" in f["title"].lower() and f["severity"] in ["High", "Critical"] for f in doc.get("risks_and_flags", []))]
    if len(indemnity_heavy) >= 2:
        conflicts.append({
            "type": "Compound Indemnity & Liability Concentration",
            "description": f"{len(indemnity_heavy)} contracts contain high-risk uncapped or one-sided indemnity clauses ({', '.join(indemnity_heavy)}), creating compounding financial exposure across the portfolio.",
            "severity": "High",
            "impacted_contracts": indemnity_heavy
        })
        
    # Serialize risk matrix
    serialized_matrix = []
    for cat_name, cat_data in all_categories.items():
        serialized_matrix.append({
            "category": cat_name,
            "total_flags": cat_data["total_flags"],
            "critical_high_count": cat_data["critical_high_count"],
            "affected_contracts": list(cat_data["affected_contracts"]),
            "flags": cat_data["flags"]
        })
    serialized_matrix.sort(key=lambda x: (x["critical_high_count"], x["total_flags"]), reverse=True)
    
    return {
        "summary": {
            "total_documents": doc_count,
            "average_risk_score": avg_score,
            "portfolio_status": portfolio_status,
            "portfolio_badge": portfolio_badge,
            "risk_distribution": risk_distribution,
            "total_risk_flags": sum(c["total_flags"] for c in serialized_matrix)
        },
        "individual_analyses": individual_analyses,
        "risk_matrix": serialized_matrix,
        "timeline_milestones": unified_timeline,
        "cross_contract_conflicts": conflicts,
        "unified_checklist": sorted(unified_checklist, key=lambda x: (0 if x["priority"] == "Urgent" else 1 if x["priority"] == "High" else 2))
    }
