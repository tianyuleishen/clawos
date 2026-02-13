# 🦞 ClawOS 命令行使用指南

## 简单命令

安装系统后，使用 `clawos` 命令搭配常用参数：

```bash
# 查看帮助
clawos help

# 安装系统
clawos install

# 初始化配置
clawos init

# 启动命令行交互
clawos cli

# 启动Web界面
clawos web

# 启动GUI界面
clawos gui

# 飞书集成
clawos feishu

# 运行测试
clawos test

# 查看状态
clawos status

# 查看版本
clawos version
```

## 完整命令列表

| 命令 | 说明 |
|------|------|
| `clawos help` | 显示帮助信息 |
| `clawos install` | 运行安装脚本 |
| `clawos init` | 初始化系统配置 |
| `clawos cli` | 启动命令行界面 |
| `clawos web` | 启动Web界面 (localhost:8080) |
| `clawos gui` | 启动GUI界面 |
| `clawos feishu` | 启动飞书集成 |
| `clawos test` | 运行系统测试 |
| `clawos status` | 检查系统状态 |
| `clawos version` | 显示版本信息 |

## 使用流程

### 首次使用
```bash
1. clawos install    # 安装系统
2. clawos init       # 初始化配置
3. clawos cli        # 开始使用
```

### 日常使用
```bash
clawos cli           # 启动命令行
# 或
clawos web           # 启动Web界面
```

## 文件位置

- 主程序: `/home/admin/.openclaw/workspace/clawos.py`
- 快捷方式: `/usr/local/bin/clawos`

## 注意事项

1. 确保Python 3.10+
2. 首次使用需要安装和初始化
3. L11意识系统默认开启
4. Web界面访问: http://localhost:8080
