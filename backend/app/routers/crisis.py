from fastapi import APIRouter, Depends
from app.database import get_db
from app.models import CrisisResource

router = APIRouter()

@router.get("/resources")
async def get_crisis_resources(db = Depends(get_db)):
    """Get crisis support resources"""
    resources = db.query(CrisisResource).filter(
        CrisisResource.is_active == True
    ).order_by(CrisisResource.priority.desc()).all()
    
    return [
        {
            "id": resource.id,
            "name": resource.name,
            "description": resource.description,
            "phone_number": resource.phone_number,
            "website": resource.website,
            "availability": resource.availability,
            "category": resource.category
        }
        for resource in resources
    ]

@router.get("/emergency")
async def get_emergency_info():
    """Get immediate emergency information"""
    return {
        "emergency": {
            "message": "If you're in immediate danger, please call emergency services",
            "us_emergency": "911",
            "crisis_line": "988",
            "crisis_text": "Text HOME to 741741"
        },
        "immediate_steps": [
            "Reach out to a trusted friend or family member",
            "Call a crisis hotline",
            "Go to your nearest emergency room",
            "Call emergency services if in immediate danger"
        ]
    }