# 🦞 Plugin Store - 插件商店

"""
插件商店 - 插件安装和管理

功能:
- 插件市场浏览
- 插件安装/更新
- 插件评分
- 本地缓存
"""

import asyncio
import os
import json
import shutil
from typing import Dict, List, Optional, Any
from pathlib import Path
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import hashlib

from .base import PluginMetadata, PluginBase
from .manager import PluginManager


class PluginCategory(Enum):
    """插件分类"""
    ALL = "all"
    PRODUCTIVITY = "productivity"  # 效率工具
    DEVELOPER = "developer"       # 开发者工具
    INTEGRATION = "integration"   # 集成
    ENTERTAINMENT = "entertainment" # 娱乐
    UTILITY = "utility"          # 实用工具
    AI = "ai"                     # AI相关
    CUSTOM = "custom"             # 自定义


@dataclass
class PluginItem:
    """商店插件项"""
    id: str
    name: str
    description: str
    version: str
    author: str
    category: str
    icon: str = ""
    screenshots: List[str] = field(default_factory=list)
    rating: float = 0.0
    download_count: int = 0
    price: float = 0.0
    tags: List[str] = field(default_factory=list)
    homepage: str = ""
    repository: str = ""
    license: str = "MIT"
    min_version: str = "0.1.0"
    max_version: str = "1.0.0"
    dependencies: List[str] = field(default_factory=list)
    installed: bool = False
    installed_version: str = None
    update_available: bool = False


@dataclass
class PluginReview:
    """插件评价"""
    id: str
    plugin_id: str
    user_id: str
    rating: int
    comment: str
    created_at: float


class PluginStore:
    """插件商店"""
    
    def __init__(self, store_path: str = "./data/store"):
        self.store_path = Path(store_path)
        self.store_path.mkdir(parents=True, exist_ok=True)
        
        self.cache_path = self.store_path / "cache"
        self.cache_path.mkdir(exist_ok=True)
        
        self.local_plugins: Dict[str, PluginItem] = {}
        self.remote_plugins: Dict[str, PluginItem] = {}
        
        self.installed_plugins: Dict[str, str] = {}  # plugin_id -> version
        self.reviews: Dict[str, List[PluginReview]] = {}
        
        # 加载本地索引
        self._load_local_index()
        
        print(f"✅ Plugin Store 已初始化")
        print(f"   商店路径: {self.store_path}")
    
    # ============ 插件管理 ============
    
    def get_plugin(self, plugin_id: str) -> Optional[PluginItem]:
        """获取插件信息"""
        # 先检查本地
        if plugin_id in self.local_plugins:
            return self.local_plugins[plugin_id]
        
        # 检查远程
        return self.remote_plugins.get(plugin_id)
    
    def get_all_plugins(self) -> List[PluginItem]:
        """获取所有插件"""
        plugins = list(self.local_plugins.values())
        plugins.extend([
            p for p in self.remote_plugins.values()
            if p.id not in self.local_plugins
        ])
        return plugins
    
    def get_plugins_by_category(self, category: PluginCategory) -> List[PluginItem]:
        """按分类获取插件"""
        plugins = self.get_all_plugins()
        
        if category == PluginCategory.ALL:
            return plugins
        
        return [p for p in plugins if p.category == category.value]
    
    def search_plugins(self, query: str) -> List[PluginItem]:
        """搜索插件"""
        query = query.lower()
        
        plugins = self.get_all_plugins()
        
        results = []
        for plugin in plugins:
            # 匹配名称、描述、标签
            if (query in plugin.name.lower() or
                query in plugin.description.lower() or
                any(query in tag.lower() for tag in plugin.tags)):
                results.append(plugin)
        
        return results
    
    def get_popular_plugins(self, limit: int = 10) -> List[PluginItem]:
        """获取热门插件"""
        plugins = self.get_all_plugins()
        plugins.sort(key=lambda x: x.download_count, reverse=True)
        return plugins[:limit]
    
    def get_new_plugins(self, limit: int = 10) -> List[PluginItem]:
        """获取新插件"""
        plugins = self.get_all_plugins()
        plugins.sort(key=lambda x: x.version, reverse=True)
        return plugins[:limit]
    
    # ============ 安装管理 ============
    
    def install_plugin(self, plugin_id: str) -> bool:
        """安装插件
        
        Args:
            plugin_id: 插件ID
        
        Returns:
            bool: 是否成功
        """
        plugin = self.get_plugin(plugin_id)
        if not plugin:
            print(f"❌ 插件不存在: {plugin_id}")
            return False
        
        if plugin.installed:
            print(f"⚠️ 插件已安装: {plugin_id}")
            return False
        
        try:
            # 下载插件
            if plugin_id in self.remote_plugins:
                # 从远程下载
                print(f"📦 下载插件: {plugin.name}")
                self._download_plugin(plugin)
            
            # 更新本地索引
            plugin.installed = True
            plugin.installed_version = plugin.version
            
            self.installed_plugins[plugin_id] = plugin.version
            self._save_local_index()
            
            print(f"✅ 插件已安装: {plugin.name}")
            return True
            
        except Exception as e:
            print(f"❌ 插件安装失败: {e}")
            return False
    
    def uninstall_plugin(self, plugin_id: str) -> bool:
        """卸载插件
        
        Args:
            plugin_id: 插件ID
        
        Returns:
            bool: 是否成功
        """
        if plugin_id not in self.installed_plugins:
            print(f"❌ 插件未安装: {plugin_id}")
            return False
        
        try:
            # 从管理器卸载
            # (由外部调用plugin_manager.uninstall_plugin)
            
            # 更新索引
            if plugin_id in self.local_plugins:
                self.local_plugins[plugin_id].installed = False
                self.local_plugins[plugin_id].installed_version = None
            
            self.installed_plugins.pop(plugin_id)
            self._save_local_index()
            
            # 删除缓存
            cache_dir = self.cache_path / plugin_id
            if cache_dir.exists():
                shutil.rmtree(cache_dir)
            
            print(f"✅ 插件已卸载: {plugin_id}")
            return True
            
        except Exception as e:
            print(f"❌ 插件卸载失败: {e}")
            return False
    
    def update_plugin(self, plugin_id: str) -> bool:
        """更新插件
        
        Args:
            plugin_id: 插件ID
        
        Returns:
            bool: 是否成功
        """
        plugin = self.get_plugin(plugin_id)
        if not plugin:
            return False
        
        if not plugin.update_available:
            print(f"⚠️ 无可用更新: {plugin_id}")
            return False
        
        # 卸载旧版本
        self.uninstall_plugin(plugin_id)
        
        # 安装新版本
        return self.install_plugin(plugin_id)
    
    def check_updates(self) -> List[PluginItem]:
        """检查更新
        
        Returns:
            List[PluginItem]: 有更新的插件列表
        """
        updates = []
        
        for plugin_id, version in self.installed_plugins.items():
            plugin = self.get_plugin(plugin_id)
            if plugin and plugin.version != version:
                updates.append(plugin)
                plugin.update_available = True
        
        return updates
    
    # ============ 评分评论 ============
    
    def rate_plugin(
        self,
        plugin_id: str,
        user_id: str,
        rating: int,
        comment: str = ""
    ) -> bool:
        """评价插件
        
        Args:
            plugin_id: 插件ID
            user_id: 用户ID
            rating: 评分 (1-5)
            comment: 评论
        
        Returns:
            bool: 是否成功
        """
        if not 1 <= rating <= 5:
            return False
        
        if plugin_id not in self.reviews:
            self.reviews[plugin_id] = []
        
        review = PluginReview(
            id=f"{user_id}_{datetime.now().timestamp()}",
            plugin_id=plugin_id,
            user_id=user_id,
            rating=rating,
            comment=comment,
            created_at=datetime.now().timestamp()
        )
        
        self.reviews[plugin_id].append(review)
        
        # 更新平均评分
        self._update_plugin_rating(plugin_id)
        
        return True
    
    def get_plugin_reviews(
        self,
        plugin_id: str,
        limit: int = 10
    ) -> List[PluginReview]:
        """获取插件评价"""
        reviews = self.reviews.get(plugin_id, [])
        return sorted(reviews, key=lambda x: x.created_at, reverse=True)[:limit]
    
    def get_plugin_rating(self, plugin_id: str) -> float:
        """获取插件平均评分"""
        reviews = self.reviews.get(plugin_id, [])
        if not reviews:
            return 0.0
        
        return sum(r.rating for r in reviews) / len(reviews)
    
    def _update_plugin_rating(self, plugin_id: str):
        """更新插件评分"""
        rating = self.get_plugin_rating(plugin_id)
        
        if plugin_id in self.local_plugins:
            self.local_plugins[plugin_id].rating = rating
        
        if plugin_id in self.remote_plugins:
            self.remote_plugins[plugin_id].rating = rating
    
    # ============ 缓存管理 ============
    
    def clear_cache(self):
        """清理缓存"""
        if self.cache_path.exists():
            shutil.rmtree(self.cache_path)
            self.cache_path.mkdir(exist_ok=True)
        print("✅ 缓存已清理")
    
    def get_cache_size(self) -> int:
        """获取缓存大小"""
        total = 0
        for path in self.cache_path.rglob("*"):
            if path.is_file():
                total += path.stat().st_size
        return total
    
    def _download_plugin(self, plugin: PluginItem):
        """下载插件"""
        from .manager import PluginManager
        
        # 模拟下载 (实际应该从服务器下载)
        plugin_dir = self.cache_path / plugin.id
        plugin_dir.mkdir(exist_ok=True)
        
        # 创建示例插件
        metadata = {
            'id': plugin.id,
            'name': plugin.name,
            'version': plugin.version,
            'description': plugin.description,
            'author': plugin.author,
            'license': plugin.license,
            'dependencies': plugin.dependencies,
            'tags': plugin.tags,
            'homepage': plugin.homepage,
            'repository': plugin.repository,
            'min_clawos_version': plugin.min_version,
            'max_clawos_version': plugin.max_version
        }
        
        with open(plugin_dir / "metadata.json", 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
        
        # 添加到本地索引
        self.local_plugins[plugin.id] = PluginItem(
            id=plugin.id,
            name=plugin.name,
            description=plugin.description,
            version=plugin.version,
            author=plugin.author,
            category=plugin.category,
            installed=True,
            installed_version=plugin.version
        )
    
    # ============ 索引管理 ============
    
    def _load_local_index(self):
        """加载本地索引"""
        index_file = self.store_path / "index.json"
        
        if index_file.exists():
            try:
                with open(index_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                self.local_plugins = {
                    k: PluginItem(**v) for k, v in data.get('plugins', {}).items()
                }
                
                self.installed_plugins = data.get('installed', {})
                
            except Exception as e:
                print(f"⚠️ 加载索引失败: {e}")
    
    def _save_local_index(self):
        """保存本地索引"""
        index_file = self.store_path / "index.json"
        
        data = {
            'plugins': {
                k: {
                    'id': v.id,
                    'name': v.name,
                    'description': v.description,
                    'version': v.version,
                    'author': v.author,
                    'category': v.category,
                    'rating': v.rating,
                    'download_count': v.download_count,
                    'installed': v.installed,
                    'installed_version': v.installed_version,
                    'tags': v.tags,
                    'icon': v.icon,
                    'homepage': v.homepage,
                    'license': v.license,
                    'dependencies': v.dependencies,
                    'min_version': v.min_version,
                    'max_version': v.max_version
                }
                for k, v in self.local_plugins.items()
            },
            'installed': self.installed_plugins,
            'updated_at': datetime.now().isoformat()
        }
        
        with open(index_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def add_local_plugin(self, plugin_dir: str) -> bool:
        """添加本地插件
        
        Args:
            plugin_dir: 插件目录
        
        Returns:
            bool: 是否成功
        """
        try:
            plugin_path = Path(plugin_dir)
            metadata_file = plugin_path / "metadata.json"
            
            if not metadata_file.exists():
                print(f"❌ 插件元数据不存在: {plugin_dir}")
                return False
            
            with open(metadata_file, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
            
            plugin = PluginItem(
                id=metadata['id'],
                name=metadata['name'],
                description=metadata.get('description', ''),
                version=metadata.get('version', '0.1.0'),
                author=metadata.get('author', ''),
                category=metadata.get('category', 'utility'),
                installed=True,
                installed_version=metadata.get('version', '0.1.0'),
                tags=metadata.get('tags', []),
                homepage=metadata.get('homepage', ''),
                license=metadata.get('license', 'MIT'),
                min_version=metadata.get('min_clawos_version', '0.1.0'),
                max_version=metadata.get('max_clawos_version', '1.0.0'),
                dependencies=metadata.get('dependencies', [])
            )
            
            self.local_plugins[plugin.id] = plugin
            self.installed_plugins[plugin.id] = plugin.version
            
            self._save_local_index()
            
            print(f"✅ 本地插件已添加: {plugin.name}")
            return True
            
        except Exception as e:
            print(f"❌ 添加本地插件失败: {e}")
            return False
    
    # ============ 统计 ============
    
    def get_stats(self) -> Dict:
        """获取商店统计"""
        return {
            'total_plugins': len(self.get_all_plugins()),
            'installed_plugins': len(self.installed_plugins),
            'categories': len(set(p.category for p in self.local_plugins.values())),
            'reviews_count': sum(len(r) for r in self.reviews.values()),
            'cache_size': self.get_cache_size()
        }


# ============ 便捷函数 ============

def create_plugin_store(store_path: str = "./data/store") -> PluginStore:
    """创建插件商店"""
    return PluginStore(store_path)


# 测试代码
if __name__ == "__main__":
    async def test():
        print("🧪 Plugin Store 测试")
        
        store = create_plugin_store("/tmp/clawos_store")
        
        # 添加示例插件
        print("\n1. 添加本地插件...")
        success = store.add_local_plugin("/tmp/example_plugin")
        print(f"   {'成功' if success else '失败'}")
        
        # 列出插件
        print("\n2. 插件列表...")
        plugins = store.get_all_plugins()
        print(f"   总数: {len(plugins)}")
        
        # 搜索
        print("\n3. 搜索插件...")
        results = store.search_plugins("示例")
        print(f"   找到: {len(results)}")
        
        # 安装
        print("\n4. 安装插件...")
        if plugins:
            success = store.install_plugin(plugins[0].id)
            print(f"   {'成功' if success else '失败'}")
        
        # 统计
        print("\n5. 商店统计...")
        stats = store.get_stats()
        print(f"   {stats}")
        
        print("\n✅ 测试完成")
    
    asyncio.run(test())
