# ClawOS GitHub Release

## Overview

This document summarizes the files included in the ClawOS GitHub release.

## Included Files

### Documentation

| File | Description |
|------|-------------|
| `README_GITHUB.md` | Main documentation (START HERE) |
| `INSTALL.md` | Installation instructions |
| `PROJECT_STRUCTURE.md` | Project structure reference |
| `COMPREHENSIVE_TEST_REPORT.md` | Benchmark results |

### Installation

| File | Description |
|------|-------------|
| `requirements.txt` | Python dependencies |
| `install.sh` | Linux/Mac installer |
| `install.bat` | Windows installer |
| `verify_install.py` | Installation verification |

### Core System

| File | Description |
|------|-------------|
| `main.py` | Main entry point |
| `comprehensive_test.py` | Benchmark testing suite |

### Source Code

| Directory | Description |
|-----------|-------------|
| `clawos/` | Main Python package |

## What's NOT Included

- Personal configuration files (`.openclaw/`)
- Git history (use `git clone` for full history)
- IDE configurations (`.vscode/`, `.idea/`)

## Installation

See [INSTALL.md](INSTALL.md) for detailed instructions.

## Quick Install

```bash
git clone https://github.com/tianyuleishen/clawos.git
cd clawos
pip install -r requirements.txt
python main.py
```

---

**GitHub**: https://github.com/tianyuleishen/clawos
