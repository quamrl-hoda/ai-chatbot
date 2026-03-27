# Alembic Migrations

This directory is managed by [Alembic](https://alembic.sqlalchemy.org/).

## Setup

```bash
# From backend/
uv run alembic init app/db/migrations
# Edit alembic.ini → sqlalchemy.url = <your DATABASE_URL>
# Edit migrations/env.py → target_metadata = Base.metadata
```

## Workflow

```bash
# Generate a new migration after changing models
uv run alembic revision --autogenerate -m "describe change"

# Apply all pending migrations
uv run alembic upgrade head

# Roll back one step
uv run alembic downgrade -1
```
