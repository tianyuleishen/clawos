# 🦞 ClawOS GitHub安装指南

## ⚠️ 关于pip安装

**问题**：`pip install clawos-ai` 提示找不到版本

**原因**：clawos-ai还没有发布到PyPI官方源

**解决方案**：使用Git克隆安装

---

## Git克隆安装

### 步骤1：打开命令提示符

按 `Win+R`，输入 `cmd`，回车

### 步骤2：执行安装命令

```bash
# 1. 克隆仓库
git clone https://github.com/tianyuleishen/clawos.git

# 2. 进入目录
cd clawos

# 3. 安装
pip install -e .
```

### 步骤3：验证安装

```bash
clawos --help
```

如果显示帮助信息，说明安装成功！

---

## 错误解决

### 错误：'git' 不是内部或外部命令

**原因**：Git未安装

**解决**：
1. 下载Git: https://git-scm.com/download/win
2. 安装后**重启命令提示符**

### 错误：'python' 不是内部或外部命令

**原因**：Python未添加到PATH

**解决**：
1. 重新安装Python
2. **勾选** "Add Python to PATH"
3. 重启命令提示符

### 错误：安装失败

**解决**：
1. 使用管理员权限运行命令提示符
2. 输入：`pip install --user clawos-ai`

---

## 使用方法

安装成功后：

```bash
# 查看帮助
clawos --help

# 初始化
clawos init

# 启动命令行
clawos cli

# 启动Web
clawos web
```

---

## GitHub

https://github.com/tianyuleishen/clawos
