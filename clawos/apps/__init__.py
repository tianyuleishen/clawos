# 🦞 ClawOS Apps - 应用控制模块

"""
应用控制模块 - 应用、浏览器、终端、截图

功能:
- App Controller (应用启动/关闭)
- Browser Automation (浏览器自动化)
- Terminal Controller (终端控制)
- Screenshot (屏幕截图)
"""

from .app_controller import AppController, AppInfo, ProcessInfo
from .browser import BrowserAutomation, Browser, TabInfo, PageInfo
from .terminal import TerminalController, CommandResult, ShellSession, ShellType
from .screenshot import Screenshot, ScreenshotInfo

__all__ = [
    # 应用控制
    'AppController',
    'AppInfo',
    'ProcessInfo',
    
    # 浏览器
    'BrowserAutomation',
    'Browser',
    'TabInfo',
    'PageInfo',
    
    # 终端
    'TerminalController',
    'CommandResult',
    'ShellSession',
    'ShellType',
    
    # 截图
    'Screenshot',
    'ScreenshotInfo',
]
