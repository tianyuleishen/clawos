# 🦞 Clipboard Manager - 剪贴板管理器

"""
剪贴板管理器 - 跨平台剪贴板操作

功能:
- 读取/写入文本
- 读取/写入图片
- 读取/写入文件
- 清空剪贴板
- 历史记录
"""

import asyncio
from typing import Optional, List, Union, Any
from dataclasses import dataclass
from enum import Enum
import platform
import base64
import io

class ClipboardType(Enum):
    """剪贴板内容类型"""
    TEXT = "text"
    IMAGE = "image"
    FILES = "files"
    HTML = "html"
    RTF = "rtf"

@dataclass
class ClipboardContent:
    """剪贴板内容"""
    type: ClipboardType
    data: Any
    format: str
    size: int
    timestamp: float

class ClipboardManager:
    """剪贴板管理器"""
    
    def __init__(self):
        self.platform = platform.system()
        self._init_platform_specific()
        self.history: List[ClipboardContent] = []
        self.max_history = 20
        
        print(f"✅ Clipboard Manager 已加载 ({self.platform})")
    
    def _init_platform_specific(self):
        """初始化平台特定的实现"""
        
        if self.platform == "Windows":
            self.impl = WindowsClipboardImpl()
        elif self.platform == "Darwin":  # macOS
            self.impl = MacOSClipboardImpl()
        elif self.platform == "Linux":
            self.impl = LinuxClipboardImpl()
        else:
            raise NotImplementedError(f"不支持的平台: {self.platform}")
    
    # ============ 文本操作 ============
    
    async def get_text(self) -> Optional[str]:
        """读取剪贴板文本
        
        Returns:
            str: 剪贴板文本内容
        """
        text = await self.impl.get_text()
        
        if text:
            # 添加到历史
            content = ClipboardContent(
                type=ClipboardType.TEXT,
                data=text,
                format="text/plain",
                size=len(text),
                timestamp=self._get_timestamp()
            )
            self._add_to_history(content)
        
        return text
    
    async def set_text(self, text: str):
        """写入剪贴板文本
        
        Args:
            text: 要写入的文本
        """
        await self.impl.set_text(text)
        
        # 添加到历史
        content = ClipboardContent(
            type=ClipboardType.TEXT,
            data=text,
            format="text/plain",
            size=len(text),
            timestamp=self._get_timestamp()
        )
        self._add_to_history(content)
    
    # ============ 图片操作 ============
    
    async def get_image(self) -> Optional[bytes]:
        """读取剪贴板图片
        
        Returns:
            bytes: PNG格式的图片数据
        """
        image_data = await self.impl.get_image()
        
        if image_data:
            content = ClipboardContent(
                type=ClipboardType.IMAGE,
                data=image_data,
                format="image/png",
                size=len(image_data),
                timestamp=self._get_timestamp()
            )
            self._add_to_history(content)
        
        return image_data
    
    async def set_image(self, image_data: bytes, format: str = "png"):
        """写入剪贴板图片
        
        Args:
            image_data: PNG格式的图片数据
            format: 图片格式
        """
        await self.impl.set_image(image_data)
        
        content = ClipboardContent(
            type=ClipboardType.IMAGE,
            data=image_data,
            format=f"image/{format}",
            size=len(image_data),
            timestamp=self._get_timestamp()
        )
        self._add_to_history(content)
    
    async def set_image_from_file(self, file_path: str):
        """从文件写入图片
        
        Args:
            file_path: 图片文件路径
        """
        with open(file_path, 'rb') as f:
            image_data = f.read()
        await self.set_image(image_data)
    
    # ============ 文件操作 ============
    
    async def get_files(self) -> List[str]:
        """读取剪贴板中的文件列表
        
        Returns:
            List[str]: 文件路径列表
        """
        files = await self.impl.get_files()
        
        if files:
            content = ClipboardContent(
                type=ClipboardType.FILES,
                data=files,
                format="file_paths",
                size=len(files),
                timestamp=self._get_timestamp()
            )
            self._add_to_history(content)
        
        return files
    
    async def set_files(self, files: List[str]):
        """写入剪贴板文件列表
        
        Args:
            files: 文件路径列表
        """
        await self.impl.set_files(files)
        
        content = ClipboardContent(
            type=ClipboardType.FILES,
            data=files,
            format="file_paths",
            size=len(files),
            timestamp=self._get_timestamp()
        )
        self._add_to_history(content)
    
    # ============ 历史记录 ============
    
    def get_history(self) -> List[ClipboardContent]:
        """获取剪贴板历史
        
        Returns:
            List[ClipboardContent]: 历史记录列表
        """
        return self.history[-self.max_history:]
    
    def clear_history(self):
        """清空历史记录"""
        self.history.clear()
    
    async def paste_from_history(self, index: int):
        """从历史粘贴
        
        Args:
            index: 历史索引 (负数表示从最新开始)
        """
        if -len(self.history) <= index < len(self.history):
            content = self.history[index]
            
            if content.type == ClipboardType.TEXT:
                await self.set_text(content.data)
            elif content.type == ClipboardType.IMAGE:
                await self.set_image(content.data)
            elif content.type == ClipboardType.FILES:
                await self.set_files(content.data)
    
    # ============ 清空 ============
    
    async def clear(self):
        """清空剪贴板"""
        await self.impl.clear()
        self.clear_history()
    
    # ============ 辅助方法 ============
    
    def _add_to_history(self, content: ClipboardContent):
        """添加到历史"""
        self.history.append(content)
        
        # 保持历史长度限制
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]
    
    def _get_timestamp(self) -> float:
        """获取时间戳"""
        import time
        return time.time()
    
    # ============ 格式转换 ============
    
    def text_to_base64(self, text: str) -> str:
        """文本转Base64"""
        return base64.b64encode(text.encode()).decode()
    
    def base64_to_text(self, base64_str: str) -> str:
        """Base64转文本"""
        return base64.b64decode(base64_str.encode()).decode()
    
    def image_to_base64(self, image_data: bytes) -> str:
        """图片转Base64"""
        return base64.b64encode(image_data).decode()
    
    def base64_to_image(self, base64_str: str) -> bytes:
        """Base64转图片"""
        return base64.b64decode(base64_str.encode())
    
    def text_to_hex(self, text: str) -> str:
        """文本转Hex"""
        return text.encode().hex()
    
    def hex_to_text(self, hex_str: str) -> str:
        """Hex转文本"""
        return bytes.fromhex(hex_str).decode()


class ClipboardImpl:
    """剪贴板实现基类"""
    
    async def get_text(self) -> Optional[str]:
        raise NotImplementedError()
    
    async def set_text(self, text: str):
        raise NotImplementedError()
    
    async def get_image(self) -> Optional[bytes]:
        raise NotImplementedError()
    
    async def set_image(self, image_data: bytes):
        raise NotImplementedError()
    
    async def get_files(self) -> List[str]:
        raise NotImplementedError()
    
    async def set_files(self, files: List[str]):
        raise NotImplementedError()
    
    async def clear(self):
        raise NotImplementedError()


class WindowsClipboardImpl(ClipboardImpl):
    """Windows平台实现"""
    
    def __init__(self):
        try:
            import win32clipboard
            self.win32clipboard = win32clipboard
        except ImportError:
            self.win32clipboard = None
    
    async def get_text(self) -> Optional[str]:
        """读取剪贴板文本"""
        try:
            if self.win32clipboard:
                self.win32clipboard.OpenClipboard()
                if self.win32clipboard.IsClipboardFormatAvailable(self.win32clipboard.CF_UNICODETEXT):
                    text = self.win32clipboard.GetClipboardData(self.win32clipboard.CF_UNICODETEXT)
                    self.win32clipboard.CloseClipboard()
                    return text
                self.win32clipboard.CloseClipboard()
            else:
                # 备用方案
                import subprocess
                result = subprocess.run(
                    ['powershell', '-Command', 'Get-Clipboard'],
                    capture_output=True, text=True
                )
                return result.stdout.strip() if result.stdout else None
        except Exception as e:
            return None
        return None
    
    async def set_text(self, text: str):
        """写入剪贴板文本"""
        try:
            if self.win32clipboard:
                self.win32clipboard.OpenClipboard()
                self.win32clipboard.EmptyClipboard()
                self.win32clipboard.SetClipboardData(
                    self.win32clipboard.CF_UNICODETEXT, text
                )
                self.win32clipboard.CloseClipboard()
            else:
                import subprocess
                subprocess.run(
                    ['powershell', '-Command', f'Set-Clipboard -Text "{text}"'],
                    capture_output=True
                )
        except Exception as e:
            pass
    
    async def get_image(self) -> Optional[bytes]:
        """读取剪贴板图片"""
        try:
            if self.win32clipboard:
                self.win32clipboard.OpenClipboard()
                if self.win32clipboard.IsClipboardFormatAvailable(
                    self.win32clipboard.CF_DIB
                ):
                    import pythoncom
                    import win32con
                    data = self.win32clipboard.GetClipboardData(win32con.CF_DIB)
                    self.win32clipboard.CloseClipboard()
                    
                    # 转换为PNG
                    from PIL import Image
                    import io
                    
                    img = Image.open(io.BytesIO(data))
                    buffer = io.BytesIO()
                    img.save(buffer, format='PNG')
                    return buffer.getvalue()
                
                self.win32clipboard.CloseClipboard()
        except Exception as e:
            pass
        return None
    
    async def set_image(self, image_data: bytes):
        """写入剪贴板图片"""
        try:
            if self.win32clipboard:
                import pythoncom
                import win32con
                import win32ui
                from PIL import Image
                import io
                
                # PNG转DIB
                img = Image.open(io.BytesIO(image_data))
                
                self.win32clipboard.OpenClipboard()
                self.win32clipboard.EmptyClipboard()
                
                output = io.BytesIO()
                img.save(output, format='DIB')
                dib_data = output.getvalue()
                
                self.win32clipboard.SetClipboardData(win32con.CF_DIB, dib_data)
                self.win32clipboard.CloseClipboard()
        except Exception as e:
            pass
    
    async def get_files(self) -> List[str]:
        """读取剪贴板文件列表"""
        return []
    
    async def set_files(self, files: List[str]):
        """写入剪贴板文件列表"""
        pass
    
    async def clear(self):
        """清空剪贴板"""
        try:
            if self.win32clipboard:
                self.win32clipboard.OpenClipboard()
                self.win32clipboard.EmptyClipboard()
                self.win32clipboard.CloseClipboard()
        except Exception as e:
            pass


class MacOSClipboardImpl(ClipboardImpl):
    """macOS平台实现"""
    
    async def get_text(self) -> Optional[str]:
        """读取剪贴板文本"""
        try:
            import subprocess
            result = subprocess.run(
                ['pbpaste'],
                capture_output=True, text=True
            )
            return result.stdout if result.stdout else None
        except Exception as e:
            return None
    
    async def set_text(self, text: str):
        """写入剪贴板文本"""
        try:
            import subprocess
            process = subprocess.Popen(
                ['pbcopy'], 
                stdin=subprocess.PIPE
            )
            process.communicate(input=text.encode())
        except Exception as e:
            pass
    
    async def get_image(self) -> Optional[bytes]:
        """读取剪贴板图片"""
        try:
            import subprocess
            # 使用osascript获取剪贴板图片
            result = subprocess.run([
                'osascript', '-e',
                'set the clipboard to (read POSIX file "/dev/stdin" as «class PNGf»)'
            ], capture_output=True)
            
            if result.stdout:
                return result.stdout
        except Exception as e:
            pass
        return None
    
    async def set_image(self, image_data: bytes):
        """写入剪贴板图片"""
        try:
            import subprocess
            process = subprocess.Popen(
                ['osascript', '-e', 
                 'set the clipboard to (read POSIX file "/dev/stdin" as «class PNGf»)'],
                stdin=subprocess.PIPE
            )
            process.communicate(input=image_data)
        except Exception as e:
            pass
    
    async def get_files(self) -> List[str]:
        """读取剪贴板文件列表"""
        return []
    
    async def set_files(self, files: List[str]):
        """写入剪贴板文件列表"""
        pass
    
    async def clear(self):
        """清空剪贴板"""
        try:
            import subprocess
            subprocess.run(['pbcopy'], input=b'', capture_output=True)
        except Exception as e:
            pass


class LinuxClipboardImpl(ClipboardImpl):
    """Linux平台实现"""
    
    def __init__(self):
        try:
            import pyperclip
            self.pyperclip = pyperclip
        except ImportError:
            self.pyperclip = None
    
    async def get_text(self) -> Optional[str]:
        """读取剪贴板文本"""
        try:
            if self.pyperclip:
                return self.pyperclip.paste()
            else:
                # 备用方案
                import subprocess
                result = subprocess.run(
                    ['xclip', '-selection', 'clipboard', '-o'],
                    capture_output=True, text=True
                )
                return result.stdout if result.stdout else None
        except Exception as e:
            return None
        return None
    
    async def set_text(self, text: str):
        """写入剪贴板文本"""
        try:
            if self.pyperclip:
                self.pyperclip.copy(text)
            else:
                import subprocess
                process = subprocess.Popen(
                    ['xclip', '-selection', 'clipboard', '-i'],
                    stdin=subprocess.PIPE
                )
                process.communicate(input=text.encode())
        except Exception as e:
            pass
    
    async def get_image(self) -> Optional[bytes]:
        """读取剪贴板图片"""
        try:
            import subprocess
            result = subprocess.run(
                ['xclip', '-selection', 'clipboard', '-t', 'image/png', '-o'],
                capture_output=True
            )
            return result.stdout if result.stdout else None
        except Exception as e:
            pass
        return None
    
    async def set_image(self, image_data: bytes):
        """写入剪贴板图片"""
        try:
            import subprocess
            process = subprocess.Popen(
                ['xclip', '-selection', 'clipboard', '-t', 'image/png', '-i'],
                stdin=subprocess.PIPE
            )
            process.communicate(input=image_data)
        except Exception as e:
            pass
    
    async def get_files(self) -> List[str]:
        """读取剪贴板文件列表"""
        return []
    
    async def set_files(self, files: List[str]):
        """写入剪贴板文件列表"""
        pass
    
    async def clear(self):
        """清空剪贴板"""
        await self.set_text("")


# 便捷函数
async def get_clipboard_text() -> Optional[str]:
    """读取剪贴板文本"""
    manager = ClipboardManager()
    return await manager.get_text()

async def set_clipboard_text(text: str):
    """写入剪贴板文本"""
    manager = ClipboardManager()
    await manager.set_text(text)

# 测试代码
if __name__ == "__main__":
    async def test():
        print("📋 剪贴板管理器测试")
        
        manager = ClipboardManager()
        
        # 测试写入文本
        print("写入文本...")
        await manager.set_text("Hello ClawOS!")
        
        # 测试读取文本
        print("读取文本...")
        text = await manager.get_text()
        print(f"读取到: {text}")
        
        # 测试历史
        print("\n历史记录:")
        history = manager.get_history()
        for i, content in enumerate(history[-3:]):
            print(f"  {i}: {content.type.value} ({content.size} bytes)")
        
        print("✅ 测试完成")
    
    asyncio.run(test())
