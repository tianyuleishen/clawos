# 🦞 Plugin Manager - 插件管理器

"""
插件管理器 - ClawOS插件管理

功能:
- 插件注册/注销
- 插件加载/卸载
- 插件启用/禁用
- 插件依赖管理
"""

import asyncio
import os
import json
import importlib
from typing import Dict, List, Optional, Any, Callable, Type
from pathlib import Path
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import logging

from .base import PluginBase, PluginMetadata, PluginState, PluginHook, HookType, create_plugin

@dataclass
class PluginInfo:
    """插件信息"""
    id: str
    name: str
    version: str
    description: str
    author: str
    state: PluginState
    enabled: bool
    path: str
    metadata: Dict = field(default_factory=dict)


class PluginManager:
    """插件管理器"""
    
    def __init__(self, plugins_path: str = "./plugins"):
        self.plugins_path = Path(plugins_path)
        self.plugins_path.mkdir(parents=True, exist_ok=True)
        
        self.plugins: Dict[str, PluginBase] = {}
        self.plugin_info: Dict[str, PluginInfo] = {}
        self.hooks: Dict[str, List[PluginHook]] = {}
        
        self.event_callbacks: Dict[str, Callable] = {}
        
        # 日志
        self.logger = logging.getLogger("plugin_manager")
        self.logger.setLevel(logging.INFO)
        
        print(f"✅ Plugin Manager 已初始化")
        print(f"   插件目录: {self.plugins_path}")
    
    # ============ 注册/注销 ============
    
    def register(self, plugin: PluginBase) -> bool:
        """注册插件
        
        Args:
            plugin: 插件实例
        
        Returns:
            bool: 是否成功
        """
        if plugin.id in self.plugins:
            print(f"⚠️ 插件已注册: {plugin.id}")
            return False
        
        self.plugins[plugin.id] = plugin
        
        print(f"✅ 插件已注册: {plugin.name} ({plugin.id})")
        return True
    
    def unregister(self, plugin_id: str) -> bool:
        """注销插件
        
        Args:
            plugin_id: 插件ID
        
        Returns:
            bool: 是否成功
        """
        if plugin_id not in self.plugins:
            return False
        
        plugin = self.plugins.pop(plugin_id)
        
        # 清除钩子
        self._remove_plugin_hooks(plugin_id)
        
        print(f"✅ 插件已注销: {plugin.name}")
        return True
    
    def get_plugin(self, plugin_id: str) -> Optional[PluginBase]:
        """获取插件"""
        return self.plugins.get(plugin_id)
    
    def get_all_plugins(self) -> List[PluginBase]:
        """获取所有插件"""
        return list(self.plugins.values())
    
    # ============ 加载/卸载 ============
    
    async def load_plugin(self, plugin_id: str) -> bool:
        """加载插件
        
        Args:
            plugin_id: 插件ID
        
        Returns:
            bool: 是否成功
        """
        plugin = self.get_plugin(plugin_id)
        if not plugin:
            print(f"❌ 插件不存在: {plugin_id}")
            return False
        
        # 检查依赖
        if plugin.metadata:
            if not await self._check_dependencies(plugin.metadata.dependencies):
                print(f"❌ 依赖检查失败: {plugin.name}")
                return False
        
        # 加载
        success = await plugin.load()
        
        if success:
            self._update_plugin_info(plugin)
        
        return success
    
    async def load_all(self) -> int:
        """加载所有插件
        
        Returns:
            int: 成功加载的数量
        """
        loaded = 0
        
        for plugin in self.get_all_plugins():
            if plugin.state == PluginState.UNLOADED:
                if await self.load_plugin(plugin.id):
                    loaded += 1
        
        print(f"✅ 已加载 {loaded}/{len(self.plugins)} 个插件")
        return loaded
    
    async def unload_plugin(self, plugin_id: str) -> bool:
        """卸载插件
        
        Args:
            plugin_id: 插件ID
        
        Returns:
            bool: 是否成功
        """
        plugin = self.get_plugin(plugin_id)
        if not plugin:
            return False
        
        # 如果已启用,先禁用
        if plugin.state == PluginState.ENABLED:
            await self.disable_plugin(plugin_id)
        
        success = await plugin.unload()
        
        if success:
            self._update_plugin_info(plugin)
        
        return success
    
    async def unload_all(self):
        """卸载所有插件"""
        for plugin_id in list(self.plugins.keys()):
            await self.unload_plugin(plugin_id)
        
        print("✅ 所有插件已卸载")
    
    # ============ 启用/禁用 ============
    
    async def enable_plugin(self, plugin_id: str) -> bool:
        """启用插件
        
        Args:
            plugin_id: 插件ID
        
        Returns:
            bool: 是否成功
        """
        plugin = self.get_plugin(plugin_id)
        if not plugin:
            return False
        
        if plugin.state == PluginState.ENABLED:
            return True
        
        if plugin.state == PluginState.UNLOADED:
            if not await self.load_plugin(plugin_id):
                return False
        
        success = await plugin.enable()
        
        if success:
            # 注册钩子
            self._register_plugin_hooks(plugin)
            self._update_plugin_info(plugin)
        
        return success
    
    async def enable_all(self) -> int:
        """启用所有插件
        
        Returns:
            int: 成功启用的数量
        """
        enabled = 0
        
        for plugin in self.get_all_plugins():
            if plugin.state == PluginState.LOADED:
                if await self.enable_plugin(plugin.id):
                    enabled += 1
        
        print(f"✅ 已启用 {enabled}/{len(self.plugins)} 个插件")
        return enabled
    
    async def disable_plugin(self, plugin_id: str) -> bool:
        """禁用插件
        
        Args:
            plugin_id: 插件ID
        
        Returns:
            bool: 是否成功
        """
        plugin = self.get_plugin(plugin_id)
        if not plugin:
            return False
        
        if plugin.state != PluginState.ENABLED:
            return True
        
        # 清除钩子
        self._remove_plugin_hooks(plugin_id)
        
        success = await plugin.disable()
        
        if success:
            self._update_plugin_info(plugin)
        
        return success
    
    async def disable_all(self):
        """禁用所有插件"""
        for plugin_id in list(self.plugins.keys()):
            await self.disable_plugin(plugin_id)
        
        print("✅ 所有插件已禁用")
    
    # ============ 依赖管理 ============
    
    async def _check_dependencies(self, dependencies: List[str]) -> bool:
        """检查依赖
        
        Args:
            dependencies: 依赖列表
        
        Returns:
            bool: 是否满足依赖
        """
        if not dependencies:
            return True
        
        for dep in dependencies:
            # 检查依赖的插件
            if dep in self.plugins:
                plugin = self.plugins[dep]
                if plugin.state not in [PluginState.LOADED, PluginState.ENABLED]:
                    print(f"❌ 依赖插件未加载: {dep}")
                    return False
            else:
                # 尝试作为Python包加载
                try:
                    importlib.import_module(dep)
                except ImportError:
                    print(f"❌ 依赖不存在: {dep}")
                    return False
        
        return True
    
    # ============ 插件发现 ============
    
    def discover_plugins(self) -> List[str]:
        """发现本地插件
        
        Returns:
            List[str]: 发现的插件ID列表
        """
        discovered = []
        
        for plugin_dir in self.plugins_path.iterdir():
            if plugin_dir.is_dir():
                plugin_id = plugin_dir.name
                metadata_file = plugin_dir / "metadata.json"
                
                if metadata_file.exists():
                    discovered.append(plugin_id)
                    print(f"📦 发现插件: {plugin_id}")
        
        return discovered
    
    async def install_plugin(self, source: str) -> bool:
        """安装插件
        
        Args:
            source: 源路径 (可以是本地路径或URL)
        
        Returns:
            bool: 是否成功
        """
        try:
            # 本地安装
            if os.path.exists(source):
                source_path = Path(source)
                plugin_id = source_path.name
                target_path = self.plugins_path / plugin_id
                
                # 复制
                import shutil
                shutil.copytree(source_path, target_path)
                
                print(f"✅ 插件已安装: {plugin_id}")
                return True
            
            # URL安装 (未来实现)
            print(f"⚠️ URL安装尚未实现: {source}")
            return False
            
        except Exception as e:
            print(f"❌ 插件安装失败: {e}")
            return False
    
    async def uninstall_plugin(self, plugin_id: str) -> bool:
        """卸载插件
        
        Args:
            plugin_id: 插件ID
        
        Returns:
            bool: 是否成功
        """
        # 先禁用和卸载
        await self.disable_plugin(plugin_id)
        await self.unload_plugin(plugin_id)
        
        # 注销
        self.unregister(plugin_id)
        
        # 删除文件
        plugin_path = self.plugins_path / plugin_id
        if plugin_path.exists():
            import shutil
            shutil.rmtree(plugin_path)
            print(f"✅ 插件已卸载: {plugin_id}")
            return True
        
        return False
    
    # ============ 钩子管理 ============
    
    def _register_plugin_hooks(self, plugin: PluginBase):
        """注册插件钩子"""
        for hook in plugin.hooks:
            if hook.enabled:
                if hook.hook_type.value not in self.hooks:
                    self.hooks[hook.hook_type.value] = []
                
                self.hooks[hook.hook_type.value].append(hook)
                
                # 按优先级排序
                self.hooks[hook.hook_type.value].sort(
                    key=lambda x: x.priority
                )
    
    def _remove_plugin_hooks(self, plugin_id: str):
        """移除插件钩子"""
        plugin = self.plugins.get(plugin_id)
        if not plugin:
            return
        
        for hook_type, hook_list in self.hooks.items():
            self.hooks[hook_type] = [
                h for h in hook_list
                if h.callback.__self__.id != plugin_id
            ]
    
    def register_hook(
        self,
        hook_type: HookType,
        callback: Callable,
        plugin_id: str = "system"
    ):
        """注册钩子 (系统级)"""
        if hook_type.value not in self.hooks:
            self.hooks[hook_type.value] = []
        
        hook = PluginHook(
            name=f"{plugin_id}_{hook_type.value}",
            hook_type=hook_type,
            callback=callback,
            plugin_id=plugin_id
        )
        
        self.hooks[hook_type.value].append(hook)
        self.hooks[hook_type.value].sort(key=lambda x: x.priority)
    
    async def trigger_hooks(
        self,
        hook_type: HookType,
        data: Dict = None
    ) -> List[Any]:
        """触发钩子
        
        Args:
            hook_type: 钩子类型
            data: 数据
        
        Returns:
            List[Any]: 所有钩子的返回值
        """
        results = []
        
        hooks = self.hooks.get(hook_type.value, [])
        
        for hook in hooks:
            if hasattr(hook.callback, '__self__'):
                plugin = hook.callback.__self__
                if plugin.id in self.plugins:
                    if self.plugins[plugin.id].state != PluginState.ENABLED:
                        continue
            
            try:
                if asyncio.iscoroutinefunction(hook.callback):
                    result = await hook.callback(data or {})
                else:
                    result = hook.callback(data or {})
                results.append(result)
            except Exception as e:
                print(f"❌ 钩子执行失败: {hook.name} - {e}")
        
        return results
    
    # ============ 事件管理 ============
    
    def on_event(self, event_type: str, callback: Callable):
        """注册事件回调
        
        Args:
            event_type: 事件类型
            callback: 回调函数
        """
        self.event_callbacks[event_type] = callback
    
    async def emit_event(self, event_type: str, data: Dict = None):
        """发送事件
        
        Args:
            event_type: 事件类型
            data: 数据
        """
        # 调用注册的回调
        callback = self.event_callbacks.get(event_type)
        if callback:
            if asyncio.iscoroutinefunction(callback):
                await callback(data or {})
            else:
                callback(data or {})
        
        # 调用ON_EVENT钩子
        await self.trigger_hooks(HookType.ON_EVENT, {'type': event_type, 'data': data})
    
    # ============ 状态查询 ============
    
    def get_status(self) -> Dict:
        """获取插件管理器状态"""
        states = {}
        for plugin in self.plugins.values():
            state = plugin.state.value
            states[state] = states.get(state, 0) + 1
        
        return {
            'total': len(self.plugins),
            'states': states,
            'hooks_count': sum(len(h) for h in self.hooks.values())
        }
    
    def list_plugins(self) -> List[PluginInfo]:
        """列出所有插件"""
        return list(self.plugin_info.values())
    
    def get_plugin_info(self, plugin_id: str) -> Optional[PluginInfo]:
        """获取插件信息"""
        return self.plugin_info.get(plugin_id)
    
    def _update_plugin_info(self, plugin: PluginBase):
        """更新插件信息"""
        enabled = plugin.state == PluginState.ENABLED
        
        self.plugin_info[plugin.id] = PluginInfo(
            id=plugin.id,
            name=plugin.name,
            version=plugin.metadata.version if plugin.metadata else "0.1.0",
            description=plugin.metadata.description if plugin.metadata else "",
            author=plugin.metadata.author if plugin.metadata else "",
            state=plugin.state,
            enabled=enabled,
            path=str(self.plugins_path / plugin.id),
            metadata={
                'name': plugin.metadata.name if plugin.metadata else plugin.name,
                'version': plugin.metadata.version if plugin.metadata else "0.1.0",
                'dependencies': plugin.metadata.dependencies if plugin.metadata else [],
                'tags': plugin.metadata.tags if plugin.metadata else []
            }
        )
    
    # ============ 初始化 ============
    
    async def initialize(self):
        """初始化插件系统"""
        print("🚀 初始化插件系统...")
        
        # 发现插件
        discovered = self.discover_plugins()
        
        # 自动加载和启用
        loaded = await self.load_all()
        enabled = await self.enable_all()
        
        print(f"✅ 插件系统初始化完成: {loaded} 加载, {enabled} 启用")
    
    async def shutdown(self):
        """关闭插件系统"""
        print("🛑 关闭插件系统...")
        
        # 禁用所有
        await self.disable_all()
        
        # 卸载所有
        await self.unload_all()
        
        print("✅ 插件系统已关闭")


# ============ 便捷函数 ============

def create_plugin_manager(plugins_path: str = "./plugins") -> PluginManager:
    """创建插件管理器"""
    return PluginManager(plugins_path)


# 测试代码
if __name__ == "__main__":
    async def test():
        print("🧪 插件管理器测试")
        
        manager = PluginManager("/tmp/clawos_plugins")
        
        # 创建示例插件
        from clawos.plugins.base import ExamplePlugin
        plugin = ExamplePlugin()
        
        # 注册
        manager.register(plugin)
        
        # 加载
        success = await manager.load_plugin(plugin.id)
        print(f"加载: {'成功' if success else '失败'}")
        
        # 启用
        success = await manager.enable_plugin(plugin.id)
        print(f"启用: {'成功' if success else '失败'}")
        
        # 状态
        status = manager.get_status()
        print(f"状态: {status}")
        
        # 列出
        plugins = manager.list_plugins()
        for p in plugins:
            print(f"  - {p.name}: {p.state.value}")
        
        # 禁用
        success = await manager.disable_plugin(plugin.id)
        print(f"禁用: {'成功' if success else '失败'}")
        
        # 卸载
        success = await manager.unload_plugin(plugin.id)
        print(f"卸载: {'成功' if success else '失败'}")
        
        print("\n✅ 测试完成")
    
    asyncio.run(test())
