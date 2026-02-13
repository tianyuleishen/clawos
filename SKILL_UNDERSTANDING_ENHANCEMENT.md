# 🦞 理解力提升技能

**技能名称**: understanding-enhancement  
**版本**: v1.0.0  
**优先级**: P0  
**作者**: ClawOS Team

---

## 📋 功能描述

提升AI的理解能力，包括：
- 指代词解析（"它"、"那个"→具体实体）
- 上下文记忆（记住对话历史）
- 隐含意图理解（从抱怨中识别需求）
- 情绪识别（理解用户情绪）

---

## 🎯 目标

| 指标 | 提升前 | 提升后 |
|------|--------|--------|
| 意图识别准确率 | 75% | 95% |
| 澄清次数 | 2次 | 0.5次 |
| 隐含意图理解 | 50% | 85% |

---

## 📁 技能结构

```
skills/
└── understanding-enhancement/
    ├── SKILL.md              # 技能说明
    ├── skill.json            # 技能元数据
    ├── requirements.txt      # 依赖
    ├── setup.py              # 安装脚本
    ├── understanding/
    │   ├── __init__.py
    │   ├── pronoun_resolver.py    # 指代词解析
    │   ├── context_tracker.py    # 上下文记忆
    │   ├── emotion_recognizer.py  # 情绪识别
    │   └── intent_inferrer.py    # 意图推断
    └── tests/
        └── test_understanding.py
```

---

## 🚀 使用方法

### 安装

```bash
clawhub install understanding-enhancement
```

### 使用

```python
from skills.understanding import EnhancedUnderstanding

# 创建理解器
understander = EnhancedUnderstanding()

# 分析输入
result = await understander.analyze(
    text="把它改成那个颜色",
    context={"color": "红色", "target": "按钮"}
)

# 理解结果
print(result.intent)  # 修改按钮颜色为蓝色
print(result.emotion)  # neutral
print(result.needs)    # []
```

---

## 📝 API

### EnhancedUnderstanding

```python
class EnhancedUnderstanding:
    async def analyze(text: str, context: dict = None) -> UnderstandingResult
    def resolve_pronouns(text: str, context: dict) -> str
    def track_context(user_input: str, system_response: str)
    def recognize_emotion(text: str) -> str
    def infer_intent(text: str, emotion: str) -> dict
```

### UnderstandingResult

```python
@dataclass
class UnderstandingResult:
    surface: str          # 表面文本
    resolved: str         # 解析后的文本
    intent: str          # 识别的意图
    emotion: str         # 情绪
    needs: list          # 隐含需求
    confidence: float    # 置信度
    context: dict        # 上下文
```

---

## 🔧 技术实现

### 1. 指代词解析

```python
PRONOUNS = {
    "它": ["按钮", "输入框", "颜色", "界面"],
    "那个": ["之前的", "刚才的", "左边的"],
    "这里": ["当前位置", "当前页面"],
}
```

### 2. 上下文追踪

```python
CONTEXT_WINDOW = 5  # 保留最近5轮
```

### 3. 情绪识别

```python
EMOTION_KEYWORDS = {
    'frustrated': ['太慢', '不行', '没用', '烦'],
    'impatient': ['快点', '怎么还没', '等不及'],
    'confused': ['不懂', '什么意思'],
}
```

### 4. 需求推断

```python
NEED_PATTERNS = {
    (['太慢', '速度'], '性能'): "优化响应速度",
    (['太复杂', '麻烦'], '易用性'): "简化操作流程",
}
```

---

## 📅 开发计划

### Week 1: 指代词解析
- Day 1-2: 指代词识别模块
- Day 3-4: 实体追踪器
- Day 5-7: 测试和优化

### Week 2: 上下文记忆
- Day 1-2: 对话状态追踪
- Day 3-4: 意图继承
- Day 5-7: 测试

### Week 3: 隐含意图理解
- Day 1-2: 情绪识别
- Day 3-4: 需求推断
- Day 5-7: 综合测试

---

## ✅ 安装验证

```bash
# 验证安装
clawhub verify understanding-enhancement

# 测试功能
python -m skills.understanding.tests.test
```

---

**🦞 理解力提升技能 v1.0.0**
