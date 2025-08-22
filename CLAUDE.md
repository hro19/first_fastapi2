# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a FastAPI project with PostgreSQL database integration (Neon) and Azure AI Vision capabilities. The project follows a modular architecture with proper separation of concerns.

## Project Status

**Current State**: Full-stack FastAPI application with database and AI integration
**Framework**: FastAPI
**Language**: Python 3.12+
**Package Manager**: uv
**Database**: PostgreSQL (Neon)
**AI Services**: Azure Cognitive Services Vision

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

## Architecture Overview

The application follows a modular FastAPI architecture:

- **`app/main.py`** - Main FastAPI application with CORS and router configuration
- **`app/core/`** - Core functionality (config, database connections)
- **`app/api/`** - API route handlers organized by feature
- **`app/models/`** - SQLAlchemy database models
- **`app/schemas/`** - Pydantic models for request/response validation
- **`app/services/`** - Business logic and external service integrations
- **`main.py`** - Entry point that imports from app directory

### Database Architecture

Uses SQLAlchemy with async support for PostgreSQL (Neon):
- Async engine for API operations
- Sync engine for database inspection/migrations
- Connection pooling configured
- Both async and sync session factories available

### External Service Integration

- **Azure AI Vision** - Image analysis capabilities through `app/services/azure_vision.py`
- **File Upload** - Image processing and storage in `uploads/` directory

## Common Development Tasks

### Running the Application
```bash
# Development mode with auto-reload
uv run uvicorn main:app --reload

# Production mode
uv run uvicorn main:app --host 0.0.0.0 --port 8000
```

### Current API Endpoints

The application provides these endpoint groups:

- `GET /` - Root endpoint with project info and available endpoints
- `GET /health` - Health check endpoint
- `/api/v1/playing-with-neon` - Neon database testing endpoints
- `/api/v1/profiles` - User profile management
- `/api/v1/products` - Product management
- `/api/v1/images` - Image analysis using Azure AI Vision

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
├── app/                 # Main application directory
│   ├── main.py         # FastAPI app configuration and routing
│   ├── core/           # Core functionality
│   │   ├── config.py   # Application settings and environment variables
│   │   └── database.py # Database connection and session management
│   ├── api/            # API route handlers by feature
│   ├── models/         # SQLAlchemy database models
│   ├── schemas/        # Pydantic request/response models
│   └── services/       # Business logic and external integrations
├── uploads/            # File upload directory
├── main.py            # Application entry point (imports from app/)
├── inspect_db.py      # Database inspection utility
├── pyproject.toml     # Project configuration and dependencies
└── uv.lock           # Lock file for reproducible installs
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

### Database Operations
```bash
# Inspect database tables (using included utility)
uv run python inspect_db.py
```

### API Documentation

FastAPI automatically generates interactive API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Environment Configuration

Create a `.env` file in the project root with these variables:
```bash
# Database Configuration (Neon PostgreSQL)
DATABASE_URL=postgresql+asyncpg://username:password@host/database
DATABASE_URL_SYNC=postgresql://username:password@host/database

# Azure AI Vision
AZURE_VISION_KEY=your_azure_vision_key
AZURE_VISION_ENDPOINT=your_azure_vision_endpoint

# File Upload Settings
UPLOAD_DIR=uploads
MAX_FILE_SIZE=10485760  # 10MB
```

## Important Dependencies

Core dependencies in `pyproject.toml`:
- **FastAPI** - Web framework
- **SQLAlchemy** - Database ORM with async support
- **asyncpg** - Async PostgreSQL driver  
- **azure-cognitiveservices-vision-computervision** - Azure AI Vision client
- **Pillow** - Image processing
- **aiofiles** - Async file operations
- **python-multipart** - File upload support

## Development Patterns

When adding new features:
1. Create model in `app/models/`
2. Create Pydantic schemas in `app/schemas/`
3. Implement business logic in `app/services/` if needed
4. Create API routes in `app/api/`
5. Register router in `app/main.py`