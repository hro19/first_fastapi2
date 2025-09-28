# Repository Guidelines

## Project Structure & Module Organization
`app/` holds the FastAPI stack: `api/` for routers, `core/` for settings and database wiring, `models/` and `schemas/` for SQLAlchemy and Pydantic types, `services/` for Azure Vision integrations, and `utils/` for shared helpers. `main.py` exposes the ASGI entry point, while scripts like `create_tables.py` and `inspect_db.py` sit at the root. Tests live under `tests/` mirroring routes and services, with shared fixtures in `tests/conftest.py`. Assets land in `uploads/`, and long-form docs in `docs/`.

## Build, Test, and Development Commands
- `uv sync` installs or refreshes dependencies from `pyproject.toml`/`uv.lock`.
- `uv run uvicorn main:app --reload` boots the API locally; add `--host 0.0.0.0 --port 8000` for container exposure.
- `uv run pytest` runs the full suite; append `-m "not slow"` for quicker feedback.
- `uv run python create_tables.py` materializes database tables after schema changes.

## Coding Style & Naming Conventions
Target Python 3.12 with 4-space indentation and async-friendly patterns. Prefer `pathlib.Path` over raw strings for filesystem work. Modules and routers stay in `snake_case`, while Pydantic schemas and SQLAlchemy models use `PascalCase`. Format with `uv run black .` and lint via `uv run ruff check`, keeping suppressions narrow.

## Testing Guidelines
Use `pytest` and `pytest-asyncio`; endpoint tests should favour the `async_client` fixture. Place new cases under `tests/test_*.py`, tagging runtime with `@pytest.mark.fast` or `@pytest.mark.slow` as needed. Avoid external service calls—mock Azure clients and keep fixtures deterministic. Run targeted suites before committing whenever behaviour or contracts shift.

## Commit & Pull Request Guidelines
Write commits that explain the change and its user impact—historically in Japanese or equally descriptive English. Each commit should cover one concern and include tests or docs when applicable. Pull requests need a clear summary, linked task or issue ID, validation notes (e.g., `uv run pytest`), and screenshots or sample payloads for API changes.

## Security & Configuration Tips
Store secrets in an untracked `.env` and surface them through `Settings` in `app/core/config.py`. Use a disposable local Postgres instance to avoid clashing with production. Clean `uploads/` of sample data before sharing dumps or artifacts.
