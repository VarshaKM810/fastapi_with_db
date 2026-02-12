from db import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer ,primary_key=True,index=True)
    email = Column(String,unique=True,index=True)
    password = Column(String)

class ChatHistory(Base):
    __tablename__ = "chat_history"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    conversation_id = Column(String, index=True) # Unique ID for each chat session
    title = Column(String, default="New Chat")
    role = Column(String) # 'user' or 'assistant'
    content = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
