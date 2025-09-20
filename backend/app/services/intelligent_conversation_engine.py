"""
Intelligent Dynamic Conversation System for MindSpark AI
Creates smart, contextual responses through real-time analysis rather than templates
"""

from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import re
import random
import asyncio
from enum import Enum
from dataclasses import dataclass
import json
try:
    from .emotional_intelligence_engine import emotional_intelligence, EmotionalProfile, EmotionalCalibration
except ImportError:
    # Fallback if emotional intelligence engine is not available
    emotional_intelligence = None
    EmotionalProfile = None
    EmotionalCalibration = None

class PersonalityMode(Enum):
    WITTY_COMPANION = "witty_companion"  # 35%
    EMPATHETIC_THERAPIST = "empathetic_therapist"  # 25% 
    MOTIVATIONAL_COACH = "motivational_coach"  # 15%
    EDUCATIONAL_MENTOR = "educational_mentor"  # 10%
    SOCIAL_NAVIGATOR = "social_navigator"  # 8%
    CREATIVE_COLLABORATOR = "creative_collaborator"  # 5%
    LIFE_PHILOSOPHY_GUIDE = "life_philosophy_guide"  # 2%

class EmotionalTone(Enum):
    PLAYFUL = "playful"
    SERIOUS = "serious"
    ENCOURAGING = "encouraging"
    COMPASSIONATE = "compassionate"
    CURIOUS = "curious"
    CELEBRATORY = "celebratory"
    PROTECTIVE = "protective"

class ConversationContext(Enum):
    GREETING = "greeting"
    ACADEMIC_STRESS = "academic_stress"
    SOCIAL_ISSUES = "social_issues"
    EMOTIONAL_SUPPORT = "emotional_support"
    CRISIS_INTERVENTION = "crisis_intervention"
    CELEBRATION = "celebration"
    CASUAL_CHAT = "casual_chat"
    GOAL_SETTING = "goal_setting"

@dataclass
class ConversationIntelligence:
    message_count: int
    emotional_trajectory: List[float]
    topic_evolution: List[str]
    relationship_depth: float
    crisis_indicators: List[str]
    positive_momentum: float
    user_preferences: Dict[str, float]
    therapeutic_progress: Dict[str, Any]

class IntelligentConversationEngine:
    def __init__(self):
        self.personality_weights = self._initialize_personality_weights()
        self.emotional_intelligence = self._initialize_emotional_intelligence()
        self.conversation_memory = {}
        self.response_patterns = self._initialize_response_patterns()
        self.adaptive_learning = self._initialize_adaptive_learning()
        
    def _initialize_adaptive_learning(self) -> Dict:
        """Initialize adaptive learning system"""
        return {
            "user_response_patterns": {},  # Track what types of responses users engage with
            "successful_personality_blends": {},  # Track which blends work best for different contexts
            "conversation_evolution_patterns": {},  # Track how conversations naturally evolve
            "emotional_journey_insights": {},  # Learn about typical emotional journeys
            "contextual_effectiveness": {},  # Track which approaches work best in different contexts
            "relationship_building_patterns": {}  # Learn optimal relationship development patterns
        }
        
    def _initialize_personality_weights(self) -> Dict[PersonalityMode, float]:
        """Initialize dynamic personality mode weights"""
        return {
            PersonalityMode.WITTY_COMPANION: 0.35,
            PersonalityMode.EMPATHETIC_THERAPIST: 0.25,
            PersonalityMode.MOTIVATIONAL_COACH: 0.15,
            PersonalityMode.EDUCATIONAL_MENTOR: 0.10,
            PersonalityMode.SOCIAL_NAVIGATOR: 0.08,
            PersonalityMode.CREATIVE_COLLABORATOR: 0.05,
            PersonalityMode.LIFE_PHILOSOPHY_GUIDE: 0.02
        }
    
    def _initialize_emotional_intelligence(self) -> Dict:
        """Initialize emotional intelligence parameters"""
        return {
            "empathy_sensitivity": 0.8,
            "humor_appropriateness": 0.7,
            "crisis_detection_threshold": 0.6,
            "emotional_mirroring": 0.6,
            "therapeutic_depth": 0.7
        }
    
    def _initialize_response_patterns(self) -> Dict:
        """Initialize intelligent response generation patterns"""
        return {
            "conversation_starters": {
                "empathetic": ["I can sense", "I hear", "It sounds like", "I notice"],
                "encouraging": ["You know what's amazing?", "I'm really impressed", "That takes courage"],
                "playful": ["Okay, so", "Let me guess", "Plot twist:", "Here's the thing"],
                "curious": ["I'm wondering", "What's interesting is", "Help me understand"]
            },
            "emotional_bridges": {
                "validation": ["That makes complete sense", "Your feelings are totally valid", "I get why you'd feel that way"],
                "reframing": ["Another way to look at this", "What if we considered", "I wonder if"],
                "encouragement": ["You've got this", "I believe in you", "You're stronger than you think"]
            },
            "conversation_deepeners": {
                "exploration": ["Tell me more about", "What's that like for you?", "How does that feel?"],
                "insight": ["What patterns do you notice?", "What would you tell a friend?", "What's your gut saying?"],
                "action": ["What feels doable?", "What's one small step?", "How can we move forward?"]
            }
        }

    async def generate_intelligent_response(self, user_message: str, conversation_history: List[Dict], user_context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Generate intelligent, contextual responses through real-time analysis
        """
        # Initialize default emotional intelligence values
        emotional_insights = {}
        emotional_summary = {}
        emotional_calibration = None
        emotional_profile = None
        
        # Use emotional intelligence if available
        if emotional_intelligence is not None:
            try:
                # Get conversation history messages for emotional analysis
                history_messages = [entry.get('content', '') for entry in conversation_history if entry.get('content')]
                
                # Analyze emotional state with emotional intelligence engine
                emotional_profile = emotional_intelligence.analyze_emotional_state(user_message, history_messages)
                emotional_calibration = emotional_intelligence.calibrate_response(emotional_profile)
                emotional_insights = emotional_intelligence.generate_emotional_insights(emotional_profile, emotional_calibration)
                
                # Update emotional conversation context
                emotional_intelligence.update_conversation_context(emotional_profile)
                emotional_summary = emotional_intelligence.get_conversation_emotional_summary()
            except Exception as e:
                print(f"Emotional intelligence error: {e}")
                # Continue without emotional intelligence
        
        # Analyze conversation intelligence
        intelligence = self._analyze_conversation_intelligence(user_message, conversation_history, user_context)
        
        # Determine optimal personality blend (enhanced with emotional calibration)
        personality_blend = self._calculate_personality_blend(user_message, intelligence, emotional_calibration)
        
        # Detect emotional tone and context (enhanced with emotional profile)
        emotional_tone = self._detect_emotional_tone(user_message, intelligence, emotional_profile)
        conversation_context = self._identify_conversation_context(user_message, intelligence)
        
        # Generate response components intelligently
        response_components = await self._generate_response_components(
            user_message, intelligence, personality_blend, emotional_tone, conversation_context, emotional_calibration
        )
        
        # Construct final intelligent response (enhanced with emotional calibration)
        final_response = self._construct_intelligent_response(response_components, personality_blend, emotional_tone, emotional_calibration)
        
        # Calculate response metadata
        confidence = self._calculate_response_confidence(intelligence, personality_blend)
        
        response_data = {
            "response": final_response,
            "content": final_response,
            "personality_blend": {mode.value: weight for mode, weight in personality_blend.items()},
            "emotional_tone": emotional_tone.value,
            "conversation_context": conversation_context.value,
            "confidence": confidence,
            "intelligence_analysis": {
                "relationship_depth": intelligence.relationship_depth,
                "emotional_trajectory": intelligence.emotional_trajectory[-3:] if intelligence.emotional_trajectory else [],
                "crisis_indicators": intelligence.crisis_indicators,
                "therapeutic_progress": intelligence.therapeutic_progress
            },
            "source": "intelligent_conversation_engine",
            "adaptive_insights": self._generate_adaptive_insights(intelligence, personality_blend, conversation_context)
        }
        
        # Add emotional intelligence data if available
        if emotional_insights:
            response_data["emotional_intelligence"] = emotional_insights
        if emotional_summary:
            response_data["conversation_emotional_summary"] = emotional_summary
            
        return response_data

    def _generate_adaptive_insights(self, intelligence: ConversationIntelligence, 
                                  personality_blend: Dict[PersonalityMode, float], 
                                  context: ConversationContext) -> Dict[str, Any]:
        """Generate adaptive learning insights for continuous improvement"""
        return {
            "recommended_follow_up": self._suggest_intelligent_follow_up(intelligence, personality_blend, context),
            "conversation_evolution_prediction": self._predict_conversation_evolution(intelligence),
            "optimal_personality_adjustment": self._suggest_personality_adjustments(intelligence, personality_blend),
            "engagement_optimization": self._analyze_engagement_potential(intelligence),
            "therapeutic_opportunity": self._identify_therapeutic_opportunities(intelligence)
        }

    def _suggest_intelligent_follow_up(self, intelligence: ConversationIntelligence, 
                                     personality_blend: Dict[PersonalityMode, float], 
                                     context: ConversationContext) -> List[str]:
        """Suggest intelligent follow-up approaches based on conversation analysis"""
        suggestions = []
        
        # Based on relationship depth
        if intelligence.relationship_depth < 0.3:
            suggestions.append("Focus on trust-building and creating psychological safety")
        elif intelligence.relationship_depth < 0.7:
            suggestions.append("Deepen engagement through personal exploration and validation")
        else:
            suggestions.append("Leverage established trust for meaningful therapeutic work")
        
        # Based on emotional trajectory
        if len(intelligence.emotional_trajectory) >= 2:
            recent_trend = intelligence.emotional_trajectory[-1] - intelligence.emotional_trajectory[-2]
            if recent_trend > 0.1:
                suggestions.append("Capitalize on positive emotional momentum")
            elif recent_trend < -0.1:
                suggestions.append("Provide additional emotional support and stabilization")
        
        # Based on dominant personality mode
        dominant_mode = max(personality_blend.items(), key=lambda x: x[1])[0]
        if dominant_mode == PersonalityMode.CREATIVE_COLLABORATOR:
            suggestions.append("Encourage creative expression as emotional outlet")
        elif dominant_mode == PersonalityMode.LIFE_PHILOSOPHY_GUIDE:
            suggestions.append("Explore meaning-making and value clarification")
        elif dominant_mode == PersonalityMode.EDUCATIONAL_MENTOR:
            suggestions.append("Provide learning strategies and academic support")
        
        return suggestions[:3]  # Return top 3 suggestions

    def _predict_conversation_evolution(self, intelligence: ConversationIntelligence) -> Dict[str, float]:
        """Predict likely conversation evolution paths"""
        predictions = {
            "therapeutic_breakthrough": 0.2,
            "crisis_escalation": 0.1,
            "positive_momentum": 0.3,
            "relationship_deepening": 0.4,
            "topic_shift_likely": 0.3
        }
        
        # Adjust based on current state
        if intelligence.crisis_indicators:
            predictions["crisis_escalation"] = 0.7
            predictions["therapeutic_breakthrough"] = 0.2
        
        if intelligence.positive_momentum > 0.6:
            predictions["positive_momentum"] = 0.8
            predictions["relationship_deepening"] = 0.6
        
        if intelligence.relationship_depth > 0.7:
            predictions["therapeutic_breakthrough"] = 0.6
            predictions["relationship_deepening"] = 0.8
        
        if len(intelligence.topic_evolution) > 3:
            recent_topics = intelligence.topic_evolution[-3:]
            if len(set(recent_topics)) < 2:  # Topics are repetitive
                predictions["topic_shift_likely"] = 0.8
        
        return predictions

    def _suggest_personality_adjustments(self, intelligence: ConversationIntelligence, 
                                       current_blend: Dict[PersonalityMode, float]) -> Dict[str, str]:
        """Suggest adaptive personality adjustments for optimization"""
        suggestions = {}
        
        # If crisis indicators but not in therapeutic mode
        if intelligence.crisis_indicators and current_blend[PersonalityMode.EMPATHETIC_THERAPIST] < 0.5:
            suggestions["emergency_adjustment"] = "Increase empathetic therapist mode for crisis support"
        
        # If positive momentum but not leveraging motivational modes
        if intelligence.positive_momentum > 0.6 and current_blend[PersonalityMode.MOTIVATIONAL_COACH] < 0.2:
            suggestions["momentum_optimization"] = "Increase motivational coach to capitalize on positive energy"
        
        # If deep relationship but still heavily witty
        if intelligence.relationship_depth > 0.7 and current_blend[PersonalityMode.WITTY_COMPANION] > 0.4:
            suggestions["depth_adjustment"] = "Reduce witty companion, increase therapeutic depth"
        
        # If long conversation without philosophical exploration
        if intelligence.message_count > 15 and current_blend[PersonalityMode.LIFE_PHILOSOPHY_GUIDE] < 0.1:
            suggestions["depth_expansion"] = "Consider introducing philosophical exploration"
        
        return suggestions

    def _analyze_engagement_potential(self, intelligence: ConversationIntelligence) -> Dict[str, float]:
        """Analyze potential for different types of engagement"""
        potential = {
            "humor_receptivity": 0.5,
            "deep_sharing_readiness": 0.3,
            "learning_engagement": 0.4,
            "creative_expression": 0.3,
            "goal_setting_motivation": 0.4
        }
        
        # Adjust based on relationship depth
        depth_factor = intelligence.relationship_depth
        potential["deep_sharing_readiness"] = min(0.9, 0.2 + depth_factor * 0.8)
        potential["creative_expression"] = min(0.8, 0.2 + depth_factor * 0.6)
        
        # Adjust based on positive momentum
        momentum_factor = intelligence.positive_momentum
        potential["humor_receptivity"] = min(0.9, 0.3 + momentum_factor * 0.6)
        potential["goal_setting_motivation"] = min(0.8, 0.2 + momentum_factor * 0.6)
        
        # Adjust based on conversation length (comfort level)
        if intelligence.message_count > 5:
            potential["learning_engagement"] = min(0.8, potential["learning_engagement"] + 0.3)
        
        return potential

    def _identify_therapeutic_opportunities(self, intelligence: ConversationIntelligence) -> List[str]:
        """Identify specific therapeutic opportunities in the conversation"""
        opportunities = []
        
        # Based on emotional trajectory patterns
        if len(intelligence.emotional_trajectory) >= 3:
            recent_emotions = intelligence.emotional_trajectory[-3:]
            if all(e < -0.3 for e in recent_emotions):
                opportunities.append("Cognitive restructuring for persistent negative thinking")
            elif max(recent_emotions) - min(recent_emotions) > 0.6:
                opportunities.append("Emotional regulation skills for mood volatility")
        
        # Based on relationship depth
        if intelligence.relationship_depth > 0.6:
            opportunities.append("Deeper therapeutic exploration and insight work")
            opportunities.append("Trauma-informed care if appropriate")
        
        # Based on positive momentum
        if intelligence.positive_momentum > 0.5:
            opportunities.append("Strength-based interventions and resilience building")
        
        # Based on conversation patterns
        if intelligence.message_count > 10:
            opportunities.append("Therapeutic relationship leveraging for behavior change")
        
        # Based on topic evolution
        if len(set(intelligence.topic_evolution)) > 3:
            opportunities.append("Pattern recognition and insight development")
        
        return opportunities[:4]  # Return top 4 opportunities

    def _analyze_conversation_intelligence(self, message: str, history: List[Dict], context: Optional[Dict] = None) -> ConversationIntelligence:
        """Analyze conversation for intelligent insights"""
        message_count = len(history) + 1
        
        # Analyze emotional trajectory
        emotional_trajectory = self._extract_emotional_trajectory(message, history)
        
        # Track topic evolution
        topic_evolution = self._analyze_topic_evolution(message, history)
        
        # Calculate relationship depth
        relationship_depth = self._calculate_relationship_depth(message, history)
        
        # Detect crisis indicators
        crisis_indicators = self._detect_crisis_indicators(message)
        
        # Measure positive momentum
        positive_momentum = self._calculate_positive_momentum(message, history)
        
        # Analyze user preferences
        user_preferences = self._analyze_user_preferences(message, history)
        
        # Track therapeutic progress
        therapeutic_progress = self._track_therapeutic_progress(message, history)
        
        return ConversationIntelligence(
            message_count=message_count,
            emotional_trajectory=emotional_trajectory,
            topic_evolution=topic_evolution,
            relationship_depth=relationship_depth,
            crisis_indicators=crisis_indicators,
            positive_momentum=positive_momentum,
            user_preferences=user_preferences,
            therapeutic_progress=therapeutic_progress
        )

    def _calculate_personality_blend(self, message: str, intelligence: ConversationIntelligence, emotional_calibration: Optional[Any] = None) -> Dict[PersonalityMode, float]:
        """Intelligently calculate personality mode blend based on context"""
        base_weights = self.personality_weights.copy()
        message_lower = message.lower()
        
        # Crisis indicators - prioritize therapeutic support
        if intelligence.crisis_indicators:
            base_weights[PersonalityMode.EMPATHETIC_THERAPIST] = 0.8
            base_weights[PersonalityMode.WITTY_COMPANION] = 0.1
            base_weights[PersonalityMode.MOTIVATIONAL_COACH] = 0.05
            base_weights[PersonalityMode.EDUCATIONAL_MENTOR] = 0.05
            for mode in [PersonalityMode.SOCIAL_NAVIGATOR, PersonalityMode.CREATIVE_COLLABORATOR, PersonalityMode.LIFE_PHILOSOPHY_GUIDE]:
                base_weights[mode] = 0.0
        
        # Celebration and high positive momentum - amplify joy
        elif intelligence.positive_momentum > 0.7 or any(word in message_lower for word in ['amazing', 'excited', 'celebrate', 'success', 'won', 'achieved', '🎉', '🎊', '🥳']):
            base_weights[PersonalityMode.WITTY_COMPANION] = 0.5
            base_weights[PersonalityMode.MOTIVATIONAL_COACH] = 0.3
            base_weights[PersonalityMode.EMPATHETIC_THERAPIST] = 0.2
        
        # Academic stress - educational focus with empathetic support
        elif any(keyword in message_lower for keyword in ['school', 'exam', 'test', 'homework', 'grade', 'study', 'college', 'university', 'assignment', 'project']):
            base_weights[PersonalityMode.EDUCATIONAL_MENTOR] = 0.4
            base_weights[PersonalityMode.MOTIVATIONAL_COACH] = 0.25
            base_weights[PersonalityMode.WITTY_COMPANION] = 0.2
            base_weights[PersonalityMode.EMPATHETIC_THERAPIST] = 0.15
        
        # Social relationships - social navigation with empathy
        elif any(keyword in message_lower for keyword in ['friend', 'relationship', 'social', 'lonely', 'connect', 'dating', 'crush', 'breakup', 'conflict']):
            base_weights[PersonalityMode.SOCIAL_NAVIGATOR] = 0.4
            base_weights[PersonalityMode.EMPATHETIC_THERAPIST] = 0.3
            base_weights[PersonalityMode.WITTY_COMPANION] = 0.3
        
        # Creative expression - creative collaboration focus
        elif any(keyword in message_lower for keyword in ['write', 'draw', 'create', 'art', 'music', 'poem', 'story', 'creative', 'imagine', 'inspiration']):
            base_weights[PersonalityMode.CREATIVE_COLLABORATOR] = 0.4
            base_weights[PersonalityMode.WITTY_COMPANION] = 0.3
            base_weights[PersonalityMode.EDUCATIONAL_MENTOR] = 0.2
            base_weights[PersonalityMode.EMPATHETIC_THERAPIST] = 0.1
        
        # Existential/philosophical questions - philosophy guide activation
        elif any(keyword in message_lower for keyword in ['meaning', 'purpose', 'why', 'existence', 'life', 'universe', 'spiritual', 'philosophy', 'point of', 'meaning of']):
            base_weights[PersonalityMode.LIFE_PHILOSOPHY_GUIDE] = 0.4
            base_weights[PersonalityMode.EMPATHETIC_THERAPIST] = 0.3
            base_weights[PersonalityMode.WITTY_COMPANION] = 0.2
            base_weights[PersonalityMode.EDUCATIONAL_MENTOR] = 0.1
        
        # Goal setting and motivation - motivational coach focus
        elif any(keyword in message_lower for keyword in ['goal', 'plan', 'want to', 'hope to', 'trying to', 'working on', 'motivation', 'achieve', 'improve']):
            base_weights[PersonalityMode.MOTIVATIONAL_COACH] = 0.4
            base_weights[PersonalityMode.WITTY_COMPANION] = 0.3
            base_weights[PersonalityMode.EDUCATIONAL_MENTOR] = 0.2
            base_weights[PersonalityMode.EMPATHETIC_THERAPIST] = 0.1
        
        # Emotional support needs - therapeutic with empathy
        elif any(keyword in message_lower for keyword in ['feel', 'emotion', 'sad', 'anxious', 'worried', 'stressed', 'overwhelmed', 'tired', 'exhausted']):
            base_weights[PersonalityMode.EMPATHETIC_THERAPIST] = 0.4
            base_weights[PersonalityMode.MOTIVATIONAL_COACH] = 0.25
            base_weights[PersonalityMode.WITTY_COMPANION] = 0.25
            base_weights[PersonalityMode.EDUCATIONAL_MENTOR] = 0.1
        
        # Relationship depth adjustment - deeper modes for longer conversations
        if intelligence.relationship_depth > 0.7:
            # Increase therapeutic and philosophical modes for deeper conversations
            base_weights[PersonalityMode.EMPATHETIC_THERAPIST] *= 1.2
            base_weights[PersonalityMode.LIFE_PHILOSOPHY_GUIDE] *= 1.5
            base_weights[PersonalityMode.WITTY_COMPANION] *= 0.8
        
        # Message count adjustment - evolve personality over conversation
        if intelligence.message_count > 10:
            # Long conversations - reduce witty companion, increase deeper modes
            base_weights[PersonalityMode.EMPATHETIC_THERAPIST] *= 1.1
            base_weights[PersonalityMode.MOTIVATIONAL_COACH] *= 1.1
            base_weights[PersonalityMode.WITTY_COMPANION] *= 0.9
        
        # Normalize weights to ensure they sum to 1
        total_weight = sum(base_weights.values())
        return {mode: weight/total_weight for mode, weight in base_weights.items()}

    def _detect_emotional_tone(self, message: str, intelligence: ConversationIntelligence, emotional_profile: Optional[Any] = None) -> EmotionalTone:
        """Intelligently detect appropriate emotional tone"""
        message_lower = message.lower()
        
        # Crisis tone
        if intelligence.crisis_indicators:
            return EmotionalTone.PROTECTIVE
        
        # Celebratory tone
        if any(word in message_lower for word in ['happy', 'excited', 'great', 'amazing', 'celebration', 'success']):
            return EmotionalTone.CELEBRATORY
        
        # Compassionate tone for emotional distress
        if any(word in message_lower for word in ['sad', 'hurt', 'pain', 'difficult', 'struggling', 'hard']):
            return EmotionalTone.COMPASSIONATE
        
        # Encouraging tone for challenges
        if any(word in message_lower for word in ['try', 'goal', 'want to', 'hope', 'wish', 'dream']):
            return EmotionalTone.ENCOURAGING
        
        # Curious tone for questions and exploration
        if '?' in message or any(word in message_lower for word in ['wonder', 'think', 'why', 'how', 'what']):
            return EmotionalTone.CURIOUS
        
        # Playful tone for casual conversation
        if intelligence.positive_momentum > 0.5 and not intelligence.crisis_indicators:
            return EmotionalTone.PLAYFUL
        
        # Default to serious for therapeutic conversations
        return EmotionalTone.SERIOUS

    def _identify_conversation_context(self, message: str, intelligence: ConversationIntelligence) -> ConversationContext:
        """Advanced context identification using semantic understanding"""
        message_lower = message.lower().strip()
        
        # Crisis context - highest priority
        if intelligence.crisis_indicators:
            return ConversationContext.CRISIS_INTERVENTION
        
        # Greeting context - handle greetings more intelligently
        greeting_words = ['hi', 'hello', 'hey', 'hie', 'good morning', 'good evening', 'what\'s up', 'sup', 'yo']
        if (intelligence.message_count <= 3 and 
            any(word in message_lower for word in greeting_words) and 
            len(message.strip()) < 20):
            return ConversationContext.GREETING
        
        # Work/professional stress context - expanded detection
        work_indicators = ['work', 'job', 'office', 'boss', 'coworker', 'colleague', 'meeting', 'deadline', 
                          'project', 'client', 'supervisor', 'manager', 'workplace', 'professional', 'career',
                          'interview', 'promotion', 'salary', 'overtime', 'corporate', 'business']
        stress_indicators = ['stressful', 'stress', 'fight', 'argument', 'conflict', 'difficult', 'problem',
                           'issue', 'trouble', 'challenging', 'overwhelming', 'frustrated', 'annoying',
                           'exhausted', 'tired', 'burnout']
        
        if (any(word in message_lower for word in work_indicators) or
            (any(word in message_lower for word in stress_indicators) and 
             any(word in message_lower for word in ['day', 'today', 'yesterday']))):
            return ConversationContext.EMOTIONAL_SUPPORT
        
        # Social/relationship context - enhanced detection
        social_indicators = ['friend', 'relationship', 'boyfriend', 'girlfriend', 'partner', 'dating', 'crush',
                           'family', 'parent', 'sibling', 'roommate', 'neighbor', 'social', 'party',
                           'hang out', 'hangout', 'text', 'call', 'chat', 'talk', 'conversation']
        
        if any(word in message_lower for word in social_indicators):
            return ConversationContext.SOCIAL_ISSUES
        
        # Academic context
        academic_indicators = ['school', 'exam', 'test', 'homework', 'grade', 'study', 'college', 'university',
                             'assignment', 'project', 'class', 'teacher', 'professor', 'student', 'semester']
        
        if any(word in message_lower for word in academic_indicators):
            return ConversationContext.ACADEMIC_STRESS
        
        # Emotional expression context - more nuanced detection
        emotion_indicators = ['feel', 'feeling', 'felt', 'emotion', 'mood', 'sad', 'happy', 'angry', 'mad',
                            'anxious', 'worried', 'nervous', 'excited', 'disappointed', 'frustrated',
                            'overwhelmed', 'confused', 'lost', 'stuck', 'hurt', 'pain', 'upset']
        
        if any(word in message_lower for word in emotion_indicators):
            return ConversationContext.EMOTIONAL_SUPPORT
        
        # Casual responses context - better detection
        casual_indicators = ['nothing much', 'not much', 'just', 'only', 'kinda', 'sort of', 'i guess',
                           'maybe', 'whatever', 'meh', 'okay', 'fine', 'alright']
        
        short_responses = ['yeah', 'yes', 'no', 'nah', 'sure', 'ok', 'k', 'hmm', 'oh', 'ah', 'um']
        
        if (len(message.strip()) < 30 and 
            (any(phrase in message_lower for phrase in casual_indicators) or
             any(word == message_lower.strip() for word in short_responses) or
             message.strip().count(' ') < 4)):
            return ConversationContext.CASUAL_CHAT
        
        # Question context - handle questions intelligently
        if '?' in message and len(message.strip()) < 100:
            return ConversationContext.CASUAL_CHAT
        
        # Goal/aspiration context
        goal_indicators = ['want to', 'trying to', 'working on', 'goal', 'plan', 'hope', 'wish', 'dream',
                         'aspire', 'achieve', 'accomplish', 'improve', 'better', 'change', 'start']
        
        if any(phrase in message_lower for phrase in goal_indicators):
            return ConversationContext.GOAL_SETTING
        
        # Celebration context
        positive_indicators = ['great', 'amazing', 'awesome', 'fantastic', 'wonderful', 'excellent',
                             'good news', 'success', 'win', 'won', 'passed', 'got', 'achieved']
        
        if any(phrase in message_lower for phrase in positive_indicators):
            return ConversationContext.CELEBRATION
        
        # Default to casual chat - but make it intelligent
        return ConversationContext.CASUAL_CHAT

    async def _generate_response_components(self, message: str, intelligence: ConversationIntelligence, 
                                          personality_blend: Dict[PersonalityMode, float], 
                                          emotional_tone: EmotionalTone, 
                                          context: ConversationContext,
                                          emotional_calibration: Optional[Any] = None) -> Dict[str, str]:
        """Generate intelligent response components"""
        
        # Generate opening/connection
        opening = self._generate_intelligent_opening(message, personality_blend, emotional_tone, context)
        
        # Generate core response
        core_response = self._generate_intelligent_core(message, intelligence, personality_blend, context)
        
        # Generate supportive elements
        support = self._generate_intelligent_support(message, intelligence, emotional_tone, context)
        
        # Generate forward momentum
        forward_momentum = self._generate_intelligent_momentum(message, intelligence, personality_blend, context)
        
        return {
            "opening": opening,
            "core_response": core_response,
            "support": support,
            "forward_momentum": forward_momentum
        }

    def _generate_intelligent_opening(self, message: str, personality_blend: Dict[PersonalityMode, float], 
                                    emotional_tone: EmotionalTone, context: ConversationContext) -> str:
        """Generate natural, context-aware openings that avoid repetitive phrases"""
        
        # Get dominant personality mode
        dominant_mode = max(personality_blend.items(), key=lambda x: x[1])[0]
        message_lower = message.lower().strip()
        
        # Crisis openings - always prioritize safety
        if context == ConversationContext.CRISIS_INTERVENTION:
            return "I can hear how much pain you're in right now, and I'm genuinely concerned about you."
        
        # Greeting context - don't use formal openings
        if context == ConversationContext.GREETING:
            return ""  # No opening needed for greetings
        
        # Casual chat context - minimal or no opening
        if context == ConversationContext.CASUAL_CHAT:
            if len(message.strip()) < 15:
                return ""  # Very casual, no formal opening
            return ""  # Let the core response handle it naturally
        
        # Work/emotional support context - natural acknowledgment
        if context == ConversationContext.EMOTIONAL_SUPPORT:
            if any(word in message_lower for word in ["work", "job", "stressful"]):
                return ""  # Let emotional core handle work stress naturally
            elif any(word in message_lower for word in ["fight", "argument"]):
                return ""  # Let the response be direct
            else:
                return ""  # Avoid generic therapeutic openings
        
        # Celebratory openings
        if context == ConversationContext.CELEBRATION:
            if dominant_mode == PersonalityMode.WITTY_COMPANION:
                return "YES! 🎉 I am absolutely here for this excitement!"
            else:
                return "I love hearing the joy in your message! This is wonderful news."
        
        # Academic stress openings
        if context == ConversationContext.ACADEMIC_STRESS:
            if dominant_mode == PersonalityMode.WITTY_COMPANION:
                return f"Ah, the eternal battle with {self._extract_academic_subject(message)}! I see what we're dealing with here."
            elif dominant_mode == PersonalityMode.EDUCATIONAL_MENTOR:
                return "I can sense the academic pressure you're feeling right now."
            else:
                return "School stress is really challenging, and what you're experiencing makes complete sense."
        
        # Social issue openings
        if context == ConversationContext.SOCIAL_ISSUES:
            if dominant_mode == PersonalityMode.WITTY_COMPANION:
                return "Ah, the beautiful complexity of human relationships strikes again!"
            elif dominant_mode == PersonalityMode.SOCIAL_NAVIGATOR:
                return "Relationship dynamics can be really tricky to navigate."
            else:
                return ""  # Let core response handle it naturally
        
        # For most contexts, skip formal openings and go straight to natural responses
        return ""

    def _generate_intelligent_core(self, message: str, intelligence: ConversationIntelligence, 
                                 personality_blend: Dict[PersonalityMode, float], context: ConversationContext) -> str:
        """Generate intelligent core response based on deep analysis"""
        
        # Crisis intervention core
        if context == ConversationContext.CRISIS_INTERVENTION:
            return self._generate_crisis_core_response(message, intelligence)
        
        # Greeting core - handle casual greetings naturally
        if context == ConversationContext.GREETING:
            return self._generate_greeting_core_response(message, intelligence, personality_blend)
        
        # Casual chat core - handle simple conversations naturally
        if context == ConversationContext.CASUAL_CHAT:
            return self._generate_casual_core_response(message, intelligence, personality_blend)
        
        # Academic stress core
        if context == ConversationContext.ACADEMIC_STRESS:
            return self._generate_academic_core_response(message, intelligence, personality_blend)
        
        # Social issues core
        if context == ConversationContext.SOCIAL_ISSUES:
            return self._generate_social_core_response(message, intelligence, personality_blend)
        
        # Emotional support core
        if context == ConversationContext.EMOTIONAL_SUPPORT:
            return self._generate_emotional_core_response(message, intelligence, personality_blend)
        
        # Celebration core
        if context == ConversationContext.CELEBRATION:
            return self._generate_celebration_core_response(message, intelligence, personality_blend)
        
        # Goal setting core
        if context == ConversationContext.GOAL_SETTING:
            return self._generate_goal_setting_core_response(message, intelligence, personality_blend)
        
        # Default casual core for unrecognized contexts
        return self._generate_casual_core_response(message, intelligence, personality_blend)

    def _generate_intelligent_support(self, message: str, intelligence: ConversationIntelligence, 
                                    emotional_tone: EmotionalTone, context: ConversationContext) -> str:
        """Generate intelligent supportive elements"""
        
        # Crisis support
        if context == ConversationContext.CRISIS_INTERVENTION:
            return "Your life has value and meaning, and there are people who want to help you through this."
        
        # Validation support
        if emotional_tone == EmotionalTone.COMPASSIONATE:
            return "Your feelings are completely valid, and it's okay to feel this way."
        
        # Encouragement support
        if emotional_tone == EmotionalTone.ENCOURAGING:
            return f"You've shown real {self._identify_strength_in_message(message)} in how you're handling this."
        
        # Playful support
        if emotional_tone == EmotionalTone.PLAYFUL:
            return "And honestly, the fact that you're reaching out shows you're already on the right track!"
        
        # Default supportive statement
        return "You don't have to navigate this alone."

    def _generate_intelligent_momentum(self, message: str, intelligence: ConversationIntelligence, 
                                     personality_blend: Dict[PersonalityMode, float], context: ConversationContext) -> str:
        """Generate intelligent forward momentum"""
        
        # Crisis momentum
        if context == ConversationContext.CRISIS_INTERVENTION:
            return "Right now, let's focus on your immediate safety. Are you somewhere safe?"
        
        # Exploratory momentum
        if intelligence.relationship_depth < 0.5:
            return f"Tell me more about {self._extract_key_topic(message)} - I'd like to understand better."
        
        # Action-oriented momentum
        if context in [ConversationContext.ACADEMIC_STRESS, ConversationContext.GOAL_SETTING]:
            return "What feels like the most manageable first step from where you are right now?"
        
        # Reflective momentum
        if context == ConversationContext.EMOTIONAL_SUPPORT:
            return "What's your gut telling you about all of this?"
        
        # Celebratory momentum
        if context == ConversationContext.CELEBRATION:
            return "How does it feel to have this positive moment? I want to hear more!"
        
        # Default curious momentum
        return "What's most on your mind about this situation?"

    def _construct_intelligent_response(self, components: Dict[str, str], personality_blend: Dict[PersonalityMode, float], 
                                      emotional_tone: EmotionalTone, emotional_calibration: Optional[Any] = None) -> str:
        """Construct final intelligent response from components"""
        
        # Get response parts and filter out empty ones
        opening = components["opening"].strip()
        core_response = components["core_response"].strip()
        support = components["support"].strip()
        momentum = components["forward_momentum"].strip()
        
        # Helper function to join non-empty parts
        def join_parts(*parts):
            return " ".join(part for part in parts if part)
        
        # Construct based on emotional tone and personality
        if emotional_tone == EmotionalTone.PROTECTIVE:
            # Crisis response - clear and supportive
            return join_parts(opening, core_response, support, momentum)
        
        elif emotional_tone == EmotionalTone.PLAYFUL:
            # Playful response - conversational and engaging
            response_parts = [opening, core_response]
            if support and "honestly" not in support:
                response_parts.append(support)
            response_parts.append(momentum)
            return join_parts(*response_parts)
        
        elif emotional_tone == EmotionalTone.COMPASSIONATE:
            # Compassionate response - gentle and validating
            return join_parts(opening, support, core_response, momentum)
        
        else:
            # Standard response construction - core response is most important
            return join_parts(opening, core_response, momentum)

    # Helper methods for intelligent analysis
    def _extract_emotional_trajectory(self, message: str, history: List[Dict]) -> List[float]:
        """Extract emotional trajectory from conversation"""
        # Simple sentiment analysis - can be enhanced with AI models
        emotional_words = {
            'positive': ['happy', 'good', 'great', 'amazing', 'excited', 'love', 'wonderful'],
            'negative': ['sad', 'bad', 'terrible', 'awful', 'hate', 'horrible', 'depressed'],
            'neutral': ['okay', 'fine', 'alright', 'normal']
        }
        
        trajectory = []
        for msg in history[-5:]:  # Last 5 messages
            content = msg.get('content', '').lower()
            positive_count = sum(1 for word in emotional_words['positive'] if word in content)
            negative_count = sum(1 for word in emotional_words['negative'] if word in content)
            
            if positive_count > negative_count:
                trajectory.append(0.7)
            elif negative_count > positive_count:
                trajectory.append(-0.7)
            else:
                trajectory.append(0.0)
        
        # Add current message
        content = message.lower()
        positive_count = sum(1 for word in emotional_words['positive'] if word in content)
        negative_count = sum(1 for word in emotional_words['negative'] if word in content)
        
        if positive_count > negative_count:
            trajectory.append(0.7)
        elif negative_count > positive_count:
            trajectory.append(-0.7)
        else:
            trajectory.append(0.0)
        
        return trajectory

    def _analyze_topic_evolution(self, message: str, history: List[Dict]) -> List[str]:
        """Analyze how topics have evolved in conversation"""
        topics = []
        
        # Simple keyword-based topic detection
        topic_keywords = {
            'academic': ['school', 'exam', 'test', 'homework', 'study', 'grade'],
            'social': ['friend', 'relationship', 'social', 'date', 'party'],
            'emotional': ['feel', 'emotion', 'sad', 'happy', 'anxious', 'angry'],
            'family': ['family', 'parent', 'mom', 'dad', 'sibling'],
            'future': ['future', 'career', 'goal', 'plan', 'dream'],
            'health': ['health', 'sleep', 'tired', 'sick', 'energy']
        }
        
        for msg in history[-3:]:  # Last 3 messages
            content = msg.get('content', '').lower()
            for topic, keywords in topic_keywords.items():
                if any(keyword in content for keyword in keywords):
                    topics.append(topic)
                    break
            else:
                topics.append('general')
        
        # Add current message topic
        content = message.lower()
        for topic, keywords in topic_keywords.items():
            if any(keyword in content for keyword in keywords):
                topics.append(topic)
                break
        else:
            topics.append('general')
        
        return topics

    def _calculate_relationship_depth(self, message: str, history: List[Dict]) -> float:
        """Calculate relationship depth based on conversation patterns"""
        depth_indicators = {
            'surface': ['hi', 'hello', 'how are you', 'fine', 'okay', 'good'],
            'personal': ['feel', 'think', 'worried', 'scared', 'excited', 'hope'],
            'deep': ['never told anyone', 'scared to say', 'really personal', 'trust you', 'vulnerable']
        }
        
        total_messages = len(history) + 1
        deep_count = 0
        personal_count = 0
        
        all_messages = [msg.get('content', '') for msg in history] + [message]
        
        for content in all_messages:
            content_lower = content.lower()
            if any(phrase in content_lower for phrase in depth_indicators['deep']):
                deep_count += 3
            elif any(word in content_lower for word in depth_indicators['personal']):
                personal_count += 1
        
        # Calculate depth score
        depth_score = (deep_count + personal_count) / max(total_messages, 1)
        return min(depth_score / 2, 1.0)  # Normalize to 0-1

    def _detect_crisis_indicators(self, message: str) -> List[str]:
        """Detect crisis indicators in message"""
        crisis_patterns = [
            'want to die', 'kill myself', 'end it all', 'hurt myself', 'suicide',
            'better off dead', 'no point living', 'want to disappear', 'end the pain',
            'can\'t go on', 'give up on life', 'not worth living'
        ]
        
        message_lower = message.lower()
        detected = []
        
        for pattern in crisis_patterns:
            if pattern in message_lower:
                detected.append(pattern)
        
        return detected

    def _calculate_positive_momentum(self, message: str, history: List[Dict]) -> float:
        """Calculate positive momentum in conversation"""
        positive_indicators = ['good', 'better', 'improving', 'progress', 'hope', 'excited', 'happy', 'grateful']
        negative_indicators = ['worse', 'hopeless', 'giving up', 'can\'t', 'impossible', 'failed']
        
        recent_messages = [msg.get('content', '') for msg in history[-3:]] + [message]
        
        positive_count = 0
        negative_count = 0
        
        for content in recent_messages:
            content_lower = content.lower()
            positive_count += sum(1 for word in positive_indicators if word in content_lower)
            negative_count += sum(1 for word in negative_indicators if word in content_lower)
        
        if positive_count + negative_count == 0:
            return 0.5  # Neutral
        
        return positive_count / (positive_count + negative_count)

    def _analyze_user_preferences(self, message: str, history: List[Dict]) -> Dict[str, float]:
        """Analyze user preferences from conversation patterns"""
        preferences = {
            'humor': 0.5,
            'directness': 0.5,
            'emotional_depth': 0.5,
            'practical_advice': 0.5,
            'validation': 0.5
        }
        
        # Analyze response patterns - simplified for now
        all_content = ' '.join([msg.get('content', '') for msg in history] + [message]).lower()
        
        # Humor preference
        if any(word in all_content for word in ['lol', 'haha', 'funny', 'joke']):
            preferences['humor'] = 0.8
        
        # Directness preference
        if any(phrase in all_content for phrase in ['just tell me', 'straight up', 'directly']):
            preferences['directness'] = 0.8
        
        # Emotional depth preference
        if any(word in all_content for word in ['feel', 'emotion', 'heart', 'soul']):
            preferences['emotional_depth'] = 0.8
        
        return preferences

    def _track_therapeutic_progress(self, message: str, history: List[Dict]) -> Dict[str, Any]:
        """Track therapeutic progress indicators"""
        return {
            'self_awareness': self._measure_self_awareness(message, history),
            'coping_skill_usage': self._measure_coping_skills(message, history),
            'emotional_regulation': self._measure_emotional_regulation(message, history),
            'goal_progress': self._measure_goal_progress(message, history)
        }

    def _measure_self_awareness(self, message: str, history: List[Dict]) -> float:
        """Measure self-awareness indicators"""
        awareness_indicators = ['i notice', 'i realize', 'i understand', 'i see that', 'pattern', 'trigger']
        content = message.lower()
        return min(sum(1 for indicator in awareness_indicators if indicator in content) * 0.3, 1.0)

    def _measure_coping_skills(self, message: str, history: List[Dict]) -> float:
        """Measure coping skill usage"""
        coping_indicators = ['breathing', 'meditation', 'exercise', 'talk to friend', 'journaling', 'take a break']
        content = message.lower()
        return min(sum(1 for indicator in coping_indicators if indicator in content) * 0.4, 1.0)

    def _measure_emotional_regulation(self, message: str, history: List[Dict]) -> float:
        """Measure emotional regulation progress"""
        regulation_indicators = ['calm down', 'take a step back', 'pause', 'breathe', 'ground myself']
        content = message.lower()
        return min(sum(1 for indicator in regulation_indicators if indicator in content) * 0.4, 1.0)

    def _measure_goal_progress(self, message: str, history: List[Dict]) -> float:
        """Measure goal achievement progress"""
        progress_indicators = ['accomplished', 'achieved', 'made progress', 'getting better', 'improving']
        content = message.lower()
        return min(sum(1 for indicator in progress_indicators if indicator in content) * 0.4, 1.0)

    def _calculate_response_confidence(self, intelligence: ConversationIntelligence, personality_blend: Dict[PersonalityMode, float]) -> float:
        """Calculate confidence in response quality"""
        base_confidence = 0.85
        
        # Increase confidence for crisis situations (we know how to handle these)
        if intelligence.crisis_indicators:
            base_confidence = 0.95
        
        # Increase confidence for deeper relationships
        relationship_bonus = intelligence.relationship_depth * 0.1
        
        # Increase confidence for clear emotional patterns
        if len(intelligence.emotional_trajectory) > 3:
            pattern_clarity = 1 - (abs(sum(intelligence.emotional_trajectory)) / len(intelligence.emotional_trajectory))
            pattern_bonus = pattern_clarity * 0.05
        else:
            pattern_bonus = 0
        
        return min(base_confidence + relationship_bonus + pattern_bonus, 1.0)

    # Helper methods for response generation
    def _extract_academic_subject(self, message: str) -> str:
        """Extract academic subject from message"""
        subjects = ['math', 'science', 'english', 'history', 'biology', 'chemistry', 'physics', 'literature']
        message_lower = message.lower()
        for subject in subjects:
            if subject in message_lower:
                return subject
        return "academics"

    def _extract_primary_emotion(self, message: str) -> str:
        """Extract primary emotion from message"""
        emotions = {
            'anxiety': ['anxious', 'worried', 'nervous', 'scared'],
            'sadness': ['sad', 'depressed', 'down', 'blue'],
            'anger': ['angry', 'mad', 'frustrated', 'annoyed'],
            'joy': ['happy', 'excited', 'joyful', 'thrilled'],
            'confusion': ['confused', 'lost', 'unclear', 'mixed up']
        }
        
        message_lower = message.lower()
        for emotion, keywords in emotions.items():
            if any(keyword in message_lower for keyword in keywords):
                return emotion
        return "emotion"

    def _identify_strength_in_message(self, message: str) -> str:
        """Identify strength demonstrated in message"""
        strengths = {
            'courage': ['scared but', 'nervous but', 'afraid but', 'trying anyway'],
            'resilience': ['keep going', 'not giving up', 'still trying', 'bounce back'],
            'self-awareness': ['i notice', 'i realize', 'i see that', 'i understand'],
            'openness': ['sharing', 'telling you', 'being honest', 'opening up']
        }
        
        message_lower = message.lower()
        for strength, indicators in strengths.items():
            if any(indicator in message_lower for indicator in indicators):
                return strength
        return "strength"

    def _extract_key_topic(self, message: str) -> str:
        """Extract key topic for follow-up questions"""
        # Simple extraction - look for important nouns/topics
        important_topics = ['school', 'family', 'friends', 'relationship', 'work', 'health', 'feelings', 'future', 'goals']
        message_lower = message.lower()
        
        for topic in important_topics:
            if topic in message_lower:
                return topic
        
        # Fallback - return generic
        return "what you're going through"

    # Specialized response generators
    def _generate_crisis_core_response(self, message: str, intelligence: ConversationIntelligence) -> str:
        """Generate crisis-specific core response"""
        severity_level = len(intelligence.crisis_indicators)
        
        if severity_level >= 3:
            return "What you're feeling is incredibly difficult, but these intense feelings can change with proper support. You don't have to face this alone."
        elif severity_level >= 2:
            return "These feelings you're experiencing are really heavy, and I want you to know that there are people who can help you work through this."
        else:
            return "I'm concerned about you, and I want you to know that what you're feeling doesn't have to be permanent."

    def _generate_academic_core_response(self, message: str, intelligence: ConversationIntelligence, personality_blend: Dict[PersonalityMode, float]) -> str:
        """Generate academic stress core response"""
        dominant_mode = max(personality_blend.items(), key=lambda x: x[1])[0]
        
        if dominant_mode == PersonalityMode.WITTY_COMPANION:
            subject = self._extract_academic_subject(message)
            return f"{subject.title()} has a way of making even the smartest people feel like they're solving puzzles in a foreign language!"
        elif dominant_mode == PersonalityMode.EDUCATIONAL_MENTOR:
            return "Academic challenges can feel overwhelming, but they're also opportunities to develop problem-solving skills and resilience."
        else:
            return "School stress is incredibly common, and what you're experiencing is a normal response to academic pressure."

    def _generate_social_core_response(self, message: str, intelligence: ConversationIntelligence, personality_blend: Dict[PersonalityMode, float]) -> str:
        """Generate social issues core response"""
        dominant_mode = max(personality_blend.items(), key=lambda x: x[1])[0]
        
        if dominant_mode == PersonalityMode.WITTY_COMPANION:
            return "Human relationships are like trying to choreograph a dance where everyone's listening to different music!"
        elif dominant_mode == PersonalityMode.SOCIAL_NAVIGATOR:
            return "Social dynamics can be complex, and it sounds like you're navigating some challenging interpersonal territory."
        else:
            return "Relationship challenges can be really emotionally draining, and your feelings about this situation make complete sense."

    def _generate_emotional_core_response(self, message: str, intelligence: ConversationIntelligence, personality_blend: Dict[PersonalityMode, float]) -> str:
        """Generate empathetic and natural emotional support responses"""
        message_lower = message.lower().strip()
        dominant_mode = max(personality_blend.items(), key=lambda x: x[1])[0]
        
        # Work stress responses
        if any(word in message_lower for word in ["work", "job", "coworker", "boss", "office"]):
            if "stressful" in message_lower or "stress" in message_lower:
                return "Work stress can really take it out of you. What's been the most challenging part of your day?"
            elif "fight" in message_lower or "argument" in message_lower:
                return "Workplace conflicts are so draining! Those situations can really stick with you. What happened?"
            else:
                return "Work stuff can be really tough to deal with. What's going on?"
        
        # General stress and overwhelm
        if any(word in message_lower for word in ["stressed", "overwhelmed", "exhausted", "tired"]):
            return "That sounds really tough. When you're feeling like this, what usually helps you feel a bit better?"
        
        # Sadness and emotional pain
        if any(word in message_lower for word in ["sad", "hurt", "pain", "upset", "crying"]):
            return "I can hear that you're really hurting right now. Do you want to talk about what's been weighing on you?"
        
        # Anxiety and worry
        if any(word in message_lower for word in ["anxious", "worried", "nervous", "panic"]):
            return "Anxiety can feel so overwhelming. What's been on your mind that's causing these feelings?"
        
        # Anger and frustration
        if any(word in message_lower for word in ["angry", "mad", "frustrated", "annoyed", "pissed"]):
            return "It sounds like you're really frustrated about something. What's been getting under your skin?"
        
        # Confusion and feeling lost
        if any(word in message_lower for word in ["confused", "lost", "stuck", "don't know"]):
            return "Feeling uncertain can be really uncomfortable. What's been on your mind that's got you feeling this way?"
        
        # Relationship issues
        if any(word in message_lower for word in ["relationship", "boyfriend", "girlfriend", "friend", "family"]):
            return "Relationship stuff can be so complex and emotionally draining. What's been happening?"
        
        # General emotional expression
        if any(word in message_lower for word in ["feel", "feeling", "emotion"]):
            return "Thanks for sharing how you're feeling. It takes courage to open up. What's been going through your mind?"
        
        # Default empathetic response based on extracted emotion
        emotion = self._extract_primary_emotion(message)
        if emotion == "anxiety":
            return "Anxiety has this way of making everything feel urgent and overwhelming, but we can work together to help you feel more grounded."
        elif emotion == "sadness":
            return "Sadness can feel so heavy and all-encompassing. It's okay to sit with these feelings while also taking care of yourself."
        elif emotion == "anger":
            return "That frustration is completely understandable - anger often shows us what we care about and what matters to us."
        else:
            return "It sounds like you're going through something difficult. I'm here to listen - what's been on your mind?"

    def _generate_celebration_core_response(self, message: str, intelligence: ConversationIntelligence, personality_blend: Dict[PersonalityMode, float]) -> str:
        """Generate celebration core response"""
        dominant_mode = max(personality_blend.items(), key=lambda x: x[1])[0]
        
        if dominant_mode == PersonalityMode.WITTY_COMPANION:
            return "This is the kind of news that makes my day! Success stories are my absolute favorite genre."
        elif dominant_mode == PersonalityMode.MOTIVATIONAL_COACH:
            return "This achievement is evidence of your capability and persistence - you made this happen!"
        else:
            return "I'm genuinely excited for you! These positive moments are so important to acknowledge and celebrate."

    def _generate_greeting_core_response(self, message: str, intelligence: ConversationIntelligence, personality_blend: Dict[PersonalityMode, float]) -> str:
        """Generate natural greeting response"""
        message_lower = message.lower().strip()
        dominant_mode = max(personality_blend.items(), key=lambda x: x[1])[0]
        
        # Handle specific greetings
        if "hey" in message_lower:
            if dominant_mode == PersonalityMode.WITTY_COMPANION:
                return "Hey there! What's on your mind today?"
            else:
                return "Hey! Good to see you here. How are you doing?"
        elif any(greeting in message_lower for greeting in ["hi", "hello"]):
            if dominant_mode == PersonalityMode.WITTY_COMPANION:
                return "Hello! Ready to dive into whatever's happening in your world?"
            else:
                return "Hi! I'm glad you're here. What would you like to talk about?"
        elif "good morning" in message_lower:
            return "Good morning! Hope you're starting your day well. What's going on?"
        elif "good evening" in message_lower:
            return "Good evening! How was your day?"
        else:
            # Generic greeting response
            return "Hi there! I'm MindSpark, and I'm here to chat about whatever's on your mind. What brings you here today?"

    def _generate_casual_core_response(self, message: str, intelligence: ConversationIntelligence, personality_blend: Dict[PersonalityMode, float]) -> str:
        """Generate intelligent casual conversation responses"""
        message_lower = message.lower().strip()
        dominant_mode = max(personality_blend.items(), key=lambda x: x[1])[0]
        
        # Handle "nothing much" responses with follow-up questions
        if any(phrase in message_lower for phrase in ["nothing much", "not much", "just chilling", "not a lot"]):
            follow_ups = [
                "Fair enough! Sometimes the quiet moments are nice. Anything on your mind though?",
                "Sounds peaceful! How's your day been overall?",
                "I hear you. Just one of those regular days?",
                "Got it. Anything you've been thinking about lately?"
            ]
            return random.choice(follow_ups)
        
        # Handle work-related stress
        if any(word in message_lower for word in ["work", "job", "stressful day"]):
            return "Ugh, work stress is the worst! What made today particularly rough?"
        
        # Handle fight/conflict mentions
        if any(word in message_lower for word in ["fight", "argument", "conflict"]):
            if "coworker" in message_lower or "colleague" in message_lower:
                return "Oh no, workplace conflicts are so draining! Want to talk about what the fight was about? Sometimes it helps to get it off your chest."
            elif "friend" in message_lower:
                return "Friend fights hit different - they're so emotionally exhausting. What happened?"
            else:
                return "Arguments are never fun. What was this one about?"
        
        # Handle specific casual questions
        if any(phrase in message_lower for phrase in ["what did i say", "what did i just say"]):
            return f"You said \"{message}\" - anything specific about that you want to talk through?"
        
        if any(phrase in message_lower for phrase in ["how are you", "how's it going", "what's up"]):
            responses = [
                "I'm doing well, thanks for asking! More importantly, how are YOU doing?",
                "I'm good! What's going on with you today?",
                "All good here! How's your day treating you?"
            ]
            return random.choice(responses)
        
        # Handle short responses (yeah, okay, sure, etc.)
        short_responses = ["yeah", "yes", "okay", "ok", "sure", "fine", "alright", "meh", "whatever"]
        if message_lower.strip() in short_responses:
            return "I'm sensing there might be more to that. Want to share what's really going on?"
        
        # Handle general casual conversation
        if len(message.strip()) < 20:
            if dominant_mode == PersonalityMode.WITTY_COMPANION:
                return "Hmm, you're being mysterious! What's brewing in that head of yours?"
            else:
                return "I'd love to hear more. What's on your mind?"
        
        # Handle questions
        if "?" in message:
            return "That's a good question! Let me think about that with you. What got you wondering about this?"
        
        # Default intelligent casual response
        responses = [
            "That's interesting! Tell me more about that.",
            "I'm curious to hear more about this. What's the story?",
            "Sounds like there's more to unpack here. Want to dive in?",
            "I'm listening. What else is going on with this?"
        ]
        return random.choice(responses)

    def _generate_goal_setting_core_response(self, message: str, intelligence: ConversationIntelligence, personality_blend: Dict[PersonalityMode, float]) -> str:
        """Generate goal setting core response"""
        dominant_mode = max(personality_blend.items(), key=lambda x: x[1])[0]
        
        if dominant_mode == PersonalityMode.MOTIVATIONAL_COACH:
            return "I love that you're thinking about goals! Having direction gives us purpose and momentum."
        elif dominant_mode == PersonalityMode.WITTY_COMPANION:
            return "Goal setting, huh! I like where your head's at - planning mode activated!"
        else:
            return "It's really great that you're thinking about what you want to work towards. Goals can be such powerful motivators."

    def generate_conversation_title(self, user_message: str, context: ConversationContext, conversation_history: Optional[List[Dict]] = None) -> str:
        """Generate intelligent, contextual conversation titles"""
        message_lower = user_message.lower().strip()
        
        # Handle different conversation contexts
        if context == ConversationContext.CRISIS_INTERVENTION:
            return "Crisis Support Session"
        
        elif context == ConversationContext.EMOTIONAL_SUPPORT:
            # Work-related emotional support
            if any(word in message_lower for word in ["work", "job", "coworker", "boss", "office"]):
                if any(word in message_lower for word in ["fight", "argument", "conflict"]):
                    return "Workplace Conflict Discussion"
                elif any(word in message_lower for word in ["stress", "stressful", "pressure", "overwhelmed"]):
                    return "Work Stress Support"
                elif any(word in message_lower for word in ["promotion", "interview", "meeting", "deadline"]):
                    return "Career Challenges Chat"
                else:
                    return "Work Life Discussion"
            
            # Relationship-related emotional support
            elif any(word in message_lower for word in ["relationship", "boyfriend", "girlfriend", "partner", "dating"]):
                if any(word in message_lower for word in ["fight", "argument", "breakup", "break up"]):
                    return "Relationship Troubles"
                else:
                    return "Relationship Discussion"
            
            elif any(word in message_lower for word in ["friend", "friendship"]):
                if any(word in message_lower for word in ["fight", "argument", "conflict"]):
                    return "Friend Conflict Support"
                else:
                    return "Friendship Chat"
            
            elif any(word in message_lower for word in ["family", "parent", "mom", "dad", "sibling"]):
                return "Family Matters Discussion"
            
            # Specific emotions
            elif any(word in message_lower for word in ["anxious", "anxiety", "worried", "panic"]):
                return "Anxiety Support Session"
            elif any(word in message_lower for word in ["sad", "depressed", "depression", "down"]):
                return "Mental Health Support"
            elif any(word in message_lower for word in ["angry", "mad", "frustrated", "annoyed"]):
                return "Managing Frustration"
            elif any(word in message_lower for word in ["lonely", "alone", "isolated"]):
                return "Loneliness Support"
            else:
                return "Emotional Support Chat"
        
        elif context == ConversationContext.ACADEMIC_STRESS:
            if any(word in message_lower for word in ["exam", "test", "quiz"]):
                return "Exam Stress Discussion"
            elif any(word in message_lower for word in ["homework", "assignment", "project"]):
                return "Academic Workload Chat"
            elif any(word in message_lower for word in ["grade", "grades", "gpa"]):
                return "Academic Performance Talk"
            else:
                return "School Stress Support"
        
        elif context == ConversationContext.SOCIAL_ISSUES:
            if any(word in message_lower for word in ["party", "social", "hang out", "hangout"]):
                return "Social Life Discussion"
            elif any(word in message_lower for word in ["dating", "crush", "like someone"]):
                return "Dating and Relationships"
            else:
                return "Social Challenges Chat"
        
        elif context == ConversationContext.GOAL_SETTING:
            if any(word in message_lower for word in ["career", "job", "professional"]):
                return "Career Goals Planning"
            elif any(word in message_lower for word in ["health", "fitness", "exercise"]):
                return "Health Goals Discussion"
            elif any(word in message_lower for word in ["study", "learn", "education"]):
                return "Learning Goals Chat"
            else:
                return "Personal Goals Session"
        
        elif context == ConversationContext.CELEBRATION:
            if any(word in message_lower for word in ["job", "work", "promotion", "hired"]):
                return "Career Success Celebration"
            elif any(word in message_lower for word in ["exam", "test", "grade", "passed"]):
                return "Academic Achievement"
            elif any(word in message_lower for word in ["relationship", "dating", "engagement"]):
                return "Relationship Milestone"
            else:
                return "Success Celebration"
        
        elif context == ConversationContext.GREETING:
            return "Getting to Know You"
        
        elif context == ConversationContext.CASUAL_CHAT:
            # Try to extract meaningful topic from casual conversation
            if any(word in message_lower for word in ["day", "today", "yesterday"]):
                return "Daily Life Chat"
            elif any(word in message_lower for word in ["weekend", "plans", "doing"]):
                return "Life Updates"
            elif "?" in user_message:
                return "Questions and Curiosity"
            elif any(word in message_lower for word in ["thinking", "wondering", "mind"]):
                return "Thoughts and Reflections"
            else:
                return "Casual Conversation"
        
        # Fallback: Create title from key meaningful words
        meaningful_words = []
        skip_words = {'i', 'me', 'my', 'am', 'is', 'are', 'was', 'were', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'the', 'a', 'an', 'and', 'or', 'but', 'so', 'if', 'when', 'where', 'why', 'how', 'what', 'who', 'that', 'this', 'these', 'those', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        
        words = user_message.split()[:8]  # First 8 words max
        for word in words:
            clean_word = re.sub(r'[^\w]', '', word.lower())
            if clean_word and clean_word not in skip_words and len(clean_word) > 2:
                meaningful_words.append(word.capitalize())
        
        if meaningful_words:
            title = " ".join(meaningful_words[:4])  # Max 4 meaningful words
            return title if len(title) <= 30 else title[:27] + "..."
        
        # Ultimate fallback
        return "Personal Chat Session"

# Export the intelligent engine
intelligent_conversation_engine = IntelligentConversationEngine()