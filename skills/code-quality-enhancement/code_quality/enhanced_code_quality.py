# 🦞 Code Quality Enhancement - 综合代码质量提升

from typing import Dict, List, Any
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class QualityReport:
    timestamp: str
    overall_score: float
    code_score: float
    style_score: float
    performance_score: float
    issues: List[Dict] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)
    summary: Dict = field(default_factory=dict)

class CodeQualityEnhancer:
    def __init__(self):
        from .code_reviewer import CodeReviewer
        from .best_practice import BestPracticeChecker
        from .error_handler import ErrorHandler
        from .performance_optimizer import PerformanceOptimizer
        
        self.code_reviewer = CodeReviewer()
        self.best_practice_checker = BestPracticeChecker()
        self.error_handler = ErrorHandler()
        self.performance_optimizer = PerformanceOptimizer()
        print("✅ Code Quality Enhancer 初始化完成")
    
    async def analyze_code(self, code: str, file_path: str = "analyzed.py") -> QualityReport:
        review_result = self.code_reviewer.review_code(code)
        perf_problems = self.performance_optimizer.analyze_code(code)
        violations = self.best_practice_checker.check_content(code)
        
        issues = []
        for issue in review_result.issues:
            issues.append({
                "source": "review",
                "line": issue.line,
                "severity": issue.severity,
                "message": issue.message
            })
        for prob in perf_problems:
            issues.append({
                "source": "performance",
                "message": prob["issue"]
            })
        
        code_score = review_result.score
        style_score = max(0, 100 - len(violations) * 2)
        perf_score = max(0, 100 - len(perf_problems) * 5)
        overall = (code_score * 0.4 + style_score * 0.3 + perf_score * 0.3)
        
        suggestions = []
        if overall < 70:
            suggestions.append("⚠️ 代码质量需要改进")
        if perf_problems:
            suggestions.append("⚡ 建议优化性能问题")
        if overall >= 90:
            suggestions.append("✨ 代码质量优秀!")
        
        return QualityReport(
            timestamp=datetime.now().isoformat(),
            overall_score=overall,
            code_score=code_score,
            style_score=style_score,
            performance_score=perf_score,
            issues=issues,
            suggestions=suggestions,
            summary={
                "total_issues": len(issues),
                "by_source": {
                    "review": len(review_result.issues),
                    "performance": len(perf_problems),
                    "best_practice": len(violations)
                }
            }
        )
    
    def get_stats(self) -> Dict:
        return {
            "code_reviewer": self.code_reviewer.get_stats(),
            "best_practice": self.best_practice_checker.get_stats(),
            "error_handler": self.error_handler.get_stats(),
            "performance_optimizer": self.performance_optimizer.get_stats()
        }

if __name__ == "__main__":
    import asyncio
    enhancer = CodeQualityEnhancer()
    code = """
def bad_example(items):
    if items == True:
        return True
    for i in range(len(items)):
        print(items[i])
    """
    result = asyncio.run(enhancer.analyze_code(code))
    print(f"评分: {result.overall_score:.0f}/100")
    print(f"问题: {result.summary['total_issues']}")
