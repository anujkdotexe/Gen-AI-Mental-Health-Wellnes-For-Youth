from fastapi import APIRouter, Depends, HTTPException, status
from app.database import get_db
from app.models import User, Conversation as ConversationModel, Message as MessageModel
from app.services.auth import get_current_user
from app.services.ai_service import ai_service
import uuid
import json
import logging
from datetime import datetime
from typing import Optional, List, Dict
from pydantic import BaseModel

router = APIRouter()

# Pydantic models for request/response
class MessageRequest(BaseModel):
    content: str
    context: Optional[Dict] = None

class MessageResponse(BaseModel):
    id: str
    content: str
    is_user: bool
    timestamp: str
    sentiment_score: Optional[float] = None
    emotions: Optional[Dict[str, float]] = None
    intent: Optional[Dict[str, float]] = None
    crisis_detected: Optional[bool] = None

class ConversationResponse(BaseModel):
    id: str
    title: str
    created_at: str
    updated_at: str
    messages: List[MessageResponse]
    summary: Optional[Dict] = None

@router.post("/start")
async def start_conversation(
    current_user: User = Depends(get_current_user),
    db = Depends(get_db)
):
    """Start a new conversation with enhanced AI capabilities"""
    try:
        conversation_id = str(uuid.uuid4())
        db_conversation = ConversationModel(
            id=conversation_id,
            user_id=current_user.id,
            title="New Conversation"
        )
        db.add(db_conversation)
        db.commit()
        
        # Add welcome message from AI
        welcome_message = """Hi! I'm MindSpark, your compassionate AI companion. I'm here to support you in your mental wellness journey. 

I can help with:
🌟 Emotional support and validation
🧠 Coping strategies and mindfulness techniques  
💭 Working through challenges using evidence-based approaches
📱 Crisis support and resource connections

Feel free to share what's on your mind - there's no judgment here, and everything we discuss is private. How are you feeling today?"""
        
        ai_message_id = str(uuid.uuid4())
        ai_message = MessageModel(
            id=ai_message_id,
            conversation_id=conversation_id,
            content=welcome_message,
            is_user=False,
            sentiment_score=0.5,  # Neutral positive
            confidence_score=1.0
        )
        db.add(ai_message)
        db.commit()
        
        return {
            "id": conversation_id,
            "title": "New Conversation",
            "created_at": db_conversation.created_at.isoformat(),
            "messages": [{
                "id": ai_message_id,
                "content": welcome_message,
                "is_user": False,
                "timestamp": ai_message.timestamp.isoformat(),
                "sentiment_score": 0.5
            }]
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to start conversation: {str(e)}"
        )

@router.post("/{conversation_id}/message")
async def send_message(
    conversation_id: str,
    message_data: MessageRequest,
    current_user: User = Depends(get_current_user),
    db = Depends(get_db)
):
    """Send a message in a conversation with enhanced AI analysis"""
    try:
        # Verify conversation exists and belongs to user
        conversation = db.query(ConversationModel).filter(
            ConversationModel.id == conversation_id,
            ConversationModel.user_id == current_user.id
        ).first()
        
        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )
        
        user_content = message_data.content
        if not user_content.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Message content cannot be empty"
            )
        
        # Get conversation history for context
        messages = db.query(MessageModel).filter(
            MessageModel.conversation_id == conversation_id
        ).order_by(MessageModel.timestamp).all()
        
        conversation_history = [
            {
                "content": msg.content,
                "is_user": msg.is_user,
                "timestamp": msg.timestamp.isoformat(),
                "sentiment_score": msg.sentiment_score
            }
            for msg in messages
        ]
        
        # Generate AI response with enhanced analysis
        ai_result = await ai_service.generate_response(user_content, conversation_history)
        
        # Save user message with analysis
        user_message_id = str(uuid.uuid4())
        user_message = MessageModel(
            id=user_message_id,
            conversation_id=conversation_id,
            content=user_content,
            is_user=True,
            sentiment_score=ai_result.get("sentiment_score"),
            crisis_keywords=json.dumps(ai_result.get("crisis_keywords", [])),
            confidence_score=ai_result.get("confidence", 0.8)
        )
        db.add(user_message)
        
        # Save AI response
        ai_message_id = str(uuid.uuid4())
        ai_message = MessageModel(
            id=ai_message_id,
            conversation_id=conversation_id,
            content=ai_result["response"],
            is_user=False,
            sentiment_score=0.5,  # AI responses are generally neutral-positive
            confidence_score=ai_result.get("confidence", 0.8)
        )
        db.add(ai_message)
        
        # Update conversation timestamp
        conversation.updated_at = datetime.utcnow()
        
        # If first real conversation message, update title
        if len(conversation_history) <= 1:  # Only welcome message exists
            # Generate a title from the first user message
            title_words = user_content.split()[:5]
            conversation.title = " ".join(title_words) + ("..." if len(title_words) == 5 else "")
        
        db.commit()
        
        # Prepare response with enhanced data
        response = {
            "user_message": {
                "id": user_message_id,
                "content": user_content,
                "is_user": True,
                "timestamp": user_message.timestamp.isoformat(),
                "sentiment_score": ai_result.get("sentiment_score"),
                "emotions": ai_result.get("emotions", {}),
                "intent": ai_result.get("intent", {}),
                "crisis_detected": ai_result.get("crisis_detected", False)
            },
            "ai_message": {
                "id": ai_message_id,
                "content": ai_result["response"],
                "is_user": False,
                "timestamp": ai_message.timestamp.isoformat(),
                "confidence": ai_result.get("confidence", 0.8)
            },
            "analysis": {
                "sentiment_score": ai_result.get("sentiment_score"),
                "emotions": ai_result.get("emotions", {}),
                "intent": ai_result.get("intent", {}),
                "crisis_detected": ai_result.get("crisis_detected", False),
                "crisis_score": ai_result.get("crisis_score", 0.0)
            }
        }
        
        # If crisis detected, add resource information
        if ai_result.get("crisis_detected", False):
            response["crisis_resources"] = {
                "immediate_help": "If you're in immediate danger, please call 911",
                "crisis_line": "National Suicide Prevention Lifeline: 988",
                "text_line": "Crisis Text Line: Text HOME to 741741",
                "chat_support": "Online chat available at suicidepreventionlifeline.org"
            }
        
        # Add personalized coping strategies for emotional support
        emotions = ai_result.get("emotions", {})
        intent = ai_result.get("intent", {})
        sentiment_score = ai_result.get("sentiment_score", 0)
        
        if not ai_result.get("crisis_detected", False) and (sentiment_score < -0.3 or any(score > 0.5 for score in emotions.values())):
            try:
                coping_strategies = ai_service.provide_personalized_coping_strategies(emotions, intent)
                if coping_strategies:
                    response["coping_strategies"] = {
                        "title": "Personalized Coping Strategies",
                        "strategies": coping_strategies,
                        "note": "These are suggestions based on how you're feeling right now. Try what feels right for you."
                    }
            except Exception as e:
                logging.warning(f"Could not generate coping strategies: {e}")
        
        return response
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to send message: {str(e)}"
        )

@router.get("/list")
async def get_conversations(
    current_user: User = Depends(get_current_user),
    db = Depends(get_db)
):
    """Get user's conversations"""
    conversations = db.query(ConversationModel).filter(
        ConversationModel.user_id == current_user.id
    ).order_by(ConversationModel.updated_at.desc()).all()
    
    result = []
    for conv in conversations:
        # Get last message for preview
        last_message = db.query(MessageModel).filter(
            MessageModel.conversation_id == conv.id
        ).order_by(MessageModel.timestamp.desc()).first()
        
        result.append({
            "id": conv.id,
            "title": conv.title,
            "created_at": conv.created_at.isoformat(),
            "updated_at": conv.updated_at.isoformat(),
            "last_message": {
                "content": last_message.content[:100] + ("..." if len(last_message.content) > 100 else "") if last_message else None,
                "timestamp": last_message.timestamp.isoformat() if last_message else None,
                "is_user": last_message.is_user if last_message else None
            } if last_message else None
        })
    
    return {"conversations": result}

@router.get("/{conversation_id}")
async def get_conversation(
    conversation_id: str,
    current_user: User = Depends(get_current_user),
    db = Depends(get_db)
):
    """Get a specific conversation with messages"""
    conversation = db.query(ConversationModel).filter(
        ConversationModel.id == conversation_id,
        ConversationModel.user_id == current_user.id
    ).first()
    
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    
    messages = db.query(MessageModel).filter(
        MessageModel.conversation_id == conversation_id
    ).order_by(MessageModel.timestamp).all()
    
    return {
        "id": conversation.id,
        "title": conversation.title,
        "created_at": conversation.created_at.isoformat(),
        "updated_at": conversation.updated_at.isoformat(),
        "messages": [
            {
                "id": msg.id,
                "content": msg.content,
                "is_user": msg.is_user,
                "timestamp": msg.timestamp.isoformat(),
                "sentiment_score": msg.sentiment_score
            }
            for msg in messages
        ]
    }

@router.get("/routing-stats")
async def get_routing_statistics(current_user: User = Depends(get_current_user)):
    """Get AI routing statistics for monitoring"""
    try:
        stats = ai_service.get_routing_statistics()
        return {
            "status": "success",
            "data": stats,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logging.error(f"Error getting routing stats: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve routing statistics"
        )

@router.post("/routing-stats/reset")
async def reset_routing_statistics(current_user: User = Depends(get_current_user)):
    """Reset AI routing statistics"""
    try:
        ai_service.reset_routing_statistics()
        return {
            "status": "success",
            "message": "Routing statistics reset successfully",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logging.error(f"Error resetting routing stats: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to reset routing statistics"
        )