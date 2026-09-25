"""
LegalLens AI - Document-Grounded Q&A Engine.
Strictly answers user questions against active contract text with verifiable clause citations.
Firmly and honestly refuses out-of-scope, ungrounded, or general legal advice queries.
"""

import re
from typing import Dict, Any, Optional
from backend.gemini_engine import grounded_qa_with_gemini

COMMON_SUGGESTED_QUESTIONS = [
    {
        "category": "Exit & Termination",
        "questions": [
            "Can I terminate this agreement early, and what are the penalties?",
            "What notice period is required for cancellation or non-renewal?",
            "Is there an automatic renewal clause?"
        ]
    },
    {
        "category": "Financial Commitments",
        "questions": [
            "What are the payment terms and are there late fee penalties?",
            "Are there mandatory ancillary fees or unbundled surcharges?",
            "How and when is the security deposit returned?"
        ]
    },
    {
        "category": "Liability & Legal Protection",
        "questions": [
            "What liabilities or indemnities am I required to assume?",
            "Who owns the work product, pre-existing code, and intellectual property?",
            "Are there non-compete or non-solicitation restrictions?"
        ]
    }
]


def answer_document_question(question: str, document_text: str, document_title: str = "Uploaded Contract", api_key: Optional[str] = None) -> Dict[str, Any]:
    """
    Answers user questions with grounded clause citations or refuses out-of-scope inquiries.
    """
    q_clean = question.strip().lower()
    
    # 1. Try Gemini Generative AI if key is available
    if api_key:
        gemini_ans = grounded_qa_with_gemini(question, document_text, api_key)
        if gemini_ans:
            return gemini_ans

    # 2. Adversarial Prompt Injection & Out-of-Scope Filter
    prompt_injection_terms = [
        "ignore all previous", "system override", "ignore previous instructions", "roleplay", "secret_api_key",
        "system prompt", "jailbreak", "print api key", "bypass"
    ]
    unrelated_keywords = [
        "recipe", "weather", "president", "capital of", "who wrote", "song", "joke", "code a python", "write an essay", "distance between", "chocolate cake"
    ]
    if any(k in q_clean for k in prompt_injection_terms) or any(k in q_clean for k in unrelated_keywords):
        return {
            "is_grounded": False,
            "answer": "This inquiry is unrelated and outside the scope of the provided legal agreement. LegalLens AI strictly provides document-grounded legal information extracted directly from your contract text.",
            "citation": "Out of Scope",
            "excerpt": "",
            "explanation": "No relevant contractual provisions exist in this document regarding this inquiry.",
            "confidence": 0.99
        }

    # 3. Intelligent Grounded Citation Search across Document
    topic_patterns = [
        (
            ["late fee", "late charge", "overdue", "late penalty"],
            r'(?:late charge|late fee|daily penalty|delinquent)[^\n\r]+(?:\n[^\n\r]+)?',
            "Late Charges & Payment Penalties"
        ),
        (
            ["monthly rent", "base rent", "how much is the rent", "rent amount", "pay per month"],
            r'(?:base monthly rent|monthly rent is|compensation|rate of \$)[^\n\r]+',
            "Monthly Rent & Compensation"
        ),
        (
            ["terminate", "termination", "early exit", "cancel the lease", "end the lease", "vacate"],
            r'(?:early termination|termination fee|if tenant vacates|liable for an early termination)[^\n\r]+',
            "Early Termination & Liquidated Damages"
        ),
        (
            ["renew", "renewal", "automatic renewal", "extend"],
            r'(?:automatic renewal|renew for successive|notice of intent not to renew)[^\n\r]+',
            "Renewal & Notice Deadlines"
        ),
        (
            ["pay", "payment", "fee", "invoice", "cost", "price", "surcharge", "net-90"],
            r'(?:monthly rent|compensation|payment terms|invoicing|technology fee|valet trash|net[\s\-]\d+)[^\n\r]+',
            "Payment Obligations & Surcharges"
        ),
        (
            ["indemnif", "liability", "hold harmless", "damage", "sue", "lawsuit", "breach"],
            r'(?:indemnif|hold harmless|limitation of liability|aggregate liability)[^\n\r]+',
            "Liability & Indemnification"
        ),
        (
            ["intellectual property", "ip", "copyright", "ownership", "work for hire", "code"],
            r'(?:intellectual property|work made for hire|pre-existing|background|patents|ownership)[^\n\r]+',
            "Intellectual Property & Ownership"
        ),
        (
            ["non-compete", "non-solicitation", "solicit", "compete", "restrict"],
            r'(?:non[\s\-]compete|non[\s\-]solicitation|shall not directly or indirectly)[^\n\r]+',
            "Restrictive Covenants"
        ),
        (
            ["deposit", "security deposit", "cleaning fee", "refund"],
            r'(?:security deposit|deposit amount|deductions & return)[^\n\r]+',
            "Security Deposit & Deductions"
        ),
        (
            ["guest", "visitor", "pets", "sublet", "occupant"],
            r'(?:guest limitations|pets|unauthorized subtenant|quiet enjoyment)[^\n\r]+',
            "Use, Guests & Property Rules"
        ),
        (
            ["governing law", "jurisdiction", "court", "venue", "dispute", "jury"],
            r'(?:governing law|dispute venue|waiver of jury trial|laws of the State of)[^\n\r]+',
            "Governing Law & Disputes"
        )
    ]

    for keywords, regex_pat, topic_label in topic_patterns:
        if any(k in q_clean for k in keywords):
            match = re.search(regex_pat, document_text, re.I)
            if match:
                raw_excerpt = match.group(0).strip()
                # Clean excerpt length
                excerpt = " ".join(raw_excerpt.split())[:260]
                
                # Dynamic clause header detection near match
                start_pos = match.start()
                preceding_text = document_text[max(0, start_pos - 200):start_pos + 5]
                clause_matches = re.findall(r'^(?:(?:Section|Article|Clause)\s+)?(\d+(?:\.\d+)*)\.?\s+([A-Za-z\s,/\-\(\)]{3,40})$', preceding_text, re.M)
                if clause_matches:
                    last_clause = clause_matches[-1]
                    citation = f"Clause {last_clause[0]}: {last_clause[1].strip().title()}"
                else:
                    citation = f"{topic_label}"

                return {
                    "is_grounded": True,
                    "answer": f"According to {citation}, the agreement specifies: \"{excerpt}\"",
                    "citation": citation,
                    "excerpt": excerpt,
                    "explanation": f"This provision directly addresses {topic_label.lower()} under the governing terms of the agreement.",
                    "confidence": 0.94
                }

    # 4. Fallback keyword scan against all paragraphs
    for line in document_text.split("\n"):
        line_clean = line.strip()
        if len(line_clean) > 40 and any(w in line_clean.lower() for w in q_clean.split() if len(w) > 4):
            return {
                "is_grounded": True,
                "answer": f"The document states: \"{line_clean[:220]}\"",
                "citation": "Document Excerpt",
                "excerpt": line_clean[:220],
                "explanation": "Extracted directly from matching contract text.",
                "confidence": 0.82
            }

    # 5. Honest Refusal when topic is not found
    return {
        "is_grounded": False,
        "answer": f"The active document (\"{document_title}\") does not contain explicit provisions or terms addressing this specific question.",
        "citation": "No Document Match",
        "excerpt": "",
        "explanation": "If this topic is important to your transaction, consider asking your attorney to draft a protective addendum.",
        "confidence": 0.95
    }
