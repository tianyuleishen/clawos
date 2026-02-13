# 🦞 Best Practice Checker - 最佳实践检查

"""
最佳实践检查模块

功能:
- PEP 8规范检查
- 编码规范
- 设计模式
- 文档规范
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
import re


class PracticeCategory(Enum):
    """实践类别"""
    CODING_STYLE = "coding_style"
    DOCUMENTATION = "documentation"
    ERROR_HANDLING = "error_handling"
    TESTING = "testing"
    DESIGN = "design"
    SECURITY = "security"
    PERFORMANCE = "performance"


@dataclass
class PracticeRule:
    """实践规则"""
    id: str
    category: str
    name: str
    description: str
    pattern: str = ""
    example_good: str = ""
    example_bad: str = ""
    reference: str = ""


class BestPracticeChecker:
    """最佳实践检查器"""
    
    # Python编码规范
    CODING_RULES = [
        PracticeRule(
            id="PEP8-001",
            category=PracticeCategory.CODING_STYLE.value,
            name="缩进使用4个空格",
            description="Python使用4个空格缩进",
            pattern=r"^\t| \t|    {5,}",
            reference="https://peps.python.org/pep-0008/#indentation"
        ),
        PracticeRule(
            id="PEP8-002",
            category=PracticeCategory.CODING_STYLE.value,
            name="行长度限制",
            description="代码行不应超过79字符",
            pattern=r".{80,}",
            reference="https://peps.python.org/pep-0008/#maximum-line-length"
        ),
        PracticeRule(
            id="PEP8-003",
            category=PracticeCategory.CODING_STYLE.value,
            name="类名使用CapWords",
            description="类名应使用CapWords命名法",
            pattern=r"^class\s+[a-z_]",
            reference="https://peps.python.org/pep-0008/#class-names"
        ),
        PracticeRule(
            id="PEP8-004",
            category=PracticeCategory.CODING_STYLE.value,
            name="函数名使用小写下划线",
            description="函数名应使用小写下划线",
            pattern=r"^def\s+[A-Z]",
            reference="https://peps.python.org/pep-0008/#function-and-method-names"
        ),
        PracticeRule(
            id="PEP8-005",
            category=PracticeCategory.CODING_STYLE.value,
            name="常量使用大写下划线",
            description="常量应使用全大写下划线",
            pattern=r"^[A-Z][a-z]",
            example_good="MAX_SIZE = 100",
            example_bad="MaxSize = 100",
            reference="https://peps.python.org/pep-0008/#constants"
        ),
        PracticeRule(
            id="DOC-001",
            category=PracticeCategory.DOCUMENTATION.value,
            name="模块文档字符串",
            description="每个模块应有文档字符串",
            pattern=r"^\"\"\"(?!\s*$)",
            example_good="\"\"\"This is a module docstring.\"\"\"",
            example_bad="",
            reference="https://peps.python.org/pep-0257/"
        ),
        PracticeRule(
            id="DOC-002",
            category=PracticeCategory.DOCUMENTATION.value,
            name="函数文档字符串",
            description="公共函数应有文档字符串",
            pattern=r"def \w+\([^)]*\):(?!\s*\"\"\")",
            reference="https://peps.python.org/pep-0257/"
        ),
    ]
    
    # 错误处理规范
    ERROR_RULES = [
        PracticeRule(
            id="ERR-001",
            category=PracticeCategory.ERROR_HANDLING.value,
            name="避免裸露的except",
            description="except块应有具体异常类型",
            pattern=r"except\s*:",
            example_good="except ValueError as e:",
            example_bad="except:",
            reference="https://docs.python.org/3/tutorial/errors.html"
        ),
        PracticeRule(
            id="ERR-002",
            category=PracticeCategory.ERROR_HANDLING.value,
            name="不要用pass忽略异常",
            description="至少记录日志或重新抛出",
            pattern=r"except.*:\s*\n\s+pass",
            example_good="except Exception as e: logger.error(e)",
            reference=""
        ),
        PracticeRule(
            id="ERR-003",
            category=PracticeCategory.ERROR_HANDLING.value,
            name="优先使用特定异常",
            description="使用具体的异常类型而非通用Exception",
            pattern=r"except\s+Exception\s*:",
            reference=""
        ),
    ]
    
    # 测试规范
    TEST_RULES = [
        PracticeRule(
            id="TEST-001",
            category=PracticeCategory.TESTING.value,
            name="测试文件以test_开头",
            description="测试文件应命名为test_*.py",
            pattern=r"^def test_",
            reference="https://docs.python.org/3/library/unittest.html"
        ),
        PracticeRule(
            id="TEST-002",
            category=PracticeCategory.TESTING.value,
            name="使用断言而非print",
            description="测试应使用assert而非print",
            pattern=r"print\(",
            reference=""
        ),
    ]
    
    # 设计规范
    DESIGN_RULES = [
        PracticeRule(
            id="DESIGN-001",
            category=PracticeCategory.DESIGN.value,
            name="函数参数不宜过多",
            description="函数参数超过5个应考虑重构",
            pattern=r"def\s+\w+\([^)]{50,}\):",
            reference=""
        ),
        PracticeRule(
            id="DESIGN-002",
            category=PracticeCategory.DESIGN.value,
            name="避免过深嵌套",
            description="嵌套层数不应超过3层",
            pattern=r"if.*:\s*\n.*if.*:\s*\n.*if.*:",
            reference=""
        ),
        PracticeRule(
            id="DESIGN-003",
            category=PracticeCategory.DESIGN.value,
            name="遵循单一职责原则",
            description="每个函数应只做一件事",
            pattern=r"def\s+\w+.*(?:and|or|;)",
            reference=""
        ),
    ]
    
    def __init__(self):
        self.rules = []
        for rules in [self.CODING_RULES, self.ERROR_RULES, 
                      self.TEST_RULES, self.DESIGN_RULES]:
            self.rules.extend(rules)
        
        self.violations = []
    
    def check_file(self, file_path: str) -> List[Dict]:
        """检查文件
        
        Args:
            file_path: 文件路径
            
        Returns:
            违规列表
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return self.check_content(content)
    
    def check_content(self, content: str) -> List[Dict]:
        """检查代码内容
        
        Args:
            content: 代码内容
            
        Returns:
            违规列表
        """
        violations = []
        lines = content.split('\n')
        
        for rule in self.rules:
            for line_num, line in enumerate(lines, 1):
                if re.search(rule.pattern, line):
                    violations.append({
                        "line": line_num,
                        "rule_id": rule.id,
                        "category": rule.category,
                        "name": rule.name,
                        "description": rule.description,
                        "code": line.strip(),
                        "suggestion": rule.example_good or rule.description,
                        "reference": rule.reference
                    })
                    self.violations.append({
                        "rule_id": rule.id,
                        "line": line_num
                    })
        
        return violations
    
    def get_report(self, violations: List[Dict]) -> Dict:
        """生成报告
        
        Args:
            violations: 违规列表
            
        Returns:
            报告
        """
        by_category = {}
        by_rule = {}
        
        for v in violations:
            cat = v["category"]
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(v)
            
            rule = v["rule_id"]
            if rule not in by_rule:
                by_rule[rule] = 0
            by_rule[rule] += 1
        
        return {
            "total_violations": len(violations),
            "by_category": {k: len(v) for k, v in by_category.items()},
            "top_rules": sorted(by_rule.items(), key=lambda x: -x[1])[:5],
            "violations": violations
        }
    
    def get_stats(self) -> Dict:
        """获取统计"""
        return {
            "total_rules": len(self.rules),
            "categories": len(set(r.category for r in self.rules)),
            "violations_found": len(self.violations)
        }


# 测试
if __name__ == "__main__":
    checker = BestPracticeChecker()
    
    bad_code = """
def BadFunction(x):
    if x == True:
        return True
    except:
        pass
    """
    
    violations = checker.check_content(bad_code)
    report = checker.get_report(violations)
    
    print(f"违规数: {report['total_violations']}")
    print(f"按类别: {report['by_category']}")
    print(f"\n违规详情:")
    for v in violations:
        print(f"  [{v['line']}] {v['name']}: {v['code']}")
