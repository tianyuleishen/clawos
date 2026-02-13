# Installation Guide

## Prerequisites

- **Python**: 3.10 or higher
- **Operating System**: Linux, macOS, or Windows
- **Memory**: 4GB RAM minimum (8GB recommended)
- **Storage**: 500MB free space

---

## Quick Install

### Linux/macOS

```bash
# Clone the repository
git clone https://github.com/tianyuleishen/clawos.git
cd clawos

# Make installation script executable
chmod +x install.sh

# Run installation
./install.sh

# Activate environment (if using conda/venv)
source venv/bin/activate  # Linux
source venv/bin/activate  # macOS

# Run the system
python main.py
```

### Windows

```bash
# Clone the repository
git clone https://github.com/tianyuleishen/clawos.git
cd clawos

# Run installation script
install.bat

# Run the system
python main.py
```

---

## Manual Installation

### Step 1: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
# Linux/macOS:
source venv/bin/activate

# Windows:
venv\Scripts\activate
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Verify Installation

```bash
python verify_install.py
```

### Step 4: Run Tests

```bash
# Run comprehensive benchmarks
python comprehensive_test.py
```

---

## Dependencies

```
# Core
python>=3.10

# All dependencies are listed in requirements.txt
```

---

## Troubleshooting

### Python Version Error

Make sure Python 3.10+ is installed:
```bash
python --version
```

### Pip Install Fails

Try upgrading pip first:
```bash
pip install --upgrade pip
```

### Permission Errors (Linux/macOS)

```bash
# Use sudo or install in user space
pip install --user -r requirements.txt
```

---

## Next Steps

1. Read [README_GITHUB.md](README_GITHUB.md) for feature overview
2. Run `python comprehensive_test.py` to verify benchmarks
3. Explore `clawos/` directory for core modules

---

## Support

- GitHub Issues: https://github.com/tianyuleishen/clawos/issues
- Report bugs and feature requests
