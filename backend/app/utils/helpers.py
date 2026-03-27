"""
app/utils/helpers.py – General-purpose helper functions.
"""
import uuid
from datetime import datetime, timezone


def new_uuid() -> str:
    """Generate a new UUID4 string."""
    return str(uuid.uuid4())


def utcnow_iso() -> str:
    """Return the current UTC time as an ISO-8601 string."""
    return datetime.now(timezone.utc).isoformat()


def truncate(text: str, max_len: int = 40, suffix: str = "…") -> str:
    """Truncate *text* to *max_len* characters, appending *suffix* if cut."""
    return text if len(text) <= max_len else text[:max_len] + suffix


def sanitize_messages(messages: list[dict]) -> list[dict]:
    """
    Remove incomplete tool-call / tool-result pairs from a message list.
    Prevents OpenAI 400 errors caused by interrupted agentic turns.
    """
    clean: list[dict] = []
    for msg in messages:
        # Drop orphaned tool messages (no preceding assistant tool_call)
        if msg.get("role") == "tool":
            if clean and clean[-1].get("role") == "assistant":
                clean.append(msg)
            # else: skip orphan
        else:
            clean.append(msg)
    return clean
