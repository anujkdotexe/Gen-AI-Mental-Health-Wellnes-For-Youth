from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from datetime import datetime, date, timedelta
from app.database import get_db
from app.schemas import MoodEntry, MoodEntryCreate, MoodTrend
from app.services.auth import get_current_user
from app.models import User, MoodEntry as MoodEntryModel
import json

router = APIRouter()

@router.post("/entries", response_model=dict)
async def create_mood_entry(
    mood_data: MoodEntryCreate,
    current_user: User = Depends(get_current_user),
    db = Depends(get_db)
):
    """Create a new mood entry"""
    try:
        # Check if user already has a mood entry for today
        today = date.today()
        existing_entry = db.query(MoodEntryModel).filter(
            MoodEntryModel.user_id == current_user.id,
            MoodEntryModel.date >= today,
            MoodEntryModel.date < today + timedelta(days=1)
        ).first()
        
        if existing_entry:
            # Update existing entry
            existing_entry.mood_level = mood_data.mood_level
            existing_entry.notes = mood_data.notes
            existing_entry.triggers = json.dumps(mood_data.triggers) if mood_data.triggers else None
            db.commit()
            return {
                "id": existing_entry.id,
                "mood_level": existing_entry.mood_level,
                "notes": existing_entry.notes,
                "triggers": json.loads(existing_entry.triggers) if existing_entry.triggers else [],
                "date": existing_entry.date.isoformat(),
                "message": "Mood entry updated for today"
            }
        else:
            # Create new entry
            import uuid
            db_entry = MoodEntryModel(
                id=str(uuid.uuid4()),
                user_id=current_user.id,
                mood_level=mood_data.mood_level,
                notes=mood_data.notes,
                triggers=json.dumps(mood_data.triggers) if mood_data.triggers else None
            )
            db.add(db_entry)
            db.commit()
            
            return {
                "id": db_entry.id,
                "mood_level": db_entry.mood_level,
                "notes": db_entry.notes,
                "triggers": json.loads(db_entry.triggers) if db_entry.triggers else [],
                "date": db_entry.date.isoformat(),
                "message": "Mood entry created successfully"
            }
            
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create mood entry"
        )

@router.get("/entries/today")
async def get_today_mood(
    current_user: User = Depends(get_current_user),
    db = Depends(get_db)
):
    """Get today's mood entry"""
    today = date.today()
    entry = db.query(MoodEntryModel).filter(
        MoodEntryModel.user_id == current_user.id,
        MoodEntryModel.date >= today,
        MoodEntryModel.date < today + timedelta(days=1)
    ).first()
    
    if not entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No mood entry found for today"
        )
    
    return {
        "id": entry.id,
        "mood_level": entry.mood_level,
        "notes": entry.notes,
        "triggers": json.loads(entry.triggers) if entry.triggers else [],
        "date": entry.date.isoformat()
    }

@router.get("/entries")
async def get_mood_entries(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db = Depends(get_db)
):
    """Get mood entries for a date range"""
    query = db.query(MoodEntryModel).filter(MoodEntryModel.user_id == current_user.id)
    
    if start_date:
        query = query.filter(MoodEntryModel.date >= start_date)
    if end_date:
        query = query.filter(MoodEntryModel.date <= end_date)
    
    entries = query.order_by(MoodEntryModel.date.desc()).all()
    
    return [
        {
            "id": entry.id,
            "mood_level": entry.mood_level,
            "notes": entry.notes,
            "triggers": json.loads(entry.triggers) if entry.triggers else [],
            "date": entry.date.isoformat()
        }
        for entry in entries
    ]

@router.get("/weekly-trend")
async def get_weekly_trend(
    current_user: User = Depends(get_current_user),
    db = Depends(get_db)
):
    """Get weekly mood trend"""
    end_date = date.today()
    start_date = end_date - timedelta(days=7)
    
    entries = db.query(MoodEntryModel).filter(
        MoodEntryModel.user_id == current_user.id,
        MoodEntryModel.date >= start_date,
        MoodEntryModel.date <= end_date
    ).order_by(MoodEntryModel.date).all()
    
    return [
        {
            "date": entry.date.isoformat(),
            "mood_level": entry.mood_level,
            "notes": entry.notes
        }
        for entry in entries
    ]

@router.get("/analytics")
async def get_mood_analytics(
    current_user: User = Depends(get_current_user),
    db = Depends(get_db)
):
    """Get mood analytics and insights"""
    # Get last 30 days of entries
    end_date = date.today()
    start_date = end_date - timedelta(days=30)
    
    entries = db.query(MoodEntryModel).filter(
        MoodEntryModel.user_id == current_user.id,
        MoodEntryModel.date >= start_date,
        MoodEntryModel.date <= end_date
    ).all()
    
    if not entries:
        return {
            "message": "No mood data available for analysis",
            "total_entries": 0
        }
    
    mood_levels = [entry.mood_level for entry in entries]
    average_mood = sum(mood_levels) / len(mood_levels)
    
    # Calculate trend
    if len(entries) >= 7:
        recent_week = mood_levels[-7:]
        previous_week = mood_levels[-14:-7] if len(mood_levels) >= 14 else mood_levels[:-7]
        
        recent_avg = sum(recent_week) / len(recent_week)
        previous_avg = sum(previous_week) / len(previous_week) if previous_week else recent_avg
        
        if recent_avg > previous_avg + 0.2:
            trend = "improving"
        elif recent_avg < previous_avg - 0.2:
            trend = "declining"
        else:
            trend = "stable"
    else:
        trend = "insufficient_data"
    
    return {
        "total_entries": len(entries),
        "average_mood": round(average_mood, 2),
        "trend": trend,
        "best_mood": max(mood_levels),
        "lowest_mood": min(mood_levels),
        "days_tracked": len(entries),
        "streak_days": len(entries)  # Simplified streak calculation
    }