"""
app/models/chat.py – Pydantic request/response schemas for the Chat API.

With AsyncSqliteSaver, the full conversation history is persisted in SQLite
and reloaded automatically by thread_id.  The client only needs to send
the new user message and the thread_id — no history payload required.
"""
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    user_input: str = Field(..., description="The user's message")
    thread_id: str = Field(
        default="default",
        description="Conversation thread ID — unique per conversation session. "
                    "The backend persists history in SQLite keyed by this ID.",
    )
    # `history` intentionally removed: the checkpointer owns the history now.


class ChatResponse(BaseModel):
    response: str = Field(..., description="The assistant's reply")
    thread_id: str = Field(..., description="The thread ID used for this invocation")
    nodes_traversed: list[str] = Field(
        default=[],
        description="LangGraph nodes visited during this invocation",
    )
