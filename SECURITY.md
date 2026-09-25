# Security Policy & Architecture

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Security Architecture & Guarantees

LegalLens AI is architected with strict enterprise-grade security, data privacy, and zero-retention principles:

1. **Zero Data Retention Policy**:
   - Uploaded documents, contracts, and extracted clauses are processed ephemerally in-memory.
   - Files are never persisted to long-term storage or written to non-volatile disk.
   - Text buffers are garbage-collected immediately upon completion of the analysis response.

2. **In-Memory Cryptographic LRU Cache**:
   - Document deduplication utilizes SHA-256 cryptographic hashes as cache keys.
   - No raw document text or PII is exposed across cache queries.
   - Cache entries auto-evict with strict capacity boundaries to prevent memory exhaustion.

3. **Rate Limiting & Abuse Prevention**:
   - In-memory sliding-window rate limiter enforcing a strict threshold (120 requests/minute per client IP).
   - Prevents denial-of-service (DoS) and automated endpoint scraping.

4. **Defensive Ingestion & ReDoS Protection**:
   - Maximum upload file size is strictly capped at 10MB to prevent decompression bombs.
   - Regex patterns for legal clause classification and risk extraction use bounded lookaheads and linear scanning complexity to eliminate Regular Expression Denial of Service (ReDoS) vectors.

5. **HTTP Security Headers**:
   All responses emit hardened HTTP response headers:
   - `X-Content-Type-Options: nosniff`
   - `X-Frame-Options: DENY`
   - `X-XSS-Protection: 1; mode=block`
   - `Referrer-Policy: strict-origin-when-cross-origin`
   - `Content-Security-Policy: default-src 'self' 'unsafe-inline' 'unsafe-eval' https: data:;`

6. **CORS Configuration**:
   - Restricts unauthenticated cross-origin resource manipulation.

## Reporting a Vulnerability

If you discover a potential security vulnerability within LegalLens AI, please report it responsibly:

1. **Email**: Open a security report via GitHub Private Vulnerability Reporting or contact the maintainer at `ronak2410@users.noreply.github.com`.
2. **Details**: Please include:
   - Detailed description of the vulnerability
   - Steps to reproduce or proof-of-concept
   - Potential impact assessment
3. **Response Timeline**:
   - Acknowledgment within 24 hours.
   - Triage and mitigation plan within 48 hours.
   - Public patch release and advisory following coordinated disclosure.
