"""
LegalLens AI - Application Server Launcher.
Starts the FastAPI server with uvicorn on http://127.0.0.1:8000.
"""

import sys
import uvicorn

if __name__ == "__main__":
    print("=====================================================")
    print("  LegalLens AI - AI for Legal Assistance & Access   ")
    print("  Starting local server at: http://127.0.0.1:8000   ")
    print("=====================================================")
    uvicorn.run("backend.app:app", host="127.0.0.1", port=8000, reload=False)
