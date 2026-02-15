# 🦞 NexusOS Windows 打包指南

## 快速开始

### 1. 安装依赖

在Windows上以管理员身份打开PowerShell或CMD，运行：

```powershell
pip install pyinstaller
```

### 2. 打包

```bash
cd nexusos-windows
python build.py
```

### 3. 找到exe

打包完成后，在 `dist` 文件夹中找到 `NexusOS.exe`

---

## 手动打包

如果自动打包失败，可以手动运行：

```bash
pyinstaller --onefile --windowed --name=NexusOS nexusos_gui.py
```

---

## 打包选项说明

| 参数 | 说明 |
|------|------|
| `--onefile` | 打包成单个exe文件 |
| `--windowed` | 不显示控制台窗口 |
| `--name` | exe文件名 |
| `--icon` | 程序图标 |

---

## 注意事项

1. **Python版本**: 推荐 Python 3.8-3.11
2. **tkinter**: 确保安装Python时勾选了tkinter
3. **管理员权限**: 建议用管理员身份运行CMD/PowerShell

---

## 问题排查

### tkinter未安装
```
pip install tk
```

### PyInstaller未安装
```
pip install pyinstaller
```

### 打包失败
尝试更新PyInstaller:
```
pip install --upgrade pyinstaller
```

---

## 输出

成功后会生成:
- `dist/NexusOS.exe` - 可执行文件
- `build/` - 临时文件
- `*.spec` - 打包配置
