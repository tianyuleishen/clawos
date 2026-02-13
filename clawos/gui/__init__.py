# 🦞 ClawOS GUI - 图形界面模块

"""
GUI模块 - 图形界面、对话、控制面板

功能:
- Main Window (主窗口)
- Conversation Interface (对话界面)
- Control Panel (控制面板)
"""

from .main_window import (
    GUIInterface,
    GUIConfig,
    GUIFramework,
    SimpleGUI,
    MockGUI,
    TkinterGUI,
    PyQtGUI,
    create_gui,
    launch_gui,
    Message
)

from .chat_interface import (
    ConversationInterface,
    ChatPanel,
    ChatMessage,
    MessageType
)

from .control_panel import (
    ControlPanel,
    ControlItem,
    SystemStatus,
    ModuleStatus
)

__all__ = [
    # 主窗口
    'GUIInterface',
    'GUIConfig',
    'GUIFramework',
    'SimpleGUI',
    'MockGUI',
    'TkinterGUI',
    'PyQtGUI',
    'create_gui',
    'launch_gui',
    'Message',
    
    # 对话界面
    'ConversationInterface',
    'ChatPanel',
    'ChatMessage',
    'MessageType',
    
    # 控制面板
    'ControlPanel',
    'ControlItem',
    'SystemStatus',
    'ModuleStatus',
]
