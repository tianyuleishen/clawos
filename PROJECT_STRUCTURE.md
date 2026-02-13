# ClawOS Project Structure

## Overview

```
clawos/                          # Project root
│
├── Core System Files
│   ├── main.py                  # Main entry point
│   ├── comprehensive_test.py    # Benchmark testing suite
│   ├── requirements.txt         # Python dependencies
│   ├── install.sh               # Linux/Mac installer
│   ├── install.bat              # Windows installer
│   └── verify_install.py        # Installation verification
│
├── clawos/                       # Main package
│   ├── __init__.py
│   ├── main.py                  # ClawOS main module
│   │
│   ├── ai/                      # AI modules
│   │   ├── __init__.py
│   │   └── nlu.py               # Natural Language Understanding
│   │
│   ├── core/                    # Core reasoning engines
│   │   ├── __init__.py
│   │   └── reasoning/           # All reasoning optimizers
│   │       ├── __init__.py
│   │       ├── phase1_optimizer.py
│   │       ├── phase2_optimizer.py
│   │       ├── ...              # Phase 1-27 optimizers
│   │       └── *.py
│   │
│   ├── security/                # Security modules
│   │   ├── __init__.py
│   │   └── ...
│   │
│   ├── storage/                 # Data persistence
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── memory.py
│   │   ├── settings.py
│   │   └── conversation.py
│   │
│   ├── controls/                # System controls
│   │   ├── __init__.py
│   │   ├── keyboard.py
│   │   ├── mouse.py
│   │   ├── clipboard.py
│   │   └── window.py
│   │
│   ├── files/                   # File management
│   │   ├── __init__.py
│   │   ├── file.py
│   │   ├── directory.py
│   │   ├── search.py
│   │   └── batch.py
│   │
│   ├── gui/                     # GUI components
│   │   ├── __init__.py
│   │   ├── main_window.py
│   │   ├── chat_interface.py
│   │   └── control_panel.py
│   │
│   ├── plugins/                 # Plugin system
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── manager.py
│   │   ├── api.py
│   │   └── store.py
│   │
│   └── ui/                      # User interface
│       ├── __init__.py
│       └── gui/
│           └── __init__.py
│
├── docs/                        # Documentation
│   └── ...
│
├── skills/                      # Agent skills
│   ├── __init__.py
│   ├── understanding-enhancement/
│   └── ... (other skills)
│
├── tests/                       # Test files
│   └── ...
│
└── memory/                      # Session memory
    └── YYYY-MM-DD.md
```

## Key Directories

| Directory | Purpose | Lines of Code |
|-----------|---------|---------------|
| `clawos/core/reasoning/` | Reasoning optimization engines | ~10,000 |
| `clawos/ai/` | AI/NLU modules | ~500 |
| `clawos/storage/` | Data persistence | ~500 |
| `clawos/controls/` | System controls | ~500 |
| `clawos/files/` | File management | ~500 |
| `clawos/gui/` | GUI components | ~500 |
| `clawos/plugins/` | Plugin system | ~500 |

## File Types

| Extension | Count | Purpose |
|----------|-------|---------|
| `.py` | 50+ | Python source files |
| `.md` | 30+ | Documentation |
| `.json` | 5+ | Configuration & results |
| `.sh` | 1 | Installation script |
| `.bat` | 1 | Windows installer |

## Total Statistics

| Metric | Value |
|--------|-------|
| Python Files | 50+ |
| Documentation | 30+ |
| Total Lines | ~10,000+ |
| Phases | 27 Complete |
| Benchmarks | 6 Datasets |

---

## Related Files

- [README_GITHUB.md](README_GITHUB.md) - GitHub-ready overview
- [INSTALL.md](INSTALL.md) - Installation guide
- [COMPREHENSIVE_TEST_REPORT.md](COMPREHENSIVE_TEST_REPORT.md) - Benchmark results
