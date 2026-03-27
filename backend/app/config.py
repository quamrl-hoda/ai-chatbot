"""
app/config.py – Centralised settings loaded from environment / .env file.

Uses only python-dotenv + os.getenv (no pydantic-settings required).
"""
import os
from functools import lru_cache
from dotenv import load_dotenv

# Load .env from the backend/ directory or project root
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", ".env"))
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))


class Settings:
    # ── OpenAI ────────────────────────────────────────────────────────────────
    openai_api_key: str  = os.getenv("OPENAI_API_KEY", "")
    openai_model:   str  = os.getenv("OPENAI_MODEL",   "gpt-4o-mini")

    # ── Google / HuggingFace (optional) ───────────────────────────────────────
    google_api_key: str = os.getenv("GOOGLE_API_KEY", "")
    hf_token:       str = os.getenv("HF_TOKEN",       "")

    # ── LangSmith tracing (optional) ──────────────────────────────────────────
    langchain_tracing_v2:  bool = os.getenv("LANGCHAIN_TRACING_V2", "false").lower() == "true"
    langchain_endpoint:    str  = os.getenv("LANGCHAIN_ENDPOINT",   "https://api.smith.langchain.com")
    langchain_api_key:     str  = os.getenv("LANGCHAIN_API_KEY",    "")
    langchain_project:     str  = os.getenv("LANGCHAIN_PROJECT",    "ai-chatbot")

    # ── Database ──────────────────────────────────────────────────────────────
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./database/chatbot.db")

    # ── App ───────────────────────────────────────────────────────────────────
    app_title:    str       = os.getenv("APP_TITLE",    "LangGraph Chatbot API")
    debug:        bool      = os.getenv("DEBUG",        "false").lower() == "true"
    cors_origins: list[str] = os.getenv("CORS_ORIGINS", "*").strip("[]\"'").split(",")


@lru_cache
def get_settings() -> Settings:
    return Settings()
