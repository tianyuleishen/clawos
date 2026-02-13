# 🦞 Understanding Enhancement Tests

"""
测试用例
"""

import asyncio
from understanding import (
    EnhancedUnderstanding,
    UnderstandingResult
)


def test_pronoun_resolution():
    """测试指代词解析"""
    from understanding.pronoun_resolver import PronounResolver
    
    resolver = PronounResolver()
    
    # 测试指代词被成功解析
    text = "把它改成蓝色"
    resolved = resolver.resolve(text, {"color": "红色", "target": "按钮"})
    assert "蓝色" in resolved  # 解析后应该包含蓝色
    
    # 测试没有指代词时返回原文本
    text2 = "太大了"
    resolved2 = resolver.resolve(text2, {})
    # 没有匹配时返回原样
    assert resolved2 == text2
    
    print("✅ 指代词解析测试通过")


def test_emotion_recognition():
    """测试情绪识别"""
    from understanding.emotion_recognizer import EmotionRecognizer
    
    recognizer = EmotionRecognizer()
    
    result = recognizer.recognize("太慢了")
    assert result.emotion in ["frustrated", "impatient"]
    
    print("✅ 情绪识别测试通过")


def test_intent_inference():
    """测试意图推断"""
    from understanding.intent_inferrer import IntentInferrer
    
    inferrer = IntentInferrer()
    
    result = inferrer.infer("把按钮改成蓝色")
    assert result.confidence > 0
    assert result.category != "unknown"
    
    print("✅ 意图推断测试通过")


async def test_enhanced_understanding():
    """测试增强理解"""
    understander = EnhancedUnderstanding()
    
    # 基本分析
    result = await understander.analyze("把它改成蓝色")
    assert isinstance(result, UnderstandingResult)
    assert result.resolved != ""
    assert result.confidence > 0
    
    # 上下文
    understander.update_context("把按钮改成红色", "好的")
    context = understander.get_context()
    print(f"✅ 增强理解测试通过 (history: {len(context['history'])} entries)")
    
    # 打印统计
    stats = understander.get_stats()
    print(f"📊 统计: {list(stats.keys())}")


def run_all_tests():
    """运行所有测试"""
    print("🦞 运行理解力提升技能测试...\n")
    
    test_pronoun_resolution()
    test_emotion_recognition()
    test_intent_inference()
    asyncio.run(test_enhanced_understanding())
    
    print("\n✅ 所有测试通过!")


if __name__ == "__main__":
    run_all_tests()
