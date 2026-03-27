"""
tests/test_routes.py – Integration-style tests for FastAPI routes.
"""
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_health():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        r = await client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_history_list_empty():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        r = await client.get("/history")
    assert r.status_code == 200
    assert r.json()["conversations"] == []


@pytest.mark.asyncio
async def test_graph_nodes():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        r = await client.get("/graph/nodes")
    assert r.status_code == 200
    assert "nodes" in r.json()
