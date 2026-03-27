"""
app/agent/state.py – Shared AgentState TypedDict for the LangGraph.
"""
from typing import Annotated
from typing_extensions import TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    """
    The graph's shared state.

    - messages   : full conversation history; uses `add_messages` reducer so
                   nodes append rather than overwrite.
    - user_input : raw text from the current user turn.
    - response   : final assistant response (written by responder / output node).
    """
    messages: Annotated[list[BaseMessage], add_messages]
    user_input: str
    response: str
