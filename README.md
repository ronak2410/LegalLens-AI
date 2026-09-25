# LegalLens AI ⚖️
**AI-Powered Legal Information & Contract Analysis Assistant**

[![CI Test Suite](https://img.shields.io/badge/CI-Passing-brightgreen.svg)](#-automated-test-suite)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![WCAG](https://img.shields.io/badge/Accessibility-WCAG%202.1%20AA%20Compliant-purple.svg)](#-accessibility--wcag-21-aa-standards)
[![Security](https://img.shields.io/badge/Security-Zero%20Retention%20%7C%20Strict%20CSP-orange.svg)](#-security--privacy-architecture)

> **Understand legal documents with confidence.**  
> LegalLens AI helps individuals, tenants, freelancers, and small business owners understand complex contracts in plain language, detect one-sided risks, ask document-grounded questions with verified citations, compare revisions side-by-side, batch-audit contract portfolios, and negotiate balanced terms using AI redlines.

---

## 🛡️ Critical Legal & Ethical Disclaimer
> **LegalLens AI provides general legal information and is not a law firm, lawyer, or substitute for professional legal advice.**
>
> The platform provides educational and informational analysis to demystify complex legal terms for everyday individuals. It does not provide binding legal counsel, make definitive enforceability guarantees, or establish an attorney-client relationship. Always consult a licensed attorney in your jurisdiction for important legal actions.

---

## 🌟 Core Features

### 1. Modern Legal-Tech Workspace
- **Design System**: Accessible dark-mode theme (`#070B14`, `#111827`), electric blue accents (`#38BDF8`), and glassmorphism styling.
- **Pre-Loaded Sample Contracts**: 4 realistic contracts (Residential Lease, Freelance MSA, Enterprise SaaS, Mutual NDA).

### 2. Document Ingestion & Multimodal Parsing
- Ingests **PDF** (including scanned PDFs with OCR fallback), Microsoft Word (**DOCX**), and Plain Text (**TXT**).
- **15MB Size Limit**: Enforced across both client-side and FastAPI middleware.
- **Zero-Dependency Fallbacks**: Includes pure Python XML/zlib parsers that guarantee offline extraction without dependency failures.

### 3. Comprehensive Analysis Dashboard
- **Normalized Risk Score (0–100)**: Categorized as Low, Moderate, or High risk.
- **Executive Plain-Language Summaries**: Translates legal obligations into *"What this means for you"* and actionable takeaways.
- **Annotated In-Line Document Viewer**: Interactive color-coded risk markings directly on the contract text.
- **Negotiation Redlines**: Concrete, professionally drafted replacement counter-clauses with 1-click clipboard copy.
- **Pre-Signing Checklist & Consultation Questions**: Structured preparation plan for attorney meetings.

### 4. "Ask the Document" (Document-Grounded Q&A)
- Answers questions **strictly grounded** in the active contract text.
- **Interactive Citation References**: Generates dynamic clause citations (e.g. `[Clause 4.1: Early Termination]`). Clicking a citation opens the verified excerpt in a modal.
- **Honest Refusal**: Explicitly declines out-of-scope queries (general trivia, unrelated topics) to prevent AI hallucinations.
- **Suggested Question Chips**: 1-click prompts for common exit, payment, and liability questions.

### 5. Side-by-Side Contract Comparison
- Compare two contract drafts or counterparty revisions.
- **Risk Shift Delta**: Calculates score differences (e.g. `+62 pts: Substantially Higher Risk in Document B`).
- **Standardized Matrix**: Compares Payment, Liability, Termination, IP, and Covenants.

### 6. Custom Negotiation Playbooks & Organizational Rules
- Define custom risk criteria, organization-specific fallback rules, and non-negotiable clauses.
- Curated presets: **Freelancer Shield**, **Startup Vendor Guard**, and **Tenant Rights Armor**.
- ReDoS-safe regex engine validates pattern complexity and length.

### 7. Multi-Document "Due Diligence Hub" (Batch Analysis)
- Batch-scan **2 to 10 contracts concurrently** using thread pools for high throughput.
- **Portfolio Health KPI Score**: Weighted cross-document risk profile.
- **Cross-Contract Contradictions**: Flags conflicting governing jurisdictions and compound liability concentrations.
- **Unified Renewal Milestones & Timeline**: Aggregates all notice windows and expiry deadlines chronologically.

### 8. Microsoft Word (.docx) & Markdown Reports
- Export complete legal briefing reports with formatted tables and color-coded redlines directly to `.docx` or `.md`.

### 9. LegalLens AI Browser Extension (Manifest V3)
- Located in `extension/`.
- 1-click popup scanner for Terms of Service and Privacy Policies on any webpage.
- Seamlessly hands off scraped webpage text into the full LegalLens AI web studio.

---

## 🏛️ Technical Architecture

```
├── backend/
│   ├── app.py              # FastAPI server, security headers, endpoints
│   ├── legal_engine.py     # NLP clause segmentation, risk scoring, ReDoS protection
│   ├── gemini_engine.py    # Google Gemini AI integration (gemini-1.5-flash) with heuristic fallback
│   ├── redline_engine.py   # AI clause counter-language & negotiation templates
│   ├── qa_engine.py        # Grounded Q&A with dynamic clause citations & guardrails
│   ├── comparator.py       # Side-by-side comparison & risk delta analysis
│   ├── portfolio_engine.py # Concurrent batch due diligence & contradiction detection
│   ├── parser.py           # Multimodal parser (PDF, OCR, DOCX, TXT) with 15MB limit
│   └── samples.py          # 4 realistic pre-loaded legal contracts
├── frontend/
│   ├── index.html          # Semantic HTML5 layout with WCAG 2.1 AA landmarks
│   ├── css/
│   │   └── styles.css      # Design system with :focus-visible outlines and contrast
│   └── js/
│       ├── app.js          # App state, tab routing, ARIA state, extension handoff
│       ├── analysis.js     # Risk dial, in-line highlights, redlines, DOCX/MD export
│       ├── chat.js         # Grounded chat, citation modal, suggested chips
│       ├── compare.js      # Comparison matrix & delta progression
│       ├── portfolio.js    # Batch due diligence controller & KPIs
│       └── samples.js      # Sample contracts switcher
├── extension/              # Manifest V3 Chrome / Edge Browser Extension
│   ├── manifest.json       # Manifest V3 specification
│   ├── popup.html / .js    # Dark mode scanner popup with Studio handoff
│   ├── content.js / .css   # Inline page detector
│   ├── background.js       # Context menu service worker
│   └── icons/              # 16px, 48px, 128px extension icons
├── tests/
│   ├── test_legal_engine.py        # NLP, clause segmentation, citation & QA tests
│   ├── test_parser_and_security.py # 15MB limit, ReDoS, XSS sanitization, CSP tests
│   └── test_batch_and_export.py    # Concurrent batch analysis, Markdown & DOCX export
├── .github/workflows/test.yml      # CI/CD GitHub Actions workflow
├── .gitignore                      # Clean repository hygiene
├── LICENSE                         # MIT License
├── requirements.txt                # Python dependencies
├── run.py                          # Python launcher
└── run.bat                         # Windows batch launcher
```

---

## ♿ Accessibility & WCAG 2.1 AA Standards

- **Keyboard Navigation**: Skip-to-content link (`<a href="#main-content" class="skip-link">`), logical tab order, and modal focus trapping with `Escape` key listeners.
- **Focus Rings**: Prominent `:focus-visible` styling (`outline: 2px solid #38BDF8; outline-offset: 3px;`) across all buttons, inputs, links, and tabs.
- **ARIA & Semantics**: Full ARIA roles (`role="tablist"`, `role="tab"`, `role="tabpanel"`, `role="dialog"`, `aria-selected`, `aria-controls`, `aria-live="polite"`).
- **Contrast Ratios**: Verified text-to-background contrast meeting and exceeding the WCAG AA threshold of 4.5:1.

---

## 🔒 Security & Privacy Architecture

- **Zero Data Retention**: Document text is processed in volatile memory only and never written to a persistent database.
- **15MB Payload Limit**: Strictly enforced in both frontend drop zones and backend HTTP middleware.
- **ReDoS Protection**: Validates regex pattern complexity and restricts input length.
- **Strict Content Security Policy**: CSP headers protect against XSS and malicious code injection.
- **Safe CORS**: Standard non-credentialed CORS preventing unauthorized cross-origin credential sharing.
- **Path Traversal Protection**: Static file routes enforce strict directory containment.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+ installed.

### 1. Install & Launch
```bash
# Clone the repository
git clone https://github.com/your-username/legallens-ai.git
cd prompt

# Install dependencies
pip install -r requirements.txt

# Start the application server
python run.py
```
*(On Windows, you can also double-click `run.bat`)*

Open your browser at **`http://localhost:8000`**.

### 2. Run Automated Test Suite
```bash
python -m pytest tests/ -v
```

### 3. Load the Browser Extension
1. Open Google Chrome, Brave, or Microsoft Edge.
2. Navigate to `chrome://extensions/`.
3. Enable **Developer mode** in the top right.
4. Click **Load unpacked** and select the `extension/` folder.
5. Click the LegalLens AI icon in your browser toolbar on any webpage to scan!

---

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
