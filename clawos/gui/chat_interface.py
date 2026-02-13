# 🦞 Conversation Interface - 对话界面

"""
对话界面 - ClawOS聊天界面

功能:
- 对话历史
- 富文本显示
- 情感状态
- 消息输入
"""

import asyncio
from typing import Callable, List, Optional, Dict, Any
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
import json

class MessageType(Enum):
    """消息类型"""
    TEXT = "text"
    CODE = "code"
    IMAGE = "image"
    SYSTEM = "system"
    ERROR = "error"

@dataclass
class ChatMessage:
    """聊天消息"""
    id: str
    type: MessageType
    content: str
    role: str  # "user" or "assistant"
    timestamp: float
    emotion: str = None
    confidence: float = None
    metadata: Dict = None


class ConversationInterface:
    """对话界面"""
    
    def __init__(self, language: str = "zh"):
        self.language = language
        self.messages: List[ChatMessage] = []
        self.callbacks: Dict[str, Callable] = {}
        
        # 情感颜色映射
        self.emotion_colors = {
            "happy": "#4CAF50",
            "sad": "#2196F3",
            "angry": "#F44336",
            "fear": "#9C27B0",
            "surprised": "#FF9800",
            "neutral": "#9E9E9E",
            "excited": "#E91E63",
            "calm": "#00BCD4"
        }
        
        print(f"✅ Conversation Interface 已加载 ({language})")
    
    # ============ 消息管理 ============
    
    def add_message(
        self,
        content: str,
        role: str,
        msg_type: MessageType = MessageType.TEXT,
        emotion: str = None,
        confidence: float = None,
        metadata: Dict = None
    ) -> ChatMessage:
        """添加消息"""
        msg = ChatMessage(
            id=str(len(self.messages)),
            type=msg_type,
            content=content,
            role=role,
            timestamp=datetime.now().timestamp(),
            emotion=emotion,
            confidence=confidence,
            metadata=metadata or {}
        )
        
        self.messages.append(msg)
        
        # 回调
        if "new_message" in self.callbacks:
            self.callbacks["new_message"](msg)
        
        return msg
    
    def add_user_message(self, content: str) -> ChatMessage:
        """添加用户消息"""
        return self.add_message(content, "user", MessageType.TEXT)
    
    def add_assistant_message(
        self, 
        content: str, 
        emotion: str = None,
        confidence: float = None
    ) -> ChatMessage:
        """添加助手消息"""
        return self.add_message(
            content, 
            "assistant", 
            MessageType.TEXT,
            emotion=emotion,
            confidence=confidence
        )
    
    def add_system_message(self, content: str) -> ChatMessage:
        """添加系统消息"""
        return self.add_message(content, "system", MessageType.SYSTEM)
    
    def add_error_message(self, content: str) -> ChatMessage:
        """添加错误消息"""
        return self.add_message(content, "assistant", MessageType.ERROR)
    
    def add_code_message(
        self, 
        code: str, 
        language: str = "python"
    ) -> ChatMessage:
        """添加代码消息"""
        return self.add_message(
            code, 
            "assistant", 
            MessageType.CODE,
            metadata={"language": language}
        )
    
    def get_history(self) -> List[ChatMessage]:
        """获取历史"""
        return self.messages.copy()
    
    def clear_history(self):
        """清空历史"""
        self.messages.clear()
        if "clear" in self.callbacks:
            self.callbacks["clear"]()
    
    def delete_message(self, message_id: str) -> bool:
        """删除消息"""
        for i, msg in enumerate(self.messages):
            if msg.id == message_id:
                self.messages.pop(i)
                return True
        return False
    
    # ============ 回调 ============
    
    def on_new_message(self, callback: Callable[[ChatMessage], None]):
        """新消息回调"""
        self.callbacks["new_message"] = callback
    
    def on_clear(self, callback: Callable[[], None]):
        """清空回调"""
        self.callbacks["clear"] = callback
    
    def on_send(self, callback: Callable[[str], None]):
        """发送回调"""
        self.callbacks["send"] = callback
    
    # ============ 格式化 ============
    
    def format_message(self, msg: ChatMessage) -> str:
        """格式化消息"""
        timestamp = datetime.fromtimestamp(msg.timestamp).strftime("%H:%M")
        role_name = "你" if msg.role == "user" else "🦞"
        
        lines = []
        
        if msg.type == MessageType.CODE:
            lines.append(f"```{msg.metadata.get('language', 'text')}```")
            lines.append(f"{msg.content}")
            lines.append("```")
        
        elif msg.type == MessageType.SYSTEM:
            lines.append(f"[系统] {msg.content}")
        
        elif msg.type == MessageType.ERROR:
            lines.append(f"[错误] {msg.content}")
        
        else:
            if msg.emotion:
                color = self.emotion_colors.get(msg.emotion, "#9E9E9E")
                lines.append(f"[情感: {msg.emotion}]")
            
            lines.append(f"{role_name} ({timestamp}): {msg.content}")
        
        return "\n".join(lines)
    
    def format_for_display(self, msg: ChatMessage) -> Dict[str, Any]:
        """格式化用于显示"""
        return {
            "id": msg.id,
            "role": msg.role,
            "content": msg.content,
            "type": msg.type.value,
            "emotion": msg.emotion,
            "timestamp": datetime.fromtimestamp(msg.timestamp).isoformat(),
            "metadata": msg.metadata
        }
    
    def export_history(self, format: str = "json") -> str:
        """导出历史"""
        data = [
            {
                "id": msg.id,
                "role": msg.role,
                "content": msg.content,
                "type": msg.type.value,
                "timestamp": msg.timestamp,
                "emotion": msg.emotion,
                "metadata": msg.metadata
            }
            for msg in self.messages
        ]
        
        if format == "json":
            return json.dumps(data, ensure_ascii=False, indent=2)
        elif format == "text":
            return "\n".join([
                f"[{datetime.fromtimestamp(m.timestamp).strftime('%Y-%m-%d %H:%M:%S')}][{m.role}] {m.content}"
                for m in self.messages
            ])
        
        return json.dumps(data)
    
    def import_history(self, data: str, format: str = "json"):
        """导入历史"""
        if format == "json":
            items = json.loads(data)
        else:
            return
        
        self.messages.clear()
        
        for item in items:
            self.add_message(
                content=item["content"],
                role=item["role"],
                msg_type=MessageType(item.get("type", "text")),
                emotion=item.get("emotion"),
                metadata=item.get("metadata")
            )
    
    # ============ 统计 ============
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计"""
        user_count = sum(1 for m in self.messages if m.role == "user")
        assistant_count = sum(1 for m in self.messages if m.role == "assistant")
        
        total_chars = sum(len(m.content) for m in self.messages)
        
        emotion_counts = {}
        for msg in self.messages:
            if msg.emotion:
                emotion_counts[msg.emotion] = emotion_counts.get(msg.emotion, 0) + 1
        
        return {
            "total_messages": len(self.messages),
            "user_messages": user_count,
            "assistant_messages": assistant_count,
            "total_characters": total_chars,
            "emotion_distribution": emotion_counts
        }


class ChatPanel:
    """聊天面板"""
    
    def __init__(self, parent=None):
        self.parent = parent
        self.interface = ConversationInterface()
        self.input_enabled = True
        
        print("✅ Chat Panel 已初始化")
    
    def render(self) -> str:
        """渲染面板HTML"""
        messages_html = []
        
        for msg in self.interface.messages:
            if msg.type == MessageType.SYSTEM:
                role_class = "system"
                role_icon = "⚙️"
            elif msg.type == MessageType.ERROR:
                role_class = "error"
                role_icon = "❌"
            elif msg.type == MessageType.CODE:
                role_class = "code"
                role_icon = "📝"
            else:
                role_class = msg.role
                role_icon = "👤" if msg.role == "user" else "🦞"
            
            emotion_badge = ""
            if msg.emotion:
                color = self.interface.emotion_colors.get(msg.emotion, "#9E9E9E")
                emotion_badge = f'<span class="emotion-badge" style="background:{color}">{msg.emotion}</span>'
            
            messages_html.append(f"""
<div class="message {role_class}">
    <div class="message-header">
        <span class="role-icon">{role_icon}</span>
        <span class="timestamp">{datetime.fromtimestamp(msg.timestamp).strftime('%H:%M')}</span>
        {emotion_badge}
    </div>
    <div class="message-content">
{self._escape_html(msg.content)}
    </div>
</div>
            """)
        
        return f"""
<div class="chat-panel">
    <div class="messages-container">
        {''.join(messages_html)}
    </div>
    <div class="input-container">
        <textarea id="chat-input" placeholder="输入消息..."></textarea>
        <button id="send-btn">发送</button>
    </div>
</div>
        """
    
    def _escape_html(self, text: str) -> str:
        """HTML转义"""
        return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br>")
    
    def get_html_template(self) -> str:
        """获取HTML模板"""
        return """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>ClawOS Chat</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Microsoft YaHei', sans-serif;
            background: #1e1e1e;
            color: #ffffff;
            height: 100vh;
            display: flex;
            flex-direction: column;
        }
        
        .chat-panel {
            display: flex;
            flex-direction: column;
            height: 100%;
            max-width: 1200px;
            margin: 0 auto;
            width: 100%;
        }
        
        .messages-container {
            flex: 1;
            overflow-y: auto;
            padding: 20px;
            display: flex;
            flex-direction: column;
            gap: 15px;
        }
        
        .message {
            max-width: 80%;
            border-radius: 15px;
            padding: 15px;
            animation: fadeIn 0.3s ease;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .message.user {
            align-self: flex-end;
            background: #4CAF50;
        }
        
        .message.assistant {
            align-self: flex-start;
            background: #2196F3;
        }
        
        .message.system {
            align-self: center;
            background: #FF9800;
            font-size: 0.9em;
        }
        
        .message.error {
            align-self: center;
            background: #F44336;
        }
        
        .message.code {
            align-self: stretch;
            background: #2d2d2d;
            font-family: 'Consolas', monospace;
        }
        
        .message-header {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 8px;
            font-size: 0.85em;
            opacity: 0.8;
        }
        
        .emotion-badge {
            padding: 2px 8px;
            border-radius: 10px;
            font-size: 0.8em;
        }
        
        .message-content {
            line-height: 1.6;
            white-space: pre-wrap;
        }
        
        .input-container {
            padding: 20px;
            background: #2d2d2d;
            display: flex;
            gap: 15px;
        }
        
        #chat-input {
            flex: 1;
            background: #1e1e1e;
            border: 1px solid #444;
            border-radius: 10px;
            padding: 15px;
            color: #fff;
            font-family: inherit;
            font-size: 16px;
            resize: none;
            min-height: 60px;
        }
        
        #chat-input:focus {
            outline: none;
            border-color: #2196F3;
        }
        
        #send-btn {
            padding: 15px 30px;
            background: #2196F3;
            border: none;
            border-radius: 10px;
            color: #fff;
            font-size: 16px;
            cursor: pointer;
            transition: background 0.3s;
        }
        
        #send-btn:hover {
            background: #1976D2;
        }
        
        #send-btn:active {
            transform: scale(0.98);
        }
    </style>
</head>
<body>
    <div class="chat-panel">
        <div class="messages-container" id="messages">
            <!-- Messages will be inserted here -->
        </div>
        <div class="input-container">
            <textarea id="chat-input" placeholder="输入消息... (支持Ctrl+Enter发送)"></textarea>
            <button id="send-btn">发送</button>
        </div>
    </div>
    <script>
        // JavaScript will be inserted here
    </script>
</body>
</html>
        """


# 便捷函数
def create_chat_panel() -> ChatPanel:
    """创建聊天面板"""
    return ChatPanel()


# 测试代码
if __name__ == "__main__":
    print("💬 Conversation Interface 测试")
    
    chat = ConversationInterface()
    
    # 添加消息
    chat.add_user_message("你好,ClawOS!")
    chat.add_assistant_message("你好!我是ClawOS AI助手。", emotion="happy")
    chat.add_user_message("帮我打开浏览器")
    chat.add_assistant_message("好的,正在打开浏览器...", emotion="excited")
    
    # 打印历史
    print("\n📋 对话历史:")
    for msg in chat.messages:
        print(f"  [{msg.role}] {msg.content[:50]}...")
    
    # 统计
    stats = chat.get_stats()
    print(f"\n📊 统计: {stats}")
    
    print("\n✅ 测试完成")
