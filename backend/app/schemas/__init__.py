from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime
import uuid

# User schemas
class UserBase(BaseModel):
    username: Optional[str] = None
    is_anonymous: bool = False

class UserCreate(UserBase):
    password: Optional[str] = None
    
    @validator('password')
    def validate_password(cls, v, values):
        if not values.get('is_anonymous') and not v:
            raise ValueError('Password required for non-anonymous users')
        return v

class UserLogin(BaseModel):
    username: str
    password: str

class User(UserBase):
    id: str
    created_at: datetime
    last_active: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[str] = None

# Mood schemas
class MoodEntryBase(BaseModel):
    mood_level: int = Field(..., ge=1, le=5, description="Mood level from 1 (very sad) to 5 (very happy)")
    notes: Optional[str] = None
    triggers: Optional[List[str]] = None

class MoodEntryCreate(MoodEntryBase):
    pass

class MoodEntry(MoodEntryBase):
    id: str
    user_id: str
    date: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True

class MoodTrend(BaseModel):
    date: str
    mood_level: float
    notes_count: int

# Journal schemas
class JournalEntryBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=500)
    content: str = Field(..., min_length=1, max_length=10000)
    tags: Optional[List[str]] = None
    ai_prompt: Optional[str] = None
    mood_level: Optional[int] = Field(None, ge=1, le=5)

class JournalEntryCreate(JournalEntryBase):
    pass

class JournalEntryUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    tags: Optional[List[str]] = None

class JournalEntry(JournalEntryBase):
    id: str
    user_id: str
    word_count: int
    date: datetime
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True

class AIPrompt(BaseModel):
    prompt: str
    category: str
    description: str

# Conversation schemas
class MessageBase(BaseModel):
    content: str = Field(..., min_length=1, max_length=2000)

class MessageCreate(MessageBase):
    pass

class Message(MessageBase):
    id: str
    conversation_id: str
    is_user: bool
    timestamp: datetime
    sentiment_score: Optional[float] = None
    
    class Config:
        from_attributes = True

class ConversationBase(BaseModel):
    title: str = "New Conversation"

class ConversationCreate(ConversationBase):
    pass

class Conversation(ConversationBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime
    messages: List[Message] = []
    
    class Config:
        from_attributes = True

class ConversationResponse(BaseModel):
    user_message: Message
    ai_response: Message
    crisis_detected: bool = False
    sentiment_score: Optional[float] = None

# Crisis support schemas
class CrisisResource(BaseModel):
    id: str
    name: str
    description: Optional[str]
    phone_number: Optional[str]
    website: Optional[str]
    availability: Optional[str]
    category: str
    priority: int
    
    class Config:
        from_attributes = True

class CrisisAlert(BaseModel):
    detected: bool
    confidence: float
    keywords: List[str]
    resources: List[CrisisResource]
    message: str

# Analytics schemas (privacy-safe)
class UserStats(BaseModel):
    total_mood_entries: int
    total_journal_entries: int
    total_conversations: int
    average_mood: Optional[float]
    streak_days: int
    last_activity: datetime

class MoodAnalytics(BaseModel):
    weekly_average: float
    monthly_average: float
    trend_direction: str  # "improving", "declining", "stable"
    best_day: Optional[str]
    challenging_day: Optional[str]