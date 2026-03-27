"""
app/agent/edges.py – Conditional edge logic for the LangGraph.

Add routing functions here when you need branching (e.g. tool-call dispatch).
"""
from app.agent.state import AgentState


def should_use_tools(state: AgentState) -> str:
    """
    Example conditional edge: route to 'executor' if the last AI message
    contains tool calls, otherwise go straight to 'responder'.
    """
    messages = state.get("messages", [])
    if messages:
        last = messages[-1]
        # LangChain tool-call check
        if hasattr(last, "tool_calls") and last.tool_calls:
            return "executor"
    return "responder"
