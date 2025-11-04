from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "sqlite:///./sme_management.db"
    
    # JWT Settings
    SECRET_KEY: str = "your-secret-key-change-in-production-use-env-variable"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # AI Model Settings
    MODEL_STORAGE_PATH: str = "./models"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

