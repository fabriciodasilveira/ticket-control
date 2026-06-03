"""
Configurações do sistema
"""

from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional
import os


class Settings(BaseSettings):
    """Configurações da aplicação"""
    
    # App
    APP_NAME: str = "TaskManager Burger API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    API_PREFIX: str = "/api/v1"
    
    # Database
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/taskmanager"
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # CORS
    CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://localhost:8080",
        "https://taskmanager.com",
    ]
    
    # Cloudflare R2
    R2_ACCOUNT_ID: str = ""
    R2_ACCESS_KEY_ID: str = ""
    R2_SECRET_ACCESS_KEY: str = ""
    R2_BUCKET_NAME: str = "taskmanager-evidence"
    R2_PUBLIC_URL: str = "https://cdn.taskmanager.com"
    
    # Email (SMTP)
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM_EMAIL: str = "noreply@taskmanager.com"
    
    # Push Notifications
    FIREBASE_PROJECT_ID: str = ""
    FIREBASE_PRIVATE_KEY: str = ""
    FIREBASE_CLIENT_EMAIL: str = ""
    
    # WhatsApp (Twilio/Future)
    TWILIO_ACCOUNT_SID: str = ""
    TWILIO_AUTH_TOKEN: str = ""
    TWILIO_WHATSAPP_NUMBER: str = ""
    
    # AI Services (Phase 2)
    AI_API_KEY: str = ""
    AI_MODEL: str = "gpt-4-vision-preview"
    
    # File Upload
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_IMAGE_TYPES: list[str] = ["image/jpeg", "image/png", "image/webp"]
    IMAGE_COMPRESSION_QUALITY: int = 80
    IMAGE_MAX_WIDTH: int = 1920
    IMAGE_MAX_HEIGHT: int = 1080
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    
    # Pagination
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Retorna configurações em cache"""
    return Settings()


settings = get_settings()
