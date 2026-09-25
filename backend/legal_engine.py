"""
LegalLens AI - Generalized Legal NLP Analysis Engine.
Extracts clauses, identifies risk asymmetries, detects financial obligations,
generates actionable plain-language takeaways, in-line highlights, and lawyer questions
for ANY arbitrary legal agreement (leases, contractor MSAs, NDAs, SaaS terms, vendor notices).
"""

import re
import html
import json
import hashlib
from typing import List, Dict, Any, Optional, Tuple
from backend.redline_engine import get_applicable_redlines
from backend.gemini_engine import summarize_contract_with_gemini

# In-Memory Analysis Hash Cache for sub-millisecond repeated evaluations
_ANALYSIS_CACHE: Dict[str, Dict[str, Any]] = {}


# Core Risk Patterns & Categories
STANDARD_RULES = [
    {
        "category": "Liability & Indemnification",
        "patterns": [
            r"indemnif(?:y|ies|ication).*?(?:unlimited|uncapped|without limit|sole|all claims|harmless)",
            r"uncapped\s+(?:indemnity|liability)",
            r"hold harmless.*?(?:from and against any and all)",
            r"limitation of liability.*?(?:preceding 30 days|zero|\$0|negligence)",
            r"waive(?:s|d)?.*?(?:jury trial|class action|any and all claims)"
        ],
        "severity": "Critical",
        "title": "Unilateral or Uncapped Indemnification & Liability Asymmetry",
        "impact": "Exposes you to unlimited third-party damages or severely caps the other party's financial accountability to minimal amounts.",
        "recommendation": "Request a mutual liability cap tied to 12 months' total contract value, and limit indemnities strictly to gross negligence or direct breach."
    },
    {
        "category": "Intellectual Property",
        "patterns": [
            r"assign(?:s|ment)?.*?(?:all rights|pre-existing|background|perpetuity|worldwide)",
            r"work(?:s)? made for hire.*?(?:all discoveries|inventions|patents)",
            r"waives all moral rights"
        ],
        "severity": "High",
        "title": "Broad Intellectual Property Overreach & Pre-Existing Code Loss",
        "impact": "You may inadvertently assign ownership of your background tools, personal boilerplates, or unrelated open-source code.",
        "recommendation": "Explicitly carve out 'Background & Pre-Existing IP', granting the counterparty a non-exclusive license rather than full ownership assignment."
    },
    {
        "category": "Term & Renewal Traps",
        "patterns": [
            r"automatic(?:ally)? renew(?:s|al)?.*?(?:60|90)\s+days",
            r"failure to deliver.*?(?:notice).*?(?:administrative surcharge|automatic.*renewal)",
            r"early termination.*?(?:forfeiture|penalty|liquidated damages|two \(2\) months)"
        ],
        "severity": "High",
        "title": "Automatic Renewal Trap & Severe Early Termination Penalties",
        "impact": "Missing a narrow notice window (e.g., 60 days before expiration) can legally lock you into an unwanted multi-month renewal with surcharges.",
        "recommendation": "Require the counterparty to provide an advance written reminder 30 days prior to the renewal deadline, and reduce early exit fees to 1 month with mitigation."
    },
    {
        "category": "Payment & Invoicing",
        "patterns": [
            r"net[\s\-]90",
            r"withhold up to.*?(?:50%|dispute)",
            r"late charge.*?(?:immediate|daily penalty|\$125)",
            r"mandatory.*?(?:technology fee|maintenance fee|surcharge)"
        ],
        "severity": "Medium",
        "title": "Extended Payment Terms (Net-90) & Mandatory Surcharges",
        "impact": "Delays cash collection for up to 3 months or introduces unbundled ancillary monthly fees beyond base pricing.",
        "recommendation": "Negotiate standard Net-30 payment terms and require detailed itemization before any invoice dispute withholdings are made."
    },
    {
        "category": "Restrictive Covenants",
        "patterns": [
            r"non[\s\-]compete.*?(?:24|12|twelve|twenty-four)\s+months",
            r"(?:24|12|twelve|twenty-four)\s+months?\s+non[\s\-]compete",
            r"not directly or indirectly.*?(?:provide.*services|compete)",
            r"non[\s\-]solicitation.*?(?:personnel|employees|clients)"
        ],
        "severity": "High",
        "title": "Post-Termination Non-Compete & Earning Restrictions",
        "impact": "Severely limits your freedom to accept contracts, work in your industry, or take on freelance clients after contract conclusion.",
        "recommendation": "Strike the non-compete clause entirely, or narrow it to specific named direct competitors with a maximum 6-month duration."
    },
    {
        "category": "Dispute Resolution & Jurisdiction",
        "patterns": [
            r"waiver of jury trial",
            r"governed by.*?laws of.*?(?:delaware|texas|california|new york)",
            r"reimbursed by.*?legal fees"
        ],
        "severity": "Low",
        "title": "Governing Jurisdiction & Dispute Venue Specifications",
        "impact": "Specifies which state's laws control disputes and which courts hold jurisdiction if formal litigation arises.",
        "recommendation": "Verify whether the chosen state requires costly travel or out-of-state legal counsel in the event of a dispute."
    }
]


def safe_regex_search(pattern: str, text: str, max_pattern_len: int = 120) -> Optional[re.Match]:
    """Safely compiles and searches regex with ReDoS length bounds."""
    if not pattern or len(pattern) > max_pattern_len:
        return None
    try:
        regex = re.compile(pattern, re.IGNORECASE | re.MULTILINE)
        return regex.search(text)
    except Exception:
        return None


def extract_document_clauses(text: str) -> List[Dict[str, Any]]:
    """
    Dynamically segments arbitrary contract text into numbered clauses, articles, or sections.
    Does not rely on hardcoded section titles.
    """
    lines = text.split("\n")
    clauses = []
    current_clause = None
    
    header_pattern = re.compile(r'^(?:(?:Section|Article|Clause)\s+)?(\d+(?:\.\d+)*|[A-Z]+)\.?\s+([A-Z\s,/\-\(\)]{3,50})$', re.I)

    for line_idx, raw_line in enumerate(lines):
        line = raw_line.strip()
        if not line:
            continue
            
        match = header_pattern.match(line)
        if match:
            if current_clause and current_clause["body"].strip():
                clauses.append(current_clause)
                
            num = match.group(1)
            title = match.group(2).strip()
            current_clause = {
                "clause_id": f"Clause {num}",
                "title": title.title(),
                "body": "",
                "start_line": line_idx + 1
            }
        else:
            if current_clause:
                current_clause["body"] += (" " + line) if current_clause["body"] else line
            else:
                if len(line) > 30 and not line.isupper():
                    current_clause = {
                        "clause_id": "Preamble",
                        "title": "Recitals & Background",
                        "body": line,
                        "start_line": 1
                    }
                
    if current_clause and current_clause["body"].strip():
        clauses.append(current_clause)
        
    return clauses if clauses else [{
        "clause_id": "Section 1",
        "title": "General Agreement Terms",
        "body": text[:3000],
        "start_line": 1
    }]


def detect_document_metadata(text: str, filename: str) -> Dict[str, Any]:
    """Extracts title, parties, effective date, governing law, and document type from text."""
    date_match = re.search(r'(?:effective|entered into|dated|made).*?(?:this\s+)?(\d{1,2}(?:st|nd|rd|th)?\s+(?:day of\s+)?[A-Za-z]+\s*,?\s*\d{4}|[A-Za-z]+\s+\d{1,2},?\s*\d{4})', text, re.I)
    effective_date = date_match.group(1) if date_match else "Current Session"
    
    # Flexible governing law matching
    gov_match = re.search(r'(?:laws of (?:the State of\s+)?|governed by (?:the laws of\s+)?(?:the State of\s+)?)([A-Za-z\s]+?)(?:\s+law|\.|\,|;|\sand\b)', text, re.I)
    governing_law = gov_match.group(1).strip() if gov_match else "Not explicitly stated"
    if governing_law.lower().endswith(" law"):
        governing_law = governing_law[:-4].strip()
    
    # Detect document type
    text_lower = text[:500].lower()
    if "lease" in text_lower or "tenant" in text_lower:
        doc_type = "Residential Lease Agreement"
        title = "Residential Lease Agreement"
    elif "freelance" in text_lower or "contractor" in text_lower or "master services" in text_lower:
        doc_type = "Independent Contractor Agreement"
        title = "Freelance Services Agreement"
    elif "non-disclosure" in text_lower or "confidentiality" in text_lower:
        doc_type = "Non-Disclosure Agreement (NDA)"
        title = "Mutual Non-Disclosure Agreement"
    elif "software" in text_lower or "cloud" in text_lower or "saas" in text_lower:
        doc_type = "Software-as-a-Service (SaaS) Agreement"
        title = "Enterprise SaaS Terms of Service"
    else:
        doc_type = "Commercial Contract"
        title = filename.replace(".txt", "").replace(".pdf", "").replace(".docx", "").replace("_", " ")

    # Detect parties
    party_matches = re.findall(r'between\s+([A-Za-z0-9\s,\.]+?)\s*(?:\(|"|and)\s+(?:and|,)\s+([A-Za-z0-9\s,\.]+?)(?:\.|\(|"|\n)', text[:800], re.I)
    parties = [party_matches[0][0].strip(), party_matches[0][1].strip()] if party_matches else ["Disclosing Party / Landlord / Client", "Receiving Party / Tenant / Contractor"]

    return {
        "title": title,
        "doc_type": doc_type,
        "parties": parties,
        "effective_date": effective_date,
        "governing_law": governing_law,
        "word_count": len(text.split())
    }


def analyze_document_text(text: str, filename: str = "Document.txt", playbook_rules: Optional[List[Dict[str, Any]]] = None, api_key: Optional[str] = None) -> Dict[str, Any]:
    """
    Main analysis pipeline.
    Combines rule-based legal heuristic evaluation with optional Google Gemini enhancement.
    """
    # 1. Check in-memory hash cache
    pb_str = json.dumps(playbook_rules, sort_keys=True) if playbook_rules else ""
    cache_key = hashlib.sha256(f"{text[:15000]}|{filename}|{pb_str}|{bool(api_key)}".encode('utf-8')).hexdigest()
    if not api_key and cache_key in _ANALYSIS_CACHE:
        return dict(_ANALYSIS_CACHE[cache_key])

    # Check if Gemini key is present for real generative AI capabilities
    if api_key:
        gemini_result = summarize_contract_with_gemini(text, api_key)
        if gemini_result:
            metadata = detect_document_metadata(text, filename)
            gemini_result["metadata"] = metadata
            flagged_cats = [r.get("category", "") for r in gemini_result.get("risks_and_flags", [])]
            gemini_result["redlines"] = get_applicable_redlines(flagged_cats)
            gemini_result["annotated_html"] = generate_annotated_html(text, gemini_result.get("risks_and_flags", []))
            return gemini_result

    metadata = detect_document_metadata(text, filename)
    clauses = extract_document_clauses(text)
    
    # Evaluate risks
    risks_and_flags = []
    category_counts = {}
    total_risk_score = 15 # baseline nominal score
    
    # 1. Evaluate standard rules
    for rule in STANDARD_RULES:
        for pat in rule["patterns"]:
            match = safe_regex_search(pat, text)
            if match:
                # Find matching clause reference
                matched_span = match.group(0)
                clause_ref = "General Agreement"
                for cl in clauses:
                    if matched_span in cl["body"] or match.start() >= cl.get("start_pos", 0):
                        clause_ref = f"{cl['clause_id']}: {cl['title']}"
                        break
                        
                severity = rule["severity"]
                score_weight = 25 if severity == "Critical" else 15 if severity == "High" else 8
                total_risk_score += score_weight
                
                risks_and_flags.append({
                    "title": rule["title"],
                    "severity": severity,
                    "category": rule["category"],
                    "clause_ref": clause_ref,
                    "impact": rule["impact"],
                    "recommendation": rule["recommendation"],
                    "excerpt": matched_span[:200]
                })
                category_counts[rule["category"]] = category_counts.get(rule["category"], 0) + 1
                break

    # 2. Evaluate user-supplied custom playbook rules (with ReDoS safety)
    if playbook_rules:
        for pb_rule in playbook_rules:
            pat = pb_rule.get("regex_pattern", "")
            match = safe_regex_search(pat, text, max_pattern_len=120)
            if match:
                sev = pb_rule.get("severity", "High")
                total_risk_score += (25 if sev == "Critical" else 15 if sev == "High" else 8)
                risks_and_flags.append({
                    "title": f"[Playbook Rule] {pb_rule.get('title', 'Custom Rule Match')}",
                    "severity": sev,
                    "category": pb_rule.get("category", "Custom Playbook"),
                    "clause_ref": "Document Match",
                    "impact": pb_rule.get("impact", "Custom playbook violation detected."),
                    "recommendation": pb_rule.get("recommendation", "Review and adjust terms according to internal playbook standards."),
                    "excerpt": match.group(0)[:200]
                })

    # Normalized risk score (0-100)
    final_score = min(max(total_risk_score, 10), 98)
    risk_level = "High" if final_score >= 60 else "Medium" if final_score >= 35 else "Low"

    # Executive Plain-Language Summary
    plain_summary = [
        {
            "title": "Commercial & Financial Commitments",
            "simple_explanation": f"Document establishes obligations for {metadata['parties'][0]} and {metadata['parties'][1]}. Governed under {metadata['governing_law']} jurisdiction.",
            "what_to_do": "Ensure all payment schedules, fee items, and notice deadlines match what was verbally negotiated."
        },
        {
            "title": "Liability & Legal Protection Balance",
            "simple_explanation": f"The agreement exhibits a {risk_level.lower()} risk profile with {len(risks_and_flags)} identified risk points.",
            "what_to_do": "Review redline counter-language to ensure mutual protection rather than unilateral liability exposure."
        }
    ]

    # Pre-Signing Action Checklist
    checklist = [
        {"label": f"Verify legal entity names for {metadata['parties'][0]} and {metadata['parties'][1]}", "priority": "Standard"},
        {"label": f"Confirm governing jurisdiction in {metadata['governing_law']} is acceptable", "priority": "Standard"},
        {"label": "Review proposed redline counter-clauses before signing", "priority": "High"}
    ]
    if any(r["severity"] in ["Critical", "High"] for r in risks_and_flags):
        checklist.insert(0, {"label": "Consult with a licensed attorney regarding critical indemnification/IP clauses", "priority": "Urgent"})

    # Lawyer Questions
    lawyer_questions = [
        f"Does the {metadata['governing_law']} governing law clause restrict our legal remedies?",
        "Are the indemnification obligations mutual and commercially standard?",
        "What are our exit rights if the other party fails to deliver or breaches terms?",
        "Are there any hidden renewal notice deadlines or liquidated damage liabilities?"
    ]

    # Applicable redlines
    flagged_cats = list(category_counts.keys())
    redlines = get_applicable_redlines(flagged_cats)

    # Annotated HTML Viewer
    annotated_html = generate_annotated_html(text, risks_and_flags)

    result = {
        "metadata": metadata,
        "risk_assessment": {
            "score": final_score,
            "level": risk_level,
            "description": f"Analysis detected {len(risks_and_flags)} notable provisions requiring attention."
        },
        "plain_language_summary": plain_summary,
        "risks_and_flags": risks_and_flags,
        "redlines": redlines,
        "checklist": checklist,
        "lawyer_questions": lawyer_questions,
        "clauses": clauses[:25],
        "annotated_html": annotated_html
    }

    # Store in cache (cap at 500 entries)
    if not api_key:
        if len(_ANALYSIS_CACHE) > 500:
            _ANALYSIS_CACHE.clear()
        _ANALYSIS_CACHE[cache_key] = result

    return result


def generate_annotated_html(text: str, flags: List[Dict[str, Any]]) -> str:
    """Creates safe, XSS-sanitized HTML with color-coded risk highlights."""
    escaped_text = html.escape(text)
    
    # Highlight flagged terms safely
    for flag in flags:
        excerpt = flag.get("excerpt", "").strip()
        if excerpt and len(excerpt) >= 8:
            escaped_excerpt = html.escape(excerpt)
            sev = flag.get("severity", "Medium").lower()
            css_class = "highlight-critical" if sev == "critical" else "highlight-high" if sev == "high" else "highlight-medium"
            title_attr = html.escape(f"[{flag.get('severity')}] {flag.get('title')}: {flag.get('impact')}")
            
            # Safe replacement
            replacement = f'<mark class="{css_class}" tabindex="0" aria-label="{title_attr}" title="{title_attr}">{escaped_excerpt}</mark>'
            escaped_text = escaped_text.replace(escaped_excerpt, replacement)

    # Wrap paragraphs cleanly
    paragraphs = escaped_text.split("\n\n")
    formatted_html = "".join([f"<p style='margin-bottom: 12px; line-height: 1.6;'>{p.replace(chr(10), '<br>')}</p>" for p in paragraphs if p.strip()])
    return formatted_html
