from fastapi import Depends
from app.core.config import get_settings, Settings
from app.services.gemini_service import GeminiService


def get_gemini_service(settings: Settings = Depends(get_settings)) -> GeminiService:
    """GeminiServiceのインスタンスを取得（依存性注入）"""
    return GeminiService(settings)
