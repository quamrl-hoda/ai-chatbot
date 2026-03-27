"""
LangGraph Simple Chatbot — Backend
------------------------------------
Graph: __start__ → input_node → llm_node → output_node → __end__

Install:
    pip install langgraph langchain-anthropic fastapi uvicorn python-dotenv

Run (from project root):
    uvicorn backend.main:app --reload --port 8000
"""

import os
from typing import Annotated
from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict

load_dotenv()

# ─── State ────────────────────────────────────────────────────────────────────

class ChatState(TypedDict):
    """
    The graph's shared state.
    `messages` uses the built-in `add_messages` reducer so nodes append
    rather than overwrite the conversation history.
    """
    messages: Annotated[list[BaseMessage], add_messages]
    user_input: str
    response: str


# ─── LLM ──────────────────────────────────────────────────────────────────────

llm = ChatOpenAI(model="gpt-4o-mini")


# ─── Nodes ────────────────────────────────────────────────────────────────────

def input_node(state: ChatState) -> ChatState:
    """Receives raw user input and appends it as a HumanMessage."""
    human_msg = HumanMessage(content=state["user_input"])
    return {
        "messages": [human_msg],
        "user_input": state["user_input"],
        "response": "",
    }


def llm_node(state: ChatState) -> ChatState:
    """Calls the LLM with the full conversation history."""
    ai_msg = llm.invoke(state["messages"])
    return {
        "messages": [ai_msg],
        "response": ai_msg.content,
    }


def output_node(state: ChatState) -> ChatState:
    """Formats / post-processes the response. Extend here for tool calls etc."""
    formatted = state["response"].strip()
    return {"response": formatted}


# ─── Graph ────────────────────────────────────────────────────────────────────

def build_graph() -> StateGraph:
    builder = StateGraph(ChatState)

    builder.add_node("input_node",  input_node)
    builder.add_node("llm_node",    llm_node)
    builder.add_node("output_node", output_node)

    builder.add_edge(START,         "input_node")
    builder.add_edge("input_node",  "llm_node")
    builder.add_edge("llm_node",    "output_node")
    builder.add_edge("output_node", END)

    return builder.compile()


graph = build_graph()


# ─── FastAPI ──────────────────────────────────────────────────────────────────

app = FastAPI(title="LangGraph Chatbot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # restrict in production
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    user_input: str
    history: list[dict] = []   # [{"role": "user"|"assistant", "content": "..."}]


class ChatResponse(BaseModel):
    response: str
    nodes_traversed: list[str]


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    history: list[BaseMessage] = []
    for m in req.history:
        if m["role"] == "user":
            history.append(HumanMessage(content=m["content"]))
        else:
            history.append(AIMessage(content=m["content"]))

    initial_state: ChatState = {
        "messages": history,
        "user_input": req.user_input,
        "response": "",
    }

    result = await graph.ainvoke(initial_state)

    return ChatResponse(
        response=result["response"],
        nodes_traversed=["__start__", "input_node", "llm_node", "output_node", "__end__"],
    )


@app.get("/graph/nodes")
def get_nodes():
    """Returns graph node names — useful for the React sidebar."""
    return {"nodes": list(graph.nodes.keys())}


@app.get("/health")
def health():
    return {"status": "ok"}
