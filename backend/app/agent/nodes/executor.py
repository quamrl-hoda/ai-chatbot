"""
app/agent/nodes/executor.py – Tool-execution node.

Runs any tool calls emitted by the LLM.  Currently a pass-through stub;
wire up `app.tools.registry` to enable real tool execution.
"""
from app.agent.state import AgentState


def executor_node(state: AgentState) -> AgentState:
    """
    Executes tool calls found in the last AI message.
    Returns tool-result messages appended to the conversation.
    """
    # Stub: no tools configured yet — pass through unchanged.
    # TODO: iterate state["messages"][-1].tool_calls and invoke registered tools.
    return state
