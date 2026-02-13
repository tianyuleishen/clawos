# 🦞 Browser Automation - 浏览器自动化

"""
浏览器自动化 - 跨平台浏览器控制

功能:
- 打开网页
- 页面导航
- 元素操作
- 表单填写
- 截图
"""

import asyncio
import subprocess
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from enum import Enum
from urllib.parse import urlparse
import platform

class Browser(Enum):
    """支持的浏览器"""
    CHROME = "chrome"
    FIREFOX = "firefox"
    EDGE = "edge"
    SAFARI = "safari"
    BRAVE = "brave"
    DEFAULT = "default"

@dataclass
class TabInfo:
    """标签页信息"""
    tab_id: str
    title: str
    url: str
    is_active: bool

@dataclass
class PageInfo:
    """页面信息"""
    title: str
    url: str
    source: str
    loaded: bool

class BrowserAutomation:
    """浏览器自动化控制器"""
    
    def __init__(self):
        self.platform = platform.system()
        self.current_browser = None
        self.tabs: List[TabInfo] = []
        print(f"✅ Browser Automation 已加载 ({self.platform})")
    
    # ============ 浏览器启动 ============
    
    async def launch_browser(
        self, 
        browser: Browser = Browser.DEFAULT,
        headless: bool = False,
        profile: str = None,
        incognito: bool = False
    ) -> bool:
        """启动浏览器
        
        Args:
            browser: 浏览器类型
            headless: 无头模式
            profile: 用户配置文件
            incognito: 隐身模式
        
        Returns:
            bool: 是否成功
        """
        cmd = self._build_launch_command(
            browser, headless, profile, incognito
        )
        
        if not cmd:
            print(f"⚠️ 未找到浏览器: {browser.value}")
            return False
        
        try:
            # 启动浏览器进程
            if self.platform == "Windows":
                await asyncio.create_subprocess_shell(
                    cmd,
                    creationflags=subprocess.CREATE_NEW_CONSOLE
                )
            else:
                await asyncio.create_subprocess_shell(cmd)
            
            self.current_browser = browser
            print(f"✅ 浏览器已启动: {browser.value}")
            return True
            
        except Exception as e:
            print(f"❌ 启动浏览器失败: {e}")
            return False
    
    async def open_url(
        self, 
        url: str,
        browser: Browser = Browser.DEFAULT,
        new_tab: bool = True
    ):
        """打开URL
        
        Args:
            url: URL地址
            browser: 浏览器类型
            new_tab: 是否在新标签页打开
        """
        # 确保URL有协议
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        # 构建命令
        if self.platform == "Windows":
            cmd = f'start "" "{url}"'
        elif self.platform == "Darwin":
            cmd = f'open "{url}"'
        else:  # Linux
            cmd = f'xdg-open "{url}"'
        
        try:
            await asyncio.create_subprocess_shell(cmd)
            print(f"🌐 已打开: {url}")
        except Exception as e:
            print(f"❌ 打开URL失败: {e}")
    
    async def search(
        self, 
        query: str,
        engine: str = "google",
        browser: Browser = Browser.DEFAULT
    ):
        """搜索引擎搜索
        
        Args:
            query: 搜索词
            engine: 搜索引擎 (google, bing, baidu)
            browser: 浏览器类型
        """
        engines = {
            "google": f"https://www.google.com/search?q={query}",
            "bing": f"https://www.bing.com/search?q={query}",
            "baidu": f"https://www.baidu.com/s?wd={query}",
            "duckduckgo": f"https://duckduckgo.com/?q={query}"
        }
        
        url = engines.get(engine, engines["google"])
        await self.open_url(url, browser)
    
    # ============ 浏览器控制 ============
    
    async def close_browser(self):
        """关闭浏览器"""
        if self.current_browser:
            try:
                if self.platform == "Windows":
                    await self.execute_shell(f"taskkill /F /IM {self.current_browser.value}.exe")
                else:
                    await self.execute_shell(f"pkill -f {self.current_browser.value}")
                print(f"✅ 浏览器已关闭")
            except Exception as e:
                print(f"❌ 关闭浏览器失败: {e}")
    
    async def go_back(self):
        """后退"""
        await self._send_key_sequence(["alt", "left"])
    
    async def go_forward(self):
        """前进"""
        await self._send_key_sequence(["alt", "right"])
    
    async def refresh(self):
        """刷新"""
        await self._send_key_sequence(["f5"])
    
    async def stop_loading(self):
        """停止加载"""
        await self._send_key_sequence(["esc"])
    
    async def scroll_top(self):
        """滚动到顶部"""
        await self._send_key_sequence(["home"])
    
    async def scroll_bottom(self):
        """滚动到底部"""
        await self._send_key_sequence(["end"])
    
    async def scroll_page_up(self):
        """向上滚动一页"""
        await self._send_key_sequence(["pageup"])
    
    async def scroll_page_down(self):
        """向下滚动一页"""
        await self._send_key_sequence(["pagedown"])
    
    # ============ 标签页控制 ============
    
    async def new_tab(self, url: str = None):
        """新建标签页
        
        Args:
            url: URL地址 (可选)
        """
        # Ctrl+T 新建标签页
        await self._send_key_sequence(["ctrl", "t"])
        
        if url:
            # 输入URL
            await asyncio.sleep(0.3)
            await self._send_key_sequence(["ctrl", "l"])
            await asyncio.sleep(0.1)
            
            # 清除现有内容
            for _ in range(50):
                await self._send_key_sequence(["backspace"])
            
            # 输入URL
            await self._type_text(url)
            await self._send_key_sequence(["enter"])
    
    async def close_tab(self):
        """关闭当前标签页"""
        await self._send_key_sequence(["ctrl", "w"])
    
    async def switch_to_next_tab(self):
        """切换到下一个标签页"""
        await self._send_key_sequence(["ctrl", "tab"])
    
    async def switch_to_previous_tab(self):
        """切换到上一个标签页"""
        await self._send_key_sequence(["ctrl", "shift", "tab"])
    
    async def switch_to_tab(self, index: int):
        """切换到指定标签页
        
        Args:
            index: 标签页索引 (从1开始)
        """
        for _ in range(index - 1):
            await self.switch_to_next_tab()
    
    async def duplicate_tab(self):
        """复制当前标签页"""
        await self._send_key_sequence(["ctrl", "k", "d"])
    
    # ============ 页面操作 ============
    
    async def get_page_info(self) -> PageInfo:
        """获取页面信息"""
        # 模拟实现
        return PageInfo(
            title="未知页面",
            url="",
            source="",
            loaded=True
        )
    
    async def get_page_source(self) -> str:
        """获取页面源代码"""
        # 使用快捷键全选复制
        await self._send_key_sequence(["ctrl", "a"])
        await asyncio.sleep(0.1)
        await self._send_key_sequence(["ctrl", "c"])
        
        # 从剪贴板获取
        try:
            import subprocess
            if self.platform == "Darwin":
                result = subprocess.run(['pbpaste'], capture_output=True, text=True)
                return result.stdout
            else:
                result = subprocess.run(['xclip', '-selection', 'clipboard', '-o'], 
                                      capture_output=True, text=True)
                return result.stdout
        except:
            pass
        
        return ""
    
    async def save_page(self, file_path: str):
        """保存当前页面
        
        Args:
            file_path: 保存路径
        """
        await self._send_key_sequence(["ctrl", "s"])
        await asyncio.sleep(0.5)
        
        # 输入文件名
        await self._type_text(file_path)
        await self._send_key_sequence(["enter"])
    
    # ============ 查找 ============
    
    async def find_text(self, text: str, forward: bool = True):
        """查找文本
        
        Args:
            text: 查找内容
            forward: 向前查找
        """
        await self._send_key_sequence(["ctrl", "f"])
        await asyncio.sleep(0.2)
        
        await self._type_text(text)
    
    async def find_next(self):
        """查找下一个"""
        await self._send_key_sequence(["enter"])
    
    async def find_previous(self):
        """查找上一个"""
        await self._send_key_sequence(["shift", "enter"])
    
    async def close_find_bar(self):
        """关闭查找栏"""
        await self._send_key_sequence(["esc"])
    
    # ============ 书签/历史 ============
    
    async def show_bookmarks(self):
        """显示书签"""
        await self._send_key_sequence(["ctrl", "shift", "o"])
    
    async def show_downloads(self):
        """显示下载"""
        await self._send_key_sequence(["ctrl", "j"])
    
    async def show_history(self):
        """显示历史"""
        await self._send_key_sequence(["ctrl", "h"])
    
    async def show_settings(self):
        """显示设置"""
        await self._send_key_sequence(["alt", "e"])
    
    # ============ 开发者工具 ============
    
    async def open_dev_tools(self):
        """打开开发者工具"""
        await self._send_key_sequence(["f12"])
    
    async def toggle_inspector(self):
        """切换检查器"""
        await self._send_key_sequence(["ctrl", "shift", "c"])
    
    async def toggle_console(self):
        """切换控制台"""
        await self._send_key_sequence(["ctrl", "shift", "j"])
    
    async def view_source(self):
        """查看源代码"""
        await self._send_key_sequence(["ctrl", "u"])
    
    # ============ 辅助方法 ============
    
    def _build_launch_command(
        self, 
        browser: Browser,
        headless: bool,
        profile: str,
        incognito: bool
    ) -> Optional[str]:
        """构建浏览器启动命令"""
        cmd = []
        
        if browser == Browser.CHROME:
            cmd.append(self._find_executable("chrome") or "google-chrome")
            if headless:
                cmd.append("--headless")
            if incognito:
                cmd.append("--incognito")
            if profile:
                cmd.append(f"--profile-directory={profile}")
        
        elif browser == Browser.FIREFOX:
            cmd.append(self._find_executable("firefox") or "firefox")
            if incognito:
                cmd.append("-private-window")
        
        elif browser == Browser.EDGE:
            cmd.append(self._find_executable("edge") or "msedge")
            if headless:
                cmd.append("--headless")
            if incognito:
                cmd.append("-inprivate")
        
        elif browser == Browser.SAFARI:
            if self.platform != "Darwin":
                return None
            return 'open -a Safari'
        
        elif browser == Browser.DEFAULT:
            if self.platform == "Windows":
                return "start"
            elif self.platform == "Darwin":
                return "open"
            else:
                return "xdg-open"
        
        return " ".join(cmd) if cmd else None
    
    def _find_executable(self, name: str) -> Optional[str]:
        """查找可执行文件"""
        import shutil
        path = shutil.which(name)
        if path:
            return path
        
        # Windows常见位置
        if self.platform == "Windows":
            paths = [
                f"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
                f"C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
                f"C:\\Program Files\\Mozilla Firefox\\firefox.exe",
                f"C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
            ]
            for p in paths:
                if os.path.exists(p):
                    return p
        
        return None
    
    async def _send_key_sequence(self, keys: List[str]):
        """发送按键序列"""
        from clawos.controls.keyboard import KeyboardController
        from clawos.controls.mouse import MouseController
        
        keyboard = KeyboardController()
        
        # 按下所有键
        for key in keys:
            await keyboard.key_down(key)
        
        # 释放所有键 (反向)
        for key in reversed(keys):
            await keyboard.key_up(key)
    
    async def _type_text(self, text: str):
        """输入文本"""
        from clawos.controls.keyboard import KeyboardController
        keyboard = KeyboardController()
        await keyboard.type_text(text, interval=0.01)
    
    async def execute_shell(self, cmd: str):
        """执行shell命令"""
        process = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        await process.communicate()


# 便捷函数
async def open_url(url: str):
    """打开URL"""
    automation = BrowserAutomation()
    await automation.open_url(url)

async def search_web(query: str, engine: str = "google"):
    """网络搜索"""
    automation = BrowserAutomation()
    await automation.search(query, engine)

# 测试代码
if __name__ == "__main__":
    async def test():
        print("🌐 浏览器自动化测试")
        
        automation = BrowserAutomation()
        
        # 测试打开URL
        print("\n1. 测试打开URL...")
        await automation.open_url("https://www.google.com")
        print("   已打开 Google")
        
        # 测试搜索
        print("\n2. 测试搜索...")
        await automation.search("ClawOS AI", "google")
        print("   已搜索: ClawOS AI")
        
        print("\n✅ 测试完成")
    
    asyncio.run(test())

import os
