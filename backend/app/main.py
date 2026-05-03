from fastapi import FastAPI
from contextlib import asynccontextmanager
import logging

from app.core.config import get_settings
from app.core.logging import setup_logging
from app.core.exceptions import FactoryAIException
from app.middleware.cors import add_cors_middleware
from app.middleware.error_handler import factory_ai_exception_handler, general_exception_handler
from app.api.v1.api import api_router

# Logging setup
logger = setup_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup process
    try:
        settings = get_settings()
        logger.info(f"FastAPI server starting up on {settings.server_host}:{settings.server_port}")
        yield
    except Exception as e:
        logger.error(f"Startup failed: {str(e)}")
        raise
    finally:
        # Shutdown process
        logger.info("FastAPI server shutting down...")

# FastAPI application creation
settings = get_settings()
app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
    lifespan=lifespan
)

# Middleware configuration
add_cors_middleware(app)

# Exception handler registration
app.add_exception_handler(FactoryAIException, factory_ai_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# API router registration
app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.server_host,
        port=settings.server_port,
        reload=True
    )
