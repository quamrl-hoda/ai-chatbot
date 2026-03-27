"""
app/db/session.py – SQLAlchemy async engine & session factory.

Note: aiosqlite must be installed for async SQLite support.
      For production swap to postgresql+asyncpg://...
"""
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", "..", ".env"))

_raw_url = os.getenv("DATABASE_URL", "sqlite:///./database/chatbot.db")
_debug   = os.getenv("DEBUG", "false").lower() == "true"

# Convert sync sqlite:/// → async sqlite+aiosqlite:/// driver
if _raw_url.startswith("sqlite:///") and "aiosqlite" not in _raw_url:
    _db_url = _raw_url.replace("sqlite:///", "sqlite+aiosqlite:///")
else:
    _db_url = _raw_url

try:
    from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

    engine = create_async_engine(_db_url, echo=_debug)
    AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

    async def get_db() -> AsyncSession:
        """FastAPI dependency that yields an async DB session."""
        async with AsyncSessionLocal() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise

    async def init_db() -> None:
        """Create all tables on startup."""
        from app.models.history import Base
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

except ImportError:
    # aiosqlite / sqlalchemy not installed — stubs so the app still starts
    engine = None
    AsyncSessionLocal = None

    async def get_db():
        raise RuntimeError("Database not configured. Install sqlalchemy + aiosqlite.")

    async def init_db():
        pass
