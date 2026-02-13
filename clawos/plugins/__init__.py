# 🦞 ClawOS Plugins - 插件系统

"""
插件系统 - 插件、API、商店

功能:
- Plugin Base (插件基类)
- Plugin Manager (插件管理器)
- Plugin API (插件接口)
- Plugin Store (插件商店)
"""

from .base import (
    PluginBase,
    PluginMetadata,
    PluginState,
    PluginHook,
    HookType,
    PluginBase,
    create_plugin,
    load_plugin_from_file
)

from .manager import (
    PluginManager,
    PluginInfo,
    create_plugin_manager
)

from .api import (
    PluginAPI,
    AIService,
    StorageService,
    MemoryService,
    ConversationService,
    SettingsService,
    EventService,
    GUIService,
    ControlsService,
    AppsService,
    FilesService,
    TerminalService,
    create_plugin_api
)

from .store import (
    PluginStore,
    PluginItem,
    PluginReview,
    PluginCategory,
    create_plugin_store
)

__all__ = [
    # 插件基类
    'PluginBase',
    'PluginMetadata',
    'PluginState',
    'PluginHook',
    'HookType',
    'create_plugin',
    'load_plugin_from_file',
    
    # 插件管理器
    'PluginManager',
    'PluginInfo',
    'create_plugin_manager',
    
    # 插件API
    'PluginAPI',
    'AIService',
    'StorageService',
    'MemoryService',
    'ConversationService',
    'SettingsService',
    'EventService',
    'GUIService',
    'ControlsService',
    'AppsService',
    'FilesService',
    'TerminalService',
    'create_plugin_api',
    
    # 插件商店
    'PluginStore',
    'PluginItem',
    'PluginReview',
    'PluginCategory',
    'create_plugin_store',
]
