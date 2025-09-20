"""
Google Gemini AI Service for Mental Health Support
Provides intelligent routing between local Hugging Face models and Gemini models
"""

import os
import google.generativeai as genai
from typing import Dict, List, Optional, Tuple, Any
import logging
import json
from datetime import datetime
from enum import Enum

logger = logging.getLogger(__name__)

class SeverityLevel(Enum):
    """User message severity levels for routing decisions"""
    LOW = "low"           # Normal conversation - use Hugging Face
    MODERATE = "moderate" # Some concern - use Gemini Basic (5-10%)
    HIGH = "high"         # Crisis situation - use Gemini Pro
    CRITICAL = "critical" # Immediate professional help needed - use Gemini Pro

class ResponseSource(Enum):
    """Source of the AI response"""
    HUGGING_FACE = "hugging_face"
    GEMINI_BASIC = "gemini_basic"
    GEMINI_PRO = "gemini_pro"

class GeminiService:
    """Google Gemini AI Service for mental health support"""
    
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.basic_model_name = os.getenv("GEMINI_BASIC_MODEL", "gemini-1.5-flash")
        self.pro_model_name = os.getenv("GEMINI_PRO_MODEL", "gemini-1.5-pro")
        
        if not self.api_key or self.api_key == "your-gemini-api-key-here":
            logger.warning("Gemini API key not configured. Gemini features will be disabled.")
            self.enabled = False
            return
        
        try:
            # Configure Gemini
            genai.configure(api_key=self.api_key)
            
            # Initialize models
            self.basic_model = genai.GenerativeModel(self.basic_model_name)
            self.pro_model = genai.GenerativeModel(self.pro_model_name)
            
            self.enabled = True
            logger.info(f"Gemini service initialized with models: {self.basic_model_name}, {self.pro_model_name}")
            
        except Exception as e:
            logger.error(f"Failed to initialize Gemini service: {e}")
            self.enabled = False
    
    def is_enabled(self) -> bool:
        """Check if Gemini service is properly configured"""
        return self.enabled
    
    def determine_severity(self, message: str, context: Dict[str, Any]) -> SeverityLevel:
        """
        Determine the severity level of the user's message
        
        Args:
            message: User's message
            context: Additional context (sentiment, crisis detection, etc.)
            
        Returns:
            SeverityLevel indicating routing decision
        """
        # Get crisis detection results
        crisis_detected = context.get('crisis_detected', False)
        crisis_level = context.get('crisis_level', 0.0)
        sentiment_score = context.get('sentiment_score', 0.0)
        
        # Critical indicators - immediate professional help needed
        critical_keywords = [
            'suicide', 'kill myself', 'end my life', 'not worth living',
            'hurt myself', 'self harm', 'cutting', 'overdose',
            'want to die', 'better off dead', 'suicide plan'
        ]
        
        # High severity indicators - serious mental health concerns
        high_severity_keywords = [
            'depressed', 'hopeless', 'worthless', 'empty inside',
            'panic attack', 'anxiety attack', 'breakdown',
            'can\'t cope', 'overwhelming', 'disaster', 'terrible',
            'scared', 'terrified', 'losing control'
        ]
        
        # Moderate severity indicators - some concern
        moderate_keywords = [
            'stressed', 'worried', 'anxious', 'sad', 'upset',
            'frustrated', 'angry', 'confused', 'tired',
            'lonely', 'overwhelmed', 'difficult'
        ]
        
        message_lower = message.lower()
        
        # Check for critical situations
        if crisis_detected and crisis_level > 0.8:
            return SeverityLevel.CRITICAL
        
        if any(keyword in message_lower for keyword in critical_keywords):
            return SeverityLevel.CRITICAL
        
        # Check for high severity
        if crisis_detected and crisis_level > 0.6:
            return SeverityLevel.HIGH
        
        if sentiment_score < -0.7 and any(keyword in message_lower for keyword in high_severity_keywords):
            return SeverityLevel.HIGH
        
        # Check for moderate severity
        if sentiment_score < -0.4 or any(keyword in message_lower for keyword in moderate_keywords):
            return SeverityLevel.MODERATE
        
        # Default to low severity
        return SeverityLevel.LOW
    
    def should_use_gemini(self, severity: SeverityLevel) -> Tuple[bool, str]:
        """
        Determine if Gemini should be used based on severity
        
        Args:
            severity: Determined severity level
            
        Returns:
            Tuple of (should_use_gemini, model_type)
        """
        if not self.enabled:
            return False, "disabled"
        
        if severity in [SeverityLevel.CRITICAL, SeverityLevel.HIGH]:
            return True, "pro"
        elif severity == SeverityLevel.MODERATE:
            # 5-10% chance for moderate cases
            import random
            if random.random() < 0.075:  # 7.5% chance
                return True, "basic"
        
        return False, "none"
    
    def create_chat_summary(self, conversation_history: List[Dict[str, Any]]) -> str:
        """
        Create a summary of the conversation history for Gemini context
        
        Args:
            conversation_history: List of previous messages
            
        Returns:
            Formatted summary string
        """
        if not conversation_history:
            return "This is the beginning of the conversation."
        
        # Take last 10 messages for context
        recent_messages = conversation_history[-10:] if len(conversation_history) > 10 else conversation_history
        
        summary_parts = []
        summary_parts.append("=== CONVERSATION SUMMARY ===")
        summary_parts.append(f"Total messages in conversation: {len(conversation_history)}")
        summary_parts.append(f"Recent conversation context (last {len(recent_messages)} messages):")
        
        for i, msg in enumerate(recent_messages, 1):
            role = "User" if msg.get('role') == 'user' else "Assistant"
            content = msg.get('content', '')[:200] + "..." if len(msg.get('content', '')) > 200 else msg.get('content', '')
            timestamp = msg.get('timestamp', 'Unknown time')
            summary_parts.append(f"{i}. [{timestamp}] {role}: {content}")
        
        summary_parts.append("=== END SUMMARY ===\\n")
        return "\\n".join(summary_parts)
    
    def create_mental_health_prompt(self, user_message: str, chat_summary: str, severity: SeverityLevel) -> str:
        """
        Create a specialized prompt for mental health support
        
        Args:
            user_message: User's current message
            chat_summary: Summary of conversation history
            severity: Determined severity level
            
        Returns:
            Formatted prompt for Gemini
        """
        base_context = """You are a compassionate AI mental health assistant specialized in providing supportive, empathetic responses to people seeking emotional support. You understand trauma-informed care principles and always prioritize user safety.

IMPORTANT GUIDELINES:
- Always respond with empathy and understanding
- Never dismiss or minimize feelings
- Provide practical coping strategies when appropriate
- Recognize when professional help is needed
- Maintain appropriate boundaries
- Use person-first language
- Be culturally sensitive"""

        if severity == SeverityLevel.CRITICAL:
            crisis_context = """
CRITICAL SITUATION DETECTED:
The user appears to be in crisis and may be experiencing thoughts of self-harm or suicide. This requires immediate, careful attention.

RESPONSE PRIORITIES:
1. Validate their feelings without judgment
2. Express genuine concern for their safety
3. Provide immediate crisis resources
4. Encourage professional help
5. Stay with them emotionally while encouraging action

CRISIS RESOURCES TO INCLUDE:
- National Suicide Prevention Lifeline: 988 (US)
- Crisis Text Line: Text HOME to 741741
- International Association for Suicide Prevention: https://www.iasp.info/resources/Crisis_Centres/
- Emergency services: 911 (if immediate danger)"""
            
            prompt = f"""{base_context}

{crisis_context}

{chat_summary}

Current message from user: "{user_message}"

Please provide an immediate, caring response that prioritizes their safety while maintaining hope and connection. Include appropriate crisis resources."""

        elif severity == SeverityLevel.HIGH:
            high_context = """
HIGH CONCERN DETECTED:
The user is experiencing significant distress and may benefit from professional support.

RESPONSE PRIORITIES:
1. Acknowledge their struggle with compassion
2. Provide emotional validation
3. Suggest coping strategies
4. Gently recommend professional support
5. Offer hope and encouragement"""
            
            prompt = f"""{base_context}

{high_context}

{chat_summary}

Current message from user: "{user_message}"

Please provide a supportive response that validates their experience and offers both immediate comfort and practical guidance."""

        else:  # MODERATE
            moderate_context = """
MODERATE CONCERN:
The user is experiencing some emotional difficulty and would benefit from supportive guidance.

RESPONSE PRIORITIES:
1. Provide empathetic listening
2. Offer perspective and validation
3. Suggest helpful coping strategies
4. Encourage self-care
5. Maintain hopeful outlook"""
            
            prompt = f"""{base_context}

{moderate_context}

{chat_summary}

Current message from user: "{user_message}"

Please provide a warm, supportive response that helps them process their feelings and offers practical guidance."""

        return prompt
    
    async def get_gemini_response(
        self, 
        user_message: str, 
        conversation_history: List[Dict[str, Any]], 
        severity: SeverityLevel,
        use_pro_model: bool = False
    ) -> Dict[str, Any]:
        """
        Get response from Gemini model
        
        Args:
            user_message: User's message
            conversation_history: Previous conversation
            severity: Severity level
            use_pro_model: Whether to use Pro model
            
        Returns:
            Response dictionary
        """
        if not self.enabled:
            raise Exception("Gemini service is not enabled")
        
        try:
            # Create chat summary
            chat_summary = self.create_chat_summary(conversation_history)
            
            # Create specialized prompt
            prompt = self.create_mental_health_prompt(user_message, chat_summary, severity)
            
            # Choose model
            model = self.pro_model if use_pro_model else self.basic_model
            model_name = self.pro_model_name if use_pro_model else self.basic_model_name
            
            # Generate response
            response = model.generate_content(prompt)
            
            # Extract response text
            response_text = response.text if hasattr(response, 'text') else str(response)
            
            return {
                'content': response_text,
                'source': ResponseSource.GEMINI_PRO.value if use_pro_model else ResponseSource.GEMINI_BASIC.value,
                'model': model_name,
                'severity': severity.value,
                'timestamp': datetime.utcnow().isoformat(),
                'success': True
            }
            
        except Exception as e:
            logger.error(f"Error getting Gemini response: {e}")
            return {
                'content': None,
                'source': None,
                'model': None,
                'severity': severity.value,
                'error': str(e),
                'success': False
            }

# Global instance
gemini_service = GeminiService()