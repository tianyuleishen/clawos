# 🦞 Emotion Module - 情感模块

"""
情感模块 - 让交互更自然
"""

import asyncio
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum
from datetime import datetime

class Sentiment(Enum):
    """情感类别"""
    HAPPY = "happy"
    SAD = "sad"
    ANGRY = "angry"
    FRUSTRATED = "frustrated"
    NEUTRAL = "neutral"
    EXCITED = "excited"
    ANXIOUS = "anxious"
    CALM = "calm"

class Personality(Enum):
    """人格类型"""
    PROFESSIONAL = "professional"
    FRIENDLY = "friendly"
    HUMOROUS = "humorous"
    EMPATHETIC = "empathetic"
    ENTHUSIASTIC = "enthusiastic"
    CALM = "calm"
    ENCOURAGING = "encouraging"

@dataclass
class SentimentResult:
    sentiment: Sentiment
    confidence: float
    intensity: float
    keywords: List[str]
    needs: List[str]

@dataclass
class EmotionalResponse:
    content: str
    sentiment: Sentiment
    tone: str
    personality: Personality
    suggestions: List[str]

class SentimentAnalyzer:
    def __init__(self):
        self.keywords = {
            'happy': ['开心', '高兴', '快乐', '兴奋', '激动', '喜悦', '幸福', '棒', '太好了'],
            'sad': ['难过', '伤心', '悲伤', '失落', '沮丧', '痛苦', '郁闷', '烦'],
            'angry': ['生气', '愤怒', '恼火', '讨厌', '可恶', '气死了'],
            'frustrated': ['挫败', '无奈', '没办法', '搞不定', '太难了', '崩溃'],
            'excited': ['太棒了', '太好了', '期待', '激动'],
            'anxious': ['担心', '焦虑', '紧张', '不安', '害怕'],
            'calm': ['平静', '淡定', '从容', '冷静'],
            'neutral': ['一般', '普通', '还好']
        }
    
    def analyze(self, text: str) -> SentimentResult:
        text_lower = text.lower()
        scores = {}
        for sentiment, keywords in self.keywords.items():
            scores[sentiment] = sum(1 for kw in keywords if kw in text_lower)
        
        if max(scores.values()) == 0:
            sentiment = Sentiment.NEUTRAL
        else:
            sentiment = max(scores, key=scores.get)
        
        keywords = [kw for kw in self.keywords.get(sentiment, []) if kw in text_lower]
        intensity = min(1.0, scores[sentiment] / 3)
        
        needs_map = {
            Sentiment.HAPPY: ['分享', '认可'],
            Sentiment.SAD: ['安慰', '陪伴'],
            Sentiment.ANGRY: ['理解', '支持'],
            Sentiment.FRUSTRATED: ['鼓励', '建议'],
            Sentiment.EXCITED: ['分享', '认可'],
            Sentiment.ANXIOUS: ['安慰', '保证'],
            Sentiment.CALM: ['继续', '专注'],
            Sentiment.NEUTRAL: ['信息', '帮助']
        }
        
        return SentimentResult(
            sentiment=sentiment,
            confidence=min(0.95, 0.5 + intensity * 0.3),
            intensity=intensity,
            keywords=keywords,
            needs=needs_map.get(sentiment, ['帮助'])
        )

class EmotionResponseGenerator:
    def __init__(self):
        self.templates = {
            Sentiment.HAPPY: {
                Personality.FRIENDLY: ["听到你这么开心，我也很高兴！🎉", "太棒了！继续保持！✨", "太好了！"],
                Personality.PROFESSIONAL: ["很高兴看到您好心情。", "积极情绪有助于效率。"],
                Personality.EMPATHETIC: ["我能感受到你的喜悦！😊", "太好了！"],
            },
            Sentiment.SAD: {
                Personality.EMPATHETIC: ["听到你难过，我也很心疼。😢", "别难过，一切都会好起来。💙"],
                Personality.FRIENDLY: ["别太难过了。", "难过的时候记得还有我。🤗"],
            },
            Sentiment.ANGRY: {
                Personality.CALM: ["深呼吸，冷静一下。🌬️", "别太生气，气坏身体不值得。"],
                Personality.EMPATHETIC: ["我能理解你为什么会生气。"],
            },
            Sentiment.FRUSTRATED: {
                Personality.ENCOURAGING: ["别灰心，你已经很努力了！💪", "暂时的挫折不代表什么。"],
                Personality.PROFESSIONAL: ["面对挫折是成长的一部分。", "换个角度思考问题。"],
            },
            Sentiment.NEUTRAL: {
                Personality.PROFESSIONAL: ["好的，请告诉我更多细节。", "请问还有什么需要帮助的？"],
                Personality.FRIENDLY: ["好的呀！还有什么想问的？😊"],
            }
        }
    
    def generate(self, sentiment: Sentiment, personality: Personality, context: str = "") -> str:
        templates = self.templates.get(sentiment, {})
        personality_templates = templates.get(personality, templates.get(Personality.FRIENDLY, ["我理解你的感受。"]))
        import random
        return random.choice(personality_templates)

class PersonalityManager:
    def __init__(self):
        self.current = Personality.FRIENDLY
    
    def set_personality(self, personality: Personality):
        self.current = personality
    
    def get_personality(self) -> Personality:
        return self.current

class EmotionModule:
    def __init__(self):
        self.version = "1.0"
        self.sentiment_analyzer = SentimentAnalyzer()
        self.response_generator = EmotionResponseGenerator()
        self.personality_manager = PersonalityManager()
        print("✅ Emotion Module v1.0 已加载")
        print(f"   当前人格: {self.personality_manager.current.value}")
    
    async def analyze(self, text: str) -> SentimentResult:
        return self.sentiment_analyzer.analyze(text)
    
    async def generate_response(self, user_text: str, system_response: str = "") -> EmotionalResponse:
        sentiment = self.sentiment_analyzer.analyze(user_text)
        personality = self.personality_manager.get_personality()
        content = self.response_generator.generate(sentiment.sentiment, personality, user_text)
        
        tone_map = {
            Sentiment.HAPPY: "热情友好",
            Sentiment.SAD: "温暖关怀",
            Sentiment.ANGRY: "冷静安抚",
            Sentiment.FRUSTRATED: "鼓励支持",
            Sentiment.NEUTRAL: "简洁友好"
        }
        
        return EmotionalResponse(
            content=content,
            sentiment=sentiment.sentiment,
            tone=tone_map.get(sentiment.sentiment, "专业友好"),
            personality=personality,
            suggestions=sentiment.needs
        )

if __name__ == "__main__":
    async def test():
        module = EmotionModule()
        tests = ["今天工作完成了，好开心！🎉", "项目失败了，好难过..."]
        for test in tests:
            result = await module.generate_response(test)
            print(f"\n输入: {test}")
            print(f"情感: {result.sentiment.value}")
            print(f"回复: {result.content}")
    asyncio.run(test())
