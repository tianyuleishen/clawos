# 🦞 ClawOS 安装指南

## 安装方式

### 方式一：Git克隆（推荐）

```bash
# 1. 克隆仓库
git clone https://github.com/tianyuleishen/clawos.git
cd clawos

# 2. 运行安装脚本
bash install.sh

# 3. 初始化配置
python clawos/onboarding.py

# 4. 开始使用
python clawos/cli.py
```

### 方式二：pip安装

```bash
# 1. 克隆仓库
git clone https://github.com/tianyuleishen/clawos.git
cd clawos

# 2. pip安装
pip install -e .

# 3. 开始使用
clawos help
```

## 快速使用

```bash
# 查看帮助
clawos help

# 安装系统
clawos install

# 初始化配置
clawos init

# 启动命令行界面
clawos cli

# 启动Web界面
clawos web
```

## 验证安装

```bash
# 检查系统状态
clawos status
```

## 常见问题

### Python版本要求
- Python 3.10+

### Git未安装
```bash
# Ubuntu/Debian
sudo apt-get install git

# macOS
brew install git

# Windows
# 下载安装: https://git-scm.com/download/win
```

### pip未安装
```bash
# Ubuntu/Debian
sudo apt-get install python3-pip

# macOS
brew install pip

# Windows
# Python安装时勾选pip
```

## 更多信息

- GitHub: https://github.com/tianyuleishen/clawos
- 文档: 查看README.md
