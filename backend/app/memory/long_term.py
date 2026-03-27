"""
app/memory/long_term.py – Persistent memory helpers backed by SqliteSaver.

The LangGraph SqliteSaver stores every checkpoint in database/chatbot.db.
These helpers let you inspect or clear that history directly (e.g. from an
API route) without going through the graph itself.

Thread ID == conversation / session ID used in graph.invoke(config={"configurable": {"thread_id": ...}}).
"""
import sqlite3
from pathlib import Path

from app.utils.logger import get_logger

logger = get_logger(__name__)

# Same path as in app/agent/graph.py
_DB_PATH = str(Path(__file__).resolve().parents[3] / "database" / "chatbot.db")


def load_history(thread_id: str) -> list[dict]:
    """
    Return a plain list of {'role': ..., 'content': ...} dicts for a thread.

    Reads the latest checkpoint blob from the SqliteSaver schema and
    extracts the ``messages`` key from the serialised state.
    """
    try:
        with sqlite3.connect(_DB_PATH) as con:
            # SqliteSaver stores JSON-serialised state in the 'checkpoints' table.
            row = con.execute(
                """
                SELECT checkpoint
                FROM   checkpoints
                WHERE  thread_id = ?
                ORDER  BY checkpoint_id DESC
                LIMIT  1
                """,
                (thread_id,),
            ).fetchone()

        if row is None:
            return []

        import json
        state = json.loads(row[0])
        # The graph state has a 'messages' key (list of LangChain message dicts)
        raw_messages = state.get("channel_values", {}).get("messages", [])

        history: list[dict] = []
        for m in raw_messages:
            # Each message is a dict like {"type": "human", "content": "..."}
            role = m.get("type", m.get("role", "unknown"))
            content = m.get("content", "")
            history.append({"role": role, "content": content})

        return history

    except Exception as exc:
        logger.warning("load_history failed for thread %s: %s", thread_id, exc)
        return []


def delete_thread(thread_id: str) -> None:
    """Remove all checkpoints for a conversation thread from the SQLite DB."""
    try:
        with sqlite3.connect(_DB_PATH) as con:
            deleted = con.execute(
                "DELETE FROM checkpoints WHERE thread_id = ?", (thread_id,)
            ).rowcount
        logger.info("Deleted %d checkpoint(s) for thread %s", deleted, thread_id)
    except Exception as exc:
        logger.warning("delete_thread failed for thread %s: %s", thread_id, exc)


def list_threads() -> list[str]:
    """Return all distinct thread IDs that have at least one checkpoint."""
    try:
        with sqlite3.connect(_DB_PATH) as con:
            rows = con.execute(
                "SELECT DISTINCT thread_id FROM checkpoints ORDER BY thread_id"
            ).fetchall()
        return [r[0] for r in rows]
    except Exception as exc:
        logger.warning("list_threads failed: %s", exc)
        return []
