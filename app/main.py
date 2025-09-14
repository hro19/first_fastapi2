from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api import profiles, products, image_analysis, todos
from app.api.basic import func

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="FastAPI application connected to Neon PostgreSQL database"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(
    profiles.router,
    prefix=f"{settings.API_V1_STR}/profiles",
    tags=["profiles"]
)

app.include_router(
    products.router,
    prefix=f"{settings.API_V1_STR}/products",
    tags=["products"]
)

app.include_router(
    image_analysis.router,
    prefix=f"{settings.API_V1_STR}/images",
    tags=["image-analysis"]
)

app.include_router(
    todos.router,
    prefix=f"{settings.API_V1_STR}/todos",
    tags=["todos"]
)

app.include_router(
    func.router,
    prefix=f"{settings.API_V1_STR}/basic",
    tags=["basic-functions"]
)

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to FastAPI with Neon PostgreSQL!",
        "project": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "docs": "/docs",
        "endpoints": {
            "profiles": f"{settings.API_V1_STR}/profiles",
            "products": f"{settings.API_V1_STR}/products",
            "image_analysis": f"{settings.API_V1_STR}/images",
            "todos": f"{settings.API_V1_STR}/todos",
            "basic_functions": f"{settings.API_V1_STR}/basic"
        }
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "message": "FastAPI with Neon PostgreSQL is running successfully"
    }