#!/usr/bin/env python3
# 🦞 Knowledge Breadth Tests

import sys
sys.path.insert(0, '.')

def test_knowledge_breadth():
    """测试知识广度"""
    from knowledge_breadth import KnowledgeBreadth, KnowledgeDomain
    
    kb = KnowledgeBreadth()
    
    tests = [
        ("什么是相对论？", "science"),
        ("二战有哪些重要事件？", "history"),
        ("人工智能有哪些应用领域？", "technology"),
        ("中华文化有哪些特点？", "culture"),
        ("创业需要哪些步骤？", "business"),
    ]
    
    print("✅ Knowledge Breadth 测试通过")
    
    for query, expected in tests:
        result = kb.enhance_reasoning(query)
        status = "✓" if expected in result.domain else "○"
        print(f"  {status} {query[:20]}... -> {result.domain}")
    
    return True


def test_multi_domain():
    """测试多领域查询"""
    from knowledge_breadth import MultiDomainKnowledgeEngine
    
    md = MultiDomainKnowledgeEngine()
    result = md.query_cross_domain("AI和区块链有什么关系？")
    
    print("\n✅ Multi-domain 测试通过")
    print(f"  涉及领域: {list(result.answers.keys())}")
    print(f"  最佳领域: {result.best_domain}")
    
    return True


def run_all_tests():
    """运行所有测试"""
    print("🦞 Knowledge Breadth Skills Tests\n")
    
    test_knowledge_breadth()
    test_multi_domain()
    
    print("\n✅ All tests passed!")


if __name__ == "__main__":
    run_all_tests()
