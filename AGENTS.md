# Repository Guidelines

## Project Structure & Module Organization
`app/` contains FastAPI packages: `api/` exposes routers (e.g., `products.py` handles product snapshots), `core/` holds settings, logging, and database wiring, `models/` & `schemas/` define SQLAlchemy and Pydantic types (including `product_result` snapshots), `services/` houses Azure Vision and image utilities, and `utils/` stores shared helpers. The ASGI entrypoint is `main.py`; auxiliary scripts such as `create_tables.py` and `inspect_db.py` live at the root. Tests mirror features under `tests/`, with shared fixtures in `tests/conftest.py`. Upload assets belong in `uploads/`, and long-form docs in `docs/`.

## Build, Test & Development Commands
- `uv sync` refreshes dependencies from `pyproject.toml` / `uv.lock`.
- `uv run uvicorn main:app --reload` launches the API locally (`--host 0.0.0.0 --port 8000` for container access).
- `uv run pytest` executes the full suite; add `-m "not slow"` for faster feedback.
- `uv run python create_tables.py` syncs schema changes (creates `product_result`, etc.) against the configured database.
- `curl -X POST https://first-fastapi2.vercel.app/api/v1/products/result` records a product snapshot; the same endpoint is wired into a manual GitHub Actions workflow.

## Coding Style & Naming Conventions
Target Python 3.12 with 4-space indent and async-friendly patterns. Prefer `pathlib.Path` for filesystem paths. Package and router names stay `snake_case`; SQLAlchemy models and Pydantic schemas use `PascalCase`. Format with `uv run black .`; lint via `uv run ruff check`, keeping rule ignores minimal and local.

## Testing Guidelines
Leverage `pytest` with `pytest-asyncio`; API tests should use the `async_client` fixture. Place new cases under `tests/test_*.py` and tag runtime with `@pytest.mark.fast` or `@pytest.mark.slow`. Mock Azure Vision services and external SMTP calls to keep suites deterministic. Run targeted tests when altering database logic (e.g., product snapshot aggregation).

## Commit & Pull Request Guidelines
Commits should describe the change and user impact—existing history mixes Japanese and descriptive English; match that tone. Keep each commit focused and include tests or docs updates when behavior shifts. Pull requests need a concise summary, linked issue/task when available, validation notes (e.g., `uv run pytest`), and evidence for API changes (sample payloads or screenshots).

## Security & Operations Tips
Keep secrets in an untracked `.env` accessed via `app/core/config.py`. Use disposable local Postgres instances to avoid clashing with Neon; run `create_tables.py` after schema edits. Serverless deployments (Vercel) run on read-only filesystems—logging now falls back to `/tmp` when needed. Use the GitHub Actions workflow (`workflow_dispatch`) to trigger daily product snapshots manually if automation is paused.
