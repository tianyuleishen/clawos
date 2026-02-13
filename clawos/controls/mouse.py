# 🦞 Mouse Controller - 鼠标控制器

"""
鼠标控制器 - 跨平台鼠标操作

功能:
- 移动鼠标
- 点击操作 (左键/右键/中键)
- 双击
- 拖拽
- 滚轮滚动
- 获取位置
- 截图
"""

import asyncio
from typing import Optional, Tuple, List
from dataclasses import dataclass
from enum import Enum
import platform

class MouseButton(Enum):
    """鼠标按键"""
    LEFT = "left"
    RIGHT = "right"
    MIDDLE = "middle"

@dataclass
class MousePosition:
    """鼠标位置"""
    x: int
    y: int
    timestamp: float

class MouseController:
    """鼠标控制器"""
    
    def __init__(self):
        self.platform = platform.system()
        self._init_platform_specific()
        
        print(f"✅ Mouse Controller 已加载 ({self.platform})")
    
    def _init_platform_specific(self):
        """初始化平台特定的实现"""
        
        if self.platform == "Windows":
            self.impl = WindowsMouseImpl()
        elif self.platform == "Darwin":  # macOS
            self.impl = MacOSMouseImpl()
        elif self.platform == "Linux":
            self.impl = LinuxMouseImpl()
        else:
            raise NotImplementedError(f"不支持的平台: {self.platform}")
    
    async def move_to(self, x: int, y: int, duration: float = 0.1):
        """移动鼠标到指定位置
        
        Args:
            x: X坐标
            y: Y坐标
            duration: 移动时间 (秒)
        """
        await self.impl.smooth_move(x, y, duration)
    
    async def move_relative(self, dx: int, dy: int, duration: float = 0.1):
        """相对移动
        
        Args:
            dx: X偏移
            dy: Y偏移
            duration: 移动时间
        """
        current = self.get_position()
        await self.impl.smooth_move(current.x + dx, current.y + dy, duration)
    
    async def click(
        self, 
        x: Optional[int] = None, 
        y: Optional[int] = None, 
        button: MouseButton = MouseButton.LEFT,
        clicks: int = 1
    ):
        """点击鼠标
        
        Args:
            x, y: 坐标 (None=当前位置)
            button: 按键
            clicks: 点击次数
        """
        if x is not None and y is not None:
            await self.impl.smooth_move(x, y, 0.05)
        
        for _ in range(clicks):
            await self.impl.press(button.value)
            await self.impl.release(button.value)
            await asyncio.sleep(0.05)
    
    async def double_click(
        self, 
        x: Optional[int] = None, 
        y: Optional[int] = None,
        button: MouseButton = MouseButton.LEFT
    ):
        """双击"""
        await self.click(x, y, button, clicks=2)
    
    async def right_click(
        self, 
        x: Optional[int] = None, 
        y: Optional[int] = None
    ):
        """右键点击"""
        await self.click(x, y, MouseButton.RIGHT)
    
    async def middle_click(
        self, 
        x: Optional[int] = None, 
        y: Optional[int] = None
    ):
        """中键点击"""
        await self.click(x, y, MouseButton.MIDDLE)
    
    async def scroll(
        self, 
        amount: int, 
        direction: str = "down"
    ):
        """滚轮滚动
        
        Args:
            amount: 滚动量
            direction: "up" 或 "down"
        """
        if direction == "up":
            await self.impl.scroll(amount)
        else:
            await self.impl.scroll(-amount)
    
    async def scroll_horizontal(self, amount: int, direction: str = "right"):
        """水平滚动"""
        if direction == "right":
            await self.impl.scroll_horizontal(amount)
        else:
            await self.impl.scroll_horizontal(-amount)
    
    async def drag(
        self, 
        x1: int, y1: int, 
        x2: int, y2: int, 
        duration: float = 0.5
    ):
        """拖拽
        
        Args:
            x1, y1: 起始位置
            x2, y2: 结束位置
            duration: 拖拽时间
        """
        # 移动到起始位置
        await self.impl.smooth_move(x1, y1, 0.05)
        
        # 按下
        await self.impl.press(MouseButton.LEFT.value)
        
        # 拖动到目标位置
        await self.impl.smooth_move(x2, y2, duration)
        
        # 释放
        await self.impl.release(MouseButton.LEFT.value)
    
    def get_position(self) -> MousePosition:
        """获取当前鼠标位置"""
        pos = self.impl.get_position()
        import time
        return MousePosition(
            x=pos[0], 
            y=pos[1], 
            timestamp=time.time()
        )
    
    async def screenshot(self) -> bytes:
        """截图
        
        Returns:
            bytes: PNG格式的截图数据
        """
        return await self.impl.screenshot()


class WindowsMouseImpl:
    """Windows平台实现"""
    
    def __init__(self):
        try:
            import pyautogui
            self.pyautogui = pyautogui
            self.FAILSAFE = False
            self.PAUSE = 0
        except ImportError:
            raise ImportError("请安装pyautogui: pip install pyautogui")
    
    async def smooth_move(self, x: int, y: int, duration: float = 0.1):
        """平滑移动"""
        self.pyautogui.moveTo(x, y, duration=duration)
    
    def press(self, button: str):
        """按下"""
        self.pyautogui.mouseDown(button=button)
    
    def release(self, button: str):
        """释放"""
        self.pyautogui.mouseUp(button=button)
    
    def scroll(self, amount: int):
        """滚动"""
        self.pyautogui.scroll(amount)
    
    def scroll_horizontal(self, amount: int):
        """水平滚动"""
        self.pyautogui.hscroll(amount)
    
    def get_position(self) -> Tuple[int, int]:
        """获取位置"""
        return self.pyautogui.position()
    
    async def screenshot(self) -> bytes:
        """截图"""
        import pyautogui
        import io
        img = pyautogui.screenshot()
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        return buffer.getvalue()


class MacOSMouseImpl:
    """macOS平台实现"""
    
    def __init__(self):
        try:
            import pyautogui
            self.pyautogui = pyautogui
            self.FAILSAFE = False
            self.PAUSE = 0
        except ImportError:
            # macOS备用方案
            self._use_appscript = False
    
    async def smooth_move(self, x: int, y: int, duration: float = 0.1):
        """平滑移动"""
        try:
            import pyautogui
            self.pyautogui.moveTo(x, y, duration=duration)
        except:
            # 使用applescript备用
            await self._move_applescript(x, y)
    
    async def _move_applescript(self, x: int, y: int):
        """AppleScript备用方案"""
        import subprocess
        script = f'tell application "System Events" to set position of mouse cursor to {{{x}, {y}}}'
        subprocess.run(['osascript', '-e', script])
    
    def press(self, button: str):
        """按下"""
        try:
            import pyautogui
            self.pyautogui.mouseDown(button=button)
        except:
            pass
    
    def release(self, button: str):
        """释放"""
        try:
            import pyautogui
            self.pyautogui.mouseUp(button=button)
        except:
            pass
    
    def scroll(self, amount: int):
        """滚动"""
        try:
            import pyautogui
            self.pyautogui.scroll(amount)
        except:
            pass
    
    def scroll_horizontal(self, amount: int):
        """水平滚动"""
        pass  # macOS pyautogui可能不支持
    
    def get_position(self) -> Tuple[int, int]:
        """获取位置"""
        try:
            import pyautogui
            return self.pyautogui.position()
        except:
            return (0, 0)
    
    async def screenshot(self) -> bytes:
        """截图"""
        try:
            import pyautogui
            import io
            img = pyautogui.screenshot()
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            return buffer.getvalue()
        except:
            return b''


class LinuxMouseImpl:
    """Linux平台实现"""
    
    def __init__(self):
        # Linux使用python-libinput或备用方案
        self._use_xlib = False
        try:
            from pynput.mouse import Controller
            self.controller = Controller()
            self._use_xlib = True
        except ImportError:
            try:
                import pyautogui
                self.pyautogui = pyautogui
            except ImportError:
                pass
    
    async def smooth_move(self, x: int, y: int, duration: float = 0.1):
        """平滑移动"""
        if self._use_xlib:
            self.controller.position = (x, y)
        else:
            try:
                import pyautogui
                self.pyautogui.moveTo(x, y, duration=duration)
            except:
                # 使用xdotool备用
                import subprocess
                subprocess.run(['xdotool', 'mousemove', str(x), str(y)])
    
    def press(self, button: str):
        """按下"""
        if self._use_xlib:
            if button == "left":
                self.controller.press(Controller.Button.left)
            elif button == "right":
                self.controller.press(Controller.Button.right)
            elif button == "middle":
                self.controller.press(Controller.Button.middle)
    
    def release(self, button: str):
        """释放"""
        if self._use_xlib:
            if button == "left":
                self.controller.release(Controller.Button.left)
            elif button == "right":
                self.controller.release(Controller.Button.right)
            elif button == "middle":
                self.controller.release(Controller.Button.middle)
    
    def scroll(self, amount: int):
        """滚动"""
        if self._use_xlib:
            self.controller.scroll(0, amount)
    
    def scroll_horizontal(self, amount: int):
        """水平滚动"""
        if self._use_xlib:
            self.controller.scroll(amount, 0)
    
    def get_position(self) -> Tuple[int, int]:
        """获取位置"""
        if self._use_xlib:
            return self.controller.position
        else:
            return (0, 0)
    
    async def screenshot(self) -> bytes:
        """截图"""
        try:
            import pyautogui
            import io
            img = pyautogui.screenshot()
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            return buffer.getvalue()
        except:
            return b''


# 便捷函数
async def get_mouse_position() -> MousePosition:
    """获取鼠标位置"""
    controller = MouseController()
    return controller.get_position()

async def click_at(x: int, y: int):
    """在指定位置点击"""
    controller = MouseController()
    await controller.click(x, y)

# 测试代码
if __name__ == "__main__":
    async def test():
        print("🖱️ 鼠标控制器测试")
        
        controller = MouseController()
        
        # 测试获取位置
        pos = controller.get_position()
        print(f"当前鼠标位置: ({pos.x}, {pos.y})")
        
        # 测试移动
        print("移动到 (100, 100)...")
        await controller.move_to(100, 100, 0.2)
        
        # 测试点击
        print("点击...")
        await controller.click(100, 100)
        
        # 测试拖拽
        print("拖拽从 (100,100) 到 (200,200)...")
        await controller.drag(100, 100, 200, 200, 0.3)
        
        print("✅ 测试完成")
    
    asyncio.run(test())
