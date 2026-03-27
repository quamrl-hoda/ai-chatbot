"""
app/api/dependencies.py – Reusable FastAPI dependency injectors.
"""
from fastapi import Header, HTTPException
from app.config import get_settings

settings = get_settings()


async def verify_api_key(x_api_key: str = Header(default="")):
    """
    Optional API-key guard.  Set APP_API_KEY in .env to enable.
    Leave blank to allow all traffic (development mode).
    """
    app_api_key = getattr(settings, "app_api_key", "")
    if app_api_key and x_api_key != app_api_key:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return x_api_key
