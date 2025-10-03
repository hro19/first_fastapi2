from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import image_analysis, products, profiles, todos, email, population
from app.api.basic import cities, func
from app.api.strand import router as strand_router
from app.core.config import settings
from app.core.logging_config import setup_logging


setup_logging()

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
    email.router,
    prefix=f"{settings.API_V1_STR}/email",
    tags=["email"]
)

app.include_router(
    func.router,
    prefix=f"{settings.API_V1_STR}/basic",
    tags=["basic-functions"]
)

app.include_router(
    cities.router,
    prefix=f"{settings.API_V1_STR}/basic",
    tags=["japanese-cities"]
)

app.include_router(
    strand_router,
    prefix=settings.API_V1_STR,
    tags=["strand"]
)

app.include_router(
    population.router,
    prefix=f"{settings.API_V1_STR}/population",
    tags=["population"]
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
            "product_results_list": f"{settings.API_V1_STR}/products/result",
            "image_analysis": f"{settings.API_V1_STR}/images",
            "todos": f"{settings.API_V1_STR}/todos",
            "email_service": f"{settings.API_V1_STR}/email/first",
            "basic_functions": f"{settings.API_V1_STR}/basic/hello",
            "japanese_cities": f"{settings.API_V1_STR}/basic/cities",
            "strand_basic": f"{settings.API_V1_STR}/strand/basic",
            "population_1990": f"{settings.API_V1_STR}/population/1990",
            "population_1990_over_4_million": f"{settings.API_V1_STR}/population/1990/over4million",
            "population_1990_series": f"{settings.API_V1_STR}/population/1990_series",
            "population_1980_2000": f"{settings.API_V1_STR}/population/1980_2000",
        }
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "message": "FastAPI with Neon PostgreSQL is running successfully"
    }
