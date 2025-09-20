from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm.session import Session
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.models import User
from app.schemas import TokenData
from app.database import get_db
import os
import uuid

# Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-super-secret-key-change-this-in-production")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Security
security = HTTPBearer()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> TokenData:
    """Verify and decode a JWT token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None or not isinstance(user_id, str):
            raise credentials_exception
        token_data = TokenData(user_id=user_id)
    except JWTError:
        raise credentials_exception
    return token_data

def get_user_by_username(db: Session, username: str) -> Optional[User]:
    """Get user by username"""
    if db is None:
        raise ValueError("Database session is None")
    return db.query(User).filter(User.username == username).first()  # type: ignore

def get_user_by_id(db: Session, user_id: str) -> Optional[User]:
    """Get user by ID"""
    if db is None:
        raise ValueError("Database session is None")
    return db.query(User).filter(User.id == user_id).first()  # type: ignore

def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    """Authenticate a user with username and password"""
    user = get_user_by_username(db, username)
    if not user or not user.password_hash:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user

def create_user(db: Session, username: Optional[str], password: Optional[str], is_anonymous: bool = False) -> User:
    """Create a new user"""
    user_id = str(uuid.uuid4())
    
    if is_anonymous:
        # Anonymous user
        db_user = User(
            id=user_id,
            username=None,
            password_hash=None,
            is_anonymous=True
        )
    else:
        # Regular user
        if not username or not password:
            raise ValueError("Username and password required for non-anonymous users")
        
        # Check if username already exists
        if get_user_by_username(db, username):
            raise ValueError("Username already registered")
        
        hashed_password = get_password_hash(password)
        db_user = User(
            id=user_id,
            username=username,
            password_hash=hashed_password,
            is_anonymous=False
        )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    """Get current authenticated user"""
    
    token = credentials.credentials
    token_data = verify_token(token)
    
    # Ensure user_id is not None (it should be guaranteed by verify_token)
    if not token_data.user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = get_user_by_id(db, token_data.user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Update last active timestamp
    user.last_active = datetime.utcnow()
    db.commit()
    
    return user