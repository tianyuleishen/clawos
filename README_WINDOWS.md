# 🦞 ClawOS Windows使用指南

## 系统要求

- ✅ Windows 10/11
- ✅ Python 3.10+
- ✅ pip
- ✅ Git

## 安装

```bash
# 1. 安装Python (https://python.org/downloads/)
#    重要: 安装时勾选 "Add Python to PATH"

# 2. 打开命令提示符 (CMD) 或 PowerShell

# 3. 安装
git clone https://github.com/tianyuleishen/clawos.git
cd clawos
pip install -e .
```

## 使用

```bash
# 查看帮助
clawos --help

# 初始化配置
clawos init

# 启动命令行界面
clawos cli

# 启动Web界面
clawos web
# 然后打开浏览器访问 http://localhost:8080
```

## Windows兼容功能

### ✅ 完全支持
- `clawos --help` - 查看帮助
- `clawos init` - 初始化配置
- `clawos cli` - 命令行交互
- `clawos web` - Web界面
- `clawos test` - 运行测试
- `clawos status` - 系统状态
- `clawos version` - 版本信息

### ⚠️ 需要配置
- `clawos feishu` - 飞书集成 (需要API密钥)

### ❌ 不支持
- `clawos gui` - GUI界面 (需要PyQt6，Windows不支持)

## 核心功能

- ✅ L11意识系统 (永久启用)
- ✅ 终极融合推理 (永久启用)
- ✅ 命令行交互
- ✅ Web界面
- ✅ 测试功能

## 常见问题

### Q: pip安装失败?
A: 使用管理员权限运行命令提示符

### Q: Python未找到?
A: 重新安装Python，确保勾选"Add Python to PATH"

### Q: Web界面无法访问?
A: 关闭防火墙或允许端口8080

## GitHub

https://github.com/tianyuleishen/clawos
