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

### 💬 IM集成

| 平台 | 状态 | 配置 |
|------|------|------|
| 飞书 | ✅ | app_id + app_secret |
| 企业微信 | ✅ | corp_id + app_secret |
| 钉钉 | ✅ | app_key + app_secret |
| QQ | ✅ | http_url (CQHTTP) |

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

---

## 💬 IM集成使用

### 配置IM平台

```bash
# 配置飞书
clawos im configure feishu \
    --app-id YOUR_APP_ID \
    --app-secret YOUR_APP_SECRET

# 配置企业微信
clawos im configure wecom \
    --corp-id YOUR_CORP_ID \
    --app-secret YOUR_APP_SECRET

# 配置钉钉
clawos im configure dingtalk \
    --app-key YOUR_APP_KEY \
    --app-secret YOUR_APP_SECRET

# 配置QQ (需要go-cqhttp)
clawos im configure qq \
    --http-url http://localhost:5700
```

### 使用IM功能

```bash
# 查看连接状态
clawos im status

# 连接平台
clawos im connect feishu

# 发送消息
clawos im send feishu USER_ID "Hello!"

# 发送到所有平台
clawos im send-all "Hello from ClawOS!"
```

### Python API

```python
from clawos.im import IMManager

# 创建管理器
manager = IMManager()

# 配置飞书
manager.configure("feishu", {
    "app_id": "your_app_id",
    "app_secret": "your_app_secret"
})

# 发送消息
await manager.connect("feishu")
await manager.send_message("feishu", "user_id", "Hello!")
```

### 凭证获取

- **飞书**: https://open.feishu.cn/
- **企业微信**: https://work.weixin.qq.com/
- **钉钉**: https://open.dingtalk.com/
- **QQ**: 使用go-cqhttp (https://github.com/Mrs4s/go-cqhttp)

