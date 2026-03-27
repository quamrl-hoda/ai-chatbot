"""
app/tools/web_search.py – Web search tool (stub using requests).

Replace the stub body with a real search API (Tavily, SerpAPI, etc.)
and decorate with @tool so LangChain can bind it to the LLM.
"""
from langchain_core.tools import tool


@tool
def web_search(query: str) -> str:
    """
    Search the web for the given query and return a short summary.

    Args:
        query: The search query string.
    """
    # TODO: call Tavily / SerpAPI / DuckDuckGo and return real results
    return f"[web_search stub] No results yet for: {query}"
