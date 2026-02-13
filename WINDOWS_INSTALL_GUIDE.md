# 🦞 ClawOS Windows安装指南

## 问题解答

### Q: 下载压缩包无法安装？
A: **ClawOS不是压缩包安装软件**，需要通过以下方式安装：

---

## Windows安装方法

### 方法1：pip安装（推荐）

```bash
# 1. 安装Python 3.10+
# 下载地址: https://www.python.org/downloads/

# 2. 打开"命令提示符" (cmd) 或 "PowerShell"

# 3. 执行安装
pip install clawos-ai
```

### 方法2：Git克隆安装

```bash
# 1. 安装Git
# 下载地址: https://git-scm.com/download/win

# 2. 安装Python
# 下载地址: https://python.org/downloads/
# 重要: 安装时勾选 "Add Python to PATH"

# 3. 打开命令提示符 (cmd)

# 4. 执行以下命令:
git clone https://github.com/tianyuleishen/clawos.git
cd clawos
pip install -e .
```

---

## 详细安装步骤

### 步骤1：安装Git

1. 访问 https://git-scm.com/download/win
2. 下载 Windows 安装程序
3. 双击运行，全部默认选项即可
4. 安装完成后，**重启命令提示符**

### 步骤2：安装Python

1. 访问 https://www.python.org/downloads/
2. 下载 Python 3.11 (推荐) 或 3.10
3. **重要**：安装时勾选 ✅ **"Add Python to PATH"**
4. 点击 "Install Now"
5. 安装完成后，**重启命令提示符**

### 步骤3：安装ClawOS

打开"命令提示符" (Win+R，输入 `cmd`，回车)：

```bash
# 方法A：直接pip安装
pip install clawos-ai

# 方法B：克隆安装
git clone https://github.com/tianyuleishen/clawos.git
cd clawos
pip install -e .
```

### 步骤4：验证安装

```bash
clawos --help
```

如果显示帮助信息，说明安装成功！

---

## 常见问题

### 问题1：'git' 不是内部或外部命令
**解决方案**：
- 安装Git后未重启命令提示符
- 重启命令提示符即可

### 问题2：'python' 不是内部或外部命令
**解决方案**：
- Python未添加到PATH
- 重新运行Python安装程序
- 勾选 "Add Python to PATH"

### 问题3：pip安装失败
**解决方案**：
- 使用管理员权限运行命令提示符
- 输入：`pip install --user clawos-ai`
- 或关闭杀毒软件后重试

### 问题4：安装后命令找不到
**解决方案**：
- 重启命令提示符
- 检查Python安装路径是否在PATH中
- 输入：`where clawos`

---

## Windows不支持的功能

### ❌ 完全不支持

| 功能 | 原因 |
|------|------|
| GUI界面 | 需要PyQt6，Linux专用 |
| 系统托盘 | Linux桌面环境特有 |
| 桌面通知 | Linux桌面环境特有 |

### ⚠️ 需要额外配置

| 功能 | 说明 |
|------|------|
| 飞书集成 | 需要API密钥和网络 |
| Web界面 | 需要浏览器支持 |

### ✅ 完全支持

| 功能 | 说明 |
|------|------|
| 命令行界面 | 主要使用方式 |
| 所有推理功能 | L11意识、终极融合 |
| 测试功能 | 基准测试、推理测试 |

---

## 使用方法

安装完成后，打开命令提示符：

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

---

## 技术支持

如果仍有问题：
1. 检查Python版本：`python --version`
2. 检查pip版本：`pip --version`
3. 检查Git版本：`git --version`
4. 截图错误信息发送给我

---

## GitHub

https://github.com/tianyuleishen/clawos
