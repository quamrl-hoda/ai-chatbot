"""
app/api/routes/chat.py – Chat inference endpoint.
"""
from fastapi import APIRouter
from langchain_core.messages import HumanMessage, AIMessage

from app.models.chat import ChatRequest, ChatResponse
from app.agent.graph import graph

router = APIRouter()


@router.post("", response_model=ChatResponse, summary="Send a message")
async def chat(req: ChatRequest):
    """
    Accepts a user message plus previous conversation history,
    runs the LangGraph agent, and returns the assistant reply.

    The `thread_id` field is used by the LangGraph checkpointer to persist
    memory across turns within the same conversation session.
    """
    # Rebuild message history from raw dicts
    history = []
    for m in req.history:
        if m["role"] == "user":
            history.append(HumanMessage(content=m["content"]))
        else:
            history.append(AIMessage(content=m["content"]))

    initial_state = {
        "messages": history,
        "user_input": req.user_input,
        "response": "",
    }

    # ── thread_id is REQUIRED when a checkpointer is attached ────────────────
    config = {"configurable": {"thread_id": req.thread_id}}

    result = await graph.ainvoke(initial_state, config=config)

    return ChatResponse(
        response=result["response"],
        thread_id=req.thread_id,
        nodes_traversed=["__start__", "planner", "responder", "__end__"],
    )
