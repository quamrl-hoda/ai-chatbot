"""
app/api/routes/history.py – Conversation history endpoints.

Currently a stub; wire up to app.memory.long_term when you add persistence.
"""
from fastapi import APIRouter

router = APIRouter()


@router.get("", summary="List saved conversations")
def list_conversations():
    """Returns all stored conversation IDs (stub – extend with DB layer)."""
    return {"conversations": []}


@router.get("/{conversation_id}", summary="Get a conversation")
def get_conversation(conversation_id: str):
    """Returns the full message history for a given conversation ID."""
    return {"conversation_id": conversation_id, "messages": []}


@router.delete("/{conversation_id}", summary="Delete a conversation")
def delete_conversation(conversation_id: str):
    """Deletes a stored conversation (stub)."""
    return {"deleted": conversation_id}
