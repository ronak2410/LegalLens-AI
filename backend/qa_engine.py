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

    # 2. Out-of-Scope / General Trivia filter
    unrelated_keywords = [
        "recipe", "weather", "president", "capital of", "who wrote", "song", "joke", "code a python", "write an essay"
    ]
    if any(k in q_clean for k in unrelated_keywords):
        return {
            "is_grounded": False,
            "answer": "This inquiry is unrelated to the provided legal agreement. LegalLens AI strictly provides document-grounded legal information extracted directly from your contract text.",
            "citation": "Out of Scope",
            "excerpt": "",
            "explanation": "No relevant provisions exist in this document regarding this general topic.",
            "confidence": 0.99
        }

    # 3. Intelligent Grounded Citation Search across Document
    topic_patterns = [
        (
            ["terminate", "termination", "cancel", "exit", "end the lease", "end the contract", "early exit"],
            r'(?:early termination|termination for convenience|term and termination|cancel|expiration).*?(?:notice|penalty|fee|month|\$)',
            "Early Termination & Exit Rights"
        ),
        (
            ["renew", "renewal", "automatic renewal", "extend"],
            r'(?:automatic renewal|renew for successive|notice of intent not to renew).*?(?:days|surcharge|market rate)',
            "Renewal & Notice Deadlines"
        ),
        (
            ["pay", "payment", "fee", "rent", "invoice", "late", "cost", "price", "surcharge"],
            r'(?:monthly rent|compensation|payment terms|invoicing|late charge|technology fee|valet trash).*?(?:\$\d+|\d+\s+days|net[\s\-]\d+)',
            "Payment Obligations & Surcharges"
        ),
        (
            ["indemnif", "liability", "hold harmless", "damage", "sue", "lawsuit", "breach"],
            r'(?:indemnif|hold harmless|limitation of liability|aggregate liability).*?(?:damages|claims|fees|gross negligence)',
            "Liability & Indemnification"
        ),
        (
            ["intellectual property", "ip", "copyright", "ownership", "work for hire", "code"],
            r'(?:intellectual property|work made for hire|pre-existing|background|patents|ownership).*?(?:sole and exclusive|assigns|retains)',
            "Intellectual Property & Ownership"
        ),
        (
            ["non-compete", "non-solicitation", "solicit", "compete", "restrict"],
            r'(?:non[\s\-]compete|non[\s\-]solicitation|shall not directly or indirectly).*?(?:months|solicit|clients)',
            "Restrictive Covenants"
        ),
        (
            ["deposit", "security deposit", "cleaning fee", "refund"],
            r'(?:security deposit|deposit amount|deductions & return).*?(?:\$\d+|\d+\s+days|cleaning fees)',
            "Security Deposit & Deductions"
        ),
        (
            ["guest", "visitor", "pets", "sublet", "occupant"],
            r'(?:guest limitations|pets|unauthorized subtenant|quiet enjoyment).*?(?:nights|pet fee|\$\d+)',
            "Use, Guests & Property Rules"
        ),
        (
            ["governing law", "jurisdiction", "court", "venue", "dispute", "jury"],
            r'(?:governing law|dispute venue|waiver of jury trial|laws of the State of).*?(?:Texas|Delaware|California|New York|courts)',
            "Governing Law & Disputes"
        )
    ]

    for keywords, regex_pat, topic_label in topic_patterns:
        if any(k in q_clean for k in keywords):
            match = re.search(regex_pat, document_text, re.I | re.DOTALL)
            if match:
                raw_excerpt = match.group(0).strip()
                # Clean excerpt length
                excerpt = " ".join(raw_excerpt.split())[:260]
                
                # Dynamic clause header detection near match
                start_pos = match.start()
                preceding_text = document_text[max(0, start_pos - 200):start_pos + 50]
                clause_match = re.search(r'(?:(?:Section|Article|Clause)\s+)?(\d+(?:\.\d+)*|[A-Z]+)\.?\s+([A-Z\s,/\-\(\)]{3,40})', preceding_text, re.I)
                citation = f"Clause {clause_match.group(1)}: {clause_match.group(2).strip().title()}" if clause_match else f"{topic_label}"

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
