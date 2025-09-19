import openai
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import os
from typing import Dict, List, Optional, Tuple
import json
import re

# Initialize sentiment analyzer
sentiment_analyzer = SentimentIntensityAnalyzer()

# Crisis keywords for detection
CRISIS_KEYWORDS = [
    'suicide', 'kill myself', 'end it all', 'want to die', 'not worth living',
    'hurt myself', 'self harm', 'cutting', 'overdose', 'pills',
    'jump off', 'hang myself', 'gun', 'knife', 'blade',
    'hopeless', 'worthless', 'burden', 'better off dead',
    'can\'t go on', 'give up', 'no point', 'end the pain'
]

class AIService:
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        if self.openai_api_key:
            openai.api_key = self.openai_api_key
        
        # Mental health conversation prompts
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

    def analyze_sentiment(self, text: str) -> Dict[str, float]:
        """Analyze sentiment of text using VADER"""
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

    async def generate_response(self, user_message: str, conversation_history: Optional[List[Dict]] = None) -> Dict:
        """Generate AI response to user message"""
        
        # Analyze sentiment and crisis indicators
        sentiment = self.analyze_sentiment(user_message)
        is_crisis, crisis_score, crisis_keywords = self.detect_crisis(user_message)
        
        # Prepare conversation context
        messages = [{"role": "system", "content": self.system_prompt}]
        
        if conversation_history:
            for msg in conversation_history[-10:]:  # Keep last 10 messages for context
                role = "user" if msg['is_user'] else "assistant"
                messages.append({"role": role, "content": msg['content']})
        
        messages.append({"role": "user", "content": user_message})
        
        try:
            if self.openai_api_key:
                # Use OpenAI API (updated for v1.0+)
                client = openai.OpenAI(api_key=self.openai_api_key)
                
                # Properly format messages for OpenAI API
                formatted_messages = []
                for msg in messages:
                    formatted_messages.append({
                        "role": msg["role"],
                        "content": msg["content"]
                    })
                
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=formatted_messages,
                    max_tokens=300,
                    temperature=0.7,
                    presence_penalty=0.1,
                    frequency_penalty=0.1
                )
                ai_response = response.choices[0].message.content
                if ai_response:
                    ai_response = ai_response.strip()
                else:
                    ai_response = self._generate_fallback_response(user_message, sentiment, is_crisis)
            else:
                # Fallback responses for demo
                ai_response = self._generate_fallback_response(user_message, sentiment, is_crisis)
            
            # If crisis detected, add crisis resources information
            if is_crisis:
                ai_response += "\n\n⚠️ I'm concerned about what you're sharing. Please know that you're not alone, and help is available. If you're in immediate danger, please call emergency services (911) or the crisis line (988)."
            
            return {
                "response": ai_response,
                "sentiment_score": sentiment['compound'],
                "crisis_detected": is_crisis,
                "crisis_score": crisis_score,
                "crisis_keywords": crisis_keywords,
                "confidence": 0.85 if self.openai_api_key else 0.6
            }
            
        except Exception as e:
            print(f"AI service error: {e}")
            return {
                "response": self._generate_fallback_response(user_message, sentiment, is_crisis),
                "sentiment_score": sentiment['compound'],
                "crisis_detected": is_crisis,
                "crisis_score": crisis_score,
                "crisis_keywords": crisis_keywords,
                "confidence": 0.6
            }

    def _generate_fallback_response(self, user_message: str, sentiment: Dict, is_crisis: bool) -> str:
        """Generate fallback response when OpenAI is not available"""
        
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

# Global AI service instance
ai_service = AIService()