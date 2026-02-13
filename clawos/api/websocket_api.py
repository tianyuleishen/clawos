# 🦞 WebSocket API - 实时通信

"""
WebSocket API - ClawOS实时通信

功能:
- 实时消息
- 事件推送
- 心跳机制
- 连接管理
"""

import asyncio
import json
from typing import Dict, List, Any, Callable, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
import secrets
import logging

from .rest_api import HTTPMethod


class MessageType(Enum):
    """消息类型"""
    CHAT = "chat"
    EVENT = "event"
    SUBSCRIBE = "subscribe"
    UNSUBSCRIBE = "unsubscribe"
    PING = "ping"
    RESPONSE = "response"
    MESSAGE = "message"
    BROADCAST = "broadcast"
    ERROR = "error"
    PONG = "pong"


@dataclass
class WSMessage:
    """WebSocket消息"""
    type: str
    payload: Dict
    message_id: str = None
    timestamp: float = None
    channel: str = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().timestamp()
        if self.message_id is None:
            self.message_id = secrets.token_hex(8)


@dataclass
class Channel:
    """消息频道"""
    name: str
    description: str
    subscribers: set = field(default_factory=set)
    history: List[WSMessage] = field(default_factory=list)
    max_history: int = 100


class WebSocketAPI:
    """WebSocket API"""
    
    def __init__(self, host: str = "0.0.0.0", port: int = 8081):
        self.host = host
        self.port = port
        self.connections: Dict[str, set] = {}
        self.channels: Dict[str, Channel] = {}
        self.handlers: Dict[str, Callable] = {}
        self.running = False
        
        self.logger = logging.getLogger("websocket_api")
        
        # 默认频道
        self._init_default_channels()
        
        print(f"✅ WebSocket API 已初始化 ({host}:{port})")
    
    def _init_default_channels(self):
        """初始化默认频道"""
        default_channels = {
            'chat': {'description': '对话消息', 'max_history': 200},
            'events': {'description': '系统事件', 'max_history': 100},
            'notifications': {'description': '通知', 'max_history': 50},
            'memory': {'description': '记忆更新', 'max_history': 100},
            'status': {'description': '状态变更', 'max_history': 50}
        }
        
        for name, config in default_channels.items():
            self.channels[name] = Channel(
                name=name,
                description=config['description'],
                max_history=config['max_history']
            )
    
    def register_handler(self, message_type: str, handler: Callable):
        """注册消息处理器"""
        self.handlers[message_type] = handler
    
    async def handle_message(
        self,
        message: WSMessage,
        connection_id: str
    ) -> Optional[WSMessage]:
        """处理消息"""
        handler = self.handlers.get(message.type)
        
        if handler:
            try:
                if asyncio.iscoroutinefunction(handler):
                    result = await handler(message.payload, connection_id)
                else:
                    result = handler(message.payload, connection_id)
                
                return WSMessage(
                    type=MessageType.RESPONSE.value,
                    payload={
                        'original_type': message.type,
                        'result': result,
                        'message_id': message.message_id
                    }
                )
            except Exception as e:
                self.logger.error(f"处理消息失败: {e}")
                return WSMessage(
                    type=MessageType.ERROR.value,
                    payload={'error': str(e), 'message_id': message.message_id}
                )
        return None
    
    def subscribe(self, connection_id: str, channel_name: str) -> bool:
        """订阅频道"""
        if channel_name not in self.channels:
            return False
        
        self.channels[channel_name].subscribers.add(connection_id)
        
        if connection_id not in self.connections:
            self.connections[connection_id] = set()
        self.connections[connection_id].add(channel_name)
        
        return True
    
    def unsubscribe(self, connection_id: str, channel_name: str) -> bool:
        """取消订阅"""
        if channel_name in self.channels:
            self.channels[channel_name].subscribers.discard(connection_id)
            
            if connection_id in self.connections:
                self.connections[connection_id].discard(channel_name)
            
            return True
        return False
    
    def get_channel_history(self, channel_name: str, limit: int = 50) -> List[Dict]:
        """获取频道历史"""
        if channel_name not in self.channels:
            return []
        
        channel = self.channels[channel_name]
        messages = channel.history[-limit:]
        
        return [
            {
                'type': msg.type,
                'payload': msg.payload,
                'timestamp': msg.timestamp
            }
            for msg in messages
        ]
    
    async def broadcast(self, channel_name: str, message: WSMessage, exclude: List[str] = None):
        """广播消息"""
        if channel_name not in self.channels:
            return
        
        channel = self.channels[channel_name]
        channel.history.append(message)
        if len(channel.history) > channel.max_history:
            channel.history = channel.history[-channel.max_history:]
    
    async def close_connection(self, connection_id: str):
        """关闭连接"""
        if connection_id in self.connections:
            for channel_name in self.connections[connection_id]:
                self.unsubscribe(connection_id, channel_name)
            del self.connections[connection_id]
    
    def get_stats(self) -> Dict:
        """获取统计"""
        total_subscribers = sum(
            len(channel.subscribers)
            for channel in self.channels.values()
        )
        
        return {
            'connections': len(self.connections),
            'channels': len(self.channels),
            'total_subscribers': total_subscribers,
            'channel_stats': {
                name: {
                    'subscribers': len(channel.subscribers),
                    'history': len(channel.history)
                }
                for name, channel in self.channels.items()
            }
        }


def create_websocket_api(host: str = "0.0.0.0", port: int = 8081) -> WebSocketAPI:
    """创建WebSocket API"""
    return WebSocketAPI(host, port)


if __name__ == "__main__":
    print("🔌 WebSocket API 测试")
    
    ws = WebSocket_API("localhost", 8081)
    
    print(f"频道数: {len(ws.channels)}")
    
    ws.subscribe("test_conn", "chat")
    print(f"chat订阅者: {len(ws.channels['chat'].subscribers)}")
    
    stats = ws.get_stats()
    print(f"统计: {stats}")
    
    print("\n✅ 测试完成")
