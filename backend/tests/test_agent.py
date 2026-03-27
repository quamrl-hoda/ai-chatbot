"""
tests/test_agent.py – Tests for the LangGraph agent.
"""
import pytest
from langchain_core.messages import HumanMessage


def test_agent_state_keys():
    """AgentState must contain messages, user_input, and response."""
    from app.agent.state import AgentState
    keys = AgentState.__annotations__.keys()
    assert "messages"   in keys
    assert "user_input" in keys
    assert "response"   in keys


def test_planner_node_appends_human_message():
    """planner_node should wrap user_input as a HumanMessage."""
    from app.agent.nodes.planner import planner_node
    state = {"messages": [], "user_input": "hello", "response": ""}
    result = planner_node(state)
    assert result["messages"][0].content == "hello"
    assert isinstance(result["messages"][0], HumanMessage)


def test_calculator_tool():
    """Calculator tool should evaluate simple expressions correctly."""
    from app.tools.calculator import calculator
    assert calculator.invoke("2 + 2") == "4"
    assert calculator.invoke("10 * 3") == "30"
