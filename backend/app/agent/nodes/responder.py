"""
app/agent/nodes/responder.py – Final response node.

Calls the LLM with the full conversation history and stores the assistant reply.
"""
from langchain_openai import ChatOpenAI
from app.agent.state import AgentState
from app.config import get_settings

settings = get_settings()
llm = ChatOpenAI(
    model=settings.openai_model,
    api_key=settings.openai_api_key or None,
)


def responder_node(state: AgentState) -> AgentState:
    """
    Calls the LLM and returns the AI message + stripped response string.
    """
    ai_msg = llm.invoke(state["messages"])
    return {
        "messages": [ai_msg],
        "response": ai_msg.content.strip(),
    }
