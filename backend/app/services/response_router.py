"""
Intelligent Response Router for Mental Health AI
Routes between Hugging Face, Gemini Basic, and Gemini Pro based on severity analysis
"""

import logging
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime
from enum import Enum

from .gemini_service import gemini_service, SeverityLevel, ResponseSource
from .crisis_detection import crisis_detector

logger = logging.getLogger(__name__)

class ResponseRouter:
    """Intelligent router for AI responses based on user needs"""
    
    def __init__(self):
        self.gemini_service = gemini_service
        self.crisis_detector = crisis_detector
        
        # Statistics tracking
        self.routing_stats = {
            'total_requests': 0,
            'hugging_face_responses': 0,
            'gemini_basic_responses': 0,
            'gemini_pro_responses': 0,
            'severity_distribution': {
                'low': 0,
                'moderate': 0,
                'high': 0,
                'critical': 0
            }
        }
    
    def analyze_message_context(self, user_message: str, conversation_history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze message context for routing decisions
        
        Args:
            user_message: User's current message
            conversation_history: Previous conversation messages
            
        Returns:
            Context dictionary with analysis results
        """
        context = {}
        
        try:
            # Crisis detection
            crisis_result = self.crisis_detector.analyze_crisis_severity(user_message, self._calculate_sentiment(user_message))
            context.update({
                'crisis_detected': crisis_result.get('is_crisis', False),
                'crisis_level': crisis_result.get('severity_score', 0.0),
                'crisis_indicators': crisis_result.get('keywords_found', [])
            })
            
            # Basic sentiment analysis (you can enhance this)
            sentiment_score = self._calculate_sentiment(user_message)
            context['sentiment_score'] = sentiment_score
            
            # Message length and urgency indicators
            context['message_length'] = len(user_message.split())
            context['has_urgency_words'] = self._has_urgency_indicators(user_message)
            
            # Conversation frequency (how often user is messaging)
            if conversation_history:
                recent_messages = [msg for msg in conversation_history[-5:] if msg.get('role') == 'user']
                context['recent_user_messages'] = len(recent_messages)
            else:
                context['recent_user_messages'] = 0
            
        except Exception as e:
            logger.error(f"Error analyzing message context: {e}")
            # Provide safe defaults
            context = {
                'crisis_detected': False,
                'crisis_level': 0.0,
                'crisis_indicators': [],
                'sentiment_score': 0.0,
                'message_length': len(user_message.split()),
                'has_urgency_words': False,
                'recent_user_messages': 0
            }
        
        return context
    
    def _calculate_sentiment(self, message: str) -> float:
        """Calculate basic sentiment score for the message"""
        try:
            # Import here to avoid circular imports
            from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
            analyzer = SentimentIntensityAnalyzer()
            scores = analyzer.polarity_scores(message)
            return scores['compound']  # Range: -1 (negative) to +1 (positive)
        except Exception as e:
            logger.warning(f"Error calculating sentiment: {e}")
            return 0.0
    
    def _has_urgency_indicators(self, message: str) -> bool:
        """Check if message contains urgency indicators"""
        urgency_words = [
            'urgent', 'emergency', 'immediately', 'right now', 'asap',
            'help me', 'please help', 'need help now', 'can\'t wait'
        ]
        message_lower = message.lower()
        return any(word in message_lower for word in urgency_words)
    
    def determine_routing_decision(
        self, 
        user_message: str, 
        conversation_history: List[Dict[str, Any]]
    ) -> Tuple[ResponseSource, SeverityLevel, Dict[str, Any]]:
        """
        Determine which AI service should handle the response
        
        Args:
            user_message: User's message
            conversation_history: Previous conversation
            
        Returns:
            Tuple of (response_source, severity_level, context)
        """
        # Analyze message context
        context = self.analyze_message_context(user_message, conversation_history)
        
        # Determine severity level
        severity = self.gemini_service.determine_severity(user_message, context)
        
        # Update statistics
        self.routing_stats['total_requests'] += 1
        self.routing_stats['severity_distribution'][severity.value] += 1
        
        # Determine if Gemini should be used
        use_gemini, model_type = self.gemini_service.should_use_gemini(severity)
        
        if use_gemini:
            if model_type == "pro":
                response_source = ResponseSource.GEMINI_PRO
                self.routing_stats['gemini_pro_responses'] += 1
            else:
                response_source = ResponseSource.GEMINI_BASIC
                self.routing_stats['gemini_basic_responses'] += 1
        else:
            response_source = ResponseSource.HUGGING_FACE
            self.routing_stats['hugging_face_responses'] += 1
        
        logger.info(f"Routing decision: {response_source.value} for severity {severity.value}")
        
        return response_source, severity, context
    
    async def get_routed_response(
        self,
        user_message: str,
        conversation_history: List[Dict[str, Any]],
        hugging_face_fallback_func=None
    ) -> Dict[str, Any]:
        """
        Get AI response using intelligent routing
        
        Args:
            user_message: User's message
            conversation_history: Previous conversation
            hugging_face_fallback_func: Function to call for Hugging Face responses
            
        Returns:
            Response dictionary with routing information
        """
        try:
            # Determine routing
            response_source, severity, context = self.determine_routing_decision(
                user_message, conversation_history
            )
            
            response_data = {
                'routing_decision': {
                    'source': response_source.value,
                    'severity': severity.value,
                    'context': context,
                    'timestamp': datetime.utcnow().isoformat()
                }
            }
            
            # Get response based on routing decision
            if response_source == ResponseSource.HUGGING_FACE:
                # Use Hugging Face models (existing implementation)
                if hugging_face_fallback_func:
                    hf_response = await hugging_face_fallback_func(user_message, conversation_history)
                    response_data.update(hf_response)
                    response_data['source'] = ResponseSource.HUGGING_FACE.value
                else:
                    response_data.update({
                        'content': "I'm here to listen and support you. Could you tell me more about what's on your mind?",
                        'source': ResponseSource.HUGGING_FACE.value,
                        'fallback': True
                    })
            
            elif response_source in [ResponseSource.GEMINI_BASIC, ResponseSource.GEMINI_PRO]:
                # Use Gemini models
                use_pro = response_source == ResponseSource.GEMINI_PRO
                gemini_response = await self.gemini_service.get_gemini_response(
                    user_message, conversation_history, severity, use_pro
                )
                
                if gemini_response.get('success'):
                    response_data.update(gemini_response)
                else:
                    # Fallback to Hugging Face if Gemini fails
                    logger.warning(f"Gemini failed, falling back to Hugging Face: {gemini_response.get('error')}")
                    if hugging_face_fallback_func:
                        hf_response = await hugging_face_fallback_func(user_message, conversation_history)
                        response_data.update(hf_response)
                        response_data['source'] = ResponseSource.HUGGING_FACE.value
                        response_data['fallback_reason'] = gemini_response.get('error')
                    else:
                        response_data.update({
                            'content': "I'm experiencing some technical difficulties, but I'm still here to support you. How are you feeling right now?",
                            'source': ResponseSource.HUGGING_FACE.value,
                            'fallback': True,
                            'fallback_reason': gemini_response.get('error')
                        })
            
            # Add routing statistics
            response_data['routing_stats'] = self.get_routing_statistics()
            
            return response_data
            
        except Exception as e:
            logger.error(f"Error in routed response: {e}")
            
            # Emergency fallback
            return {
                'content': "I'm here to support you, though I'm experiencing some technical issues. Please tell me what's on your mind.",
                'source': ResponseSource.HUGGING_FACE.value,
                'fallback': True,
                'error': str(e),
                'routing_decision': {
                    'source': 'error_fallback',
                    'severity': 'unknown',
                    'timestamp': datetime.utcnow().isoformat()
                }
            }
    
    def get_routing_statistics(self) -> Dict[str, Any]:
        """Get current routing statistics"""
        if self.routing_stats['total_requests'] == 0:
            return self.routing_stats
        
        total = self.routing_stats['total_requests']
        
        return {
            **self.routing_stats,
            'percentages': {
                'hugging_face': round((self.routing_stats['hugging_face_responses'] / total) * 100, 1),
                'gemini_basic': round((self.routing_stats['gemini_basic_responses'] / total) * 100, 1),
                'gemini_pro': round((self.routing_stats['gemini_pro_responses'] / total) * 100, 1)
            }
        }
    
    def reset_statistics(self):
        """Reset routing statistics"""
        self.routing_stats = {
            'total_requests': 0,
            'hugging_face_responses': 0,
            'gemini_basic_responses': 0,
            'gemini_pro_responses': 0,
            'severity_distribution': {
                'low': 0,
                'moderate': 0,
                'high': 0,
                'critical': 0
            }
        }

# Global instance
response_router = ResponseRouter()