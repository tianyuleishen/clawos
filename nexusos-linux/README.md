# 🦞 NexusOS 独立版本

## 简介

NexusOS Linux CLI 和 Windows GUI 版本，独立于主工作区，方便日常使用。

## 📁 目录结构

```
nexusos-linux/          # Linux命令行版本
├── nexusos           # 主程序
├── install.py        # 安装脚本
└── README.md         # 说明文档

nexusos-windows/       # Windows图形界面版本
├── nexusos_gui.py   # GUI主程序
├── install.bat       # 安装脚本
└── README.md         # 说明文档
```

## 🐧 Linux版本

### 安装

```bash
cd ~/nexusos-linux
chmod +x nexusos
sudo ln -s ~/nexusos-linux/nexusos /usr/local/bin/nexusos
```

### 使用

```bash
# 启动服务
nexusos start

# 停止服务
nexusos stop

# 查看状态
nexusos status

# 提问
nexusos ask 你好

# 查看帮助
nexusos help
```

### 命令列表

| 命令 | 说明 |
|------|------|
| `nexusos start` | 启动服务 |
| `nexusos stop` | 停止服务 |
| `nexusos status` | 查看状态 |
| `nexusos restart` | 重启服务 |
| `nexusos log` | 查看日志 |
| `nexusos ask <问题>` | 提问 |
| `nexusos chat` | 交互对话 |
| `nexusos plugin list` | 插件列表 |
| `nexusos task create` | 创建任务 |
| `nexusos version` | 版本信息 |
| `nexusos help` | 帮助 |

---

## 🪟 Windows版本

### 安装

1. 双击 `install.bat` 运行安装程序
2. 或直接将 `nexusos_gui.py` 复制到任意位置

### 使用

1. 双击 `NexusOS.lnk` 快捷方式
2. 或运行 `python nexusos_gui.py`

### 功能

- 🎨 简洁美观的UI界面
- 💬 聊天对话
- 🚀 一键启动/停止
- 📊 状态监控
- 📝 对话历史

---

## 📋 系统要求

### Linux
- Python 3.8+
- psutil (可选)

### Windows
- Python 3.8+
- tkinter (Python自带)

---

## 📞 支持

如有问题，请联系维护者。

---

*版本: 1.0.0*
*更新日期: 2026-02-15*
