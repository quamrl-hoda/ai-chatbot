"""
app/agent/nodes/planner.py – Planning node.

Receives the user input and prepares the HumanMessage for downstream nodes.
Extend this node to add retrieval, chain-of-thought prompting, or tool selection.
"""
from langchain_core.messages import HumanMessage
from app.agent.state import AgentState


def planner_node(state: AgentState) -> AgentState:
    """
    Planning step: converts raw `user_input` into a HumanMessage and
    appends it to the conversation history.
    """
    human_msg = HumanMessage(content=state["user_input"])
    return {
        "messages": [human_msg],
        "user_input": state["user_input"],
        "response": "",
    }
