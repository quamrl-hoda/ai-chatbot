"""
run.py – Root-level launcher for the FastAPI backend.

Run from the project root:
    python run.py

This inserts backend/ into sys.path so all `from app.xxx` imports resolve
without needing to cd into backend/ or set PYTHONPATH manually.
"""
import sys
import os

# ── Fix Python path ───────────────────────────────────────────────────────────
ROOT    = os.path.dirname(os.path.abspath(__file__))
BACKEND = os.path.join(ROOT, "backend")

if BACKEND not in sys.path:
    sys.path.insert(0, BACKEND)

# ── Check key dependencies ────────────────────────────────────────────────────
_missing = []
for pkg in ("fastapi", "uvicorn", "langchain_openai", "langgraph", "dotenv"):
    try:
        __import__(pkg)
    except ImportError:
        _missing.append(pkg)

if _missing:
    print("⚠️  Missing packages:", ", ".join(_missing))
    print("   Run:  pip install fastapi uvicorn langchain-openai langgraph python-dotenv")
    sys.exit(1)

# ── Start server ──────────────────────────────────────────────────────────────
import uvicorn

if __name__ == "__main__":
    print(f"🚀  Starting backend from {BACKEND}")
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        reload_dirs=[BACKEND],
    )
