"""
app/main.py – FastAPI application entry point.

Uses a lifespan context manager to:
  1. Open the AsyncSqliteSaver connection once at startup.
  2. Build the LangGraph graph with that checkpointer.
  3. Store the compiled graph on app.state so routes can access it.
  4. Close the connection cleanly on shutdown.
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.agent.graph import build_graph, DB_PATH

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # ── Startup ───────────────────────────────────────────────────────────────
    from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver

    async with AsyncSqliteSaver.from_conn_string(str(DB_PATH)) as checkpointer:
        app.state.graph = build_graph(checkpointer)
        yield
    # ── Shutdown: connection closed automatically by the async context manager ─


app = FastAPI(
    title=settings.app_title,
    version="0.1.0",
    description="LangGraph-powered AI chatbot backend",
    debug=settings.debug,
    lifespan=lifespan,
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
from app.api.routes import chat, history, health  # noqa: E402  (after app is created)

app.include_router(health.router, tags=["Health"])
app.include_router(chat.router,    prefix="/chat",    tags=["Chat"])
app.include_router(history.router, prefix="/history", tags=["History"])
