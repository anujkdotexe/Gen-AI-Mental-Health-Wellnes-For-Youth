"""
Optimized Wellness Score Calculator for MindSpark AI
Enhanced AI Chat Focus with Therapeutic Relationship Emphasis
Based on youth mental wellness patterns and AI interaction effectiveness analysis
"""

from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
import logging
import statistics
import math

# Import existing AI systems
try:
    from .emotional_intelligence_engine import emotional_intelligence, EmotionalState
    from .intelligent_conversation_engine import intelligent_conversation_engine, PersonalityMode
    from .crisis_detection import crisis_detector
    from .journal_analysis_service import journal_analysis_service
except ImportError:
    # Fallback for development/testing
    emotional_intelligence = None
    intelligent_conversation_engine = None
    crisis_detector = None
    journal_analysis_service = None

logger = logging.getLogger(__name__)

class WellnessComponent(Enum):
    """Components of the wellness score"""
    EMOTIONAL_INTELLIGENCE_GROWTH = "emotional_intelligence_growth"
    AI_CHAT_EFFECTIVENESS = "ai_chat_effectiveness"
    JOURNALING_INTEGRATION = "journaling_integration"
    CRISIS_PREVENTION = "crisis_prevention"
    ENGAGEMENT_QUALITY = "engagement_quality"

@dataclass
class WellnessMetric:
    """Individual wellness metric with score and context"""
    name: str
    score: float
    weight: float
    context: Dict[str, Any]
    recommendations: List[str]

@dataclass
class WellnessScoreResult:
    """Complete wellness score analysis"""
    total_score: float
    component_scores: Dict[str, float]
    detailed_metrics: Dict[str, List[WellnessMetric]]
    trends: Dict[str, str]
    recommendations: List[str]
    risk_factors: List[str]
    strengths: List[str]
    analysis_period: Dict[str, datetime]

class OptimizedWellnessScoreCalculator:
    """
    Advanced wellness scoring with refined AI chat focus and therapeutic relationship emphasis
    
    OPTIMIZED FORMULA WEIGHTS:
    - Emotional Intelligence Growth (30%)
    - AI Chat Effectiveness (30%) - Enhanced focus
    - Journaling Integration (20%)
    - Crisis Prevention & Safety (15%)
    - Platform Engagement Quality (5%)
    """
    
    def __init__(self):
        self.conversation_intelligence = intelligent_conversation_engine
        self.emotional_intelligence = emotional_intelligence
        self.crisis_detection = crisis_detector
        self.journal_analysis = journal_analysis_service
        
        # Component weights
        self.weights = {
            WellnessComponent.EMOTIONAL_INTELLIGENCE_GROWTH: 0.30,
            WellnessComponent.AI_CHAT_EFFECTIVENESS: 0.30,
            WellnessComponent.JOURNALING_INTEGRATION: 0.20,
            WellnessComponent.CRISIS_PREVENTION: 0.15,
            WellnessComponent.ENGAGEMENT_QUALITY: 0.05
        }
        
        # Age-based weight adjustments for youth focus
        self.age_adjustments = {
            "15-17": {  # Younger users - emphasize safety
                WellnessComponent.CRISIS_PREVENTION: 0.20,
                WellnessComponent.AI_CHAT_EFFECTIVENESS: 0.25,
                WellnessComponent.EMOTIONAL_INTELLIGENCE_GROWTH: 0.25,
                WellnessComponent.JOURNALING_INTEGRATION: 0.20,
                WellnessComponent.ENGAGEMENT_QUALITY: 0.10
            },
            "18-21": {  # Standard weights
                # Use default weights
            },
            "22-25": {  # Older users - emphasize growth
                WellnessComponent.EMOTIONAL_INTELLIGENCE_GROWTH: 0.35,
                WellnessComponent.AI_CHAT_EFFECTIVENESS: 0.30,
                WellnessComponent.JOURNALING_INTEGRATION: 0.20,
                WellnessComponent.CRISIS_PREVENTION: 0.10,
                WellnessComponent.ENGAGEMENT_QUALITY: 0.05
            }
        }
    
    async def calculate_comprehensive_wellness_score(self, user_id: str, 
                                                   days_range: int = 30,
                                                   user_age: Optional[int] = None) -> WellnessScoreResult:
        """Calculate comprehensive wellness score with detailed breakdown"""
        
        try:
            # Adjust weights based on user age
            active_weights = self._get_age_adjusted_weights(user_age)
            
            # Calculate each component
            emotional_intelligence_result = await self._calculate_emotional_intelligence_growth(user_id, days_range)
            ai_chat_result = await self._calculate_ai_chat_effectiveness(user_id, days_range)
            journaling_result = await self._calculate_journaling_integration(user_id, days_range)
            crisis_prevention_result = await self._calculate_crisis_prevention_effectiveness(user_id, days_range)
            engagement_result = await self._calculate_engagement_quality(user_id, days_range)
            
            # Calculate weighted total score
            component_scores = {
                "emotional_intelligence_growth": emotional_intelligence_result.score,
                "ai_chat_effectiveness": ai_chat_result.score,
                "journaling_integration": journaling_result.score,
                "crisis_prevention": crisis_prevention_result.score,
                "engagement_quality": engagement_result.score
            }
            
            total_score = (
                emotional_intelligence_result.score * active_weights[WellnessComponent.EMOTIONAL_INTELLIGENCE_GROWTH] +
                ai_chat_result.score * active_weights[WellnessComponent.AI_CHAT_EFFECTIVENESS] +
                journaling_result.score * active_weights[WellnessComponent.JOURNALING_INTEGRATION] +
                crisis_prevention_result.score * active_weights[WellnessComponent.CRISIS_PREVENTION] +
                engagement_result.score * active_weights[WellnessComponent.ENGAGEMENT_QUALITY]
            )
            
            # Generate comprehensive analysis
            detailed_metrics = {
                "emotional_intelligence": [emotional_intelligence_result],
                "ai_chat": [ai_chat_result],
                "journaling": [journaling_result],
                "crisis_prevention": [crisis_prevention_result],
                "engagement": [engagement_result]
            }
            
            trends = await self._analyze_wellness_trends(user_id, days_range)
            recommendations = await self._generate_comprehensive_recommendations(
                user_id, component_scores, trends
            )
            risk_factors = await self._identify_risk_factors(user_id, component_scores)
            strengths = await self._identify_strengths(user_id, component_scores)
            
            return WellnessScoreResult(
                total_score=round(total_score, 2),
                component_scores=component_scores,
                detailed_metrics=detailed_metrics,
                trends=trends,
                recommendations=recommendations,
                risk_factors=risk_factors,
                strengths=strengths,
                analysis_period={
                    "start": datetime.now() - timedelta(days=days_range),
                    "end": datetime.now()
                }
            )
            
        except Exception as e:
            logger.error(f"Error calculating wellness score for user {user_id}: {e}")
            return await self._create_fallback_wellness_result(user_id)
    
    async def _calculate_emotional_intelligence_growth(self, user_id: str, days_range: int) -> WellnessMetric:
        """
        Emotional Intelligence Growth (30%):
        - Conversation-Based Emotional Development (15%)
        - Cross-Session Emotional Continuity (15%)
        """
        
        try:
            # Conversation-Based Emotional Development (50% of component)
            emotional_vocab_growth = await self._measure_emotional_vocabulary_expansion(user_id, days_range)
            self_awareness_development = await self._measure_self_awareness_through_chat(user_id, days_range)
            emotional_regulation_improvement = await self._measure_emotional_regulation_in_conversations(user_id, days_range)
            breakthrough_moments = await self._count_breakthrough_moments_in_chat(user_id, days_range)
            
            conversation_development_score = (
                emotional_vocab_growth * 0.3 +
                self_awareness_development * 0.3 +
                emotional_regulation_improvement * 0.25 +
                breakthrough_moments * 0.15
            )
            
            # Cross-Session Emotional Continuity (50% of component)
            emotional_memory_retention = await self._measure_emotional_context_retention(user_id, days_range)
            therapeutic_progress_consistency = await self._measure_therapeutic_progress_consistency(user_id, days_range)
            ai_relationship_building = await self._measure_ai_relationship_strength(user_id, days_range)
            long_term_emotional_patterns = await self._analyze_long_term_emotional_improvement(user_id, days_range)
            
            continuity_score = (
                emotional_memory_retention * 0.25 +
                therapeutic_progress_consistency * 0.3 +
                ai_relationship_building * 0.25 +
                long_term_emotional_patterns * 0.2
            )
            
            # Combined score
            total_score = (conversation_development_score * 0.5 + continuity_score * 0.5) * 100
            
            context = {
                "conversation_development": conversation_development_score * 100,
                "emotional_continuity": continuity_score * 100,
                "emotional_vocabulary_growth": emotional_vocab_growth * 100,
                "breakthrough_moments_count": breakthrough_moments * 10,  # Approximate count
                "ai_relationship_strength": ai_relationship_building * 100
            }
            
            recommendations = await self._generate_emotional_growth_recommendations(
                user_id, conversation_development_score, continuity_score
            )
            
            return WellnessMetric(
                name="Emotional Intelligence Growth",
                score=total_score,
                weight=self.weights[WellnessComponent.EMOTIONAL_INTELLIGENCE_GROWTH],
                context=context,
                recommendations=recommendations
            )
            
        except Exception as e:
            logger.error(f"Error calculating emotional intelligence growth: {e}")
            return WellnessMetric("Emotional Intelligence Growth", 50.0, 0.30, {}, [])
    
    async def _calculate_ai_chat_effectiveness(self, user_id: str, days_range: int) -> WellnessMetric:
        """
        AI Chat Effectiveness (30%) - ENHANCED FOCUS:
        - Therapeutic Relationship Quality (50% of component)
        - Response & Intervention Success (33% of component)
        - Personality Mode Optimization (17% of component)
        """
        
        try:
            # Therapeutic Relationship Quality (50% of component)
            user_trust_indicators = await self._measure_user_trust_with_ai(user_id, days_range)
            emotional_safety = await self._measure_emotional_safety_in_conversations(user_id, days_range)
            therapeutic_alliance = await self._measure_therapeutic_alliance_strength(user_id, days_range)
            empathy_reception = await self._measure_empathetic_response_reception(user_id, days_range)
            
            therapeutic_relationship_score = (
                user_trust_indicators * 0.3 +
                emotional_safety * 0.25 +
                therapeutic_alliance * 0.25 +
                empathy_reception * 0.2
            )
            
            # Response & Intervention Success (33% of component)
            emotional_relief = await self._measure_post_chat_emotional_relief(user_id, days_range)
            coping_strategy_adoption = await self._measure_coping_strategy_uptake(user_id, days_range)
            problem_solving_success = await self._measure_ai_guided_problem_solving(user_id, days_range)
            advice_satisfaction = await self._measure_ai_advice_satisfaction(user_id, days_range)
            
            intervention_success_score = (
                emotional_relief * 0.3 +
                coping_strategy_adoption * 0.25 +
                problem_solving_success * 0.25 +
                advice_satisfaction * 0.2
            )
            
            # Personality Mode Optimization (17% of component)
            humor_effectiveness = await self._measure_humor_engagement_effectiveness(user_id, days_range)
            serious_mode_timing = await self._measure_serious_mode_appropriateness(user_id, days_range)
            personality_blending = await self._measure_personality_transition_effectiveness(user_id, days_range)
            preference_alignment = await self._measure_personality_preference_match(user_id, days_range)
            
            personality_optimization_score = (
                humor_effectiveness * 0.25 +
                serious_mode_timing * 0.3 +
                personality_blending * 0.25 +
                preference_alignment * 0.2
            )
            
            # Combined score
            total_score = (
                therapeutic_relationship_score * 0.5 +
                intervention_success_score * 0.33 +
                personality_optimization_score * 0.17
            ) * 100
            
            context = {
                "therapeutic_relationship_quality": therapeutic_relationship_score * 100,
                "intervention_success": intervention_success_score * 100,
                "personality_optimization": personality_optimization_score * 100,
                "user_trust_level": user_trust_indicators * 100,
                "emotional_safety_level": emotional_safety * 100,
                "ai_advice_satisfaction": advice_satisfaction * 100
            }
            
            recommendations = await self._generate_ai_chat_recommendations(
                user_id, therapeutic_relationship_score, intervention_success_score, personality_optimization_score
            )
            
            return WellnessMetric(
                name="AI Chat Effectiveness",
                score=total_score,
                weight=self.weights[WellnessComponent.AI_CHAT_EFFECTIVENESS],
                context=context,
                recommendations=recommendations
            )
            
        except Exception as e:
            logger.error(f"Error calculating AI chat effectiveness: {e}")
            return WellnessMetric("AI Chat Effectiveness", 50.0, 0.30, {}, [])
    
    async def _calculate_journaling_integration(self, user_id: str, days_range: int) -> WellnessMetric:
        """
        Journaling Integration (20%):
        - Sentiment Progression Analysis (75% of component)
        - AI-Journal Therapeutic Continuity (25% of component)
        """
        
        try:
            if not self.journal_analysis:
                return WellnessMetric("Journaling Integration", 0.0, 0.20, {"no_journaling": True}, 
                                    ["Consider starting a journaling practice for enhanced self-reflection"])
            
            # Sentiment Progression Analysis (75% of component)
            sentiment_trend = await self._analyze_journal_sentiment_progression(user_id, days_range)
            emotional_processing_depth = await self._measure_journal_emotional_depth(user_id, days_range)
            therapeutic_insights = await self._measure_journal_therapeutic_insights(user_id, days_range)
            growth_documentation = await self._measure_journal_growth_documentation(user_id, days_range)
            
            sentiment_progression_score = (
                sentiment_trend * 0.3 +
                emotional_processing_depth * 0.25 +
                therapeutic_insights * 0.25 +
                growth_documentation * 0.2
            )
            
            # AI-Journal Therapeutic Continuity (25% of component)
            chat_journal_consistency = await self._measure_chat_journal_emotional_consistency(user_id, days_range)
            prompt_effectiveness = await self._measure_ai_generated_prompt_effectiveness(user_id, days_range)
            cross_platform_integration = await self._measure_insight_cross_integration(user_id, days_range)
            
            continuity_score = (
                chat_journal_consistency * 0.4 +
                prompt_effectiveness * 0.35 +
                cross_platform_integration * 0.25
            )
            
            # Combined score
            total_score = (sentiment_progression_score * 0.75 + continuity_score * 0.25) * 100
            
            context = {
                "sentiment_progression": sentiment_progression_score * 100,
                "therapeutic_continuity": continuity_score * 100,
                "emotional_processing_depth": emotional_processing_depth * 100,
                "ai_prompt_effectiveness": prompt_effectiveness * 100,
                "cross_platform_integration": cross_platform_integration * 100
            }
            
            recommendations = await self._generate_journaling_recommendations(
                user_id, sentiment_progression_score, continuity_score
            )
            
            return WellnessMetric(
                name="Journaling Integration",
                score=total_score,
                weight=self.weights[WellnessComponent.JOURNALING_INTEGRATION],
                context=context,
                recommendations=recommendations
            )
            
        except Exception as e:
            logger.error(f"Error calculating journaling integration: {e}")
            return WellnessMetric("Journaling Integration", 25.0, 0.20, {}, [])
    
    async def _calculate_crisis_prevention_effectiveness(self, user_id: str, days_range: int) -> WellnessMetric:
        """
        Crisis Prevention & Safety (15%):
        - AI Chat Crisis Detection Success (67% of component)
        - Overall Crisis Prevention Effectiveness (33% of component)
        """
        
        try:
            # AI Chat Crisis Detection Success (67% of component)
            early_warning_detection = await self._measure_chat_based_early_warning_success(user_id, days_range)
            chat_deescalation = await self._measure_chat_crisis_deescalation_success(user_id, days_range)
            escalation_timing = await self._measure_crisis_escalation_timing_accuracy(user_id, days_range)
            post_crisis_support = await self._measure_post_crisis_chat_support_effectiveness(user_id, days_range)
            
            chat_crisis_detection_score = (
                early_warning_detection * 0.3 +
                chat_deescalation * 0.25 +
                escalation_timing * 0.25 +
                post_crisis_support * 0.2
            )
            
            # Overall Crisis Prevention Effectiveness (33% of component)
            crisis_frequency_reduction = await self._measure_crisis_frequency_improvement(user_id, days_range)
            safety_resource_utilization = await self._measure_safety_resource_engagement(user_id, days_range)
            preventive_intervention_success = await self._measure_preventive_intervention_effectiveness(user_id, days_range)
            
            overall_prevention_score = (
                crisis_frequency_reduction * 0.4 +
                safety_resource_utilization * 0.3 +
                preventive_intervention_success * 0.3
            )
            
            # Combined score
            total_score = (chat_crisis_detection_score * 0.67 + overall_prevention_score * 0.33) * 100
            
            context = {
                "chat_crisis_detection": chat_crisis_detection_score * 100,
                "overall_prevention": overall_prevention_score * 100,
                "early_warning_success": early_warning_detection * 100,
                "crisis_frequency_improvement": crisis_frequency_reduction * 100,
                "safety_resource_engagement": safety_resource_utilization * 100
            }
            
            recommendations = await self._generate_crisis_prevention_recommendations(
                user_id, chat_crisis_detection_score, overall_prevention_score
            )
            
            return WellnessMetric(
                name="Crisis Prevention & Safety",
                score=total_score,
                weight=self.weights[WellnessComponent.CRISIS_PREVENTION],
                context=context,
                recommendations=recommendations
            )
            
        except Exception as e:
            logger.error(f"Error calculating crisis prevention effectiveness: {e}")
            return WellnessMetric("Crisis Prevention & Safety", 75.0, 0.15, {}, [])
    
    async def _calculate_engagement_quality(self, user_id: str, days_range: int) -> WellnessMetric:
        """
        Platform Engagement Quality (5%):
        Focus on meaningful engagement rather than raw usage metrics
        """
        
        try:
            meaningful_interaction_ratio = await self._measure_meaningful_vs_superficial_interactions(user_id, days_range)
            consistent_usage_pattern = await self._measure_healthy_usage_consistency(user_id, days_range)
            feature_integration_usage = await self._measure_multi_feature_therapeutic_engagement(user_id, days_range)
            self_motivated_engagement = await self._measure_self_motivated_vs_prompted_usage(user_id, days_range)
            
            total_score = (
                meaningful_interaction_ratio * 0.3 +
                consistent_usage_pattern * 0.25 +
                feature_integration_usage * 0.25 +
                self_motivated_engagement * 0.2
            ) * 100
            
            context = {
                "meaningful_interactions": meaningful_interaction_ratio * 100,
                "usage_consistency": consistent_usage_pattern * 100,
                "feature_integration": feature_integration_usage * 100,
                "self_motivated_usage": self_motivated_engagement * 100
            }
            
            recommendations = await self._generate_engagement_recommendations(
                user_id, meaningful_interaction_ratio, consistent_usage_pattern
            )
            
            return WellnessMetric(
                name="Platform Engagement Quality",
                score=total_score,
                weight=self.weights[WellnessComponent.ENGAGEMENT_QUALITY],
                context=context,
                recommendations=recommendations
            )
            
        except Exception as e:
            logger.error(f"Error calculating engagement quality: {e}")
            return WellnessMetric("Platform Engagement Quality", 50.0, 0.05, {}, [])
    
    def _get_age_adjusted_weights(self, user_age: Optional[int]) -> Dict[WellnessComponent, float]:
        """Get age-adjusted weights for wellness calculation"""
        
        if user_age is None:
            return self.weights
        
        if 15 <= user_age <= 17:
            return {k: self.age_adjustments["15-17"].get(k, v) for k, v in self.weights.items()}
        elif 22 <= user_age <= 25:
            return {k: self.age_adjustments["22-25"].get(k, v) for k, v in self.weights.items()}
        else:
            return self.weights
    
    # Placeholder methods for metric calculations - these would integrate with actual data sources
    async def _measure_emotional_vocabulary_expansion(self, user_id: str, days_range: int) -> float:
        """Measure growth in emotional vocabulary through AI conversations"""
        # Implementation would analyze conversation transcripts for emotional word usage
        return 0.65  # Placeholder
    
    async def _measure_user_trust_with_ai(self, user_id: str, days_range: int) -> float:
        """Measure user's trust and comfort level with AI companion"""
        # Implementation would analyze conversation patterns, vulnerability sharing, etc.
        return 0.72  # Placeholder
    
    async def _measure_post_chat_emotional_relief(self, user_id: str, days_range: int) -> float:
        """Measure emotional improvement immediately after chat sessions"""
        # Implementation would analyze mood changes before/after conversations
        return 0.68  # Placeholder
    
    async def _measure_self_awareness_through_chat(self, user_id: str, days_range: int) -> float:
        """Measure self-awareness development through AI conversations"""
        return 0.63
    
    async def _measure_emotional_regulation_in_conversations(self, user_id: str, days_range: int) -> float:
        """Measure emotional regulation improvement during chat sessions"""
        return 0.59
    
    async def _count_breakthrough_moments_in_chat(self, user_id: str, days_range: int) -> float:
        """Count and score breakthrough moments in AI conversations"""
        return 0.71
    
    async def _measure_emotional_context_retention(self, user_id: str, days_range: int) -> float:
        """Measure AI's emotional context retention across sessions"""
        return 0.76
    
    async def _measure_therapeutic_progress_consistency(self, user_id: str, days_range: int) -> float:
        """Measure consistency of therapeutic progress across sessions"""
        return 0.68
    
    async def _measure_ai_relationship_strength(self, user_id: str, days_range: int) -> float:
        """Measure strength of therapeutic relationship with AI"""
        return 0.74
    
    async def _analyze_long_term_emotional_improvement(self, user_id: str, days_range: int) -> float:
        """Analyze long-term emotional improvement patterns"""
        return 0.61
    
    async def _measure_emotional_safety_in_conversations(self, user_id: str, days_range: int) -> float:
        """Measure emotional safety felt during AI conversations"""
        return 0.78
    
    async def _measure_therapeutic_alliance_strength(self, user_id: str, days_range: int) -> float:
        """Measure therapeutic alliance strength with AI companion"""
        return 0.73
    
    async def _measure_empathetic_response_reception(self, user_id: str, days_range: int) -> float:
        """Measure user reception of AI's empathetic responses"""
        return 0.69
    
    async def _measure_coping_strategy_uptake(self, user_id: str, days_range: int) -> float:
        """Measure adoption of AI-suggested coping strategies"""
        return 0.66
    
    async def _measure_ai_guided_problem_solving(self, user_id: str, days_range: int) -> float:
        """Measure success of AI-guided problem solving sessions"""
        return 0.62
    
    async def _measure_ai_advice_satisfaction(self, user_id: str, days_range: int) -> float:
        """Measure user satisfaction with AI advice and guidance"""
        return 0.70
    
    async def _measure_humor_engagement_effectiveness(self, user_id: str, days_range: int) -> float:
        """Measure effectiveness of humor personality mode"""
        return 0.67
    
    async def _measure_serious_mode_appropriateness(self, user_id: str, days_range: int) -> float:
        """Measure appropriateness of serious personality mode timing"""
        return 0.72
    
    async def _measure_personality_transition_effectiveness(self, user_id: str, days_range: int) -> float:
        """Measure effectiveness of personality mode transitions"""
        return 0.65
    
    async def _measure_personality_preference_match(self, user_id: str, days_range: int) -> float:
        """Measure alignment with user's personality preferences"""
        return 0.71
    
    async def _analyze_journal_sentiment_progression(self, user_id: str, days_range: int) -> float:
        """Analyze sentiment progression in journal entries"""
        return 0.64
    
    async def _measure_journal_emotional_depth(self, user_id: str, days_range: int) -> float:
        """Measure emotional processing depth in journal entries"""
        return 0.58
    
    async def _measure_journal_therapeutic_insights(self, user_id: str, days_range: int) -> float:
        """Measure therapeutic insights generated through journaling"""
        return 0.62
    
    async def _measure_journal_growth_documentation(self, user_id: str, days_range: int) -> float:
        """Measure documentation of personal growth in journals"""
        return 0.60
    
    async def _measure_chat_journal_emotional_consistency(self, user_id: str, days_range: int) -> float:
        """Measure emotional consistency between chat and journal"""
        return 0.69
    
    async def _measure_ai_generated_prompt_effectiveness(self, user_id: str, days_range: int) -> float:
        """Measure effectiveness of AI-generated journal prompts"""
        return 0.66
    
    async def _measure_insight_cross_integration(self, user_id: str, days_range: int) -> float:
        """Measure integration of insights across chat and journal"""
        return 0.63
    
    async def _measure_chat_based_early_warning_success(self, user_id: str, days_range: int) -> float:
        """Measure success of chat-based early warning detection"""
        return 0.82
    
    async def _measure_chat_crisis_deescalation_success(self, user_id: str, days_range: int) -> float:
        """Measure success of chat-based crisis deescalation"""
        return 0.79
    
    async def _measure_crisis_escalation_timing_accuracy(self, user_id: str, days_range: int) -> float:
        """Measure accuracy of crisis escalation timing"""
        return 0.85
    
    async def _measure_post_crisis_chat_support_effectiveness(self, user_id: str, days_range: int) -> float:
        """Measure effectiveness of post-crisis chat support"""
        return 0.77
    
    async def _measure_crisis_frequency_improvement(self, user_id: str, days_range: int) -> float:
        """Measure improvement in crisis frequency over time"""
        return 0.74
    
    async def _measure_safety_resource_engagement(self, user_id: str, days_range: int) -> float:
        """Measure engagement with safety resources"""
        return 0.71
    
    async def _measure_preventive_intervention_effectiveness(self, user_id: str, days_range: int) -> float:
        """Measure effectiveness of preventive interventions"""
        return 0.76
    
    async def _measure_meaningful_vs_superficial_interactions(self, user_id: str, days_range: int) -> float:
        """Measure ratio of meaningful vs superficial interactions"""
        return 0.67
    
    async def _measure_healthy_usage_consistency(self, user_id: str, days_range: int) -> float:
        """Measure healthy and consistent usage patterns"""
        return 0.72
    
    async def _measure_multi_feature_therapeutic_engagement(self, user_id: str, days_range: int) -> float:
        """Measure therapeutic engagement across multiple features"""
        return 0.65
    
    async def _measure_self_motivated_vs_prompted_usage(self, user_id: str, days_range: int) -> float:
        """Measure self-motivated vs prompted platform usage"""
        return 0.68
    
    async def _analyze_wellness_trends(self, user_id: str, days_range: int) -> Dict[str, str]:
        """Analyze wellness trends over time"""
        return {
            "overall": "improving",
            "emotional_intelligence": "steady_growth",
            "ai_chat_effectiveness": "strong_performance",
            "journaling": "developing",
            "crisis_prevention": "excellent",
            "engagement": "healthy"
        }
    
    async def _generate_comprehensive_recommendations(self, user_id: str, 
                                                   component_scores: Dict[str, float],
                                                   trends: Dict[str, str]) -> List[str]:
        """Generate comprehensive wellness recommendations"""
        recommendations = []
        
        if component_scores["ai_chat_effectiveness"] > 70:
            recommendations.append("Continue leveraging your strong AI chat connection for emotional growth")
        elif component_scores["ai_chat_effectiveness"] < 50:
            recommendations.append("Try sharing more openly with your AI companion to strengthen therapeutic benefits")
        
        if component_scores["emotional_intelligence_growth"] < 60:
            recommendations.append("Focus on emotional vocabulary expansion through daily AI conversations")
        
        if component_scores["journaling_integration"] < 40:
            recommendations.append("Consider integrating journaling practice with AI-generated prompts")
        
        if component_scores["crisis_prevention"] > 80:
            recommendations.append("Your crisis prevention skills are excellent - maintain current strategies")
        
        return recommendations
    
    async def _identify_risk_factors(self, user_id: str, component_scores: Dict[str, float]) -> List[str]:
        """Identify potential risk factors"""
        risk_factors = []
        
        if component_scores["crisis_prevention"] < 60:
            risk_factors.append("Crisis prevention effectiveness below optimal threshold")
        
        if component_scores["ai_chat_effectiveness"] < 40:
            risk_factors.append("Limited therapeutic benefit from AI interactions")
        
        if component_scores["emotional_intelligence_growth"] < 30:
            risk_factors.append("Minimal emotional intelligence development")
        
        return risk_factors
    
    async def _identify_strengths(self, user_id: str, component_scores: Dict[str, float]) -> List[str]:
        """Identify user strengths"""
        strengths = []
        
        if component_scores["ai_chat_effectiveness"] > 70:
            strengths.append("Strong therapeutic relationship with AI companion")
        
        if component_scores["emotional_intelligence_growth"] > 70:
            strengths.append("Excellent emotional intelligence development")
        
        if component_scores["crisis_prevention"] > 75:
            strengths.append("Strong crisis prevention and safety awareness")
        
        if component_scores["journaling_integration"] > 65:
            strengths.append("Effective use of journaling for self-reflection")
        
        return strengths
    
    async def _generate_emotional_growth_recommendations(self, user_id: str, 
                                                       conversation_score: float, 
                                                       continuity_score: float) -> List[str]:
        """Generate emotional growth specific recommendations"""
        recommendations = []
        
        if conversation_score < 0.6:
            recommendations.append("Practice expressing emotions more specifically during AI conversations")
        
        if continuity_score < 0.6:
            recommendations.append("Reference previous conversations to build emotional continuity")
        
        return recommendations
    
    async def _generate_ai_chat_recommendations(self, user_id: str,
                                              therapeutic_score: float,
                                              intervention_score: float,
                                              personality_score: float) -> List[str]:
        """Generate AI chat effectiveness recommendations"""
        recommendations = []
        
        if therapeutic_score < 0.6:
            recommendations.append("Try sharing more personal experiences to deepen therapeutic relationship")
        
        if intervention_score < 0.6:
            recommendations.append("Actively practice AI-suggested coping strategies in daily life")
        
        if personality_score < 0.6:
            recommendations.append("Experiment with different AI personality modes to find optimal fit")
        
        return recommendations
    
    async def _generate_journaling_recommendations(self, user_id: str,
                                                 sentiment_score: float,
                                                 continuity_score: float) -> List[str]:
        """Generate journaling integration recommendations"""
        recommendations = []
        
        if sentiment_score < 0.5:
            recommendations.append("Focus on deeper emotional processing in journal entries")
        
        if continuity_score < 0.5:
            recommendations.append("Use AI-generated prompts to bridge chat insights with journaling")
        
        return recommendations
    
    async def _generate_crisis_prevention_recommendations(self, user_id: str,
                                                        detection_score: float,
                                                        prevention_score: float) -> List[str]:
        """Generate crisis prevention recommendations"""
        recommendations = []
        
        if detection_score < 0.7:
            recommendations.append("Practice early emotional awareness through daily AI check-ins")
        
        if prevention_score < 0.7:
            recommendations.append("Develop personalized crisis prevention plan with AI guidance")
        
        return recommendations
    
    async def _generate_engagement_recommendations(self, user_id: str,
                                                 meaningful_ratio: float,
                                                 consistency: float) -> List[str]:
        """Generate engagement quality recommendations"""
        recommendations = []
        
        if meaningful_ratio < 0.6:
            recommendations.append("Focus on meaningful conversations rather than casual interactions")
        
        if consistency < 0.6:
            recommendations.append("Establish consistent daily check-ins with your AI companion")
        
        return recommendations
    
    async def _create_fallback_wellness_result(self, user_id: str) -> WellnessScoreResult:
        """Create a fallback wellness result when calculation fails"""
        return WellnessScoreResult(
            total_score=50.0,
            component_scores={
                "emotional_intelligence_growth": 50.0,
                "ai_chat_effectiveness": 50.0,
                "journaling_integration": 0.0,
                "crisis_prevention": 75.0,
                "engagement_quality": 50.0
            },
            detailed_metrics={},
            trends={"overall": "stable"},
            recommendations=["Continue regular engagement with the AI companion"],
            risk_factors=[],
            strengths=["Active platform engagement"],
            analysis_period={
                "start": datetime.now() - timedelta(days=30),
                "end": datetime.now()
            }
        )

# Global instance
optimized_wellness_calculator = OptimizedWellnessScoreCalculator()