from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_ID: str
    GOOGLE_APPLICATION_CREDENTIALS: str
    GEMINI_API_KEY: str
    ENVIRONMENT: str = "development"
    
    # AI Settings
    GEMINI_MODEL: str = "gemini-1.5-pro"
    MAX_RETRIES: int = 3
    
    # API Settings
    API_V1_STR: str = "/api/v1"
    
    class Config:
        env_file = ".env"

settings = Settings()
