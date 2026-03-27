"""
app/api/routes/health.py – Health-check endpoint.
"""
from fastapi import APIRouter

router = APIRouter()


@router.get("/health", summary="Health check")
def health():
    """Returns 200 OK when the service is up."""
    return {"status": "ok"}


@router.get("/graph/nodes", summary="Graph node list")
def get_nodes():
    """Returns the names of all nodes registered in the LangGraph."""
    from app.agent.graph import graph
    return {"nodes": list(graph.nodes.keys())}
