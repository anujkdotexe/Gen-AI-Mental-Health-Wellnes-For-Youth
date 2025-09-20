from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import torch
import os
from typing import Dict, List, Optional, Tuple, Union, Any
import json
import re
import logging
import random
from .crisis_detection import crisis_detector
from .response_router import response_router
from .intelligent_conversation_engine import intelligent_conversation_engine

# Initialize sentiment analyzer
sentiment_analyzer = SentimentIntensityAnalyzer()

# Crisis keywords for detection
CRISIS_KEYWORDS = [
    'suicide', 'kill myself', 'end it all', 'want to die', 'not worth living',
    'hurt myself', 'self harm', 'cutting', 'overdose', 'pills',
    'jump off', 'hang myself', 'gun', 'knife', 'blade',
    'hopeless', 'worthless', 'burden', 'better off dead',
    'can\'t go on', 'give up', 'no point', 'end the pain',
    'no one cares', 'alone forever', 'nothing matters', 'wish I was dead'
]

# Enhanced emotion detection keywords
EMOTION_KEYWORDS = {
    'happy': ['happy', 'joy', 'excited', 'great', 'amazing', 'wonderful', 'fantastic', 'good mood'],
    'sad': ['sad', 'down', 'depressed', 'blue', 'miserable', 'crying', 'tears', 'heartbroken'],
    'anxious': ['anxious', 'worried', 'nervous', 'stressed', 'panic', 'overwhelming', 'scared', 'afraid'],
    'angry': ['angry', 'mad', 'furious', 'rage', 'pissed', 'irritated', 'frustrated', 'annoyed'],
    'confused': ['confused', 'lost', 'don\'t understand', 'mixed up', 'unclear', 'puzzled'],
    'grateful': ['grateful', 'thankful', 'blessed', 'appreciate', 'lucky', 'fortunate'],
    'lonely': ['lonely', 'alone', 'isolated', 'disconnected', 'no friends', 'nobody understands'],
    'overwhelmed': ['overwhelmed', 'too much', 'can\'t handle', 'drowning', 'exhausted', 'burnt out']
}

class AIService:
    def __init__(self):
        # Initialize Hugging Face models
        self.device = 0 if torch.cuda.is_available() else -1
        
        # Type annotations for pipeline attributes
        self.sentiment_pipeline: Optional[Any] = None
        self.emotion_pipeline: Optional[Any] = None
        self.text_generator: Optional[Any] = None
        self.intent_pipeline: Optional[Any] = None
        
        try:
            # Sentiment analysis pipeline
            self.sentiment_pipeline = pipeline(
                task="sentiment-analysis",  # type: ignore
                model="cardiffnlp/twitter-roberta-base-sentiment-latest",
                device=self.device
            )
            
            # Emotion detection pipeline
            self.emotion_pipeline = pipeline(
                task="text-classification",  # type: ignore
                model="j-hartmann/emotion-english-distilroberta-base",
                device=self.device
            )
            
            # Text generation pipeline for responses
            self.text_generator = pipeline(
                task="text-generation",  # type: ignore
                model="microsoft/DialoGPT-medium",
                device=self.device,
                max_length=100,
                do_sample=True,
                temperature=0.7
            )
            
            # Intent classification (using a general classification model)
            self.intent_pipeline = pipeline(
                task="zero-shot-classification",  # type: ignore
                model="facebook/bart-large-mnli",
                device=self.device
            )
            
            logging.info("AI Service initialized with Hugging Face models")
            
        except Exception as e:
            logging.error(f"Error initializing AI models: {e}")
            # Fallback to basic functionality if models fail to load
            self.sentiment_pipeline = None
            self.emotion_pipeline = None
            self.text_generator = None
            self.intent_pipeline = None
        
        # Mental health conversation prompts and templates
        self.system_prompt = """
You are MindSpark, a compassionate AI companion designed to support youth mental wellness. 
Your role is to:

1. Provide empathetic, non-judgmental support
2. Use evidence-based techniques from CBT, DBT, and mindfulness
3. Encourage healthy coping strategies
4. Validate emotions while promoting resilience
5. Suggest professional help when appropriate
6. NEVER provide medical advice or replace professional treatment

Guidelines:
- Keep responses conversational and age-appropriate (15-25 years old)
- Use a warm, understanding tone
- Ask follow-up questions to encourage reflection
- Provide practical coping strategies
- If you detect crisis language, gently suggest professional resources
- Focus on strengths and hope
- Respect privacy and anonymity

Remember: You are a supportive companion, not a therapist. Always encourage professional help for serious issues.
"""

        # Response templates for different emotional states
        self.response_templates = {
            'crisis': [
                "I'm really concerned about what you're going through right now. Your feelings are valid, but I want you to know that there are people who can help. Have you considered reaching out to a counselor or trusted adult?",
                "It sounds like you're in a lot of pain right now. You don't have to go through this alone. There are crisis resources available 24/7. Would you like me to share some contact information?",
                "I hear how much you're struggling, and I want you to know that what you're feeling is temporary, even though it might not feel that way. Professional support can make a real difference. Can we talk about getting you connected with help?"
            ],
            'sad': [
                "I can hear the sadness in what you're sharing. It's okay to feel this way - these emotions are part of being human. What's been weighing on your heart lately?",
                "Thank you for trusting me with how you're feeling. Sadness can feel overwhelming sometimes. Have you been able to talk to anyone else about this?",
                "I'm here with you in this difficult moment. Sometimes when we're sad, it helps to remember that emotions come and go like waves. What usually helps you feel a little better when you're down?"
            ],
            'anxious': [
                "I can sense the anxiety in your message. Feeling worried or nervous is really common, especially for young people dealing with a lot. What's been on your mind that's causing these anxious feelings?",
                "Anxiety can feel really overwhelming. Let's try to slow down for a moment. Can you tell me what you're experiencing right now - both in your thoughts and in your body?",
                "It sounds like anxiety is making things feel really intense right now. One thing that can help is focusing on your breathing. Would you like to try a quick breathing exercise together?"
            ],
            'angry': [
                "I can feel the frustration and anger in what you're sharing. These are completely valid emotions. What happened that triggered these feelings?",
                "Anger often shows up when we feel hurt, misunderstood, or like something unfair has happened. Can you help me understand what's behind these feelings?",
                "It's okay to feel angry - it's a normal human emotion. The important thing is how we handle it. What usually helps you when you're feeling this way?"
            ],
            'positive': [
                "I love hearing the positivity in your message! It's wonderful when things are going well. What's been contributing to these good feelings?",
                "That's fantastic! It's so important to celebrate the good moments. How are you planning to keep this positive momentum going?",
                "I'm really happy to hear you're feeling good! Positive emotions are just as important to acknowledge as difficult ones. What's been the highlight recently?"
            ],
            'neutral': [
                "Thanks for sharing with me. I'm here to listen and support you in whatever way I can. What's on your mind today?",
                "I appreciate you taking the time to connect. Sometimes it helps just to have someone to talk to. How has your day been going?",
                "I'm glad you're here. Whether you're having a good day or a tough one, I'm here to listen. What would you like to talk about?"
            ]
        }

        # Evidence-based therapeutic response templates
        self.therapeutic_templates = {
            'validation': [
                "I hear you, and what you're feeling is completely valid.",
                "It takes courage to share what you're going through.",
                "Your emotions are real and important, and I'm here to listen.",
                "Thank you for trusting me with your feelings.",
                "It's okay to feel this way - you're not alone in this."
            ],
            'cognitive_reframing': [
                "Sometimes our thoughts can feel overwhelming. What evidence do we have for and against this thought?",
                "Let's try looking at this from a different angle. What would you tell a friend in this situation?",
                "That sounds like a really tough thought. What would a more balanced way of looking at this be?",
                "What would happen if we challenged that thought? Is there another way to see this?"
            ],
            'mindfulness_grounding': [
                "Let's take a moment to ground ourselves. Can you name 5 things you can see right now?",
                "Try this: Take a deep breath in for 4 counts, hold for 4, and breathe out for 6.",
                "Sometimes it helps to focus on the present moment. What's one thing you can feel right now?",
                "Let's practice a quick grounding exercise together. Focus on your breath for a moment."
            ],
            'coping_strategies': [
                "What are some things that have helped you feel better in the past?",
                "Let's think of some healthy ways to manage these feelings. What sounds doable for you?",
                "Here are some strategies that many people find helpful...",
                "What's one small step you could take today to care for yourself?"
            ],
            'hope_building': [
                "Even in difficult times, there are always possibilities for positive change.",
                "You've overcome challenges before, which shows your strength and resilience.",
                "This feeling is temporary, even though it might not feel that way right now.",
                "What's one thing you're looking forward to, even if it's small?"
            ],
            'behavioral_activation': [
                "Sometimes when we're feeling down, small activities can help. What's one tiny thing you could do today?",
                "Even small accomplishments matter. What's something manageable you could try?",
                "Movement can sometimes help shift our mood. What's a gentle activity you might enjoy?",
                "Breaking things into smaller steps can make them feel more manageable."
            ],
            'emotional_regulation': [
                "Strong emotions can feel overwhelming. What helps you when feelings get intense?",
                "It's okay to feel what you're feeling. How can we help you ride this wave?",
                "Emotions are like weather - they change. What helps you weather the storm?",
                "Let's work on some ways to help you feel more balanced."
            ]
        }

        # Crisis intervention templates
        self.crisis_intervention = {
            'immediate_safety': [
                "I'm really concerned about you right now. Your safety is the most important thing.",
                "It sounds like you're in a lot of pain. Let's focus on keeping you safe right now.",
                "I want you to know that you matter, and there are people who want to help you.",
                "Right now, let's focus on your immediate safety. You don't have to handle this alone."
            ],
            'crisis_resources': [
                "🚨 Crisis Hotlines:\n• National Suicide Prevention Lifeline: 988\n• Crisis Text Line: Text HOME to 741741\n• Your local emergency services: 911",
                "Please reach out to one of these resources immediately:\n• National Suicide Prevention Lifeline: 988\n• Crisis Text Line: Text HOME to 741741",
                "You deserve support right now. Here are some immediate resources:\n• 988 Suicide & Crisis Lifeline\n• Crisis Text Line: 741741",
                "Help is available 24/7:\n• Call or text 988 for the Suicide & Crisis Lifeline\n• Text HOME to 741741 for Crisis Text Line"
            ],
            'safety_planning': [
                "Let's create a safety plan together. What are some things that usually help when you're struggling?",
                "Who are the people in your life you can reach out to when things get tough?",
                "What are some warning signs that tell you when you need extra support?",
                "What are some coping strategies that have worked for you before?"
            ]
        }

        # Therapeutic technique guides
        self.technique_guides = {
            'deep_breathing': {
                'name': 'Deep Breathing Exercise',
                'instructions': [
                    "Let's try a simple breathing exercise together:",
                    "1. Breathe in slowly through your nose for 4 counts",
                    "2. Hold your breath for 4 counts", 
                    "3. Exhale slowly through your mouth for 6 counts",
                    "4. Repeat this 3-5 times",
                    "Focus only on your breathing and counting."
                ]
            },
            'grounding_5_4_3_2_1': {
                'name': '5-4-3-2-1 Grounding Technique',
                'instructions': [
                    "This technique helps bring you back to the present moment:",
                    "Name 5 things you can SEE around you",
                    "Name 4 things you can TOUCH", 
                    "Name 3 things you can HEAR",
                    "Name 2 things you can SMELL",
                    "Name 1 thing you can TASTE",
                    "Take your time with each step."
                ]
            },
            'thought_challenging': {
                'name': 'Thought Challenging',
                'instructions': [
                    "Let's examine this thought together:",
                    "1. What evidence supports this thought?",
                    "2. What evidence contradicts it?",
                    "3. What would you tell a friend having this thought?",
                    "4. What's a more balanced way to look at this?",
                    "5. How does this thought make you feel vs. how does the balanced thought make you feel?"
                ]
            },
            'progressive_muscle_relaxation': {
                'name': 'Progressive Muscle Relaxation',
                'instructions': [
                    "This helps release physical tension:",
                    "1. Start with your toes - tense them for 5 seconds, then relax",
                    "2. Move to your calves - tense, then relax",
                    "3. Continue with thighs, abdomen, hands, arms, shoulders",
                    "4. Finally, tense and relax your face muscles",
                    "Notice the difference between tension and relaxation."
                ]
            }
        }

    def analyze_sentiment(self, text: str) -> Dict[str, float]:
        """Analyze sentiment of text using VADER (fallback method)"""
        scores = sentiment_analyzer.polarity_scores(text)
        return {
            'compound': scores['compound'],
            'positive': scores['pos'],
            'neutral': scores['neu'],
            'negative': scores['neg']
        }

    def detect_crisis(self, text: str) -> Tuple[bool, float, List[str]]:
        """Detect crisis indicators in text"""
        text_lower = text.lower()
        detected_keywords = []
        
        # Check for crisis keywords
        for keyword in CRISIS_KEYWORDS:
            if keyword in text_lower:
                detected_keywords.append(keyword)
        
        # Calculate crisis score
        sentiment_scores = self.analyze_sentiment(text)
        negative_sentiment = sentiment_scores['negative']
        compound_sentiment = sentiment_scores['compound']
        
        # Crisis detection logic
        crisis_score = 0.0
        
        # Keyword-based scoring
        if detected_keywords:
            crisis_score += len(detected_keywords) * 0.3
        
        # Sentiment-based scoring
        if compound_sentiment < -0.5:
            crisis_score += abs(compound_sentiment) * 0.4
        
        if negative_sentiment > 0.7:
            crisis_score += negative_sentiment * 0.3
        
        # Determine if crisis detected
        crisis_threshold = float(os.getenv("CRISIS_THRESHOLD", "0.7"))
        is_crisis = crisis_score > crisis_threshold
        
        return is_crisis, crisis_score, detected_keywords

    def analyze_sentiment_advanced(self, text: str) -> Dict[str, float]:
        """Enhanced sentiment analysis using Hugging Face model"""
        try:
            if self.sentiment_pipeline:
                # Use HuggingFace sentiment analysis
                result = self.sentiment_pipeline(text)
                score = result[0]['score'] if result[0]['label'] == 'POSITIVE' else -result[0]['score']
                
                return {
                    'compound': score,
                    'positive': result[0]['score'] if result[0]['label'] == 'POSITIVE' else 0,
                    'negative': result[0]['score'] if result[0]['label'] == 'NEGATIVE' else 0,
                    'neutral': 1 - abs(score)
                }
            else:
                # Fallback to VADER
                return self.analyze_sentiment(text)
        except Exception as e:
            logging.error(f"Error in advanced sentiment analysis: {e}")
            return self.analyze_sentiment(text)

    def detect_emotions(self, text: str) -> Dict[str, float]:
        """Detect emotions using Hugging Face emotion model"""
        try:
            if self.emotion_pipeline:
                results = self.emotion_pipeline(text)
                emotions = {}
                for result in results:
                    emotions[result['label'].lower()] = result['score']
                return emotions
            else:
                # Fallback to keyword-based emotion detection
                emotions = {emotion: 0.0 for emotion in EMOTION_KEYWORDS.keys()}
                text_lower = text.lower()
                
                for emotion, keywords in EMOTION_KEYWORDS.items():
                    score = sum(1 for keyword in keywords if keyword in text_lower)
                    emotions[emotion] = min(score * 0.2, 1.0)
                
                return emotions
        except Exception as e:
            logging.error(f"Error in emotion detection: {e}")
            return {'neutral': 1.0}

    def classify_intent(self, text: str) -> Dict[str, float]:
        """Classify user intent using zero-shot classification"""
        try:
            if self.intent_pipeline:
                candidate_labels = [
                    "seeking emotional support",
                    "asking for advice",
                    "expressing crisis or distress",
                    "sharing positive news",
                    "wanting to vent",
                    "looking for coping strategies",
                    "requesting resources",
                    "casual conversation"
                ]
                
                result = self.intent_pipeline(text, candidate_labels)
                intent_scores = {}
                
                # Handle the pipeline result properly
                if isinstance(result, dict) and 'labels' in result and 'scores' in result:
                    for label, score in zip(result['labels'], result['scores']):
                        intent_scores[label] = float(score)
                elif isinstance(result, list) and len(result) > 0:
                    # Handle list response format
                    for item in result:
                        if isinstance(item, dict) and 'label' in item and 'score' in item:
                            intent_scores[item['label']] = float(item['score'])
                
                return intent_scores
            else:
                # Simple fallback intent detection
                text_lower = text.lower()
                if any(word in text_lower for word in ['help', 'advice', 'what should']):
                    return {'asking for advice': 0.8}
                elif any(word in text_lower for word in CRISIS_KEYWORDS):
                    return {'expressing crisis or distress': 0.9}
                elif any(word in text_lower for word in ['happy', 'great', 'amazing', 'wonderful']):
                    return {'sharing positive news': 0.7}
                else:
                    return {'seeking emotional support': 0.6}
        except Exception as e:
            logging.error(f"Error in intent classification: {e}")
            return {'seeking emotional support': 0.6}

    async def generate_response(self, user_message: str, conversation_history: Optional[List[Dict]] = None) -> Dict:
        """Generate AI response using intelligent conversation engine with dynamic personality adaptation"""
        
        # Use intelligent conversation engine for smart, contextual responses
        try:
            # Prepare user context for intelligent analysis
            user_context = {
                'message_count': len(conversation_history or []) + 1,
                'time_of_day': self._get_time_of_day(),
                'conversation_length': len(str(user_message))
            }
            
            intelligent_response = await intelligent_conversation_engine.generate_intelligent_response(
                user_message=user_message,
                conversation_history=conversation_history or [],
                user_context=user_context
            )
            
            # Add traditional analysis for comprehensive data
            sentiment = self.analyze_sentiment_advanced(user_message)
            emotions = self.detect_emotions(user_message)
            intent = self.classify_intent(user_message)
            
            # Enhanced crisis detection
            crisis_analysis = crisis_detector.analyze_crisis_severity(user_message, sentiment['compound'])
            crisis_keywords = ['suicide', 'kill myself', 'end it all', 'want to die', 'better off dead', 'hurt myself']
            has_explicit_crisis_language = any(keyword in user_message.lower() for keyword in crisis_keywords)
            is_crisis = has_explicit_crisis_language or crisis_analysis['crisis_level'] >= 4
            
            # Combine intelligent response with traditional analysis
            return {
                "content": intelligent_response["response"],
                "response": intelligent_response["response"],
                "sentiment_score": sentiment['compound'],
                "emotions": emotions,
                "intent": intent,
                "crisis_detected": is_crisis,
                "crisis_analysis": crisis_analysis,
                "personality_blend": intelligent_response["personality_blend"],
                "emotional_tone": intelligent_response["emotional_tone"],
                "conversation_context": intelligent_response["conversation_context"],
                "intelligence_analysis": intelligent_response["intelligence_analysis"],
                "adaptive_insights": intelligent_response.get("adaptive_insights", {}),
                "confidence": intelligent_response["confidence"],
                "source": "intelligent_conversation_engine"
            }
            
        except Exception as e:
            logging.error(f"Intelligent conversation engine error: {e}")
            # Fallback to enhanced response system
            return await self._generate_enhanced_response(user_message, conversation_history or [])
    
    def _get_time_of_day(self) -> str:
        """Get current time of day for context"""
        from datetime import datetime
        hour = datetime.now().hour
        if 5 <= hour < 12:
            return "morning"
        elif 12 <= hour < 17:
            return "afternoon"
        elif 17 <= hour < 21:
            return "evening"
        else:
            return "night"
    
    async def _generate_enhanced_response(self, user_message: str, conversation_history: List[Dict]) -> Dict:
        """Generate enhanced therapeutic response with conversation phase awareness"""
        
        # Analyze conversation context
        message_count = len(conversation_history)
        conversation_phase = self._determine_conversation_phase(message_count)
        
        # Analyze sentiment and emotions for enhanced understanding
        sentiment = self.analyze_sentiment_advanced(user_message)
        emotions = self.detect_emotions(user_message)
        intent = self.classify_intent(user_message)
        
        # Enhanced crisis detection with more nuanced analysis
        crisis_analysis = crisis_detector.analyze_crisis_severity(user_message, sentiment['compound'])
        
        # More sophisticated crisis determination
        crisis_keywords = ['suicide', 'kill myself', 'end it all', 'want to die', 'better off dead', 'hurt myself']
        has_explicit_crisis_language = any(keyword in user_message.lower() for keyword in crisis_keywords)
        
        # Only trigger crisis mode for explicit crisis language OR very high crisis levels
        is_crisis = has_explicit_crisis_language or crisis_analysis['crisis_level'] >= 4
        
        # Generate sophisticated response based on conversation phase and analysis
        if is_crisis:
            # Use crisis-specific enhanced response
            crisis_response = self._generate_enhanced_crisis_response(crisis_analysis, conversation_phase)
            ai_response = crisis_response
        else:
            # Generate phase-aware therapeutic response
            ai_response = self._generate_phase_aware_response(
                user_message, sentiment, emotions, intent, conversation_phase, message_count
            )
        
        return {
            "content": ai_response,
            "response": ai_response,
            "sentiment_score": sentiment['compound'],
            "emotions": emotions,
            "intent": intent,
            "crisis_detected": is_crisis,
            "crisis_analysis": crisis_analysis,
            "conversation_phase": conversation_phase,
            "confidence": 0.90,
            "source": "enhanced_ai_service"
        }
    
    def _determine_conversation_phase(self, message_count: int) -> str:
        """Determine conversation phase based on message count and context"""
        if message_count <= 2:
            return "initial_contact"
        elif message_count <= 5:
            return "early_building"
        elif message_count <= 10:
            return "deepening_engagement"
        else:
            return "sustained_conversation"
    
    def _generate_enhanced_crisis_response(self, crisis_analysis: Dict, conversation_phase: str) -> str:
        """Generate enhanced crisis intervention response"""
        severity = crisis_analysis['crisis_level']
        
        if severity >= 4:  # Critical
            return """I'm extremely concerned about you right now and want you to know that your life has value and meaning, even when it doesn't feel that way. These feelings you're experiencing are incredibly painful, but they can change with proper support.

Please reach out for immediate help:
🚨 If you're in immediate danger: Call 911
📞 National Suicide Prevention Lifeline: 988 (available 24/7)
💬 Crisis Text Line: Text HOME to 741741
🌐 Online chat: suicidepreventionlifeline.org

You don't have to face this alone. There are people who want to help you through this difficult time."""
        
        elif severity == 3:  # High
            return """I hear how much pain you're in right now, and I'm genuinely concerned about you. What you're feeling is incredibly difficult, but please know that these intense feelings can change, and you deserve support through this.

It's important that you don't have to handle this alone. Would you consider reaching out to:
📞 National Suicide Prevention Lifeline: 988
💬 Crisis Text Line: Text HOME to 741741
Or talking to a trusted friend, family member, or counselor?

Your life matters, and there are people who want to help you feel better."""
        
        else:
            return """I can sense you're going through a really tough time, and I want you to know that what you're feeling is understandable given what you're dealing with. While these feelings are intense right now, they don't have to be permanent.

You deserve support through this. If these feelings get stronger, please remember:
📞 Crisis support is available 24/7 at 988
💬 Text HOME to 741741 for crisis text support

Is there someone in your life you feel comfortable talking to about this?"""

    def _generate_phase_aware_response(self, user_message: str, sentiment: Dict, emotions: Dict, intent: Dict, phase: str, message_count: int) -> str:
        """Generate sophisticated response based on conversation phase"""
        
        # Base empathy and validation layer
        empathy_response = self._generate_empathy_layer(user_message, emotions)
        
        # Phase-specific response elements
        if phase == "initial_contact":
            phase_response = self._generate_initial_contact_response(user_message, sentiment)
        elif phase == "early_building":
            phase_response = self._generate_early_building_response(user_message, emotions, intent)
        elif phase == "deepening_engagement":
            phase_response = self._generate_deepening_response(user_message, sentiment, emotions)
        else:  # sustained_conversation
            phase_response = self._generate_sustained_response(user_message, sentiment, emotions, intent)
        
        # Combine layers with therapeutic techniques
        therapeutic_element = self._add_therapeutic_technique(emotions, sentiment, phase)
        
        # Construct final response
        response_parts = [empathy_response, phase_response]
        if therapeutic_element:
            response_parts.append(therapeutic_element)
        
        return " ".join(response_parts)
    
    def _generate_empathy_layer(self, user_message: str, emotions: Dict) -> str:
        """Generate empathetic foundation for response"""
        primary_emotion = max(emotions.items(), key=lambda x: x[1])[0] if emotions else 'neutral'
        
        empathy_responses = {
            'sad': "I can really hear the sadness in what you're sharing, and I want you to know that these feelings are completely valid.",
            'anxious': "I can sense the anxiety and worry in your words, and that must feel really overwhelming right now.",
            'angry': "I can feel the frustration and anger in what you're telling me, and those are completely understandable emotions.",
            'lonely': "The loneliness you're describing sounds really painful, and I want you to know that you're not alone in feeling this way.",
            'overwhelmed': "It sounds like you're dealing with so much right now, and feeling overwhelmed makes complete sense.",
            'hopeless': "I hear how hopeless things feel right now, and I can only imagine how heavy that must be to carry.",
            'default': "Thank you for sharing what's on your heart with me. I can hear that you're going through something significant."
        }
        
        return empathy_responses.get(primary_emotion, empathy_responses['default'])
    
    def _generate_initial_contact_response(self, user_message: str, sentiment: Dict) -> str:
        """Generate response for initial contact phase"""
        if sentiment['compound'] < -0.5:
            return "I'm really glad you felt safe enough to reach out and share this with me. It takes courage to open up about difficult feelings, and I'm honored that you trust me with this."
        elif sentiment['compound'] > 0.3:
            return "It's wonderful to hear from you, and I love that you're sharing these positive feelings. There's something really powerful about acknowledging and celebrating the good moments."
        else:
            return "I appreciate you taking the time to connect with me today. Whatever brought you here, I'm glad you're reaching out and I'm here to listen and support you."
    
    def _generate_early_building_response(self, user_message: str, emotions: Dict, intent: Dict) -> str:
        """Generate response for early relationship building phase"""
        if any(intent.get(key, 0) > 0.6 for key in ['seeking emotional support', 'wanting to vent']):
            return "I want you to feel completely free to share whatever is on your mind. Sometimes just having someone listen can make a real difference. What would be most helpful for you right now?"
        else:
            return "I'm starting to understand what you're going through, and I want you to know that your feelings make complete sense. Let's explore this together - what feels most important to talk about?"
    
    def _generate_deepening_response(self, user_message: str, sentiment: Dict, emotions: Dict) -> str:
        """Generate response for deepening engagement phase"""
        return "As we've been talking, I'm getting a deeper sense of what you're experiencing. Your insights about yourself show real self-awareness, and that's actually a strength even in difficult times. How are you feeling about the things we've been exploring together?"
    
    def _generate_sustained_response(self, user_message: str, sentiment: Dict, emotions: Dict, intent: Dict) -> str:
        """Generate response for sustained conversation phase"""
        return "I really value the trust you've built with me through our conversations. You've been so open about your experiences, and I can see the growth and reflection happening. What feels most important to focus on as we continue this journey together?"
    
    def _add_therapeutic_technique(self, emotions: Dict, sentiment: Dict, phase: str) -> Optional[str]:
        """Add appropriate therapeutic technique based on emotional state and phase"""
        primary_emotion = max(emotions.items(), key=lambda x: x[1])[0] if emotions else 'neutral'
        sentiment_score = sentiment.get('compound', 0)
        
        if phase in ["deepening_engagement", "sustained_conversation"]:
            if primary_emotion in ['anxious', 'overwhelmed'] and sentiment_score < -0.4:
                return "\n\nSince you're feeling anxious, would you like to try a quick grounding exercise? We could do the 5-4-3-2-1 technique together - it can help bring you back to the present moment when anxiety feels overwhelming."
            elif primary_emotion == 'sad' and sentiment_score < -0.5:
                return "\n\nWhen we're feeling this way, sometimes it helps to challenge our thoughts gently. What evidence do we have that supports this difficult thought? And what evidence might contradict it? You don't have to figure it all out right now."
            elif primary_emotion in ['angry', 'frustrated']:
                return "\n\nIntense emotions like anger can be really draining. Have you tried any techniques that help you release that energy in healthy ways? Sometimes physical movement or even writing can help process these feelings."
        
        return None
    
    async def _generate_routed_response(self, user_message: str, conversation_history: Optional[List[Dict]] = None) -> Dict:
        """Generate AI response using intelligent routing between Hugging Face and Gemini models"""
        
        # Use the intelligent routing system
        routed_response = await response_router.get_routed_response(
            user_message=user_message,
            conversation_history=conversation_history or [],
            hugging_face_fallback_func=self._generate_hugging_face_response
        )
        
        return routed_response
    
    async def _generate_hugging_face_response(self, user_message: str, conversation_history: Optional[List[Dict]] = None) -> Dict:
        """Generate AI response using Hugging Face models (original implementation)"""
        
        # Analyze sentiment and emotions
        sentiment = self.analyze_sentiment_advanced(user_message)
        emotions = self.detect_emotions(user_message)
        intent = self.classify_intent(user_message)
        
        # Check for crisis using enhanced detection system
        crisis_analysis = crisis_detector.analyze_crisis_severity(user_message, sentiment['compound'])
        is_crisis = crisis_analysis['crisis_level'] >= 3
        crisis_score = crisis_analysis['confidence']
        crisis_keywords = crisis_analysis['detected_keywords']
        
        try:
            # Generate therapeutic response
            if is_crisis:
                # Use crisis-specific response
                crisis_response = crisis_detector.get_crisis_response(crisis_analysis)
                ai_response = crisis_response['message']
            else:
                # Generate therapeutic response
                ai_response = self.generate_therapeutic_response(
                    user_message, sentiment, emotions, intent, crisis_analysis
                )
            
            return {
                "content": ai_response,
                "response": ai_response,  # For backward compatibility
                "sentiment_score": sentiment['compound'],
                "emotions": emotions,
                "intent": intent,
                "crisis_detected": is_crisis,
                "crisis_analysis": crisis_analysis,
                "crisis_score": crisis_score,
                "crisis_keywords": crisis_keywords,
                "confidence": 0.85 if self.sentiment_pipeline else 0.6,
                "source": "hugging_face"
            }
            
        except Exception as e:
            logging.error(f"AI service error: {e}")
            return {
                "content": self._generate_fallback_response(user_message, sentiment, is_crisis),
                "response": self._generate_fallback_response(user_message, sentiment, is_crisis),  # For backward compatibility
                "sentiment_score": sentiment['compound'],
                "emotions": emotions,
                "intent": intent,
                "crisis_detected": is_crisis,
                "crisis_score": crisis_score,
                "crisis_keywords": crisis_keywords,
                "confidence": 0.6,
                "source": "hugging_face"
            }

    def _generate_fallback_response(self, user_message: str, sentiment: Dict, is_crisis: bool) -> str:
        """Generate fallback response when AI models are not available"""
        
        if is_crisis:
            return """I hear that you're going through a really difficult time right now, and I'm genuinely concerned about you. What you're feeling is incredibly hard, but please know that you matter and that there are people who want to help.

These feelings can feel overwhelming, but they can change. You don't have to face this alone. Would you consider reaching out to someone you trust, or calling a crisis helpline where trained counselors can provide immediate support?

Your life has value, and there are people who care about you, even when it doesn't feel that way."""

        if sentiment['compound'] < -0.3:
            responses = [
                "I can hear that you're going through a tough time. It's okay to feel this way - your feelings are valid. What's one small thing that might bring you a tiny bit of comfort right now?",
                "That sounds really difficult. Thank you for sharing this with me. Sometimes when we're struggling, it can help to remember that difficult emotions are temporary. What's helped you get through hard times before?",
                "I'm glad you felt safe enough to share this with me. When we're feeling low, it's important to be gentle with ourselves. Have you been able to take care of your basic needs today - eating, sleeping, staying hydrated?"
            ]
        elif sentiment['compound'] > 0.3:
            responses = [
                "It's wonderful to hear some positivity in your message! Those moments of feeling good are so important. What do you think contributed to feeling this way?",
                "I love hearing about the good moments! It's great that you're noticing and appreciating them. How can you carry this positive energy forward?",
                "That's fantastic! It's so valuable to acknowledge and celebrate these positive feelings. What made this experience special for you?"
            ]
        else:
            responses = [
                "Thank you for sharing with me. How are you feeling in this moment? Sometimes it helps to just pause and check in with ourselves.",
                "I appreciate you taking the time to connect. What's on your mind today? I'm here to listen and support you.",
                "How has your day been so far? Remember, it's okay to have ups and downs - that's part of being human."
            ]
        
        import random
        return random.choice(responses)

    def generate_journal_prompt(self, mood_level: Optional[int] = None, recent_entries: Optional[List[str]] = None) -> str:
        """Generate personalized journal prompt"""
        
        prompts_by_mood = {
            1: [  # Very sad
                "Write about one small thing that brought you comfort today, no matter how tiny it might seem.",
                "What would you say to a friend who was feeling the way you feel right now?",
                "Describe a place where you feel safe and peaceful. What makes it special?"
            ],
            2: [  # Sad
                "What's one challenge you're facing, and what's one small step you could take toward addressing it?",
                "Write about someone who cares about you. How do they show they care?",
                "What's something you're looking forward to, even if it's small?"
            ],
            3: [  # Neutral
                "Reflect on your day - what went well, and what could have been better?",
                "What's something new you learned about yourself recently?",
                "Describe a moment today when you felt most like yourself."
            ],
            4: [  # Good
                "What made you feel good today? How can you create more moments like this?",
                "Write about a strength or skill you used today. How did it help you?",
                "What's something you're proud of accomplishing lately?"
            ],
            5: [  # Very happy
                "Capture this good feeling - what led to it, and how can you remember this moment?",
                "What are three things you're grateful for today, and why?",
                "How can you share this positive energy with others?"
            ]
        }
        
        general_prompts = [
            "What are three things you're grateful for today?",
            "Describe a moment when you felt proud of yourself.",
            "What's one thing you'd like to let go of, and one thing you'd like to embrace?",
            "Write about a person who has positively influenced your life.",
            "What does self-care look like for you right now?",
            "What's a lesson you've learned recently about yourself or life?",
            "Describe your ideal day. What elements from it can you incorporate into your real life?",
            "What's something that challenges you, and how are you growing from it?",
            "Write about a time when you overcame a difficulty. What strengths did you use?",
            "What would you tell your younger self about handling difficult emotions?"
        ]
        
        if mood_level and mood_level in prompts_by_mood:
            import random
            return random.choice(prompts_by_mood[mood_level])
        else:
            import random
            return random.choice(general_prompts)

    def generate_therapeutic_response(self, user_message: str, sentiment: Dict[str, float], emotions: Dict[str, float], intent: Dict[str, float], crisis_analysis: Dict) -> str:
        """Generate evidence-based therapeutic response based on user input analysis"""
        
        # Handle crisis situations first
        if crisis_analysis['crisis_level'] >= 3:
            safety_response = random.choice(self.crisis_intervention['immediate_safety'])
            resources = random.choice(self.crisis_intervention['crisis_resources'])
            return f"{safety_response}\n\n{resources}"
        
        # Determine primary emotion and sentiment
        primary_emotion = max(emotions.items(), key=lambda x: x[1])[0] if emotions else 'neutral'
        sentiment_score = sentiment.get('compound', 0)
        
        # Select therapeutic approach based on primary emotion and intent
        therapeutic_responses = []
        
        # Always start with validation
        validation = random.choice(self.therapeutic_templates['validation'])
        therapeutic_responses.append(validation)
        
        # Add emotion-specific therapeutic response
        if primary_emotion in ['sad', 'depressed'] and sentiment_score < -0.3:
            # Depression support with behavioral activation
            behavioral_response = random.choice(self.therapeutic_templates['behavioral_activation'])
            hope_response = random.choice(self.therapeutic_templates['hope_building'])
            therapeutic_responses.extend([behavioral_response, hope_response])
            
        elif primary_emotion in ['anxious', 'worried', 'nervous'] or any('anxious' in k for k in intent.keys() if intent[k] > 0.5):
            # Anxiety management with grounding
            grounding_response = random.choice(self.therapeutic_templates['mindfulness_grounding'])
            coping_response = random.choice(self.therapeutic_templates['coping_strategies'])
            therapeutic_responses.extend([grounding_response, coping_response])
            
        elif primary_emotion in ['angry', 'frustrated', 'irritated']:
            # Emotional regulation support
            regulation_response = random.choice(self.therapeutic_templates['emotional_regulation'])
            coping_response = random.choice(self.therapeutic_templates['coping_strategies'])
            therapeutic_responses.extend([regulation_response, coping_response])
            
        elif any('negative thoughts' in k for k in intent.keys() if intent[k] > 0.5):
            # Cognitive reframing for negative thinking
            reframing_response = random.choice(self.therapeutic_templates['cognitive_reframing'])
            therapeutic_responses.append(reframing_response)
            
        else:
            # General support with coping strategies
            coping_response = random.choice(self.therapeutic_templates['coping_strategies'])
            therapeutic_responses.append(coping_response)
        
        # Add technique suggestion if appropriate
        if sentiment_score < -0.5 or primary_emotion in ['anxious', 'overwhelmed']:
            technique = self.suggest_therapeutic_technique(primary_emotion, sentiment_score)
            if technique:
                therapeutic_responses.append(technique)
        
        # End with hope and encouragement if sentiment is very negative
        if sentiment_score < -0.6:
            hope_response = random.choice(self.therapeutic_templates['hope_building'])
            therapeutic_responses.append(hope_response)
        
        return ' '.join(therapeutic_responses)

    def suggest_therapeutic_technique(self, emotion: str, sentiment_score: float) -> Optional[str]:
        """Suggest specific therapeutic techniques based on emotional state"""
        
        if emotion in ['anxious', 'worried', 'nervous', 'overwhelmed']:
            # Suggest anxiety management techniques
            if sentiment_score < -0.7:
                technique = self.technique_guides['grounding_5_4_3_2_1']
                instructions = '\n'.join(technique['instructions'])
                return f"\n\n**{technique['name']}:**\n{instructions}"
            else:
                technique = self.technique_guides['deep_breathing']
                instructions = '\n'.join(technique['instructions'])
                return f"\n\n**{technique['name']}:**\n{instructions}"
                
        elif emotion in ['sad', 'depressed'] and sentiment_score < -0.6:
            # Suggest thought challenging for negative thinking
            technique = self.technique_guides['thought_challenging']
            instructions = '\n'.join(technique['instructions'])
            return f"\n\n**{technique['name']}:**\n{instructions}"
            
        elif emotion in ['angry', 'frustrated'] or sentiment_score < -0.8:
            # Suggest muscle relaxation for intense emotions
            technique = self.technique_guides['progressive_muscle_relaxation']
            instructions = '\n'.join(technique['instructions'])
            return f"\n\n**{technique['name']}:**\n{instructions}"
        
        return None

    def provide_personalized_coping_strategies(self, emotions: Dict[str, float], intent: Dict[str, float]) -> List[str]:
        """Provide personalized coping strategies based on user's emotional state and intent"""
        
        strategies = []
        primary_emotion = max(emotions.items(), key=lambda x: x[1])[0] if emotions else 'neutral'
        
        # Emotion-specific strategies
        if primary_emotion in ['anxious', 'worried']:
            strategies.extend([
                "🧘 Try the 4-7-8 breathing technique: breathe in for 4, hold for 7, out for 8",
                "📝 Write down your worries and rate how likely they are to happen (1-10)",
                "🚶 Take a 5-minute walk outside if possible",
                "📱 Use a grounding app or listen to calming music"
            ])
        elif primary_emotion in ['sad', 'depressed']:
            strategies.extend([
                "☀️ Get some natural light - even 10 minutes helps",
                "👥 Reach out to one friend or family member",
                "📚 Do one small thing you usually enjoy, even briefly",
                "🛌 Maintain a regular sleep schedule"
            ])
        elif primary_emotion in ['angry', 'frustrated']:
            strategies.extend([
                "💨 Try intense physical exercise or punch a pillow",
                "🧊 Hold ice cubes or take a cold shower",
                "📝 Write out your feelings without censoring",
                "🎵 Listen to music that matches then shifts your mood"
            ])
        elif primary_emotion == 'lonely':
            strategies.extend([
                "📞 Call or text someone you trust",
                "👥 Join an online community or support group",
                "🐕 Volunteer with animals or community organizations",
                "☕ Go to a public place like a coffee shop or library"
            ])
        
        # Intent-specific strategies
        if any('coping' in k for k in intent.keys() if intent[k] > 0.5):
            strategies.extend([
                "🎯 Create a daily routine with small, achievable goals",
                "📱 Use mental health apps like Headspace or Calm",
                "🧘 Practice mindfulness for just 5 minutes daily",
                "📓 Keep a mood journal to track patterns"
            ])
        
        return strategies[:4]  # Return top 4 strategies
    
    def get_routing_statistics(self) -> Dict[str, Any]:
        """Get current routing statistics from the response router"""
        return response_router.get_routing_statistics()
    
    def reset_routing_statistics(self) -> None:
        """Reset routing statistics"""
        response_router.reset_statistics()

# Global AI service instance
ai_service = AIService()