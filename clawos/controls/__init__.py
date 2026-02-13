# 🦞 ClawOS Controls - 电脑控制模块

"""
电脑控制模块 - 鼠标、键盘、窗口、剪贴板

功能:
- Mouse Controller (鼠标控制)
- Keyboard Controller (键盘控制)
- Window Manager (窗口管理)
- Clipboard Manager (剪贴板管理)
"""

from .mouse import MouseController, MouseButton, MousePosition
from .keyboard import KeyboardController, Key, Hotkey
from .window import WindowManager, WindowInfo, WindowState
from .clipboard import ClipboardManager, ClipboardContent, ClipboardType

__all__ = [
    # 鼠标
    'MouseController',
    'MouseButton',
    'MousePosition',
    
    # 键盘
    'KeyboardController',
    'Key',
    'Hotkey',
    
    # 窗口
    'WindowManager',
    'WindowInfo',
    'WindowState',
    
    # 剪贴板
    'ClipboardManager',
    'ClipboardContent',
    'ClipboardType',
]
