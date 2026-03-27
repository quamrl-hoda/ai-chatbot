"""
app/api/routes/chat.py – Chat inference endpoint.

Long-term memory is handled entirely by AsyncSqliteSaver via the thread_id.
The client sends ONLY the new user_input + thread_id — the checkpointer
reloads the full conversation history from SQLite automatically.
"""
from fastapi import APIRouter, Request

from app.models.chat import ChatRequest, ChatResponse

router = APIRouter()


@router.post("", response_model=ChatResponse, summary="Send a message")
async def chat(req: ChatRequest, request: Request):
    """
    Accepts a user message and a thread_id.
    LangGraph reloads the full conversation from SQLite (via AsyncSqliteSaver),
    appends the new turn, calls the LLM, and saves the updated state back.
    """
    graph = request.app.state.graph

    # Only the NEW user message is passed — the checkpointer provides the rest.
    initial_state = {
        "user_input": req.user_input,
        "messages":   [],   # empty: will be merged with checkpoint by add_messages
        "response":   "",
    }

    config = {"configurable": {"thread_id": req.thread_id}}

    result = await graph.ainvoke(initial_state, config=config)

    return ChatResponse(
        response=result["response"],
        thread_id=req.thread_id,
        nodes_traversed=["__start__", "planner", "responder", "__end__"],
    )
