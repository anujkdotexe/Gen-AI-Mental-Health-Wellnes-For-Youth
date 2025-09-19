from fastapi import APIRouter, Depends, HTTPException, status
from app.database import get_db
from app.models import User, Conversation as ConversationModel, Message as MessageModel
from app.services.auth import get_current_user
from app.services.ai_service import ai_service
import uuid
import json
from datetime import datetime

router = APIRouter()

@router.post("/start")
async def start_conversation(
    current_user: User = Depends(get_current_user),
    db = Depends(get_db)
):
    """Start a new conversation"""
    try:
        conversation_id = str(uuid.uuid4())
        db_conversation = ConversationModel(
            id=conversation_id,
            user_id=current_user.id,
            title="New Conversation"
        )
        db.add(db_conversation)
        db.commit()
        
        return {
            "id": conversation_id,
            "title": "New Conversation",
            "created_at": db_conversation.created_at.isoformat(),
            "messages": []
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to start conversation"
        )

@router.post("/{conversation_id}/message")
async def send_message(
    conversation_id: str,
    message_data: dict,
    current_user: User = Depends(get_current_user),
    db = Depends(get_db)
):
    """Send a message in a conversation"""
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
        
        user_content = message_data.get("content", "")
        if not user_content.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Message content cannot be empty"
            )
        
        # Get conversation history
        messages = db.query(MessageModel).filter(
            MessageModel.conversation_id == conversation_id
        ).order_by(MessageModel.timestamp).all()
        
        conversation_history = [
            {
                "content": msg.content,
                "is_user": msg.is_user,
                "timestamp": msg.timestamp.isoformat()
            }
            for msg in messages
        ]
        
        # Generate AI response
        ai_result = await ai_service.generate_response(user_content, conversation_history)
        
        # Save user message
        user_message_id = str(uuid.uuid4())
        user_message = MessageModel(
            id=user_message_id,
            conversation_id=conversation_id,
            content=user_content,
            is_user=True,
            sentiment_score=ai_result.get("sentiment_score")
        )
        db.add(user_message)
        
        # Save AI response
        ai_message_id = str(uuid.uuid4())
        ai_message = MessageModel(
            id=ai_message_id,
            conversation_id=conversation_id,
            content=ai_result["response"],
            is_user=False,
            sentiment_score=None,
            confidence_score=ai_result.get("confidence"),
            crisis_keywords=json.dumps(ai_result.get("crisis_keywords", []))
        )
        db.add(ai_message)
        
        # Update conversation title based on first message
        if len(conversation_history) == 0:
            # First message - update conversation title
            conversation.title = user_content[:50] + ("..." if len(user_content) > 50 else "")
        
        db.commit()
        
        return {
            "user_message": {
                "id": user_message_id,
                "content": user_content,
                "is_user": True,
                "timestamp": user_message.timestamp.isoformat(),
                "sentiment_score": ai_result.get("sentiment_score")
            },
            "ai_response": {
                "id": ai_message_id,
                "content": ai_result["response"],
                "is_user": False,
                "timestamp": ai_message.timestamp.isoformat(),
                "confidence_score": ai_result.get("confidence")
            },
            "crisis_detected": ai_result.get("crisis_detected", False),
            "sentiment_score": ai_result.get("sentiment_score")
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send message"
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