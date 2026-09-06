from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
import os

class Settings(BaseSettings):
    # API Keys
    GOOGLE_API_KEY: str
    GOOGLE_APPLICATION_CREDENTIALS: Optional[str] = None
    
    # Database
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/jansunwai"
    
    # App Config
    APP_NAME: str = "Jan-Sunwai AI"
    APP_ENV: str = "development"
    LOG_LEVEL: str = "INFO"
    
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
