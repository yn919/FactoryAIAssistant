from fastapi import APIRouter

router = APIRouter()


@router.get("/", tags=["Root"])
async def root():
    """ルートエンドポイント"""
    return {"message": "Factory AI Assistant API is running"}
