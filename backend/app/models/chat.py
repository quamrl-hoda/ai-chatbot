"""
app/models/chat.py – Pydantic request/response schemas for the Chat API.
"""
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    user_input: str = Field(..., description="The user's message")
    thread_id: str = Field(
        default="default",
        description="Conversation thread ID — must be unique per conversation session",
    )
    history: list[dict] = Field(
        default=[],
        description='Previous turns: [{"role": "user"|"assistant", "content": "..."}]',
    )


class ChatResponse(BaseModel):
    response: str = Field(..., description="The assistant's reply")
    thread_id: str = Field(..., description="The thread ID used for this invocation")
    nodes_traversed: list[str] = Field(
        default=[],
        description="LangGraph nodes visited during this invocation",
    )
