from pydantic_settings import BaseSettings
from typing import List, Optional
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings"""
    
    # API configuration
    gemini_api_key: Optional[str] = None
    server_host: str = "0.0.0.0"
    server_port: int = 8000
    
    # CORS configuration
    cors_origins: List[str] = ["*"]
    cors_allow_credentials: bool = True
    cors_allow_methods: List[str] = ["*"]
    cors_allow_headers: List[str] = ["*"]
    
    # Logging configuration
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Application configuration
    app_name: str = "Factory AI Assistant API"
    app_version: str = "1.0.0"
    app_description: str = "Gemini AI assistant API for Unity app integration"
    
    # Environment configuration
    environment: str = "development"
    debug: bool = False
    
    # Gemini API configuration
    gemini_model: str = "gemini-1.5-pro"
    gemini_temperature: Optional[float] = None
    gemini_max_tokens: Optional[int] = None
    
    @classmethod
    def validate(cls, settings: 'Settings'):
        """Required settings validation"""
        if not settings.gemini_api_key:
            raise ValueError("GEMINI_API_KEY is required. Please set it in .env file.")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get settings instance (cached)"""
    return Settings()


# Alias for backward compatibility (lazy loading)
def get_cached_settings():
    return get_settings()
