"""
Emotional Intelligence Engine for MindSpark AI
Provides real-time emotional analysis, response calibration, and contextual conversation enhancement
"""

from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
import re
import logging
from datetime import datetime, timedelta
import math

logger = logging.getLogger(__name__)

class EmotionalState(Enum):
    """Core emotional states for analysis"""
    JOYFUL = "joyful"
    ANXIOUS = "anxious"
    DEPRESSED = "depressed"
    ANGRY = "angry"
    CONFUSED = "confused"
    EXCITED = "excited"
    CALM = "calm"
    FRUSTRATED = "frustrated"
    HOPEFUL = "hopeful"
    OVERWHELMED = "overwhelmed"
    CONTENT = "content"
    LONELY = "lonely"
    CONFIDENT = "confident"
    INSECURE = "insecure"
    MOTIVATED = "motivated"

class EmotionalIntensity(Enum):
    """Emotional intensity levels"""
    SUBTLE = "subtle"
    MODERATE = "moderate"
    STRONG = "strong"
    INTENSE = "intense"
    OVERWHELMING = "overwhelming"

class ResponseTone(Enum):
    """Adaptive response tones based on emotional state"""
    GENTLE_SUPPORTIVE = "gentle_supportive"
    ENERGETIC_ENCOURAGING = "energetic_encouraging"
    CALM_GROUNDING = "calm_grounding"
    VALIDATING_EMPATHETIC = "validating_empathetic"
    PLAYFUL_UPLIFTING = "playful_uplifting"
    THOUGHTFUL_REFLECTIVE = "thoughtful_reflective"
    PRACTICAL_SOLUTION_FOCUSED = "practical_solution_focused"
    WARM_CONVERSATIONAL = "warm_conversational"

@dataclass
class EmotionalProfile:
    """Comprehensive emotional analysis of user state"""
    primary_emotion: EmotionalState
    secondary_emotions: List[EmotionalState] = field(default_factory=list)
    intensity: EmotionalIntensity = EmotionalIntensity.MODERATE
    emotional_trajectory: str = "stable"  # rising, falling, stable, volatile
    vulnerability_level: float = 0.5  # 0.0 to 1.0
    openness_to_support: float = 0.5  # 0.0 to 1.0
    energy_level: float = 0.5  # 0.0 to 1.0
    coherence_level: float = 0.8  # 0.0 to 1.0 (how clear/organized thoughts are)
    trust_indicators: List[str] = field(default_factory=list)
    resistance_indicators: List[str] = field(default_factory=list)

@dataclass
class EmotionalCalibration:
    """Response calibration based on emotional analysis"""
    recommended_tone: ResponseTone
    empathy_level: float  # 0.0 to 1.0
    validation_priority: float  # 0.0 to 1.0
    solution_focus: float  # 0.0 to 1.0
    emotional_mirroring: float  # 0.0 to 1.0
    conversational_pacing: str  # slow, moderate, energetic
    therapeutic_approach: str  # supportive, reflective, motivational, crisis
    response_length: str  # brief, moderate, detailed
    relationship_building_focus: float  # 0.0 to 1.0

@dataclass
class ConversationEmotionalContext:
    """Emotional context tracking for conversation"""
    session_emotional_arc: List[EmotionalState] = field(default_factory=list)
    emotional_patterns: Dict[str, float] = field(default_factory=dict)
    breakthrough_moments: List[str] = field(default_factory=list)
    emotional_needs_identified: List[str] = field(default_factory=list)
    trust_building_progress: float = 0.0
    emotional_safety_level: float = 0.5

class EmotionalIntelligenceEngine:
    """Real-time emotional intelligence and response calibration system"""
    
    def __init__(self):
        self.emotional_patterns = self._initialize_emotional_patterns()
        self.response_calibrations = self._initialize_response_calibrations()
        self.conversation_context = ConversationEmotionalContext()
        
    def _initialize_emotional_patterns(self) -> Dict[str, Dict[str, Any]]:
        """Initialize emotional pattern recognition rules"""
        return {
            # Language patterns for emotional state detection
            "joyful_patterns": {
                "keywords": ["happy", "excited", "wonderful", "amazing", "great", "fantastic", "love", "joy", "thrilled"],
                "phrases": ["feeling good", "so happy", "really excited", "going well", "love this"],
                "intensifiers": ["really", "so", "absolutely", "incredibly", "extremely"],
                "emotional_indicators": ["exclamation marks", "positive emojis", "energetic language"]
            },
            "anxious_patterns": {
                "keywords": ["worried", "anxious", "nervous", "scared", "afraid", "stress", "panic", "overwhelmed"],
                "phrases": ["can't stop thinking", "what if", "worried about", "so nervous", "freaking out"],
                "physical_symptoms": ["heart racing", "can't breathe", "shaking", "sweaty palms"],
                "temporal_indicators": ["future-focused concerns", "catastrophic thinking"]
            },
            "depressed_patterns": {
                "keywords": ["sad", "depressed", "down", "empty", "hopeless", "worthless", "numb", "tired"],
                "phrases": ["don't care", "what's the point", "nothing matters", "too tired", "can't do this"],
                "energy_indicators": ["no motivation", "everything is hard", "too much effort"],
                "cognitive_patterns": ["all or nothing", "negative self-talk", "hopelessness"]
            },
            "angry_patterns": {
                "keywords": ["angry", "mad", "furious", "hate", "annoyed", "frustrated", "irritated"],
                "phrases": ["so annoying", "can't stand", "makes me mad", "fed up", "had enough"],
                "intensity_markers": ["caps lock", "harsh language", "blame language"],
                "triggers": ["unfairness", "disrespect", "boundaries crossed"]
            },
            "confused_patterns": {
                "keywords": ["confused", "lost", "don't understand", "unclear", "mixed up", "uncertain"],
                "phrases": ["don't know", "not sure", "doesn't make sense", "so confusing"],
                "question_patterns": ["multiple questions", "seeking clarification", "self-doubt"],
                "cognitive_indicators": ["difficulty deciding", "contradictory statements"]
            }
        }
    
    def _initialize_response_calibrations(self) -> Dict[EmotionalState, EmotionalCalibration]:
        """Initialize response calibration templates for each emotional state"""
        return {
            EmotionalState.JOYFUL: EmotionalCalibration(
                recommended_tone=ResponseTone.PLAYFUL_UPLIFTING,
                empathy_level=0.7,
                validation_priority=0.8,
                solution_focus=0.3,
                emotional_mirroring=0.8,
                conversational_pacing="energetic",
                therapeutic_approach="supportive",
                response_length="moderate",
                relationship_building_focus=0.9
            ),
            EmotionalState.ANXIOUS: EmotionalCalibration(
                recommended_tone=ResponseTone.CALM_GROUNDING,
                empathy_level=0.9,
                validation_priority=0.9,
                solution_focus=0.6,
                emotional_mirroring=0.4,
                conversational_pacing="slow",
                therapeutic_approach="supportive",
                response_length="detailed",
                relationship_building_focus=0.8
            ),
            EmotionalState.DEPRESSED: EmotionalCalibration(
                recommended_tone=ResponseTone.GENTLE_SUPPORTIVE,
                empathy_level=0.9,
                validation_priority=1.0,
                solution_focus=0.2,
                emotional_mirroring=0.3,
                conversational_pacing="slow",
                therapeutic_approach="reflective",
                response_length="moderate",
                relationship_building_focus=0.9
            ),
            EmotionalState.ANGRY: EmotionalCalibration(
                recommended_tone=ResponseTone.VALIDATING_EMPATHETIC,
                empathy_level=0.8,
                validation_priority=1.0,
                solution_focus=0.4,
                emotional_mirroring=0.2,
                conversational_pacing="moderate",
                therapeutic_approach="reflective",
                response_length="moderate",
                relationship_building_focus=0.7
            ),
            EmotionalState.CONFUSED: EmotionalCalibration(
                recommended_tone=ResponseTone.THOUGHTFUL_REFLECTIVE,
                empathy_level=0.7,
                validation_priority=0.8,
                solution_focus=0.8,
                emotional_mirroring=0.5,
                conversational_pacing="moderate",
                therapeutic_approach="supportive",
                response_length="detailed",
                relationship_building_focus=0.6
            ),
            EmotionalState.OVERWHELMED: EmotionalCalibration(
                recommended_tone=ResponseTone.CALM_GROUNDING,
                empathy_level=0.9,
                validation_priority=1.0,
                solution_focus=0.7,
                emotional_mirroring=0.3,
                conversational_pacing="slow",
                therapeutic_approach="crisis",
                response_length="brief",
                relationship_building_focus=0.8
            ),
            EmotionalState.LONELY: EmotionalCalibration(
                recommended_tone=ResponseTone.WARM_CONVERSATIONAL,
                empathy_level=0.9,
                validation_priority=0.9,
                solution_focus=0.4,
                emotional_mirroring=0.6,
                conversational_pacing="moderate",
                therapeutic_approach="supportive",
                response_length="detailed",
                relationship_building_focus=1.0
            )
        }
    
    def analyze_emotional_state(self, message: str, conversation_history: Optional[List[str]] = None) -> EmotionalProfile:
        """Analyze user's emotional state from message and context"""
        if conversation_history is None:
            conversation_history = []
            
        # Detect primary emotions
        emotion_scores = self._calculate_emotion_scores(message)
        
        # Determine primary and secondary emotions
        sorted_emotions = sorted(emotion_scores.items(), key=lambda x: x[1], reverse=True)
        primary_emotion = EmotionalState(sorted_emotions[0][0]) if sorted_emotions else EmotionalState.CALM
        secondary_emotions = [EmotionalState(emotion) for emotion, score in sorted_emotions[1:3] if score > 0.3]
        
        # Assess emotional intensity
        intensity = self._assess_emotional_intensity(message, emotion_scores)
        
        # Analyze emotional trajectory from conversation history
        trajectory = self._analyze_emotional_trajectory(conversation_history + [message])
        
        # Calculate psychological metrics
        vulnerability_level = self._assess_vulnerability(message, primary_emotion)
        openness_to_support = self._assess_openness(message, conversation_history)
        energy_level = self._assess_energy_level(message)
        coherence_level = self._assess_coherence(message)
        
        # Identify trust and resistance indicators
        trust_indicators = self._identify_trust_indicators(message)
        resistance_indicators = self._identify_resistance_indicators(message)
        
        return EmotionalProfile(
            primary_emotion=primary_emotion,
            secondary_emotions=secondary_emotions,
            intensity=intensity,
            emotional_trajectory=trajectory,
            vulnerability_level=vulnerability_level,
            openness_to_support=openness_to_support,
            energy_level=energy_level,
            coherence_level=coherence_level,
            trust_indicators=trust_indicators,
            resistance_indicators=resistance_indicators
        )
    
    def _calculate_emotion_scores(self, message: str) -> Dict[str, float]:
        """Calculate emotional state scores based on language patterns"""
        message_lower = message.lower()
        scores = {}
        
        for emotion in EmotionalState:
            score = 0.0
            emotion_key = f"{emotion.value}_patterns"
            
            if emotion_key in self.emotional_patterns:
                patterns = self.emotional_patterns[emotion_key]
                
                # Keyword matching
                for keyword in patterns.get("keywords", []):
                    if keyword in message_lower:
                        score += 0.3
                
                # Phrase matching
                for phrase in patterns.get("phrases", []):
                    if phrase in message_lower:
                        score += 0.4
                
                # Special pattern matching
                if "exclamation marks" in patterns.get("emotional_indicators", []):
                    score += message.count("!") * 0.1
                
                # Intensifier boost
                for intensifier in patterns.get("intensifiers", []):
                    if intensifier in message_lower:
                        score *= 1.2
            
            scores[emotion.value] = min(score, 1.0)
        
        return scores
    
    def _assess_emotional_intensity(self, message: str, emotion_scores: Dict[str, float]) -> EmotionalIntensity:
        """Assess the intensity of emotional expression"""
        max_score = max(emotion_scores.values()) if emotion_scores else 0.0
        
        # Factor in linguistic intensity markers
        intensity_markers = {
            "caps": len([c for c in message if c.isupper()]) / len(message) if message else 0,
            "exclamations": message.count("!"),
            "repetition": self._detect_repetition(message),
            "extreme_words": self._count_extreme_words(message)
        }
        
        # Calculate combined intensity
        base_intensity = max_score
        linguistic_boost = sum(intensity_markers.values()) * 0.1
        total_intensity = base_intensity + linguistic_boost
        
        if total_intensity >= 0.8:
            return EmotionalIntensity.OVERWHELMING
        elif total_intensity >= 0.6:
            return EmotionalIntensity.INTENSE
        elif total_intensity >= 0.4:
            return EmotionalIntensity.STRONG
        elif total_intensity >= 0.2:
            return EmotionalIntensity.MODERATE
        else:
            return EmotionalIntensity.SUBTLE
    
    def _analyze_emotional_trajectory(self, conversation_history: List[str]) -> str:
        """Analyze emotional trajectory over conversation"""
        if len(conversation_history) < 2:
            return "stable"
        
        # Get emotion scores for recent messages
        recent_scores = []
        for message in conversation_history[-3:]:
            scores = self._calculate_emotion_scores(message)
            recent_scores.append(max(scores.values()) if scores else 0.0)
        
        # Analyze trend
        if len(recent_scores) >= 2:
            if recent_scores[-1] > recent_scores[-2] + 0.2:
                return "rising"
            elif recent_scores[-1] < recent_scores[-2] - 0.2:
                return "falling"
            elif max(recent_scores) - min(recent_scores) > 0.4:
                return "volatile"
        
        return "stable"
    
    def _assess_vulnerability(self, message: str, primary_emotion: EmotionalState) -> float:
        """Assess user's vulnerability level"""
        vulnerability_indicators = [
            "personal disclosure", "emotional openness", "seeking help",
            "admitting struggles", "sharing fears", "expressing uncertainty"
        ]
        
        base_vulnerability = {
            EmotionalState.DEPRESSED: 0.9,
            EmotionalState.ANXIOUS: 0.8,
            EmotionalState.OVERWHELMED: 0.9,
            EmotionalState.LONELY: 0.7,
            EmotionalState.CONFUSED: 0.6,
            EmotionalState.ANGRY: 0.5,
            EmotionalState.JOYFUL: 0.2
        }.get(primary_emotion, 0.5)
        
        # Adjust based on message content
        message_lower = message.lower()
        vulnerability_boost = 0.0
        
        if any(phrase in message_lower for phrase in ["i'm struggling", "i don't know", "help me", "scared"]):
            vulnerability_boost += 0.2
        
        if any(phrase in message_lower for phrase in ["never told anyone", "first time", "embarrassed"]):
            vulnerability_boost += 0.3
        
        return min(base_vulnerability + vulnerability_boost, 1.0)
    
    def _assess_openness(self, message: str, conversation_history: List[str]) -> float:
        """Assess openness to support and connection"""
        openness_indicators = [
            "asking questions", "sharing details", "responding to suggestions",
            "expressing gratitude", "showing interest"
        ]
        
        message_lower = message.lower()
        openness_score = 0.5  # baseline
        
        # Positive indicators
        if "?" in message:
            openness_score += 0.1
        if any(phrase in message_lower for phrase in ["thank you", "helps", "appreciate", "glad"]):
            openness_score += 0.2
        if len(message.split()) > 20:  # detailed sharing
            openness_score += 0.1
        
        # Negative indicators
        if any(phrase in message_lower for phrase in ["don't want", "won't help", "tried everything"]):
            openness_score -= 0.2
        if len(message.split()) < 5:  # very brief responses
            openness_score -= 0.1
        
        return max(0.0, min(1.0, openness_score))
    
    def _assess_energy_level(self, message: str) -> float:
        """Assess user's energy level from language patterns"""
        energy_indicators = {
            "high": ["excited", "energetic", "ready", "let's go", "pumped", "motivated"],
            "low": ["tired", "exhausted", "drained", "no energy", "can't", "too much"]
        }
        
        message_lower = message.lower()
        energy_score = 0.5  # baseline
        
        # High energy indicators
        for indicator in energy_indicators["high"]:
            if indicator in message_lower:
                energy_score += 0.2
        
        # Low energy indicators
        for indicator in energy_indicators["low"]:
            if indicator in message_lower:
                energy_score -= 0.2
        
        # Punctuation and capitalization as energy markers
        if message.count("!") > 1:
            energy_score += 0.1
        if len([c for c in message if c.isupper()]) / len(message) > 0.1:
            energy_score += 0.1
        
        return max(0.0, min(1.0, energy_score))
    
    def _assess_coherence(self, message: str) -> float:
        """Assess thought coherence and organization"""
        # Factors that indicate good coherence
        sentences = message.split(".")
        if len(sentences) > 1:
            coherence_score = 0.7  # multi-sentence shows organization
        else:
            coherence_score = 0.5
        
        # Logical connectors indicate coherence
        connectors = ["because", "so", "therefore", "however", "but", "and then", "first", "next"]
        for connector in connectors:
            if connector in message.lower():
                coherence_score += 0.1
        
        # Incoherence indicators
        if any(phrase in message.lower() for phrase in ["can't think", "all over the place", "confused"]):
            coherence_score -= 0.3
        
        return max(0.0, min(1.0, coherence_score))
    
    def _identify_trust_indicators(self, message: str) -> List[str]:
        """Identify indicators of trust and therapeutic alliance"""
        trust_indicators = []
        message_lower = message.lower()
        
        trust_patterns = {
            "personal_disclosure": ["i've never told", "personal", "private", "secret"],
            "vulnerability_sharing": ["embarrassed", "ashamed", "scared to say", "hard to admit"],
            "gratitude_expression": ["thank you", "appreciate", "helpful", "glad i talked"],
            "future_orientation": ["next time", "will try", "looking forward", "plan to"],
            "collaborative_language": ["we", "together", "help me", "work with"]
        }
        
        for category, patterns in trust_patterns.items():
            if any(pattern in message_lower for pattern in patterns):
                trust_indicators.append(category)
        
        return trust_indicators
    
    def _identify_resistance_indicators(self, message: str) -> List[str]:
        """Identify indicators of resistance or defensiveness"""
        resistance_indicators = []
        message_lower = message.lower()
        
        resistance_patterns = {
            "dismissive_language": ["whatever", "doesn't matter", "who cares", "pointless"],
            "defensive_responses": ["not my fault", "you don't understand", "easy for you to say"],
            "hopelessness": ["nothing works", "tried everything", "no point", "give up"],
            "avoidance": ["don't want to talk about", "change subject", "rather not say"],
            "minimizing": ["it's fine", "not a big deal", "i'm okay", "no problem"]
        }
        
        for category, patterns in resistance_patterns.items():
            if any(pattern in message_lower for pattern in patterns):
                resistance_indicators.append(category)
        
        return resistance_indicators
    
    def _detect_repetition(self, message: str) -> float:
        """Detect repetitive patterns that might indicate emotional intensity"""
        words = message.lower().split()
        if len(words) < 2:
            return 0.0
        
        # Check for repeated words
        word_counts = {}
        for word in words:
            word_counts[word] = word_counts.get(word, 0) + 1
        
        max_repetition = max(word_counts.values())
        return min((max_repetition - 1) * 0.2, 1.0)
    
    def _count_extreme_words(self, message: str) -> float:
        """Count extreme/absolute words that indicate emotional intensity"""
        extreme_words = [
            "never", "always", "completely", "totally", "absolutely", "extremely",
            "horrible", "terrible", "amazing", "incredible", "impossible", "perfect"
        ]
        
        message_lower = message.lower()
        count = sum(1 for word in extreme_words if word in message_lower)
        return min(count * 0.2, 1.0)
    
    def calibrate_response(self, emotional_profile: EmotionalProfile) -> EmotionalCalibration:
        """Generate response calibration based on emotional analysis"""
        base_calibration = self.response_calibrations.get(
            emotional_profile.primary_emotion,
            self.response_calibrations[EmotionalState.CALM]
        )
        
        # Create a copy to modify
        calibration = EmotionalCalibration(
            recommended_tone=base_calibration.recommended_tone,
            empathy_level=base_calibration.empathy_level,
            validation_priority=base_calibration.validation_priority,
            solution_focus=base_calibration.solution_focus,
            emotional_mirroring=base_calibration.emotional_mirroring,
            conversational_pacing=base_calibration.conversational_pacing,
            therapeutic_approach=base_calibration.therapeutic_approach,
            response_length=base_calibration.response_length,
            relationship_building_focus=base_calibration.relationship_building_focus
        )
        
        # Adjust based on intensity
        if emotional_profile.intensity == EmotionalIntensity.OVERWHELMING:
            calibration.empathy_level = min(1.0, calibration.empathy_level + 0.2)
            calibration.validation_priority = 1.0
            calibration.response_length = "brief"
            calibration.therapeutic_approach = "crisis"
        elif emotional_profile.intensity == EmotionalIntensity.SUBTLE:
            calibration.emotional_mirroring *= 0.7
            calibration.validation_priority *= 0.8
        
        # Adjust based on vulnerability
        if emotional_profile.vulnerability_level > 0.7:
            calibration.empathy_level = min(1.0, calibration.empathy_level + 0.1)
            calibration.relationship_building_focus = min(1.0, calibration.relationship_building_focus + 0.2)
        
        # Adjust based on openness
        if emotional_profile.openness_to_support < 0.4:
            calibration.solution_focus *= 0.5
            calibration.validation_priority = min(1.0, calibration.validation_priority + 0.2)
        
        # Adjust based on resistance indicators
        if emotional_profile.resistance_indicators:
            calibration.validation_priority = 1.0
            calibration.solution_focus *= 0.3
            calibration.empathy_level = min(1.0, calibration.empathy_level + 0.2)
        
        return calibration
    
    def generate_emotional_insights(self, emotional_profile: EmotionalProfile, calibration: EmotionalCalibration) -> Dict[str, Any]:
        """Generate comprehensive emotional insights for AI response generation"""
        return {
            "emotional_state_summary": {
                "primary_emotion": emotional_profile.primary_emotion.value,
                "intensity": emotional_profile.intensity.value,
                "trajectory": emotional_profile.emotional_trajectory,
                "vulnerability_level": emotional_profile.vulnerability_level
            },
            "response_guidance": {
                "recommended_tone": calibration.recommended_tone.value,
                "empathy_level": calibration.empathy_level,
                "validation_priority": calibration.validation_priority,
                "therapeutic_approach": calibration.therapeutic_approach,
                "pacing": calibration.conversational_pacing
            },
            "conversation_dynamics": {
                "trust_indicators": emotional_profile.trust_indicators,
                "resistance_indicators": emotional_profile.resistance_indicators,
                "openness_to_support": emotional_profile.openness_to_support,
                "relationship_building_focus": calibration.relationship_building_focus
            },
            "adaptive_recommendations": {
                "solution_focus": calibration.solution_focus,
                "emotional_mirroring": calibration.emotional_mirroring,
                "response_length": calibration.response_length,
                "energy_matching": emotional_profile.energy_level
            }
        }
    
    def update_conversation_context(self, emotional_profile: EmotionalProfile):
        """Update ongoing conversation emotional context"""
        # Track emotional arc
        self.conversation_context.session_emotional_arc.append(emotional_profile.primary_emotion)
        
        # Update emotional patterns
        emotion_key = emotional_profile.primary_emotion.value
        current_count = self.conversation_context.emotional_patterns.get(emotion_key, 0)
        self.conversation_context.emotional_patterns[emotion_key] = current_count + 1
        
        # Track trust building progress
        if emotional_profile.trust_indicators:
            self.conversation_context.trust_building_progress = min(
                1.0, self.conversation_context.trust_building_progress + 0.1
            )
        
        # Update emotional safety level
        if emotional_profile.vulnerability_level > 0.6 and not emotional_profile.resistance_indicators:
            self.conversation_context.emotional_safety_level = min(
                1.0, self.conversation_context.emotional_safety_level + 0.1
            )
        
        # Identify breakthrough moments
        if (emotional_profile.vulnerability_level > 0.7 and 
            emotional_profile.openness_to_support > 0.7 and
            not emotional_profile.resistance_indicators):
            timestamp = datetime.now().isoformat()
            self.conversation_context.breakthrough_moments.append(
                f"High vulnerability + openness at {timestamp}"
            )
        
        # Identify emotional needs
        needs_mapping = {
            EmotionalState.ANXIOUS: "reassurance and grounding",
            EmotionalState.DEPRESSED: "validation and gentle support",
            EmotionalState.ANGRY: "acknowledgment and understanding",
            EmotionalState.LONELY: "connection and companionship",
            EmotionalState.CONFUSED: "clarity and guidance",
            EmotionalState.OVERWHELMED: "simplification and calm"
        }
        
        if emotional_profile.primary_emotion in needs_mapping:
            need = needs_mapping[emotional_profile.primary_emotion]
            if need not in self.conversation_context.emotional_needs_identified:
                self.conversation_context.emotional_needs_identified.append(need)
    
    def get_conversation_emotional_summary(self) -> Dict[str, Any]:
        """Get comprehensive emotional summary of the conversation"""
        return {
            "emotional_arc": [emotion.value for emotion in self.conversation_context.session_emotional_arc],
            "emotional_patterns": self.conversation_context.emotional_patterns,
            "trust_building_progress": self.conversation_context.trust_building_progress,
            "emotional_safety_level": self.conversation_context.emotional_safety_level,
            "breakthrough_moments": self.conversation_context.breakthrough_moments,
            "identified_needs": self.conversation_context.emotional_needs_identified,
            "session_insights": self._generate_session_insights()
        }
    
    def _generate_session_insights(self) -> List[str]:
        """Generate insights about the emotional journey of the session"""
        insights = []
        
        # Emotional progression analysis
        if len(self.conversation_context.session_emotional_arc) > 2:
            recent_emotions = self.conversation_context.session_emotional_arc[-3:]
            if all(emotion in [EmotionalState.CALM, EmotionalState.HOPEFUL, EmotionalState.CONTENT] for emotion in recent_emotions[-2:]):
                insights.append("User showing emotional stabilization and positive progression")
        
        # Trust building analysis
        if self.conversation_context.trust_building_progress > 0.6:
            insights.append("Strong therapeutic alliance and trust established")
        
        # Emotional safety analysis
        if self.conversation_context.emotional_safety_level > 0.7:
            insights.append("High emotional safety - user feels comfortable sharing")
        
        # Pattern analysis
        most_common_emotion = max(
            self.conversation_context.emotional_patterns.items(),
            key=lambda x: x[1],
            default=(None, 0)
        )[0]
        
        if most_common_emotion and self.conversation_context.emotional_patterns[most_common_emotion] > 2:
            insights.append(f"Recurring emotional theme: {most_common_emotion}")
        
        return insights

# Global instance for use across the application
emotional_intelligence = EmotionalIntelligenceEngine()