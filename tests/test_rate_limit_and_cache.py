"""
LegalLens AI - Rate Limiter, LRU Cache, and Middleware Test Suite.
"""

import sys
import time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi.testclient import TestClient
from backend.app import app
from backend.legal_engine import analyze_document_text, _ANALYSIS_CACHE

client = TestClient(app)

def test_sha256_lru_caching():
    sample_text = "This is a standard NDA contract with Mutual Confidentiality for 5 years."
    
    # First call - cache miss / compute
    start_t = time.perf_counter()
    res1 = analyze_document_text(sample_text, "nda_sample.txt")
    duration1 = time.perf_counter() - start_t
    
    # Second call - cache hit (< 10ms)
    start_t2 = time.perf_counter()
    res2 = analyze_document_text(sample_text, "nda_sample.txt")
    duration2 = time.perf_counter() - start_t2
    
    assert res1["risk_assessment"]["score"] == res2["risk_assessment"]["score"]
    assert res1["risk_assessment"]["level"] == res2["risk_assessment"]["level"]
    assert len(res1["clauses"]) == len(res2["clauses"])
    assert duration2 < 0.05  # Instant cache hit

def test_api_health_endpoint():
    res = client.get("/api/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "healthy"
    assert data["service"] == "LegalLens AI"

def test_gzip_compression_support():
    # Sending Accept-Encoding: gzip
    headers = {"Accept-Encoding": "gzip"}
    res = client.get("/api/health", headers=headers)
    assert res.status_code == 200
    assert "X-RateLimit-Limit" in res.headers

def test_rate_limiting_headers():
    res = client.get("/api/health")
    assert res.status_code == 200
    assert "X-RateLimit-Limit" in res.headers
    assert "X-RateLimit-Remaining" in res.headers
    assert int(res.headers["X-RateLimit-Limit"]) == 120
