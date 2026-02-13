# 🦞 Understanding Enhancement Skill

提升AI的理解能力。

## 功能

- **指代词解析**: "它"、"那个" → 具体实体
- **上下文记忆**: 记住对话历史
- **情绪识别**: 理解用户情绪
- **意图推断**: 识别真实需求

## 安装

```bash
# 方法1: 从clawhub安装
clawhub install understanding-enhancement

# 方法2: 手动安装
cd skills/understanding-enhancement
pip install -e .

# 方法3: 复制到openclaw
cp -r understanding-enhancement ~/.openclaw/skills/
```

## 使用

```python
from skills.understanding import EnhancedUnderstanding

# 创建理解器
understander = EnhancedUnderstanding()

# 分析输入
result = await understander.analyze(
    text="把它改成那个颜色",
    context={"color": "红色", "target": "按钮"}
)

# 使用结果
print(result.resolved)   # 解析后的文本
print(result.intent)     # 意图类别
print(result.emotion)    # 情绪
print(result.needs)      # 隐含需求
```

## API

### EnhancedUnderstanding

```python
class EnhancedUnderstanding:
    async def analyze(text: str, context: Dict = None) -> UnderstandingResult
    def update_context(user_input: str, system_response: str)
    def get_context() -> Dict
    def clear_context()
```

### UnderstandingResult

```python
@dataclass
class UnderstandingResult:
    surface: str           # 表面文本
    resolved: str          # 解析后的文本
    intent: str            # 意图类别
    action: str             # 具体动作
    target: str            # 目标对象
    emotion: str           # 情绪
    emotion_intensity: float
    implied_needs: List[str]
    confidence: float
    context: Dict
    suggestions: List[str]
```

## 示例

```python
# 例子1: 指代词解析
result = await understander.analyze("把它改成蓝色")
# 解析: "把按钮改成蓝色"

# 例子2: 上下文继承
await understander.update_context("把按钮改成红色", "好的")
result = await understander.analyze("太大了")
# 解析: "把按钮太大了"

# 例子3: 情绪识别
result = await understander.analyze("太慢了，等不及了")
# 情绪: impatient
# 建议: 提供更快的响应

# 例子4: 隐含需求
result = await understander.analyze("这个太复杂了，学不会")
# 隐含需求: ["需要更详细的学习资料", "需要简化步骤"]
```

## 统计

```python
stats = understander.get_stats()
print(stats)
# {
#     "pronoun_resolver": {"pronoun_count": 7},
#     "context_tracker": {"history_length": 3},
#     "emotion_recognizer": {"emotion_count": 6},
#     "intent_inferrer": {"category_count": 6}
# }
```

## 配置

```python
# 设置上下文窗口大小（默认5轮）
understander.set_window_size(10)

# 清空上下文
understander.clear_context()
```

## 卸载

```bash
clawhub uninstall understanding-enhancement
```

---

**🦞 Understanding Enhancement v1.0.0**
