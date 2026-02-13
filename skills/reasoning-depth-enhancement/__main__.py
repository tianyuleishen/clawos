#!/usr/bin/env python3
# 🦞 Reasoning Depth Enhancement - Main Entry

"""
运行测试或使用推理深度提升功能
"""

import sys
sys.path.insert(0, '.')

import asyncio


def main():
    """主入口"""
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        from tests import run_all_tests
        run_all_tests()
    else:
        print("🦞 Reasoning Depth Enhancement - 推理深度提升")
        print("=" * 50)
        print("用法:")
        print("  python -m reasoning_depth              # 交互模式")
        print("  python -m reasoning_depth --test    # 运行测试")
        print()
        
        # 简单演示
        from reasoning_depth.enhanced_fusion import EnhancedFusionEngine
        
        async def demo():
            engine = EnhancedFusionEngine()
            
            examples = [
                "如果A大于B，B大于C，那么A大于C吗？",
                "因为下雨，所以地湿了",
                "假如地球是方的，会怎样？",
                "努力学习的步骤是什么？",
            ]
            
            for q in examples:
                result = await engine.analyze(q)
                print(f"\n📝 问题: {q}")
                print(f"   类型: {result.task_type}")
                print(f"   引擎: {result.engine_used}")
                print(f"   结果: {result.result}")
                print(f"   置信度: {result.confidence:.0%}")
                if result.depth > 0:
                    print(f"   深度: {result.depth}")
        
        asyncio.run(demo())


if __name__ == "__main__":
    main()
