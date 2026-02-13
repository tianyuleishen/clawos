# 🦞 Code Quality Enhancement Skill

代码质量提升技能。

## 功能

- **代码审查**: 识别代码问题、异味、改进建议
- **最佳实践**: PEP8规范、编码规范检查
- **错误处理**: 错误模式识别、修复建议
- **性能优化**: 识别瓶颈、生成优化代码
- **综合报告**: Markdown格式质量报告

## 安装

```bash
# 方法1: 手动安装
cd skills/code-quality-enhancement
pip install -e .

# 方法2: 复制到openclaw
cp -r code-quality-enhancement ~/.openclaw/skills/
```

## 使用

```python
from code_quality import CodeQualityEnhancer

# 创建增强器
enhancer = CodeQualityEnhancer()

# 分析代码质量
result = await enhancer.analyze_code(code)
print(f"评分: {result.overall_score:.0f}/100")
print(f"问题数: {result.summary['total_issues']}")

# 获取优化建议
for issue in result.issues[:5]:
    print(f"- {issue['message']}")
```

## API

### CodeQualityEnhancer

```python
class CodeQualityEnhancer:
    async def analyze_code(code: str, file_path: str) -> QualityReport
    def optimize_code(code: str) -> Dict
    def check_best_practices(code: str) -> Dict
    def handle_error(error_message: str) -> List[Dict]
    def get_stats() -> Dict
```

### QualityReport

```python
@dataclass
class QualityReport:
    timestamp: str
    overall_score: float
    code_score: float
    style_score: float
    performance_score: float
    issues: List[Dict]
    suggestions: List[str]
    summary: Dict
```

## 示例

### 示例1: 分析代码

```python
code = '''
def bad_function(x):
    if x == True:
        return True
    for i in range(len(items)):
        print(items[i])
'''

result = await enhancer.analyze_code(code)
print(f"评分: {result.overall_score:.0f}/100")
```

### 示例2: 优化代码

```python
optimized = enhancer.optimize_code(code)
print(f"改进: {optimized['improvements']}")
print(f"加速: {optimized['speedup']}")
```

### 示例3: 处理错误

```python
suggestions = enhancer.handle_error("IndexError: list index out of range")
for s in suggestions:
    print(f"类型: {s['error_type']}")
    print(f"建议: {s['suggestion']}")
```

## 检查项目

### 代码审查

- 性能问题
- 安全问题
- 可读性问题
- 可维护性问题

### 最佳实践

- PEP8规范
- 编码规范
- 错误处理
- 测试规范
- 设计规范

### 性能优化

- range(len()) → enumerate
- list(keys()) → list(dict)
- 字符串拼接优化
- 循环优化

## 评分标准

| 评分 | 等级 | 说明 |
|------|------|------|
| 90-100 | A | 优秀 |
| 80-89 | B | 良好 |
| 70-79 | C | 一般 |
| 60-69 | D | 需改进 |
| <60 | F | 较差 |

## 卸载

```bash
clawhub uninstall code-quality-enhancement
```

---

**🦞 Code Quality Enhancement v1.0.0**
