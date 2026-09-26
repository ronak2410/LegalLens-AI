import sys
import os
import urllib.parse

# Ensure root directory is on Python sys.path
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from backend.app import app as fastapi_app

async def app(scope, receive, send):
    """
    ASGI entrypoint for Vercel Serverless Python environment.
    Normalizes Vercel rewritten paths (e.g. /api/index.py or __vercel_subpath__)
    so FastAPI routes (GET, POST, OPTIONS) resolve accurately.
    """
    if scope.get("type") == "http":
        target_path = None
        
        # 1. Check if subpath was passed in query parameters via vercel.json rewrite
        query_bytes = scope.get("query_string", b"")
        if query_bytes:
            qs_str = query_bytes.decode("utf-8", errors="ignore")
            parsed_qs = urllib.parse.parse_qs(qs_str)
            if "__vercel_subpath__" in parsed_qs:
                sub = parsed_qs["__vercel_subpath__"][0]
                if sub:
                    target_path = "/api/" + sub.lstrip("/")
                else:
                    target_path = "/api"
                
                # Reconstruct query string without __vercel_subpath__
                cleaned_pairs = [(k, v) for k, vals in parsed_qs.items() if k != "__vercel_subpath__" for v in vals]
                new_qs = urllib.parse.urlencode(cleaned_pairs)
                scope["query_string"] = new_qs.encode("utf-8")

        # 2. If not found in query param, check Vercel routing headers
        if not target_path:
            headers = dict(scope.get("headers", []))
            matched = (
                headers.get(b"x-matched-path")
                or headers.get(b"x-vercel-matched-path")
                or headers.get(b"x-forwarded-uri")
                or headers.get(b"x-original-uri")
            )
            if matched:
                decoded = matched.decode("utf-8", errors="ignore").split("?")[0]
                if decoded.startswith("/api"):
                    target_path = decoded

        # 3. Fallback to path manipulation
        curr_path = scope.get("path", "")
        if target_path:
            scope["path"] = target_path
        elif curr_path.startswith("/api/index.py"):
            sub = curr_path[len("/api/index.py"):]
            if not sub or sub == "/":
                scope["path"] = "/api"
            else:
                scope["path"] = "/api" + (sub if sub.startswith("/") else "/" + sub)
        elif curr_path == "/api/index":
            scope["path"] = "/api"
            
        if "raw_path" in scope:
            scope["raw_path"] = scope["path"].encode("utf-8")

    await fastapi_app(scope, receive, send)
