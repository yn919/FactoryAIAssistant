from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.config import settings
from app.services.gemini_service import get_gemini_service
from app.models.chat import ChatRequest, ChatResponse, HealthResponse

# ロギング設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 起動時の処理
    try:
        settings.validate()
        logger.info("FastAPI server starting up...")
        yield
    except Exception as e:
        logger.error(f"Startup failed: {str(e)}")
        raise
    finally:
        # シャットダウン時の処理
        logger.info("FastAPI server shutting down...")

# FastAPIアプリケーション作成
app = FastAPI(
    title="Factory AI Assistant API",
    description="Unityアプリと連携するGemini AIアシスタントAPI",
    version="1.0.0",
    lifespan=lifespan
)

# CORSミドルウェア設定（Unityからのアクセスを許可）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 本番環境では具体的なドメインを指定
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Root"])
async def root():
    """ルートエンドポイント"""
    return {"message": "Factory AI Assistant API is running"}

@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """ヘルスチェックエンドポイント"""
    try:
        gemini_service = get_gemini_service()
        is_healthy = gemini_service.health_check()
        if is_healthy:
            return HealthResponse(status="healthy")
        else:
            raise HTTPException(status_code=503, detail="Gemini API is unavailable")
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=503, detail="Service unavailable")

@app.post("/chat", response_model=ChatResponse, tags=["Chat"])
async def chat(request: ChatRequest):
    """
    チャットエンドポイント
    ユーザーメッセージを受け取り、Gemini AIからの応答を返す
    """
    try:
        # Geminiサービスを使用して応答を生成
        gemini_service = get_gemini_service()
        response_text = await gemini_service.generate_response(
            message=request.message,
            context=request.context
        )
        
        return ChatResponse(response=response_text)
        
    except Exception as e:
        logger.error(f"Chat endpoint error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="チャット処理中にエラーが発生しました"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=True
    )
