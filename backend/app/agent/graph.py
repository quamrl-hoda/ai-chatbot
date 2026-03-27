"""
app/agent/graph.py – LangGraph graph definition.

Builds and compiles the agent state-machine from individual nodes and edges.
Uses AsyncSqliteSaver for persistent long-term memory that works with
FastAPI's async runtime.  Swap for AsyncPostgresSaver in production.

The `graph` singleton is built at import time with the checkpointer already
wired in.  The checkpointer connection is opened/closed via the FastAPI
lifespan in app/main.py.
"""
from pathlib import Path

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver

from app.agent.state import AgentState
from app.agent.nodes.planner import planner_node
from app.agent.nodes.executor import executor_node
from app.agent.nodes.responder import responder_node

# ── DB path ───────────────────────────────────────────────────────────────────
# backend/app/agent/ → 3 levels up → project root → database/chatbot.db
DB_PATH = Path(__file__).resolve().parents[3] / "database" / "chatbot.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)


def build_graph(checkpointer: AsyncSqliteSaver) -> StateGraph:
    builder = StateGraph(AgentState)

    # ── Register nodes ────────────────────────────────────────────────────────
    builder.add_node("planner",   planner_node)
    builder.add_node("executor",  executor_node)
    builder.add_node("responder", responder_node)

    # ── Edges ─────────────────────────────────────────────────────────────────
    builder.add_edge(START,       "planner")
    builder.add_edge("planner",   "responder")
    builder.add_edge("executor",  "responder")
    builder.add_edge("responder", END)

    return builder.compile(checkpointer=checkpointer)
