# 🦞 Keyboard Controller - 键盘控制器

"""
键盘控制器 - 跨平台键盘操作

功能:
- 输入文本
- 单键操作
- 组合键 (热键)
- 快捷键
- 粘贴/复制
"""

import asyncio
from typing import List, Optional, Union
from dataclasses import dataclass
from enum import Enum
import platform

class Key(Enum):
    """键盘按键"""
    # 字母
    A = "a"
    B = "b"
    C = "c"
    D = "d"
    E = "e"
    F = "f"
    G = "g"
    H = "h"
    I = "i"
    J = "j"
    K = "k"
    L = "l"
    M = "m"
    N = "n"
    O = "o"
    P = "p"
    Q = "q"
    R = "r"
    S = "s"
    T = "t"
    U = "u"
    V = "v"
    W = "w"
    X = "x"
    Y = "y"
    Z = "z"
    
    # 数字
    ZERO = "0"
    ONE = "1"
    TWO = "2"
    THREE = "3"
    FOUR = "4"
    FIVE = "5"
    SIX = "6"
    SEVEN = "7"
    EIGHT = "8"
    NINE = "9"
    
    # 功能键
    F1 = "f1"
    F2 = "f2"
    F3 = "f3"
    F4 = "f4"
    F5 = "f5"
    F6 = "f6"
    F7 = "f7"
    F8 = "f8"
    F9 = "f9"
    F10 = "f10"
    F11 = "f11"
    F12 = "f12"
    
    # 符号
    SPACE = "space"
    ENTER = "enter"
    ESCAPE = "esc"
    TAB = "tab"
    BACKSPACE = "backspace"
    DELETE = "delete"
    INSERT = "insert"
    HOME = "home"
    END = "end"
    PAGE_UP = "pageup"
    PAGE_DOWN = "pagedown"
    
    # 箭头
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"
    
    # 控制键
    CTRL = "ctrl"
    ALT = "alt"
    SHIFT = "shift"
    COMMAND = "command"  # macOS
    WINDOWS = "win"  # Windows
    
    # 标点
    COMMA = ","
    PERIOD = "."
    SLASH = "/"
    SEMICOLON = ";"
    COLON = ":"
    QUOTE = "'"
    BACKSLASH = "\\"
    BRACKET_LEFT = "["
    BRACKET_RIGHT = "]"
    EQUAL = "="
    MINUS = "-"
    GRAVE = "`"


class Hotkey(Enum):
    """常用组合键"""
    # 复制粘贴
    COPY = ("ctrl", "c")
    PASTE = ("ctrl", "v")
    CUT = ("ctrl", "x")
    SELECT_ALL = ("ctrl", "a")
    UNDO = ("ctrl", "z")
    REDO = ("ctrl", "y")
    SAVE = ("ctrl", "s")
    PRINT = ("ctrl", "p")
    NEW = ("ctrl", "n")
    OPEN = ("ctrl", "o")
    CLOSE = ("ctrl", "w")
    QUIT = ("ctrl", "q")
    FIND = ("ctrl", "f")
    REPLACE = ("ctrl", "h")
    TAB_SWITCH = ("ctrl", "tab")
    
    # macOS
    COPY_MAC = ("command", "c")
    PASTE_MAC = ("command", "v")
    SAVE_MAC = ("command", "s")
    QUIT_MAC = ("command", "q")


class KeyboardController:
    """键盘控制器"""
    
    def __init__(self):
        self.platform = platform.system()
        self._init_platform_specific()
        
        print(f"✅ Keyboard Controller 已加载 ({self.platform})")
    
    def _init_platform_specific(self):
        """初始化平台特定的实现"""
        
        if self.platform == "Windows":
            self.impl = WindowsKeyboardImpl()
        elif self.platform == "Darwin":  # macOS
            self.impl = MacOSKeyboardImpl()
        elif self.platform == "Linux":
            self.impl = LinuxKeyboardImpl()
        else:
            raise NotImplementedError(f"不支持的平台: {self.platform}")
    
    async def type_text(self, text: str, interval: float = 0.01):
        """输入文本
        
        Args:
            text: 要输入的文本
            interval: 字符间隔时间 (秒)
        """
        for char in text:
            await self.press_key(char)
            await asyncio.sleep(interval)
    
    async def type_text_fast(self, text: str):
        """快速输入文本"""
        await self.type_text(text, interval=0.001)
    
    async def press_key(self, key: Union[Key, str]):
        """按下并释放单个按键
        
        Args:
            key: 按键
        """
        key_str = key.value if isinstance(key, Key) else key.lower()
        await self.impl.key_down(key_str)
        await self.impl.key_up(key_str)
    
    async def key_down(self, key: Union[Key, str]):
        """按下按键"""
        key_str = key.value if isinstance(key, Key) else key.lower()
        await self.impl.key_down(key_str)
    
    async def key_up(self, key: Union[Key, str]):
        """释放按键"""
        key_str = key.value if isinstance(key, Key) else key.lower()
        await self.impl.key_up(key_str)
    
    async def hotkey(self, *keys: Union[Key, str]):
        """执行组合键
        
        Args:
            *keys: 按键序列 (从左到右按下，再从右到左释放)
        """
        # 按下所有键
        for key in keys:
            key_str = key.value if isinstance(key, Key) else key.lower()
            await self.impl.key_down(key_str)
        
        # 释放所有键 (反向)
        for key in reversed(keys):
            key_str = key.value if isinstance(key, Key) else key.lower()
            await self.impl.key_up(key_str)
    
    async def hotkey_by_name(self, hotkey: Hotkey):
        """使用预定义组合键"""
        await self.hotkey(*hotkey.value)
    
    # 常用快捷键
    async def copy(self):
        """复制 (Ctrl+C)"""
        if self.platform == "Darwin":
            await self.hotkey(Key.COMMAND, Key.C)
        else:
            await self.hotkey(Key.CTRL, Key.C)
    
    async def paste(self):
        """粘贴 (Ctrl+V)"""
        if self.platform == "Darwin":
            await self.hotkey(Key.COMMAND, Key.V)
        else:
            await self.hotkey(Key.CTRL, Key.V)
    
    async def cut(self):
        """剪切 (Ctrl+X)"""
        if self.platform == "Darwin":
            await self.hotkey(Key.COMMAND, Key.X)
        else:
            await self.hotkey(Key.CTRL, Key.X)
    
    async def select_all(self):
        """全选 (Ctrl+A)"""
        if self.platform == "Darwin":
            await self.hotkey(Key.COMMAND, Key.A)
        else:
            await self.hotkey(Key.CTRL, Key.A)
    
    async def undo(self):
        """撤销 (Ctrl+Z)"""
        if self.platform == "Darwin":
            await self.hotkey(Key.COMMAND, Key.Z)
        else:
            await self.hotkey(Key.CTRL, Key.Z)
    
    async def redo(self):
        """重做 (Ctrl+Y)"""
        if self.platform == "Darwin":
            await self.hotkey(Key.COMMAND, Key.SHIFT, Key.Z)
        else:
            await self.hotkey(Key.CTRL, Key.Y)
    
    async def save(self):
        """保存 (Ctrl+S)"""
        if self.platform == "Darwin":
            await self.hotkey(Key.COMMAND, Key.S)
        else:
            await self.hotkey(Key.CTRL, Key.S)
    
    async def new_window(self):
        """新建窗口 (Ctrl+N)"""
        if self.platform == "Darwin":
            await self.hotkey(Key.COMMAND, Key.N)
        else:
            await self.hotkey(Key.CTRL, Key.N)
    
    async def close_window(self):
        """关闭窗口 (Ctrl+W)"""
        if self.platform == "Darwin":
            await self.hotkey(Key.COMMAND, Key.W)
        else:
            await self.hotkey(Key.CTRL, Key.W)
    
    async def find(self):
        """查找 (Ctrl+F)"""
        if self.platform == "Darwin":
            await self.hotkey(Key.COMMAND, Key.F)
        else:
            await self.hotkey(Key.CTRL, Key.F)
    
    async def tab_next(self):
        """切换标签页 (Ctrl+Tab)"""
        if self.platform == "Darwin":
            await self.hotkey(Key.COMMAND, Key.TAB)
        else:
            await self.hotkey(Key.CTRL, Key.TAB)
    
    async def tab_previous(self):
        """切换到上一个标签页 (Ctrl+Shift+Tab)"""
        if self.platform == "Darwin":
            await self.hotkey(Key.COMMAND, Key.SHIFT, Key.TAB)
        else:
            await self.hotkey(Key.CTRL, Key.SHIFT, Key.TAB)
    
    async def go_back(self):
        """后退 (Alt+Left)"""
        if self.platform == "Darwin":
            await self.hotkey(Key.COMMAND, Key.LEFT)
        else:
            await self.hotkey(Key.ALT, Key.LEFT)
    
    async def go_forward(self):
        """前进 (Alt+Right)"""
        if self.platform == "Darwin":
            await self.hotkey(Key.COMMAND, Key.RIGHT)
        else:
            await self.hotkey(Key.ALT, Key.RIGHT)
    
    async def refresh(self):
        """刷新 (F5 或 Ctrl+R)"""
        if self.platform == "Darwin":
            await self.hotkey(Key.COMMAND, Key.R)
        else:
            await self.hotkey(Key.CTRL, Key.R)
    
    async def escape(self):
        """ESC键"""
        await self.press_key(Key.ESCAPE)
    
    async def enter(self):
        """Enter键"""
        await self.press_key(Key.ENTER)
    
    async def space(self):
        """空格键"""
        await self.press_key(Key.SPACE)
    
    async def tab(self):
        """Tab键"""
        await self.press_key(Key.TAB)
    
    async def backspace(self):
        """退格键"""
        await self.press_key(Key.BACKSPACE)
    
    async def delete(self):
        """Delete键"""
        await self.press_key(Key.DELETE)
    
    async def arrow_up(self):
        """上箭头"""
        await self.press_key(Key.UP)
    
    async def arrow_down(self):
        """下箭头"""
        await self.press_key(Key.DOWN)
    
    async def arrow_left(self):
        """左箭头"""
        await self.press_key(Key.LEFT)
    
    async def arrow_right(self):
        """右箭头"""
        await self.press_key(Key.RIGHT)
    
    async def page_up(self):
        """Page Up"""
        await self.press_key(Key.PAGE_UP)
    
    async def page_down(self):
        """Page Down"""
        await self.press_key(Key.PAGE_DOWN)
    
    async def home(self):
        """Home"""
        await self.press_key(Key.HOME)
    
    async def end_key(self):
        """End"""
        await self.press_key(Key.END)


class KeyboardImpl:
    """键盘实现基类"""
    
    async def key_down(self, key: str):
        raise NotImplementedError()
    
    async def key_up(self, key: str):
        raise NotImplementedError()


class WindowsKeyboardImpl(KeyboardImpl):
    """Windows平台实现"""
    
    def __init__(self):
        try:
            import pyautogui
            self.pyautogui = pyautogui
        except ImportError:
            raise ImportError("请安装pyautogui: pip install pyautogui")
    
    async def key_down(self, key: str):
        """按下"""
        self.pyautogui.keyDown(key)
    
    async def key_up(self, key: str):
        """释放"""
        self.pyautogui.keyUp(key)


class MacOSKeyboardImpl(KeyboardImpl):
    """macOS平台实现"""
    
    def __init__(self):
        try:
            import pyautogui
            self.pyautogui = pyautogui
        except ImportError:
            self.pyautogui = None
    
    async def key_down(self, key: str):
        """按下"""
        if self.pyautogui:
            self.pyautogui.keyDown(key)
        else:
            # AppleScript备用
            await self._key_applescript(key, "key down")
    
    async def key_up(self, key: str):
        """释放"""
        if self.pyautogui:
            self.pyautogui.keyUp(key)
        else:
            await self._key_applescript(key, "key up")
    
    async def _key_applescript(self, key: str, action: str):
        """AppleScript备用方案"""
        import subprocess
        script = f'tell application "System Events" to {action} {key}'
        subprocess.run(['osascript', '-e', script])


class LinuxKeyboardImpl(KeyboardImpl):
    """Linux平台实现"""
    
    def __init__(self):
        try:
            from pynput.keyboard import Controller
            self.controller = Controller()
            self._use_pynput = True
        except ImportError:
            self._use_pynput = False
        
        try:
            import pyautogui
            self.pyautogui = pyautogui
        except ImportError:
            self.pyautogui = None
    
    async def key_down(self, key: str):
        """按下"""
        if self._use_pynput:
            self.controller.press(key)
        elif self.pyautogui:
            self.pyautogui.keyDown(key)
        else:
            # xdotool备用
            import subprocess
            subprocess.run(['xdotool', 'keydown', key])
    
    async def key_up(self, key: str):
        """释放"""
        if self._use_pynput:
            self.controller.release(key)
        elif self.pyautogui:
            self.pyautogui.keyUp(key)
        else:
            import subprocess
            subprocess.run(['xdotool', 'keyup', key])


# 便捷函数
async def type_text(text: str, interval: float = 0.01):
    """输入文本"""
    controller = KeyboardController()
    await controller.type_text(text, interval)

async def copy():
    """复制"""
    controller = KeyboardController()
    await controller.copy()

async def paste():
    """粘贴"""
    controller = KeyboardController()
    await controller.paste()

# 测试代码
if __name__ == "__main__":
    async def test():
        print("⌨️ 键盘控制器测试")
        
        controller = KeyboardController()
        
        # 测试输入
        print("输入 'Hello World'...")
        await controller.type_text("Hello World", interval=0.05)
        
        # 测试快捷键
        print("全选 (Ctrl+A)...")
        await controller.select_all()
        
        print("✅ 测试完成")
    
    asyncio.run(test())
