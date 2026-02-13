#!/usr/bin/env python3
# 🦞 Code Quality Enhancement - Main Entry

"""
运行测试或使用代码质量提升功能
"""

import sys
sys.path.insert(0, '.')

import asyncio


def main():
    """主入口"""
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        # 运行测试
        from tests.test_code_quality import run_all_tests
        run_all_tests()
    else:
        # 交互模式
        print("🦞 Code Quality Enhancement - 代码质量提升")
        print("=" * 50)
        print("用法:")
        print("  python -m code_quality              # 交互模式")
        print("  python -m code_quality --test       # 运行测试")
        print()
        
        # 简单演示
        from code_quality.enhanced_code_quality import CodeQualityEnhancer
        
        async def demo():
            enhancer = CodeQualityEnhancer()
            
            examples = [
                """
def bad_example(items):
    if items == True:
        return True
    for i in range(len(items)):
        print(items[i])
                """,
                """
password = "secret123"
eval("dangerous code")
                """,
            ]
            
            for i, code in enumerate(examples, 1):
                print(f"\n📝 示例 {i}:")
                result = await enhancer.analyze_code(code)
                print(f"   评分: {result.overall_score:.0f}/100")
                print(f"   问题: {result.summary['total_issues']} 个")
                for issue in result.issues[:3]:
                    print(f"   - {issue['message']}")
        
        asyncio.run(demo())


if __name__ == "__main__":
    main()
