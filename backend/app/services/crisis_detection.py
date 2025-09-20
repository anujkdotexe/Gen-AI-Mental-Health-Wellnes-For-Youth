"""
Crisis Detection and Response System for MindSpark AI

This module provides enhanced crisis detection capabilities including:
- Multi-layered crisis detection (keywords, sentiment, ML models)
- Crisis intervention protocols
- Resource recommendation system
- Emergency escalation procedures
"""

from typing import Dict, List, Tuple, Optional, Any
import re
import json
from datetime import datetime
import logging
from app.models import CrisisResource
from app.database import get_db

# Enhanced crisis detection patterns
SEVERE_CRISIS_KEYWORDS = [
    'suicide', 'kill myself', 'end my life', 'want to die', 'better off dead',
    'hanging myself', 'overdose', 'pills to die', 'jump off', 'gun to my head',
    'razor blade', 'cutting deep', 'bleeding out', 'final goodbye'
]

MODERATE_CRISIS_KEYWORDS = [
    'self harm', 'hurt myself', 'cutting', 'burn myself', 'hate myself',
    'worthless', 'useless', 'burden', 'hopeless', 'no point living',
    'give up', 'can\'t go on', 'end the pain', 'nothing matters'
]

MILD_CRISIS_KEYWORDS = [
    'depressed', 'overwhelmed', 'can\'t handle', 'breaking down',
    'falling apart', 'lost', 'alone', 'scared', 'anxious'
]

# Emotional distress patterns
DISTRESS_PATTERNS = [
    r'\b(i\s+want\s+to\s+die|want\s+to\s+kill\s+myself)\b',
    r'\b(life\s+isn\'t\s+worth\s+living|not\s+worth\s+living)\b',
    r'\b(everyone\s+would\s+be\s+better\s+off\s+without\s+me)\b',
    r'\b(i\s+have\s+a\s+plan\s+to|planning\s+to\s+kill)\b',
    r'\b(goodbye\s+forever|this\s+is\s+goodbye)\b'
]

class CrisisDetectionSystem:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def analyze_crisis_severity(self, text: str, sentiment_score: float) -> Dict[str, Any]:
        """
        Comprehensive crisis analysis using multiple detection methods
        Returns crisis level (0-4) and detailed analysis
        """
        text_lower = text.lower()
        crisis_level = 0
        detected_keywords = []
        detected_patterns = []
        risk_factors = []
        
        # Keyword-based detection
        for keyword in SEVERE_CRISIS_KEYWORDS:
            if keyword in text_lower:
                crisis_level = max(crisis_level, 4)  # Severe crisis
                detected_keywords.append(keyword)
                risk_factors.append(f"Severe crisis language: '{keyword}'")
        
        for keyword in MODERATE_CRISIS_KEYWORDS:
            if keyword in text_lower:
                crisis_level = max(crisis_level, 3)  # Moderate crisis
                detected_keywords.append(keyword)
                risk_factors.append(f"Moderate crisis language: '{keyword}'")
        
        for keyword in MILD_CRISIS_KEYWORDS:
            if keyword in text_lower:
                crisis_level = max(crisis_level, 2)  # Mild crisis
                detected_keywords.append(keyword)
                risk_factors.append(f"Emotional distress indicators: '{keyword}'")
        
        # Pattern-based detection
        for pattern in DISTRESS_PATTERNS:
            matches = re.finditer(pattern, text_lower, re.IGNORECASE)
            for match in matches:
                crisis_level = max(crisis_level, 4)  # Severe crisis
                detected_patterns.append(match.group())
                risk_factors.append(f"Critical pattern detected: '{match.group()}'")
        
        # Sentiment-based adjustment
        if sentiment_score < -0.8:
            crisis_level = max(crisis_level, 3)
            risk_factors.append(f"Extremely negative sentiment: {sentiment_score}")
        elif sentiment_score < -0.5:
            crisis_level = max(crisis_level, 2)
            risk_factors.append(f"Highly negative sentiment: {sentiment_score}")
        
        # Calculate confidence score
        confidence = self._calculate_confidence(
            len(detected_keywords), 
            len(detected_patterns), 
            abs(sentiment_score) if sentiment_score < 0 else 0
        )
        
        return {
            'crisis_level': crisis_level,
            'confidence': confidence,
            'detected_keywords': detected_keywords,
            'detected_patterns': detected_patterns,
            'risk_factors': risk_factors,
            'immediate_action_required': crisis_level >= 4,
            'professional_help_recommended': crisis_level >= 3,
            'additional_support_suggested': crisis_level >= 2
        }
    
    def _calculate_confidence(self, keyword_count: int, pattern_count: int, sentiment_intensity: float) -> float:
        """Calculate confidence in crisis detection"""
        base_confidence = 0.0
        
        # Keyword confidence
        if keyword_count > 0:
            base_confidence += min(keyword_count * 0.3, 0.6)
        
        # Pattern confidence
        if pattern_count > 0:
            base_confidence += min(pattern_count * 0.4, 0.8)
        
        # Sentiment confidence
        if sentiment_intensity > 0.5:
            base_confidence += sentiment_intensity * 0.3
        
        return min(base_confidence, 1.0)
    
    def get_crisis_response(self, crisis_analysis: Dict) -> Dict[str, Any]:
        """Generate appropriate crisis response based on analysis"""
        crisis_level = crisis_analysis['crisis_level']
        
        if crisis_level >= 4:
            return self._get_severe_crisis_response()
        elif crisis_level == 3:
            return self._get_moderate_crisis_response()
        elif crisis_level == 2:
            return self._get_mild_crisis_response()
        else:
            return self._get_supportive_response()
    
    def _get_severe_crisis_response(self) -> Dict[str, Any]:
        """Response for severe crisis (level 4)"""
        return {
            'priority': 'IMMEDIATE',
            'message': """I'm very concerned about what you're sharing with me. Your safety is the most important thing right now. Please know that you matter and that help is available immediately.

🚨 If you're in immediate danger, please call 911 right now.

For immediate support:
• National Suicide Prevention Lifeline: 988 (available 24/7)
• Crisis Text Line: Text HOME to 741741
• Emergency Services: 911

You don't have to go through this alone. These trained professionals are ready to help you right now.""",
            'actions': [
                'Display emergency resources prominently',
                'Log crisis event for follow-up',
                'Offer immediate connection to crisis counselor',
                'Provide local emergency numbers'
            ],
            'resources': self._get_emergency_resources(),
            'follow_up_required': True,
            'escalate_to_human': True
        }
    
    def _get_moderate_crisis_response(self) -> Dict[str, Any]:
        """Response for moderate crisis (level 3)"""
        return {
            'priority': 'HIGH',
            'message': """I hear how much pain you're experiencing right now, and I'm genuinely concerned about you. What you're feeling is incredibly difficult, but you don't have to face this alone.

Professional support can make a real difference:
• National Suicide Prevention Lifeline: 988
• Crisis Text Line: Text HOME to 741741
• SAMHSA National Helpline: 1-800-662-4357

Would you consider reaching out to a trusted adult, counselor, or calling one of these resources? You deserve support, and there are people trained to help you through this.""",
            'actions': [
                'Provide crisis resources',
                'Encourage professional help',
                'Offer coping strategies',
                'Schedule follow-up check-in'
            ],
            'resources': self._get_crisis_support_resources(),
            'follow_up_required': True,
            'escalate_to_human': False
        }
    
    def _get_mild_crisis_response(self) -> Dict[str, Any]:
        """Response for mild crisis (level 2)"""
        return {
            'priority': 'MEDIUM',
            'message': """I can see you're going through a really tough time right now. Your feelings are completely valid, and it's brave of you to share what you're experiencing.

Here are some immediate steps that might help:
• Take slow, deep breaths
• Reach out to someone you trust
• Consider talking to a counselor or therapist
• Remember that difficult emotions are temporary

If things feel overwhelming:
• Crisis Text Line: Text HOME to 741741
• National Suicide Prevention Lifeline: 988

You matter, and there are people who want to help. Would you like to talk about some coping strategies that might help right now?""",
            'actions': [
                'Provide coping strategies',
                'Suggest professional resources',
                'Offer emotional validation',
                'Check in regularly'
            ],
            'resources': self._get_support_resources(),
            'follow_up_required': False,
            'escalate_to_human': False
        }
    
    def _get_supportive_response(self) -> Dict[str, Any]:
        """Response for general support (level 0-1)"""
        return {
            'priority': 'NORMAL',
            'message': """I'm here to listen and support you. It sounds like you might be dealing with some challenges, and that's completely normal. Everyone goes through difficult times.

Some things that might help:
• Talk to someone you trust about how you're feeling
• Practice self-care activities you enjoy
• Consider speaking with a counselor if you'd like additional support

Remember, asking for help is a sign of strength, not weakness. You don't have to handle everything on your own.""",
            'actions': [
                'Provide emotional support',
                'Suggest self-care strategies',
                'Normalize seeking help'
            ],
            'resources': self._get_general_resources(),
            'follow_up_required': False,
            'escalate_to_human': False
        }
    
    def _get_emergency_resources(self) -> List[Dict]:
        """Get emergency crisis resources"""
        return [
            {
                'name': 'Emergency Services',
                'phone': '911',
                'description': 'For immediate danger or medical emergency',
                'availability': '24/7'
            },
            {
                'name': 'National Suicide Prevention Lifeline',
                'phone': '988',
                'description': 'Free, confidential crisis support',
                'availability': '24/7',
                'website': 'suicidepreventionlifeline.org'
            },
            {
                'name': 'Crisis Text Line',
                'contact': 'Text HOME to 741741',
                'description': 'Free, 24/7 crisis support via text',
                'availability': '24/7',
                'website': 'crisistextline.org'
            }
        ]
    
    def _get_crisis_support_resources(self) -> List[Dict]:
        """Get crisis support resources"""
        return [
            {
                'name': 'National Suicide Prevention Lifeline',
                'phone': '988',
                'description': 'Free, confidential crisis support',
                'availability': '24/7'
            },
            {
                'name': 'Crisis Text Line',
                'contact': 'Text HOME to 741741',
                'description': 'Free crisis support via text',
                'availability': '24/7'
            },
            {
                'name': 'SAMHSA National Helpline',
                'phone': '1-800-662-4357',
                'description': 'Treatment referral and information service',
                'availability': '24/7'
            },
            {
                'name': 'Teen Line',
                'phone': '1-800-852-8336',
                'description': 'Teen-to-teen support',
                'availability': 'Daily 6 PM - 10 PM PST'
            }
        ]
    
    def _get_support_resources(self) -> List[Dict]:
        """Get general support resources"""
        return [
            {
                'name': 'Crisis Text Line',
                'contact': 'Text HOME to 741741',
                'description': 'Free crisis support via text',
                'availability': '24/7'
            },
            {
                'name': 'National Alliance on Mental Illness (NAMI)',
                'phone': '1-800-950-6264',
                'description': 'Information and support',
                'availability': 'M-F 10 AM - 10 PM ET'
            },
            {
                'name': 'Psychology Today',
                'website': 'psychologytoday.com',
                'description': 'Find therapists and support groups',
                'availability': 'Online directory'
            }
        ]
    
    def _get_general_resources(self) -> List[Dict]:
        """Get general mental health resources"""
        return [
            {
                'name': 'Mental Health America',
                'website': 'mhanational.org',
                'description': 'Mental health information and resources',
                'availability': 'Online'
            },
            {
                'name': 'National Alliance on Mental Illness (NAMI)',
                'website': 'nami.org',
                'description': 'Education, support, and advocacy',
                'availability': 'Online'
            },
            {
                'name': 'Mindfulness Apps',
                'description': 'Headspace, Calm, Insight Timer for meditation',
                'availability': 'Mobile apps'
            }
        ]
    
    def log_crisis_event(self, user_id: str, crisis_analysis: Dict, response: Dict) -> None:
        """Log crisis event for follow-up and safety monitoring"""
        try:
            crisis_log = {
                'user_id': user_id,
                'timestamp': datetime.utcnow().isoformat(),
                'crisis_level': crisis_analysis['crisis_level'],
                'confidence': crisis_analysis['confidence'],
                'risk_factors': crisis_analysis['risk_factors'],
                'response_priority': response['priority'],
                'escalated': response.get('escalate_to_human', False)
            }
            
            # Log to file or database
            self.logger.critical(f"CRISIS EVENT: {json.dumps(crisis_log)}")
            
            # TODO: Implement database logging and alerting system
            # TODO: Notify crisis response team if escalation required
            
        except Exception as e:
            self.logger.error(f"Failed to log crisis event: {e}")

# Global crisis detection instance
crisis_detector = CrisisDetectionSystem()