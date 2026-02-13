# 🦞 Settings Storage - 设置存储

"""
用户设置存储 - ClawOS配置持久化

功能:
- 用户偏好设置
- 模块配置
- 快捷键设置
- 主题和UI配置
"""

import asyncio
import json
import os
from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, field, asdict
from enum import Enum
import uuid

from .base import JSONStorage, StorageConfig

class Theme(Enum):
    """主题"""
    DARK = "dark"
    LIGHT = "light"
    AUTO = "auto"

class Language(Enum):
    """语言"""
    ZH = "zh"
    EN = "en"
    AUTO = "auto"


@dataclass
class UserSettings:
    """用户设置"""
    # 基础设置
    language: str = "zh"
    theme: str = "dark"
    font_size: int = 14
    
    # 界面设置
    show_emotions: bool = True
    show_thinking: bool = True
    show_timestamps: bool = True
    compact_mode: bool = False
    
    # 功能设置
    auto_save: bool = True
    auto_save_interval: int = 60  # 秒
    max_history: int = 1000
    max_conversations: int = 100
    
    # 语音设置
    speech_enabled: bool = False
    tts_enabled: bool = False
    voice_id: str = "zh-CN-XiaoxiaoNeural"
    speech_rate: float = 1.0
    speech_pitch: int = 0
    
    # 快捷键
    hotkeys: Dict = field(default_factory=lambda: {
        "send": ["Enter"],
        "new_line": ["Shift+Enter"],
        "clear": ["Ctrl+L"],
        "search": ["Ctrl+F"]
    })
    
    # 模块状态
    enabled_modules: List = field(default_factory=lambda: [
        "consciousness", "reasoning", "emotion",
        "mouse", "keyboard", "window",
        "file_manager", "search",
        "nlu", "terminal"
    ])
    
    # 高级设置
    debug_mode: bool = False
    log_level: str = "INFO"
    
    # 元数据
    created_at: float = 0
    updated_at: float = 0
    version: str = "1.0"


class ModuleConfig:
    """模块配置"""
    
    def __init__(self, module_name: str):
        self.module_name = module_name
        self.enabled: bool = True
        self.settings: Dict[str, Any] = {}
        self.load()
    
    def load(self):
        """加载配置"""
        config_path = f"./data/config/{self.module_name}.json"
        
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.enabled = data.get('enabled', True)
                    self.settings = data.get('settings', {})
            except:
                pass
    
    def save(self):
        """保存配置"""
        config_path = f"./data/config/{self.module_name}.json"
        
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump({
                'enabled': self.enabled,
                'settings': self.settings
            }, f, ensure_ascii=False, indent=2)
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置"""
        return self.settings.get(key, default)
    
    def set(self, key: str, value: Any):
        """设置配置"""
        self.settings[key] = value
    
    def enable(self):
        """启用"""
        self.enabled = True
        self.save()
    
    def disable(self):
        """禁用"""
        self.enabled = False
        self.save()


class SettingsStorage:
    """设置存储"""
    
    def __init__(self, settings_path: str = "./data/settings"):
        self.settings_path = Path(settings_path)
        self.settings_path.mkdir(parents=True, exist_ok=True)
        
        # 配置文件
        self.user_settings_path = self.settings_path / "user_settings.json"
        
        # 模块配置目录
        self.config_dir = self.settings_path / "config"
        self.config_dir.mkdir(exist_ok=True)
        
        # 当前设置
        self.settings = UserSettings()
        self.module_configs: Dict[str, ModuleConfig] = {}
        
        # 加载
        self.load()
        
        print(f"✅ Settings Storage 已初始化")
    
    # ============ 用户设置 ============
    
    def load(self):
        """加载设置"""
        if self.user_settings_path.exists():
            try:
                with open(self.user_settings_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                    self.settings.language = data.get('language', self.settings.language)
                    self.settings.theme = data.get('theme', self.settings.theme)
                    self.settings.font_size = data.get('font_size', self.settings.font_size)
                    self.settings.show_emotions = data.get('show_emotions', self.settings.show_emotions)
                    self.settings.show_thinking = data.get('show_thinking', self.settings.show_thinking)
                    self.settings.show_timestamps = data.get('show_timestamps', self.settings.show_timestamps)
                    self.settings.compact_mode = data.get('compact_mode', self.settings.compact_mode)
                    self.settings.auto_save = data.get('auto_save', self.settings.auto_save)
                    self.settings.auto_save_interval = data.get('auto_save_interval', self.settings.auto_save_interval)
                    self.settings.max_history = data.get('max_history', self.settings.max_history)
                    self.settings.max_conversations = data.get('max_conversations', self.settings.max_conversations)
                    self.settings.speech_enabled = data.get('speech_enabled', self.settings.speech_enabled)
                    self.settings.tts_enabled = data.get('tts_enabled', self.settings.tts_enabled)
                    self.settings.voice_id = data.get('voice_id', self.settings.voice_id)
                    self.settings.speech_rate = data.get('speech_rate', self.settings.speech_rate)
                    self.settings.speech_pitch = data.get('speech_pitch', self.settings.speech_pitch)
                    self.settings.hotkeys = data.get('hotkeys', self.settings.hotkeys)
                    self.settings.enabled_modules = data.get('enabled_modules', self.settings.enabled_modules)
                    self.settings.debug_mode = data.get('debug_mode', self.settings.debug_mode)
                    self.settings.log_level = data.get('log_level', self.settings.log_level)
                    
                print(f"✅ 用户设置已加载")
                
            except Exception as e:
                print(f"⚠️ 设置加载失败: {e}")
                self.settings.created_at = datetime.now().timestamp()
        else:
            self.settings.created_at = datetime.now().timestamp()
            print("📝 使用默认设置")
        
        self.settings.updated_at = datetime.now().timestamp()
    
    def save(self):
        """保存设置"""
        data = {
            'language': self.settings.language,
            'theme': self.settings.theme,
            'font_size': self.settings.font_size,
            'show_emotions': self.settings.show_emotions,
            'show_thinking': self.settings.show_thinking,
            'show_timestamps': self.settings.show_timestamps,
            'compact_mode': self.settings.compact_mode,
            'auto_save': self.settings.auto_save,
            'auto_save_interval': self.settings.auto_save_interval,
            'max_history': self.settings.max_history,
            'max_conversations': self.settings.max_conversations,
            'speech_enabled': self.settings.speech_enabled,
            'tts_enabled': self.settings.tts_enabled,
            'voice_id': self.settings.voice_id,
            'speech_rate': self.settings.speech_rate,
            'speech_pitch': self.settings.speech_pitch,
            'hotkeys': self.settings.hotkeys,
            'enabled_modules': self.settings.enabled_modules,
            'debug_mode': self.settings.debug_mode,
            'log_level': self.settings.log_level,
            'version': self.settings.version,
            'updated_at': datetime.now().timestamp()
        }
        
        with open(self.user_settings_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 用户设置已保存")
    
    def reset(self):
        """重置设置"""
        self.settings = UserSettings()
        self.settings.created_at = datetime.now().timestamp()
        self.settings.updated_at = datetime.now().timestamp()
        self.save()
        print("✅ 设置已重置")
    
    # ============ 设置操作 ============
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取设置"""
        return getattr(self.settings, key, default)
    
    def set(self, key: str, value: Any):
        """设置"""
        if hasattr(self.settings, key):
            setattr(self.settings, key, value)
            self.settings.updated_at = datetime.now().timestamp()
    
    def update(self, updates: Dict[str, Any]):
        """批量更新"""
        for key, value in updates.items():
            self.set(key, value)
        self.save()
    
    # ============ 主题 ============
    
    def set_theme(self, theme: str):
        """设置主题"""
        self.settings.theme = theme
        self.save()
    
    def get_theme(self) -> str:
        """获取主题"""
        return self.settings.theme
    
    # ============ 语言 ============
    
    def set_language(self, language: str):
        """设置语言"""
        self.settings.language = language
        self.save()
    
    def get_language(self) -> str:
        """获取语言"""
        return self.settings.language
    
    # ============ 快捷键 ============
    
    def set_hotkey(self, action: str, keys: List[str]):
        """设置快捷键"""
        self.settings.hotkeys[action] = keys
        self.save()
    
    def get_hotkey(self, action: str) -> List[str]:
        """获取快捷键"""
        return self.settings.hotkeys.get(action, [])
    
    def get_all_hotkeys(self) -> Dict[str, List[str]]:
        """获取所有快捷键"""
        return self.settings.hotkeys.copy()
    
    # ============ 模块 ============
    
    def get_module_config(self, module_name: str) -> ModuleConfig:
        """获取模块配置"""
        if module_name not in self.module_configs:
            self.module_configs[module_name] = ModuleConfig(module_name)
        return self.module_configs[module_name]
    
    def is_module_enabled(self, module_name: str) -> bool:
        """检查模块是否启用"""
        return module_name in self.settings.enabled_modules
    
    def enable_module(self, module_name: str):
        """启用模块"""
        if module_name not in self.settings.enabled_modules:
            self.settings.enabled_modules.append(module_name)
            self.save()
            
            config = self.get_module_config(module_name)
            config.enable()
    
    def disable_module(self, module_name: str):
        """禁用模块"""
        if module_name in self.settings.enabled_modules:
            self.settings.enabled_modules.remove(module_name)
            self.save()
            
            config = self.get_module_config(module_name)
            config.disable()
    
    # ============ 语音 ============
    
    def set_voice(self, voice_id: str):
        """设置语音"""
        self.settings.voice_id = voice_id
        self.save()
    
    def get_voice(self) -> str:
        """获取语音"""
        return self.settings.voice_id
    
    def set_speech_rate(self, rate: float):
        """设置语速"""
        self.settings.speech_rate = rate
        self.save()
    
    def get_speech_rate(self) -> float:
        """获取语速"""
        return self.settings.speech_rate
    
    # ============ 导出/导入 ============
    
    def export(self, path: str = None) -> str:
        """导出设置"""
        data = {
            'settings': asdict(self.settings),
            'modules': {}
        }
        
        for name, config in self.module_configs.items():
            data['modules'][name] = {
                'enabled': config.enabled,
                'settings': config.settings
            }
        
        path = path or str(self.settings_path / "export.json")
        
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 设置已导出: {path}")
        return path
    
    def import_settings(self, path: str):
        """导入设置"""
        if not os.path.exists(path):
            print(f"❌ 文件不存在: {path}")
            return False
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if 'settings' in data:
                for key, value in data['settings'].items():
                    if hasattr(self.settings, key):
                        setattr(self.settings, key, value)
            
            self.settings.updated_at = datetime.now().timestamp()
            self.save()
            
            print(f"✅ 设置已导入: {path}")
            return True
            
        except Exception as e:
            print(f"❌ 导入失败: {e}")
            return False
    
    # ============ 统计 ============
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计"""
        return {
            'theme': self.settings.theme,
            'language': self.settings.language,
            'enabled_modules': len(self.settings.enabled_modules),
            'max_history': self.settings.max_history,
            'max_conversations': self.settings.max_conversations,
            'auto_save': self.settings.auto_save,
            'tts_enabled': self.settings.tts_enabled,
            'debug_mode': self.settings.debug_mode,
            'created_at': datetime.fromtimestamp(self.settings.created_at).isoformat(),
            'updated_at': datetime.fromtimestamp(self.settings.updated_at).isoformat()
        }


# 便捷函数
def create_settings_storage(path: str = "./data/settings") -> SettingsStorage:
    """创建设置存储"""
    return SettingsStorage(path)


# 测试代码
if __name__ == "__main__":
    print("⚙️ 设置存储测试")
    
    storage = create_settings_storage("/tmp/clawos_settings")
    
    # 获取统计
    print("\n1. 设置统计...")
    stats = storage.get_stats()
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    # 修改设置
    print("\n2. 修改设置...")
    storage.set_theme("dark")
    storage.set_language("zh")
    storage.set_voice("zh-CN-XiaoxiaoNeural")
    
    theme = storage.get_theme()
    print(f"   主题: {theme}")
    
    # 快捷键
    print("\n3. 快捷键...")
    hotkeys = storage.get_all_hotkeys()
    print(f"   快捷键: {hotkeys}")
    
    # 模块
    print("\n4. 模块...")
    enabled = storage.settings.enabled_modules
    print(f"   启用模块: {len(enabled)}")
    
    # 导出
    print("\n5. 导出...")
    storage.export("/tmp/clawos_settings/export.json")
    
    # 重置
    print("\n6. 重置...")
    storage.reset()
    
    print("\n✅ 测试完成")
