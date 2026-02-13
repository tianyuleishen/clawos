# 🦞 Error Handler - 错误处理增强

"""
错误处理增强模块

功能:
- 识别错误模式
- 生成修复建议
- 最佳实践建议
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum


@dataclass
class ErrorPattern:
    """错误模式"""
    pattern: str
    error_type: str
    description: str
    cause: str
    fix: str
    example: str


@dataclass
class FixSuggestion:
    """修复建议"""
    line: int
    error_type: str
    suggestion: str
    explanation: str
    example_code: str


class ErrorHandler:
    """错误处理器"""
    
    # Python常见错误模式
    ERROR_PATTERNS = [
        ErrorPattern(
            pattern="IndexError.*list index out of range",
            error_type="IndexError",
            description="列表索引越界",
            cause="访问了不存在的索引",
            fix="使用len()检查或try-except",
            example="for i in range(len(list)): list[i]"
        ),
        ErrorPattern(
            pattern="KeyError.*",
            error_type="KeyError",
            description="字典键不存在",
            cause="访问了字典中不存在的键",
            fix="使用dict.get()或dict.setdefault()",
            example="dict.get(key, default)"
        ),
        ErrorPattern(
            pattern="AttributeError.*object has no attribute",
            error_type="AttributeError",
            description="对象没有该属性",
            cause="拼写错误或对象类型错误",
            fix="检查属性名是否正确或对象类型",
            example="hasattr(obj, 'attr')"
        ),
        ErrorPattern(
            pattern="TypeError.*",
            error_type="TypeError",
            description="类型错误",
            cause="操作使用了不兼容的类型",
            fix="确保类型匹配或使用类型转换",
            example="str(x) if not isinstance(x, str)"
        ),
        ErrorPattern(
            pattern="ValueError.*",
            error_type="ValueError",
            description="值错误",
            cause="函数收到正确的类型但值不对",
            fix="验证输入值",
            example="if 0 <= x <= 100: return x"
        ),
        ErrorPattern(
            pattern="NameError.*name.*is not defined",
            error_type="NameError",
            description="名称未定义",
            cause="使用了未定义的变量或函数",
            fix="先定义变量或检查拼写",
            example="if 'var' in locals(): var = default"
        ),
        ErrorPattern(
            pattern="ImportError.*No module named",
            error_type="ImportError",
            description="模块导入错误",
            cause="模块不存在或未正确安装",
            fix="安装模块或检查导入路径",
            example="try: import module except ImportError: pip install"
        ),
        ErrorPattern(
            pattern="FileNotFoundError.*",
            error_type="FileNotFoundError",
            description="文件未找到",
            cause="尝试打开不存在的文件",
            fix="检查文件路径或使用os.path.exists()",
            example="if os.path.exists(path): f = open(path)"
        ),
        ErrorPattern(
            pattern="PermissionError.*",
            error_type="PermissionError",
            description="权限错误",
            cause="没有操作文件的权限",
            fix="检查文件权限或使用管理员运行",
            example="os.chmod(path, 0o777)"
        ),
        ErrorPattern(
            pattern="MemoryError.*",
            error_type="MemoryError",
            description="内存不足",
            cause="使用的内存超出限制",
            fix="分批处理或使用生成器",
            example="for chunk in iter: yield chunk"
        ),
    ]
    
    # 错误处理最佳实践
    BEST_PRACTICES = [
        {
            "id": "ERR-BP001",
            "name": "具体异常优于通用异常",
            "description": "尽可能使用具体的异常类型",
            "good": "except ValueError as e:",
            "bad": "except Exception as e:"
        },
        {
            "id": "ERR-BP002",
            "name": "记录异常信息",
            "description": "记录异常以便调试",
            "good": "except Exception as e: logger.error(e)",
            "bad": "except: pass"
        },
        {
            "id": "ERR-BP003",
            "name": "重新抛出更具体的异常",
            "description": "包装异常提供更多信息",
            "good": "except ValueError as e: raise CustomError(f\"无效输入: {e}\") from e",
            "bad": "except: pass"
        },
        {
            "id": "ERR-BP004",
            "name": "使用finally清理资源",
            "description": "确保资源被正确释放",
            "good": "try: f = open(f) finally: f.close()",
            "bad": "try: f = open(f) except: pass"
        },
        {
            "id": "ERR-BP005",
            "name": "避免空的except块",
            "description": "至少记录错误",
            "good": "except Exception as e: logger.warning(f\"Ignored: {e}\")",
            "bad": "except: pass"
        },
        {
            "id": "ERR-BP006",
            "name": "使用else执行无异常时的代码",
            "description": "区分成功和异常处理",
            "good": "try: x = int(s) except: pass else: print(x)",
            "bad": "try: x = int(s) except: pass"
        },
        {
            "id": "ERR-BP007",
            "name": "使用with管理资源",
            "description": "自动清理资源",
            "good": "with open(f) as f: data = f.read()",
            "bad": "f = open(f); data = f.read()"
        },
    ]
    
    def __init__(self):
        self.patterns = {p.error_type: p for p in self.ERROR_PATTERNS}
        self.practices = self.BEST_PRACTICES
    
    def analyze_error(self, error_message: str) -> List[FixSuggestion]:
        """分析错误消息
        
        Args:
            error_message: 错误消息
            
        Returns:
            修复建议列表
        """
        suggestions = []
        
        for error_type, pattern in self.patterns.items():
            if re.search(pattern.pattern, error_message, re.IGNORECASE):
                # 提取行号（如果存在）
                line = self._extract_line(error_message)
                
                suggestion = FixSuggestion(
                    line=line or 0,
                    error_type=error_type,
                    suggestion=pattern.fix,
                    explanation=pattern.description,
                    example_code=self._get_example(error_type)
                )
                suggestions.append(suggestion)
        
        # 如果没有匹配的错误模式
        if not suggestions:
            suggestions.append(FixSuggestion(
                line=0,
                error_type="Unknown",
                suggestion="查看完整错误堆栈跟踪",
                explanation="无法识别的错误类型",
                example_code="# 检查代码逻辑和输入数据"
            ))
        
        return suggestions
    
    def _extract_line(self, error_message: str) -> Optional[int]:
        """提取行号"""
        # 匹配 "line X" 或 "Line X" 或 "line X"
        match = re.search(r'line\s*(\d+)', error_message, re.IGNORECASE)
        if match:
            return int(match.group(1))
        return None
    
    def _get_example(self, error_type: str) -> str:
        """获取示例代码"""
        examples = {
            "IndexError": """# 修复前
for i in range(len(items)):
    print(items[i])

# 修复后
for item in items:
    print(item)
# 或
for i, item in enumerate(items):
    print(i, item)""",
            
            "KeyError": """# 修复前
value = my_dict['key']

# 修复后
value = my_dict.get('key', default_value)
# 或
if 'key' in my_dict:
    value = my_dict['key']""",
            
            "TypeError": """# 修复前
result = number + " string"

# 修复后
result = str(number) + " string"
# 或
result = f"{number} string"""",
            
            "AttributeError": """# 修复前
obj = MyClass()
obj.my_method()

# 修复后 - 检查拼写
obj = MyClass()
obj.my_method()  # 或检查是否存在
if hasattr(obj, 'my_method'):
    obj.my_method()""",
        }
        
        return examples.get(error_type, "# 请检查错误消息获取具体修复建议")
    
    def get_best_practices(self) -> List[Dict]:
        """获取最佳实践列表"""
        return self.practices
    
    def generate_error_handling(self, error_type: str, context: str) -> str:
        """生成错误处理代码
        
        Args:
            error_type: 错误类型
            context: 代码上下文
            
        Returns:
            错误处理代码
        """
        templates = {
            "IndexError": f"""
try:
    {context}
except IndexError as e:
    logger.error(f"索引越界: {{e}}")
    # 处理越界情况
""",
            
            "KeyError": f"""
try:
    {context}
except KeyError as e:
    logger.error(f"键不存在: {{e}}")
    # 提供默认值或创建键
""",
            
            "ValueError": f"""
try:
    {context}
except ValueError as e:
    logger.error(f"值错误: {{e}}")
    # 验证和清理输入
""",
        }
        
        return templates.get(error_type, f"""
try:
    {context}
except Exception as e:
    logger.error(f"错误: {{e}}")
""")
    
    def get_stats(self) -> Dict:
        """获取统计"""
        return {
            "error_patterns": len(self.patterns),
            "best_practices": len(self.practices)
        }


# 测试
if __name__ == "__main__":
    handler = ErrorHandler()
    
    test_errors = [
        "IndexError: list index out of range at line 10",
        "KeyError: 'username' at line 25",
        "AttributeError: 'MyClass' object has no attribute 'get_name'",
        "TypeError: unsupported operand type(s) for +: 'int' and 'str'"
    ]
    
    print("🦞 错误处理测试\n")
    
    for error in test_errors:
        print(f"错误: {error}")
        suggestions = handler.analyze_error(error)
        
        for s in suggestions:
            print(f"  类型: {s.error_type}")
            print(f"  建议: {s.suggestion}")
            print()
    
    print(f"\n统计: {handler.get_stats()}")
