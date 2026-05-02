from fastapi.middleware.cors import CORSMiddleware
from app.core.config import get_settings


def add_cors_middleware(app):
    """CORSミドルウェアを追加"""
    settings = get_settings()
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=settings.cors_allow_credentials,
        allow_methods=settings.cors_allow_methods,
        allow_headers=settings.cors_allow_headers,
    )
