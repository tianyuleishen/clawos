# 🦞 ClawOS 一步一步安装指南 (Windows)

## ⚠️ 重要说明

**ClawOS不是exe安装程序，不能双击安装！**

ClawOS是一个**Python软件包**，需要通过**命令行**安装。

---

## 第一步：准备环境

### 1.1 安装Git

1. 浏览器打开：https://git-scm.com/download/win
2. 下载 `Git for Windows`
3. **双击下载的文件**，全部默认选项
4. 完成安装

### 1.2 安装Python

1. 浏览器打开：https://python.org/downloads/
2. 下载 **Python 3.11** (或3.10)
3. **重要** - 安装时勾选 ⬜ **"Add Python to PATH"** ⬜
4. 点击 "Install Now"
5. 等待完成

### 1.3 验证安装

打开"命令提示符" (按 `Win+R`，输入 `cmd`，回车)：

```bash
# 检查Python
python --version
# 应该显示: Python 3.11.x

# 检查pip
pip --version
# 应该显示版本号

# 检查git
git --version
# 应该显示版本号
```

---

## 第二步：安装ClawOS

在命令提示符中输入以下命令：

### 方法一：pip安装（推荐）

```bash
pip install clawos-ai
```

### 方法二：克隆安装

```bash
# 1. 克隆仓库
git clone https://github.com/tianyuleishen/clawos.git

# 2. 进入目录
cd clawos

# 3. 安装
pip install -e .
```

---

## 第三步：验证安装

```bash
clawos --help
```

**成功的表现**：
```
🦞 ClawOS AI操作系统 v2.0
...
```

**失败的表现**：
```
'clawos' 不是内部或外部命令...
```

---

## 第四步：开始使用

```bash
# 1. 初始化配置
clawos init

# 2. 启动命令行界面
clawos cli
```

---

## 常见错误解决

### 错误1：'python' 不是内部或外部命令

**原因**：Python未添加到PATH

**解决**：
1. 重新运行Python安装程序
2. 勾选 ✅ "Add Python to PATH"
3. 重启命令提示符

### 错误2：'pip' 不是内部或外部命令

**原因**：pip未安装或未添加到PATH

**解决**：
```bash
python -m ensurepip
python -m pip install --upgrade pip
```

### 错误3：安装失败，提示权限不足

**解决**：
1. 关闭杀毒软件
2. 使用管理员权限运行命令提示符
3. 重试安装

### 错误4：'git' 不是内部或外部命令

**原因**：Git未安装或未添加到PATH

**解决**：
1. 重启命令提示符
2. 如果还是不行，重新安装Git

---

## Windows上不能用的功能

| 功能 | 能否使用 | 说明 |
|------|----------|------|
| 命令行界面 | ✅ 可以 | `clawos cli` |
| Web界面 | ✅ 可以 | `clawos web` |
| L11意识 | ✅ 可以 | 永久启用 |
| 终极融合推理 | ✅ 可以 | 永久启用 |
| 测试功能 | ✅ 可以 | `clawos test` |
| GUI界面 | ❌ 不可以 | 需要Linux |
| 系统托盘 | ❌ 不可以 | 需要Linux |

---

## 使用流程图

```
安装Python和Git
      ↓
打开命令提示符
      ↓
pip install clawos-ai  (或克隆安装)
      ↓
clawos --help  (验证)
      ↓
clawos init    (初始化)
      ↓
clawos cli     (开始使用！)
```

---

## 需要帮助？

发送以下信息给我：
1. 操作系统版本 (Win10还是Win11)
2. Python版本 (`python --version` 结果)
3. 截图错误信息

---

## GitHub

https://github.com/tianyuleishen/clawos
