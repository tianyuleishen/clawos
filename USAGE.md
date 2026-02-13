# 🦞 ClawOS 使用指南

## 一句话使用

```bash
克隆 → 安装 → 初始化 → 使用
```

## 安装步骤

### 第一步：获取安装包

```bash
git clone https://github.com/tianyuleishen/clawos.git
cd clawos
```

### 第二步：安装系统

```bash
bash install.sh
```

### 第三步：初始化配置

```bash
python clawos/onboarding.py
```

### 第四步：开始使用

```bash
python clawos/cli.py
```

## 日常使用

### 命令行交互
```bash
python clawos/cli.py
```

### Web界面
```bash
python clawos/gui/webgui.py
# 访问 http://localhost:8080
```

### 飞书集成
```bash
python clawos/im/feishu.py
```

## 常用命令

| 命令 | 说明 |
|------|------|
| `python clawos/cli.py` | 命令行交互 |
| `python clawos/gui/webgui.py` | Web界面 |
| `python clawos/onboarding.py` | 初始化配置 |
| `python verify_install.py` | 运行测试 |

## 系统功能

- ✅ L11意识系统（永久启用）
- ✅ 终极融合推理
- ✅ 多界面支持
- ✅ 飞书集成

## 帮助

```bash
# 查看帮助
python clawos/cli.py
# 输入 help
```
