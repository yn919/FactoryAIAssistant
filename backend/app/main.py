from fastapi import FastAPI
from contextlib import asynccontextmanager
import logging

from app.core.config import get_settings
from app.core.logging import setup_logging
from app.core.exceptions import FactoryAIException
from app.middleware.cors import add_cors_middleware
from app.middleware.error_handler import factory_ai_exception_handler, general_exception_handler
from app.api.v1.api import api_router

# ロギング設定
logger = setup_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 起動時の処理
    try:
        settings = get_settings()
        logger.info(f"FastAPI server starting up on {settings.server_host}:{settings.server_port}")
        yield
    except Exception as e:
        logger.error(f"Startup failed: {str(e)}")
        raise
    finally:
        # シャットダウン時の処理
        logger.info("FastAPI server shutting down...")

# FastAPIアプリケーション作成
settings = get_settings()
app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
    lifespan=lifespan
)

# ミドルウェアの設定
add_cors_middleware(app)

# 例外ハンドラーの登録
app.add_exception_handler(FactoryAIException, factory_ai_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# APIルーターの登録
app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.server_host,
        port=settings.server_port,
        reload=True
    )
