from fastapi import APIRouter, Depends, HTTPException
from app.models.chat import HealthResponse
from app.services.gemini_service import GeminiService
from app.core.dependencies import get_gemini_service
from app.core.exceptions import FactoryAIException
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check(gemini_service: GeminiService = Depends(get_gemini_service)):
    """ヘルスチェックエンドポイント"""
    try:
        is_healthy = gemini_service.health_check()
        if is_healthy:
            return HealthResponse(status="healthy")
        else:
            raise HTTPException(status_code=503, detail="Gemini API is unavailable")
    except FactoryAIException as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=503, detail="Service unavailable")
