# 🦞 Performance Optimizer - 性能优化

"""
性能优化模块

功能:
- 识别性能问题
- 优化代码结构
- 提供最佳实践
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
import re


@dataclass
class OptimizationResult:
    """优化结果"""
    original_code: str
    optimized_code: str
    improvements: List[str]
    speedup: str
    lines_changed: int


class PerformanceOptimizer:
    """性能优化器"""
    
    # 常见性能问题模式
    PERFORMANCE_ISSUES = [
        {
            "id": "PERF-001",
            "issue": "使用range(len())遍历",
            "pattern": r"for\s+i\s+in\s+range\(len\(",
            "explanation": "使用enumerate()更高效",
            "example_bad": "for i in range(len(items)): print(items[i])",
            "example_good": "for i, item in enumerate(items): print(item)",
            "speedup": "~2-3x"
        },
        {
            "id": "PERF-002",
            "issue": "字符串拼接使用+",
            "pattern": r"\+\s*(?!\s*[\"'\n])",
            "explanation": "使用join()或f-string",
            "example_bad": "result = \"a\" + \"b\" + \"c\"",
            "example_good": "result = \"\".join([\"a\", \"b\", \"c\"])",
            "speedup": "~5-10x"
        },
        {
            "id": "PERF-003",
            "issue": "在循环中重复计算",
            "pattern": r"for\s+.*:\s*\n\s*len\(",
            "explanation": "将计算移到循环外",
            "example_bad": "for i in range(1000): print(len(items))",
            "example_good": "length = len(items)\nfor i in range(1000): print(length)",
            "speedup": "~Nx (N为循环次数)"
        },
        {
            "id": "PERF-004",
            "issue": "重复调用函数",
            "pattern": r"\.append\(.*\.append\(",
            "explanation": "使用extend()或+=代替嵌套append",
            "example_bad": "for x in lists: result.append(x)",
            "example_good": "result = []\nfor x in lists: result.extend(x)",
            "speedup": "~2x"
        },
        {
            "id": "PERF-005",
            "issue": "使用list()转换生成器",
            "pattern": r"list\([^)]*for.*in",
            "explanation": "直接使用列表推导式",
            "example_bad": "list(x for x in range(100))",
            "example_good": "[x for x in range(100)]",
            "speedup": "~1.5x"
        },
        {
            "id": "PERF-006",
            "issue": "使用字典keys()创建列表",
            "pattern": r"list\(dict\.keys\(\)\)",
            "explanation": "直接使用list(dict)或dict.keys()",
            "example_bad": "keys = list(my_dict.keys())",
            "example_good": "keys = list(my_dict)",
            "speedup": "~2x"
        },
        {
            "id": "PERF-007",
            "issue": "深拷贝大对象",
            "pattern": r"deepcopy\(",
            "explanation": "考虑是否真的需要深拷贝",
            "example_bad": "new_obj = deepcopy(old_obj)",
            "example_good": "new_obj = old_obj.copy()  # 如果只需浅拷贝",
            "speedup": "根据对象大小"
        },
        {
            "id": "PERF-008",
            "issue": "未使用集合成员测试",
            "pattern": r"in\s+\[",
            "explanation": "使用set进行成员测试",
            "example_bad": "if x in [a, b, c]: pass",
            "example_good": "if x in {a, b, c}: pass",
            "speedup": "~10x"
        },
        {
            "id": "PERF-009",
            "issue": "正则表达式重复编译",
            "pattern": r"re\.(search|match|findall)\(",
            "explanation": "预编译正则表达式",
            "example_bad": "re.search(pattern, text)",
            "example_good": "pattern = re.compile(pattern)\npattern.search(text)",
            "speedup": "~5-10x"
        },
        {
            "id": "PERF-010",
            "issue": "使用map而非列表推导式",
            "pattern": r"list\(map\(",
            "explanation": "列表推导式通常更快",
            "example_bad": "list(map(lambda x: x*2, items))",
            "example_good": "[x*2 for x in items]",
            "speedup": "~1.5x"
        },
    ]
    
    # 优化策略
    OPTIMIZATION_STRATEGIES = [
        {
            "strategy": "使用适当的数据结构",
            "description": "选择正确的数据结构可以大幅提升性能",
            "examples": [
                "使用set进行成员测试(O(1) vs O(n))",
                "使用deque进行队列操作(O(1) vs O(n))",
                "使用dict进行快速查找"
            ]
        },
        {
            "strategy": "减少函数调用开销",
            "description": "内联简单函数或使用lambda",
            "examples": [
                "避免在循环中调用小函数",
                "使用本地变量缓存函数引用"
            ]
        },
        {
            "strategy": "惰性计算",
            "description": "只在需要时计算",
            "examples": [
                "使用生成器替代列表",
                "使用itertools进行惰性迭代"
            ]
        },
        {
            "strategy": "缓存重复计算",
            "description": "使用lru_cache或手动缓存",
            "examples": [
                "@lru_cache装饰器",
                "memoization模式"
            ]
        },
        {
            "strategy": "并行处理",
            "description": "利用多核CPU",
            "examples": [
                "multiprocessing模块",
                "concurrent.futures",
                "asyncio异步编程"
            ]
        }
    ]
    
    def __init__(self):
        self.issues = self.PERFORMANCE_ISSUES.copy()
        self.strategies = self.OPTIMIZATION_STRATEGIES.copy()
    
    def analyze_code(self, code: str) -> List[Dict]:
        """分析代码中的性能问题
        
        Args:
            code: 代码
            
        Returns:
            问题列表
        """
        problems = []
        
        for issue in self.issues:
            matches = re.finditer(issue["pattern"], code, re.MULTILINE)
            for match in matches:
                line_num = code[:match.start()].count('\n') + 1
                problems.append({
                    "id": issue["id"],
                    "line": line_num,
                    "issue": issue["issue"],
                    "explanation": issue["explanation"],
                    "example_bad": issue["example_bad"],
                    "example_good": issue["example_good"],
                    "speedup": issue["speedup"]
                })
        
        return problems
    
    def optimize_code(self, code: str) -> OptimizationResult:
        """生成优化后的代码
        
        Args:
            code: 原始代码
            
        Returns:
            优化结果
        """
        optimized = code
        improvements = []
        lines_changed = 0
        
        # 优化1: range(len()) -> enumerate
        if re.search(r"for\s+i\s+in\s+range\(len\(", code):
            optimized = re.sub(
                r"for\s+(\w+)\s+in\s+range\(len\((\w+)\)\):",
                r"for \1, \2 in enumerate(\2):",
                optimized
            )
            improvements.append("将range(len())替换为enumerate()")
            lines_changed += 1
        
        # 优化2: list(keys()) -> list(dict)
        optimized = re.sub(
            r"list\(([\w\.]+)\.keys\(\)\)",
            r"list(\1)",
            optimized
        )
        if "list(" in optimized and "keys" not in optimized:
            pass  # 已经替换
        
        # 优化3: list(map()) -> 列表推导式
        optimized = re.sub(
            r"list\(map\((lambda\s+)?(.+?),\s*(.+?)\)\)",
            r"[\2 for \2 in \3]",
            optimized
        )
        
        # 计算改进
        speedup = self._estimate_speedup(improvements, len(code))
        
        return OptimizationResult(
            original_code=code,
            optimized_code=optimized,
            improvements=improvements,
            speedup=speedup,
            lines_changed=lines_changed
        )
    
    def _estimate_speedup(self, improvements: List[str], code_size: int) -> str:
        """估算加速比"""
        if not improvements:
            return "无明显改进"
        
        # 估算加速比
        base = 1.0
        for imp in improvements:
            if "range(len())" in imp:
                base *= 2.5
            elif "list(keys())" in imp:
                base *= 2.0
            elif "list(map())" in imp:
                base *= 1.5
        
        return f"~{base:.1f}x"
    
    def suggest_optimizations(self, problems: List[Dict]) -> List[Dict]:
        """针对问题提供优化建议
        
        Args:
            problems: 问题列表
            
        Returns:
            优化建议列表
        """
        suggestions = []
        
        problem_types = set(p["id"].split("-")[0] for p in problems)
        
        for strategy in self.strategies:
            strategy_related = any(
                strategy["strategy"] in [
                    "使用适当的数据结构",  # PERF-008
                    "减少函数调用开销",     # PERF-003, PERF-004
                    "惰性计算",           # PERF-005
                ] for _ in [1]
            )
            
            suggestions.append({
                "strategy": strategy["strategy"],
                "description": strategy["description"],
                "related_problems": [p["issue"] for p in problems if p["id"].startswith(tuple(problem_types))],
                "examples": strategy["examples"]
            })
        
        return suggestions
    
    def generate_optimized_version(self, code: str) -> str:
        """生成优化后的代码版本
        
        Args:
            code: 原始代码
            
        Returns:
            优化后的代码
        """
        optimized = code
        
        # 替换模式
        replacements = [
            # range(len()) -> enumerate
            (r"for\s+i\s+in\s+range\(len\((\w+)\)\):", 
             r"for i, \1 in enumerate(\1):"),
            
            # list(keys()) -> list()
            (r"list\(([\w\.]+)\.keys\(\)\)", 
             r"list(\1)"),
            
            # list(map()) -> 列表推导式
            (r"list\(map\((lambda\s+)?(.+?),\s*(.+?)\)\)", 
             r"[\2 for \2 in \3]"),
        ]
        
        for pattern, replacement in replacements:
            optimized = re.sub(pattern, replacement, optimized)
        
        # 添加优化注释
        if optimized != code:
            header = "# 优化版本\n"
            optimized = header + optimized
        
        return optimized
    
    def get_stats(self) -> Dict:
        """获取统计"""
        return {
            "known_issues": len(self.issues),
            "optimization_strategies": len(self.strategies)
        }


# 测试
if __name__ == "__main__":
    optimizer = PerformanceOptimizer()
    
    test_code = """
items = [1, 2, 3, 4, 5]
for i in range(len(items)):
    print(items[i])

keys = list(my_dict.keys())

result = []
for x in lists:
    result.append(x)
    """
    
    print("🦞 性能优化测试\n")
    
    # 分析
    problems = optimizer.analyze_code(test_code)
    print(f"发现 {len(problems)} 个性能问题:\n")
    
    for p in problems:
        print(f"[{p['id']}] {p['issue']}")
        print(f"   位置: 第{p['line']}行")
        print(f"   优化: {p['speedup']}\n")
    
    # 优化
    result = optimizer.optimize_code(test_code)
    print(f"\n改进: {result.improvements}")
    print(f"加速比: {result.speedup}")
