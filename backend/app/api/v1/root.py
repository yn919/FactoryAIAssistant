from fastapi import APIRouter

router = APIRouter()


@router.get("/", tags=["Root"])
async def root():
    """Root endpoint"""
    return {"message": "Factory AI Assistant API is running"}
