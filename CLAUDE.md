# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a FastAPI project using **uv** as the package manager. The project includes a basic FastAPI application with sample endpoints.

## Project Status

**Current State**: Basic FastAPI application implemented
**Framework**: FastAPI
**Language**: Python 3.12+
**Package Manager**: uv (version 0.8.4)

## Development Setup

### Using uv (Recommended)

This project uses **uv** for Python package management and virtual environment handling.

1. **Activate virtual environment**:
   ```bash
   source .venv/bin/activate  # On Linux/Mac
   ```

2. **Install dependencies**:
   ```bash
   uv sync  # Installs all dependencies from pyproject.toml
   ```

3. **Add new dependencies**:
   ```bash
   uv add package-name
   uv add --dev package-name  # For development dependencies
   ```

4. **Run development server**:
   ```bash
   uv run uvicorn main:app --reload
   # Or with custom host/port:
   uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

## Common Development Tasks

### Running the Application
```bash
# Development mode with auto-reload
uv run uvicorn main:app --reload

# Production mode
uv run uvicorn main:app --host 0.0.0.0 --port 8000
```

### Current API Endpoints

The application currently provides these endpoints:

- `GET /` - Root endpoint returning a welcome message
- `GET /health` - Health check endpoint
- `GET /items/{item_id}` - Get item by ID with optional query parameter
- `POST /items/` - Create a new item

### Adding Dependencies
```bash
# Production dependency
uv add package-name

# Development dependency
uv add --dev pytest pytest-asyncio httpx

# Update all dependencies
uv sync
```

### Project Structure
```
first_fastapi/
├── .venv/                # Virtual environment (created by uv)
├── main.py              # FastAPI application entry point
├── pyproject.toml       # Project configuration and dependencies
├── uv.lock             # Lock file for reproducible installs
├── CLAUDE.md           # This file
├── README.md           # Project documentation
└── .gitignore          # Git ignore rules
```

### Testing
When tests are added:
```bash
# Run tests with pytest
uv run pytest

# Run with coverage
uv run pytest --cov=.

# Run specific test
uv run pytest tests/test_file.py::test_function
```

### Code Quality
When linting/formatting tools are added:
```bash
# Format code
uv run black .
uv run ruff format

# Lint code
uv run ruff check

# Type checking
uv run mypy main.py
```

### API Documentation

FastAPI automatically generates interactive API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Important Configuration Files

### pyproject.toml
Contains project metadata and dependencies. Key sections:
- `[project]` - Project name, version, Python requirements
- `[project.dependencies]` - Production dependencies
- `[project.optional-dependencies]` - Development dependencies

### uv.lock
Auto-generated lock file ensuring reproducible installations across environments. Do not edit manually.

## Important Notes

- Python 3.12+ is required (specified in pyproject.toml)
- The `.gitignore` file is configured for Python projects
- Virtual environment is in `.venv/` directory
- FastAPI and uvicorn[standard] are already installed
- Database configuration and ORM setup can be added as needed
- Authentication/authorization can be implemented based on requirements