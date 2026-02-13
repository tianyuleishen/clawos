# 🦞 Plugin Base - 插件基类

"""
插件基类 - ClawOS插件基础框架

功能:
- 插件生命周期
- 插件元数据
- 插件事件
- 钩子系统
"""

import asyncio
from typing import Dict, List, Optional, Any, Callable, Type, TypeVar
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
import json
import uuid
import importlib

T = TypeVar('T')


class PluginState(Enum):
    """插件状态"""
    LOADED = "loaded"
    ENABLED = "enabled"
    DISABLED = "disabled"
    ERROR = "error"
    UNLOADED = "unloaded"


class HookType(Enum):
    """钩子类型"""
    BEFORE_TASK = "before_task"
    AFTER_TASK = "after_task"
    ON_MESSAGE = "on_message"
    ON_ERROR = "on_error"
    ON_SHUTDOWN = "on_shutdown"
    ON_STARTUP = "on_startup"
    CUSTOM = "custom"


@dataclass
class PluginMetadata:
    """插件元数据"""
    id: str
    name: str
    version: str
    description: str
    author: str
    license: str = "MIT"
    dependencies: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    homepage: str = ""
    repository: str = ""
    min_clawos_version: str = "0.1.0"
    max_clawos_version: str = "1.0.0"


@dataclass
class PluginHook:
    """插件钩子"""
    name: str
    hook_type: HookType
    callback: Callable
    priority: int = 0  # 优先级,越小越先执行
    enabled: bool = True


class PluginBase:
    """插件基类"""
    
    # 子类必须设置
    metadata: PluginMetadata = None
    
    def __init__(self, plugin_id: str = None):
        self.id = plugin_id or (self.metadata.id if self.metadata else str(uuid.uuid4())[:8])
        self.name = self.metadata.name if self.metadata else self.__class__.__name__
        self.state = PluginState.UNLOADED
        self.hooks: List[PluginHook] = []
        self.config: Dict[str, Any] = {}
        self.logger = None
        
        print(f"✅ 插件已创建: {self.name}")
    
    # ============ 生命周期 ============
    
    async def load(self) -> bool:
        """加载插件
        
        Returns:
            bool: 是否成功
        """
        try:
            print(f"📦 加载插件: {self.name}")
            
            # 初始化日志
            self._init_logger()
            
            # 加载配置
            await self._load_config()
            
            # 初始化
            await self._initialize()
            
            self.state = PluginState.LOADED
            self.logger.info(f"插件 {self.name} 已加载")
            
            return True
            
        except Exception as e:
            self.state = PluginState.ERROR
            print(f"❌ 插件加载失败: {self.name} - {e}")
            return False
    
    async def enable(self) -> bool:
        """启用插件
        
        Returns:
            bool: 是否成功
        """
        try:
            if self.state == PluginState.ENABLED:
                return True
            
            print(f"▶️ 启用插件: {self.name}")
            
            await self._enable()
            
            self.state = PluginState.ENABLED
            
            if self.logger:
                self.logger.info(f"插件 {self.name} 已启用")
            
            return True
            
        except Exception as e:
            self.state = PluginState.ERROR
            print(f"❌ 插件启用失败: {self.name} - {e}")
            return False
    
    async def disable(self) -> bool:
        """禁用插件
        
        Returns:
            bool: 是否成功
        """
        try:
            if self.state == PluginState.DISABLED:
                return True
            
            print(f"⏸️ 禁用插件: {self.name}")
            
            await self._disable()
            
            self.state = PluginState.DISABLED
            
            if self.logger:
                self.logger.info(f"插件 {self.name} 已禁用")
            
            return True
            
        except Exception as e:
            self.state = PluginState.ERROR
            print(f"❌ 插件禁用失败: {self.name} - {e}")
            return False
    
    async def unload(self) -> bool:
        """卸载插件
        
        Returns:
            bool: 是否成功
        """
        try:
            print(f"📤 卸载插件: {self.name}")
            
            # 禁用
            if self.state == PluginState.ENABLED:
                await self.disable()
            
            # 清理
            await self._unload()
            
            # 保存配置
            await self._save_config()
            
            # 清除钩子
            self.hooks.clear()
            
            self.state = PluginState.UNLOADED
            
            if self.logger:
                self.logger.info(f"插件 {self.name} 已卸载")
            
            return True
            
        except Exception as e:
            self.state = PluginState.ERROR
            print(f"❌ 插件卸载失败: {self.name} - {e}")
            return False
    
    async def reload(self) -> bool:
        """重新加载插件
        
        Returns:
            bool: 是否成功
        """
        await self.unload()
        return await self.load()
    
    # ============ 子类重写 ============
    
    async def _initialize(self):
        """初始化 (子类可重写)"""
        pass
    
    async def _enable(self):
        """启用 (子类可重写)"""
        pass
    
    async def _disable(self):
        """禁用 (子类可重写)"""
        pass
    
    async def _unload(self):
        """卸载 (子类可重写)"""
        pass
    
    # ============ 配置 ============
    
    async def _load_config(self):
        """加载配置"""
        config_path = Path(f"./data/plugins/{self.id}/config.json")
        
        if config_path.exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
            except:
                self.config = {}
        else:
            self.config = {}
    
    async def _save_config(self):
        """保存配置"""
        config_path = Path(f"./data/plugins/{self.id}")
        config_path.mkdir(parents=True, exist_ok=True)
        
        with open(config_path / "config.json", 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)
    
    def get_config(self, key: str, default: Any = None) -> Any:
        """获取配置"""
        return self.config.get(key, default)
    
    def set_config(self, key: str, value: Any):
        """设置配置"""
        self.config[key] = value
    
    # ============ 钩子 ============
    
    def register_hook(
        self,
        name: str,
        hook_type: HookType,
        callback: Callable,
        priority: int = 0
    ):
        """注册钩子
        
        Args:
            name: 钩子名称
            hook_type: 钩子类型
            callback: 回调函数
            priority: 优先级
        """
        hook = PluginHook(
            name=name,
            hook_type=hook_type,
            callback=callback,
            priority=priority
        )
        
        self.hooks.append(hook)
        
        if self.logger:
            self.logger.debug(f"钩子已注册: {name}")
    
    def unregister_hook(self, name: str):
        """注销钩子"""
        self.hooks = [h for h in self.hooks if h.name != name]
    
    def get_hooks(self, hook_type: HookType = None) -> List[PluginHook]:
        """获取钩子列表"""
        if hook_type:
            return [h for h in self.hooks if h.hook_type == hook_type]
        return self.hooks.copy()
    
    # ============ 事件 ============
    
    async def emit_event(self, event_type: str, data: Dict = None):
        """发送事件
        
        Args:
            event_type: 事件类型
            data: 事件数据
        """
        if self.logger:
            self.logger.debug(f"事件: {event_type}")
        
        # 通知管理器
        await self._on_event(event_type, data or {})
    
    async def _on_event(self, event_type: str, data: Dict):
        """处理事件 (子类可重写)"""
        pass
    
    # ============ 工具 ============
    
    def _init_logger(self):
        """初始化日志"""
        import logging
        
        self.logger = logging.getLogger(f"plugin.{self.id}")
        self.logger.setLevel(logging.INFO)
        
        # 创建控制台处理器
        handler = logging.StreamHandler()
        handler.setFormatter(
            logging.Formatter(f'[{self.name}] %(levelname)s: %(message)s')
        )
        self.logger.addHandler(handler)
    
    def get_state(self) -> Dict:
        """获取插件状态"""
        return {
            'id': self.id,
            'name': self.name,
            'state': self.state.value,
            'hooks_count': len(self.hooks),
            'config_keys': list(self.config.keys())
        }
    
    def get_info(self) -> Dict:
        """获取插件信息"""
        return {
            'id': self.id,
            'name': self.metadata.name if self.metadata else self.name,
            'version': self.metadata.version if self.metadata else "0.1.0",
            'description': self.metadata.description if self.metadata else "",
            'author': self.metadata.author if self.metadata else "",
            'state': self.state.value
        }


# ============ 便捷函数 ============

def create_plugin(
    class_path: str,
    plugin_id: str = None
) -> Optional[PluginBase]:
    """创建插件实例
    
    Args:
        class_path: 类路径,例如 "my_plugins.example:MyPlugin"
        plugin_id: 插件ID
    
    Returns:
        PluginBase: 插件实例,或None
    """
    try:
        module_path, class_name = class_path.rsplit(':', 1)
        
        module = importlib.import_module(module_path)
        plugin_class = getattr(module, class_name)
        
        return plugin_class(plugin_id)
        
    except Exception as e:
        print(f"❌ 创建插件失败: {class_path} - {e}")
        return None


def load_plugin_from_file(file_path: str) -> Optional[PluginBase]:
    """从文件加载插件
    
    Args:
        file_path: 插件文件路径
    
    Returns:
        PluginBase: 插件实例,或None
    """
    try:
        plugin_path = Path(file_path)
        
        # 加载元数据
        metadata_path = plugin_path / "metadata.json"
        if metadata_path.exists():
            with open(metadata_path, 'r', encoding='utf-8') as f:
                metadata = PluginMetadata(**json.load(f))
        
        # 加载主模块
        main_file = plugin_path / "__init__.py"
        if main_file.exists():
            import sys
            sys.path.insert(0, str(plugin_path.parent))
            
            module_name = plugin_path.stem
            module = importlib.import_module(module_name)
            
            if hasattr(module, 'create_plugin'):
                return module.create_plugin(metadata)
        
        return None
        
    except Exception as e:
        print(f"❌ 加载插件失败: {file_path} - {e}")
        return None


# ============ 示例插件 ============

class ExamplePlugin(PluginBase):
    """示例插件"""
    
    metadata = PluginMetadata(
        id="example",
        name="示例插件",
        version="0.1.0",
        description="这是一个示例插件",
        author="ClawOS",
        tags=["example", "demo"],
        homepage="https://clawos.ai"
    )
    
    async def _initialize(self):
        """初始化"""
        self.logger.info("示例插件初始化")
        
        # 注册钩子
        self.register_hook(
            name="on_message_example",
            hook_type=HookType.ON_MESSAGE,
            callback=self._on_message_handler,
            priority=10
        )
    
    async def _on_message_handler(self, data: Dict):
        """消息处理"""
        self.logger.info(f"收到消息: {data}")
        
        return {"processed": True, "plugin": self.name}


# 测试代码
if __name__ == "__main__":
    async def test():
        print("🧪 插件基类测试")
        
        # 创建插件
        plugin = ExamplePlugin()
        
        # 加载
        success = await plugin.load()
        print(f"加载: {'成功' if success else '失败'}")
        
        # 启用
        success = await plugin.enable()
        print(f"启用: {'成功' if success else '失败'}")
        
        # 获取状态
        status = plugin.get_state()
        print(f"状态: {status}")
        
        # 获取信息
        info = plugin.get_info()
        print(f"信息: {info}")
        
        # 卸载
        success = await plugin.unload()
        print(f"卸载: {'成功' if success else '失败'}")
        
        print("\n✅ 测试完成")
    
    asyncio.run(test())
