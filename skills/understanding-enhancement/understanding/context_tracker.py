# 🦞 Context Tracker - 上下文记忆

"""
上下文记忆模块

功能:
- 追踪对话历史
- 记录话题状态
- 管理上下文窗口
"""

from typing import Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
import json


@dataclass
class ContextEntry:
    """上下文条目"""
    user_input: str
    system_response: str
    entities: Dict = field(default_factory=dict)
    topic: str = ""
    timestamp: float = field(default_factory=datetime.now().timestamp)


@dataclass
class DialogueState:
    """对话状态"""
    current_topic: Optional[str] = None
    pending_actions: List[str] = field(default_factory=list)
    user_preferences: Dict = field(default_factory=dict)
    entities: Dict = field(default_factory=dict)
    last_subject: Optional[str] = None


class ContextTracker:
    """上下文追踪器"""
    
    def __init__(self, window_size: int = 5):
        """
        Args:
            window_size: 上下文窗口大小（保留最近N轮对话）
        """
        self.window_size = window_size
        self.history: List[ContextEntry] = []
        self.state = DialogueState()
        self._current_entities = {}
    
    def update(
        self,
        user_input: str,
        system_response: str,
        entities: Dict = None,
        topic: str = None
    ):
        """更新上下文
        
        Args:
            user_input: 用户输入
            system_response: 系统回复
            entities: 识别的实体
            topic: 话题
        """
        # 创建新条目
        entry = ContextEntry(
            user_input=user_input,
            system_response=system_response,
            entities=entities or {},
            topic=topic or self._extract_topic(user_input)
        )
        
        # 添加到历史
        self.history.append(entry)
        
        # 截断窗口
        if len(self.history) > self.window_size:
            self.history = self.history[-self.window_size:]
        
        # 更新状态
        self._current_entities.update(entities or {})
        self.state.entities = self._current_entities
        
        if topic:
            self.state.current_topic = topic
        
        # 更新最后主语
        self._update_last_subject(user_input)
    
    def get_context(self) -> Dict:
        """获取完整上下文"""
        return {
            "history": [
                {
                    "user": entry.user_input,
                    "system": entry.system_response,
                    "topic": entry.topic,
                    "entities": entry.entities
                }
                for entry in self.history
            ],
            "state": {
                "current_topic": self.state.current_topic,
                "pending_actions": self.state.pending_actions,
                "preferences": self.state.user_preferences,
                "entities": self.state.entities,
                "last_subject": self.state.last_subject
            }
        }
    
    def get_last_input(self) -> str:
        """获取最后用户输入"""
        if self.history:
            return self.history[-1].user_input
        return ""
    
    def get_last_entities(self) -> Dict:
        """获取最后识别的实体"""
        if self.history:
            return self.history[-1].entities
        return {}
    
    def is_continuation(self, text: str) -> bool:
        """检查是否是之前话题的延续"""
        if not self.history:
            return False
        
        last_input = self.get_last_input()
        
        # 省略主语的检测
        ellipsis_patterns = [
            "再试一次", "继续", "改成", "改为",
            "再", "还", "然后"
        ]
        
        return any(pattern in text.lower() for pattern in ellipsis_patterns)
    
    def inherit_context(self, text: str) -> Dict:
        """继承上下文补全输入
        
        Returns:
            补全后的输入和上下文
        """
        if not self.is_continuation(text):
            return {"text": text, "context": self.get_context()}
        
        # 继承最后的话题和实体
        last_topic = self.state.current_topic
        last_entities = self.state.entities
        
        # 继承最后主语
        if self.state.last_subject:
            text = f"{self.state.last_subject}，{text}"
        
        return {
            "text": text,
            "context": {
                "inherited_topic": last_topic,
                "inherited_entities": last_entities,
                "original_context": self.get_context()
            }
        }
    
    def _extract_topic(self, text: str) -> str:
        """提取话题"""
        topic_keywords = {
            "颜色": ["颜色", "红色", "蓝色", "改成"],
            "大小": ["大小", "大小", "太大", "太小"],
            "速度": ["速度", "慢", "快"],
            "界面": ["界面", "按钮", "输入框"],
            "功能": ["功能", "添加", "删除", "修改"],
        }
        
        for topic, keywords in topic_keywords.items():
            if any(kw in text for kw in keywords):
                return topic
        
        return "general"
    
    def _update_last_subject(self, text: str):
        """更新最后主语"""
        subjects = ["我", "你", "系统", "按钮", "输入框", "界面"]
        for subject in subjects:
            if subject in text:
                self.state.last_subject = subject
                break
    
    def clear(self):
        """清空上下文"""
        self.history = []
        self.state = DialogueState()
        self._current_entities = {}
    
    def get_stats(self) -> Dict:
        """获取统计"""
        return {
            "history_length": len(self.history),
            "window_size": self.window_size,
            "current_topic": self.state.current_topic,
            "entities_count": len(self.state.entities)
        }


# 测试
if __name__ == "__main__":
    tracker = ContextTracker(window_size=3)
    
    # 模拟对话
    conversation = [
        ("把按钮颜色改成蓝色", "好的，已将按钮颜色改为蓝色"),
        ("太大了", None),  # 继续之前的话题
        ("再试一次", None),  # 继续操作
    ]
    
    for i, (user_input, system_response) in enumerate(conversation):
        if system_response:
            tracker.update(user_input, system_response)
        else:
            # 检查是否是延续
            if tracker.is_continuation(user_input):
                inherited = tracker.inherit_context(user_input)
                print(f"原文: {user_input}")
                print(f"补全: {inherited['text']}")
                print(f"上下文: {inherited['context']}")
                print()
