# 🦞 Code Quality Enhancement - 代码质量增强

"""
代码质量增强模块

整合:
- 代码审查
- 最佳实践
- 错误处理
- 性能优化
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
import json


@dataclass
class QualityReport:
    """质量报告"""
    timestamp: str
    overall_score: float
    code_score: float
    style_score: float
    performance_score: float
    issues: List[Dict]
    suggestions: List[str]
    summary: Dict


class CodeQualityEnhancer:
    """代码质量增强器"""
    
    def __init__(self):
        # 导入子模块
        from .code_reviewer import CodeReviewer
        from .best_practice import BestPracticeChecker
        from .error_handler import ErrorHandler
        from .performance_optimizer import PerformanceOptimizer
        
        # 初始化组件
        self.code_reviewer = CodeReviewer()
        self.best_practice_checker = BestPracticeChecker()
        self.error_handler = ErrorHandler()
        self.performance_optimizer = PerformanceOptimizer()
        
        print("✅ Code Quality Enhancer 初始化完成")
    
    async def analyze_code(
        self,
        code: str,
        file_path: str = "analyzed.py"
    ) -> QualityReport:
        """分析代码质量
        
        Args:
            code: 代码
            file_path: 文件路径
            
        Returns:
            质量报告
        """
        # 1. 代码审查
        review_result = self.code_reviewer.review_code(code)
        
        # 2. 最佳实践检查
        violations = self.best_practice_checker.check_content(code)
        
        # 3. 性能分析
        perf_problems = self.performance_optimizer.analyze_code(code)
        
        # 整合问题
        issues = []
        
        # 添加审查问题
        for issue in review_result.issues:
            issues.append({
                "source": "review",
                "line": issue.line,
                "severity": issue.severity,
                "type": issue.issue_type,
                "message": issue.message,
                "suggestion": issue.suggestion
            })
        
        # 添加性能问题
        for prob in perf_problems:
            issues.append({
                "source": "performance",
                "line": prob.get("line", 0),
                "severity": "warning",
                "type": "performance",
                "message": prob["issue"],
                "suggestion": prob["explanation"]
            })
        
        # 添加最佳实践违规
        for v in violations:
            issues.append({
                "source": "best_practice",
                "line": v["line"],
                "severity": "info",
                "type": v["category"],
                "message": v["name"],
                "suggestion": v["description"]
            })
        
        # 计算分数
        code_score = review_result.score
        style_score = max(0, 100 - len(violations) * 2)
        perf_score = max(0, 100 - len(perf_problems) * 5)
        
        overall_score = (code_score * 0.4 + 
                         style_score * 0.3 + 
                         perf_score * 0.3)
        
        # 生成建议
        suggestions = []
        if review_result.score < 70:
            suggestions.append("⚠️ 代码质量需要重点改进")
        if len(perf_problems) > 0:
            suggestions.append("⚡ 建议优化性能问题")
        if len(violations) > 0:
            suggestions.append("📝 建议遵循最佳实践")
        if overall_score >= 90:
            suggestions.append("✨ 代码质量优秀！")
        
        return QualityReport(
            timestamp=datetime.now().isoformat(),
            overall_score=overall_score,
            code_score=code_score,
            style_score=style_score,
            performance_score=perf_score,
            issues=issues,
            suggestions=suggestions,
            summary={
                "total_issues": len(issues),
                "by_severity": self._count_by_severity(issues),
                "by_source": {
                    "review": len(review_result.issues),
                    "performance": len(perf_problems),
                    "best_practice": len(violations)
                }
            }
        )
    
    def _count_by_severity(self, issues: List[Dict]) -> Dict[str, int]:
        """按严重级别统计"""
        counts = {"error": 0, "warning": 0, "info": 0, "suggestion": 0}
        for issue in issues:
            severity = issue.get("severity", "info")
            if severity in counts:
                counts[severity] += 1
        return counts
    
    def optimize_code(self, code: str) -> Dict:
        """优化代码
        
        Args:
            code: 原始代码
            
        Returns:
            优化结果
        """
        perf_result = self.performance_optimizer.optimize_code(code)
        
        return {
            "original": code,
            "optimized": perf_result.optimized_code,
            "improvements": perf_result.improvements,
            "speedup": perf_result.speedup
        }
    
    def check_best_practices(self, code: str) -> Dict:
        """检查最佳实践
        
        Args:
            code: 代码
            
        Returns:
            检查结果
        """
        violations = self.best_practice_checker.check_content(code)
        return self.best_practice_checker.get_report(violations)
    
    def handle_error(self, error_message: str) -> List[Dict]:
        """分析错误并提供修复建议
        
        Args:
            error_message: 错误消息
            
        Returns:
            修复建议
        """
        suggestions = self.error_handler.analyze_error(error_message)
        
        return [
            {
                "error_type": s.error_type,
                "suggestion": s.suggestion,
                "explanation": s.explanation,
                "example": s.example_code
            }
            for s in suggestions
        ]
    
    def get_stats(self) -> Dict:
        """获取统计"""
        return {
            "code_reviewer": self.code_reviewer.get_stats(),
            "best_practice": self.best_practice_checker.get_stats(),
            "error_handler": self.error_handler.get_stats(),
            "performance_optimizer": self.performance_optimizer.get_stats()
        }
    
    def generate_report(self, report: QualityReport) -> str:
        """生成Markdown报告
        
        Args:
            report: 质量报告
            
        Returns:
            Markdown格式报告
        """
        lines = [
            "# 📊 代码质量报告",
            f"**时间**: {report.timestamp}",
            "",
            "## 总体评分",
            f"**{report.overall_score:.0f}/100**",
            "",
            "## 详细评分",
            f"- 代码质量: {report.code_score:.0f}/100",
            f"- 代码风格: {report.style_score:.0f}/100",
            f"- 性能: {report.performance_score:.0f}/100",
            "",
            "## 问题统计",
            f"总计: {report.summary['total_issues']} 个问题",
            "",
            "### 按严重级别",
        ]
        
        for severity, count in report.summary['by_severity'].items():
            emoji = {"error": "🔴", "warning": "🟡", "info": "🔵"}.get(severity, "⚪")
            lines.append(f"{emoji} {severity}: {count}")
        
        lines.extend([
            "",
            "## 改进建议"
        ])
        
        for suggestion in report.suggestions:
            lines.append(f"- {suggestion}")
        
        if report.issues:
            lines.extend([
                "",
                "## 问题详情"
            ])
            
            for issue in report.issues[:20]:  # 最多显示20个
                lines.append(
                    f"- [{issue['severity']}] {issue['message']} "
                    f"(第{issue['line']}行)"
                )
        
        return "\n".join(lines)


# 便捷函数
async def analyze(code: str) -> QualityReport:
    """快速分析代码质量"""
    enhancer = CodeQualityEnhancer()
    return await enhancer.analyze_code(code)


# 测试
if __name__ == "__main__":
    import asyncio
    
    async def test():
        enhancer = CodeQualityEnhancer()
        
        test_code = """
def bad_example(items):
    if items == True:
        return True
    for i in range(len(items)):
        print(items[i])
    keys = list(my_dict.keys())
    return items
"""
        
        print("🦞 代码质量分析测试\n")
        
        # 分析
        report = await enhancer.analyze_code(test_code)
        
        print(f"总体评分: {report.overall_score:.0f}/100")
        print(f"代码质量: {report.code_score:.0f}/100")
        print(f"代码风格: {report.style_score:.0f}/100")
        print(f"性能: {report.performance_score:.0f}/100")
        print(f"\n问题数: {report.summary['total_issues']}")
        
        print(f"\n建议:")
        for s in report.suggestions:
            print(f"  {s}")
        
        print(f"\n统计: {enhancer.get_stats()}")
    
    asyncio.run(test())
