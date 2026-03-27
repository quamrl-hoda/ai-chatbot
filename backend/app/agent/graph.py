"""
app/agent/graph.py – LangGraph graph definition.

Builds and compiles the agent state-machine from individual nodes and edges.
"""
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver

from app.agent.state import AgentState
from app.agent.nodes.planner import planner_node
from app.agent.nodes.executor import executor_node
from app.agent.nodes.responder import responder_node

# Shared in-memory checkpointer (swap for SqliteSaver / PostgresSaver in prod)
checkpointer = InMemorySaver()


def build_graph() -> StateGraph:
    builder = StateGraph(AgentState)

    # ── Register nodes ────────────────────────────────────────────────────────
    builder.add_node("planner",   planner_node)
    builder.add_node("executor",  executor_node)
    builder.add_node("responder", responder_node)

    # ── Edges ─────────────────────────────────────────────────────────────────
    builder.add_edge(START,       "planner")
    builder.add_edge("planner",   "responder")   # direct path (no tools yet)
    builder.add_edge("executor",  "responder")   # tool results → responder
    builder.add_edge("responder", END)

    return builder.compile(checkpointer=checkpointer)


# Module-level singleton — imported by routes/chat.py and routes/health.py
graph = build_graph()
