from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=1000, description="チャットメッセージ")
    context: Optional[str] = Field(None, max_length=500, description="オプションのコンテキスト情報")

class ChatResponse(BaseModel):
    response: str = Field(..., description="AIからの応答メッセージ")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="応答タイムスタンプ")

class HealthResponse(BaseModel):
    status: str = Field(default="healthy", description="サーバーの健康状態")
