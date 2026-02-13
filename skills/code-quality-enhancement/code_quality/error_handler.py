# 🦞 Error Handler - 错误处理增强

from typing import Dict, List, Optional
from dataclasses import dataclass
import re

@dataclass
class ErrorPattern:
    pattern: str
    error_type: str
    description: str
    fix: str

@dataclass
class FixSuggestion:
    line: int
    error_type: str
    suggestion: str
    explanation: str

class ErrorHandler:
    ERROR_PATTERNS = {
        "IndexError": ErrorPattern(
            pattern=r"IndexError.*list index out of range",
            error_type="IndexError",
            description="列表索引越界",
            fix="使用enumerate()或try-except"
        ),
        "KeyError": ErrorPattern(
            pattern=r"KeyError",
            error_type="KeyError",
            description="字典键不存在",
            fix="使用dict.get()"
        ),
        "TypeError": ErrorPattern(
            pattern=r"TypeError",
            error_type="TypeError",
            description="类型错误",
            fix="确保类型匹配"
        ),
        "ValueError": ErrorPattern(
            pattern=r"ValueError",
            error_type="ValueError",
            description="值错误",
            fix="验证输入值"
        ),
    }
    
    def analyze_error(self, error_message: str) -> List[FixSuggestion]:
        suggestions = []
        for error_type, pattern in self.ERROR_PATTERNS.items():
            if re.search(pattern.pattern, error_message, re.IGNORECASE):
                suggestions.append(FixSuggestion(
                    line=0,
                    error_type=error_type,
                    suggestion=pattern.fix,
                    explanation=pattern.description
                ))
        if not suggestions:
            suggestions.append(FixSuggestion(
                line=0,
                error_type="Unknown",
                suggestion="查看完整错误堆栈",
                explanation="无法识别的错误类型"
            ))
        return suggestions
    
    def get_stats(self) -> Dict:
        return {"error_patterns": len(self.ERROR_PATTERNS)}

if __name__ == "__main__":
    handler = ErrorHandler()
    suggestions = handler.analyze_error("IndexError: list index out of range")
    print(f"发现 {len(suggestions)} 个建议")
    for s in suggestions:
        print(f"  {s.error_type}: {s.suggestion}")
