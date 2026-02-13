# 🦞 ClawOS 功能清单

## 一、核心AI能力

| 功能 | 状态 | 说明 |
|------|------|------|
| L11意识系统 | ✅ 启用 | TRANSCENDENT级别，95%深度 |
| 终极融合推理 | ✅ 启用 | 5种推理方法，95%置信度 |
| 自然语言理解 | ✅ 可用 | NLU处理 |
| 逻辑推理 | ✅ 可用 | 链式推理 |
| 因果分析 | ✅ 可用 | 因果关系分析 |
| 反事实推理 | ✅ 可用 | 假设推理 |
| 元认知 | ✅ 可用 | 自我认知 |

## 二、命令行命令

| 命令 | 状态 | Windows | 说明 |
|------|------|---------|------|
| `clawos --help` | ✅ | ✅ | 查看帮助 |
| `clawos init` | ✅ | ✅ | 初始化配置 |
| `clawos cli` | ✅ | ✅ | 命令行交互 |
| `clawos web` | ✅ | ✅ | Web界面 |
| `clawos gui` | ❌ | ❌ | GUI界面 |
| `clawos feishu` | ⚠️ | ⚠️ | 飞书集成 |
| `clawos test` | ✅ | ✅ | 运行测试 |
| `clawos status` | ✅ | ✅ | 系统状态 |
| `clawos version` | ✅ | ✅ | 版本信息 |

## 三、安装方式

| 方式 | 状态 | Windows | 说明 |
|------|------|---------|------|
| pip install clawos-ai | ⚠️ | ⚠️ | 需完善包配置 |
| git clone + pip install -e . | ✅ | ✅ | 推荐方式 |
| python -m clawos | ✅ | ✅ | 直接运行 |

## 四、文件结构

```
clawos/
├── __init__.py         # 包初始化
├── __main__.py         # python -m clawos
├── main.py             # 主程序
├── cli.py              # 命令行
├── gui/
│   └── webgui.py      # Web界面
├── im/
│   └── feishu.py      # 飞书集成
├── core/
│   ├── consciousness/  # L11意识
│   └── fusion/        # 终极融合
└── ...
```

## 五、安装要求

| 要求 | 最低 | 推荐 |
|------|------|------|
| Python | 3.10 | 3.11+ |
| 内存 | 512MB | 2GB |
| 磁盘 | 100MB | 1GB |
| 网络 | 可选 | 推荐 |

## 六、Windows兼容性

### ✅ 完全兼容
- 命令行界面
- Web界面
- 所有推理功能
- 测试功能

### ⚠️ 部分兼容
- pip安装 (需完善)
- 飞书集成 (需API)

### ❌ 不兼容
- GUI界面 (PyQt6)

## 七、使用流程

```bash
# Windows
git clone https://github.com/tianyuleishen/clawos.git
cd clawos
pip install -e .
clawos --help
clawos init
clawos cli
```

## GitHub

https://github.com/tianyuleishen/clawos
