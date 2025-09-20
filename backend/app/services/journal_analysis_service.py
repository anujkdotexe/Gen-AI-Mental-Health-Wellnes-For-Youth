"""
Privacy-preserving AI analysis service for journal entries
Integrates with existing emotional intelligence and conversation engines
"""

from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
import logging
import asyncio
import json

# Import existing AI systems
try:
    from .emotional_intelligence_engine import (
        emotional_intelligence, EmotionalState, ResponseTone,
        EmotionalProfile, ConversationEmotionalContext
    )
    from .intelligent_conversation_engine import (
        intelligent_conversation_engine, PersonalityMode
    )
    from .crisis_detection import crisis_detector
except ImportError:
    # Fallback for development/testing
    emotional_intelligence = None
    intelligent_conversation_engine = None
    crisis_detector = None

from .journaling_service import JournalAnalysis, JournalPrivacyLevel

logger = logging.getLogger(__name__)

@dataclass
class AnalysisContext:
    """Context for journal analysis"""
    user_id: str
    privacy_level: JournalPrivacyLevel
    content: str
    entry_metadata: Dict[str, Any]
    user_history: Optional[Dict[str, Any]] = None
    conversation_context: Optional[Dict[str, Any]] = None

class JournalAnalysisService:
    """Privacy-preserving AI analysis for journal entries"""
    
    def __init__(self):
        self.emotional_intelligence = emotional_intelligence
        self.conversation_engine = intelligent_conversation_engine
        self.crisis_detector = crisis_detector
        
        # Analysis configuration
        self.sentiment_keywords = {
            "positive": ["happy", "joy", "grateful", "love", "excited", "accomplished", "proud", "peaceful"],
            "negative": ["sad", "angry", "frustrated", "worried", "anxious", "stressed", "overwhelmed", "depressed"],
            "growth": ["learned", "realized", "understand", "progress", "improved", "overcome", "insight", "breakthrough"],
            "struggle": ["difficult", "hard", "challenging", "stuck", "confused", "lost", "failing", "hopeless"]
        }
        
        # Therapeutic insights templates
        self.insight_templates = {
            EmotionalState.ANXIOUS: [
                "You're showing awareness of your anxiety, which is an important first step in managing it.",
                "Consider exploring what specific thoughts or situations trigger your anxiety.",
                "Remember that anxiety often contains valuable information about what matters to you."
            ],
            EmotionalState.DEPRESSED: [
                "Writing about difficult feelings takes courage and can be healing.",
                "You're taking an important step by expressing these emotions rather than keeping them inside.",
                "Consider reaching out for additional support during this challenging time."
            ],
            EmotionalState.JOYFUL: [
                "It's wonderful that you're taking time to acknowledge and savor positive experiences.",
                "Consider what contributed to these good feelings so you can cultivate more of them.",
                "Gratitude and joy are powerful forces for mental wellbeing."
            ],
            EmotionalState.ANGRY: [
                "Anger often signals that something important to you has been threatened or violated.",
                "You're processing your anger in a healthy way by writing about it.",
                "Consider what boundaries or values your anger is trying to protect."
            ],
            EmotionalState.CONFUSED: [
                "Confusion is often a natural part of growth and learning.",
                "Writing can help clarify your thoughts and feelings.",
                "It's okay not to have all the answers right now."
            ]
        }
        
        # Crisis safety phrases
        self.crisis_indicators = [
            "end it all", "kill myself", "not worth living", "want to die",
            "suicide", "suicidal", "self harm", "hurt myself", "no way out",
            "better off dead", "can't go on", "nothing matters"
        ]
        
        # Resilience indicators
        self.resilience_indicators = [
            "getting better", "feeling stronger", "making progress", "learned from",
            "overcame", "survived", "growing", "healing", "moving forward",
            "hope", "optimistic", "grateful", "supported", "love"
        ]
    
    async def analyze_journal_entry(self, context: AnalysisContext) -> Optional[JournalAnalysis]:
        """Analyze journal entry with privacy protection"""
        
        try:
            if context.privacy_level == JournalPrivacyLevel.PRIVATE:
                # No analysis for private entries
                return None
            
            analysis = JournalAnalysis(entry_id="")
            
            # Basic sentiment analysis (available for all privacy levels)
            analysis.sentiment_score = await self._analyze_sentiment(context.content)
            analysis.emotional_themes = await self._extract_emotional_themes(context.content)
            
            # Crisis safety check (always performed for safety)
            analysis.crisis_safety_score = await self._assess_crisis_safety(
                context.content, context.user_id
            )
            
            # Enhanced analysis for therapeutic insights level
            if context.privacy_level == JournalPrivacyLevel.THERAPEUTIC_INSIGHTS:
                analysis.growth_indicators = await self._identify_growth_indicators(
                    context.content, context.user_history
                )
                analysis.therapeutic_insights = await self._generate_therapeutic_insights(
                    context.content, context.user_id, context.conversation_context
                )
                analysis.recommended_follow_up = await self._suggest_follow_up_actions(
                    context.content, analysis
                )
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing journal entry: {e}")
            return None
    
    async def _analyze_sentiment(self, content: str) -> float:
        """Calculate sentiment score using emotional intelligence engine"""
        
        try:
            if self.emotional_intelligence:
                # Use existing emotional intelligence engine
                emotional_profile = self.emotional_intelligence.analyze_emotional_state(
                    message=content,
                    conversation_history=[]
                )
                
                if emotional_profile:
                    # Map emotional states to sentiment scores
                    sentiment_mapping = {
                        EmotionalState.JOYFUL: 0.8,
                        EmotionalState.CONTENT: 0.5,
                        EmotionalState.CALM: 0.3,
                        EmotionalState.HOPEFUL: 0.6,
                        EmotionalState.CONFIDENT: 0.7,
                        EmotionalState.MOTIVATED: 0.6,
                        EmotionalState.EXCITED: 0.8,
                        EmotionalState.CONFUSED: -0.2,
                        EmotionalState.ANXIOUS: -0.4,
                        EmotionalState.OVERWHELMED: -0.6,
                        EmotionalState.FRUSTRATED: -0.5,
                        EmotionalState.ANGRY: -0.3,
                        EmotionalState.DEPRESSED: -0.8,
                        EmotionalState.LONELY: -0.6,
                        EmotionalState.INSECURE: -0.4
                    }
                    
                    return sentiment_mapping.get(emotional_profile.primary_emotion, 0.0)
            
            # Fallback: Simple keyword-based sentiment analysis
            return await self._keyword_sentiment_analysis(content)
            
        except Exception as e:
            logger.error(f"Error in sentiment analysis: {e}")
            return 0.0
    
    async def _keyword_sentiment_analysis(self, content: str) -> float:
        """Fallback keyword-based sentiment analysis"""
        
        content_lower = content.lower()
        positive_count = sum(1 for word in self.sentiment_keywords["positive"] if word in content_lower)
        negative_count = sum(1 for word in self.sentiment_keywords["negative"] if word in content_lower)
        
        total_words = len(content.split())
        if total_words == 0:
            return 0.0
        
        # Calculate normalized sentiment score
        positive_score = positive_count / total_words
        negative_score = negative_count / total_words
        
        sentiment = positive_score - negative_score
        
        # Clamp between -1 and 1
        return max(-1.0, min(1.0, sentiment * 10))
    
    async def _extract_emotional_themes(self, content: str) -> List[str]:
        """Extract emotional themes from content"""
        
        try:
            if self.emotional_intelligence:
                # Use existing emotional intelligence engine
                emotional_profile = self.emotional_intelligence.analyze_emotional_state(
                    message=content,
                    conversation_history=[]
                )
                
                if emotional_profile:
                    themes = []
                    
                    # Add primary emotional state
                    themes.append(emotional_profile.primary_emotion.value)
                    
                    # Add secondary emotions if present
                    if emotional_profile.secondary_emotions:
                        themes.extend([emotion.value for emotion in emotional_profile.secondary_emotions[:3]])
                    
                    # Add intensity information
                    themes.append(f"intensity_{emotional_profile.intensity.value}")
                    
                    return themes
            
            # Fallback: Keyword-based theme extraction
            return await self._keyword_theme_extraction(content)
            
        except Exception as e:
            logger.error(f"Error extracting emotional themes: {e}")
            return ["reflection"]
    
    async def _keyword_theme_extraction(self, content: str) -> List[str]:
        """Fallback keyword-based theme extraction"""
        
        content_lower = content.lower()
        themes = []
        
        # Check for various emotional themes
        theme_keywords = {
            "anxiety": ["anxious", "worried", "nervous", "panic", "fear"],
            "depression": ["sad", "depressed", "down", "hopeless", "empty"],
            "anger": ["angry", "mad", "frustrated", "annoyed", "rage"],
            "joy": ["happy", "joy", "excited", "elated", "cheerful"],
            "gratitude": ["grateful", "thankful", "blessed", "appreciate"],
            "growth": ["learned", "progress", "improved", "understand", "insight"],
            "relationships": ["family", "friend", "partner", "love", "connection"],
            "work": ["job", "work", "career", "stress", "meeting"],
            "health": ["tired", "sick", "energy", "sleep", "exercise"]
        }
        
        for theme, keywords in theme_keywords.items():
            if any(keyword in content_lower for keyword in keywords):
                themes.append(theme)
        
        return themes[:5]  # Return top 5 themes
    
    async def _assess_crisis_safety(self, content: str, user_id: str) -> float:
        """Assess crisis indicators in content"""
        
        try:
            if self.crisis_detector:
                # Use existing crisis detection system
                crisis_analysis = self.crisis_detector.analyze_crisis_severity(
                    text=content,
                    sentiment_score=0.0  # We'll calculate this separately
                )
                
                if crisis_analysis:
                    return crisis_analysis.get("crisis_level", 0.0)
            
            # Fallback: Keyword-based crisis detection
            return await self._keyword_crisis_detection(content)
            
        except Exception as e:
            logger.error(f"Error in crisis safety assessment: {e}")
            return 0.0
    
    async def _keyword_crisis_detection(self, content: str) -> float:
        """Fallback keyword-based crisis detection"""
        
        content_lower = content.lower()
        
        # Check for direct crisis indicators
        crisis_score = 0.0
        for indicator in self.crisis_indicators:
            if indicator in content_lower:
                crisis_score += 2.0
        
        # Check for resilience indicators (lower crisis score)
        for indicator in self.resilience_indicators:
            if indicator in content_lower:
                crisis_score -= 0.5
        
        # Normalize score (0-5 scale)
        return max(0.0, min(5.0, crisis_score))
    
    async def _identify_growth_indicators(self, content: str, 
                                        user_history: Optional[Dict[str, Any]]) -> List[str]:
        """Identify signs of personal growth and insight"""
        
        growth_indicators = []
        content_lower = content.lower()
        
        # Growth patterns to look for
        growth_patterns = {
            "self_awareness": ["i realized", "i understand", "i notice", "i see that"],
            "learning": ["learned", "discovered", "figured out", "now i know"],
            "progress": ["getting better", "improving", "making progress", "moving forward"],
            "coping": ["handled it", "managed to", "coped with", "dealt with"],
            "insight": ["insight", "breakthrough", "clarity", "perspective"],
            "resilience": ["bounced back", "recovered", "overcome", "survived"],
            "acceptance": ["accepting", "letting go", "making peace", "okay with"],
            "gratitude": ["grateful", "thankful", "appreciate", "blessed"]
        }
        
        for pattern_name, keywords in growth_patterns.items():
            if any(keyword in content_lower for keyword in keywords):
                growth_indicators.append(pattern_name.replace("_", " "))
        
        # Look for comparative language indicating progress
        if any(phrase in content_lower for phrase in ["better than", "more than before", "used to"]):
            growth_indicators.append("comparative progress")
        
        return growth_indicators[:5]  # Return top 5 indicators
    
    async def _generate_therapeutic_insights(self, content: str, user_id: str,
                                           conversation_context: Optional[Dict[str, Any]]) -> List[str]:
        """Generate therapeutic insights using existing AI systems"""
        
        insights = []
        
        try:
            if self.emotional_intelligence:
                # Get emotional analysis
                emotional_profile = self.emotional_intelligence.analyze_emotional_state(
                    message=content,
                    conversation_history=[]
                )
                
                if emotional_profile:
                    # Get insights based on emotional state
                    state_insights = self.insight_templates.get(
                        emotional_profile.primary_emotion, 
                        ["You're engaging in valuable self-reflection through writing."]
                    )
                    insights.extend(state_insights[:2])
            
            # Add general therapeutic insights
            content_lower = content.lower()
            
            if any(word in content_lower for word in ["feel", "feeling", "felt"]):
                insights.append("You're connecting with your emotions, which is important for emotional wellbeing.")
            
            if any(word in content_lower for word in ["because", "why", "reason"]):
                insights.append("You're exploring the reasons behind your experiences, which promotes self-understanding.")
            
            if any(word in content_lower for word in ["hope", "future", "tomorrow", "next"]):
                insights.append("Your forward-thinking perspective shows resilience and hope.")
            
            # Limit to 3-4 insights to avoid overwhelming
            return insights[:4]
            
        except Exception as e:
            logger.error(f"Error generating therapeutic insights: {e}")
            return ["Writing about your experiences is a valuable form of self-care."]
    
    async def _suggest_follow_up_actions(self, content: str, 
                                       analysis: JournalAnalysis) -> Optional[str]:
        """Suggest follow-up actions based on analysis"""
        
        try:
            # Crisis safety check first
            if analysis.crisis_safety_score >= 4:
                return "Consider reaching out to a mental health professional or crisis hotline for immediate support."
            elif analysis.crisis_safety_score >= 3:
                return "It might be helpful to talk to someone you trust about how you're feeling."
            
            # Sentiment-based suggestions
            if analysis.sentiment_score <= -0.6:
                return "Consider practicing a self-care activity or reaching out to someone supportive."
            elif analysis.sentiment_score >= 0.6:
                return "Consider how you might build on these positive feelings or share them with others."
            
            # Theme-based suggestions
            if "anxiety" in analysis.emotional_themes:
                return "Try some deep breathing or grounding exercises if you're feeling anxious."
            elif "growth" in analysis.growth_indicators:
                return "Reflect on how you can apply these insights to other areas of your life."
            
            return None
            
        except Exception as e:
            logger.error(f"Error suggesting follow-up actions: {e}")
            return None
    
    async def generate_writing_insights(self, user_id: str, 
                                      entries_analysis: List[JournalAnalysis],
                                      time_period: int = 30) -> Dict[str, Any]:
        """Generate comprehensive writing insights from multiple entries"""
        
        try:
            if not entries_analysis:
                return {"message": "Not enough data for insights"}
            
            # Aggregate sentiment trends
            sentiments = [a.sentiment_score for a in entries_analysis if a.sentiment_score is not None]
            avg_sentiment = sum(sentiments) / len(sentiments) if sentiments else 0.0
            
            # Analyze emotional themes over time
            all_themes = []
            for analysis in entries_analysis:
                all_themes.extend(analysis.emotional_themes)
            
            theme_frequency = {}
            for theme in all_themes:
                theme_frequency[theme] = theme_frequency.get(theme, 0) + 1
            
            top_themes = sorted(theme_frequency.items(), key=lambda x: x[1], reverse=True)[:5]
            
            # Identify growth patterns
            all_growth = []
            for analysis in entries_analysis:
                all_growth.extend(analysis.growth_indicators)
            
            growth_patterns = list(set(all_growth))
            
            # Calculate writing consistency
            date_range = time_period
            writing_frequency = len(entries_analysis) / date_range if date_range > 0 else 0
            
            return {
                "time_period_days": time_period,
                "entries_analyzed": len(entries_analysis),
                "average_sentiment": round(avg_sentiment, 2),
                "writing_frequency": round(writing_frequency, 2),
                "common_emotional_themes": [{"theme": theme, "frequency": freq} for theme, freq in top_themes],
                "growth_patterns": growth_patterns,
                "therapeutic_summary": await self._generate_therapeutic_summary(
                    avg_sentiment, top_themes, growth_patterns, writing_frequency
                )
            }
            
        except Exception as e:
            logger.error(f"Error generating writing insights: {e}")
            return {"error": "Could not generate insights"}
    
    async def _generate_therapeutic_summary(self, avg_sentiment: float, 
                                          top_themes: List[Tuple[str, int]],
                                          growth_patterns: List[str],
                                          writing_frequency: float) -> str:
        """Generate therapeutic summary of writing patterns"""
        
        try:
            summary_parts = []
            
            # Sentiment summary
            if avg_sentiment > 0.3:
                summary_parts.append("Your writing shows generally positive emotional processing.")
            elif avg_sentiment < -0.3:
                summary_parts.append("Your writing indicates you're working through some challenging emotions.")
            else:
                summary_parts.append("Your writing shows balanced emotional reflection.")
            
            # Growth summary
            if growth_patterns:
                summary_parts.append(f"You demonstrate {len(growth_patterns)} different growth patterns including {', '.join(growth_patterns[:2])}.")
            
            # Writing consistency
            if writing_frequency >= 0.5:
                summary_parts.append("Your consistent writing practice is a valuable form of self-care.")
            elif writing_frequency >= 0.2:
                summary_parts.append("Regular journaling can enhance the therapeutic benefits you're already experiencing.")
            
            # Theme summary
            if top_themes:
                primary_theme = top_themes[0][0]
                summary_parts.append(f"Your primary focus has been on {primary_theme}, which is important for your wellbeing.")
            
            return " ".join(summary_parts)
            
        except Exception as e:
            logger.error(f"Error generating therapeutic summary: {e}")
            return "Your writing practice shows thoughtful self-reflection and emotional processing."

# Global instance
journal_analysis_service = JournalAnalysisService()