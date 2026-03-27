"""
app/memory/short_term.py – In-session (in-memory) conversation store.

Backed by LangGraph's InMemorySaver, which lives in app.agent.graph.
This module exposes helper functions if you need direct access outside the graph.
"""
from langgraph.checkpoint.memory import InMemorySaver

# Singleton shared with the graph (imported from graph.py in real use)
_store: dict[str, list[dict]] = {}


def get_session(session_id: str) -> list[dict]:
    """Return the message list for a session, or an empty list."""
    return _store.get(session_id, [])


def save_session(session_id: str, messages: list[dict]) -> None:
    """Overwrite the stored messages for a session."""
    _store[session_id] = messages


def clear_session(session_id: str) -> None:
    """Delete a session from memory."""
    _store.pop(session_id, None)
