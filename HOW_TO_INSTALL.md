# 🦞 ClawOS 安装失败的解决方法

## 问题：git clone 提示找不到仓库

**99%的原因**：电脑上**没有安装Git**

---

## 解决方法

### 第一步：检查电脑是否有Git

打开"命令提示符" (按 Win+R，输入 cmd，回车)，输入：

```bash
git --version
```

**如果显示版本号**（如 git version 2.39.0），说明Git已安装，直接到第二步。

**如果显示"'git' 不是内部或外部命令"**，说明Git未安装，继续第三步。

---

### 第二步：直接克隆

```bash
git clone https://github.com/tianyuleishen/clawos.git
```

---

### 第三步：安装Git（如果没安装）

1. **下载Git**：
   浏览器打开：https://git-scm.com/download/win
   
2. **安装Git**：
   - 双击下载的文件
   - **全部选择默认选项**
   - 一路点击"Next"或"Install"

3. **重要**：安装完成后，**关闭命令提示符，重新打开**

4. **再次检查**：
   ```bash
   git --version
   ```
   如果显示版本号，说明安装成功！

---

### 第四步：克隆并安装

在命令提示符中输入：

```bash
git clone https://github.com/tianyuleishen/clawos.git
cd clawos
pip install -e .
```

---

## 常见问题

### Q: 找不到git命令？
A: Git未安装或未添加到PATH。重新安装Git即可。

### Q: pip安装失败？
A: 尝试：
   ```bash
   pip install --user -e .
   ```

### Q: 仓库不存在？
A: 检查网络连接，确保能访问GitHub。

---

## 简单记忆

**一句话**：
```
先装Git，再克隆，最后pip安装
```

**完整命令**：
```bash
# 1. 安装Git (如果没安装)
# 下载: https://git-scm.com/download/win

# 2. 打开命令提示符

# 3. 执行
git clone https://github.com/tianyuleishen/clawos.git
cd clawos
pip install -e .
```

---

## 如果还不行

请发送以下信息给我：
1. 操作系统 (Windows 10 还是 11)
2. `git --version` 的结果
3. `python --version` 的结果
4. 截图错误信息

---

## GitHub仓库地址

https://github.com/tianyuleishen/clawos
