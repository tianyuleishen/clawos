# 🦞 ClawOS Storage - 数据持久化模块

"""
数据持久化模块 - 存储、对话、设置、记忆

功能:
- Storage Base (存储基类)
- Conversation Storage (对话历史)
- Settings Storage (用户设置)
- Memory Storage (记忆存储)
"""

from .base import (
    StorageBase,
    StorageConfig,
    Record,
    JSONStorage,
    SQLiteStorage,
    create_storage
)

from .conversation import (
    ConversationStorage,
    ConversationMessage,
    ConversationSession,
    MessageRole,
    create_conversation_storage
)

from .settings import (
    SettingsStorage,
    UserSettings,
    ModuleConfig,
    Theme,
    Language,
    create_settings_storage
)

from .memory import (
    MemoryStorage,
    Memory,
    Fact,
    Experience,
    MemoryType,
    Importance,
    create_memory_storage
)

__all__ = [
    # 存储基类
    'StorageBase',
    'StorageConfig',
    'Record',
    'JSONStorage',
    'SQLiteStorage',
    'create_storage',
    
    # 对话存储
    'ConversationStorage',
    'ConversationMessage',
    'ConversationSession',
    'MessageRole',
    'create_conversation_storage',
    
    # 设置存储
    'SettingsStorage',
    'UserSettings',
    'ModuleConfig',
    'Theme',
    'Language',
    'create_settings_storage',
    
    # 记忆存储
    'MemoryStorage',
    'Memory',
    'Fact',
    'Experience',
    'MemoryType',
    'Importance',
    'create_memory_storage',
]
