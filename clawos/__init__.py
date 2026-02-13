# 🦞 ClawOS - AI操作系统

"""
ClawOS AI操作系统

功能:
- 世界级推理引擎
- L11意识系统
- 情感交互
- 电脑控制
- 文件管理
- 应用控制
- 智能功能
- GUI界面
- 数据持久化
- 插件系统
- API接口
- 首次引导配置
"""

__version__ = "1.0.0"
__author__ = "ClawOS Team"

# 核心模块
from .core.reasoning import UltimateFusionEngine
from .core.consciousness import L11Consciousness
from .core.emotion import EmotionModule

# 控制模块
from .controls.mouse import MouseController
from .controls.keyboard import KeyboardController
from .controls.window import WindowManager
from .controls.clipboard import ClipboardManager

# 文件模块
from .files.file import FileManager
from .files.directory import DirectoryManager
from .files.search import FileSearcher
from .files.batch import BatchOperations

# 应用模块
from .apps.app_controller import AppController
from .apps.browser import BrowserAutomation
from .apps.terminal import TerminalController

# AI模块
from .ai.speech_recognition import SpeechRecognizer
from .ai.text_to_speech import TextToSpeech
from .ai.nlu import NaturalLanguageUnderstanding
from .ai.task_planner import TaskPlanner

# GUI模块
from .gui.main_window import GUIFramework
from .gui.chat_interface import ConversationInterface
from .gui.control_panel import ControlPanel

# 存储模块
from .storage.base import JSONStorage, SQLiteStorage
from .storage.conversation import ConversationStorage
from .storage.settings import SettingsStorage
from .storage.memory import MemoryStorage

# 插件模块
from .plugins.base import PluginBase
from .plugins.manager import PluginManager
from .plugins.api import PluginAPI
from .plugins.store import PluginStore

# API模块
from .api import RESTAPI, WebSocketAPI, CloudService

# 引导模块
from .onboarding import OnboardingManager, get_onboarding_manager, AVAILABLE_MODELS

__all__ = [
    # 版本
    '__version__',
    '__author__',
    
    # 核心
    'UltimateFusionEngine',
    'L11Consciousness',
    'EmotionModule',
    
    # 控制
    'MouseController',
    'KeyboardController',
    'WindowManager',
    'ClipboardManager',
    
    # 文件
    'FileManager',
    'DirectoryManager',
    'FileSearcher',
    'BatchOperations',
    
    # 应用
    'AppController',
    'BrowserAutomation',
    'TerminalController',
    
    # AI
    'SpeechRecognizer',
    'TextToSpeech',
    'NaturalLanguageUnderstanding',
    'TaskPlanner',
    
    # GUI
    'GUIFramework',
    'ConversationInterface',
    'ControlPanel',
    
    # 存储
    'JSONStorage',
    'SQLiteStorage',
    'ConversationStorage',
    'SettingsStorage',
    'MemoryStorage',
    
    # 插件
    'PluginBase',
    'PluginManager',
    'PluginAPI',
    'PluginStore',
    
    # API
    'RESTAPI',
    'WebSocketAPI',
    'CloudService',
    
    # 引导
    'OnboardingManager',
    'get_onboarding_manager',
    'AVAILABLE_MODELS',
]
