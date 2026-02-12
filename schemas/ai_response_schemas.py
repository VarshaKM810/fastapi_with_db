from pydantic import BaseModel
from datetime import datetime

class AIRequest(BaseModel):
    message: str
    conversation_id: str # Required to group sessions
    system_prompt: str = "You are a helpful assistant."

class AIResponse(BaseModel):
    response: str

class ConversationSummary(BaseModel):
    conversation_id: str
    title: str
    last_updated: datetime

class ConversationListResponse(BaseModel):
    conversations: list[ConversationSummary]
