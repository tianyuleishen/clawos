# 🦞 ClawOS 安装指南

## 方式一：pip安装（推荐）

### 1. 安装
```bash
pip install clawos-ai
```

### 2. 使用
```bash
clawos --help     # 查看帮助
clawos init       # 初始化配置
clawos cli        # 命令行交互
```

## 方式二：Git克隆

### 1. 获取安装包
```bash
git clone https://github.com/tianyuleishen/clawos.git
cd clawos
```

### 2. 安装
```bash
pip install -e .
```

### 3. 使用
```bash
clawos --help
```

## 方式三：直接运行（无需安装）

```bash
git clone https://github.com/tianyuleishen/clawos.git
cd clawos

# 直接使用
python -m clawos --help
python -m clawos init
python -m clawos cli
```

## 命令列表

| 命令 | 说明 |
|------|------|
| `clawos --help` | 查看帮助 |
| `clawos init` | 初始化配置 |
| `clawos cli` | 命令行交互 |
| `clawos web` | Web界面 |
| `clawos gui` | GUI界面 |
| `clawos test` | 运行测试 |

## 快速开始

```bash
# 1. 安装
pip install clawos-ai

# 2. 初始化
clawos init

# 3. 使用
clawos cli
```

## 系统要求

- Python 3.10+
- pip

## GitHub

https://github.com/tianyuleishen/clawos
