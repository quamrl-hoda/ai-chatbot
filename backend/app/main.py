"""
app/main.py – FastAPI application entry point.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.api.routes import chat, history, health

settings = get_settings()

app = FastAPI(
    title=settings.app_title,
    version="0.1.0",
    description="LangGraph-powered AI chatbot backend",
    debug=settings.debug,
)

# ── CORS ──────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(health.router, tags=["Health"])
app.include_router(chat.router,    prefix="/chat",    tags=["Chat"])
app.include_router(history.router, prefix="/history", tags=["History"])
