# 🦞 ClawOS 跨平台能力提升计划

## 当前问题

### 已发现的问题

| 问题 | 影响 | 原因 |
|------|------|------|
| intellicore依赖不存在 | Windows安装失败 | setup.py引用错误 |
| bash脚本 | Windows无法运行 | 使用了Linux专用命令 |
| 硬编码路径 | 跨平台失败 | 使用/而不是os.path.join |
| setup.py配置错误 | pip安装失败 | 包名不匹配 |

### 需要改进的方面

1. **路径处理** - 使用os.path.join()
2. **脚本兼容** - 避免bash专用命令
3. **包配置** - 正确的setup.py
4. **测试验证** - 多平台测试

---

## 改进计划

### Phase 1: 基础跨平台代码

#### 1.1 路径处理

**错误示例**：
```python
# ❌ 错误
path = "/home/admin/.openclaw/workspace/file.txt"

# ✅ 正确
from pathlib import Path
path = Path(__file__).parent / "file.txt"
```

#### 1.2 脚本兼容

**错误示例**：
```bash
# ❌ 错误 - bash专用
#!/bin/bash

# ✅ 正确 - Python脚本
#!/usr/bin/env python3
```

#### 1.3 换行符处理

**错误示例**：
```python
# ❌ 错误 - 硬编码\n
text = "line1\nline2"

# ✅ 正确 - 使用os.linesep
import os
text = f"line1{os.linesep}line2"
```

---

### Phase 2: 正确的包配置

#### 2.1 setup.py模板

```python
#!/usr/bin/env python3
"""
跨平台Python包配置示例
"""

from setuptools import setup, find_packages

setup(
    name="my-package",
    version="1.0.0",
    packages=find_packages(exclude=["test_*"]),
    python_requires=">=3.10",
    entry_points={
        "console_scripts": [
            "mycmd=my_package.cli:main",
        ],
    },
    classifiers=[
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
```

#### 2.2 pyproject.toml模板

```toml
[tool.poetry]
name = "my-package"
version = "1.0.0"
description = "跨平台Python包"
authors = ["author"]

[tool.poetry.dependencies]
python = "^3.10"
requests = "^2.31.0"

[tool.poetry.scripts]
mycmd = "my_package.cli:main"

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"
```

---

### Phase 3: 测试验证

#### 3.1 自动化测试

```python
import sys
import os

def test_cross_platform():
    """测试跨平台兼容性"""
    
    # 测试1: Python版本
    assert sys.version_info >= (3, 10), "需要Python 3.10+"
    
    # 测试2: 路径处理
    from pathlib import Path
    path = Path(".") / "test.txt"
    assert str(path) == "test.txt"
    
    # 测试3: 编码
    text = "测试中文"
    encoded = text.encode("utf-8")
    assert encoded.decode("utf-8") == text
    
    print("✅ 所有跨平台测试通过")

if __name__ == "__main__":
    test_cross_platform()
```

#### 3.2 GitHub Actions测试

```yaml
# .github/workflows/test.yml
name: Cross-platform Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -e .
      
      - name: Run tests
        run: |
          python test_cross_platform.py
```

---

## 检查清单

### 发布前检查

- [ ] 使用`Path`或`os.path`处理路径
- [ ] 避免bash专用命令
- [ ] 测试Python版本兼容性
- [ ] 测试不同操作系统
- [ ] 检查编码为UTF-8
- [ ] 验证包名不冲突

### 代码审查要点

- [ ] 没有硬编码路径
- [ ] 使用跨平台模块
- [ ] 避免os-specific代码

---

## 常用跨平台模块

| 模块 | 用途 |
|------|------|
| `os.path` | 路径处理 |
| `pathlib` | 现代化路径 |
| `subprocess` | 执行命令 |
| `platform` | 系统信息 |
| `shutil` | 文件操作 |
| `tempfile` | 临时文件 |

---

## 最佳实践

### 1. 路径处理

```python
from pathlib import Path

# ✅ 正确
data_dir = Path(__file__).parent / "data"
config_file = data_dir / "config.json"

# ❌ 错误
config_file = "/home/admin/.openclaw/workspace/data/config.json"
```

### 2. 执行命令

```python
import subprocess

# ✅ 正确 - 使用shell=False
result = subprocess.run(
    ["python", "--version"],
    capture_output=True,
    text=True,
    shell=False  # 避免Windows问题
)
```

### 3. 环境检测

```python
from sys import platform

if platform == "win32":
    # Windows
    config_path = Path(os.environ["APPDATA"]) / "myapp"
elif platform == "darwin":
    # macOS
    config_path = Path.home() / "Library" / "Application Support" / "myapp"
else:
    # Linux
    config_path = Path.home() / ".config" / "myapp"
```

---

## 总结

### 提升步骤

1. **意识** - 认识到跨平台问题
2. **学习** - 掌握跨平台模块
3. **实践** - 编写跨平台代码
4. **测试** - 多平台验证
5. **改进** - 从错误中学习

### 核心理念

> "Write once, run everywhere"

---

## GitHub

https://github.com/tianyuleishen/clawos
