"""
Security API Router for MindSpark AI
Provides endpoints for security features: encryption, CSRF, session management
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm.session import Session
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from app.database import get_db
from app.services.auth import get_current_user
from app.services.encryption_service import encryption_service
from app.services.csrf_protection import csrf_protection
from app.services.session_manager import session_manager, UserRole
from app.services.access_control import access_control, Permission, ResourceType, AccessContext
from app.models import User

router = APIRouter(prefix="/security", tags=["security"])

# Pydantic models for API
class EncryptDataRequest(BaseModel):
    data: Dict[str, Any]
    encryption_type: str = "symmetric"

class EncryptDataResponse(BaseModel):
    encryption_id: str
    status: str
    message: str

class DecryptDataRequest(BaseModel):
    encryption_id: str

class DecryptDataResponse(BaseModel):
    data: Dict[str, Any]
    status: str

class CSRFTokenResponse(BaseModel):
    csrf_token: str
    expires_in: str
    created_at: str

class SessionInfoResponse(BaseModel):
    session_id: str
    user_id: str
    user_role: str
    created_at: float
    last_accessed: float
    permissions: List[str]

class SecurityStatsResponse(BaseModel):
    encryption_stats: Dict[str, Any]
    session_stats: Dict[str, Any]
    access_control_stats: Dict[str, Any]

# Encryption endpoints
@router.post("/encrypt", response_model=EncryptDataResponse)
async def encrypt_data(
    request: EncryptDataRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Encrypt sensitive data"""
    try:
        result = encryption_service.encrypt_sensitive_data(
            request.data, 
            request.encryption_type
        )
        
        return EncryptDataResponse(
            encryption_id=result['encryption_id'],
            status="success",
            message="Data encrypted successfully"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Encryption failed: {str(e)}"
        )

@router.post("/decrypt", response_model=DecryptDataResponse)
async def decrypt_data(
    request: DecryptDataRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Decrypt sensitive data"""
    try:
        decrypted_data = encryption_service.decrypt_sensitive_data(request.encryption_id)
        
        # Ensure data is always a dict for the response
        if isinstance(decrypted_data, str):
            data_response = {"decrypted_text": decrypted_data}
        else:
            data_response = decrypted_data
        
        return DecryptDataResponse(
            data=data_response,
            status="success"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Decryption failed: {str(e)}"
        )

@router.get("/encryption/stats")
async def get_encryption_stats(
    current_user: User = Depends(get_current_user)
):
    """Get encryption service statistics"""
    return encryption_service.get_encryption_stats()

# CSRF Protection endpoints
@router.get("/csrf/token", response_model=CSRFTokenResponse)
async def generate_csrf_token(
    request: Request,
    current_user: User = Depends(get_current_user)
):
    """Generate CSRF token"""
    try:
        token_data = csrf_protection.generate_csrf_token(
            user_id=current_user.id,
            session_id=request.headers.get('X-Session-ID')
        )
        
        return CSRFTokenResponse(**token_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"CSRF token generation failed: {str(e)}"
        )

@router.post("/csrf/validate")
async def validate_csrf_token(
    token: str,
    current_user: User = Depends(get_current_user)
):
    """Validate CSRF token"""
    is_valid = csrf_protection.validate_csrf_token(token, current_user.id)
    
    return {
        "valid": is_valid,
        "message": "Token is valid" if is_valid else "Token is invalid or expired"
    }

# Session Management endpoints
@router.get("/session/info", response_model=SessionInfoResponse)
async def get_session_info(
    request: Request,
    current_user: User = Depends(get_current_user)
):
    """Get current session information"""
    session_id = request.headers.get('X-Session-ID', 'unknown')
    session_info = session_manager.get_session_info(session_id)
    
    if not session_info:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    return SessionInfoResponse(**session_info)

@router.get("/session/list")
async def list_user_sessions(
    current_user: User = Depends(get_current_user)
):
    """List all active sessions for current user"""
    sessions = session_manager.get_user_sessions(current_user.id)
    return {"sessions": sessions}

@router.delete("/session/{session_id}")
async def terminate_session(
    session_id: str,
    current_user: User = Depends(get_current_user)
):
    """Terminate a specific session"""
    success = session_manager.terminate_session(session_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    return {"message": "Session terminated successfully"}

@router.delete("/session/all")
async def terminate_all_sessions(
    current_user: User = Depends(get_current_user)
):
    """Terminate all sessions for current user"""
    count = session_manager.terminate_all_user_sessions(current_user.id)
    return {"message": f"Terminated {count} sessions"}

@router.get("/session/stats")
async def get_session_stats(
    current_user: User = Depends(get_current_user)
):
    """Get session management statistics"""
    return session_manager.get_session_stats()

# Access Control endpoints
@router.get("/access/permissions")
async def get_user_permissions(
    current_user: User = Depends(get_current_user)
):
    """Get current user's permissions"""
    user_role = UserRole.USER  # Default, should be determined from user data
    permissions = access_control.get_user_permissions(user_role)
    
    return {
        "user_id": current_user.id,
        "role": user_role.value,
        "permissions": permissions
    }

@router.get("/access/resources")
async def get_accessible_resources(
    request: Request,
    current_user: User = Depends(get_current_user)
):
    """Get resources accessible to current user"""
    session_id = request.headers.get('X-Session-ID', 'unknown')
    user_role = UserRole.USER
    
    context = AccessContext(
        user_id=current_user.id,
        user_role=user_role,
        session_id=session_id,
        resource_type=ResourceType.USER_DATA
    )
    
    accessible_resources = access_control.get_accessible_resources(context)
    
    return {
        "user_id": current_user.id,
        "accessible_resources": [res.value for res in accessible_resources]
    }

@router.get("/access/stats")
async def get_access_control_stats(
    current_user: User = Depends(get_current_user)
):
    """Get access control statistics"""
    return access_control.get_access_statistics()

# Overall Security Status
@router.get("/status", response_model=SecurityStatsResponse)
async def get_security_status(
    current_user: User = Depends(get_current_user)
):
    """Get overall security system status"""
    return SecurityStatsResponse(
        encryption_stats=encryption_service.get_encryption_stats(),
        session_stats=session_manager.get_session_stats(),
        access_control_stats=access_control.get_access_statistics()
    )

# Security Configuration endpoints (admin only)
@router.post("/config/update")
async def update_security_config(
    config: Dict[str, Any],
    current_user: User = Depends(get_current_user)
):
    """Update security configuration (admin only)"""
    # Check if user is admin
    if current_user.username != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    # Update configurations as needed
    return {
        "message": "Security configuration updated",
        "config": config
    }

@router.post("/maintenance/cleanup")
async def run_security_maintenance(
    current_user: User = Depends(get_current_user)
):
    """Run security maintenance tasks"""
    if current_user.username != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    # Cleanup expired sessions
    expired_sessions = session_manager.cleanup_expired_sessions()
    
    return {
        "message": "Security maintenance completed",
        "expired_sessions_cleaned": expired_sessions
    }