from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from app.core.exceptions import FactoryAIException
import logging

logger = logging.getLogger(__name__)


async def factory_ai_exception_handler(request: Request, exc: FactoryAIException):
    """FactoryAIException handler"""
    logger.error(f"FactoryAIException: {exc.message}", extra={"details": exc.details})
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "message": exc.message,
                "status_code": exc.status_code,
                "details": exc.details
            }
        }
    )


async def general_exception_handler(request: Request, exc: Exception):
    """General exception handler"""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "message": "Internal server error occurred",
                "status_code": 500
            }
        }
    )
