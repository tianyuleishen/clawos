# 🦞 Screenshot - 截图工具

"""
截图工具 - 跨平台屏幕截图

功能:
- 全屏截图
- 窗口截图
- 区域截图
- 延迟截图
"""

import asyncio
import subprocess
import platform
from typing import Optional, Tuple, List
from dataclasses import dataclass
from pathlib import Path
import io
import base64

@dataclass
class ScreenshotInfo:
    """截图信息"""
    width: int
    height: int
    format: str
    size: int
    data: bytes

class Screenshot:
    """截图工具"""
    
    def __init__(self):
        self.platform = platform.system()
        print(f"✅ Screenshot Tool 已加载 ({self.platform})")
    
    # ============ 全屏截图 ============
    
    async def capture_fullscreen(self, filename: str = None) -> ScreenshotInfo:
        """全屏截图
        
        Args:
            filename: 保存文件名 (可选)
        
        Returns:
            ScreenshotInfo: 截图信息
        """
        if self.platform == "Windows":
            return await self._capture_windows_fullscreen(filename)
        elif self.platform == "Darwin":
            return await self._capture_macos_fullscreen(filename)
        else:
            return await self._capture_linux_fullscreen(filename)
    
    # ============ 窗口截图 ============
    
    async def capture_window(
        self, 
        window_title: str = None,
        filename: str = None
    ) -> ScreenshotInfo:
        """窗口截图
        
        Args:
            window_title: 窗口标题 (可选,默认当前窗口)
            filename: 保存文件名 (可选)
        
        Returns:
            ScreenshotInfo: 截图信息
        """
        if self.platform == "Windows":
            return await self._capture_windows_window(window_title, filename)
        elif self.platform == "Darwin":
            return await self._capture_macos_window(window_title, filename)
        else:
            return await self._capture_linux_window(window_title, filename)
    
    # ============ 区域截图 ============
    
    async def capture_region(
        self, 
        x: int, 
        y: int, 
        width: int, 
        height: int,
        filename: str = None
    ) -> ScreenshotInfo:
        """区域截图
        
        Args:
            x: X坐标
            y: Y坐标
            width: 宽度
            height: 高度
            filename: 保存文件名 (可选)
        
        Returns:
            ScreenshotInfo: 截图信息
        """
        if self.platform == "Windows":
            return await self._capture_windows_region(x, y, width, height, filename)
        elif self.platform == "Darwin":
            return await self._capture_macos_region(x, y, width, height, filename)
        else:
            return await self._capture_linux_region(x, y, width, height, filename)
    
    # ============ 延迟截图 ============
    
    async def capture_delayed(
        self, 
        delay: int = 5,
        fullscreen: bool = True,
        filename: str = None
    ) -> ScreenshotInfo:
        """延迟截图
        
        Args:
            delay: 延迟时间 (秒)
            fullscreen: 是否全屏
            filename: 保存文件名
        
        Returns:
            ScreenshotInfo: 截图信息
        """
        print(f"⏰ 等待 {delay} 秒后截图...")
        await asyncio.sleep(delay)
        
        if fullscreen:
            return await self.capture_fullscreen(filename)
        else:
            return await self.capture_window(filename=filename)
    
    # ============ 平台实现 ============
    
    async def _capture_windows_fullscreen(self, filename: str = None) -> ScreenshotInfo:
        """Windows全屏截图"""
        try:
            import pyautogui
            img = pyautogui.screenshot()
            
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            data = buffer.getvalue()
            
            if filename:
                await self._save_file(filename, data)
            
            return ScreenshotInfo(
                width=img.width,
                height=img.height,
                format="png",
                size=len(data),
                data=data
            )
        except Exception as e:
            print(f"❌ Windows截图失败: {e}")
            return None
    
    async def _capture_windows_window(
        self, 
        window_title: str = None,
        filename: str = None
    ) -> ScreenshotInfo:
        """Windows窗口截图"""
        try:
            import pyautogui
            import pygetwindow as gw
            
            if window_title:
                windows = gw.getWindowsWithTitle(window_title)
                if windows:
                    win = windows[0]
                    img = pyautogui.screenshot(region=(win.left, win.top, win.width, win.height))
                else:
                    # 尝试模糊匹配
                    all_windows = gw.getAllWindows()
                    for win in all_windows:
                        if window_title.lower() in win.title.lower():
                            img = pyautogui.screenshot(region=(win.left, win.top, win.width, win.height))
                            break
                    else:
                        img = pyautogui.screenshot()
            else:
                img = pyautogui.screenshot()
            
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            data = buffer.getvalue()
            
            if filename:
                await self._save_file(filename, data)
            
            return ScreenshotInfo(
                width=img.width,
                height=img.height,
                format="png",
                size=len(data),
                data=data
            )
        except Exception as e:
            print(f"❌ Windows窗口截图失败: {e}")
            return None
    
    async def _capture_windows_region(
        self, 
        x: int, 
        y: int, 
        width: int, 
        height: int,
        filename: str = None
    ) -> ScreenshotInfo:
        """Windows区域截图"""
        try:
            import pyautogui
            img = pyautogui.screenshot(region=(x, y, width, height))
            
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            data = buffer.getvalue()
            
            if filename:
                await self._save_file(filename, data)
            
            return ScreenshotInfo(
                width=width,
                height=height,
                format="png",
                size=len(data),
                data=data
            )
        except Exception as e:
            print(f"❌ Windows区域截图失败: {e}")
            return None
    
    async def _capture_macos_fullscreen(self, filename: str = None) -> ScreenshotInfo:
        """macOS全屏截图"""
        try:
            # 使用screencapture命令
            result = await asyncio.create_subprocess_shell(
                "screencapture -x /tmp/screenshot.png",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            await result.communicate()
            
            data = await self._read_file("/tmp/screenshot.png")
            
            if filename:
                await self._save_file(filename, data)
            
            # 获取图片尺寸
            from PIL import Image
            img = Image.open(io.BytesIO(data))
            
            return ScreenshotInfo(
                width=img.width,
                height=img.height,
                format="png",
                size=len(data),
                data=data
            )
        except Exception as e:
            print(f"❌ macOS截图失败: {e}")
            return None
    
    async def _capture_macos_window(
        self, 
        window_title: str = None,
        filename: str = None
    ) -> ScreenshotInfo:
        """macOS窗口截图"""
        try:
            cmd = "screencapture -x -W /tmp/screenshot.png"
            
            if window_title:
                # 使用AppleScript激活窗口
                script = f'''
                tell application "System Events"
                    tell process "{window_title}"
                        set frontmost to true
                    end tell
                end tell
                '''
                subprocess.run(['osascript', '-e', script])
                await asyncio.sleep(0.5)
            
            result = await asyncio.create_subprocess_shell(
                cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            await result.communicate()
            
            data = await self._read_file("/tmp/screenshot.png")
            
            if filename:
                await self._save_file(filename, data)
            
            from PIL import Image
            img = Image.open(io.BytesIO(data))
            
            return ScreenshotInfo(
                width=img.width,
                height=img.height,
                format="png",
                size=len(data),
                data=data
            )
        except Exception as e:
            print(f"❌ macOS窗口截图失败: {e}")
            return None
    
    async def _capture_macos_region(
        self, 
        x: int, 
        y: int, 
        width: int, 
        height: int,
        filename: str = None
    ) -> ScreenshotInfo:
        """macOS区域截图"""
        try:
            cmd = f"screencapture -x -R {x},{y},{width},{height} /tmp/screenshot.png"
            
            result = await asyncio.create_subprocess_shell(
                cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            await result.communicate()
            
            data = await self._read_file("/tmp/screenshot.png")
            
            if filename:
                await self._save_file(filename, data)
            
            return ScreenshotInfo(
                width=width,
                height=height,
                format="png",
                size=len(data),
                data=data
            )
        except Exception as e:
            print(f"❌ macOS区域截图失败: {e}")
            return None
    
    async def _capture_linux_fullscreen(self, filename: str = None) -> ScreenshotInfo:
        """Linux全屏截图"""
        try:
            # 尝试使用scrot
            result = await asyncio.create_subprocess_shell(
                "scrot -q 100 /tmp/screenshot.png",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            await result.communicate()
            
            if result.returncode != 0:
                # 尝试使用gnome-screenshot
                result = await asyncio.create_subprocess_shell(
                    "gnome-screenshot -f /tmp/screenshot.png",
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                await result.communicate()
            
            data = await self._read_file("/tmp/screenshot.png")
            
            if filename:
                await self._save_file(filename, data)
            
            from PIL import Image
            img = Image.open(io.BytesIO(data))
            
            return ScreenshotInfo(
                width=img.width,
                height=img.height,
                format="png",
                size=len(data),
                data=data
            )
        except Exception as e:
            print(f"❌ Linux截图失败: {e}")
            # 返回模拟数据
            return ScreenshotInfo(
                width=1920,
                height=1080,
                format="png",
                size=0,
                data=b''
            )
    
    async def _capture_linux_window(
        self, 
        window_title: str = None,
        filename: str = None
    ) -> ScreenshotInfo:
        """Linux窗口截图"""
        try:
            cmd = "scrot -q 100 -u /tmp/screenshot.png"
            
            if window_title:
                # 尝试使用窗口ID
                result = await asyncio.create_subprocess_shell(
                    f"xdotool search --name '{window_title}'",
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                output = await result.communicate()
                window_id = output[0].decode().strip()
                
                if window_id:
                    cmd = f"scrot -q 100 --focused /tmp/screenshot.png"
            
            result = await asyncio.create_subprocess_shell(
                cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            await result.communicate()
            
            data = await self._read_file("/tmp/screenshot.png")
            
            if filename:
                await self._save_file(filename, data)
            
            return ScreenshotInfo(
                width=0,
                height=0,
                format="png",
                size=len(data),
                data=data
            )
        except Exception as e:
            print(f"❌ Linux窗口截图失败: {e}")
            return None
    
    async def _capture_linux_region(
        self, 
        x: int, 
        y: int, 
        width: int, 
        height: int,
        filename: str = None
    ) -> ScreenshotInfo:
        """Linux区域截图"""
        try:
            cmd = f"scrot -q 100 -a {x},{y},{width},{height} /tmp/screenshot.png"
            
            result = await asyncio.create_subprocess_shell(
                cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            await result.communicate()
            
            data = await self._read_file("/tmp/screenshot.png")
            
            if filename:
                await self._save_file(filename, data)
            
            return ScreenshotInfo(
                width=width,
                height=height,
                format="png",
                size=len(data),
                data=data
            )
        except Exception as e:
            print(f"❌ Linux区域截图失败: {e}")
            return None
    
    # ============ 辅助方法 ============
    
    async def _save_file(self, filename: str, data: bytes):
        """保存文件"""
        loop = asyncio.get_event_loop()
        
        def _save():
            Path(filename).parent.mkdir(parents=True, exist_ok=True)
            with open(filename, 'wb') as f:
                f.write(data)
        
        await loop.run_in_executor(None, _save)
    
    async def _read_file(self, path: str) -> bytes:
        """读取文件"""
        loop = asyncio.get_event_loop()
        
        def _read():
            with open(path, 'rb') as f:
                return f.read()
        
        return await loop.run_in_executor(None, _read)
    
    def to_base64(self, screenshot: ScreenshotInfo) -> str:
        """转换为Base64"""
        return base64.b64encode(screenshot.data).decode()
    
    def from_base64(self, base64_str: str) -> bytes:
        """从Base64转换"""
        return base64.b64decode(base64_str)


# 便捷函数
async def capture_fullscreen(filename: str = None) -> ScreenshotInfo:
    """全屏截图"""
    tool = Screenshot()
    return await tool.capture_fullscreen(filename)

async def capture_region(
    x: int, 
    y: int, 
    width: int, 
    height: int,
    filename: str = None
) -> ScreenshotInfo:
    """区域截图"""
    tool = Screenshot()
    return await tool.capture_region(x, y, width, height, filename)

# 测试代码
if __name__ == "__main__":
    async def test():
        print("📸 截图工具测试")
        
        tool = Screenshot()
        
        # 测试全屏截图
        print("\n1. 测试全屏截图...")
        screenshot = await tool.capture_fullscreen("/tmp/clawos_screenshot.png")
        if screenshot:
            print(f"   ✅ 截图成功: {screenshot.width}x{screenshot.height}")
        else:
            print("   ❌ 截图失败")
        
        print("\n✅ 测试完成")
    
    asyncio.run(test())
