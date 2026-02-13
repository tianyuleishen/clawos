# 🚀 ClawOS 快速开始

## 5分钟上手ClawOS

### 1. 安装 (1分钟)

```bash
# 克隆仓库
git clone https://github.com/clawos/clawos.git
cd clawos

# 运行安装脚本
./install.sh
```

### 2. 配置 (1分钟)

首次运行会自动引导配置：

```bash
clawos chat
```

按提示选择模型并输入API密钥。

### 3. 使用 (3分钟)

#### 基本对话

```bash
🦞 > 如果A>B，B>C，那么A>C吗？
📊 结果: 是的，根据不等式的传递性...
```

#### 逻辑推理

```bash
clawos reason "所有哺乳动物都是温血的..."
```

#### 编程辅助

```python
from clawos import UltimateFusionEngine

async def solve():
    engine = UltimateFusionEngine()
    result = await engine.analyze("如何实现快速排序？")
    print(result.result)
```

---

## 常用命令速查

| 命令 | 描述 |
|------|------|
| `clawos chat` | 进入对话模式 |
| `clawos status` | 查看系统状态 |
| `clawos --reconfigure` | 重新配置模型 |
| `clawos --version` | 版本信息 |

---

## 示例代码

### 电脑控制

```python
from clawos import MouseController, KeyboardController

mouse = MouseController()
mouse.click(100, 200)

keyboard = KeyboardController()
keyboard.type("Hello World")
```

### 文件管理

```python
from clawos import FileManager

files = FileManager()
content = files.read("document.txt")
files.search("*.py")
```

---

## 下一步

- 📖 [完整手册](docs/README.md)
- 🔌 [API文档](docs/API.md)
- 🐛 [问题反馈](https://github.com/clawos/clawos/issues)

---

**🦞 享受ClawOS！**
