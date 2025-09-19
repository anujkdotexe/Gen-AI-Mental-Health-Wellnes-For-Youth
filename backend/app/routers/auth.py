from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm.session import Session
from app.database import get_db
from app.schemas import UserCreate, UserLogin, Token
from app.models import User
from app.services.auth import (
    authenticate_user, 
    create_user, 
    create_access_token,
    get_current_user
)
from datetime import timedelta
import os

router = APIRouter()

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))

@router.post("/register", response_model=dict)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    try:
        db_user = create_user(
            db=db, 
            username=user.username, 
            password=user.password, 
            is_anonymous=user.is_anonymous
        )
        
        # Create access token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": db_user.id}, expires_delta=access_token_expires
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": db_user.id,
                "username": db_user.username,
                "is_anonymous": db_user.is_anonymous
            }
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/login", response_model=dict)
async def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    """Login with username and password"""
    user = authenticate_user(db, user_credentials.username, user_credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "username": user.username,
            "is_anonymous": user.is_anonymous
        }
    }

@router.post("/anonymous", response_model=dict)
async def login_anonymous(db: Session = Depends(get_db)):
    """Create an anonymous user session"""
    try:
        db_user = create_user(db=db, username=None, password=None, is_anonymous=True)
        
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": db_user.id}, expires_delta=access_token_expires
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": db_user.id,
                "username": None,
                "is_anonymous": True
            }
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/me", response_model=dict)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user information"""
    return {
        "id": current_user.id,
        "username": current_user.username,
        "is_anonymous": current_user.is_anonymous,
        "created_at": current_user.created_at,
        "last_active": current_user.last_active
    }

@router.post("/logout")
async def logout():
    """Logout endpoint (client should discard token)"""
    return {"message": "Successfully logged out. Please discard your access token."}

@router.delete("/account")
async def delete_account(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Delete user account and all associated data"""
    try:
        # Delete user and all related data (cascade will handle related records)
        db.delete(current_user)
        db.commit()
        
        return {"message": "Account and all associated data have been permanently deleted"}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete account"
        )

@router.get("/privacy-settings")
async def get_privacy_settings(current_user: User = Depends(get_current_user)):
    """Get user privacy settings"""
    return {
        "data_retention_days": current_user.data_retention_days,
        "allow_analytics": current_user.allow_analytics,
        "is_anonymous": current_user.is_anonymous
    }

@router.put("/privacy-settings")
async def update_privacy_settings(
    settings: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update user privacy settings"""
    try:
        if "data_retention_days" in settings:
            current_user.data_retention_days = settings["data_retention_days"]
        if "allow_analytics" in settings:
            current_user.allow_analytics = settings["allow_analytics"]
        
        db.commit()
        
        return {
            "message": "Privacy settings updated successfully",
            "settings": {
                "data_retention_days": current_user.data_retention_days,
                "allow_analytics": current_user.allow_analytics
            }
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update privacy settings"
        )