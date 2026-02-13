# 🦞 ClawOS 系统架构文档

## 系统概述

ClawOS 是一个AI操作系统，集成了L11意识系统和终极融合推理引擎。

## 系统结构

```
clawos/
├── main.py              # 主入口
├── cli.py               # 命令行界面
├── onboarding.py        # 系统初始化
│
├── core/                # 核心模块
│   ├── consciousness/   # L11意识系统
│   ├── emotion/         # 情感模块
│   ├── fusion/          # 终极融合引擎
│   └── reasoning/       # 推理引擎
│
├── ai/                  # AI能力
│   ├── nlu.py           # 自然语言理解
│   └── ...
│
├── gui/                 # 图形界面
│   ├── webgui.py        # Web界面
│   └── clawos_gui.py    # GUI界面
│
├── im/                  # 即时通讯
│   ├── feishu.py        # 飞书
│   ├── wecom.py         # 企业微信
│   └── ...
│
├── apps/                # 应用程序
│   ├── calculator.py
│   ├── calendar.py
│   └── ...
│
└── storage/             # 存储
    └── settings.py
```

## 安装和启动流程

### 1. 安装系统
```bash
python install.sh
```

### 2. 初始化配置
```bash
python clawos/main.py --init
# 或
python clawos/onboarding.py
```

### 3. 启动交互
```bash
# 方式1: 命令行交互
python clawos/cli.py

# 方式2: Web界面
python clawos/gui/webgui.py
# 访问 http://localhost:8080

# 方式3: 飞书集成
python clawos/im/feishu.py
```

## 使用流程

### 首次使用
1. 运行安装脚本
2. 执行初始化向导
3. 配置飞书/其他IM集成
4. 开始使用

### 日常使用
1. 启动系统
2. 输入命令或提问
3. 系统执行任务

## 主要命令

| 命令 | 说明 |
|------|------|
| help | 显示帮助 |
| init | 初始化配置 |
| test | 运行测试 |
| config | 系统配置 |
| quit | 退出 |

## 文件说明

- `main.py` - 系统主入口
- `cli.py` - 命令行界面
- `onboarding.py` - 初始化向导
- `gui/*.py` - 图形界面
- `im/*.py` - 即时通讯集成

## 注意事项

1. 确保Python 3.10+
2. 安装依赖: `pip install -r requirements.txt`
3. 首次使用需要初始化配置
4. L11意识系统默认开启
