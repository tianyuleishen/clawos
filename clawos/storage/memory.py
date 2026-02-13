# 🦞 Memory Storage - 内存存储

"""
内存存储 - ClawOS记忆持久化

功能:
- 短期记忆
- 长期记忆
- 事实存储
- 经验学习
"""

import asyncio
import json
import os
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from pathlib import Path
from dataclasses import dataclass, field
from enum import Enum
import uuid
import time

from .base import JSONStorage, StorageConfig

class MemoryType(Enum):
    """记忆类型"""
    SHORT_TERM = "short_term"      # 短期记忆
    LONG_TERM = "long_term"         # 长期记忆
    EPISODIC = "episodic"          # 情景记忆
    SEMANTIC = "semantic"           # 语义记忆
    PROCEDURAL = "procedural"       # 程序性记忆
    WORKING = "working"            # 工作记忆

class Importance(Enum):
    """重要性"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class Memory:
    """记忆"""
    id: str
    content: str
    memory_type: str
    importance: int
    timestamp: float
    last_accessed: float
    access_count: int
    metadata: Dict
    embedding: List[float] = None


@dataclass
class Fact:
    """事实"""
    id: str
    statement: str
    category: str
    confidence: float
    source: str
    timestamp: float
    verified: bool


@dataclass
class Experience:
    """经验"""
    id: str
    situation: str
    action: str
    outcome: str
    lessons: List[str]
    timestamp: float
    success: bool


class MemoryStorage:
    """记忆存储"""
    
    def __init__(self, storage_path: str = "./data/memory"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        # 各类存储
        self.short_term = JSONStorage(
            "short_term",
            StorageConfig(path=str(self.storage_path))
        )
        
        self.long_term = JSONStorage(
            "long_term",
            StorageConfig(path=str(self.storage_path))
        )
        
        self.episodic = JSONStorage(
            "episodic",
            StorageConfig(path=str(self.storage_path))
        )
        
        self.semantic = JSONStorage(
            "semantic",
            StorageConfig(path=str(self.storage_path))
        )
        
        self.procedural = JSONStorage(
            "procedural",
            StorageConfig(path=str(self.storage_path))
        )
        
        self.working = JSONStorage(
            "working",
            StorageConfig(path=str(self.storage_path))
        )
        
        # 事实存储
        self.facts = JSONStorage(
            "facts",
            StorageConfig(path=str(self.storage_path))
        )
        
        # 经验存储
        self.experiences = JSONStorage(
            "experiences",
            StorageConfig(path=str(self.storage_path))
        )
        
        # 创建索引
        self.long_term.create_index("importance")
        self.semantic.create_index("category")
        self.episodic.create_index("timestamp")
        
        print(f"✅ Memory Storage 已初始化")
    
    # ============ 短期记忆 ============
    
    def add_short_term(
        self,
        content: str,
        importance: int = Importance.MEDIUM.value,
        metadata: Dict = None
    ) -> str:
        """添加短期记忆"""
        now = time.time()
        
        record_id = str(uuid.uuid4())[:8]
        
        self.short_term.create(record_id, {
            'content': content,
            'importance': importance,
            'timestamp': now,
            'last_accessed': now,
            'access_count': 0,
            'metadata': metadata or {}
        })
        
        return record_id
    
    def get_short_term(self, id: str = None, limit: int = 10) -> List[Dict]:
        """获取短期记忆"""
        records = self.short_term.read_all()
        
        # 按时间排序
        records.sort(key=lambda x: x.data['timestamp'], reverse=True)
        
        if limit:
            records = records[:limit]
        
        return [
            {
                'id': r.id,
                'content': r.data['content'],
                'importance': r.data['importance'],
                'timestamp': r.data['timestamp']
            }
            for r in records
        ]
    
    def clear_short_term(self):
        """清空短期记忆"""
        self.short_term.clear()
    
    def promote_to_long_term(self, id: str) -> bool:
        """提升为长期记忆"""
        record = self.short_term.read(id)
        if record:
            self.long_term.create(id, record.data)
            self.short_term.delete(id)
            return True
        return False
    
    # ============ 长期记忆 ============
    
    def add_long_term(
        self,
        content: str,
        importance: int = Importance.MEDIUM.value,
        metadata: Dict = None
    ) -> str:
        """添加长期记忆"""
        now = time.time()
        
        record_id = str(uuid.uuid4())[:8]
        
        self.long_term.create(record_id, {
            'content': content,
            'importance': importance,
            'timestamp': now,
            'last_accessed': now,
            'access_count': 0,
            'metadata': metadata or {}
        })
        
        return record_id
    
    def get_long_term(
        self,
        min_importance: int = Importance.LOW.value,
        limit: int = 100
    ) -> List[Dict]:
        """获取长期记忆"""
        records = self.long_term.read_all()
        
        # 按重要性过滤
        records = [r for r in records if r.data['importance'] >= min_importance]
        
        # 按访问时间排序
        records.sort(key=lambda x: x.data['last_accessed'], reverse=True)
        
        if limit:
            records = records[:limit]
        
        return [
            {
                'id': r.id,
                'content': r.data['content'],
                'importance': r.data['importance'],
                'last_accessed': r.data['last_accessed'],
                'access_count': r.data['access_count']
            }
            for r in records
        ]
    
    def access_memory(self, id: str, memory_type: str = "long_term"):
        """访问记忆"""
        storage = getattr(self, memory_type, self.long_term)
        
        record = storage.read(id)
        if record:
            record.data['last_accessed'] = time.time()
            record.data['access_count'] += 1
            storage.modified = True
    
    # ============ 情景记忆 ============
    
    def add_episodic(
        self,
        content: str,
        situation: str,
        outcome: str,
        importance: int = Importance.MEDIUM.value
    ) -> str:
        """添加情景记忆"""
        now = time.time()
        
        record_id = str(uuid.uuid4())[:8]
        
        self.episodic.create(record_id, {
            'content': content,
            'situation': situation,
            'outcome': outcome,
            'importance': importance,
            'timestamp': now,
            'last_accessed': now,
            'access_count': 0
        })
        
        return record_id
    
    def get_episodic(
        self,
        situation: str = None,
        limit: int = 50
    ) -> List[Dict]:
        """获取情景记忆"""
        records = self.episodic.read_all()
        
        if situation:
            records = [
                r for r in records
                if situation.lower() in r.data.get('situation', '').lower()
            ]
        
        records.sort(key=lambda x: x.data['timestamp'], reverse=True)
        
        if limit:
            records = records[:limit]
        
        return [
            {
                'id': r.id,
                'content': r.data['content'],
                'situation': r.data['situation'],
                'outcome': r.data['outcome'],
                'timestamp': r.data['timestamp']
            }
            for r in records
        ]
    
    # ============ 语义记忆 ============
    
    def add_semantic(
        self,
        statement: str,
        category: str,
        confidence: float = 0.9,
        metadata: Dict = None
    ) -> str:
        """添加语义记忆"""
        now = time.time()
        
        record_id = str(uuid.uuid4())[:8]
        
        self.semantic.create(record_id, {
            'statement': statement,
            'category': category,
            'confidence': confidence,
            'timestamp': now,
            'metadata': metadata or {}
        })
        
        return record_id
    
    def get_semantic(
        self,
        category: str = None,
        limit: int = 100
    ) -> List[Dict]:
        """获取语义记忆"""
        records = self.semantic.read_all()
        
        if category:
            records = [
                r for r in records
                if r.data.get('category') == category
            ]
        
        if limit:
            records = records[:limit]
        
        return [
            {
                'id': r.id,
                'statement': r.data['statement'],
                'category': r.data['category'],
                'confidence': r.data['confidence'],
                'timestamp': r.data['timestamp']
            }
            for r in records
        ]
    
    def query_semantic(self, query: str) -> List[Dict]:
        """语义查询"""
        records = self.semantic.read_all()
        
        # 简单关键词匹配
        keywords = query.lower().split()
        results = []
        
        for r in records:
            content = r.data['statement'].lower()
            if any(kw in content for kw in keywords):
                results.append({
                    'id': r.id,
                    'statement': r.data['statement'],
                    'category': r.data['category'],
                    'confidence': r.data['confidence']
                })
        
        return results
    
    # ============ 程序性记忆 ============
    
    def add_procedural(
        self,
        procedure: str,
        steps: List[str],
        category: str
    ) -> str:
        """添加程序性记忆"""
        now = time.time()
        
        record_id = str(uuid.uuid4())[:8]
        
        self.procedural.create(record_id, {
            'procedure': procedure,
            'steps': steps,
            'category': category,
            'timestamp': now,
            'executed_count': 0,
            'success_rate': 0.0
        })
        
        return record_id
    
    def get_procedures(
        self,
        category: str = None,
        limit: int = 50
    ) -> List[Dict]:
        """获取程序"""
        records = self.procedural.read_all()
        
        if category:
            records = [
                r for r in records
                if r.data.get('category') == category
            ]
        
        if limit:
            records = records[:limit]
        
        return [
            {
                'id': r.id,
                'procedure': r.data['procedure'],
                'steps': r.data['steps'],
                'category': r.data['category'],
                'executed_count': r.data['executed_count']
            }
            for r in records
        ]
    
    # ============ 工作记忆 ============
    
    def set_working(self, key: str, value: Any):
        """设置工作记忆"""
        self.working.create(key, {
            'value': value,
            'timestamp': time.time()
        })
    
    def get_working(self, key: str) -> Any:
        """获取工作记忆"""
        record = self.working.read(key)
        if record:
            return record.data['value']
        return None
    
    def clear_working(self):
        """清空工作记忆"""
        self.working.clear()
    
    # ============ 事实 ============
    
    def add_fact(
        self,
        statement: str,
        category: str,
        confidence: float = 1.0,
        source: str = "user"
    ) -> str:
        """添加事实"""
        now = time.time()
        
        record_id = str(uuid.uuid4())[:8]
        
        self.facts.create(record_id, {
            'statement': statement,
            'category': category,
            'confidence': confidence,
            'source': source,
            'timestamp': now,
            'verified': False
        })
        
        return record_id
    
    def verify_fact(self, id: str) -> bool:
        """验证事实"""
        record = self.facts.read(id)
        if record:
            self.facts.update(id, {'verified': True})
            return True
        return False
    
    def get_facts(
        self,
        category: str = None,
        verified: bool = None
    ) -> List[Dict]:
        """获取事实"""
        records = self.facts.read_all()
        
        if category is not None:
            records = [
                r for r in records
                if r.data.get('category') == category
            ]
        
        if verified is not None:
            records = [
                r for r in records
                if r.data.get('verified') == verified
            ]
        
        return [
            {
                'id': r.id,
                'statement': r.data['statement'],
                'category': r.data['category'],
                'confidence': r.data['confidence'],
                'verified': r.data['verified'],
                'source': r.data['source']
            }
            for r in records
        ]
    
    # ============ 经验 ============
    
    def add_experience(
        self,
        situation: str,
        action: str,
        outcome: str,
        success: bool,
        lessons: List[str] = None
    ) -> str:
        """添加经验"""
        now = time.time()
        
        record_id = str(uuid.uuid4())[:8]
        
        self.experiences.create(record_id, {
            'situation': situation,
            'action': action,
            'outcome': outcome,
            'lessons': lessons or [],
            'timestamp': now,
            'success': success
        })
        
        return record_id
    
    def get_experiences(
        self,
        success: bool = None,
        limit: int = 50
    ) -> List[Dict]:
        """获取经验"""
        records = self.experiences.read_all()
        
        if success is not None:
            records = [
                r for r in records
                if r.data.get('success') == success
            ]
        
        records.sort(key=lambda x: x.data['timestamp'], reverse=True)
        
        if limit:
            records = records[:limit]
        
        return [
            {
                'id': r.id,
                'situation': r.data['situation'],
                'action': r.data['action'],
                'outcome': r.data['outcome'],
                'lessons': r.data['lessons'],
                'success': r.data['success'],
                'timestamp': r.data['timestamp']
            }
            for r in records
        ]
    
    # ============ 统计 ============
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计"""
        return {
            'short_term': self.short_term.count(),
            'long_term': self.long_term.count(),
            'episodic': self.episodic.count(),
            'semantic': self.semantic.count(),
            'procedural': self.procedural.count(),
            'working': self.working.count(),
            'facts': self.facts.count(),
            'experiences': self.experiences.count()
        }
    
    # ============ 保存/加载 ============
    
    def save(self):
        """保存所有"""
        self.short_term.save()
        self.long_term.save()
        self.episodic.save()
        self.semantic.save()
        self.procedural.save()
        self.working.save()
        self.facts.save()
        self.experiences.save()
        print("✅ 记忆数据已保存")
    
    def cleanup(self, older_than_days: int = 30):
        """清理旧数据"""
        cutoff = time.time() - (older_than_days * 24 * 3600)
        
        # 清理短期记忆
        for record in self.short_term.read_all():
            if record.data['timestamp'] < cutoff:
                self.short_term.delete(record.id)
        
        print("✅ 旧记忆已清理")


# 便捷函数
def create_memory_storage(path: str = "./data/memory") -> MemoryStorage:
    """创建记忆存储"""
    return MemoryStorage(path)


# 测试代码
if __name__ == "__main__":
    print("🧠 记忆存储测试")
    
    memory = create_memory_storage("/tmp/clawos_memory")
    
    # 短期记忆
    print("\n1. 短期记忆...")
    id1 = memory.add_short_term("用户问关于天气的问题", Importance.HIGH.value)
    id2 = memory.add_short_term("用户想要听音乐", Importance.MEDIUM.value)
    st = memory.get_short_term()
    print(f"   {len(st)} 条")
    
    # 长期记忆
    print("\n2. 长期记忆...")
    id3 = memory.add_long_term("用户偏好深色主题", Importance.HIGH.value)
    id4 = memory.add_long_term("用户经常使用中文", Importance.MEDIUM.value)
    lt = memory.get_long_term()
    print(f"   {len(lt)} 条")
    
    # 情景记忆
    print("\n3. 情景记忆...")
    memory.add_episodic(
        "用户询问天气",
        "天气查询",
        "提供了天气信息",
        Importance.MEDIUM.value
    )
    ep = memory.get_episodic()
    print(f"   {len(ep)} 条")
    
    # 语义记忆
    print("\n4. 语义记忆...")
    memory.add_semantic("北京是中国的首都", "地理", 1.0)
    memory.add_semantic("Python是一种编程语言", "技术", 0.95)
    sm = memory.get_semantic()
    print(f"   {len(sm)} 条")
    
    # 事实
    print("\n5. 事实...")
    fact_id = memory.add_fact("用户叫张三", "个人信息", 0.9)
    facts = memory.get_facts()
    print(f"   {len(facts)} 条")
    
    # 经验
    print("\n6. 经验...")
    memory.add_experience(
        "用户要求打开应用",
        "使用系统命令启动应用",
        "成功打开",
        True,
        ["可以使用os.system", "更好的方法是subprocess"]
    )
    exp = memory.get_experiences()
    print(f"   {len(exp)} 条")
    
    # 统计
    print("\n7. 统计...")
    stats = memory.get_stats()
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    # 保存
    print("\n8. 保存...")
    memory.save()
    
    print("\n✅ 测试完成")
