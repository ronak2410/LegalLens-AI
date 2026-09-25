"""
LegalLens AI - Google Gemini Generative AI Integration.
Provides optional multimodal & generative legal reasoning using Google Gemini API (gemini-1.5-flash / gemini-2.0-flash).
Gracefully falls back to heuristic engines if API key is missing or quota is exhausted.
"""

import os
import json
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger("LegalLens.Gemini")

try:
    import google.generativeai as genai
except ImportError:
    genai = None


def configure_gemini(api_key: Optional[str] = None) -> bool:
    """Configures the Gemini client with provided key or environment variable."""
    key = api_key or os.environ.get("GEMINI_API_KEY")
    if not key or not genai:
        return False
    try:
        genai.configure(api_key=key)
        return True
    except Exception as e:
        logger.warning(f"Failed to configure Gemini client: {e}")
        return False


def summarize_contract_with_gemini(text: str, api_key: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Uses Gemini to generate structured legal executive summaries and risk ratings."""
    if not configure_gemini(api_key):
        return None
        
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = f"""
        You are LegalLens AI, an expert legal information assistant for non-lawyers.
        Analyze the following legal agreement and provide a structured JSON response with:
        1. "overall_risk_score": integer from 0 (safest) to 100 (highest risk)
        2. "risk_level": "Low", "Medium", or "High"
        3. "executive_summary": concise 2-sentence plain English summary of what this document does
        4. "plain_language_summary": list of 3-4 key areas with "title", "simple_explanation", "what_to_do"
        5. "risks_and_flags": list of identified risks with "title", "severity" ("Critical", "High", "Medium", "Low"), "clause_ref", "impact", "recommendation"
        6. "lawyer_questions": list of 4 specific questions for attorney consultation
        7. "checklist": list of 5 pre-signing action items with "label" and "priority"

        Document Text:
        \"\"\"{text[:20000]}\"\"\"

        Return ONLY a valid JSON object matching the schema above.
        """
        response = model.generate_content(prompt)
        raw_text = response.text.strip()
        # Clean markdown backticks if present
        if raw_text.startswith("```json"):
            raw_text = raw_text[7:]
        if raw_text.startswith("```"):
            raw_text = raw_text[3:]
        if raw_text.endswith("```"):
            raw_text = raw_text[:-3]
        return json.loads(raw_text.strip())
    except Exception as e:
        logger.info(f"Gemini summarization fallback to heuristics: {e}")
        return None


def grounded_qa_with_gemini(question: str, document_text: str, api_key: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Uses Gemini to strictly answer user questions grounded in document text with citations."""
    if not configure_gemini(api_key):
        return None
        
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = f"""
        You are LegalLens AI's Grounded Q&A engine.
        Answer the following question STRICTLY and SOLELY based on the contract text provided below.
        Rules:
        1. If the contract does NOT mention or contain information to answer the question, you MUST respond stating that the document does not contain this information.
        2. If information is present, cite the exact clause number or heading and quote a concise excerpt (under 250 characters).
        3. Clarify that this is legal information, not legal advice.

        Output JSON schema:
        {{
            "is_grounded": true or false,
            "answer": "Plain-language direct answer",
            "citation": "Clause X.X: [Heading]",
            "excerpt": "Exact text quote from document",
            "explanation": "Why this clause applies",
            "confidence": 0.95
        }}

        Question: {question}

        Contract Text:
        \"\"\"{document_text[:20000]}\"\"\"

        Return ONLY a valid JSON object.
        """
        response = model.generate_content(prompt)
        raw_text = response.text.strip()
        if raw_text.startswith("```json"):
            raw_text = raw_text[7:]
        if raw_text.startswith("```"):
            raw_text = raw_text[3:]
        if raw_text.endswith("```"):
            raw_text = raw_text[:-3]
        return json.loads(raw_text.strip())
    except Exception as e:
        logger.info(f"Gemini Q&A fallback to heuristics: {e}")
        return None
