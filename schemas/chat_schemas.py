from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ChatMessage(BaseModel):
    role: str
    content: str
    timestamp: Optional[datetime] = None

    class Config:
        from_attributes = True

class ChatHistoryResponse(BaseModel):
    messages: list[ChatMessage]
