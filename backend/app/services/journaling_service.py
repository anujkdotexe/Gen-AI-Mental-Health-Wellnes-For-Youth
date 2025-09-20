"""
MindSpark AI Journaling Service
Privacy-first therapeutic journaling with AI-enhanced prompts and analysis
"""

from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
import json
import logging
import uuid
from cryptography.fernet import Fernet
import os
import hashlib

# Import existing AI systems and analysis service
try:
    from .emotional_intelligence_engine import emotional_intelligence, EmotionalState
    from .intelligent_conversation_engine import intelligent_conversation_engine
    from .crisis_detection import crisis_detector
    from .journal_analysis_service import journal_analysis_service, AnalysisContext
except ImportError:
    # Fallback for development/testing
    emotional_intelligence = None
    intelligent_conversation_engine = None
    crisis_detector = None
    journal_analysis_service = None

logger = logging.getLogger(__name__)

class TherapeuticFramework(Enum):
    """Evidence-based therapeutic approaches"""
    CBT = "cognitive_behavioral_therapy"
    DBT = "dialectical_behavior_therapy"
    MINDFULNESS = "mindfulness_based"
    ACT = "acceptance_commitment_therapy"
    TRAUMA_INFORMED = "trauma_informed"

class JournalPrivacyLevel(Enum):
    """Privacy levels for journal entries"""
    PRIVATE = "private"  # No AI analysis
    ANONYMOUS_ANALYSIS = "anonymous_analysis"  # AI analysis without personal data
    THERAPEUTIC_INSIGHTS = "therapeutic_insights"  # Full analysis for therapeutic benefit

class JournalEntryType(Enum):
    """Types of journal entries"""
    FREE_FORM = "free_form"
    PROMPTED = "prompted"
    STRUCTURED_TEMPLATE = "structured_template"
    CRISIS_PROCESSING = "crisis_processing"
    GRATITUDE = "gratitude"
    GOAL_REFLECTION = "goal_reflection"

@dataclass
class JournalEntry:
    """Secure journal entry with privacy controls"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str = ""
    encrypted_content: str = ""
    entry_type: JournalEntryType = JournalEntryType.FREE_FORM
    privacy_level: JournalPrivacyLevel = JournalPrivacyLevel.PRIVATE
    therapeutic_framework: Optional[TherapeuticFramework] = None
    prompt_used: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    analysis_data: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

@dataclass
class TherapeuticPrompt:
    """AI-generated therapeutic writing prompt"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    prompt_text: str = ""
    emotional_context: str = ""
    therapeutic_framework: TherapeuticFramework = TherapeuticFramework.MINDFULNESS
    intensity_level: str = "gentle"  # gentle, moderate, deep
    follow_up_prompts: List[str] = field(default_factory=list)
    safety_considerations: List[str] = field(default_factory=list)
    estimated_time: int = 10  # minutes
    created_at: datetime = field(default_factory=datetime.now)

@dataclass
class JournalAnalysis:
    """Privacy-preserving analysis of journal content"""
    entry_id: str = ""
    sentiment_score: float = 0.0
    emotional_themes: List[str] = field(default_factory=list)
    growth_indicators: List[str] = field(default_factory=list)
    therapeutic_insights: List[str] = field(default_factory=list)
    crisis_safety_score: float = 0.0
    recommended_follow_up: Optional[str] = None
    analysis_timestamp: datetime = field(default_factory=datetime.now)

class JournalEncryptionService:
    """End-to-end encryption for journal entries"""
    
    def __init__(self):
        self.key_storage_path = os.getenv("JOURNAL_KEY_STORAGE_PATH", "./keys")
        os.makedirs(self.key_storage_path, exist_ok=True)
    
    def _get_user_key_path(self, user_id: str) -> str:
        """Get secure path for user's encryption key"""
        # Hash user_id for filename security
        hashed_user_id = hashlib.sha256(user_id.encode()).hexdigest()
        return os.path.join(self.key_storage_path, f"{hashed_user_id}.key")
    
    def get_or_create_user_key(self, user_id: str) -> bytes:
        """Get existing user key or create new one"""
        key_path = self._get_user_key_path(user_id)
        
        if os.path.exists(key_path):
            with open(key_path, 'rb') as key_file:
                return key_file.read()
        else:
            # Create new key
            key = Fernet.generate_key()
            with open(key_path, 'wb') as key_file:
                key_file.write(key)
            return key
    
    def encrypt_content(self, content: str, user_id: str) -> str:
        """Encrypt journal content with user-specific key"""
        try:
            key = self.get_or_create_user_key(user_id)
            cipher_suite = Fernet(key)
            encrypted_content = cipher_suite.encrypt(content.encode())
            return encrypted_content.decode()
        except Exception as e:
            logger.error(f"Encryption error for user {user_id}: {e}")
            raise
    
    def decrypt_content(self, encrypted_content: str, user_id: str) -> str:
        """Decrypt journal content for authorized user"""
        try:
            key = self.get_or_create_user_key(user_id)
            cipher_suite = Fernet(key)
            decrypted_content = cipher_suite.decrypt(encrypted_content.encode())
            return decrypted_content.decode()
        except Exception as e:
            logger.error(f"Decryption error for user {user_id}: {e}")
            raise

class JournalPrivacyController:
    """Granular privacy controls for journal features"""
    
    def __init__(self):
        self.user_privacy_preferences = {}
    
    def set_privacy_preference(self, user_id: str, preference_type: str, enabled: bool) -> None:
        """Set user privacy preference"""
        if user_id not in self.user_privacy_preferences:
            self.user_privacy_preferences[user_id] = {}
        self.user_privacy_preferences[user_id][preference_type] = enabled
    
    def has_analysis_consent(self, user_id: str) -> bool:
        """Check if user consents to AI analysis"""
        return self.user_privacy_preferences.get(user_id, {}).get("ai_analysis", False)
    
    def allows_cross_feature_insights(self, user_id: str) -> bool:
        """Check if user allows journal insights to inform other features"""
        return self.user_privacy_preferences.get(user_id, {}).get("cross_feature_integration", False)
    
    def get_privacy_level(self, user_id: str) -> JournalPrivacyLevel:
        """Get user's preferred privacy level"""
        preferences = self.user_privacy_preferences.get(user_id, {})
        
        if preferences.get("ai_analysis", False):
            if preferences.get("therapeutic_insights", False):
                return JournalPrivacyLevel.THERAPEUTIC_INSIGHTS
            else:
                return JournalPrivacyLevel.ANONYMOUS_ANALYSIS
        
        return JournalPrivacyLevel.PRIVATE

class TherapeuticPromptGenerator:
    """AI-enhanced prompt generation using existing emotional intelligence"""
    
    def __init__(self):
        self.emotional_intelligence = emotional_intelligence
        self.conversation_engine = intelligent_conversation_engine
        
        # Therapeutic prompt templates
        self.prompt_templates = {
            EmotionalState.ANXIOUS: {
                "gentle": [
                    "What thoughts are creating anxiety for you right now? Sometimes writing them down can help us see them more clearly.",
                    "Anxiety often carries important information. What is your anxiety trying to protect you from?",
                    "Take a deep breath. What would you like to say to your anxious thoughts right now?"
                ],
                "structured": [
                    "Let's explore this anxiety step by step:\n1. What specifically are you worried about?\n2. How likely is this concern to actually happen?\n3. What evidence supports this worry?\n4. What evidence contradicts it?\n5. What would you tell a friend having this worry?",
                    "Complete this anxiety thought record:\n• Situation that triggered anxiety:\n• Automatic thoughts:\n• Physical sensations:\n• How intense is the anxiety (1-10)?\n• What coping strategy could help right now?"
                ]
            },
            
            EmotionalState.DEPRESSED: {
                "gentle": [
                    "It's okay to feel this way. Your emotions are valid. What would you like to express without any judgment?",
                    "Depression can make everything feel heavy. What's one small thing that went okay today, even if it seems insignificant?",
                    "What would you say to a dear friend who was feeling exactly like you are right now?"
                ],
                "compassionate": [
                    "When you're ready, write about a time when you felt better than you do now. What was different then?",
                    "What parts of yourself do you miss right now? How might you gently reconnect with those parts?",
                    "Depression often tells us lies about ourselves. What would your most compassionate self want you to know right now?"
                ]
            },
            
            EmotionalState.JOYFUL: {
                "celebration": [
                    "You're feeling good right now! What's contributing to these positive feelings? Let's capture this moment.",
                    "Joy is precious. Describe this feeling in detail so you can remember it during tougher times.",
                    "What are you most grateful for in this moment of happiness?"
                ],
                "building": [
                    "How can you build on these good feelings? What would you like to do with this positive energy?",
                    "What does this joyful feeling teach you about what matters most to you?",
                    "Who would you like to share this happiness with, and how might you do that?"
                ]
            },
            
            EmotionalState.ANGRY: {
                "expression": [
                    "Anger often has important information for us. What is your anger trying to tell you?",
                    "Let yourself express this anger fully on paper. Don't hold back - this is your safe space.",
                    "What boundary was crossed that led to this anger? How do you want to protect that boundary?"
                ],
                "processing": [
                    "Behind anger, there's often hurt, fear, or injustice. What might be underneath this feeling?",
                    "Now that you've expressed the anger, what (if anything) would you like to do about the situation?",
                    "How can you honor your anger while also taking care of yourself?"
                ]
            },
            
            EmotionalState.CONFUSED: {
                "exploration": [
                    "Confusion can be uncomfortable, but it's often a sign that you're growing. What feels unclear right now?",
                    "Sometimes writing helps untangle our thoughts. What are all the different pieces of this confusion?",
                    "What questions are you sitting with? It's okay not to have answers yet."
                ],
                "clarity": [
                    "If you could have clarity about one aspect of this confusion, what would it be?",
                    "What would your wisest self advise you about this confusing situation?",
                    "What small step could help you move forward, even without complete clarity?"
                ]
            },
            
            EmotionalState.OVERWHELMED: {
                "grounding": [
                    "When everything feels like too much, let's start small. What's one thing you can control right now?",
                    "Overwhelm often comes from trying to hold too much at once. What can you set down, even temporarily?",
                    "Take a moment to breathe. What does your body need right now to feel more grounded?"
                ],
                "prioritizing": [
                    "What are the most important things demanding your attention? Can you list them in order of priority?",
                    "If you could only focus on three things today, what would they be?",
                    "What support do you need to feel less overwhelmed? Who or what could provide that support?"
                ]
            }
        }
        
        # Crisis-specific prompts
        self.crisis_prompts = {
            "safety_check": [
                "Right now, in this moment, you are safe. Can you write about what safety feels like to you?",
                "What are the things in your life that anchor you? Who are the people who care about you?",
                "What has helped you get through difficult times before? What strengths did you use?"
            ],
            "hope_building": [
                "Even in the darkest moments, there can be tiny sparks of hope. What's one small thing you're looking forward to?",
                "What would you want to say to yourself one year from now, looking back on this difficult time?",
                "What are the reasons you want to keep going, even if they feel small right now?"
            ],
            "connection": [
                "Who in your life would want to know you're struggling right now? How could you reach out to them?",
                "What would you want someone to say to you if they knew how you were feeling?",
                "Write a letter to someone who cares about you (you don't have to send it)."
            ]
        }
    
    async def generate_personalized_prompt(self, user_id: str, 
                                         entry_type: JournalEntryType = JournalEntryType.FREE_FORM) -> TherapeuticPrompt:
        """Generate contextual writing prompt using existing AI systems"""
        
        try:
            # Get current emotional state from emotional intelligence engine
            current_emotional_state = self._get_current_emotional_state(user_id)
            
            # Get conversation context from intelligent conversation engine
            conversation_context = self._get_conversation_context(user_id)
            
            # Check for crisis indicators
            crisis_level = self._check_crisis_level(user_id)
            
            # Generate appropriate prompt
            if crisis_level >= 3:
                return self._create_crisis_prompt(current_emotional_state, crisis_level)
            else:
                return self._create_contextual_prompt(
                    emotional_state=current_emotional_state,
                    conversation_themes=conversation_context.get("themes", []),
                    entry_type=entry_type
                )
                
        except Exception as e:
            logger.error(f"Error generating prompt for user {user_id}: {e}")
            return self._create_fallback_prompt()
    
    def _get_current_emotional_state(self, user_id: str) -> EmotionalState:
        """Get user's current emotional state from emotional intelligence engine"""
        if self.emotional_intelligence:
            try:
                # This would integrate with the emotional intelligence engine
                # For now, return a default state
                return EmotionalState.CALM
            except Exception as e:
                logger.error(f"Error getting emotional state: {e}")
        
        return EmotionalState.CALM
    
    def _get_conversation_context(self, user_id: str) -> Dict[str, Any]:
        """Get recent conversation themes from intelligent conversation engine"""
        if self.conversation_engine:
            try:
                # This would integrate with the conversation engine
                # For now, return empty context
                return {"themes": [], "mood": "neutral"}
            except Exception as e:
                logger.error(f"Error getting conversation context: {e}")
        
        return {"themes": [], "mood": "neutral"}
    
    def _check_crisis_level(self, user_id: str) -> int:
        """Check for crisis indicators using existing crisis detection"""
        try:
            # This would integrate with existing crisis detection
            # For now, return no crisis
            return 0
        except Exception as e:
            logger.error(f"Error checking crisis level: {e}")
            return 0
    
    def _create_contextual_prompt(self, emotional_state: EmotionalState, 
                                      conversation_themes: List[str],
                                      entry_type: JournalEntryType) -> TherapeuticPrompt:
        """Create prompt based on current context"""
        
        # Get appropriate prompts for emotional state
        state_prompts = self.prompt_templates.get(emotional_state, 
                                                self.prompt_templates[EmotionalState.CALM])
        
        # Choose intensity based on entry type
        if entry_type == JournalEntryType.STRUCTURED_TEMPLATE:
            intensity = "structured"
        else:
            intensity = "gentle"
        
        # Select prompt
        prompt_options = state_prompts.get(intensity, state_prompts.get("gentle", []))
        selected_prompt = prompt_options[0] if prompt_options else "What's on your mind today?"
        
        return TherapeuticPrompt(
            prompt_text=selected_prompt,
            emotional_context=emotional_state.value,
            therapeutic_framework=self._select_therapeutic_framework(emotional_state),
            intensity_level=intensity,
            follow_up_prompts=self._generate_follow_up_prompts(emotional_state),
            safety_considerations=self._get_safety_considerations(emotional_state)
        )
    
    def _create_crisis_prompt(self, emotional_state: EmotionalState, 
                                  crisis_level: int) -> TherapeuticPrompt:
        """Create specialized prompts for crisis situations"""
        
        if crisis_level >= 4:
            # High crisis - focus on immediate safety
            prompt_category = "safety_check"
        elif crisis_level == 3:
            # Moderate crisis - build hope and connection
            prompt_category = "hope_building"
        else:
            # Lower crisis - encourage connection
            prompt_category = "connection"
        
        crisis_prompts = self.crisis_prompts.get(prompt_category, self.crisis_prompts["safety_check"])
        selected_prompt = crisis_prompts[0]
        
        return TherapeuticPrompt(
            prompt_text=selected_prompt,
            emotional_context=emotional_state.value,
            therapeutic_framework=TherapeuticFramework.TRAUMA_INFORMED,
            intensity_level="crisis",
            follow_up_prompts=["How are you feeling after writing that?", "What support do you need right now?"],
            safety_considerations=["Crisis resources available", "Professional support recommended", "Check safety plan"]
        )
    
    def _create_fallback_prompt(self) -> TherapeuticPrompt:
        """Create a safe, general prompt when other systems are unavailable"""
        return TherapeuticPrompt(
            prompt_text="How are you feeling right now? Take your time and write whatever comes to mind.",
            emotional_context="neutral",
            therapeutic_framework=TherapeuticFramework.MINDFULNESS,
            intensity_level="gentle"
        )
    
    def _select_therapeutic_framework(self, emotional_state: EmotionalState) -> TherapeuticFramework:
        """Select appropriate therapeutic framework based on emotional state"""
        framework_mapping = {
            EmotionalState.ANXIOUS: TherapeuticFramework.CBT,
            EmotionalState.ANGRY: TherapeuticFramework.DBT,
            EmotionalState.DEPRESSED: TherapeuticFramework.CBT,
            EmotionalState.OVERWHELMED: TherapeuticFramework.MINDFULNESS,
            EmotionalState.CONFUSED: TherapeuticFramework.ACT
        }
        
        return framework_mapping.get(emotional_state, TherapeuticFramework.MINDFULNESS)
    
    def _generate_follow_up_prompts(self, emotional_state: EmotionalState) -> List[str]:
        """Generate follow-up prompts based on emotional state"""
        follow_ups = {
            EmotionalState.ANXIOUS: [
                "How do you feel after writing about your anxiety?",
                "What coping strategy could help you right now?",
                "What would you like to do with these insights?"
            ],
            EmotionalState.DEPRESSED: [
                "What was it like to express these feelings?",
                "What small act of self-care could you do today?",
                "Who could you reach out to for support?"
            ],
            EmotionalState.JOYFUL: [
                "How can you carry this positive energy forward?",
                "What does this joy teach you about yourself?",
                "How might you share this happiness with others?"
            ]
        }
        
        return follow_ups.get(emotional_state, [
            "How are you feeling after writing?",
            "What insights emerged for you?",
            "What would be helpful to explore next?"
        ])
    
    def _get_safety_considerations(self, emotional_state: EmotionalState) -> List[str]:
        """Get safety considerations for different emotional states"""
        safety_notes = {
            EmotionalState.DEPRESSED: ["Monitor for crisis indicators", "Encourage professional support if persistent"],
            EmotionalState.ANXIOUS: ["Watch for panic triggers", "Offer grounding techniques"],
            EmotionalState.ANGRY: ["Ensure safe expression", "Avoid escalation triggers"],
            EmotionalState.OVERWHELMED: ["Prevent additional stressors", "Focus on immediate safety"]
        }
        
        return safety_notes.get(emotional_state, ["Monitor user wellbeing"])

class JournalService:
    """Main journaling service orchestrating all components"""
    
    def __init__(self):
        self.encryption_service = JournalEncryptionService()
        self.privacy_controller = JournalPrivacyController()
        self.prompt_generator = TherapeuticPromptGenerator()
        self.journal_storage = {}  # This will be replaced with database integration
        
    async def create_journal_entry(self, user_id: str, content: str, 
                                 entry_type: JournalEntryType = JournalEntryType.FREE_FORM,
                                 prompt_id: Optional[str] = None,
                                 therapeutic_framework: Optional[TherapeuticFramework] = None) -> JournalEntry:
        """Create a new journal entry with privacy protection"""
        
        try:
            # Get user's privacy level
            privacy_level = self.privacy_controller.get_privacy_level(user_id)
            
            # Encrypt content
            encrypted_content = self.encryption_service.encrypt_content(content, user_id)
            
            # Create entry
            entry = JournalEntry(
                user_id=user_id,
                encrypted_content=encrypted_content,
                entry_type=entry_type,
                privacy_level=privacy_level,
                therapeutic_framework=therapeutic_framework,
                prompt_used=prompt_id,
                metadata={
                    "content_length": len(content),
                    "word_count": len(content.split()),
                    "creation_method": "manual" if not prompt_id else "prompted"
                }
            )
            
            # Perform analysis if user consents
            if privacy_level != JournalPrivacyLevel.PRIVATE and journal_analysis_service:
                analysis_context = AnalysisContext(
                    user_id=user_id,
                    privacy_level=privacy_level,
                    content=content,
                    entry_metadata=entry.metadata
                )
                analysis = await journal_analysis_service.analyze_journal_entry(analysis_context)
                entry.analysis_data = analysis.__dict__ if analysis else {}
            
            # Store entry (this will use database in production)
            if user_id not in self.journal_storage:
                self.journal_storage[user_id] = []
            self.journal_storage[user_id].append(entry)
            
            logger.info(f"Created journal entry for user {user_id}, privacy level: {privacy_level.value}")
            return entry
            
        except Exception as e:
            logger.error(f"Error creating journal entry for user {user_id}: {e}")
            raise
    
    async def get_journal_entries(self, user_id: str, 
                                start_date: Optional[datetime] = None,
                                end_date: Optional[datetime] = None,
                                entry_type: Optional[JournalEntryType] = None,
                                limit: int = 50) -> List[JournalEntry]:
        """Get user's journal entries with privacy protection"""
        
        try:
            user_entries = self.journal_storage.get(user_id, [])
            
            # Filter by date range
            if start_date:
                user_entries = [e for e in user_entries if e.created_at >= start_date]
            if end_date:
                user_entries = [e for e in user_entries if e.created_at <= end_date]
            
            # Filter by entry type
            if entry_type:
                user_entries = [e for e in user_entries if e.entry_type == entry_type]
            
            # Sort by creation date (newest first) and limit
            user_entries.sort(key=lambda x: x.created_at, reverse=True)
            user_entries = user_entries[:limit]
            
            logger.info(f"Retrieved {len(user_entries)} journal entries for user {user_id}")
            return user_entries
            
        except Exception as e:
            logger.error(f"Error retrieving journal entries for user {user_id}: {e}")
            return []
    
    async def get_journal_entry_content(self, user_id: str, entry_id: str) -> Optional[str]:
        """Decrypt and return journal entry content for authorized user"""
        
        try:
            # Find the entry
            user_entries = self.journal_storage.get(user_id, [])
            entry = next((e for e in user_entries if e.id == entry_id), None)
            
            if not entry:
                logger.warning(f"Entry {entry_id} not found for user {user_id}")
                return None
            
            # Decrypt content
            decrypted_content = self.encryption_service.decrypt_content(
                entry.encrypted_content, user_id
            )
            
            return decrypted_content
            
        except Exception as e:
            logger.error(f"Error retrieving entry content for user {user_id}, entry {entry_id}: {e}")
            return None
    
    async def update_journal_entry(self, user_id: str, entry_id: str, 
                                 new_content: str) -> Optional[JournalEntry]:
        """Update existing journal entry with new content"""
        
        try:
            # Find the entry
            user_entries = self.journal_storage.get(user_id, [])
            entry = next((e for e in user_entries if e.id == entry_id), None)
            
            if not entry:
                logger.warning(f"Entry {entry_id} not found for user {user_id}")
                return None
            
            # Encrypt new content
            encrypted_content = self.encryption_service.encrypt_content(new_content, user_id)
            
            # Update entry
            entry.encrypted_content = encrypted_content
            entry.updated_at = datetime.now()
            entry.metadata["word_count"] = len(new_content.split())
            entry.metadata["content_length"] = len(new_content)
            entry.metadata["last_modified"] = "user_edit"
            
            # Re-analyze if user consents
            if entry.privacy_level != JournalPrivacyLevel.PRIVATE and journal_analysis_service:
                analysis_context = AnalysisContext(
                    user_id=user_id,
                    privacy_level=entry.privacy_level,
                    content=new_content,
                    entry_metadata=entry.metadata
                )
                analysis = await journal_analysis_service.analyze_journal_entry(analysis_context)
                entry.analysis_data = analysis.__dict__ if analysis else {}
            
            logger.info(f"Updated journal entry {entry_id} for user {user_id}")
            return entry
            
        except Exception as e:
            logger.error(f"Error updating entry {entry_id} for user {user_id}: {e}")
            return None
    
    async def delete_journal_entry(self, user_id: str, entry_id: str) -> bool:
        """Permanently delete journal entry and associated data"""
        
        try:
            user_entries = self.journal_storage.get(user_id, [])
            entry_index = next((i for i, e in enumerate(user_entries) if e.id == entry_id), None)
            
            if entry_index is None:
                logger.warning(f"Entry {entry_id} not found for user {user_id}")
                return False
            
            # Remove the entry
            removed_entry = user_entries.pop(entry_index)
            
            logger.info(f"Deleted journal entry {entry_id} for user {user_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting entry {entry_id} for user {user_id}: {e}")
            return False
    
    async def generate_writing_prompt(self, user_id: str, 
                                    entry_type: JournalEntryType = JournalEntryType.PROMPTED,
                                    therapeutic_framework: Optional[TherapeuticFramework] = None) -> TherapeuticPrompt:
        """Generate personalized therapeutic writing prompt"""
        
        try:
            prompt = await self.prompt_generator.generate_personalized_prompt(user_id, entry_type)
            
            # Override therapeutic framework if specified
            if therapeutic_framework:
                prompt.therapeutic_framework = therapeutic_framework
            
            logger.info(f"Generated prompt for user {user_id}, framework: {prompt.therapeutic_framework.value}")
            return prompt
            
        except Exception as e:
            logger.error(f"Error generating prompt for user {user_id}: {e}")
            # Return fallback prompt
            return self.prompt_generator._create_fallback_prompt()
    
    async def get_journal_insights(self, user_id: str, 
                                 days_range: int = 30) -> Optional[Dict[str, Any]]:
        """Get privacy-preserving insights from journal entries"""
        
        try:
            # Check if user allows insights
            if not self.privacy_controller.has_analysis_consent(user_id):
                logger.info(f"User {user_id} has not consented to journal analysis")
                return None
            
            # Get recent entries
            cutoff_date = datetime.now() - timedelta(days=days_range)
            entries = await self.get_journal_entries(
                user_id=user_id,
                start_date=cutoff_date,
                limit=100
            )
            
            if not entries:
                return None
            
            # Aggregate insights from entry analyses
            insights = await self._aggregate_insights(entries, user_id)
            
            logger.info(f"Generated insights for user {user_id} from {len(entries)} entries")
            return insights
            
        except Exception as e:
            logger.error(f"Error generating insights for user {user_id}: {e}")
            return None
    
    async def set_privacy_preferences(self, user_id: str, preferences: Dict[str, bool]) -> bool:
        """Update user's privacy preferences"""
        
        try:
            for pref_type, enabled in preferences.items():
                self.privacy_controller.set_privacy_preference(user_id, pref_type, enabled)
            
            logger.info(f"Updated privacy preferences for user {user_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error updating privacy preferences for user {user_id}: {e}")
            return False
    
    async def get_privacy_preferences(self, user_id: str) -> Dict[str, Any]:
        """Get user's current privacy preferences and explanations"""
        
        try:
            current_level = self.privacy_controller.get_privacy_level(user_id)
            preferences = self.privacy_controller.user_privacy_preferences.get(user_id, {})
            
            return {
                "current_privacy_level": current_level.value,
                "preferences": preferences,
                "available_options": {
                    "ai_analysis": "Allow AI to analyze journal entries for insights",
                    "therapeutic_insights": "Enable therapeutic insights and recommendations",
                    "cross_feature_integration": "Allow journal insights to inform other features",
                    "prompt_personalization": "Use conversation history to personalize writing prompts"
                },
                "privacy_levels": {
                    level.value: self._get_privacy_level_description(level)
                    for level in JournalPrivacyLevel
                }
            }
            
        except Exception as e:
            logger.error(f"Error getting privacy preferences for user {user_id}: {e}")
            return {}
    
    async def _analyze_entry_content(self, content: str, user_id: str, 
                                   privacy_level: JournalPrivacyLevel) -> Optional[JournalAnalysis]:
        """Analyze journal entry content with privacy protection"""
        
        try:
            # Create analysis based on privacy level
            analysis = JournalAnalysis()
            
            if privacy_level == JournalPrivacyLevel.ANONYMOUS_ANALYSIS:
                # Basic sentiment and theme analysis without personal data
                analysis.sentiment_score = await self._calculate_sentiment(content)
                analysis.emotional_themes = await self._extract_emotional_themes(content)
                
            elif privacy_level == JournalPrivacyLevel.THERAPEUTIC_INSIGHTS:
                # Full analysis for therapeutic benefit
                analysis.sentiment_score = await self._calculate_sentiment(content)
                analysis.emotional_themes = await self._extract_emotional_themes(content)
                analysis.growth_indicators = await self._identify_growth_indicators(content)
                analysis.therapeutic_insights = await self._generate_therapeutic_insights(content, user_id)
                analysis.crisis_safety_score = await self._assess_crisis_safety(content, user_id)
                analysis.recommended_follow_up = await self._suggest_follow_up(content, analysis)
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing entry content: {e}")
            return None
    
    async def _calculate_sentiment(self, content: str) -> float:
        """Calculate sentiment score from content"""
        # This would integrate with existing AI systems
        # For now, return neutral sentiment
        return 0.0
    
    async def _extract_emotional_themes(self, content: str) -> List[str]:
        """Extract emotional themes from content"""
        # This would integrate with emotional intelligence engine
        return ["reflection", "processing"]
    
    async def _identify_growth_indicators(self, content: str) -> List[str]:
        """Identify signs of personal growth or insight"""
        # This would use existing AI systems to identify growth patterns
        return []
    
    async def _generate_therapeutic_insights(self, content: str, user_id: str) -> List[str]:
        """Generate therapeutic insights from content"""
        # This would integrate with conversation engine for deeper insights
        return []
    
    async def _assess_crisis_safety(self, content: str, user_id: str) -> float:
        """Assess crisis indicators in content"""
        # This would integrate with existing crisis detection
        return 0.0
    
    async def _suggest_follow_up(self, content: str, analysis: JournalAnalysis) -> Optional[str]:
        """Suggest follow-up actions based on analysis"""
        if analysis.crisis_safety_score >= 3:
            return "Consider reaching out for support if you're struggling"
        elif analysis.sentiment_score < -0.5:
            return "It might help to explore these feelings with someone you trust"
        else:
            return None
    
    async def _aggregate_insights(self, entries: List[JournalEntry], user_id: str) -> Dict[str, Any]:
        """Aggregate insights from multiple journal entries"""
        
        # Extract analysis data from entries
        analyses = [JournalAnalysis(**entry.analysis_data) for entry in entries if entry.analysis_data]
        
        if not analyses:
            return {"message": "Not enough data for insights", "entries_analyzed": 0}
        
        # Calculate aggregated metrics
        avg_sentiment = sum(a.sentiment_score for a in analyses) / len(analyses)
        all_themes = [theme for a in analyses for theme in a.emotional_themes]
        theme_counts = {}
        for theme in all_themes:
            theme_counts[theme] = theme_counts.get(theme, 0) + 1
        
        # Get most common themes
        top_themes = sorted(theme_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return {
            "entries_analyzed": len(analyses),
            "date_range": {
                "start": min(a.analysis_timestamp for a in analyses).isoformat(),
                "end": max(a.analysis_timestamp for a in analyses).isoformat()
            },
            "average_sentiment": round(avg_sentiment, 2),
            "sentiment_trend": self._calculate_sentiment_trend(analyses),
            "common_themes": [{"theme": theme, "frequency": count} for theme, count in top_themes],
            "growth_indicators": list(set([indicator for a in analyses for indicator in a.growth_indicators])),
            "overall_insight": await self._generate_overall_insight(analyses, user_id)
        }
    
    def _calculate_sentiment_trend(self, analyses: List[JournalAnalysis]) -> str:
        """Calculate sentiment trend over time"""
        if len(analyses) < 2:
            return "insufficient_data"
        
        # Sort by timestamp
        sorted_analyses = sorted(analyses, key=lambda x: x.analysis_timestamp)
        
        # Compare first half to second half
        midpoint = len(sorted_analyses) // 2
        first_half_avg = sum(a.sentiment_score for a in sorted_analyses[:midpoint]) / midpoint
        second_half_avg = sum(a.sentiment_score for a in sorted_analyses[midpoint:]) / (len(sorted_analyses) - midpoint)
        
        difference = second_half_avg - first_half_avg
        
        if difference > 0.2:
            return "improving"
        elif difference < -0.2:
            return "declining"
        else:
            return "stable"
    
    async def _generate_overall_insight(self, analyses: List[JournalAnalysis], user_id: str) -> str:
        """Generate overall insight from journal analysis"""
        # This would use existing AI systems for deeper insight generation
        avg_sentiment = sum(a.sentiment_score for a in analyses) / len(analyses)
        
        if avg_sentiment > 0.2:
            return "Your writing shows generally positive emotional processing and reflection."
        elif avg_sentiment < -0.2:
            return "Your writing shows you're working through some challenging feelings. Consider additional support if needed."
        else:
            return "Your writing shows balanced emotional processing and self-reflection."
    
    def _get_privacy_level_description(self, level: JournalPrivacyLevel) -> str:
        """Get description of privacy level"""
        descriptions = {
            JournalPrivacyLevel.PRIVATE: "Complete privacy - no AI analysis or insights",
            JournalPrivacyLevel.ANONYMOUS_ANALYSIS: "Basic insights without personal data integration",
            JournalPrivacyLevel.THERAPEUTIC_INSIGHTS: "Full therapeutic insights and personalized recommendations"
        }
        return descriptions.get(level, "Unknown privacy level")

# Global service instances
encryption_service = JournalEncryptionService()
privacy_controller = JournalPrivacyController()
prompt_generator = TherapeuticPromptGenerator()
journal_service = JournalService()