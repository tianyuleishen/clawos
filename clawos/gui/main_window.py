# 🦞 ClawOS GUI - 图形界面模块

"""
GUI模块 - ClawOS图形界面

功能:
- 主窗口
- 对话界面
- 控制面板
- 状态显示
"""

import asyncio
from typing import Callable, Optional, Dict, Any
from dataclasses import dataclass
from enum import Enum
import threading

class GUIFramework(Enum):
    """GUI框架"""
    TKINTER = "tkinter"      # 内置,简单
    PYQT = "pyqt"            # 功能强大
    PYSIDE = "pyside"       # Qt官方Python
    CUSTOM = "custom"       # 自定义

@dataclass
class Message:
    """消息"""
    id: str
    role: str  # "user" or "assistant"
    content: str
    timestamp: float
    emotions: Dict[str, float] = None

@dataclass
class GUIConfig:
    """GUI配置"""
    title: str = "ClawOS AI"
    width: int = 800
    height: int = 600
    theme: str = "dark"
    font_size: int = 12
    language: str = "zh"
    show_emotions: bool = True
    show_thinking: bool = True


class GUIInterface:
    """GUI接口基类"""
    
    def __init__(self, config: GUIConfig = None):
        self.config = config or GUIConfig()
        self.is_running = False
        print(f"✅ GUI Interface 已加载")
    
    def run(self):
        """运行GUI"""
        raise NotImplementedError()
    
    def stop(self):
        """停止GUI"""
        self.is_running = False
    
    def send_message(self, message: str):
        """发送消息"""
        raise NotImplementedError()
    
    def on_message(self, callback: Callable[[Message], None]):
        """消息回调"""
        raise NotImplementedError()


class SimpleGUI:
    """简单GUI实现 (命令行增强版)"""
    
    def __init__(self, config: GUIConfig = None):
        self.config = config or GUIConfig()
        self.message_callback = None
        self.conversation_history: list = []
        self.system_status = {
            "consciousness": "active",
            "emotion": "neutral",
            "tasks": 0,
            "memory_usage": "normal"
        }
        
        print(f"✅ Simple GUI 已初始化")
        print(f"   标题: {self.config.title}")
        print(f"   主题: {self.config.theme}")
    
    def run(self):
        """运行命令行界面"""
        self.is_running = True
        
        print("\n" + "="*60)
        print(f"🦞 {self.config.title} - 命令行模式")
        print("="*60)
        print("输入 'quit' 退出, 'help' 查看帮助")
        print("-"*60)
        
        while self.is_running:
            try:
                message = input("\n👤 你: ").strip()
                
                if not message:
                    continue
                
                if message.lower() == 'quit':
                    print("👋 再见!")
                    break
                
                if message.lower() == 'help':
                    self._show_help()
                    continue
                
                if message.lower() == 'status':
                    self._show_status()
                    continue
                
                if message.lower() == 'clear':
                    self.conversation_history.clear()
                    print("🗑️ 对话已清空")
                    continue
                
                # 发送消息
                if self.message_callback:
                    msg = Message(
                        id=str(len(self.conversation_history)),
                        role="user",
                        content=message,
                        timestamp=0
                    )
                    self.message_callback(msg)
                
            except KeyboardInterrupt:
                print("\n👋 再见!")
                break
            except EOFError:
                break
    
    def stop(self):
        """停止"""
        self.is_running = False
    
    def send_message(self, message: str, role: str = "assistant"):
        """发送消息到界面"""
        print(f"\n🦞 {'助手' if role == 'assistant' else '用户'}: {message}")
        
        self.conversation_history.append({
            "role": role,
            "content": message,
            "timestamp": 0
        })
    
    def on_message(self, callback: Callable[[Message], None]):
        """设置消息回调"""
        self.message_callback = callback
    
    def update_status(self, status: Dict[str, Any]):
        """更新状态"""
        self.system_status.update(status)
    
    def _show_help(self):
        """显示帮助"""
        print("""
📖 帮助命令:
   help     - 显示此帮助
   status   - 显示系统状态
   clear    - 清空对话历史
   quit     - 退出程序

💡 使用提示:
   - 直接输入文字与AI对话
   - 可以要求执行系统操作
   - 支持语音输入(需配置)
        """)
    
    def _show_status(self):
        """显示状态"""
        print("\n📊 系统状态:")
        for key, value in self.system_status.items():
            print(f"   {key}: {value}")
        print(f"   对话数: {len(self.conversation_history)}")


class MockGUI:
    """Mock GUI - 无界面环境使用"""
    
    def __init__(self, config: GUIConfig = None):
        self.config = config or GUIConfig()
        self.message_callback = None
        print(f"✅ Mock GUI 已加载 (无界面模式)")
    
    def run(self):
        """Mock运行"""
        print(f"\n🦞 {self.config.title} - Mock模式")
        print("⚠️ 无GUI环境,使用命令行交互")
    
    def send_message(self, message: str, role: str = "assistant"):
        """发送消息"""
        print(f"\n[{role.upper()}] {message}")
    
    def on_message(self, callback: Callable[[Message], None]):
        """设置回调"""
        self.message_callback = callback


def create_gui(framework: GUIFramework = GUIFramework.TKINTER) -> GUIInterface:
    """创建GUI
    
    Args:
        framework: GUI框架
    
    Returns:
        GUIInterface: GUI实例
    """
    config = GUIConfig()
    
    # 尝试导入
    if framework == GUIFramework.TKINTER:
        try:
            import tkinter as tk
            from tkinter import scrolledtext
            
            return TkinterGUI(config)
        except ImportError:
            print("⚠️ tkinter不可用,使用简单GUI")
            return SimpleGUI(config)
    
    elif framework == GUIFramework.PYQT:
        try:
            from PyQt6.QtWidgets import QApplication
            return PyQtGUI(config)
        except ImportError:
            print("⚠️ PyQt6不可用,使用简单GUI")
            return SimpleGUI(config)
    
    else:
        return SimpleGUI(config)


class TkinterGUI:
    """Tkinter GUI实现"""
    
    def __init__(self, config: GUIConfig):
        import tkinter as tk
        from tkinter import scrolledtext, messagebox
        
        self.tk = tk
        self.root = None
        self.config = config
        self.message_callback = None
        self.conversation_history = []
        
        print(f"✅ Tkinter GUI 已加载")
    
    def run(self):
        import tkinter as tk
        from tkinter import scrolledtext, messagebox
        
        self.root = tk.Tk()
        self.root.title(self.config.title)
        self.root.geometry(f"{self.config.width}x{self.config.height}")
        
        # 主题色
        bg_color = "#1e1e1e" if self.config.theme == "dark" else "#ffffff"
        fg_color = "#ffffff" if self.config.theme == "dark" else "#000000"
        input_bg = "#2d2d2d" if self.config.theme == "dark" else "#f0f0f0"
        
        self.root.configure(bg=bg_color)
        
        # 对话区域
        self.chat_area = scrolledtext.ScrolledText(
            self.root,
            wrap=tk.WORD,
            bg=bg_color,
            fg=fg_color,
            font=("Microsoft YaHei", self.config.font_size)
        )
        self.chat_area.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        # 输入区域
        input_frame = tk.Frame(self.root, bg=bg_color)
        input_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.input_field = tk.Entry(
            input_frame,
            bg=input_bg,
            fg=fg_color,
            font=("Microsoft YaHei", self.config.font_size)
        )
        self.input_field.pack(side=tk.LEFT, expand=True, fill=tk.X)
        self.input_field.bind("<Return>", self._send_message)
        
        send_btn = tk.Button(
            input_frame,
            text="发送",
            command=self._send_message,
            bg="#4CAF50",
            fg="white"
        )
        send_btn.pack(side=tk.RIGHT, padx=(5, 0))
        
        # 状态栏
        self.status_var = tk.StringVar(value="就绪")
        status_bar = tk.Label(
            self.root,
            textvariable=self.status_var,
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.root.mainloop()
    
    def _send_message(self, event=None):
        """发送消息"""
        message = self.input_field.get().strip()
        if not message:
            return
        
        self.input_field.delete(0, tk.END)
        
        # 显示用户消息
        self._append_message("你", message, "#4CAF50")
        
        # 回调
        if self.message_callback:
            msg = Message(
                id=str(len(self.conversation_history)),
                role="user",
                content=message,
                timestamp=0
            )
            self.message_callback(msg)
    
    def _append_message(self, role: str, content: str, color: str):
        """追加消息"""
        self.chat_area.insert(tk.END, f"\n{role}: {content}\n", color)
        self.chat_area.see(tk.END)
    
    def send_message(self, message: str, role: str = "assistant"):
        """发送消息"""
        if role == "assistant":
            self._append_message("🦞 ClawOS", message, "#2196F3")
        else:
            self._append_message("你", message, "#4CAF50")
    
    def on_message(self, callback: Callable[[Message], None]):
        """设置回调"""
        self.message_callback = callback
    
    def update_status(self, status: Dict[str, Any]):
        """更新状态"""
        self.status_var.set(" | ".join([f"{k}: {v}" for k, v in status.items()]))
    
    def stop(self):
        """停止"""
        if self.root:
            self.root.quit()


class PyQtGUI:
    """PyQt6 GUI实现"""
    
    def __init__(self, config: GUIConfig):
        self.config = config
        self.app = None
        self.message_callback = None
        
        print(f"✅ PyQt GUI 已加载")
    
    def run(self):
        try:
            from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, 
                                         QVBoxLayout, QHBoxLayout, QTextEdit, 
                                         QLineEdit, QPushButton, QLabel, QStatusBar)
            from PyQt6.QtCore import Qt
            from PyQt6.QtGui import QFont, QColor
            
            self.app = QApplication([])
            
            # 主窗口
            window = QMainWindow()
            window.setWindowTitle(self.config.title)
            window.setGeometry(100, 100, self.config.width, self.config.height)
            
            # 中央部件
            central = QWidget()
            layout = QVBoxLayout()
            
            # 对话区域
            self.chat_area = QTextEdit()
            self.chat_area.setReadOnly(True)
            self.chat_area.setFont(QFont("Microsoft YaHei", 12))
            layout.addWidget(self.chat_area)
            
            # 输入区域
            input_layout = QHBoxLayout()
            self.input_field = QLineEdit()
            self.input_field.setFont(QFont("Microsoft YaHei", 12))
            self.input_field.returnPressed.connect(self._send_message)
            input_layout.addWidget(self.input_field)
            
            send_btn = QPushButton("发送")
            send_btn.clicked.connect(self._send_message)
            input_layout.addWidget(send_btn)
            
            layout.addLayout(input_layout)
            
            # 状态栏
            self.status_bar = QStatusBar()
            self.status_bar.showMessage("就绪")
            window.setStatusBar(self.status_bar)
            
            central.setLayout(layout)
            window.setCentralWidget(central)
            
            window.show()
            self.app.exec()
            
        except ImportError as e:
            print(f"⚠️ PyQt6不可用: {e}")
            print("使用SimpleGUI替代")
            gui = SimpleGUI(self.config)
            gui.run()
    
    def _send_message(self):
        """发送消息"""
        message = self.input_field.text().strip()
        if not message:
            return
        
        self.input_field.clear()
        
        self.chat_area.append(f"<b>你:</b> {message}<br>")
        
        if self.message_callback:
            self.message_callback(message)
    
    def send_message(self, message: str, role: str = "assistant"):
        """发送消息"""
        if role == "assistant":
            self.chat_area.append(f"<b>🦞 ClawOS:</b> {message}<br>")
        else:
            self.chat_area.append(f"<b>你:</b> {message}<br>")
    
    def on_message(self, callback: Callable[[str], None]):
        """设置回调"""
        self.message_callback = callback
    
    def update_status(self, status: Dict[str, Any]):
        """更新状态"""
        self.status_bar.showMessage(" | ".join([f"{k}: {v}" for k, v in status.items()]))
    
    def stop(self):
        """停止"""
        if self.app:
            self.app.quit()


# 便捷函数
def launch_gui(title: str = "ClawOS AI") -> GUIInterface:
    """启动GUI"""
    config = GUIConfig(title=title)
    
    # 尝试Tkinter,失败则SimpleGUI
    try:
        return TkinterGUI(config)
    except:
        return SimpleGUI(config)


# 测试代码
if __name__ == "__main__":
    import sys
    
    print("="*60)
    print("🦞 ClawOS GUI 测试")
    print("="*60)
    
    # 创建GUI
    gui = SimpleGUI(GUIConfig(title="ClawOS AI - 测试"))
    
    # 设置回调
    def on_user_message(msg):
        print(f"\n📨 收到消息: {msg.content}")
        
        # 模拟回复
        gui.send_message(f"收到: {msg.content}", role="assistant")
    
    gui.on_message(on_user_message)
    
    # 运行
    gui.run()
