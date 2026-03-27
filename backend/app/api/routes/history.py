"""
app/api/routes/history.py – Conversation history endpoints.

Backed by the long_term helpers which read directly from the SQLite
checkpoint DB (database/chatbot.db) written by AsyncSqliteSaver.
"""
from fastapi import APIRouter, HTTPException
from app.memory.long_term import list_threads, load_history, delete_thread

router = APIRouter()


@router.get("", summary="List all conversation thread IDs")
def list_conversations():
    """Returns every thread_id that has at least one saved checkpoint."""
    threads = list_threads()
    return {"threads": threads, "count": len(threads)}


@router.get("/{thread_id}", summary="Get message history for a thread")
def get_conversation(thread_id: str):
    """Returns the latest saved messages for the given thread_id."""
    messages = load_history(thread_id)
    if not messages:
        raise HTTPException(status_code=404, detail=f"No history found for thread '{thread_id}'")
    return {"thread_id": thread_id, "messages": messages, "count": len(messages)}


@router.delete("/{thread_id}", summary="Delete a conversation thread")
def delete_conversation(thread_id: str):
    """Removes all checkpoints for the given thread_id from the DB."""
    delete_thread(thread_id)
    return {"deleted": thread_id}
