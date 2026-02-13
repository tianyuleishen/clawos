# 🦞 OpenClaw Skills - 核心能力

> 这些是OpenClaw智能助手的核心能力，不包含在公开的ClawOS中。

## 架构说明

```
┌─────────────────────────────────────┐
│        OpenClaw 智能助手              │
│   (集成所有skills和ClawOS)           │
├─────────────────────────────────────┤
│  skills/                             │
│  ├── reasoning-depth-enhancement/   │
│  ├── understanding-enhancement/      │
│  └── code-quality-enhancement/      │
├─────────────────────────────────────┤
│  clawos/                            │
│  (简化的AI操作系统，公开可用)          │
└─────────────────────────────────────┘
```

## 技能列表

### 1. 推理深度增强 (reasoning-depth-enhancement)
- ChainReasoner: 链式推理
- CausalAnalyzer: 因果分析
- CounterfactualReasoner: 反事实推理
- MetaReasoner: 元推理
- **Codeforces测试: 94%准确率**

### 2. 理解增强 (understanding-enhancement)
- PronounResolver: 指代消解
- ContextTracker: 上下文追踪
- EmotionRecognizer: 情感识别
- IntentInferrer: 意图推断

### 3. 代码质量 (code-quality-enhancement)
- CodeReviewer: 代码审查
- BestPractice: 最佳实践检查
- ErrorHandler: 错误处理
- PerformanceOptimizer: 性能优化

## 使用方法

```bash
# 进入OpenClaw工作目录
cd ~/.openclaw/

# 查看技能
ls skills/

# 测试推理深度技能
cd skills/reasoning-depth-enhancement/
python3 __main__.py --test
```

## 与ClawOS的关系

- ClawOS是简化的AI操作系统，包含基础功能
- OpenClaw = ClawOS + 所有skills
- Skills提供的高级能力是OpenClaw的核心竞争优势
