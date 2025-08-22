import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    DATABASE_URL_SYNC: str = os.getenv("DATABASE_URL_SYNC", "")
    DATABASE_HOST: str = os.getenv("DATABASE_HOST", "")
    DATABASE_PORT: int = int(os.getenv("DATABASE_PORT", "5432"))
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "neondb")
    DATABASE_USER: str = os.getenv("DATABASE_USER", "")
    DATABASE_PASSWORD: str = os.getenv("DATABASE_PASSWORD", "")
    
    PROJECT_NAME: str = "First FastAPI with Neon"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"


settings = Settings()