import os
from sqlalchemy.engine.create import create_engine
from sqlalchemy.orm.session import sessionmaker
from dotenv import load_dotenv

load_dotenv()

# Database configuration
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "sqlite:///./mindspark.db"  # Default to SQLite for development
)

# For production PostgreSQL, use:
# DATABASE_URL = "postgresql://username:password@localhost/mindspark_db"

# Create engine
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Import all models to register them with SQLAlchemy
from app.models import Base, User, MoodEntry, JournalEntry, Conversation, Message, CrisisResource

# Create all tables
def create_tables():
    """Create all database tables"""
    Base.metadata.create_all(bind=engine)  # type: ignore

# Dependency to get DB session
def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize database with default data
def init_db():
    """Initialize database with default crisis resources and AI models"""
    from app.models import CrisisResource, AIModel
    
    create_tables()
    
    db = SessionLocal()
    try:
        # Check if crisis resources already exist
        existing_resources = db.query(CrisisResource).first()
        if not existing_resources:
            # Add default crisis resources
            crisis_resources = [
                CrisisResource(
                    name="National Suicide Prevention Lifeline",
                    description="24/7 crisis support and suicide prevention",
                    phone_number="988",
                    website="https://suicidepreventionlifeline.org/",
                    availability="24/7",
                    category="emergency",
                    priority=1
                ),
                CrisisResource(
                    name="Crisis Text Line",
                    description="Free, 24/7 crisis support via text",
                    phone_number="Text HOME to 741741",
                    website="https://www.crisistextline.org/",
                    availability="24/7",
                    category="text",
                    priority=2
                ),
                CrisisResource(
                    name="National Alliance on Mental Illness (NAMI)",
                    description="Mental health support and resources",
                    phone_number="1-800-950-6264",
                    website="https://www.nami.org/",
                    availability="Mon-Fri 10am-10pm ET",
                    category="support",
                    priority=3
                ),
                CrisisResource(
                    name="SAMHSA National Helpline",
                    description="Treatment referral and information service",
                    phone_number="1-800-662-4357",
                    website="https://www.samhsa.gov/find-help/national-helpline",
                    availability="24/7",
                    category="referral",
                    priority=4
                ),
                CrisisResource(
                    name="The Trevor Project",
                    description="Crisis support for LGBTQ+ youth",
                    phone_number="1-866-488-7386",
                    website="https://www.thetrevorproject.org/",
                    availability="24/7",
                    category="specialized",
                    priority=2
                ),
            ]
            
            for resource in crisis_resources:
                db.add(resource)
        
        # Add default AI model configurations
        existing_models = db.query(AIModel).first()
        if not existing_models:
            import json
            ai_models = [
                AIModel(
                    name="OpenAI GPT-3.5 Turbo",
                    model_type="conversation",
                    model_path="gpt-3.5-turbo",
                    version="1.0",
                    is_active=True,
                    performance_metrics=json.dumps({"accuracy": 0.85, "safety": 0.95})
                ),
                AIModel(
                    name="VADER Sentiment Analyzer",
                    model_type="sentiment",
                    model_path="vaderSentiment",
                    version="3.3.2",
                    is_active=True,
                    performance_metrics=json.dumps({"accuracy": 0.78})
                ),
            ]
            
            for model in ai_models:
                db.add(model)
        
        db.commit()
        print("Database initialized successfully!")
        
    except Exception as e:
        print(f"Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_db()