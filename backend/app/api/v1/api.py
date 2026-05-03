from fastapi import APIRouter
from app.api.v1 import chat, health, root

api_router = APIRouter()

# Register each router
api_router.include_router(root.router, tags=["Root"])
api_router.include_router(health.router, prefix="/api/v1", tags=["Health"])
api_router.include_router(chat.router, prefix="/api/v1", tags=["Chat"])
