# 🦞 NexusOS Windows 完整版

## 简介

NexusOS Windows完整版是一个具备完整AI能力的桌面助手。

## 功能

### 核心功能
- 意图理解 - 理解用户想做什么
- 电脑控制 - 打开应用/文件/网页
- UI自动化 - 鼠标/键盘控制、截图
- 语音合成 - 4种音色
- 日志系统 - 自动记录运行日志

### 界面
- 科技感UI
- 数据流动画
- 情感人脸显示

## 安装

### 方式1：从源码运行

```bash
# 1. 进入目录
cd nexusos-windows

# 2. 安装依赖
python install.py

# 3. 运行
python nexusos_gui.py
```

### 方式2：exe安装包（推荐）

1. 下载 `NexusOS_Setup.exe`
2. 双击运行安装向导
3. 自动安装依赖
4. 桌面创建快捷方式
5. 双击运行

### 方式3：便携版

1. 解压 `NexusOS_Portable.zip`
2. 直接运行 `NexusOS.exe`

## 打包

### 打包成exe

```bash
# 1. 进入目录
cd nexusos-windows

# 2. 安装PyInstaller
pip install pyinstaller

# 3. 打包
python build.py

# 输出: dist/NexusOS.exe
```

### 打包成安装包

```bash
python build.py --installer

# 输出: installer/NexusOS_Setup.exe
```

## 文件说明

| 文件 | 说明 |
|------|------|
| nexusos_gui.py | 主程序 |
| ui_automation.py | UI自动化模块 |
| voice_module.py | 语音模块 |
| install.py | 自动安装脚本 |
| build.py | PyInstaller打包脚本 |

## 配置

### LLM配置

编辑 `~/.nexusos/config/llm.json`:

```json
{
  "provider": "minimax-portal",
  "model": "MiniMax-M2.1",
  "api_key": "你的API密钥",
  "api_base": "https://api.minimax.chat/v1"
}
```

### 日志

位置: `~/.nexusos/logs/nexusos.log`

查看日志:
```bash
tail -f ~/.nexusos/logs/nexusos.log
```

## 使用

### 对话示例

```
用户: 打开微信
AI: ✓ 已打开微信

用户: 搜索天气
AI: ✓ 已打开浏览器搜索

用户: 帮我执行ls命令
AI: ✓ 命令已执行
```

### 快捷操作

| 按钮 | 功能 |
|------|------|
| 启动 | 启动AI服务 |
| 停止 | 停止AI服务 |
| 浏览器 | 打开浏览器 |
| 文件 | 打开文件管理器 |
| 命令 | 执行终端命令 |
| 截图 | 屏幕截图 |
| 设置 | LLM配置 |

## 版本

v2.9.0 - 完整版
