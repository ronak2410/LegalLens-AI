import sys
import os

# Ensure root directory is on Python sys.path
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from backend.app import app as fastapi_app

async def app(scope, receive, send):
    """
    ASGI entrypoint for Vercel Serverless Python environment.
    Normalizes Vercel rewritten paths (e.g. /api/index.py or x-matched-path)
    so FastAPI routes (GET, POST, OPTIONS) resolve accurately.
    """
    if scope.get("type") == "http":
        headers = dict(scope.get("headers", []))
        
        # Check Vercel routing headers
        matched = (
            headers.get(b"x-matched-path")
            or headers.get(b"x-vercel-matched-path")
            or headers.get(b"x-forwarded-uri")
            or headers.get(b"x-original-uri")
        )
        
        target_path = None
        if matched:
            decoded = matched.decode("utf-8", errors="ignore").split("?")[0]
            if decoded.startswith("/api"):
                target_path = decoded
        
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
