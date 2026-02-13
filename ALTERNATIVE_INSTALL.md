# 🦞 ClawOS 替代安装方法

## 问题：git clone 找不到仓库

如果Git命令无法克隆，尝试以下方法：

---

## 方法1：使用GitHub CLI

### 1. 安装GitHub CLI
下载：https://cli.github.com/packages/

### 2. 安装后执行
```bash
gh repo clone tianyuleishen/clawos
cd clawos
pip install -e .
```

---

## 方法2：直接下载ZIP

### 1. 下载ZIP文件
浏览器打开以下地址：
```
https://github.com/tianyuleishen/clawos/archive/refs/heads/main.zip
```

### 2. 解压文件
- 右键点击下载的 `main.zip`
- 选择"解压到当前文件夹"

### 3. 安装
```bash
# 打开命令提示符
cd clawos-main  (解压后的文件夹名)
pip install -e .
```

---

## 方法3：使用Python下载

```bash
# 使用Python下载
python -c "import urllib.request; urllib.request.urlretrieve('https://github.com/tianyuleishen/clawos/archive/refs/heads/main.zip', 'clawos.zip')"

# 解压
python -c "import zipfile; zipfile.ZipFile('clawos.zip').extractall('.')"

# 进入目录
cd clawos-main

# 安装
pip install -e .
```

---

## 方法4：检查网络

如果以上都失败，检查：

```bash
# 测试GitHub连接
ping github.com

# 测试HTTPS连接
curl -I https://github.com/tianyuleishen/clawos
```

---

## 最简单方法（推荐）

1. **浏览器打开**：
   ```
   https://github.com/tianyuleishen/clawos
   ```

2. **点击绿色按钮"Code"**

3. **选择"Download ZIP"**

4. **解压并安装**

---

## 安装步骤（下载ZIP后）

```bash
# 1. 解压文件到某个文件夹，例如 D:\

# 2. 打开命令提示符

# 3. 进入解压后的文件夹
cd D:\clawos-main

# 4. 安装
pip install -e .

# 5. 验证
clawos --help
```

---

## 如果还是失败

请发送以下信息给我：

1. `git --version` 的结果
2. `python --version` 的结果
3. 具体的错误信息截图

---

## GitHub地址

https://github.com/tianyuleishen/clawos
