# 🦞 Enhanced Understanding - 增强理解

"""
增强理解模块

整合:
- 指代词解析
- 上下文记忆
- 情绪识别
- 意图推断
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
import json


@dataclass
class UnderstandingResult:
    """理解结果"""
    surface: str                    # 表面文本
    resolved: str                    # 解析后的文本
    intent: str                      # 意图类别
    action: str                      # 具体动作
    target: str                     # 目标对象
    emotion: str                    # 情绪
    emotion_intensity: float        # 情绪强度
    implied_needs: List[str]        # 隐含需求
    confidence: float               # 置信度
    context: Dict                   # 上下文
    suggestions: List[str]          # 建议
    raw_result: Dict = field(default_factory=dict)  # 原始结果
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "surface": self.surface,
            "resolved": self.resolved,
            "intent": self.intent,
            "action": self.action,
            "target": self.target,
            "emotion": self.emotion,
            "emotion_intensity": self.emotion_intensity,
            "implied_needs": self.implied_needs,
            "confidence": self.confidence,
            "context": self.context,
            "suggestions": self.suggestions
        }
    
    def to_json(self) -> str:
        """转换为JSON"""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)
    
    def __str__(self) -> str:
        return f"UnderstandingResult(intent={self.intent}, emotion={self.emotion}, confidence={self.confidence:.0%})"


class EnhancedUnderstanding:
    """增强理解器"""
    
    def __init__(self, window_size: int = 5):
        """
        初始化
        
        Args:
            window_size: 上下文窗口大小
        """
        # 导入子模块
        from .pronoun_resolver import PronounResolver
        from .context_tracker import ContextTracker
        from .emotion_recognizer import EmotionRecognizer
        from .intent_inferrer import IntentInferrer
        
        # 初始化组件
        self.pronoun_resolver = PronounResolver()
        self.context_tracker = ContextTracker(window_size=window_size)
        self.emotion_recognizer = EmotionRecognizer()
        self.intent_inferrer = IntentInferrer()
        
        print("✅ Enhanced Understanding 初始化完成")
    
    async def analyze(
        self,
        text: str,
        context: Dict = None,
        remember: bool = True
    ) -> UnderstandingResult:
        """
        分析输入
        
        Args:
            text: 用户输入
            context: 外部上下文（可选）
            remember: 是否记录到历史
            
        Returns:
            UnderstandingResult: 理解结果
        """
        # 1. 继承上下文（如果需要）
        if self.context_tracker.is_continuation(text):
            inherited = self.context_tracker.inherit_context(text)
            text = inherited["text"]
            context = {**(context or {}), **inherited.get("context", {})}
        
        # 2. 解析指代词
        resolved_text = self.pronoun_resolver.resolve(text, context)
        
        # 3. 识别情绪
        emotion_result = self.emotion_recognizer.recognize(resolved_text)
        
        # 4. 推断意图
        intent_result = self.intent_inferrer.infer(resolved_text)
        
        # 5. 获取上下文
        ctx = self.context_tracker.get_context()
        if context:
            ctx["external"] = context
        
        # 6. 整合结果
        result = UnderstandingResult(
            surface=text,
            resolved=resolved_text,
            intent=intent_result.category,
            action=intent_result.action,
            target=intent_result.target,
            emotion=emotion_result.emotion,
            emotion_intensity=emotion_result.intensity,
            implied_needs=intent_result.implied_needs,
            confidence=intent_result.confidence,
            context=ctx,
            suggestions=intent_result.suggestions,
            raw_result={
                "pronoun": self.pronoun_resolver.resolve_detailed(text, context),
                "emotion": emotion_result,
                "intent": intent_result
            }
        )
        
        # 7. 记录到历史（如果需要）
        if remember:
            self.context_tracker.update(
                user_input=text,
                system_response="",  # 还没有回复
                entities={
                    "intent": intent_result.category,
                    "action": intent_result.action,
                    "target": intent_result.target
                },
                topic=intent_result.category
            )
        
        return result
    
    def update_context(
        self,
        user_input: str,
        system_response: str,
        entities: Dict = None
    ):
        """更新上下文（记录对话）"""
        self.context_tracker.update(
            user_input=user_input,
            system_response=system_response,
            entities=entities
        )
    
    def get_context(self) -> Dict:
        """获取当前上下文"""
        return self.context_tracker.get_context()
    
    def clear_context(self):
        """清空上下文"""
        self.context_tracker.clear()
    
    def set_window_size(self, size: int):
        """设置上下文窗口大小"""
        self.context_tracker.window_size = size
    
    def get_stats(self) -> Dict:
        """获取统计"""
        return {
            "pronoun_resolver": self.pronoun_resolver.get_stats(),
            "context_tracker": self.context_tracker.get_stats(),
            "emotion_recognizer": self.emotion_recognizer.get_stats(),
            "intent_inferrer": self.intent_inferrer.get_stats()
        }


# 便捷函数
async def understand(
    text: str,
    context: Dict = None
) -> UnderstandingResult:
    """快速理解"""
    understander = EnhancedUnderstanding()
    return await understander.analyze(text, context)


# 测试
if __name__ == "__main__":
    import asyncio
    
    async def test():
        understander = EnhancedUnderstanding()
        
        # 测试用例
        tests = [
            "把它改成蓝色",
            "太大了，受不了了",
            "怎么使用这个功能？",
            "不错，挺好用的",
            "再试一次"
        ]
        
        for text in tests:
            result = await understander.analyze(text)
            
            print(f"\n{'='*50}")
            print(f"原文: {text}")
            print(f"解析: {result.resolved}")
            print(f"意图: {result.intent} -> {result.action} {result.target}")
            print(f"情绪: {result.emotion} ({result.emotion_intensity:.0%})")
            print(f"需求: {result.implied_needs}")
            print(f"置信度: {result.confidence:.0%}")
            print(f"上下文: {len(result.context.get('history', []))} 轮")
            
            # 如果是延续，测试继承
            if understander.context_tracker.is_continuation(text):
                inherited = understander.context_tracker.inherit_context(text)
                print(f"继承后: {inherited['text']}")
    
    asyncio.run(test())
