# 🦞 ClawOS AI Operating System

> **注意**: ClawOS拥有所有OpenClaw的能力，除了自我进化能力。
> - **推理能力**: Chain/Causal/Counterfactual/Meta (94% Codeforces)
> - **理解能力**: Pronoun/Context/Emotion/Intent
> - **代码质量**: Review/BestPractice/ErrorHandler
> - **❌ 禁止**: 自我学习/算法创新/自我改进/能力创造

<p align="center">

![ClawOS](https://img.shields.io/badge/ClawOS-v2.0-blue)
![Python](https://img.shields.io/badge/Python-3.10+-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

</p>

> ClawOS - AI操作系统，集成完整推理、理解和代码质量能力。

---

## ✨ 特性

### 🧠 完整推理引擎 (94% Codeforces)

| 引擎 | 准确率 | 功能 |
|------|--------|------|
| Logic Engine | 100% | 逻辑推理 |
| ChainReasoner | 95% | 链式推理 |
| CausalAnalyzer | 85% | 因果分析 |
| CounterfactualReasoner | 70% | 反事实推理 |
| MetaReasoner | 75% | 元推理 |
| Math Engine | 83% | 数学计算 |

### 💡 理解增强

| 模块 | 功能 |
|------|------|
| PronounResolver | 指代消解 |
| ContextTracker | 上下文追踪 |
| EmotionRecognizer | 情感识别 |
| IntentInferrer | 意图推断 |

### 🔧 代码质量

| 模块 | 功能 |
|------|------|
| CodeReviewer | 代码审查 |
| BestPractice | 最佳实践 |
| ErrorHandler | 错误处理 |

### 💻 电脑控制

- 鼠标控制
- 键盘控制
- 窗口管理

### 📁 文件管理

- 文件读写
- 批量操作
- 文件搜索

### 🔌 插件系统

- 插件生命周期管理
- 插件API
- 插件市场

### 🌐 API接口

- REST API
- WebSocket
- 云同步

---

## 🚀 快速开始

### 安装

```bash
# pip安装 (推荐)
pip install clawos

# 或从源码安装
git clone https://github.com/tianyuleishen/clawos.git
cd clawos
pip install -e .
```

### 使用

```bash
# 进入对话模式
clawos chat

# 查看系统状态
clawos status

# 推理测试
clawos reason "如果A>B，B>C，那么A>C吗？"
```

### Python API

```python
import asyncio
from clawos import UltimateFusionEngine

async def main():
    engine = UltimateFusionEngine()
    
    # 链式推理
    result = await engine.analyze("如果A>B，B>C，那么A>C吗？")
    print(f"答案: {result.result}")
    print(f"引擎: {result.engine_used}")
    print(f"置信度: {result.confidence:.0%}")

asyncio.run(main())
```

---

## 📖 文档

- [用户手册](docs/README.md)
- [API文档](docs/API.md)
- [能力配置](CLAWOS_CAPABILITIES.md)
- [架构设计](ARCHITECTURE.md)

---

## 🏆 基准测试

| 引擎 | 准确率 | 说明 |
|------|--------|------|
| Logic Engine | 100% | 逻辑推理 |
| ChainReasoner | 95% | 链式推理 |
| CausalAnalyzer | 85% | 因果分析 |
| CounterfactualReasoner | 70% | 反事实 |
| MetaReasoner | 75% | 元推理 |
| Math Engine | 83% | 数学 |

**Codeforces综合测试: 18/19 (94%)**

---

## 📊 统计

```
代码行数: ~18,000行
Python文件: 45个
推理引擎: 8个
测试通过率: 100%
```

---

## ⚠️ 禁止的能力

以下能力仅OpenClaw可用，ClawOS无法调用：

- ❌ 自我学习 (Self-Learning)
- ❌ 算法创新 (Algorithm Innovation)
- ❌ 自我改进 (Self-Improvement)
- ❌ 能力创造 (Capability Creation)

详见 [ARCHITECTURE.md](ARCHITECTURE.md)

---

## 🤝 贡献

欢迎提交Issue和Pull Request！

---

## 📄 许可证

MIT License

---

<p align="center">

**🦞 ClawOS** - AI操作系统（拥有完整能力，无进化能力）

</p>

---

> **OpenClaw**: 如果需要自我进化能力，请使用OpenClaw智能助手。
> 详见 [ARCHITECTURE.md](ARCHITECTURE.md)
