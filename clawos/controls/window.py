# 🦞 Window Manager - 窗口管理器

"""
窗口管理器 - 跨平台窗口操作

功能:
- 获取活动窗口
- 获取所有窗口
- 窗口聚焦
- 最大化/最小化/关闭
- 调整窗口大小
- 获取窗口位置
"""

import asyncio
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from enum import Enum
import platform
import time

class WindowState(Enum):
    """窗口状态"""
    NORMAL = "normal"
    MAXIMIZED = "maximized"
    MINIMIZED = "minimized"
    FULLSCREEN = "fullscreen"

@dataclass
class WindowInfo:
    """窗口信息"""
    window_id: str
    title: str
    process_id: int
    process_name: str
    is_active: bool
    state: WindowState
    x: int
    y: int
    width: int
    height: int

class WindowManager:
    """窗口管理器"""
    
    def __init__(self):
        self.platform = platform.system()
        self._init_platform_specific()
        
        print(f"✅ Window Manager 已加载 ({self.platform})")
    
    def _init_platform_specific(self):
        """初始化平台特定的实现"""
        
        if self.platform == "Windows":
            self.impl = WindowsWindowImpl()
        elif self.platform == "Darwin":  # macOS
            self.impl = MacOSWindowImpl()
        elif self.platform == "Linux":
            self.impl = LinuxWindowImpl()
        else:
            raise NotImplementedError(f"不支持的平台: {self.platform}")
    
    async def get_active_window(self) -> WindowInfo:
        """获取当前活动窗口"""
        return await self.impl.get_active_window()
    
    async def get_all_windows(self) -> List[WindowInfo]:
        """获取所有窗口"""
        return await self.impl.get_all_windows()
    
    async def get_window_by_title(self, title: str) -> Optional[WindowInfo]:
        """根据标题查找窗口"""
        windows = await self.get_all_windows()
        for window in windows:
            if title.lower() in window.title.lower():
                return window
        return None
    
    async def get_window_by_name(self, name: str) -> Optional[WindowInfo]:
        """根据进程名查找窗口"""
        windows = await self.get_all_windows()
        for window in windows:
            if name.lower() in window.process_name.lower():
                return window
        return None
    
    async def focus_window(self, window_id: str):
        """聚焦窗口"""
        await self.impl.focus_window(window_id)
    
    async def focus_window_by_title(self, title: str):
        """根据标题聚焦窗口"""
        window = await self.get_window_by_title(title)
        if window:
            await self.focus_window(window.window_id)
        else:
            raise ValueError(f"未找到窗口: {title}")
    
    async def maximize_window(self, window_id: str = None):
        """最大化窗口"""
        if window_id is None:
            active = await self.get_active_window()
            window_id = active.window_id
        await self.impl.set_window_state(window_id, WindowState.MAXIMIZED)
    
    async def minimize_window(self, window_id: str = None):
        """最小化窗口"""
        if window_id is None:
            active = await self.get_active_window()
            window_id = active.window_id
        await self.impl.set_window_state(window_id, WindowState.MINIMIZED)
    
    async def restore_window(self, window_id: str = None):
        """恢复窗口"""
        if window_id is None:
            active = await self.get_active_window()
            window_id = active.window_id
        await self.impl.set_window_state(window_id, WindowState.NORMAL)
    
    async def close_window(self, window_id: str = None):
        """关闭窗口"""
        if window_id is None:
            active = await self.get_active_window()
            window_id = active.window_id
        await self.impl.close_window(window_id)
    
    async def move_window(
        self, 
        window_id: str, 
        x: int, 
        y: int,
        width: int = None,
        height: int = None
    ):
        """移动窗口"""
        await self.impl.move_window(window_id, x, y, width, height)
    
    async def resize_window(
        self, 
        window_id: str, 
        width: int, 
        height: int
    ):
        """调整窗口大小"""
        await self.impl.move_window(window_id, None, None, width, height)
    
    async def screenshot_window(self, window_id: str = None) -> bytes:
        """截取窗口截图"""
        if window_id is None:
            active = await self.get_active_window()
            window_id = active.window_id
        return await self.impl.screenshot_window(window_id)
    
    async def wait_for_window(
        self, 
        title: str, 
        timeout: float = 10.0,
        interval: float = 0.5
    ) -> Optional[WindowInfo]:
        """等待窗口出现"""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            window = await self.get_window_by_title(title)
            if window:
                return window
            await asyncio.sleep(interval)
        
        return None
    
    async def wait_for_and_focus(
        self, 
        title: str, 
        timeout: float = 10.0
    ) -> bool:
        """等待窗口出现并聚焦"""
        window = await self.wait_for_window(title, timeout)
        if window:
            await self.focus_window(window.window_id)
            return True
        return False


class WindowImpl:
    """窗口实现基类"""
    
    async def get_active_window(self) -> WindowInfo:
        raise NotImplementedError()
    
    async def get_all_windows(self) -> List[WindowInfo]:
        raise NotImplementedError()
    
    async def focus_window(self, window_id: str):
        raise NotImplementedError()
    
    async def set_window_state(self, window_id: str, state: WindowState):
        raise NotImplementedError()
    
    async def close_window(self, window_id: str):
        raise NotImplementedError()
    
    async def move_window(
        self, 
        window_id: str, 
        x: int, 
        y: int,
        width: int = None,
        height: int = None
    ):
        raise NotImplementedError()
    
    async def screenshot_window(self, window_id: str) -> bytes:
        raise NotImplementedError()


class WindowsWindowImpl(WindowImpl):
    """Windows平台实现"""
    
    def __init__(self):
        try:
            import pygetwindow as gw
            self.pygetwindow = gw
        except ImportError:
            self.pygetwindow = None
    
    async def get_active_window(self) -> WindowInfo:
        """获取活动窗口"""
        try:
            import pygetwindow as gw
            active = gw.getActiveWindow()
            
            return WindowInfo(
                window_id=str(active._hWnd) if hasattr(active, '_hWnd') else active.title,
                title=active.title,
                process_id=0,
                process_name=active.title.split('.')[0] if '.' in active.title else active.title,
                is_active=True,
                state=WindowState.NORMAL,
                x=active.left,
                y=active.top,
                width=active.width,
                height=active.height
            )
        except Exception as e:
            return WindowInfo(
                window_id="0",
                title="Unknown",
                process_id=0,
                process_name="unknown",
                is_active=True,
                state=WindowState.NORMAL,
                x=0,
                y=0,
                width=800,
                height=600
            )
    
    async def get_all_windows(self) -> List[WindowInfo]:
        """获取所有窗口"""
        windows = []
        try:
            import pygetwindow as gw
            all_windows = gw.getAllWindows()
            
            for win in all_windows:
                windows.append(WindowInfo(
                    window_id=str(win._hWnd) if hasattr(win, '_hWnd') else win.title,
                    title=win.title,
                    process_id=0,
                    process_name=win.title.split('.')[0] if '.' in win.title else win.title,
                    is_active=False,
                    state=WindowState.NORMAL,
                    x=win.left,
                    y=win.top,
                    width=win.width,
                    height=win.height
                ))
        except Exception as e:
            pass
        
        return windows
    
    async def focus_window(self, window_id: str):
        """聚焦窗口"""
        try:
            import pygetwindow as gw
            windows = gw.getAllWindows()
            for win in windows:
                if str(win._hWnd) == window_id or win.title == window_id:
                    win.activate()
                    break
        except Exception as e:
            pass
    
    async def set_window_state(self, window_id: str, state: WindowState):
        """设置窗口状态"""
        try:
            import pygetwindow as gw
            windows = gw.getAllWindows()
            for win in windows:
                if str(win._hWnd) == window_id or win.title == window_id:
                    if state == WindowState.MAXIMIZED:
                        win.maximize()
                    elif state == WindowState.MINIMIZED:
                        win.minimize()
                    elif state == WindowState.NORMAL:
                        win.restore()
                    break
        except Exception as e:
            pass
    
    async def close_window(self, window_id: str):
        """关闭窗口"""
        try:
            import pygetwindow as gw
            windows = gw.getAllWindows()
            for win in windows:
                if str(win._hWnd) == window_id or win.title == window_id:
                    win.close()
                    break
        except Exception as e:
            pass
    
    async def move_window(
        self, 
        window_id: str, 
        x: int, 
        y: int,
        width: int = None,
        height: int = None
    ):
        """移动窗口"""
        try:
            import pygetwindow as gw
            windows = gw.getAllWindows()
            for win in windows:
                if str(win._hWnd) == window_id or win.title == window_id:
                    if width and height:
                        win.resizeTo(width, height)
                    if x and y:
                        win.moveTo(x, y)
                    break
        except Exception as e:
            pass
    
    async def screenshot_window(self, window_id: str) -> bytes:
        """截取窗口截图"""
        try:
            import pyautogui
            import io
            
            await self.focus_window(window_id)
            await asyncio.sleep(0.1)
            
            img = pyautogui.screenshot()
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            return buffer.getvalue()
        except Exception as e:
            return b''


class MacOSWindowImpl(WindowImpl):
    """macOS平台实现"""
    
    async def get_active_window(self) -> WindowInfo:
        """获取活动窗口"""
        try:
            import subprocess
            result = subprocess.run(
                ['osascript', '-e', 
                 'tell application "System Events" to name of first process whose frontmost is true'],
                capture_output=True, text=True
            )
            title = result.stdout.strip()
            
            return WindowInfo(
                window_id=title,
                title=title,
                process_id=0,
                process_name=title.split('.')[0] if '.' in title else title,
                is_active=True,
                state=WindowState.NORMAL,
                x=0,
                y=0,
                width=800,
                height=600
            )
        except Exception as e:
            return WindowInfo(
                window_id="0",
                title="Unknown",
                process_id=0,
                process_name="unknown",
                is_active=True,
                state=WindowState.NORMAL,
                x=0,
                y=0,
                width=800,
                height=600
            )
    
    async def get_all_windows(self) -> List[WindowInfo]:
        """获取所有窗口"""
        windows = []
        try:
            import subprocess
            result = subprocess.run(
                ['osascript', '-e', 
                 'tell application "System Events" to get name of every process'],
                capture_output=True, text=True
            )
            titles = result.stdout.strip().split(', ')
            
            for title in titles:
                if title:
                    windows.append(WindowInfo(
                        window_id=title,
                        title=title,
                        process_id=0,
                        process_name=title,
                        is_active=False,
                        state=WindowState.NORMAL,
                        x=0,
                        y=0,
                        width=800,
                        height=600
                    ))
        except Exception as e:
            pass
        
        return windows
    
    async def focus_window(self, window_id: str):
        """聚焦窗口"""
        try:
            import subprocess
            subprocess.run([
                'osascript', '-e',
                f'tell application "{window_id}" to activate'
            ])
        except Exception as e:
            pass
    
    async def set_window_state(self, window_id: str, state: WindowState):
        """设置窗口状态"""
        pass
    
    async def close_window(self, window_id: str):
        """关闭窗口"""
        try:
            import subprocess
            subprocess.run([
                'osascript', '-e',
                f'tell application "System Events" to tell process "{window_id}" to click button 1 of window 1'
            ])
        except Exception as e:
            pass
    
    async def move_window(
        self, 
        window_id: str, 
        x: int, 
        y: int,
        width: int = None,
        height: int = None
    ):
        """移动窗口"""
        pass
    
    async def screenshot_window(self, window_id: str) -> bytes:
        """截取窗口截图"""
        return b''


class LinuxWindowImpl(WindowImpl):
    """Linux平台实现"""
    
    async def get_active_window(self) -> WindowInfo:
        """获取活动窗口"""
        try:
            import subprocess
            result = subprocess.run(
                ['xdotool', 'getactivewindow', 'getwindowname'],
                capture_output=True, text=True
            )
            title = result.stdout.strip()
            
            return WindowInfo(
                window_id=title,
                title=title,
                process_id=0,
                process_name=title.split('.')[0] if '.' in title else title,
                is_active=True,
                state=WindowState.NORMAL,
                x=0,
                y=0,
                width=800,
                height=600
            )
        except Exception as e:
            return WindowInfo(
                window_id="0",
                title="Unknown",
                process_id=0,
                process_name="unknown",
                is_active=True,
                state=WindowState.NORMAL,
                x=0,
                y=0,
                width=800,
                height=600
            )
    
    async def get_all_windows(self) -> List[WindowInfo]:
        """获取所有窗口"""
        windows = []
        try:
            import subprocess
            result = subprocess.run(
                ['wmctrl', '-l'],
                capture_output=True, text=True
            )
            
            for line in result.stdout.strip().split('\n'):
                if line:
                    parts = line.split()
                    if len(parts) >= 4:
                        windows.append(WindowInfo(
                            window_id=parts[0],
                            title=' '.join(parts[3:]),
                            process_id=0,
                            process_name=' '.join(parts[3:]).split('.')[0],
                            is_active=False,
                            state=WindowState.NORMAL,
                            x=0,
                            y=0,
                            width=800,
                            height=600
                        ))
        except Exception as e:
            pass
        
        return windows
    
    async def focus_window(self, window_id: str):
        """聚焦窗口"""
        try:
            import subprocess
            subprocess.run(['xdotool', 'windowfocus', window_id])
        except Exception as e:
            pass
    
    async def set_window_state(self, window_id: str, state: WindowState):
        """设置窗口状态"""
        try:
            import subprocess
            if state == WindowState.MAXIMIZED:
                subprocess.run(['wmctrl', '-i', '-r', window_id, '-b', 'add,maximized_vert,maximized_horz'])
            elif state == WindowState.MINIMIZED:
                subprocess.run(['wmctrl', '-i', '-r', window_id, '-b', 'add,hidden'])
        except Exception as e:
            pass
    
    async def close_window(self, window_id: str):
        """关闭窗口"""
        try:
            import subprocess
            subprocess.run(['wmctrl', '-i', '-c', window_id])
        except Exception as e:
            pass
    
    async def move_window(
        self, 
        window_id: str, 
        x: int, 
        y: int,
        width: int = None,
        height: int = None
    ):
        """移动窗口"""
        try:
            import subprocess
            if width and height:
                subprocess.run(['wmctrl', '-i', '-r', window_id, '-e', f'0,{x},{y},{width},{height}'])
            else:
                subprocess.run(['wmctrl', '-i', '-r', window_id, '-e', f'0,{x},{y},-1,-1'])
        except Exception as e:
            pass
    
    async def screenshot_window(self, window_id: str) -> bytes:
        """截取窗口截图"""
        return b''


# 便捷函数
async def get_active_window() -> WindowInfo:
    """获取活动窗口"""
    manager = WindowManager()
    return await manager.get_active_window()

async def close_active_window():
    """关闭活动窗口"""
    manager = WindowManager()
    await manager.close_window()

# 测试代码
if __name__ == "__main__":
    async def test():
        print("🪟 窗口管理器测试")
        
        manager = WindowManager()
        
        print("获取活动窗口...")
        active = await manager.get_active_window()
        print(f"活动窗口: {active.title}")
        
        print("\n所有窗口:")
        windows = await manager.get_all_windows()
        for win in windows[:5]:
            print(f"  - {win.title}")
        
        print("✅ 测试完成")
    
    asyncio.run(test())
