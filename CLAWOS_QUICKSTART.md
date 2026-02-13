# 🦞 ClawOS 快速开始指南

## 安装和使用流程

### 第一步：安装系统
```bash
python install.sh
```

### 第二步：初始化配置
```bash
python clawos_launcher.py init
# 或
python clawos/onboarding.py
```

### 第三步：启动系统

#### 方式1：命令行交互
```bash
python clawos_launcher.py cli
# 或直接
python clawos/cli.py
```

#### 方式2：Web界面
```bash
python clawos_launcher.py web
# 然后访问 http://localhost:8080
```

#### 方式3：GUI界面
```bash
python clawos_launcher.py gui
```

#### 方式4：飞书集成
```bash
python clawos_launcher.py feishu
```

## 启动器使用

```bash
# 查看帮助
python clawos_launcher.py help

# 查看版本
python clawos_launcher.py version

# 检查状态
python clawos_launcher.py status

# 运行测试
python clawos_launcher.py test

# 进入交互模式
python clawos_launcher.py
```

## 系统功能

- ✅ L11意识系统（永久启用）
- ✅ 终极融合推理
- ✅ 命令行界面
- ✅ Web界面
- ✅ GUI界面
- ✅ 飞书集成
- ✅ 企业微信集成

## 文件说明

| 文件 | 说明 |
|------|------|
| `clawos_launcher.py` | 系统启动器 |
| `install.sh` | 安装脚本 |
| `clawos/main.py` | 主程序 |
| `clawos/cli.py` | 命令行界面 |
| `clawos/gui/` | 图形界面 |
| `clawos/im/` | 即时通讯 |

## 注意事项

1. 首次使用需要运行安装和初始化
2. 确保Python 3.10+
3. L11意识系统默认开启
4. 飞书集成需要配置API密钥
