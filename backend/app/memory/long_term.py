"""
app/memory/long_term.py – Persistent memory layer (PostgreSQL / SQLite via SQLAlchemy).

Currently a stub.  Wire up app.db.session.get_db() to enable real persistence.
"""
from app.utils.logger import get_logger

logger = get_logger(__name__)


async def load_history(conversation_id: str) -> list[dict]:
    """
    Load conversation history from the database.
    Returns a list of {'role': ..., 'content': ...} dicts.
    """
    # TODO: query Message table via SQLAlchemy session
    logger.debug("load_history called for %s (stub)", conversation_id)
    return []


async def save_message(conversation_id: str, role: str, content: str) -> None:
    """Persist a single message to the database."""
    # TODO: insert Message row via SQLAlchemy session
    logger.debug("save_message stub: [%s] %s: %s", conversation_id, role, content[:60])


async def delete_conversation(conversation_id: str) -> None:
    """Remove all messages for a conversation from the database."""
    # TODO: delete Message rows via SQLAlchemy session
    logger.debug("delete_conversation stub: %s", conversation_id)
