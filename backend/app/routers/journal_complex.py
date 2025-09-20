"""
Simple Journal API Router
Basic CRUD operations for journal entries matching frontend expectations
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, JournalEntry
from app.services.auth import get_current_user
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

# Simple Pydantic schemas matching frontend expectations
class JournalEntryCreateRequest(BaseModel):
    title: Optional[str] = None
    content: str
    mood: Optional[str] = None

class JournalEntryUpdateRequest(BaseModel):
    title: Optional[str] = None
    content: str
    mood: Optional[str] = None

class JournalEntryResponse(BaseModel):
    id: str
    user_id: str
    title: Optional[str]
    content: str
    mood: Optional[str]
    created_at: str
    updated_at: str

@router.get("/entries", response_model=List[JournalEntryResponse])
async def get_journal_entries(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get journal entries for the current user"""
    try:
        entries = db.query(JournalEntry).filter(
            JournalEntry.user_id == current_user.id
        ).order_by(JournalEntry.created_at.desc()).all()
        
        return [
            JournalEntryResponse(
                id=entry.id,
                user_id=entry.user_id,
                title=entry.title,
                content=entry.content,
                mood=str(entry.mood_level) if entry.mood_level else None,
                created_at=entry.created_at.isoformat(),
                updated_at=entry.updated_at.isoformat() if entry.updated_at else entry.created_at.isoformat()
            )
            for entry in entries
        ]
        
    except Exception as e:
        logger.error(f"Error retrieving journal entries for user {current_user.id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve journal entries"
        )

@router.get("/entries/{entry_id}", response_model=JournalEntryResponse)
async def get_journal_entry(
    entry_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific journal entry"""
    try:
        entry = db.query(JournalEntry).filter(
            JournalEntry.id == entry_id,
            JournalEntry.user_id == current_user.id
        ).first()
        
        if not entry:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Journal entry not found"
            )
        
        return JournalEntryResponse(
            id=entry.id,
            user_id=entry.user_id,
            title=entry.title,
            content=entry.content,
            mood=str(entry.mood_level) if entry.mood_level else None,
            created_at=entry.created_at.isoformat(),
            updated_at=entry.updated_at.isoformat() if entry.updated_at else entry.created_at.isoformat()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving journal entry {entry_id} for user {current_user.id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve journal entry"
        )

@router.post("/entries", response_model=JournalEntryResponse)
async def create_journal_entry(
    entry_data: JournalEntryCreateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new journal entry"""
    try:
        # Convert mood string to integer if provided
        mood_level = None
        if entry_data.mood:
            try:
                mood_level = int(entry_data.mood)
            except ValueError:
                # If mood is not a number, store it as part of content or ignore
                pass
        
        new_entry = JournalEntry(
            user_id=current_user.id,
            title=entry_data.title or "Untitled Entry",
            content=entry_data.content,
            mood_level=mood_level,
            word_count=len(entry_data.content.split())
        )
        
        db.add(new_entry)
        db.commit()
        db.refresh(new_entry)
        
        return JournalEntryResponse(
            id=new_entry.id,
            user_id=new_entry.user_id,
            title=new_entry.title,
            content=new_entry.content,
            mood=str(new_entry.mood_level) if new_entry.mood_level else None,
            created_at=new_entry.created_at.isoformat(),
            updated_at=new_entry.updated_at.isoformat() if new_entry.updated_at else new_entry.created_at.isoformat()
        )
        
    except Exception as e:
        logger.error(f"Error creating journal entry for user {current_user.id}: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create journal entry"
        )

@router.put("/entries/{entry_id}", response_model=JournalEntryResponse)
async def update_journal_entry(
    entry_id: str,
    entry_data: JournalEntryUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update an existing journal entry"""
    try:
        entry = db.query(JournalEntry).filter(
            JournalEntry.id == entry_id,
            JournalEntry.user_id == current_user.id
        ).first()
        
        if not entry:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Journal entry not found"
            )
        
        # Convert mood string to integer if provided
        mood_level = None
        if entry_data.mood:
            try:
                mood_level = int(entry_data.mood)
            except ValueError:
                pass
        
        # Update entry fields
        if entry_data.title is not None:
            entry.title = entry_data.title
        entry.content = entry_data.content
        entry.mood_level = mood_level
        entry.word_count = len(entry_data.content.split())
        entry.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(entry)
        
        return JournalEntryResponse(
            id=entry.id,
            user_id=entry.user_id,
            title=entry.title,
            content=entry.content,
            mood=str(entry.mood_level) if entry.mood_level else None,
            created_at=entry.created_at.isoformat(),
            updated_at=entry.updated_at.isoformat()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating journal entry {entry_id} for user {current_user.id}: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update journal entry"
        )

@router.delete("/entries/{entry_id}")
async def delete_journal_entry(
    entry_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a journal entry"""
    try:
        entry = db.query(JournalEntry).filter(
            JournalEntry.id == entry_id,
            JournalEntry.user_id == current_user.id
        ).first()
        
        if not entry:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Journal entry not found"
            )
        
        db.delete(entry)
        db.commit()
        
        return {"message": "Journal entry deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting journal entry {entry_id} for user {current_user.id}: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete journal entry"
        )