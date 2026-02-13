#!/usr/bin/env python3
# 🦞 Understanding Enhancement - Main Entry

"""
运行测试或使用理解力提升功能
"""

import sys
import asyncio


def main():
    """主入口"""
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        # 运行测试
        from tests.test_understanding import run_all_tests
        run_all_tests()
    else:
        # 交互模式
        print("🦞 Understanding Enhancement - 理解力提升")
        print("=" * 50)
        print("用法:")
        print("  python -m understanding              # 交互模式")
        print("  python -m understanding --test       # 运行测试")
        print()
        
        # 简单演示
        from understanding import EnhancedUnderstanding
        
        async def demo():
            understander = EnhancedUnderstanding()
            
            examples = [
                "把它改成蓝色",
                "太慢了，受不了了",
                "怎么使用这个功能？",
                "不错，挺好用的",
                "再试一次"
            ]
            
            for text in examples:
                result = await understander.analyze(text)
                print(f"\n📝 输入: {text}")
                print(f"   解析: {result.resolved}")
                print(f"   意图: {result.intent}")
                print(f"   情绪: {result.emotion}")
                print(f"   置信度: {result.confidence:.0%}")
        
        asyncio.run(demo())


if __name__ == "__main__":
    main()
