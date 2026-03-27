"""
app/tools/registry.py – Central tool registry.

Add new tools here and bind them to the LLM in app.agent.nodes.responder.
"""
from app.tools.web_search import web_search
from app.tools.calculator import calculator
from app.tools.file_reader import file_reader

# All tools available to the agent
ALL_TOOLS = [
    web_search,
    calculator,
    file_reader,
]

# Keyed by name for quick lookup in the executor node
TOOL_MAP = {t.name: t for t in ALL_TOOLS}
