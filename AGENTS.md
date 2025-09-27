# Repository Guidelines

## Project Structure & Module Organization
- `app/` holds FastAPI packages: `api/` for routers, `core/` for config and DB wiring, `models/` and `schemas/` for SQLAlchemy and Pydantic types, `services/` for Azure Vision and business logic, and `utils/` for shared helpers.
- `main.py` exposes the FastAPI entry point; auxiliary scripts such as `create_tables.py` and `inspect_db.py` live at the project root.
- `tests/` mirrors route and service features; keep new fixtures in `tests/conftest.py`. Assets such as sample uploads reside in `uploads/`, and long-form docs sit in `docs/`.

## Build, Test, and Development Commands
- `uv sync` installs or refreshes dependencies from `pyproject.toml` and `uv.lock`.
- `uv run uvicorn main:app --reload` launches the API with hot-reload for local work; append `--host 0.0.0.0 --port 8000` when exposing to containers.
- `uv run pytest` executes the full test suite; add `-m "not slow"` to skip long-running cases.
- `uv run python create_tables.py` materializes tables against the configured database; run after schema changes.

## Coding Style & Naming Conventions
- Target Python 3.12, 4-space indentation, and async-friendly patterns; prefer `Path` over raw strings for filesystem work.
- Name routers and modules in `snake_case`; Pydantic schemas and SQLAlchemy models stay in `PascalCase`.
- Type hints are expected for public functions. Before pushing, format with `uv run black .` and lint with `uv run ruff check` (keep rule suppressions localized).

## Testing Guidelines
- Tests use `pytest` with `pytest-asyncio`; prefer async tests when touching FastAPI endpoints via the `async_client` fixture.
- Place new tests under `tests/` following the `test_*.py` pattern noted in `pyproject.toml`.
- Leverage `@pytest.mark.fast` and `@pytest.mark.slow` to categorize runtime, and keep fixtures deterministic (avoid external services; mock Azure clients).

## Commit & Pull Request Guidelines
- Git history favors complete sentences that explain both the change and the user impact (many entries are Japanese; match that tone or use equally descriptive English).
- Commits should remain focused on one concern and include accompanying tests or docs updates.
- Pull requests need a clear summary, linked issue or task ID when available, validation notes (commands run), and screenshots or sample payloads for API/UI changes.

## Environment & Configuration Tips
- Store secrets in `.env` and keep the file untracked; reference keys via `Settings` in `app/core/config.py`.
- For local Postgres, run against a temporary database to avoid clashing with production Neon instances, and clear the `uploads/` directory of sample data before sharing dumps.
