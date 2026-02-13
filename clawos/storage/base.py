# 🦞 Storage Base - 存储基类

"""
存储基类 - ClawOS数据持久化基础

功能:
- 基础CRUD操作
- 数据验证
- 序列化/反序列化
- 索引管理
"""

import asyncio
import json
import os
import sqlite3
from typing import Dict, List, Any, Optional, Type, TypeVar
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from abc import ABC, abstractmethod

T = TypeVar('T')

@dataclass
class StorageConfig:
    """存储配置"""
    path: str = "./data"
    max_records: int = 10000
    auto_save: bool = True
    compress: bool = False
    encrypt: bool = False

@dataclass
class Record:
    """记录"""
    id: str
    data: Dict[str, Any]
    created_at: float
    updated_at: float
    version: int = 1
    deleted: bool = False

class StorageBase(ABC):
    """存储基类"""
    
    def __init__(self, name: str, config: StorageConfig = None):
        self.name = name
        self.config = config or StorageConfig()
        self.records: Dict[str, Record] = {}
        self.indexes: Dict[str, Dict[str, str]] = {}
        self.modified = False
        
        # 确保目录存在
        Path(self.config.path).mkdir(parents=True, exist_ok=True)
        
        print(f"✅ Storage {name} 已初始化")
    
    # ============ CRUD操作 ============
    
    def create(self, id: str, data: Dict[str, Any]) -> Record:
        """创建记录"""
        if id in self.records:
            raise ValueError(f"记录已存在: {id}")
        
        now = datetime.now().timestamp()
        
        record = Record(
            id=id,
            data=data,
            created_at=now,
            updated_at=now,
            version=1,
            deleted=False
        )
        
        self.records[id] = record
        
        # 更新索引
        self._update_indexes(id, data)
        
        self.modified = True
        
        return record
    
    def read(self, id: str) -> Optional[Record]:
        """读取记录"""
        record = self.records.get(id)
        if record and not record.deleted:
            return record
        return None
    
    def read_all(self, include_deleted: bool = False) -> List[Record]:
        """读取所有记录"""
        records = [r for r in self.records.values() if include_deleted or not r.deleted]
        return records
    
    def update(self, id: str, data: Dict[str, Any]) -> Optional[Record]:
        """更新记录"""
        if id not in self.records:
            return None
        
        record = self.records[id]
        record.data.update(data)
        record.updated_at = datetime.now().timestamp()
        record.version += 1
        
        # 更新索引
        self._update_indexes(id, record.data)
        
        self.modified = True
        
        return record
    
    def delete(self, id: str, permanent: bool = False) -> bool:
        """删除记录"""
        if id not in self.records:
            return False
        
        if permanent:
            del self.records[id]
            self._remove_from_indexes(id)
        else:
            self.records[id].deleted = True
            self.records[id].updated_at = datetime.now().timestamp()
        
        self.modified = True
        
        return True
    
    def undelete(self, id: str) -> bool:
        """恢复删除"""
        if id in self.records and self.records[id].deleted:
            self.records[id].deleted = False
            self.records[id].updated_at = datetime.now().timestamp()
            self.modified = True
            return True
        return False
    
    # ============ 查询 ============
    
    def find(self, **criteria) -> List[Record]:
        """条件查询"""
        results = []
        
        for record in self.records.values():
            if record.deleted:
                continue
            
            match = True
            
            for key, value in criteria.items():
                if key not in record.data:
                    match = False
                    break
                if record.data[key] != value:
                    match = False
                    break
            
            if match:
                results.append(record)
        
        return results
    
    def find_one(self, **criteria) -> Optional[Record]:
        """查询单个"""
        results = self.find(**criteria)
        return results[0] if results else None
    
    def count(self, include_deleted: bool = False) -> int:
        """计数"""
        return len([r for r in self.records.values() 
                   if include_deleted or not r.deleted])
    
    def exists(self, id: str) -> bool:
        """检查存在"""
        return id in self.records and not self.records[id].deleted
    
    # ============ 索引 ============
    
    def create_index(self, field: str):
        """创建索引"""
        if field not in self.indexes:
            self.indexes[field] = {}
            for id, record in self.records.items():
                if not record.deleted and field in record.data:
                    self.indexes[field][record.data[field]] = id
    
    def _update_indexes(self, id: str, data: Dict[str, Any]):
        """更新索引"""
        for field, index in self.indexes.items():
            if field in data:
                index[data[field]] = id
    
    def _remove_from_indexes(self, id: str):
        """从索引移除"""
        record = self.records.get(id)
        if record:
            for field, index in self.indexes.items():
                if field in record.data:
                    index.pop(record.data[field], None)
    
    def query_by_index(self, field: str, value: Any) -> Optional[Record]:
        """按索引查询"""
        if field not in self.indexes:
            return None
        
        id = self.indexes[field].get(value)
        if id:
            return self.read(id)
        return None
    
    # ============ 批量操作 ============
    
    def bulk_create(self, records: List[Dict[str, Any]]) -> List[Record]:
        """批量创建"""
        created = []
        
        for record_data in records:
            import uuid
            id = record_data.get('id', str(uuid.uuid4())[:8])
            created.append(self.create(id, record_data))
        
        return created
    
    def bulk_delete(self, ids: List[str], permanent: bool = False) -> int:
        """批量删除"""
        count = 0
        for id in ids:
            if self.delete(id, permanent):
                count += 1
        return count
    
    def clear(self, permanent: bool = True):
        """清空"""
        if permanent:
            self.records.clear()
            self.indexes.clear()
        else:
            for record in self.records.values():
                record.deleted = True
                record.updated_at = datetime.now().timestamp()
        self.modified = True
    
    # ============ 序列化 ============
    
    def serialize(self, record: Record) -> str:
        """序列化"""
        return json.dumps({
            'id': record.id,
            'data': record.data,
            'created_at': record.created_at,
            'updated_at': record.updated_at,
            'version': record.version,
            'deleted': record.deleted
        }, ensure_ascii=False)
    
    def deserialize(self, json_str: str) -> Record:
        """反序列化"""
        data = json.loads(json_str)
        
        return Record(
            id=data['id'],
            data=data['data'],
            created_at=data['created_at'],
            updated_at=data['updated_at'],
            version=data['version'],
            deleted=data['deleted']
        )
    
    # ============ 保存/加载 ============
    
    @abstractmethod
    def save(self, path: str = None) -> bool:
        """保存数据"""
        pass
    
    @abstractmethod
    def load(self, path: str = None) -> bool:
        """加载数据"""
        pass
    
    # ============ 统计 ============
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计"""
        records = [r for r in self.records.values() if not r.deleted]
        
        total_size = sum(
            len(json.dumps(r.data)) for r in records
        )
        
        return {
            'total_records': len(self.records),
            'active_records': len(records),
            'deleted_records': len(self.records) - len(records),
            'indexes': len(self.indexes),
            'size_bytes': total_size,
            'modified': self.modified
        }


class JSONStorage(StorageBase):
    """JSON文件存储"""
    
    def __init__(self, name: str, config: StorageConfig = None):
        super().__init__(name, config)
        self.file_path = os.path.join(self.config.path, f"{name}.json")
        
        # 自动加载
        if os.path.exists(self.file_path):
            self.load()
    
    def save(self, path: str = None) -> bool:
        """保存到JSON文件"""
        file_path = path or self.file_path
        
        try:
            data = {
                'version': 1,
                'saved_at': datetime.now().isoformat(),
                'records': [
                    {
                        'id': r.id,
                        'data': r.data,
                        'created_at': r.created_at,
                        'updated_at': r.updated_at,
                        'version': r.version,
                        'deleted': r.deleted
                    }
                    for r in self.records.values()
                ],
                'indexes': self.indexes
            }
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            self.modified = False
            
            print(f"✅ 已保存: {file_path} ({len(self.records)} 条记录)")
            return True
            
        except Exception as e:
            print(f"❌ 保存失败: {e}")
            return False
    
    def load(self, path: str = None) -> bool:
        """从JSON文件加载"""
        file_path = path or self.file_path
        
        if not os.path.exists(file_path):
            return False
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.records.clear()
            self.indexes.clear()
            
            for record_data in data.get('records', []):
                record = Record(
                    id=record_data['id'],
                    data=record_data['data'],
                    created_at=record_data['created_at'],
                    updated_at=record_data['updated_at'],
                    version=record_data['version'],
                    deleted=record_data.get('deleted', False)
                )
                self.records[record.id] = record
            
            self.indexes = data.get('indexes', {})
            
            self.modified = False
            
            print(f"✅ 已加载: {file_path} ({len(self.records)} 条记录)")
            return True
            
        except Exception as e:
            print(f"❌ 加载失败: {e}")
            return False


class SQLiteStorage(StorageBase):
    """SQLite数据库存储"""
    
    def __init__(self, name: str, config: StorageConfig = None):
        super().__init__(name, config)
        
        db_path = os.path.join(self.config.path, f"{name}.db")
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        
        # 初始化表
        self._init_table()
        
        # 加载数据
        self._load_from_db()
    
    def _init_table(self):
        """初始化表"""
        cursor = self.conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS records (
                id TEXT PRIMARY KEY,
                data TEXT,
                created_at REAL,
                updated_at REAL,
                version INTEGER,
                deleted INTEGER DEFAULT 0
            )
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_updated_at 
            ON records(updated_at)
        ''')
        
        self.conn.commit()
    
    def _load_from_db(self):
        """从数据库加载"""
        cursor = self.conn.cursor()
        
        cursor.execute('SELECT * FROM records WHERE deleted = 0')
        
        for row in cursor.fetchall():
            record = Record(
                id=row['id'],
                data=json.loads(row['data'] or '{}'),
                created_at=row['created_at'],
                updated_at=row['updated_at'],
                version=row['version'],
                deleted=bool(row['deleted'])
            )
            self.records[record.id] = record
        
        self.modified = False
    
    def save(self, path: str = None) -> bool:
        """保存到数据库"""
        try:
            cursor = self.conn.cursor()
            
            for id, record in self.records.items():
                cursor.execute('''
                    INSERT OR REPLACE INTO records 
                    (id, data, created_at, updated_at, version, deleted)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    id,
                    json.dumps(record.data, ensure_ascii=False),
                    record.created_at,
                    record.updated_at,
                    record.version,
                    1 if record.deleted else 0
                ))
            
            self.conn.commit()
            self.modified = False
            
            print(f"✅ 数据库已保存: ({len(self.records)} 条记录)")
            return True
            
        except Exception as e:
            print(f"❌ 保存失败: {e}")
            return False
    
    def load(self, path: str = None) -> bool:
        """加载数据"""
        self._load_from_db()
        return True
    
    def close(self):
        """关闭连接"""
        if self.conn:
            self.conn.close()


# 便捷函数
def create_storage(
    name: str,
    storage_type: str = "json",
    path: str = "./data"
) -> StorageBase:
    """创建存储实例"""
    config = StorageConfig(path=path)
    
    if storage_type == "json":
        return JSONStorage(name, config)
    elif storage_type == "sqlite":
        return SQLiteStorage(name, config)
    else:
        return JSONStorage(name, config)


# 测试代码
if __name__ == "__main__":
    import uuid
    
    print("💾 存储基类测试")
    
    # 创建JSON存储
    storage = JSONStorage("test", StorageConfig(path="/tmp"))
    
    # 创建记录
    print("\n1. 测试CRUD操作...")
    
    id1 = str(uuid.uuid4())[:8]
    record1 = storage.create(id1, {"name": "测试1", "value": 100})
    print(f"   创建: {record1.id}")
    
    id2 = str(uuid.uuid4())[:8]
    record2 = storage.create(id2, {"name": "测试2", "value": 200})
    print(f"   创建: {record2.id}")
    
    # 读取
    print(f"\n2. 测试读取...")
    found = storage.read(id1)
    print(f"   读取: {found.data}")
    
    # 查询
    print(f"\n3. 测试查询...")
    results = storage.find(name="测试1")
    print(f"   查询结果: {len(results)} 条")
    
    # 统计
    print(f"\n4. 测试统计...")
    stats = storage.get_stats()
    print(f"   统计: {stats}")
    
    # 保存
    print(f"\n5. 测试保存...")
    storage.save()
    
    # 清空
    print(f"\n6. 测试清空...")
    storage.clear()
    print(f"   清空后: {storage.count()} 条")
    
    print("\n✅ 测试完成")
