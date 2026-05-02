from pydantic_settings import BaseSettings
from typing import List, Optional
from functools import lru_cache


class Settings(BaseSettings):
    """アプリケーション設定"""
    
    # API設定
    gemini_api_key: Optional[str] = None
    server_host: str = "0.0.0.0"
    server_port: int = 8000
    
    # CORS設定
    cors_origins: List[str] = ["*"]
    cors_allow_credentials: bool = True
    cors_allow_methods: List[str] = ["*"]
    cors_allow_headers: List[str] = ["*"]
    
    # ロギング設定
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # アプリケーション設定
    app_name: str = "Factory AI Assistant API"
    app_version: str = "1.0.0"
    app_description: str = "Unityアプリと連携するGemini AIアシスタントAPI"
    
    # 環境設定
    environment: str = "development"
    debug: bool = False
    
    # Gemini API設定
    gemini_model: str = "gemini-1.5-pro"
    gemini_temperature: Optional[float] = None
    gemini_max_tokens: Optional[int] = None
    
    @classmethod
    def validate(cls):
        """必須設定のバリデーション"""
        if not cls.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is required. Please set it in .env file.")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """設定インスタンスの取得（キャッシュ付き）"""
    return Settings()


# 後方互換性のためのエイリアス（遅延読み込み）
def get_cached_settings():
    return get_settings()
