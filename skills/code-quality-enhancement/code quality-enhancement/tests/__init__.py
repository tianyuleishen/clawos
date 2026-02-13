# 🦞 Code Quality Enhancement Tests

"""
测试用例
"""

import asyncio
from code_quality import CodeQualityEnhancer


def test_code_review():
    """测试代码审查"""
    from code_quality.code_reviewer import CodeReviewer
    
    reviewer = CodeReviewer()
    
    bad_code = """
password = "secret123"
eval("print('hello')")
for i in range(len(items)):
    print(items[i])
    """
    
    result = reviewer.review_code(bad_code)
    
    assert result.score < 100, "应该有错误"
    assert result.summary["total"] > 0, "应该有发现问题"
    
    print("✅ 代码审查测试通过")


def test_best_practice():
    """测试最佳实践检查"""
    from code_quality.best_practice import BestPracticeChecker
    
    checker = BestPracticeChecker()
    
    bad_code = """
def BadFunction(x):
    if x == True:
        return True
    except:
        pass
    """
    
    violations = checker.check_content(bad_code)
    
    assert len(violations) > 0, "应该有违规"
    
    print("✅ 最佳实践检查测试通过")


def test_error_handler():
    """测试错误处理"""
    from code_quality.error_handler import ErrorHandler
    
    handler = ErrorHandler()
    
    suggestions = handler.analyze_error("IndexError: list index out of range")
    
    assert len(suggestions) > 0, "应该有建议"
    assert suggestions[0].error_type == "IndexError"
    
    print("✅ 错误处理测试通过")


def test_performance():
    """测试性能优化"""
    from code_quality.performance_optimizer import PerformanceOptimizer
    
    optimizer = PerformanceOptimizer()
    
    code = "for i in range(len(items)): print(items[i])"
    
    problems = optimizer.analyze_code(code)
    
    assert len(problems) > 0, "应该有性能问题"
    
    print("✅ 性能优化测试通过")


async def test_enhancer():
    """测试综合增强器"""
    enhancer = CodeQualityEnhancer()
    
    code = """
def bad_example(items):
    if items == True:
        return True
    for i in range(len(items)):
        print(items[i])
    keys = list(my_dict.keys())
    return items
    """
    
    result = await enhancer.analyze_code(code)
    
    assert isinstance(result.overall_score, float)
    assert result.summary["total_issues"] > 0
    
    print("✅ 综合增强器测试通过")
    
    # 打印统计
    stats = enhancer.get_stats()
    print(f"📊 统计: {list(stats.keys())}")


def run_all_tests():
    """运行所有测试"""
    print("🦞 运行代码质量提升技能测试...\n")
    
    test_code_review()
    test_best_practice()
    test_error_handler()
    test_performance()
    asyncio.run(test_enhancer())
    
    print("\n✅ 所有测试通过!")


if __name__ == "__main__":
    run_all_tests()
