# 🦞 Code Reviewer - 代码审查

"""
代码审查模块

功能:
- 检查代码问题
- 识别代码异味
- 生成改进建议
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
import re


class IssueSeverity(Enum):
    """问题严重级别"""
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"
    SUGGESTION = "suggestion"


class IssueType(Enum):
    """问题类型"""
    SYNTAX = "syntax"
    STYLE = "style"
    PERFORMANCE = "performance"
    SECURITY = "security"
    BUG_RISK = "bug_risk"
    MAINTAINABILITY = "maintainability"
    READABILITY = "readability"


@dataclass
class Issue:
    """代码问题"""
    line: int
    column: int
    severity: str
    issue_type: str
    message: str
    code: str
    suggestion: str
    rule_id: str = ""


@dataclass
class ReviewResult:
    """审查结果"""
    file_path: str
    issues: List[Issue] = field(default_factory=list)
    score: float = 100.0
    summary: Dict = field(default_factory=dict)
    suggestions: List[str] = field(default_factory=list)


class CodeReviewer:
    """代码审查器"""
    
    # 代码异味模式
    CODE_SMELLS = {
        IssueType.PERFORMANCE: [
            (r"for .* in range\(len\(", "使用enumerate()代替range(len())"),
            (r"\.append\(.*\.append\(", "避免嵌套append"),
            (r"list\(dict\.keys\(\)", "直接使用dict.keys()"),
            (r"\+\s*\"", "使用f-string或join"),
            (r"while True.*break", "考虑使用迭代器模式"),
        ],
        IssueType.READABILITY: [
            (r"if .* == True", "直接使用if x"),
            (r"if .* == False", "直接使用if not x"),
            (r"and .* and .* and .* and", "拆分为多个if"),
            (r"or .* or .* or .* or", "拆分为多个if"),
            (r"variable\s*=\s*\d+", "使用有意义的变量名"),
        ],
        IssueType.MAINTAINABILITY: [
            (r"function\s*\([^)]*\)", "函数参数过多，考虑拆分"),
            (r"class\s.*\(object\)", "可以省略(object)"),
            (r"try:.*except:.*pass", "不要用空的except块"),
            (r"print\(", "使用日志代替print"),
            (r"# TODO.*$", "处理TODO注释"),
        ],
        IssueType.SECURITY: [
            (r"eval\(", "避免使用eval()"),
            (r"exec\(", "避免使用exec()"),
            (r"os\.system\(", "使用subprocess代替"),
            (r"pickle\.load", "pickle不安全，考虑其他方案"),
            (r"password\s*=\s*[\"'][^\"']+[\"']", "不要硬编码密码"),
            (r"api[_-]?key\s*=\s*[\"'][^\"']+[\"']", "不要硬编码API密钥"),
        ],
        IssueType.BUG_RISK: [
            (r"is\s*==", "使用==而不是is比较"),
            (r"\[-0\]", "可能是笔误，应该是[0]或[:-1]"),
            (r"defaultdict\(dict\)", "应该用defaultdict(list)"),
            (r"for\s+.*:\s*\n\s+for\s+.*:", "嵌套循环，考虑优化"),
            (r"if.*:.*return.*\n.*if.*:.*return", "考虑使用字典映射"),
        ],
    }
    
    # 最佳实践规则
    BEST_PRACTICES = [
        {
            "id": "BP001",
            "message": "使用类型注解",
            "pattern": r"def \w+\([^)]*\):",
            "severity": IssueSeverity.INFO,
            "suggestion": "添加类型注解: def func(x: int) -> str:"
        },
        {
            "id": "BP002",
            "message": "使用上下文管理器",
            "pattern": r"open\([^)]*\)(?!\s*with)",
            "severity": IssueSeverity.WARNING,
            "suggestion": "使用with语句: with open() as f:"
        },
        {
            "id": "BP003",
            "message": "使用列表推导式",
            "pattern": r"for\s+\w+\s+in\s+.*:\s*\n\s+\w+\.append\(",
            "severity": IssueSeverity.SUGGESTION,
            "suggestion": "使用列表推导式: [f(x) for x in ...]"
        },
        {
            "id": "BP004",
            "message": "使用生成器",
            "pattern": r"return\s*\[.*for.*in.*\]",
            "severity": IssueSeverity.SUGGESTION,
            "suggestion": "考虑使用生成器: (x for x in ...)"
        },
        {
            "id": "BP005",
            "message": "添加文档字符串",
            "pattern": r"def \w+\([^)]*\):\n(?!\s*\"\"\")",
            "severity": IssueSeverity.INFO,
            "suggestion": "添加docstring: \"\"\"函数说明\"\"\""
        },
    ]
    
    def __init__(self):
        self.smells = self.CODE_SMELLS.copy()
        self.rules = self.BEST_PRACTICES.copy()
        self.issues_found = 0
    
    def review_file(self, file_path: str, content: str = None) -> ReviewResult:
        """审查文件
        
        Args:
            file_path: 文件路径
            content: 文件内容（可选，如果未提供则读取文件）
            
        Returns:
            ReviewResult: 审查结果
        """
        if content is None:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        
        result = ReviewResult(file_path=file_path)
        
        # 获取行列表
        lines = content.split('\n')
        
        # 逐行检查
        for line_num, line in enumerate(lines, 1):
            for issue_type, patterns in self.smells.items():
                for pattern, suggestion in patterns:
                    if re.search(pattern, line):
                        issue = Issue(
                            line=line_num,
                            column=self._get_column(line, pattern),
                            severity=self._get_severity(issue_type),
                            issue_type=issue_type.value,
                            message=self._get_message(issue_type, pattern),
                            code=line.strip(),
                            suggestion=suggestion,
                            rule_id=f"SMELL_{issue_type.value.upper()}"
                        )
                        result.issues.append(issue)
                        self.issues_found += 1
        
        # 检查最佳实践
        for rule in self.rules:
            for line_num, line in enumerate(lines, 1):
                if re.search(rule["pattern"], line):
                    issue = Issue(
                        line=line_num,
                        column=line.find(re.search(rule["pattern"], line).group()),
                        severity=rule["severity"].value,
                        issue_type="best_practice",
                        message=rule["message"],
                        code=line.strip(),
                        suggestion=rule["suggestion"],
                        rule_id=rule["id"]
                    )
                    result.issues.append(issue)
        
        # 计算分数
        result.score = self._calculate_score(result.issues)
        
        # 生成摘要
        result.summary = self._generate_summary(result.issues)
        
        # 生成建议
        result.suggestions = self._generate_suggestions(result)
        
        return result
    
    def review_code(self, code: str) -> ReviewResult:
        """审查代码片段
        
        Args:
            code: 代码字符串
            
        Returns:
            ReviewResult: 审查结果
        """
        return self.review_file("inline_code.py", code)
    
    def _get_column(self, line: str, pattern: str) -> int:
        """获取匹配的列号"""
        match = re.search(pattern, line)
        return match.start() if match else 0
    
    def _get_severity(self, issue_type: IssueType) -> str:
        """获取严重级别"""
        severity_map = {
            IssueType.SECURITY: "error",
            IssueType.BUG_RISK: "error",
            IssueType.PERFORMANCE: "warning",
            IssueType.READABILITY: "info",
            IssueType.MAINTAINABILITY: "info",
        }
        return severity_map.get(issue_type, "warning")
    
    def _get_message(self, issue_type: IssueType, pattern: str) -> str:
        """获取问题消息"""
        messages = {
            IssueType.PERFORMANCE: "性能问题",
            IssueType.READABILITY: "可读性问题",
            IssueType.MAINTAINABILITY: "可维护性问题",
            IssueType.SECURITY: "安全问题",
            IssueType.BUG_RISK: "潜在的bug",
        }
        return messages.get(issue_type, "代码问题")
    
    def _calculate_score(self, issues: List[Issue]) -> float:
        """计算代码分数"""
        if not issues:
            return 100.0
        
        score = 100.0
        for issue in issues:
            if issue.severity == "error":
                score -= 5
            elif issue.severity == "warning":
                score -= 2
            else:
                score -= 0.5
        
        return max(0.0, score)
    
    def _generate_summary(self, issues: List[Issue]) -> Dict:
        """生成摘要"""
        summary = {
            "total": len(issues),
            "by_severity": {"error": 0, "warning": 0, "info": 0, "suggestion": 0},
            "by_type": {}
        }
        
        for issue in issues:
            summary["by_severity"][issue.severity] += 1
            
            if issue.issue_type not in summary["by_type"]:
                summary["by_type"][issue.issue_type] = 0
            summary["by_type"][issue.issue_type] += 1
        
        return summary
    
    def _generate_suggestions(self, result: ReviewResult) -> List[str]:
        """生成改进建议"""
        suggestions = []
        
        if result.score < 60:
            suggestions.append("⚠️ 代码质量较低，建议重点关注")
        
        if result.summary["by_severity"].get("error", 0) > 0:
            suggestions.append("🐛 优先修复错误级别的问题")
        
        if result.summary["by_type"].get("security", 0) > 0:
            suggestions.append("🔒 检查安全问题")
        
        if result.summary["by_type"].get("performance", 0) > 0:
            suggestions.append("⚡ 考虑性能优化")
        
        if result.score >= 90:
            suggestions.append("✨ 代码质量很好！")
        
        return suggestions
    
    def get_stats(self) -> Dict:
        """获取统计"""
        return {
            "issues_found": self.issues_found,
            "smell_patterns": len(self.smells),
            "best_practices": len(self.rules)
        }


# 测试
if __name__ == "__main__":
    reviewer = CodeReviewer()
    
    test_code = """
def bad_function(x):
    if x == True:
        return True
    for i in range(len(x)):
        x.append(i)
    return x

password = "secret123"
eval("print('hello')")
    """
    
    result = reviewer.review_code(test_code)
    
    print(f"文件: {result.file_path}")
    print(f"分数: {result.score:.0f}/100")
    print(f"问题数: {result.summary['total']}")
    print(f"\n按严重级别:")
    for severity, count in result.summary['by_severity'].items():
        print(f"  {severity}: {count}")
    
    print(f"\n改进建议:")
    for suggestion in result.suggestions:
        print(f"  {suggestion}")
