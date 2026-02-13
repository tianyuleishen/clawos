# 🦞 ClawOS 简单安装指南

## 问题

之前安装失败是因为：
1. 依赖包太多、太复杂
2. 一些包不支持Python 3.12/3.15

## 简单安装方法（推荐）

### 步骤1：下载ZIP文件

1. 浏览器打开：
   ```
   https://github.com/tianyuleishen/clawos
   ```
2. 点击绿色按钮 **"Code"**
3. 点击 **"Download ZIP"**

### 步骤2：解压文件

右键点击下载的 `clawos-main.zip`，选择"解压到当前文件夹"

### 步骤3：安装（跳过复杂依赖）

在解压后的文件夹中，打开**命令提示符**，输入：

```bash
python EASY_INSTALL.py
```

### 步骤4：使用

```bash
# 方法1：直接运行
python clawos.py

# 方法2：查看帮助
python clawos.py help
```

---

## 如果EASY_INSTALL也失败

直接使用简化版本：

```bash
python run_clawos.py
```

这个版本**不需要安装**，可以直接运行！

---

## 功能对比

| 方法 | 功能 | 难度 |
|------|------|------|
| `python run_clawos.py` | 简化版（命令行测试） | ⭐ 最简单 |
| `python clawos.py` | 完整版（基础功能） | ⭐⭐ 简单 |
| `pip install -e .` | 完整版（全部功能） | ⭐⭐⭐ 复杂 |

---

## 快速开始

```bash
# 最简单的方法（推荐新手）
python run_clawos.py

# 或者
python clawos.py
```

---

## 常见问题

### Q: 报错"找不到模块"？
A: 使用 `python run_clawos.py`，这个版本不需要安装

### Q: pip安装失败？
A: 使用 `python EASY_INSTALL.py` 跳过复杂依赖

### Q: Python版本问题？
A: 使用 `python run_clawos.py` 简化版

---

## GitHub

https://github.com/tianyuleishen/clawos
