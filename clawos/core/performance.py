# 🦞 Performance - 性能优化

"""
性能优化模块

功能:
- 缓存管理
- 懒加载
- 并发优化
- 内存优化
"""

import asyncio
import time
import hashlib
from typing import Dict, Any, Optional, Callable
from functools import wraps
from dataclasses import dataclass
from pathlib import Path
import json


@dataclass
class CacheEntry:
    """缓存条目"""
    key: str
    value: Any
    created_at: float
    expires_at: float
    hits: int = 0


class CacheManager:
    """缓存管理器"""
    
    def __init__(self, max_size: int = 1000, ttl: int = 3600):
        self.cache: Dict[str, CacheEntry] = {}
        self.max_size = max_size
        self.default_ttl = ttl
        self.hits = 0
        self.misses = 0
    
    def get(self, key: str) -> Optional[Any]:
        """获取缓存"""
        if key in self.cache:
            entry = self.cache[key]
            if time.time() < entry.expires_at:
                entry.hits += 1
                self.hits += 1
                return entry.value
            else:
                del self.cache[key]
        self.misses += 1
        return None
    
    def set(self, key: str, value: Any, ttl: int = None):
        """设置缓存"""
        # 清理过期
        if len(self.cache) >= self.max_size:
            self._cleanup()
        
        expires = time.time() + (ttl or self.default_ttl)
        self.cache[key] = CacheEntry(
            key=key,
            value=value,
            created_at=time.time(),
            expires_at=expires
        )
    
    def _cleanup(self):
        """清理过期条目"""
        now = time.time()
        expired = [k for k, v in self.cache.items() if v.expires_at < now]
        for k in expired:
            del self.cache[k]
    
    def clear(self):
        """清空缓存"""
        self.cache.clear()
    
    def get_stats(self) -> Dict:
        """获取统计"""
        return {
            'size': len(self.cache),
            'hits': self.hits,
            'misses': self.misses,
            'hit_rate': self.hits / (self.hits + self.misses) if (self.hits + self.misses) > 0 else 0
        }


# 全局缓存
cache = CacheManager()


def cached(ttl: int = 3600, key_builder: Callable = None):
    """缓存装饰器"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # 构建缓存键
            if key_builder:
                cache_key = key_builder(*args, **kwargs)
            else:
                cache_key = hashlib.md5(
                    f"{args}{kwargs}".encode()
                ).hexdigest()
            
            # 检查缓存
            cached_value = cache.get(cache_key)
            if cached_value is not None:
                return cached_value
            
            # 执行函数
            if asyncio.iscoroutinefunction(func):
                result = await func(*args, **kwargs)
            else:
                result = func(*args, **kwargs)
            
            # 保存缓存
            cache.set(cache_key, result, ttl)
            return result
        return wrapper
    return decorator


class LazyLoader:
    """懒加载器"""
    
    def __init__(self):
        self._cache = {}
        self._loaders: Dict[str, Callable] = {}
    
    def register(self, name: str, loader: Callable):
        """注册加载器"""
        self._loaders[name] = loader
    
    def get(self, name: str) -> Any:
        """获取对象"""
        if name not in self._cache:
            if name in self._loaders:
                self._cache[name] = self._loaders[name]()
            else:
                raise ValueError(f"No loader for: {name}")
        return self._cache[name]


# 并发工具
async def gather_with_limit(tasks: list, limit: int = 10) -> list:
    """限制并发数"""
    semaphore = asyncio.Semaphore(limit)
    
    async def run_with_limit(task):
        async with semaphore:
            return await task
    
    return await asyncio.gather(*[run_with_limit(t) for t in tasks])


# 测试
if __name__ == "__main__":
    print("🔧 性能优化模块测试")
    
    # 缓存测试
    cache.set("test", "value")
    assert cache.get("test") == "value"
    print("✅ 缓存测试通过")
    
    # 统计
    stats = cache.get_stats()
    print(f"📊 缓存统计: {stats}")
    
    print("\n✅ 性能优化模块完成")
