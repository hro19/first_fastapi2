from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api import playing_with_neon, profiles, products, image_analysis

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
    playing_with_neon.router,
    prefix=f"{settings.API_V1_STR}/playing-with-neon",
    tags=["playing-with-neon"]
)

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

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to FastAPI with Neon PostgreSQL!",
        "project": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "docs": "/docs",
        "endpoints": {
            "playing_with_neon": f"{settings.API_V1_STR}/playing-with-neon",
            "profiles": f"{settings.API_V1_STR}/profiles",
            "products": f"{settings.API_V1_STR}/products",
            "image_analysis": f"{settings.API_V1_STR}/images"
        }
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "message": "FastAPI with Neon PostgreSQL is running successfully"
    }