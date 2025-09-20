r"""
CSRF Protection Middleware for MindSpark AI
Provides Cross-Site Request Forgery protection for API endpoints
"""
import secrets
import hmac
import hashlib
import time
from typing import Dict, Any, Optional, Set
from datetime import datetime, timedelta
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from itsdangerous import URLSafeTimedSerializer, BadTimeSignature, SignatureExpired
import json


class CSRFProtection:
    """CSRF Protection service with token generation and validation"""
    
    def __init__(self, secret_key: Optional[str] = None):
        self.secret_key = secret_key or secrets.token_hex(32)
        self.serializer = URLSafeTimedSerializer(self.secret_key)
        
        # Token storage (in production, use Redis or database)
        self.valid_tokens: Dict[str, Dict[str, Any]] = {}
        self.token_expiry = 3600  # 1 hour
        
        # Protected endpoints
        self.protected_methods = {'POST', 'PUT', 'DELETE', 'PATCH'}
        self.exempt_paths: Set[str] = {
            '/auth/login',
            '/auth/register',
            '/docs',
            '/openapi.json',
            '/health'
        }
        
        # Rate limiting for token generation
        self.token_generation_limit = {}
        self.generation_limit_per_ip = 10  # per hour
        
    def generate_csrf_token(self, user_id: Optional[str] = None, session_id: Optional[str] = None) -> Dict[str, Any]:
        """Generate a new CSRF token"""
        token_data = {
            'user_id': user_id,
            'session_id': session_id,
            'created_at': datetime.now().isoformat(),
            'nonce': secrets.token_hex(16)
        }
        
        # Create signed token
        csrf_token = self.serializer.dumps(token_data)
        token_str = str(csrf_token)
        
        # Store token metadata
        self.valid_tokens[token_str] = {
            'data': token_data,
            'created_at': time.time(),
            'used': False
        }
        
        # Clean expired tokens
        self._cleanup_expired_tokens()
        
        return {
            'csrf_token': token_str,
            'expires_in': str(self.token_expiry),
            'created_at': token_data['created_at']
        }
    
    def validate_csrf_token(self, token: str, user_id: Optional[str] = None, max_age: Optional[int] = None) -> bool:
        """Validate CSRF token"""
        try:
            if not token:
                return False
            
            # Check if token exists in our storage
            if token not in self.valid_tokens:
                return False
            
            token_info = self.valid_tokens[token]
            
            # Check if token is already used (for one-time use)
            if token_info.get('used', False):
                return False
            
            # Verify token signature and age
            max_age = max_age or self.token_expiry
            token_data = self.serializer.loads(token, max_age=max_age)
            
            # Validate user ID if provided
            if user_id and token_data.get('user_id') != user_id:
                return False
            
            # Mark token as used
            self.valid_tokens[token]['used'] = True
            
            return True
            
        except (BadTimeSignature, SignatureExpired, KeyError) as e:
            print(f"CSRF token validation failed: {e}")
            return False
    
    def _cleanup_expired_tokens(self):
        """Remove expired tokens from storage"""
        current_time = time.time()
        expired_tokens = []
        
        for token, info in self.valid_tokens.items():
            if current_time - info['created_at'] > self.token_expiry:
                expired_tokens.append(token)
        
        for token in expired_tokens:
            del self.valid_tokens[token]
    
    def is_exempt_path(self, path: str) -> bool:
        """Check if path is exempt from CSRF protection"""
        return path in self.exempt_paths or path.startswith('/static/')
    
    def check_rate_limit(self, client_ip: str) -> bool:
        """Check rate limit for token generation"""
        current_time = time.time()
        hour_ago = current_time - 3600
        
        # Clean old entries
        if client_ip in self.token_generation_limit:
            self.token_generation_limit[client_ip] = [
                timestamp for timestamp in self.token_generation_limit[client_ip]
                if timestamp > hour_ago
            ]
        else:
            self.token_generation_limit[client_ip] = []
        
        # Check limit
        if len(self.token_generation_limit[client_ip]) >= self.generation_limit_per_ip:
            return False
        
        # Add current request
        self.token_generation_limit[client_ip].append(current_time)
        return True
    
    async def csrf_middleware(self, request: Request, call_next):
        """CSRF protection middleware"""
        # Skip for exempt paths
        if self.is_exempt_path(request.url.path):
            response = await call_next(request)
            return response
        
        # Skip for safe methods
        if request.method not in self.protected_methods:
            response = await call_next(request)
            return response
        
        # Extract CSRF token from headers or form data
        csrf_token = None
        
        # Check X-CSRF-Token header
        if 'X-CSRF-Token' in request.headers:
            csrf_token = request.headers['X-CSRF-Token']
        
        # Check Authorization header for token
        elif 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('CSRF '):
                csrf_token = auth_header[5:]
        
        # For form data, check body (if content-type allows)
        elif request.headers.get('content-type', '').startswith('application/x-www-form-urlencoded'):
            try:
                form_data = await request.form()
                csrf_token_field = form_data.get('csrf_token')
                csrf_token = str(csrf_token_field) if csrf_token_field else None
            except:
                pass
        
        # Validate token
        if not csrf_token or not self.validate_csrf_token(csrf_token):
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={
                    'error': 'CSRF_TOKEN_INVALID',
                    'message': 'Invalid or missing CSRF token',
                    'code': 'CSRF_PROTECTION_FAILED'
                }
            )
        
        # Continue with request
        response = await call_next(request)
        return response


class DoubleSubmitCookieCSRF:
    """Double Submit Cookie CSRF Protection"""
    
    def __init__(self, secret_key: Optional[str] = None):
        self.secret_key = secret_key or secrets.token_hex(32)
        self.cookie_name = 'csrf_token'
        self.header_name = 'X-CSRF-Token'
        
    def generate_token(self) -> str:
        """Generate CSRF token for double submit cookie"""
        return secrets.token_urlsafe(32)
    
    def create_signed_token(self, token: str, user_id: Optional[str] = None) -> str:
        """Create signed version of token"""
        data = {
            'token': token,
            'user_id': user_id,
            'timestamp': time.time()
        }
        
        message = json.dumps(data, separators=(',', ':')).encode('utf-8')
        signature = hmac.new(
            self.secret_key.encode('utf-8'),
            message,
            hashlib.sha256
        ).hexdigest()
        
        return f"{token}.{signature}"
    
    def verify_signed_token(self, signed_token: str, user_id: Optional[str] = None) -> bool:
        """Verify signed token"""
        try:
            if '.' not in signed_token:
                return False
            
            token, signature = signed_token.rsplit('.', 1)
            
            # Recreate signature
            data = {
                'token': token,
                'user_id': user_id,
                'timestamp': time.time()  # Note: In production, include original timestamp
            }
            
            message = json.dumps(data, separators=(',', ':')).encode('utf-8')
            expected_signature = hmac.new(
                self.secret_key.encode('utf-8'),
                message,
                hashlib.sha256
            ).hexdigest()
            
            return hmac.compare_digest(signature, expected_signature)
            
        except Exception:
            return False
    
    async def double_submit_middleware(self, request: Request, call_next):
        """Double submit cookie CSRF middleware"""
        # Skip for safe methods and exempt paths
        if (request.method not in {'POST', 'PUT', 'DELETE', 'PATCH'} or
            request.url.path in {'/auth/login', '/auth/register', '/docs', '/openapi.json'}):
            response = await call_next(request)
            return response
        
        # Get token from cookie
        cookie_token = request.cookies.get(self.cookie_name)
        
        # Get token from header
        header_token = request.headers.get(self.header_name)
        
        # Both tokens must be present and match
        if not cookie_token or not header_token or cookie_token != header_token:
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={
                    'error': 'CSRF_TOKEN_MISMATCH',
                    'message': 'CSRF token mismatch between cookie and header',
                    'code': 'DOUBLE_SUBMIT_FAILED'
                }
            )
        
        response = await call_next(request)
        return response


class CSRFConfig:
    """CSRF Configuration and management"""
    
    def __init__(self):
        self.csrf_protection = CSRFProtection()
        self.double_submit = DoubleSubmitCookieCSRF()
        
        # Configuration
        self.protection_mode = 'standard'  # 'standard', 'double_submit', 'both'
        self.token_expiry = 3600
        self.same_site_policy = 'strict'
        self.secure_cookies = True
        
    def get_csrf_config(self) -> Dict[str, Any]:
        """Get current CSRF configuration"""
        return {
            'protection_mode': self.protection_mode,
            'token_expiry': self.token_expiry,
            'same_site_policy': self.same_site_policy,
            'secure_cookies': self.secure_cookies,
            'active_tokens': len(self.csrf_protection.valid_tokens),
            'exempt_paths': list(self.csrf_protection.exempt_paths)
        }
    
    def update_config(self, config: Dict[str, Any]) -> Dict[str, str]:
        """Update CSRF configuration"""
        if 'protection_mode' in config:
            self.protection_mode = config['protection_mode']
        
        if 'token_expiry' in config:
            self.token_expiry = config['token_expiry']
            self.csrf_protection.token_expiry = config['token_expiry']
        
        if 'exempt_paths' in config:
            self.csrf_protection.exempt_paths.update(config['exempt_paths'])
        
        return {'status': 'updated', 'timestamp': datetime.now().isoformat()}
    
    async def apply_csrf_protection(self, request: Request, call_next):
        """Apply configured CSRF protection"""
        if self.protection_mode == 'standard':
            return await self.csrf_protection.csrf_middleware(request, call_next)
        elif self.protection_mode == 'double_submit':
            return await self.double_submit.double_submit_middleware(request, call_next)
        elif self.protection_mode == 'both':
            # Apply both protections
            response = await self.csrf_protection.csrf_middleware(request, call_next)
            if response.status_code == 200:
                return await self.double_submit.double_submit_middleware(request, call_next)
            return response
        else:
            return await call_next(request)


# Global CSRF protection instances
csrf_config = CSRFConfig()
csrf_protection = csrf_config.csrf_protection
double_submit_csrf = csrf_config.double_submit