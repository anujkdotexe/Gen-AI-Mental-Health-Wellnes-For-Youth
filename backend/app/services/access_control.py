"""
Access Control Service for MindSpark AI
Provides role-based access control and permission management
"""
from enum import Enum
from typing import Dict, Set, List, Optional, Any
from dataclasses import dataclass
from functools import wraps
from fastapi import HTTPException, status, Depends, Request
from sqlalchemy.orm.session import Session
from app.models import User
from app.services.session_manager import session_manager, UserRole
import time


class Permission(Enum):
    """System permissions"""
    # Data permissions
    READ_OWN_DATA = "read_own_data"
    WRITE_OWN_DATA = "write_own_data"
    DELETE_OWN_DATA = "delete_own_data"
    EXPORT_OWN_DATA = "export_own_data"
    
    # Feature permissions
    USE_AI_CHAT = "use_ai_chat"
    MOOD_TRACKING = "mood_tracking"
    JOURNAL_WRITING = "journal_writing"
    CRISIS_SUPPORT = "crisis_support"
    ADVANCED_ANALYTICS = "advanced_analytics"
    
    # Administrative permissions
    VIEW_USER_STATS = "view_user_stats"
    MODERATE_CONTENT = "moderate_content"
    MANAGE_CRISIS_RESOURCES = "manage_crisis_resources"
    SYSTEM_ADMIN = "system_admin"
    
    # Security permissions
    MANAGE_SECURITY = "manage_security"
    VIEW_AUDIT_LOGS = "view_audit_logs"
    ENCRYPT_DATA = "encrypt_data"
    BLOCKCHAIN_VERIFY = "blockchain_verify"


class ResourceType(Enum):
    """System resources"""
    USER_DATA = "user_data"
    MOOD_ENTRY = "mood_entry"
    JOURNAL_ENTRY = "journal_entry"
    CONVERSATION = "conversation"
    CRISIS_RESOURCE = "crisis_resource"
    AI_MODEL = "ai_model"
    SYSTEM_CONFIG = "system_config"
    AUDIT_LOG = "audit_log"


@dataclass
class AccessContext:
    """Context for access control decisions"""
    user_id: str
    user_role: UserRole
    session_id: str
    resource_type: ResourceType
    resource_id: Optional[str] = None
    action: str = "read"
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    timestamp: Optional[float] = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = time.time()


class AccessControlService:
    """Role-based access control service"""
    
    def __init__(self):
        # Role-based permissions mapping
        self.role_permissions: Dict[UserRole, Set[Permission]] = {
            UserRole.ANONYMOUS: {
                Permission.USE_AI_CHAT,
                Permission.MOOD_TRACKING,
                Permission.CRISIS_SUPPORT,
            },
            UserRole.USER: {
                Permission.READ_OWN_DATA,
                Permission.WRITE_OWN_DATA,
                Permission.DELETE_OWN_DATA,
                Permission.USE_AI_CHAT,
                Permission.MOOD_TRACKING,
                Permission.JOURNAL_WRITING,
                Permission.CRISIS_SUPPORT,
            },
            UserRole.PREMIUM_USER: {
                Permission.READ_OWN_DATA,
                Permission.WRITE_OWN_DATA,
                Permission.DELETE_OWN_DATA,
                Permission.EXPORT_OWN_DATA,
                Permission.USE_AI_CHAT,
                Permission.MOOD_TRACKING,
                Permission.JOURNAL_WRITING,
                Permission.CRISIS_SUPPORT,
                Permission.ADVANCED_ANALYTICS,
                Permission.ENCRYPT_DATA,
                Permission.BLOCKCHAIN_VERIFY,
            },
            UserRole.MODERATOR: {
                Permission.READ_OWN_DATA,
                Permission.WRITE_OWN_DATA,
                Permission.DELETE_OWN_DATA,
                Permission.USE_AI_CHAT,
                Permission.MOOD_TRACKING,
                Permission.JOURNAL_WRITING,
                Permission.CRISIS_SUPPORT,
                Permission.VIEW_USER_STATS,
                Permission.MODERATE_CONTENT,
                Permission.MANAGE_CRISIS_RESOURCES,
            },
            UserRole.ADMIN: set(Permission),  # All permissions
        }
        
        # Resource ownership rules
        self.ownership_rules: Dict[ResourceType, str] = {
            ResourceType.USER_DATA: "user_id",
            ResourceType.MOOD_ENTRY: "user_id",
            ResourceType.JOURNAL_ENTRY: "user_id",
            ResourceType.CONVERSATION: "user_id",
        }
        
        # Rate limiting
        self.rate_limits: Dict[str, List[float]] = {}
        
        # Access log
        self.access_log: List[Dict[str, Any]] = []
    
    def check_permission(self, context: AccessContext, permission: Permission) -> bool:
        """Check if user has specific permission"""
        user_permissions = self.role_permissions.get(context.user_role, set())
        
        # Admin role has all permissions
        if context.user_role == UserRole.ADMIN:
            return True
        
        return permission in user_permissions
    
    def check_resource_access(self, context: AccessContext, resource_data: Optional[Dict[str, Any]] = None) -> bool:
        """Check if user can access specific resource"""
        # Check basic permission first
        if context.action == "read" and not self.check_permission(context, Permission.READ_OWN_DATA):
            return False
        elif context.action == "write" and not self.check_permission(context, Permission.WRITE_OWN_DATA):
            return False
        elif context.action == "delete" and not self.check_permission(context, Permission.DELETE_OWN_DATA):
            return False
        
        # Check resource ownership
        if context.resource_type in self.ownership_rules:
            ownership_field = self.ownership_rules[context.resource_type]
            
            if resource_data and ownership_field in resource_data:
                resource_owner = resource_data[ownership_field]
                
                # Users can only access their own resources (unless admin/moderator)
                if context.user_role not in [UserRole.ADMIN, UserRole.MODERATOR]:
                    if resource_owner != context.user_id:
                        return False
        
        return True
    
    def enforce_rate_limit(self, context: AccessContext, limit: int = 100, window: int = 3600) -> bool:
        """Enforce rate limiting per user"""
        current_time = time.time()
        user_key = f"{context.user_id}:{context.action}:{context.resource_type.value}"
        
        if user_key not in self.rate_limits:
            self.rate_limits[user_key] = []
        
        # Clean old requests
        self.rate_limits[user_key] = [
            req_time for req_time in self.rate_limits[user_key]
            if current_time - req_time < window
        ]
        
        # Check limit
        if len(self.rate_limits[user_key]) >= limit:
            return False
        
        # Add current request
        self.rate_limits[user_key].append(current_time)
        return True
    
    def log_access(self, context: AccessContext, granted: bool, reason: Optional[str] = None):
        """Log access attempt"""
        log_entry = {
            'timestamp': context.timestamp,
            'user_id': context.user_id,
            'user_role': context.user_role.value,
            'session_id': context.session_id,
            'resource_type': context.resource_type.value,
            'resource_id': context.resource_id,
            'action': context.action,
            'granted': granted,
            'reason': reason,
            'ip_address': context.ip_address,
            'user_agent': context.user_agent[:100] if context.user_agent else None,
        }
        
        self.access_log.append(log_entry)
        
        # Keep only recent logs (in production, store in database)
        if len(self.access_log) > 10000:
            self.access_log = self.access_log[-5000:]
    
    def get_user_permissions(self, user_role: UserRole) -> List[str]:
        """Get list of permissions for user role"""
        permissions = self.role_permissions.get(user_role, set())
        return [perm.value for perm in permissions]
    
    def can_access_feature(self, context: AccessContext, feature: str) -> bool:
        """Check if user can access specific feature"""
        feature_permissions = {
            'ai_chat': Permission.USE_AI_CHAT,
            'mood_tracking': Permission.MOOD_TRACKING,
            'journal': Permission.JOURNAL_WRITING,
            'crisis_support': Permission.CRISIS_SUPPORT,
            'analytics': Permission.ADVANCED_ANALYTICS,
            'admin_panel': Permission.SYSTEM_ADMIN,
            'moderation': Permission.MODERATE_CONTENT,
        }
        
        required_permission = feature_permissions.get(feature)
        if not required_permission:
            return False
        
        return self.check_permission(context, required_permission)
    
    def get_accessible_resources(self, context: AccessContext) -> List[ResourceType]:
        """Get list of resources user can access"""
        accessible = []
        
        for resource_type in ResourceType:
            test_context = AccessContext(
                user_id=context.user_id,
                user_role=context.user_role,
                session_id=context.session_id,
                resource_type=resource_type,
                action="read"
            )
            
            if self.check_resource_access(test_context):
                accessible.append(resource_type)
        
        return accessible
    
    def validate_data_access(self, context: AccessContext, encryption_required: bool = False) -> bool:
        """Validate access to sensitive data"""
        # Check basic permissions
        if not self.check_resource_access(context):
            return False
        
        # For encrypted data, check encryption permission
        if encryption_required:
            if not self.check_permission(context, Permission.ENCRYPT_DATA):
                return False
        
        # Additional security checks for premium features
        if context.user_role == UserRole.PREMIUM_USER:
            if not self.check_permission(context, Permission.BLOCKCHAIN_VERIFY):
                return False
        
        return True
    
    def get_access_statistics(self) -> Dict[str, Any]:
        """Get access control statistics"""
        if not self.access_log:
            return {'total_requests': 0}
        
        total_requests = len(self.access_log)
        granted_requests = sum(1 for log in self.access_log if log['granted'])
        denied_requests = total_requests - granted_requests
        
        # Requests by role
        role_stats = {}
        for log in self.access_log:
            role = log['user_role']
            role_stats[role] = role_stats.get(role, 0) + 1
        
        # Requests by resource type
        resource_stats = {}
        for log in self.access_log:
            resource = log['resource_type']
            resource_stats[resource] = resource_stats.get(resource, 0) + 1
        
        return {
            'total_requests': total_requests,
            'granted_requests': granted_requests,
            'denied_requests': denied_requests,
            'success_rate': granted_requests / total_requests if total_requests > 0 else 0,
            'requests_by_role': role_stats,
            'requests_by_resource': resource_stats,
            'rate_limited_users': len(self.rate_limits),
        }


# Decorator for access control
def require_permission(permission: Permission, resource_type: Optional[ResourceType] = None):
    """Decorator to require specific permission for endpoint"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Extract request and user from arguments
            request = None
            current_user = None
            
            for arg in args:
                if isinstance(arg, Request):
                    request = arg
                elif hasattr(arg, 'id') and hasattr(arg, 'username'):  # User object
                    current_user = arg
            
            if not current_user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authentication required"
                )
            
            # Create access context
            session_id = request.headers.get('X-Session-ID', 'unknown') if request else 'unknown'
            user_role = UserRole.USER  # Default, should be determined from user data
            
            context = AccessContext(
                user_id=current_user.id,
                user_role=user_role,
                session_id=session_id,
                resource_type=resource_type or ResourceType.USER_DATA,
                action="access",
                ip_address=getattr(request.client, 'host', None) if request and hasattr(request, 'client') else None,
                user_agent=request.headers.get('User-Agent') if request else None,
            )
            
            # Check permission
            if not access_control.check_permission(context, permission):
                access_control.log_access(context, False, f"Missing permission: {permission.value}")
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Insufficient permissions: {permission.value} required"
                )
            
            # Check rate limiting
            if not access_control.enforce_rate_limit(context):
                access_control.log_access(context, False, "Rate limit exceeded")
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail="Rate limit exceeded"
                )
            
            # Log successful access
            access_control.log_access(context, True)
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator


# Global access control instance
access_control = AccessControlService()