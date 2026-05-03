from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=1000, description="Chat message")
    context: Optional[str] = Field(None, max_length=500, description="Optional context information")

class ChatResponse(BaseModel):
    response: str = Field(..., description="AI response message")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Response timestamp")

class HealthResponse(BaseModel):
    status: str = Field(default="healthy", description="Server health status")
