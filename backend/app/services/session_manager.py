"""
Enhanced Session Management Service for MindSpark AI
Provides secure session handling, access control, and user state management
"""
import secrets
import time
import json
from typing import Dict, Any, Optional, Set, List
from datetime import datetime, timedelta
from enum import Enum
import hashlib
import hmac
from itsdangerous import URLSafeTimedSerializer, BadTimeSignature, SignatureExpired
from cryptography.fernet import Fernet


class UserRole(Enum):
    """User roles for access control"""
    ANONYMOUS = "anonymous"
    USER = "user"
    PREMIUM_USER = "premium_user"
    MODERATOR = "moderator"
    ADMIN = "admin"


class SessionStatus(Enum):
    """Session status enumeration"""
    ACTIVE = "active"
    EXPIRED = "expired"
    TERMINATED = "terminated"
    SUSPENDED = "suspended"


class SessionSecurity:
    """Security configuration for sessions"""
    
    def __init__(self):
        self.max_session_duration = 86400  # 24 hours
        self.idle_timeout = 3600  # 1 hour
        self.max_sessions_per_user = 5
        self.require_https = True
        self.same_site_policy = "strict"
        self.secure_cookies = True
        self.session_rotation_interval = 1800  # 30 minutes


class SessionData:
    """Session data container"""
    
    def __init__(self, session_id: str, user_id: str, user_role: UserRole):
        self.session_id = session_id
        self.user_id = user_id
        self.user_role = user_role
        self.created_at = time.time()
        self.last_accessed = time.time()
        self.ip_address: Optional[str] = None
        self.user_agent: Optional[str] = None
        self.status = SessionStatus.ACTIVE
        self.permissions: Set[str] = set()
        self.custom_data: Dict[str, Any] = {}
        self.csrf_token: Optional[str] = None
        self.rotation_count = 0
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert session data to dictionary"""
        return {
            'session_id': self.session_id,
            'user_id': self.user_id,
            'user_role': self.user_role.value,
            'created_at': self.created_at,
            'last_accessed': self.last_accessed,
            'ip_address': self.ip_address,
            'user_agent': self.user_agent,
            'status': self.status.value,
            'permissions': list(self.permissions),
            'custom_data': self.custom_data,
            'csrf_token': self.csrf_token,
            'rotation_count': self.rotation_count
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SessionData':
        """Create session data from dictionary"""
        session = cls(
            session_id=data['session_id'],
            user_id=data['user_id'],
            user_role=UserRole(data['user_role'])
        )
        session.created_at = data['created_at']
        session.last_accessed = data['last_accessed']
        session.ip_address = data.get('ip_address')
        session.user_agent = data.get('user_agent')
        session.status = SessionStatus(data['status'])
        session.permissions = set(data.get('permissions', []))
        session.custom_data = data.get('custom_data', {})
        session.csrf_token = data.get('csrf_token')
        session.rotation_count = data.get('rotation_count', 0)
        return session


class EnhancedSessionManager:
    """Enhanced session management with security features"""
    
    def __init__(self, secret_key: Optional[str] = None):
        self.secret_key = secret_key or secrets.token_hex(32)
        self.serializer = URLSafeTimedSerializer(self.secret_key)
        self.fernet = Fernet(Fernet.generate_key())
        
        # Session storage (in production, use Redis or database)
        self.active_sessions: Dict[str, SessionData] = {}
        self.user_sessions: Dict[str, Set[str]] = {}  # user_id -> session_ids
        
        # Security configuration
        self.security = SessionSecurity()
        
        # Role permissions
        self.role_permissions = {
            UserRole.ANONYMOUS: {'read_public'},
            UserRole.USER: {'read_own_data', 'write_own_data', 'use_ai_chat', 'mood_tracking'},
            UserRole.PREMIUM_USER: {'read_own_data', 'write_own_data', 'use_ai_chat', 'mood_tracking', 'advanced_analytics', 'export_data'},
            UserRole.MODERATOR: {'read_own_data', 'write_own_data', 'use_ai_chat', 'mood_tracking', 'moderate_content', 'view_user_stats'},
            UserRole.ADMIN: {'all_permissions'}
        }
    
    def create_session(self, user_id: str, user_role: UserRole, ip_address: Optional[str] = None, user_agent: Optional[str] = None) -> SessionData:
        """Create a new session"""
        # Check session limits
        self._enforce_session_limits(user_id)
        
        # Generate secure session ID
        session_id = self._generate_session_id(user_id)
        
        # Create session data
        session = SessionData(session_id, user_id, user_role)
        session.ip_address = ip_address
        session.user_agent = user_agent
        session.csrf_token = secrets.token_urlsafe(32)
        
        # Set permissions based on role
        session.permissions = self.role_permissions.get(user_role, set()).copy()
        
        # Store session
        self.active_sessions[session_id] = session
        
        # Track user sessions
        if user_id not in self.user_sessions:
            self.user_sessions[user_id] = set()
        self.user_sessions[user_id].add(session_id)
        
        return session
    
    def validate_session(self, session_id: str, ip_address: Optional[str] = None) -> Optional[SessionData]:
        """Validate and refresh session"""
        if session_id not in self.active_sessions:
            return None
        
        session = self.active_sessions[session_id]
        current_time = time.time()
        
        # Check if session is expired
        if self._is_session_expired(session, current_time):
            self.terminate_session(session_id)
            return None
        
        # Check IP address consistency (if enabled)
        if ip_address and session.ip_address and session.ip_address != ip_address:
            # In production, might want to log this as suspicious activity
            pass
        
        # Update last accessed time
        session.last_accessed = current_time
        
        # Check if session rotation is needed
        if self._should_rotate_session(session, current_time):
            return self._rotate_session(session)
        
        return session
    
    def terminate_session(self, session_id: str) -> bool:
        """Terminate a specific session"""
        if session_id not in self.active_sessions:
            return False
        
        session = self.active_sessions[session_id]
        session.status = SessionStatus.TERMINATED
        
        # Remove from active sessions
        del self.active_sessions[session_id]
        
        # Remove from user sessions
        if session.user_id in self.user_sessions:
            self.user_sessions[session.user_id].discard(session_id)
            if not self.user_sessions[session.user_id]:
                del self.user_sessions[session.user_id]
        
        return True
    
    def terminate_all_user_sessions(self, user_id: str) -> int:
        """Terminate all sessions for a user"""
        if user_id not in self.user_sessions:
            return 0
        
        session_ids = self.user_sessions[user_id].copy()
        terminated_count = 0
        
        for session_id in session_ids:
            if self.terminate_session(session_id):
                terminated_count += 1
        
        return terminated_count
    
    def get_session_info(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session information"""
        if session_id not in self.active_sessions:
            return None
        
        session = self.active_sessions[session_id]
        return session.to_dict()
    
    def has_permission(self, session_id: str, permission: str) -> bool:
        """Check if session has specific permission"""
        session = self.validate_session(session_id)
        if not session:
            return False
        
        # Admin role has all permissions
        if session.user_role == UserRole.ADMIN:
            return True
        
        return permission in session.permissions
    
    def add_permission(self, session_id: str, permission: str) -> bool:
        """Add permission to session"""
        if session_id not in self.active_sessions:
            return False
        
        session = self.active_sessions[session_id]
        session.permissions.add(permission)
        return True
    
    def remove_permission(self, session_id: str, permission: str) -> bool:
        """Remove permission from session"""
        if session_id not in self.active_sessions:
            return False
        
        session = self.active_sessions[session_id]
        session.permissions.discard(permission)
        return True
    
    def set_session_data(self, session_id: str, key: str, value: Any) -> bool:
        """Set custom data in session"""
        if session_id not in self.active_sessions:
            return False
        
        session = self.active_sessions[session_id]
        session.custom_data[key] = value
        return True
    
    def get_session_data(self, session_id: str, key: str) -> Any:
        """Get custom data from session"""
        if session_id not in self.active_sessions:
            return None
        
        session = self.active_sessions[session_id]
        return session.custom_data.get(key)
    
    def get_user_sessions(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all active sessions for a user"""
        if user_id not in self.user_sessions:
            return []
        
        sessions = []
        for session_id in self.user_sessions[user_id]:
            if session_id in self.active_sessions:
                sessions.append(self.active_sessions[session_id].to_dict())
        
        return sessions
    
    def cleanup_expired_sessions(self) -> int:
        """Clean up expired sessions"""
        current_time = time.time()
        expired_sessions = []
        
        for session_id, session in self.active_sessions.items():
            if self._is_session_expired(session, current_time):
                expired_sessions.append(session_id)
        
        for session_id in expired_sessions:
            self.terminate_session(session_id)
        
        return len(expired_sessions)
    
    def get_session_stats(self) -> Dict[str, Any]:
        """Get session statistics"""
        total_sessions = len(self.active_sessions)
        user_sessions_count = len(self.user_sessions)
        
        role_counts = {}
        for session in self.active_sessions.values():
            role = session.user_role.value
            role_counts[role] = role_counts.get(role, 0) + 1
        
        return {
            'total_active_sessions': total_sessions,
            'unique_users': user_sessions_count,
            'sessions_by_role': role_counts,
            'security_config': {
                'max_session_duration': self.security.max_session_duration,
                'idle_timeout': self.security.idle_timeout,
                'max_sessions_per_user': self.security.max_sessions_per_user
            }
        }
    
    def _generate_session_id(self, user_id: str) -> str:
        """Generate secure session ID"""
        timestamp = str(time.time())
        random_data = secrets.token_hex(16)
        combined = f"{user_id}:{timestamp}:{random_data}"
        
        # Create HMAC signature
        signature = hmac.new(
            self.secret_key.encode('utf-8'),
            combined.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        session_id = f"{secrets.token_urlsafe(32)}:{signature[:16]}"
        return session_id
    
    def _enforce_session_limits(self, user_id: str):
        """Enforce session limits per user"""
        if user_id in self.user_sessions:
            current_sessions = len(self.user_sessions[user_id])
            if current_sessions >= self.security.max_sessions_per_user:
                # Remove oldest session
                oldest_session_id = None
                oldest_time = float('inf')
                
                for session_id in self.user_sessions[user_id]:
                    if session_id in self.active_sessions:
                        session = self.active_sessions[session_id]
                        if session.last_accessed < oldest_time:
                            oldest_time = session.last_accessed
                            oldest_session_id = session_id
                
                if oldest_session_id:
                    self.terminate_session(oldest_session_id)
    
    def _is_session_expired(self, session: SessionData, current_time: float) -> bool:
        """Check if session is expired"""
        # Check absolute expiration
        if current_time - session.created_at > self.security.max_session_duration:
            return True
        
        # Check idle timeout
        if current_time - session.last_accessed > self.security.idle_timeout:
            return True
        
        return False
    
    def _should_rotate_session(self, session: SessionData, current_time: float) -> bool:
        """Check if session should be rotated"""
        return (current_time - session.created_at) > (
            self.security.session_rotation_interval * (session.rotation_count + 1)
        )
    
    def _rotate_session(self, old_session: SessionData) -> SessionData:
        """Rotate session ID while preserving session data"""
        # Create new session with same data
        new_session = SessionData(
            self._generate_session_id(old_session.user_id),
            old_session.user_id,
            old_session.user_role
        )
        
        # Copy important data
        new_session.ip_address = old_session.ip_address
        new_session.user_agent = old_session.user_agent
        new_session.permissions = old_session.permissions.copy()
        new_session.custom_data = old_session.custom_data.copy()
        new_session.rotation_count = old_session.rotation_count + 1
        new_session.csrf_token = secrets.token_urlsafe(32)  # New CSRF token
        
        # Update storage
        old_session_id = old_session.session_id
        self.active_sessions[new_session.session_id] = new_session
        
        # Update user sessions tracking
        if old_session.user_id in self.user_sessions:
            self.user_sessions[old_session.user_id].discard(old_session_id)
            self.user_sessions[old_session.user_id].add(new_session.session_id)
        
        # Remove old session
        if old_session_id in self.active_sessions:
            del self.active_sessions[old_session_id]
        
        return new_session


# Global session manager instance
session_manager = EnhancedSessionManager()