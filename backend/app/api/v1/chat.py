from fastapi import APIRouter, Depends, HTTPException
from app.models.chat import ChatRequest, ChatResponse
from app.services.gemini_service import GeminiService
from app.core.dependencies import get_gemini_service
from app.core.exceptions import FactoryAIException
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/chat", response_model=ChatResponse, tags=["Chat"])
async def chat(
    request: ChatRequest,
    gemini_service: GeminiService = Depends(get_gemini_service)
):
    """
    チャットエンドポイント
    ユーザーメッセージを受け取り、Gemini AIからの応答を返す
    """
    try:
        # Geminiサービスを使用して応答を生成
        response_text = await gemini_service.generate_response(
            message=request.message,
            context=request.context
        )
        
        return ChatResponse(response=response_text)
        
    except FactoryAIException as e:
        logger.error(f"Chat endpoint error: {str(e)}")
        raise HTTPException(
            status_code=e.status_code,
            detail=e.message
        )
    except Exception as e:
        logger.error(f"Chat endpoint error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="チャット処理中にエラーが発生しました"
        )
