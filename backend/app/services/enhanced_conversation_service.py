"""
Enhanced Conversation Response System for MindSpark AI
Implements sophisticated therapeutic conversation patterns from greetings to crisis support
"""

from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, time
import re
import random
from enum import Enum
from dataclasses import dataclass

class ConversationPhase(Enum):
    INITIAL_CONTACT = "initial_contact"
    EARLY_BUILDING = "early_building" 
    DEEPENING_ENGAGEMENT = "deepening_engagement"
    SUSTAINED_CONVERSATION = "sustained_conversation"
    CRISIS_INTERVENTION = "crisis_intervention"
    CONVERSATION_CLOSURE = "conversation_closure"

class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class ConversationContext:
    user_id: str
    message_count: int
    time_of_day: str
    recent_mood_patterns: List[Dict]
    previous_conversations: List[Dict]
    crisis_history: List[Dict]
    is_new_user: bool
    last_interaction_days: int
    current_mood_indicators: Dict

@dataclass
class ResponseLayers:
    empathy_foundation: str
    cognitive_processing: str
    action_oriented_support: str
    therapeutic_framework: str
    safety_validation: str

class EnhancedConversationService:
    def __init__(self):
        self.greeting_patterns = self._initialize_greeting_patterns()
        self.therapeutic_frameworks = self._initialize_therapeutic_frameworks()
        self.crisis_indicators = self._initialize_crisis_indicators()
        self.coping_strategies = self._initialize_coping_strategies()
        self.conversation_closures = self._initialize_conversation_closures()
    
    def _initialize_greeting_patterns(self) -> Dict:
        return {
            "simple_greetings": ["hi", "hello", "hey", "heya", "hiya", "sup", "what's up"],
            "question_greetings": ["how are you", "how's it going", "how are things"],
            "time_specific": {
                "morning": ["good morning", "morning"],
                "afternoon": ["good afternoon", "afternoon"],
                "evening": ["good evening", "evening"],
                "night": ["good night", "night"]
            }
        }
    
    def _initialize_therapeutic_frameworks(self) -> Dict:
        return {
            "cbt_techniques": [
                "What thoughts go through your mind when this happens?",
                "How does your body feel when you experience this?", 
                "What evidence supports or challenges this thought?",
                "What would you tell a friend going through something similar?"
            ],
            "dbt_skills": [
                "Let's try a grounding technique - can you name 5 things you can see right now?",
                "Sometimes taking deep breaths can help. Want to try breathing with me?",
                "What emotion are you feeling most strongly right now?",
                "How intense is this feeling on a scale of 1-10?"
            ],
            "mindfulness_practices": [
                "Let's focus on this moment together. What are you noticing right now?",
                "Sometimes it helps to observe our thoughts without judgment.",
                "Can you take a moment to notice your breathing?",
                "What would it feel like to be kind to yourself right now?"
            ],
            "act_principles": [
                "What matters most to you in this situation?",
                "How does this align with your values?",
                "What would you do if this feeling wasn't in the way?",
                "What small step could you take toward what's important to you?"
            ]
        }
    
    def _initialize_crisis_indicators(self) -> Dict:
        return {
            "low_risk": {
                "keywords": ["stressed", "overwhelmed", "tired", "frustrated", "annoyed"],
                "patterns": ["having a hard time", "difficult day", "not great"]
            },
            "medium_risk": {
                "keywords": ["hopeless", "worthless", "trapped", "desperate", "empty"],
                "patterns": ["can't take it", "want to give up", "nothing matters"]
            },
            "high_risk": {
                "keywords": ["suicide", "kill myself", "end it all", "better off dead"],
                "patterns": ["want to die", "hurt myself", "not worth living"]
            },
            "critical_risk": {
                "keywords": ["plan to die", "going to kill", "tonight is the night"],
                "patterns": ["have a plan", "already decided", "goodbye"]
            }
        }
    
    def _initialize_coping_strategies(self) -> Dict:
        return {
            "anxiety": [
                "Try the 4-7-8 breathing technique: breathe in for 4, hold for 7, out for 8",
                "Ground yourself with the 5-4-3-2-1 technique: 5 things you see, 4 you hear, 3 you touch, 2 you smell, 1 you taste",
                "Progressive muscle relaxation can help - tense and release each muscle group"
            ],
            "depression": [
                "Even small activities can help - maybe try taking a short walk or calling a friend",
                "Depression lies to us about our worth. You matter, even when it doesn't feel that way",
                "Sometimes just getting through today is enough, and that's okay"
            ],
            "stress": [
                "Let's break this down into smaller, manageable pieces",
                "What's one thing you have control over in this situation?",
                "Taking breaks isn't giving up - it's taking care of yourself"
            ],
            "social_anxiety": [
                "Remember that most people are focused on themselves, not judging you",
                "Start with small social interactions and build up gradually",
                "Your worth isn't determined by others' opinions of you"
            ]
        }
    
    def _initialize_conversation_closures(self) -> List[str]:
        return [
            "Thank you for sharing all of this with me today. I can really see your strength in how you're working through these challenges, even when it feels overwhelming. Remember that the coping strategies we talked about are always available to you, and I'll be here whenever you need to talk. You're not alone in this, and reaching out today shows incredible courage. Take care of yourself, and remember - you've got this! 💙",
            
            "I'm so glad you felt comfortable opening up with me today. The insights you've shared show real self-awareness, and that's a powerful tool for healing. Keep being gentle with yourself as you navigate these feelings. I'm here whenever you need support, and remember that seeking help is a sign of strength, not weakness. You matter, and your feelings are valid. Until next time, take care! 🌟",
            
            "What a meaningful conversation we've had today. You've shown such courage in exploring these difficult emotions and I'm honored you trusted me with them. The progress you're making, even in small steps, is something to be proud of. Remember, healing isn't linear - be patient with yourself. I'm always here when you need someone to listen. You're stronger than you know! 💜"
        ]
        
        # Generate appropriate response based on phase
        if phase == ConversationPhase.INITIAL_CONTACT:
            return await self._generate_initial_contact_response(user_message, context)
        elif phase == ConversationPhase.EARLY_BUILDING:
            return await self._generate_early_building_response(user_message, context)
        elif phase == ConversationPhase.DEEPENING_ENGAGEMENT:
            return await self._generate_deepening_response(user_message, context)
        elif phase == ConversationPhase.SUSTAINED_CONVERSATION:
            return await self._generate_sustained_response(user_message, context)
        else:
            return await self._generate_closure_response(user_message, context)
    
    def _determine_conversation_phase(self, user_message: str, context: ConversationContext) -> ConversationPhase:
        """Determine what phase of conversation we're in"""
        
        if context.message_count <= 1:
            return ConversationPhase.INITIAL_CONTACT
        elif context.message_count <= 5:
            return ConversationPhase.EARLY_BUILDING
        elif context.message_count <= 15:
            return ConversationPhase.DEEPENING_ENGAGEMENT
        elif context.message_count > 15:
            return ConversationPhase.SUSTAINED_CONVERSATION
        else:
            return ConversationPhase.CONVERSATION_CLOSURE
    
    def _assess_crisis_risk(self, user_message: str, context: ConversationContext) -> RiskLevel:
        """Assess crisis risk level based on message content and context"""
        
        message_lower = user_message.lower()
        
        # Check for critical risk indicators
        for keyword in self.crisis_indicators["critical_risk"]["keywords"]:
            if keyword in message_lower:
                return RiskLevel.CRITICAL
        
        for pattern in self.crisis_indicators["critical_risk"]["patterns"]:
            if pattern in message_lower:
                return RiskLevel.CRITICAL
        
        # Check for high risk indicators
        for keyword in self.crisis_indicators["high_risk"]["keywords"]:
            if keyword in message_lower:
                return RiskLevel.HIGH
        
        for pattern in self.crisis_indicators["high_risk"]["patterns"]:
            if pattern in message_lower:
                return RiskLevel.HIGH
        
        # Check for medium risk indicators
        for keyword in self.crisis_indicators["medium_risk"]["keywords"]:
            if keyword in message_lower:
                return RiskLevel.MEDIUM
        
        for pattern in self.crisis_indicators["medium_risk"]["patterns"]:
            if pattern in message_lower:
                return RiskLevel.MEDIUM
        
        # Check for low risk indicators
        for keyword in self.crisis_indicators["low_risk"]["keywords"]:
            if keyword in message_lower:
                return RiskLevel.LOW
        
        return RiskLevel.LOW
    
    async def _generate_initial_contact_response(self, user_message: str, context: ConversationContext) -> Dict[str, Any]:
        """Generate sophisticated initial contact responses"""
        
        message_lower = user_message.lower().strip()
        time_period = self._get_time_period()
        
        # Check if it's a greeting
        is_greeting = any(greeting in message_lower for greeting in self.greeting_patterns["simple_greetings"])
        is_question_greeting = any(greeting in message_lower for greeting in self.greeting_patterns["question_greetings"])
        
        if is_greeting or is_question_greeting:
            return await self._generate_greeting_response(context, time_period)
        else:
            return await self._generate_opening_response(user_message, context)
    
    async def _generate_greeting_response(self, context: ConversationContext, time_period: str) -> Dict[str, Any]:
        """Generate personalized greeting responses"""
        
        # Base greeting components
        time_greetings = {
            "morning": ["Good morning! 🌅", "Morning! Hope you're starting your day well ☀️"],
            "afternoon": ["Good afternoon! 🌞", "Hi there! Hope your day is going okay 🌤️"],
            "evening": ["Good evening! 🌅", "Evening! Thanks for reaching out 🌆"],
            "night": ["Hi there! 🌙", "Thanks for reaching out tonight 🌟"]
        }
        
        # Select appropriate time-based greeting
        greeting_options = time_greetings.get(time_period, ["Hi there! 😊", "Hello! So glad you reached out 🌟"])
        base_greeting = random.choice(greeting_options)
        
        # Add personalization based on user context
        if context.is_new_user:
            personalization = "I'm really glad you decided to reach out today. I'm here as your supportive companion whenever you need someone to talk with. "
            mood_check = "How are you feeling right now? Whether you want to share something specific or just chat, I'm here to listen without any judgment."
        else:
            if context.last_interaction_days == 0:
                personalization = "Good to see you again today! I'm always here when you need support. "
            elif context.last_interaction_days == 1:
                personalization = "Welcome back! It's good to hear from you again. "
            else:
                personalization = f"It's been {context.last_interaction_days} days since we last talked - I'm glad you're here now. "
            
            # Reference previous conversations if appropriate
            if context.previous_conversations:
                last_topic = context.previous_conversations[-1].get('main_theme', '')
                if last_topic:
                    personalization += f"I've been thinking about our conversation regarding {last_topic}. "
            
            mood_check = "How are things going for you today? I'm here to listen and support you however I can."
        
        # Add privacy reassurance for new users
        privacy_note = ""
        if context.is_new_user:
            privacy_note = " Everything we discuss is completely private and confidential."
        
        response_text = f"{base_greeting} {personalization}{mood_check}{privacy_note}"
        
        return {
            "response": response_text,
            "confidence": 0.95,
            "source": "enhanced_conversation_service",
            "conversation_phase": "initial_contact",
            "therapeutic_elements": ["empathy", "safety_building", "invitation_to_share"],
            "suggested_follow_ups": [
                "Tell me more about how you're feeling",
                "What's been on your mind lately?",
                "Is there something specific you'd like to talk about?"
            ]
        }
    
    async def _generate_opening_response(self, user_message: str, context: ConversationContext) -> Dict[str, Any]:
        """Generate response when user opens with something other than greeting"""
        
        # Build empathy foundation
        empathy_phrases = [
            "Thank you for sharing that with me.",
            "I really appreciate you opening up about this.",
            "It takes courage to reach out when you're going through something difficult.",
            "I'm glad you felt comfortable talking about this with me."
        ]
        
        empathy = random.choice(empathy_phrases)
        
        # Add validation and gentle exploration
        validation = "Your feelings are completely valid, and it's important that you're acknowledging them."
        exploration = "Would you like to tell me more about what's been going on? I'm here to listen and support you."
        
        response_text = f"{empathy} {validation} {exploration}"
        
        return {
            "response": response_text,
            "confidence": 0.90,
            "source": "enhanced_conversation_service", 
            "conversation_phase": "initial_contact",
            "therapeutic_elements": ["empathy", "validation", "gentle_exploration"],
            "suggested_follow_ups": [
                "How long have you been feeling this way?",
                "What do you think might be contributing to these feelings?",
                "Have you experienced something like this before?"
            ]
        }
    
    async def _generate_early_building_response(self, user_message: str, context: ConversationContext) -> Dict[str, Any]:
        """Generate responses for early conversation building (messages 2-5)"""
        
        # Analyze message for emotional content
        emotional_keywords = self._extract_emotional_keywords(user_message)
        main_concern = self._identify_main_concern(user_message)
        
        # Build response layers
        empathy = self._generate_empathy_layer(emotional_keywords, main_concern)
        validation = self._generate_validation_layer(user_message)
        exploration = self._generate_gentle_exploration(main_concern)
        
        response_text = f"{empathy} {validation} {exploration}"
        
        # Add coping suggestion if appropriate
        if main_concern in self.coping_strategies:
            coping_suggestion = random.choice(self.coping_strategies[main_concern])
            response_text += f" In the meantime, {coping_suggestion.lower()}"
        
        return {
            "response": response_text,
            "confidence": 0.88,
            "source": "enhanced_conversation_service",
            "conversation_phase": "early_building",
            "therapeutic_elements": ["empathy", "validation", "gentle_exploration", "coping_support"],
            "main_concern_identified": main_concern,
            "emotional_keywords": emotional_keywords
        }
    
    async def _generate_deepening_response(self, user_message: str, context: ConversationContext) -> Dict[str, Any]:
        """Generate responses for deepening engagement (messages 6-15)"""
        
        # Select appropriate therapeutic framework
        framework = self._select_therapeutic_framework(user_message, context)
        
        # Generate multi-layer response
        empathy = self._generate_empathy_layer(self._extract_emotional_keywords(user_message), self._identify_main_concern(user_message))
        cognitive_processing = self._generate_cognitive_processing(user_message, framework)
        action_support = self._generate_action_oriented_support(user_message)
        
        response_text = f"{empathy} {cognitive_processing} {action_support}"
        
        return {
            "response": response_text,
            "confidence": 0.92,
            "source": "enhanced_conversation_service",
            "conversation_phase": "deepening_engagement", 
            "therapeutic_framework": framework,
            "therapeutic_elements": ["empathy", "cognitive_processing", "action_oriented_support"]
        }
    
    async def _generate_sustained_response(self, user_message: str, context: ConversationContext) -> Dict[str, Any]:
        """Generate responses for sustained conversations (15+ messages)"""
        
        # Check for conversation fatigue
        energy_level = self._assess_conversation_energy(user_message, context)
        
        if energy_level == "low":
            return await self._suggest_conversation_break(context)
        
        # Continue with advanced therapeutic techniques
        empathy = self._generate_empathy_layer(self._extract_emotional_keywords(user_message), self._identify_main_concern(user_message))
        insight_building = self._generate_insight_building_response(user_message, context)
        progress_acknowledgment = self._acknowledge_therapeutic_progress(context)
        
        response_text = f"{empathy} {insight_building} {progress_acknowledgment}"
        
        return {
            "response": response_text,
            "confidence": 0.90,
            "source": "enhanced_conversation_service",
            "conversation_phase": "sustained_conversation",
            "therapeutic_elements": ["empathy", "insight_building", "progress_acknowledgment"]
        }
    
    async def _generate_crisis_response(self, user_message: str, context: ConversationContext, risk_level: RiskLevel) -> Dict[str, Any]:
        """Generate crisis intervention responses"""
        
        if risk_level == RiskLevel.CRITICAL:
            return await self._generate_critical_crisis_response(user_message, context)
        elif risk_level == RiskLevel.HIGH:
            return await self._generate_high_risk_response(user_message, context)
        elif risk_level == RiskLevel.MEDIUM:
            return await self._generate_medium_risk_response(user_message, context)
        else:
            return await self._generate_low_risk_response(user_message, context)
    
    async def _generate_critical_crisis_response(self, user_message: str, context: ConversationContext) -> Dict[str, Any]:
        """Generate response for critical crisis situations"""
        
        immediate_concern = "I'm very concerned about what you've shared with me. Your safety is the most important thing right now."
        
        crisis_resources = """
🆘 **IMMEDIATE HELP AVAILABLE 24/7:**
• National Suicide Prevention Lifeline: 988
• Crisis Text Line: Text HOME to 741741  
• Emergency Services: 911

🌟 **You are not alone. People want to help you.**
        """
        
        safety_check = "Can you tell me if you have a safe place to be right now? Is there a trusted person you can reach out to?"
        
        hope_message = "I know it might not feel like it right now, but there are people who care about you and want to help. These feelings can change, and there are ways through this pain."
        
        response_text = f"{immediate_concern}\n\n{crisis_resources}\n{safety_check}\n\n{hope_message}"
        
        return {
            "response": response_text,
            "confidence": 1.0,
            "source": "crisis_intervention_system",
            "conversation_phase": "crisis_intervention",
            "risk_level": "critical",
            "crisis_resources_provided": True,
            "requires_immediate_attention": True,
            "therapeutic_elements": ["immediate_safety", "crisis_resources", "hope_instillation"]
        }
    
    async def _generate_high_risk_response(self, user_message: str, context: ConversationContext) -> Dict[str, Any]:
        """Generate response for high-risk situations"""
        
        concern = "I notice you mentioned feeling hopeless about this situation. Those feelings can be really overwhelming, and I'm concerned about you."
        
        immediate_support = "Let's talk about some ways to manage these intense emotions. What has helped you get through difficult times before?"
        
        resources = """
**Support available anytime:**
• National Suicide Prevention Lifeline: 988
• Crisis Text Line: Text HOME to 741741
• Or talk to a trusted friend, family member, or counselor
        """
        
        coping_strategies = "Right now, try to focus on getting through this moment. Some people find it helpful to take slow, deep breaths, call someone they trust, or do something that usually brings them comfort."
        
        response_text = f"{concern} {immediate_support}\n\n{resources}\n\n{coping_strategies}"
        
        return {
            "response": response_text,
            "confidence": 0.95,
            "source": "crisis_intervention_system", 
            "conversation_phase": "crisis_intervention",
            "risk_level": "high",
            "crisis_resources_provided": True,
            "therapeutic_elements": ["concern_expression", "immediate_coping", "resource_provision"]
        }
    
    # Utility methods
    def _get_time_period(self) -> str:
        """Determine current time period for appropriate greetings"""
        current_hour = datetime.now().hour
        
        if 6 <= current_hour < 12:
            return "morning"
        elif 12 <= current_hour < 17:
            return "afternoon" 
        elif 17 <= current_hour < 22:
            return "evening"
        else:
            return "night"
    
    def _extract_emotional_keywords(self, text: str) -> List[str]:
        """Extract emotional keywords from user message"""
        emotional_words = [
            "sad", "happy", "angry", "frustrated", "anxious", "worried", "scared", "excited",
            "depressed", "overwhelmed", "stressed", "lonely", "hopeful", "grateful", "confused",
            "hurt", "disappointed", "proud", "ashamed", "guilty", "relieved", "peaceful"
        ]
        
        text_lower = text.lower()
        found_emotions = [word for word in emotional_words if word in text_lower]
        return found_emotions
    
    def _identify_main_concern(self, text: str) -> str:
        """Identify the main concern category from user message"""
        concern_keywords = {
            "anxiety": ["anxious", "worried", "panic", "nervous", "scared", "fear"],
            "depression": ["sad", "depressed", "hopeless", "empty", "worthless"],
            "stress": ["stressed", "overwhelmed", "pressure", "busy", "deadline"],
            "social_anxiety": ["social", "friends", "embarrassed", "judged", "awkward"],
            "relationships": ["relationship", "boyfriend", "girlfriend", "family", "friends"],
            "academic": ["school", "homework", "exam", "grades", "college", "study"],
            "work": ["job", "work", "boss", "career", "interview", "workplace"]
        }
        
        text_lower = text.lower()
        for concern, keywords in concern_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                return concern
        
        return "general"
    
    def _generate_empathy_layer(self, emotional_keywords: List[str], main_concern: str) -> str:
        """Generate empathetic foundation for response"""
        empathy_templates = [
            "That sounds really difficult to experience.",
            "I can understand why you'd feel that way.",
            "It makes complete sense that you're experiencing this.",
            "Those feelings sound really overwhelming.",
            "I hear how much this is affecting you."
        ]
        
        if emotional_keywords:
            emotion = emotional_keywords[0]
            specific_empathy = f"Feeling {emotion} can be really tough to deal with."
            return specific_empathy
        
        return random.choice(empathy_templates)
    
    def _generate_validation_layer(self, user_message: str) -> str:
        """Generate validation for user's experience"""
        validation_templates = [
            "Your feelings are completely valid and understandable.",
            "It's important that you're acknowledging these feelings.",
            "Thank you for trusting me with something so personal.",
            "What you're experiencing is real and significant.",
            "It takes strength to recognize and share these feelings."
        ]
        
        return random.choice(validation_templates)
    
    def _generate_gentle_exploration(self, main_concern: str) -> str:
        """Generate gentle exploration questions"""
        exploration_templates = {
            "anxiety": "What tends to trigger these anxious feelings for you?",
            "depression": "How long have you been feeling this way?",
            "stress": "What's contributing most to your stress right now?",
            "social_anxiety": "What social situations feel most challenging?",
            "academic": "Which part of school feels most overwhelming?",
            "general": "What would be most helpful to talk about right now?"
        }
        
        return exploration_templates.get(main_concern, "Would you like to tell me more about what's been going on?")
    
    def _select_therapeutic_framework(self, user_message: str, context: ConversationContext) -> str:
        """Select appropriate therapeutic framework based on context"""
        
        # CBT for thought patterns and cognitive distortions
        if any(word in user_message.lower() for word in ["think", "thoughts", "believe", "assume"]):
            return "cbt_techniques"
        
        # DBT for emotional regulation and distress tolerance
        if any(word in user_message.lower() for word in ["overwhelmed", "intense", "can't handle"]):
            return "dbt_skills"
        
        # Mindfulness for present-moment awareness
        if any(word in user_message.lower() for word in ["racing", "mind", "can't focus", "scattered"]):
            return "mindfulness_practices"
        
        # ACT for values and behavior change
        if any(word in user_message.lower() for word in ["stuck", "meaningless", "direction", "purpose"]):
            return "act_principles"
        
        return "cbt_techniques"  # Default to CBT
    
    def _generate_cognitive_processing(self, user_message: str, framework: str) -> str:
        """Generate cognitive processing component based on therapeutic framework"""
        techniques = self.therapeutic_frameworks.get(framework, self.therapeutic_frameworks["cbt_techniques"])
        return random.choice(techniques)
    
    def _generate_action_oriented_support(self, user_message: str) -> str:
        """Generate action-oriented support suggestions"""
        main_concern = self._identify_main_concern(user_message)
        
        if main_concern in self.coping_strategies:
            strategy = random.choice(self.coping_strategies[main_concern])
            return f"Here's something that might help: {strategy}"
        
        general_support = [
            "Sometimes it helps to take things one moment at a time.",
            "Remember that it's okay to ask for help when you need it.",
            "You're showing real strength by talking about this.",
            "Small steps forward are still progress."
        ]
        
        return random.choice(general_support)
    
    def _assess_conversation_energy(self, user_message: str, context: ConversationContext) -> str:
        """Assess user's energy level in sustained conversations"""
        fatigue_indicators = ["tired", "exhausted", "can't", "done", "enough"]
        
        if any(indicator in user_message.lower() for indicator in fatigue_indicators):
            return "low"
        elif context.message_count > 25:
            return "medium"
        else:
            return "high"
    
    async def _suggest_conversation_break(self, context: ConversationContext) -> Dict[str, Any]:
        """Suggest a conversation break when energy is low"""
        break_suggestion = """
I can sense that this conversation has been a lot to process. That's completely normal and healthy - deep conversations can be emotionally taxing.

Would it be helpful to take a break for now? Sometimes stepping away and letting things settle can be really valuable. I'll be here whenever you're ready to continue, whether that's later today or another time.

Take care of yourself, and remember that everything we've talked about shows real insight and courage on your part. 💙
        """
        
        return {
            "response": break_suggestion.strip(),
            "confidence": 0.90,
            "source": "enhanced_conversation_service",
            "conversation_phase": "break_suggestion", 
            "therapeutic_elements": ["self_care", "boundary_setting", "encouragement"]
        }
    
    def _generate_insight_building_response(self, user_message: str, context: ConversationContext) -> str:
        """Generate insight-building responses for advanced conversations"""
        insight_builders = [
            "I'm noticing a pattern in what you've shared - have you seen this connection too?",
            "It sounds like you're developing some real self-awareness about this situation.",
            "What do you think has been most helpful in our conversation so far?",
            "How does talking about this feel different now compared to when we started?",
            "What insights are you taking away from this exploration?"
        ]
        
        return random.choice(insight_builders)
    
    def _acknowledge_therapeutic_progress(self, context: ConversationContext) -> str:
        """Acknowledge progress made during the conversation"""
        progress_acknowledgments = [
            "I can really see your growth in how you're processing these feelings.",
            "The way you're exploring these emotions shows real courage and maturity.",
            "You're developing some valuable insights about yourself through this conversation.",
            "I'm impressed by how thoughtfully you're approaching these challenges.",
            "The self-reflection you're doing is incredibly valuable for your wellbeing."
        ]
        
        return random.choice(progress_acknowledgments)
    
    async def _generate_closure_response(self, user_message: str, context: ConversationContext) -> Dict[str, Any]:
        """Generate conversation closure responses"""
        closure_response = random.choice(self.conversation_closures)
        
        return {
            "response": closure_response,
            "confidence": 0.95,
            "source": "enhanced_conversation_service",
            "conversation_phase": "conversation_closure",
            "therapeutic_elements": ["gratitude", "validation", "encouragement", "hope_instillation"]
        }
    
    async def _generate_medium_risk_response(self, user_message: str, context: ConversationContext) -> Dict[str, Any]:
        """Generate response for medium-risk situations"""
        
        concern = "I can hear that you're going through a really difficult time right now, and I want you to know that I'm here to support you."
        
        validation = "These intense feelings you're experiencing are valid, but they don't have to be permanent. Many people go through periods like this and find their way through."
        
        coping_support = "Let's focus on some things that might help you feel a bit more stable right now. Have you tried any coping strategies that have helped before?"
        
        resources = """
**Remember, support is available:**
• Crisis Text Line: Text HOME to 741741
• National Suicide Prevention Lifeline: 988
• Or reach out to someone you trust
        """
        
        hope_message = "I believe in your ability to get through this difficult time. You're stronger than you know."
        
        response_text = f"{concern} {validation} {coping_support}\n\n{resources}\n\n{hope_message}"
        
        return {
            "response": response_text,
            "confidence": 0.88,
            "source": "enhanced_conversation_service",
            "conversation_phase": "crisis_intervention",
            "risk_level": "medium",
            "therapeutic_elements": ["concern_expression", "validation", "coping_support", "hope_instillation"]
        }
    
    async def _generate_low_risk_response(self, user_message: str, context: ConversationContext) -> Dict[str, Any]:
        """Generate response for low-risk situations with enhanced support"""
        
    async def generate_response(self, user_message: str, context: ConversationContext, conversation_history: Optional[List[Dict]] = None) -> Dict[str, Any]:
        """
        Main interface for generating sophisticated therapeutic responses
        """
        try:
            # Determine conversation phase based on context
            conversation_phase = self._determine_conversation_phase(context, conversation_history or [])
            
            # Assess risk level
            risk_level = self._assess_risk_level(user_message, context)
            
            # Handle crisis situations immediately
            if risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]:
                return await self._generate_crisis_response(user_message, context, risk_level)
            
            # Generate layered response based on phase
            response_layers = self._generate_response_layers(user_message, context, conversation_phase)
            
            # Combine layers into cohesive response
            final_response = self._combine_response_layers(response_layers, conversation_phase, risk_level)
            
            return {
                "response": final_response,
                "content": final_response,  # For backward compatibility
                "conversation_phase": conversation_phase.value,
                "risk_level": risk_level.value,
                "therapeutic_elements": self._identify_therapeutic_elements(response_layers),
                "confidence": self._calculate_confidence(conversation_phase, risk_level),
                "source": "enhanced_conversation_service",
                "sentiment_score": self._calculate_response_sentiment(final_response),
                "next_phase_suggestions": self._suggest_next_phase(conversation_phase, risk_level)
            }
            
        except Exception as e:
            # Fallback to basic response
            return self._generate_fallback_response(user_message)

    def _determine_conversation_phase(self, context: ConversationContext, conversation_history: List[Dict]) -> ConversationPhase:
        """Determine the appropriate conversation phase based on context"""
        message_count = context.message_count
        
        if message_count <= 2:
            return ConversationPhase.INITIAL_CONTACT
        elif message_count <= 5:
            return ConversationPhase.EARLY_BUILDING
        elif message_count <= 10:
            return ConversationPhase.DEEPENING_ENGAGEMENT
        else:
            return ConversationPhase.SUSTAINED_CONVERSATION

    def _assess_risk_level(self, user_message: str, context: ConversationContext) -> RiskLevel:
        """Assess the risk level based on message content and context"""
        message_lower = user_message.lower()
        
        # Check for critical risk indicators
        critical_indicators = ["plan to die", "going to kill", "tonight is the night", "have a plan", "already decided"]
        if any(indicator in message_lower for indicator in critical_indicators):
            return RiskLevel.CRITICAL
        
        # Check for high risk indicators
        high_risk_indicators = ["suicide", "kill myself", "end it all", "better off dead", "want to die"]
        if any(indicator in message_lower for indicator in high_risk_indicators):
            return RiskLevel.HIGH
        
        # Check for medium risk indicators
        medium_risk_indicators = ["hopeless", "worthless", "trapped", "desperate", "can't take it"]
        if any(indicator in message_lower for indicator in medium_risk_indicators):
            return RiskLevel.MEDIUM
        
        return RiskLevel.LOW

    def _generate_response_layers(self, user_message: str, context: ConversationContext, phase: ConversationPhase) -> ResponseLayers:
        """Generate layered response components"""
        return ResponseLayers(
            empathy_foundation=self._generate_empathy_layer(self._extract_emotional_keywords(user_message), self._identify_main_concern(user_message)),
            cognitive_processing=self._generate_cognitive_layer(user_message, phase),
            action_oriented_support=self._generate_action_oriented_support(user_message),
            therapeutic_framework=self._select_therapeutic_framework(user_message, context, phase),
            safety_validation=self._generate_safety_validation(user_message, context)
        )

    def _combine_response_layers(self, layers: ResponseLayers, phase: ConversationPhase, risk_level: RiskLevel) -> str:
        """Combine response layers into a cohesive therapeutic response"""
        if risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]:
            return f"{layers.empathy_foundation} {layers.safety_validation}"
        
        if phase == ConversationPhase.INITIAL_CONTACT:
            return f"{layers.empathy_foundation} {layers.cognitive_processing}"
        elif phase in [ConversationPhase.EARLY_BUILDING, ConversationPhase.DEEPENING_ENGAGEMENT]:
            return f"{layers.empathy_foundation} {layers.cognitive_processing} {layers.therapeutic_framework}"
        else:
            return f"{layers.empathy_foundation} {layers.cognitive_processing} {layers.action_oriented_support} {layers.therapeutic_framework}"

    def _identify_therapeutic_elements(self, layers: ResponseLayers) -> List[str]:
        """Identify which therapeutic elements are present in the response"""
        elements = ["empathy"]
        if layers.cognitive_processing:
            elements.append("cognitive_processing")
        if layers.action_oriented_support:
            elements.append("action_support")
        if layers.therapeutic_framework:
            elements.append("evidence_based_techniques")
        if layers.safety_validation:
            elements.append("safety_validation")
        return elements

    def _calculate_confidence(self, phase: ConversationPhase, risk_level: RiskLevel) -> float:
        """Calculate confidence score for the response"""
        base_confidence = 0.85
        
        if risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]:
            return 0.95  # High confidence in crisis responses
        
        if phase == ConversationPhase.INITIAL_CONTACT:
            return 0.90  # High confidence in initial responses
        
        return base_confidence

    def _calculate_response_sentiment(self, response: str) -> float:
        """Calculate the sentiment score of the generated response"""
        # Simple positive sentiment calculation for therapeutic responses
        positive_words = ["support", "help", "understand", "care", "hope", "strength", "better", "together"]
        response_lower = response.lower()
        
        positive_count = sum(1 for word in positive_words if word in response_lower)
        return min(0.3 + (positive_count * 0.1), 0.8)  # Therapeutic responses should be mildly positive

    def _suggest_next_phase(self, current_phase: ConversationPhase, risk_level: RiskLevel) -> List[str]:
        """Suggest next conversation phases or actions"""
        if risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]:
            return ["crisis_support", "safety_planning", "professional_resources"]
        
        if current_phase == ConversationPhase.INITIAL_CONTACT:
            return ["explore_feelings", "build_rapport", "assess_needs"]
        elif current_phase == ConversationPhase.EARLY_BUILDING:
            return ["deepen_understanding", "introduce_techniques", "explore_patterns"]
        else:
            return ["maintain_support", "practice_techniques", "monitor_progress"]

    async def _generate_crisis_response(self, user_message: str, context: ConversationContext, risk_level: RiskLevel) -> Dict[str, Any]:
        """Generate specialized crisis intervention response"""
        if risk_level == RiskLevel.CRITICAL:
            response = self._generate_critical_risk_response(user_message, context)
        else:
            response = self._generate_high_risk_response(user_message, context)
        
        return {
            "response": response,
            "content": response,
            "conversation_phase": ConversationPhase.CRISIS_INTERVENTION.value,
            "risk_level": risk_level.value,
            "therapeutic_elements": ["crisis_intervention", "safety_validation", "resource_provision"],
            "confidence": 0.95,
            "source": "enhanced_conversation_service",
            "crisis_resources": self._get_crisis_resources(),
            "immediate_actions": ["safety_assessment", "professional_help", "crisis_hotline"]
        }

    def _get_crisis_resources(self) -> Dict[str, str]:
        """Get crisis intervention resources"""
        return {
            "crisis_line": "National Suicide Prevention Lifeline: 988",
            "text_line": "Crisis Text Line: Text HOME to 741741",
            "emergency": "If in immediate danger: 911",
            "chat_support": "Online chat: suicidepreventionlifeline.org"
        }

    def _generate_fallback_response(self, user_message: str) -> Dict[str, Any]:
        """Generate fallback response when enhanced service fails"""
        empathy = self._generate_empathy_layer(self._extract_emotional_keywords(user_message), self._identify_main_concern(user_message))
        validation = self._generate_validation_layer(user_message)
        
        enhanced_support = "While these feelings are challenging, there are definitely ways to work through them. You don't have to handle this all on your own."
        
        coping_suggestion = self._generate_action_oriented_support(user_message)
        
        response_text = f"{empathy} {validation} {enhanced_support} {coping_suggestion}"
        
        return {
            "response": response_text,
            "content": response_text,
            "confidence": 0.85,
            "source": "enhanced_conversation_service",
            "conversation_phase": "supportive_response",
            "risk_level": "low",
            "therapeutic_elements": ["empathy", "validation", "enhanced_support", "coping_guidance"]
        }

    def _generate_cognitive_layer(self, user_message: str, phase: ConversationPhase) -> str:
        """Generate cognitive processing layer based on conversation phase"""
        if phase == ConversationPhase.INITIAL_CONTACT:
            return "I want you to know that sharing these feelings takes courage, and I'm honored that you trust me with them."
        elif phase == ConversationPhase.EARLY_BUILDING:
            return "Let's explore what you're experiencing together. Sometimes understanding our feelings better can help us navigate them."
        else:
            return "It sounds like you're processing a lot right now. Let's work through this step by step."

    def _generate_safety_validation(self, user_message: str, context: ConversationContext) -> str:
        """Generate safety validation layer"""
        return "Your safety and wellbeing are my primary concerns. You matter, and your life has value."

    def _generate_critical_risk_response(self, user_message: str, context: ConversationContext) -> str:
        """Generate critical risk intervention response"""
        return """I'm extremely concerned about you right now. Your life has value and meaning, even when it doesn't feel that way. Please reach out for immediate help:

🚨 Call 911 if you're in immediate danger
📞 National Suicide Prevention Lifeline: 988 (available 24/7)
💬 Crisis Text Line: Text HOME to 741741
🌐 Online chat available at suicidepreventionlifeline.org

You don't have to go through this alone. These feelings can change with proper support."""

    async def _generate_low_risk_response(self, user_message: str, context: ConversationContext) -> Dict[str, Any]:
        """Generate supportive response for low-risk situations"""
        empathy = self._generate_empathy_layer(self._extract_emotional_keywords(user_message), self._identify_main_concern(user_message))
        validation = self._generate_validation_layer(user_message)
        
        enhanced_support = "While these feelings are challenging, there are definitely ways to work through them. You don't have to handle this all on your own."
        
        coping_suggestion = self._generate_action_oriented_support(user_message)
        
        response_text = f"{empathy} {validation} {enhanced_support} {coping_suggestion}"
        
        return {
            "response": response_text,
            "content": response_text,
            "confidence": 0.85,
            "source": "enhanced_conversation_service",
            "conversation_phase": "supportive_response",
            "risk_level": "low",
            "therapeutic_elements": ["empathy", "validation", "enhanced_support", "coping_guidance"]
        }

# Export the service
enhanced_conversation_service = EnhancedConversationService()