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
        """Intelligently identify conversation context"""
        message_lower = message.lower().strip()
        
        # Crisis context - highest priority
        if intelligence.crisis_indicators:
            return ConversationContext.CRISIS_INTERVENTION
        
        # Greeting context - early in conversation with greeting words
        if intelligence.message_count <= 3 and any(word in message_lower for word in ['hi', 'hello', 'hey', 'good morning', 'good evening', 'what\'s up']):
            return ConversationContext.GREETING
        
        # Simple casual context - short messages, questions about previous conversation, basic responses
        if (len(message.strip()) < 15 or 
            any(phrase in message_lower for phrase in ['what did i say', 'what did i just say', 'how are you', 'nothing much', 'not much', 'just thinking']) or
            (message.strip().count(' ') < 3 and '?' in message)):
            return ConversationContext.CASUAL_CHAT
        
        # Academic stress context
        if any(word in message_lower for word in ['school', 'exam', 'test', 'homework', 'grade', 'study', 'college', 'university', 'assignment', 'project']):
            return ConversationContext.ACADEMIC_STRESS
        
        # Social issues context
        if any(word in message_lower for word in ['friend', 'relationship', 'social', 'lonely', 'connect', 'dating', 'breakup', 'crush']):
            return ConversationContext.SOCIAL_ISSUES
        
        # Celebration context
        if any(word in message_lower for word in ['happy', 'excited', 'great', 'amazing', 'celebration', 'success', 'achieved', 'won', 'passed']):
            return ConversationContext.CELEBRATION
        
        # Goal setting context
        if any(word in message_lower for word in ['goal', 'plan', 'want to', 'hope to', 'trying to', 'working on', 'motivation', 'achieve']):
            return ConversationContext.GOAL_SETTING
        
        # Emotional support context - only for explicit emotional language
        if any(word in message_lower for word in ['feel', 'feeling', 'emotion', 'sad', 'anxious', 'worried', 'stressed', 'overwhelmed', 'depressed', 'upset']):
            return ConversationContext.EMOTIONAL_SUPPORT
        
        # Default to casual chat for unrecognized patterns
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
        """Generate intelligent opening based on context and personality"""
        
        # Get dominant personality mode
        dominant_mode = max(personality_blend.items(), key=lambda x: x[1])[0]
        
        # Crisis openings - always prioritize safety
        if context == ConversationContext.CRISIS_INTERVENTION:
            return "I can hear how much pain you're in right now, and I'm genuinely concerned about you."
        
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
                return "I can hear how much this social situation is affecting you."
        
        # Emotional support openings
        if context == ConversationContext.EMOTIONAL_SUPPORT:
            if emotional_tone == EmotionalTone.COMPASSIONATE:
                return f"I can really sense the {self._extract_primary_emotion(message)} in what you're sharing."
            else:
                return "Thank you for trusting me with what you're feeling right now."
        
        # Default empathetic opening
        return "I appreciate you sharing this with me."

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
        
        # Get response parts
        opening = components["opening"]
        core_response = components["core_response"]
        support = components["support"]
        momentum = components["forward_momentum"]
        
        # Construct based on emotional tone and personality
        if emotional_tone == EmotionalTone.PROTECTIVE:
            # Crisis response - clear and supportive
            return f"{opening} {core_response} {support} {momentum}"
        
        elif emotional_tone == EmotionalTone.PLAYFUL:
            # Playful response - conversational and engaging
            response_parts = [opening, core_response]
            if support and "honestly" not in support:
                response_parts.append(support)
            response_parts.append(momentum)
            return " ".join(response_parts)
        
        elif emotional_tone == EmotionalTone.COMPASSIONATE:
            # Compassionate response - gentle and validating
            return f"{opening} {support} {core_response} {momentum}"
        
        else:
            # Standard response construction
            return f"{opening} {core_response} {momentum}"

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
        """Generate emotional support core response"""
        emotion = self._extract_primary_emotion(message)
        
        if emotion == "anxiety":
            return "Anxiety has this way of making everything feel urgent and overwhelming, but we can work together to help you feel more grounded."
        elif emotion == "sadness":
            return "Sadness can feel so heavy and all-encompassing. It's okay to sit with these feelings while also taking care of yourself."
        elif emotion == "anger":
            return "That frustration is completely understandable - anger often shows us what we care about and what matters to us."
        else:
            return "Emotions can be so complex and sometimes contradictory. What you're feeling is valid and important."

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
        """Generate natural casual conversation response"""
        message_lower = message.lower().strip()
        dominant_mode = max(personality_blend.items(), key=lambda x: x[1])[0]
        
        # Handle specific casual messages
        if any(phrase in message_lower for phrase in ["what did i say", "what did i just say", "what was that"]):
            return "You just said \"" + message + "\" - is there something specific about that you'd like to explore?"
        
        if any(phrase in message_lower for phrase in ["how are you", "how's it going", "what's up"]):
            if dominant_mode == PersonalityMode.WITTY_COMPANION:
                return "I'm doing great, thanks for asking! More importantly though, how are YOU doing?"
            else:
                return "I'm well, thank you! I'm curious to hear how you're doing today."
        
        if any(phrase in message_lower for phrase in ["nothing much", "not much", "just thinking", "just here"]):
            return "Sometimes the quiet moments are when our minds are actually the most active. Anything particular you're thinking about?"
        
        if "?" in message:
            # It's a question - be curious and helpful
            return "That's an interesting question! Let me think about that with you. What got you wondering about this?"
        
        # For very short messages or unclear context
        if len(message.strip()) < 10:
            if dominant_mode == PersonalityMode.WITTY_COMPANION:
                return "I'm picking up some mysterious vibes here! Want to fill me in on what's going through your head?"
            else:
                return "I'd love to hear more about what you're thinking. Can you tell me a bit more?"
        
        # Default casual response
        return "That's interesting! Tell me more about what's on your mind."

    def _generate_goal_setting_core_response(self, message: str, intelligence: ConversationIntelligence, personality_blend: Dict[PersonalityMode, float]) -> str:
        """Generate goal setting core response"""
        dominant_mode = max(personality_blend.items(), key=lambda x: x[1])[0]
        
        if dominant_mode == PersonalityMode.MOTIVATIONAL_COACH:
            return "I love that you're thinking about goals! Having direction gives us purpose and momentum."
        elif dominant_mode == PersonalityMode.WITTY_COMPANION:
            return "Goal setting, huh? I like where your head's at - planning mode activated!"
        else:
            return "It's really great that you're thinking about what you want to work towards. Goals can be such powerful motivators."

# Export the intelligent engine
intelligent_conversation_engine = IntelligentConversationEngine()