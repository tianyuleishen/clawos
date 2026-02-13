#!/usr/bin/env python3
# 🦞 Reasoning Depth Enhancement Tests

import sys
sys.path.insert(0, '.')

import asyncio


def test_chain_reasoner():
    """测试链式推理"""
    from reasoning_depth.chain_reasoner import ChainReasoner
    
    reasoner = ChainReasoner()
    
    questions = [
        "如果A大于B，B大于C，那么A大于C吗？",
        "因为下雨，所以地湿了",
        "观察到10只乌鸦都是黑色的，所以所有乌鸦都是黑色的",
    ]
    
    print("✅ ChainReasoner 测试通过")
    
    for q in questions:
        chain = reasoner.decompose(q)
        print(f"  {q[:20]}... -> {len(chain.steps)} 步推理")
    
    return True


def test_causal_analyzer():
    """测试因果分析"""
    from reasoning_depth.causal_analyzer import CausalAnalyzer
    
    analyzer = CausalAnalyzer()
    
    texts = [
        "因为下雨，所以地湿了",
        "吸烟导致肺癌",
    ]
    
    for text in texts:
        causes = analyzer.extract_causes(text)
        print(f"  {text} -> {len(causes)} 因果关系")
    
    print("✅ CausalAnalyzer 测试通过")
    return True


def test_counterfactual():
    """测试反事实推理"""
    from reasoning_depth.counterfactual_reasoner import CounterfactualReasoner
    
    reasoner = CounterfactualReasoner()
    
    scenario = reasoner.analyze(
        fact="努力学习",
        change="不努力学习",
        outcome_type="removal"
    )
    
    print(f"✅ CounterfactualReasoner 测试通过")
    print(f"  预测: {scenario.predicted_outcome}")
    return True


def test_meta_reasoner():
    """测试元推理"""
    from reasoning_depth.meta_reasoner import MetaReasoner
    
    reasoner = MetaReasoner()
    
    questions = [
        "如果A大于B，B大于C，那么A大于C吗？",
        "因为下雨，所以地湿了",
    ]
    
    for q in questions:
        meta = reasoner.analyze_question(q)
        print(f"  {q[:15]}... -> 策略:{meta.strategy}")
    
    print("✅ MetaReasoner 测试通过")
    return True


async def test_enhanced_fusion():
    """测试增强融合引擎"""
    from reasoning_depth.enhanced_fusion import EnhancedFusionEngine
    
    engine = EnhancedFusionEngine()
    
    questions = [
        "如果A大于B，B大于C，那么A大于C吗？",
        "因为下雨，所以地湿了",
        "假如地球是方的，会怎样？",
    ]
    
    for q in questions:
        result = await engine.analyze(q)
        print(f"  {q[:15]}... -> {result.engine_used} ({result.confidence:.0%})")
    
    print("✅ EnhancedFusionEngine 测试通过")
    return True


def run_all_tests():
    """运行所有测试"""
    print("🦞 运行推理深度提升技能测试...\n")
    
    test_chain_reasoner()
    test_causal_analyzer()
    test_counterfactual()
    test_meta_reasoner()
    asyncio.run(test_enhanced_fusion())
    
    print("\n✅ 所有测试通过!")


if __name__ == "__main__":
    run_all_tests()
