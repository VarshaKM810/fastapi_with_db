from fastapi import APIRouter, HTTPException, Depends, Header
from sqlalchemy.orm import Session
from sqlalchemy import func
from db import get_db
from models import ChatHistory
from utils.ai_response import get_completion
from utils.jwt_handler import verify_token
from schemas.ai_response_schemas import AIRequest, AIResponse, ConversationListResponse, ConversationSummary
from schemas.chat_schemas import ChatHistoryResponse, ChatMessage

router = APIRouter()

def get_current_user_id(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    token = authorization.split(" ")[1]
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    return int(payload.get("sub"))

@router.post("/ask", response_model=AIResponse)
def ask_ai(request: AIRequest, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    """Get response from AI model and save to history with session grouping."""
    try:
        # Fetch previous history for this specific conversation to provide context (Memory)
        history = db.query(ChatHistory).filter(
            ChatHistory.user_id == user_id, 
            ChatHistory.conversation_id == request.conversation_id
        ).order_by(ChatHistory.timestamp.asc()).all()

        # Get AI completion with context
        response_text = get_completion(request.message, request.system_prompt, history=history)
        
        # Determine title (use first 30 chars of first message in session if it's new)
        existing_chat = db.query(ChatHistory).filter(ChatHistory.conversation_id == request.conversation_id).first()
        title = existing_chat.title if existing_chat else (request.message[:40] + "...")
        
        # Save User Message
        user_msg = ChatHistory(user_id=user_id, conversation_id=request.conversation_id, title=title, role="user", content=request.message)
        db.add(user_msg)
        
        # Save Assistant Message
        ai_msg = ChatHistory(user_id=user_id, conversation_id=request.conversation_id, title=title, role="assistant", content=response_text)
        db.add(ai_msg)
        
        db.commit()
        return AIResponse(response=response_text)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/conversations", response_model=ConversationListResponse)
def list_conversations(db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    """List all unique conversations for a user."""
    results = db.query(
        ChatHistory.conversation_id, 
        ChatHistory.title, 
        func.max(ChatHistory.timestamp).label("last_updated")
    ).filter(ChatHistory.user_id == user_id).group_by(ChatHistory.conversation_id).order_by(func.max(ChatHistory.timestamp).desc()).all()
    
    return ConversationListResponse(conversations=[
        ConversationSummary(conversation_id=r[0], title=r[1], last_updated=r[2]) for r in results
    ])

@router.get("/history/{conversation_id}", response_model=ChatHistoryResponse)
def get_history(conversation_id: str, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    """Retrieve chat history for a specific conversation session."""
    history = db.query(ChatHistory).filter(
        ChatHistory.user_id == user_id, 
        ChatHistory.conversation_id == conversation_id
    ).order_by(ChatHistory.timestamp.asc()).all()
    return ChatHistoryResponse(messages=[ChatMessage.from_orm(m) for m in history])
