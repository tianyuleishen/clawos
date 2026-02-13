# 🦞 Emotion Recognizer - 情绪识别

"""
情绪识别模块

功能:
- 识别用户情绪（ frustration、impatience等）
- 根据情绪调整回复策略
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


class EmotionType(Enum):
    """情绪类型"""
    FRUSTRATED = "frustrated"  # 沮丧/烦躁
    IMPATIENT = "impatient"      # 急躁
    CONFUSED = "confused"       # 困惑
    SATISFIED = "satisfied"      # 满意
    ANGRY = "angry"              # 生气
    NEUTRAL = "neutral"          # 中性


@dataclass
class EmotionResult:
    """情绪识别结果"""
    emotion: str
    intensity: float  # 0-1
    keywords: List[str]
    suggestion: str


# 情绪关键词
EMOTION_KEYWORDS = {
    EmotionType.FRUSTRATED: [
        "太慢", "不行", "没用", "烦", "讨厌",
        "算了", "算了算了", "够了", "怎么会这样",
        "搞不定", "总是错", "一点都不好"
    ],
    EmotionType.IMPATIENT: [
        "快点", "怎么还没", "等不及", "太久了",
        "能不能快点", "快点啊", "都等半天了",
        "怎么这么慢", "能不能效率点"
    ],
    EmotionType.CONFUSED: [
        "不懂", "什么意思", "怎么用", "不理解",
        "不明白", "什么情况", "啥意思",
        "哪个", "怎么操作"
    ],
    EmotionType.SATISFIED: [
        "好的", "不错", "可以", "厉害",
        "很棒", "太好了", "感谢", "满意",
        "不错不错", "挺好"
    ],
    EmotionType.ANGRY: [
        "垃圾", "太差", "废物", "滚",
        "蠢", "傻", "烂", "怒了"
    ],
}


# 情绪对应的需求
EMOTION_NEEDS = {
    EmotionType.FRUSTRATED: [
        "需要简化步骤",
        "需要更清晰的指导",
        "需要提供替代方案",
        "需要道歉和安抚"
    ],
    EmotionType.IMPATIENT: [
        "需要更快的响应",
        "需要提供快捷操作",
        "需要减少步骤"
    ],
    EmotionType.CONFUSED: [
        "需要更多解释",
        "需要提供示例",
        "需要分步指导"
    ],
    EmotionType.SATISFIED: [
        "继续保持",
        "可以推荐相关功能"
    ],
    EmotionType.ANGRY: [
        "需要立即道歉",
        "需要人工客服",
        "需要紧急修复"
    ],
}


# 情绪回复建议
EMOTION_SUGGESTIONS = {
    EmotionType.FRUSTRATED: "抱歉给您带来不便，让我简化这个过程。",
    EmotionType.IMPATIENT: "我理解您很着急，马上为您处理。",
    EmotionType.CONFUSED: "让我详细解释一下...",
    EmotionType.SATISFIED: "很高兴能帮到您！",
    EmotionType.ANGRY: "非常抱歉，我会立即解决您的问题。",
    EmotionType.NEUTRAL: "",
}


class EmotionRecognizer:
    """情绪识别器"""
    
    def __init__(self):
        self.emotions = EMOTION_KEYWORDS.copy()
        self.needs = EMOTION_NEEDS.copy()
        self.suggestions = EMOTION_SUGGESTIONS.copy()
    
    def recognize(self, text: str) -> EmotionResult:
        """
        识别情绪
        
        Args:
            text: 用户输入文本
            
        Returns:
            EmotionResult: 情绪识别结果
        """
        text_lower = text.lower()
        
        found_emotions = []
        
        # 查找情绪关键词
        for emotion_type, keywords in self.emotions.items():
            matches = [kw for kw in keywords if kw in text]
            if matches:
                found_emotions.append({
                    "emotion": emotion_type.value,
                    "count": len(matches),
                    "keywords": matches
                })
        
        if not found_emotions:
            return EmotionResult(
                emotion=EmotionType.NEUTRAL.value,
                intensity=0.0,
                keywords=[],
                suggestion=self.suggestions[EmotionType.NEUTRAL]
            )
        
        # 选择最匹配的情绪
        best_match = max(found_emotions, key=lambda x: x["count"])
        
        # 计算强度
        intensity = min(1.0, len(best_match["keywords"]) * 0.3)
        
        return EmotionResult(
            emotion=best_match["emotion"],
            intensity=intensity,
            keywords=best_match["keywords"],
            suggestion=self.suggestions.get(
                EmotionType(best_match["emotion"]),
                ""
            )
        )
    
    def get_implied_needs(self, text: str) -> List[str]:
        """获取隐含需求"""
        result = self.recognize(text)
        
        emotion = EmotionType(result.emotion)
        
        if emotion in self.needs:
            return self.needs[emotion]
        
        return []
    
    def get_suggestion(self, text: str) -> str:
        """获取回复建议"""
        result = self.recognize(text)
        return result.suggestion
    
    def adjust_response_strategy(self, text: str) -> Dict:
        """调整回复策略"""
        result = self.recognize(text)
        
        strategy = {
            "tone": "sympathetic",  # 语气
            "speed_emphasis": False,  # 强调速度
            "provide_examples": False,  # 提供示例
            "offer_alternatives": False,  # 提供替代方案
            "need_apology": False,  # 需要道歉
        }
        
        if result.emotion == EmotionType.FRUSTRATED.value:
            strategy["tone"] = "sympathetic"
            strategy["provide_examples"] = True
            strategy["offer_alternatives"] = True
            strategy["need_apology"] = True
        
        elif result.emotion == EmotionType.IMPATIENT.value:
            strategy["tone"] = "urgent"
            strategy["speed_emphasis"] = True
        
        elif result.emotion == EmotionType.CONFUSED.value:
            strategy["tone"] = "patient"
            strategy["provide_examples"] = True
        
        elif result.emotion == EmotionType.ANGRY.value:
            strategy["tone"] = "apologetic"
            strategy["need_apology"] = True
        
        return strategy
    
    def add_custom_emotion(
        self,
        emotion_type: EmotionType,
        keywords: List[str],
        needs: List[str] = None
    ):
        """添加自定义情绪"""
        self.emotions[emotion_type] = keywords
        if needs:
            self.needs[emotion_type] = needs
    
    def get_stats(self) -> Dict:
        """获取统计"""
        return {
            "emotion_count": len(self.emotions),
            "emotions": list(self.emotions.keys())
        }


# 测试
if __name__ == "__main__":
    recognizer = EmotionRecognizer()
    
    tests = [
        "太慢了，等了这么久还没好",
        "什么意思？我听不懂",
        "不错，挺好用的",
        "能不能快点啊，急死了",
        "太差了，根本不行"
    ]
    
    for text in tests:
        result = recognizer.recognize(text)
        needs = recognizer.get_implied_needs(text)
        strategy = recognizer.adjust_response_strategy(text)
        
        print(f"输入: {text}")
        print(f"情绪: {result.emotion} ({result.intensity:.0%})")
        print(f"关键词: {result.keywords}")
        print(f"建议: {result.suggestion}")
        print(f"隐含需求: {needs}")
        print(f"策略: {strategy}")
        print()
