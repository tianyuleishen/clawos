#!/usr/bin/env python3
"""
🦞 ClawOS 主入口
使用: python -m clawos
"""

import sys
import os

sys.path.insert(0, '/home/admin/.openclaw/workspace')

from clawos.main import main

if __name__ == "__main__":
    main()
