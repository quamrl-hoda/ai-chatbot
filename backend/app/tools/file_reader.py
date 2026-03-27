"""
app/tools/file_reader.py – Safe local file reading tool.
"""
from pathlib import Path
from langchain_core.tools import tool

_ALLOWED_EXTENSIONS = {".txt", ".md", ".csv", ".json", ".yaml", ".yml"}
_MAX_CHARS = 8_000


@tool
def file_reader(path: str) -> str:
    """
    Read a local text file and return its contents (up to 8 000 characters).

    Args:
        path: Absolute or relative path to the file.
    """
    fp = Path(path).resolve()
    if fp.suffix not in _ALLOWED_EXTENSIONS:
        return f"Error: file type '{fp.suffix}' is not allowed."
    if not fp.exists():
        return f"Error: file not found at '{fp}'."
    content = fp.read_text(encoding="utf-8", errors="replace")
    if len(content) > _MAX_CHARS:
        content = content[:_MAX_CHARS] + "\n...[truncated]"
    return content
