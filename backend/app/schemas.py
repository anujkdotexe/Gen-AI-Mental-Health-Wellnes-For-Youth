"""
Pydantic schemas for MindSpark AI backend
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TokenData(BaseModel):
    user_id: str

class Token(BaseModel):
    access_token: str
    token_type: str

class UserBase(BaseModel):
    username: Optional[str] = None
    is_anonymous: bool = False

class UserCreate(UserBase):
    password: Optional[str] = None

class UserLogin(BaseModel):
    username: str
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    data_retention_days: Optional[int] = None
    allow_analytics: Optional[bool] = None

class UserResponse(UserBase):
    id: str
    created_at: datetime
    last_active: datetime
    data_retention_days: int
    allow_analytics: bool
    
    class Config:
        from_attributes = True

class MoodEntryBase(BaseModel):
    mood_level: int
    notes: Optional[str] = None
    triggers: Optional[str] = None

class MoodEntryCreate(MoodEntryBase):
    pass

class MoodEntryResponse(MoodEntryBase):
    id: str
    user_id: str
    date: datetime
    
    class Config:
        from_attributes = True

class JournalEntryBase(BaseModel):
    title: str
    content: str
    
class JournalEntryCreate(JournalEntryBase):
    mood_level: Optional[int] = None

class JournalEntryResponse(JournalEntryBase):
    id: str
    user_id: str
    mood_level: Optional[int] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class ConversationBase(BaseModel):
    title: Optional[str] = None

class ConversationCreate(ConversationBase):
    pass

class ConversationResponse(ConversationBase):
    id: str
    user_id: str
    created_at: datetime
    
    class Config:
        from_attributes = True