#!/usr/bin/env python3
# 🦞 Knowledge Breadth Skill - Main Entry

"""
运行知识广度技能测试
"""

import sys
sys.path.insert(0, '.')


def main():
    """主入口"""
    print("="*60)
    print("🦞 Knowledge Breadth Enhancement Skill")
    print("="*60)
    
    from .knowledge_breadth import KnowledgeBreadth
    
    kb = KnowledgeBreadth()
    
    examples = [
        "什么是相对论？",
        "二战有哪些重要事件？",
        "人工智能有哪些应用领域？",
        "中华文化有哪些特点？",
        "创业的步骤有哪些？",
        "苏格拉底的核心思想是什么？"
    ]
    
    print("\n📚 Knowledge Examples:\n")
    
    for query in examples:
        result = kb.enhance_reasoning(query)
        print(f"Q: {query}")
        print(f"   Domain: {result.domain}")
        print(f"   Confidence: {result.confidence:.0%}")
        print(f"   A: {result.answer[:60]}...")
        print()
    
    print(f"Stats: {kb.get_stats()}")


if __name__ == "__main__":
    main()
