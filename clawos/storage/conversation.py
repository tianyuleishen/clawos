# 🦞 Conversation Storage - 对话历史存储

"""
对话历史存储 - ClawOS对话持久化

功能:
- 对话消息存储
- 对话会话管理
- 搜索和检索
- 导出功能
"""

import asyncio
import json
import os
from typing import Dict, List, Optional, Any
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, field
from enum import Enum
import uuid

from .base import JSONStorage, StorageConfig, Record

class MessageRole(Enum):
    """消息角色"""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

@dataclass
class ConversationMessage:
    """对话消息"""
    id: str
    role: str
    content: str
    timestamp: float
    emotion: str = None
    confidence: float = None
    metadata: Dict = field(default_factory=dict)

@dataclass
class ConversationSession:
    """对话会话"""
    id: str
    title: str
    messages: List[ConversationMessage]
    created_at: float
    updated_at: float
    metadata: Dict = field(default_factory=dict)


class ConversationStorage:
    """对话历史存储"""
    
    def __init__(self, storage_path: str = "./data/conversations"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        # 主存储 (会话索引)
        self.sessions_storage = JSONStorage(
            "conversation_sessions",
            StorageConfig(path=str(self.storage_path))
        )
        
        # 消息存储
        self.messages_storage = JSONStorage(
            "conversation_messages",
            StorageConfig(path=str(self.storage_path))
        )
        
        # 当前会话
        self.current_session_id: str = None
        
        # 创建索引
        self.sessions_storage.create_index("title")
        self.sessions_storage.create_index("updated_at")
        
        print(f"✅ Conversation Storage 已初始化")
        print(f"   存储路径: {self.storage_path}")
    
    # ============ 会话管理 ============
    
    def create_session(
        self,
        title: str = "新对话",
        metadata: Dict = None
    ) -> ConversationSession:
        """创建会话"""
        import time
        now = time.time()
        
        session = ConversationSession(
            id=str(uuid.uuid4())[:8],
            title=title,
            messages=[],
            created_at=now,
            updated_at=now,
            metadata=metadata or {}
        )
        
        # 保存会话
        self.sessions_storage.create(session.id, {
            'title': title,
            'message_count': 0,
            'created_at': now,
            'updated_at': now,
            'metadata': metadata or {}
        })
        
        return session
    
    def get_session(self, session_id: str) -> Optional[ConversationSession]:
        """获取会话"""
        record = self.sessions_storage.read(session_id)
        if not record:
            return None
        
        # 获取消息
        messages = self._load_messages(session_id)
        
        return ConversationSession(
            id=session_id,
            title=record.data['title'],
            messages=messages,
            created_at=record.data['created_at'],
            updated_at=record.data['updated_at'],
            metadata=record.data.get('metadata', {})
        )
    
    def get_all_sessions(self) -> List[Dict]:
        """获取所有会话摘要"""
        sessions = self.sessions_storage.read_all()
        
        return [
            {
                'id': s.id,
                'title': s.data['title'],
                'message_count': s.data['message_count'],
                'created_at': s.data['created_at'],
                'updated_at': s.data['updated_at']
            }
            for s in sorted(sessions, key=lambda x: x.data['updated_at'], reverse=True)
        ]
    
    def update_session_title(self, session_id: str, title: str) -> bool:
        """更新会话标题"""
        record = self.sessions_storage.read(session_id)
        if record:
            self.sessions_storage.update(session_id, {'title': title})
            return True
        return False
    
    def delete_session(self, session_id: str, permanent: bool = True) -> bool:
        """删除会话"""
        # 删除消息
        messages = self._load_messages(session_id)
        for msg in messages:
            self.messages_storage.delete(msg.id, permanent)
        
        # 删除会话
        return self.sessions_storage.delete(session_id, permanent)
    
    # ============ 消息管理 ============
    
    def add_message(
        self,
        session_id: str,
        role: str,
        content: str,
        emotion: str = None,
        confidence: float = None,
        metadata: Dict = None
    ) -> ConversationMessage:
        """添加消息"""
        import time
        now = time.time()
        
        if not session_id:
            session_id = self.current_session_id or "default"
        
        message = ConversationMessage(
            id=str(uuid.uuid4())[:8],
            role=role,
            content=content,
            timestamp=now,
            emotion=emotion,
            confidence=confidence,
            metadata=metadata or {}
        )
        
        # 保存消息
        self.messages_storage.create(message.id, {
            'session_id': session_id,
            'role': role,
            'content': content,
            'timestamp': now,
            'emotion': emotion,
            'confidence': confidence,
            'metadata': metadata or {}
        })
        
        # 更新会话
        self._update_session_message_count(session_id)
        self.current_session_id = session_id
        
        return message
    
    def add_user_message(
        self,
        content: str,
        session_id: str = None
    ) -> ConversationMessage:
        """添加用户消息"""
        return self.add_message(
            session_id or self.current_session_id,
            MessageRole.USER.value,
            content
        )
    
    def add_assistant_message(
        self,
        content: str,
        emotion: str = None,
        confidence: float = None,
        session_id: str = None
    ) -> ConversationMessage:
        """添加助手消息"""
        return self.add_message(
            session_id or self.current_session_id,
            MessageRole.ASSISTANT.value,
            content,
            emotion=emotion,
            confidence=confidence
        )
    
    def add_system_message(
        self,
        content: str,
        session_id: str = None
    ) -> ConversationMessage:
        """添加系统消息"""
        return self.add_message(
            session_id or self.current_session_id,
            MessageRole.SYSTEM.value,
            content
        )
    
    def get_messages(
        self,
        session_id: str = None,
        limit: int = None,
        offset: int = 0
    ) -> List[ConversationMessage]:
        """获取消息列表"""
        session = session_id or self.current_session_id
        
        messages = self._load_messages(session)
        
        # 排序 (按时间)
        messages.sort(key=lambda x: x.timestamp)
        
        # 分页
        if offset:
            messages = messages[offset:]
        if limit:
            messages = messages[:limit]
        
        return messages
    
    def _load_messages(self, session_id: str) -> List[ConversationMessage]:
        """加载消息"""
        records = self.messages_storage.find(session_id=session_id)
        
        messages = []
        for record in records:
            messages.append(ConversationMessage(
                id=record.id,
                role=record.data['role'],
                content=record.data['content'],
                timestamp=record.data['timestamp'],
                emotion=record.data.get('emotion'),
                confidence=record.data.get('confidence'),
                metadata=record.data.get('metadata', {})
            ))
        
        return messages
    
    def _update_session_message_count(self, session_id: str):
        """更新会话消息数"""
        record = self.sessions_storage.read(session_id)
        if record:
            count = len(self._load_messages(session_id))
            self.sessions_storage.update(session_id, {
                'message_count': count,
                'updated_at': datetime.now().timestamp()
            })
    
    # ============ 当前会话 ============
    
    def set_current_session(self, session_id: str):
        """设置当前会话"""
        self.current_session_id = session_id
    
    def get_current_session(self) -> Optional[ConversationSession]:
        """获取当前会话"""
        if self.current_session_id:
            return self.get_session(self.current_session_id)
        return None
    
    def new_session(self, title: str = "新对话") -> ConversationSession:
        """创建并切换到新会话"""
        session = self.create_session(title)
        self.current_session_id = session.id
        return session
    
    # ============ 搜索 ============
    
    def search_messages(
        self,
        query: str,
        session_id: str = None,
        limit: int = 100
    ) -> List[ConversationMessage]:
        """搜索消息"""
        messages = self._load_messages(session_id)
        
        # 简单文本搜索
        results = [
            msg for msg in messages
            if query.lower() in msg.content.lower()
        ]
        
        return results[:limit]
    
    def search_sessions(self, query: str) -> List[Dict]:
        """搜索会话"""
        sessions = self.sessions_storage.find()
        
        results = []
        for session in sessions:
            if query.lower() in session.data['title'].lower():
                results.append({
                    'id': session.id,
                    'title': session.data['title'],
                    'message_count': session.data['message_count'],
                    'created_at': session.data['created_at']
                })
        
        return results
    
    # ============ 导出/导入 ============
    
    def export_session(
        self,
        session_id: str = None,
        format: str = "json"
    ) -> str:
        """导出会话"""
        session = self.get_session(session_id or self.current_session_id)
        if not session:
            return ""
        
        if format == "json":
            return json.dumps({
                'id': session.id,
                'title': session.title,
                'created_at': session.created_at,
                'messages': [
                    {
                        'id': msg.id,
                        'role': msg.role,
                        'content': msg.content,
                        'timestamp': msg.timestamp,
                        'emotion': msg.emotion
                    }
                    for msg in session.messages
                ]
            }, ensure_ascii=False, indent=2)
        
        elif format == "text":
            lines = [f"# {session.title}\n"]
            lines.append(f"创建时间: {datetime.fromtimestamp(session.created_at)}\n")
            lines.append("-" * 50)
            
            for msg in session.messages:
                role_name = "用户" if msg.role == "user" else "助手"
                lines.append(f"[{role_name}] {datetime.fromtimestamp(msg.timestamp)}")
                lines.append(msg.content)
                lines.append("")
            
            return "\n".join(lines)
        
        return ""
    
    def import_session(self, data: str, format: str = "json") -> Optional[ConversationSession]:
        """导入会话"""
        try:
            if format == "json":
                session_data = json.loads(data)
                
                session = self.create_session(
                    title=session_data.get('title', '导入的对话'),
                    metadata={'imported': True}
                )
                
                for msg_data in session_data.get('messages', []):
                    self.add_message(
                        session.id,
                        msg_data['role'],
                        msg_data['content'],
                        emotion=msg_data.get('emotion')
                    )
                
                return session
            
        except Exception as e:
            print(f"导入失败: {e}")
        
        return None
    
    # ============ 统计 ============
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计"""
        sessions = self.sessions_storage.read_all()
        
        total_messages = 0
        for session in sessions:
            total_messages += session.data.get('message_count', 0)
        
        return {
            'total_sessions': len(sessions),
            'total_messages': total_messages,
            'current_session': self.current_session_id
        }
    
    # ============ 保存/加载 ============
    
    def save(self):
        """保存所有数据"""
        self.sessions_storage.save()
        self.messages_storage.save()
        print("✅ 对话数据已保存")
    
    def cleanup(self, keep_days: int = 30):
        """清理旧数据"""
        import time
        cutoff = time.time() - (keep_days * 24 * 3600)
        
        sessions = self.sessions_storage.read_all(include_deleted=True)
        
        deleted_count = 0
        for session in sessions:
            if session.data.get('updated_at', 0) < cutoff:
                self.delete_session(session.id)
                deleted_count += 1
        
        print(f"✅ 清理完成: {deleted_count} 个会话")


# 便捷函数
def create_conversation_storage(path: str = "./data/conversations") -> ConversationStorage:
    """创建对话存储"""
    return ConversationStorage(path)


# 测试代码
if __name__ == "__main__":
    print("💬 对话存储测试")
    
    storage = create_conversation_storage("/tmp/clawos_conversations")
    
    # 创建会话
    print("\n1. 创建会话...")
    session = storage.new_session("测试对话")
    print(f"   会话ID: {session.id}")
    
    # 添加消息
    print("\n2. 添加消息...")
    storage.add_user_message("你好,ClawOS!")
    storage.add_assistant_message("你好!我是ClawOS AI助手。", emotion="happy")
    storage.add_user_message("帮我打开浏览器")
    storage.add_assistant_message("好的,正在打开浏览器...", emotion="excited")
    
    # 获取消息
    print("\n3. 获取消息...")
    messages = storage.get_messages()
    for msg in messages:
        print(f"   [{msg.role}] {msg.content[:30]}...")
    
    # 统计
    print("\n4. 统计...")
    stats = storage.get_stats()
    print(f"   {stats}")
    
    # 导出
    print("\n5. 导出...")
    exported = storage.export_session(format="text")
    print(exported[:200])
    
    # 保存
    print("\n6. 保存...")
    storage.save()
    
    print("\n✅ 测试完成")
