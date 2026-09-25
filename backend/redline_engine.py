"""
LegalLens AI - Clause Redline & Counter-Language Engine.
Provides standard, balanced, and tenant/contractor-protective replacement clauses
with actionable rationale to empower users during contract negotiations.
"""

from typing import List, Dict, Any

REDLINE_CATALOG = {
    "unlimited_indemnity": {
        "title": "Mutual & Capped Indemnification",
        "category": "Liability & Indemnity",
        "description": "Replaces unilateral, uncapped indemnity with a standard mutual indemnification capped at total fees paid.",
        "proposed_clause": (
            "Each party ('Indemnifying Party') shall indemnify, defend, and hold harmless the other party "
            "from and against third-party claims arising solely out of the Indemnifying Party's gross negligence, "
            "willful misconduct, or material breach of this Agreement. In no event shall either party's cumulative "
            "indemnity liability exceed the total amounts paid or payable under this Agreement in the preceding twelve (12) months."
        ),
        "rationale": "Protects individuals and service providers from existential liability by placing a commercially standard monetary ceiling and ensuring mutuality."
    },
    "ip_overreach": {
        "title": "Protection of Pre-Existing & Background IP",
        "category": "Intellectual Property",
        "description": "Carves out contractor background code, developer tools, and pre-existing frameworks while granting client full license.",
        "proposed_clause": (
            "Contractor assigns to Client all right, title, and interest in custom deliverables created specifically "
            "for Client under an applicable Statement of Work upon receipt of full payment. Contractor retains all right, "
            "title, and ownership in Contractor's pre-existing code, tools, frameworks, and background intellectual property, "
            "granting Client a perpetual, worldwide, royalty-free license to use such background IP solely as integrated into the deliverables."
        ),
        "rationale": "Prevents accidental forfeiture of personal tools, boilerplates, and open-source libraries."
    },
    "auto_renewal_trap": {
        "title": "Fair Notice for Automatic Renewal",
        "category": "Term & Termination",
        "description": "Requires landlord or vendor to deliver written reminder 30 days prior to renewal deadline, avoiding accidental lock-in.",
        "proposed_clause": (
            "This Agreement shall renew only upon mutual written agreement, or automatically only if Provider delivers "
            "written notice reminding Customer of upcoming renewal between forty-five (45) and thirty (30) days prior to the expiration date. "
            "Customer may elect not to renew at any time up to fifteen (15) days prior to term conclusion without penalty or surcharge."
        ),
        "rationale": "Prevents silent automatic renewals and punitive administrative surcharges."
    },
    "harsh_early_termination": {
        "title": "Commercially Reasonable Early Termination",
        "category": "Term & Termination",
        "description": "Replaces full forfeiture of deposits and punitive multi-month liquidated damages with reasonable 30-day notice and fee mitigation.",
        "proposed_clause": (
            "Tenant may terminate this Lease prior to the expiration date by providing thirty (30) days' prior written notice "
            "and paying an early re-letting fee equal to one (1) month's base rent. Landlord shall make commercially reasonable efforts "
            "to mitigate damages by promptly marketing the unit. Security deposits shall remain subject only to legitimate physical repair deductions."
        ),
        "rationale": "Alleviates severe liquidated damage burdens and aligns with statutory duty of landlord mitigation."
    },
    "net_90_payment": {
        "title": "Standard Net-30 Payment & Dispute Clause",
        "category": "Payment Terms",
        "description": "Shortens payment terms from 90 days to 30 days and limits dispute withholdings strictly to disputed line items.",
        "proposed_clause": (
            "Client shall pay all undisputed invoice amounts within thirty (30) calendar days of invoice receipt ('Net-30'). "
            "If Client disputes any portion of an invoice in good faith, Client shall pay the undisputed balance on schedule "
            "and provide detailed written justification for the disputed item within fourteen (14) days."
        ),
        "rationale": "Ensures predictable cash flow for freelancers and small businesses and prevents entire invoices from being held hostage."
    },
    "broad_non_compete": {
        "title": "Narrowed Non-Solicitation & No Non-Compete",
        "category": "Restrictive Covenants",
        "description": "Strikes overly broad non-competes in favor of narrow non-solicitation of active clients/staff.",
        "proposed_clause": (
            "During the term of this Agreement and for a period of six (6) months thereafter, Contractor agrees not to directly "
            "solicit any active employee of Client with whom Contractor worked directly. Contractor remains free to provide software "
            "engineering and consulting services to any other clients or industries without geographic restriction."
        ),
        "rationale": "Preserves contractor's livelihood and freedom to work while respecting legitimate client relationships."
    }
}


def get_applicable_redlines(flagged_categories: List[str]) -> List[Dict[str, Any]]:
    """Returns curated counter-language redlines matching the identified contract risks."""
    results = []
    category_map = {
        "indemnity": "unlimited_indemnity",
        "liability": "unlimited_indemnity",
        "intellectual property": "ip_overreach",
        "ip": "ip_overreach",
        "renewal": "auto_renewal_trap",
        "termination": "harsh_early_termination",
        "payment": "net_90_payment",
        "non-compete": "broad_non_compete",
        "covenant": "broad_non_compete"
    }
    
    seen_keys = set()
    for cat in flagged_categories:
        cat_lower = cat.lower()
        for keyword, key in category_map.items():
            if keyword in cat_lower and key not in seen_keys:
                seen_keys.add(key)
                item = REDLINE_CATALOG[key].copy()
                item["id"] = key
                results.append(item)
                
    # If no specific match, provide general fair balance redlines
    if not results:
        results.append(REDLINE_CATALOG["unlimited_indemnity"])
        results.append(REDLINE_CATALOG["auto_renewal_trap"])
        
    return results
