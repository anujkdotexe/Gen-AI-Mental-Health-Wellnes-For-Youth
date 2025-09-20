from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm.session import Session
from .database import get_db, init_db
from .routers import auth, mood, journal, conversation, crisis
from .routers import security as security_router
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(
    title="MindSpark AI API",
    description="A comprehensive mental health and wellness API with AI-powered features",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    init_db()

# Health check endpoint
@app.get("/")
async def root():
    return {"message": "MindSpark AI API is running!", "status": "healthy"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "message": "MindSpark AI API is operational",
        "features": [
            "Authentication & User Management",
            "Mood Tracking",
            "Journal Entries",
            "AI-Powered Conversations", 
            "Crisis Support Resources",
            "Advanced Security Features"
        ]
    }

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(mood.router, prefix="/api/mood", tags=["Mood Tracking"])
app.include_router(journal.router, prefix="/api/journal", tags=["Journal"])
app.include_router(conversation.router, prefix="/api/conversation", tags=["AI Chat"])
app.include_router(crisis.router, prefix="/api/crisis", tags=["Crisis Support"])
app.include_router(security_router.router, prefix="/api/security", tags=["Security"])

# Security headers middleware
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)