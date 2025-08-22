# First FastAPI

A modern, full-stack FastAPI application with PostgreSQL database integration and Azure AI Vision capabilities.

## 🚀 Features

- **Modern FastAPI Framework** - High-performance, async web framework
- **PostgreSQL Integration** - Using Neon database with async SQLAlchemy
- **AI-Powered Image Analysis** - Azure Cognitive Services Vision integration
- **Modular Architecture** - Clean separation of concerns with organized project structure
- **File Upload & Processing** - Secure image upload and processing capabilities
- **Interactive API Documentation** - Auto-generated Swagger UI and ReDoc
- **CORS Support** - Cross-origin resource sharing enabled
- **Environment Configuration** - Flexible configuration management

## 🛠 Tech Stack

- **Backend**: FastAPI, Python 3.12+
- **Database**: PostgreSQL (Neon), SQLAlchemy (async)
- **AI Services**: Azure Cognitive Services Vision
- **Package Manager**: uv
- **Image Processing**: Pillow
- **File Handling**: aiofiles, python-multipart

## 📋 Prerequisites

- Python 3.12 or higher
- uv package manager
- PostgreSQL database (Neon recommended)
- Azure Cognitive Services Vision account (optional, for image analysis features)

## ⚡ Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd first_fastapi
```

### 2. Install Dependencies

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install project dependencies
uv sync
```

### 3. Environment Setup

Create a `.env` file in the project root:

```bash
# Database Configuration (Neon PostgreSQL)
DATABASE_URL=postgresql+asyncpg://username:password@host/database
DATABASE_URL_SYNC=postgresql://username:password@host/database

# Database Connection Details
DATABASE_HOST=your-neon-host
DATABASE_PORT=5432
DATABASE_NAME=your-database-name
DATABASE_USER=your-username
DATABASE_PASSWORD=your-password

# Azure AI Vision (Optional)
AZURE_VISION_KEY=your_azure_vision_key
AZURE_VISION_ENDPOINT=your_azure_vision_endpoint

# File Upload Settings
UPLOAD_DIR=uploads
MAX_FILE_SIZE=10485760  # 10MB
```

### 4. Run the Application

```bash
# Development mode with auto-reload
uv run uvicorn main:app --reload

# Custom host and port
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The application will be available at:
- **API**: http://localhost:8000
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📚 API Endpoints

### Core Endpoints
- `GET /` - Welcome message and project info
- `GET /health` - Health check endpoint

### Feature Endpoints
- `GET /api/v1/profiles` - User profile management
- `GET /api/v1/products` - Product management  
- `GET /api/v1/images` - Image analysis using Azure AI Vision

## 🏗 Project Structure

```
first_fastapi/
├── app/                    # Main application directory
│   ├── main.py            # FastAPI app configuration and routing
│   ├── core/              # Core functionality
│   │   ├── config.py      # Application settings
│   │   └── database.py    # Database connections
│   ├── api/               # API route handlers
│   │   ├── image_analysis.py
│   │   ├── products.py
│   │   └── profiles.py
│   ├── models/            # SQLAlchemy database models
│   ├── schemas/           # Pydantic request/response models
│   └── services/          # Business logic and external integrations
│       ├── azure_vision.py
│       └── image_processing.py
├── uploads/               # File upload directory
├── main.py               # Application entry point
├── inspect_db.py         # Database inspection utility
├── pyproject.toml        # Project configuration
└── README.md            # This file
```

## 🔧 Development

### Adding Dependencies

```bash
# Production dependency
uv add package-name

# Development dependency  
uv add --dev package-name

# Update all dependencies
uv sync
```

### Database Operations

```bash
# Inspect database tables
uv run python inspect_db.py
```

### Code Quality

```bash
# Format code (when tools are added)
uv run black .
uv run ruff format

# Lint code
uv run ruff check

# Type checking
uv run mypy app/
```

### Testing

```bash
# Run tests (when test suite is added)
uv run pytest

# Run with coverage
uv run pytest --cov=app

# Run specific test
uv run pytest tests/test_file.py::test_function
```

## 🌐 Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `DATABASE_URL` | Async PostgreSQL connection string | Yes | - |
| `DATABASE_URL_SYNC` | Sync PostgreSQL connection string | Yes | - |
| `DATABASE_HOST` | Database host | Yes | - |
| `DATABASE_PORT` | Database port | No | 5432 |
| `DATABASE_NAME` | Database name | Yes | - |
| `DATABASE_USER` | Database username | Yes | - |
| `DATABASE_PASSWORD` | Database password | Yes | - |
| `AZURE_VISION_KEY` | Azure Vision API key | No | - |
| `AZURE_VISION_ENDPOINT` | Azure Vision endpoint | No | - |
| `UPLOAD_DIR` | File upload directory | No | uploads |
| `MAX_FILE_SIZE` | Max file size in bytes | No | 10485760 |

## 🚀 Deployment

### Production Setup

1. Set production environment variables
2. Configure CORS origins properly in `app/main.py`
3. Use a production WSGI server like Gunicorn with Uvicorn workers:

```bash
uv add gunicorn
uv run gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

## 🤝 Development Patterns

When adding new features:

1. **Create Model** - Add SQLAlchemy model in `app/models/`
2. **Create Schema** - Add Pydantic models in `app/schemas/`
3. **Business Logic** - Implement in `app/services/` if needed
4. **API Routes** - Create routes in `app/api/`
5. **Register Router** - Add to `app/main.py`

## 📝 License

[Add your license information here]

## 🤝 Contributing

[Add contributing guidelines here]

## 📞 Support

[Add support/contact information here]