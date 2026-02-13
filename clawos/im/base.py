# 🦞 IM基础模块

"""
即时通讯基础类和配置
"""

from enum import Enum
from dataclasses import dataclass
from typing import Optional, Dict, Any


class IMPlatform(Enum):
    """IM平台枚举"""
    FEISHU = "feishu"       # 飞书
    WECOM = "wecom"          # 企业微信
    DINGTALK = "dingtalk"   # 钉钉
    QQ = "qq"               # QQ


@dataclass
class IMConfig:
    """IM配置"""
    platform: IMPlatform
    # 通用配置
    webhook_url: str = ""           # Webhook地址
    access_token: str = ""           # Access Token
    # 飞书/企业微信配置
    app_id: str = ""                # App ID
    app_secret: str = ""            # App Secret
    # 钉钉配置
    agent_id: str = ""              # Agent ID
    # QQ配置
    bot_token: str = ""             # Bot Token
    app_key: str = ""              # App Key
    # 消息接收配置
    receive_mode: str = "webhook"   # webhook: Webhook回调, api: API轮询
    api_interval: int = 3          # API轮询间隔(秒)

    @classmethod
    def from_dict(cls, config: Dict[str, Any]) -> 'IMConfig':
        """从字典创建配置"""
        return cls(
            platform=IMPlatform(config.get("platform", "feishu")),
            webhook_url=config.get("webhook_url", ""),
            access_token=config.get("access_token", ""),
            app_id=config.get("app_id", ""),
            app_secret=config.get("app_secret", ""),
            agent_id=config.get("agent_id", ""),
            bot_token=config.get("bot_token", ""),
            app_key=config.get("app_key", ""),
            receive_mode=config.get("receive_mode", "webhook"),
            api_interval=config.get("api_interval", 3)
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "platform": self.platform.value,
            "webhook_url": self.webhook_url,
            "access_token": self.access_token,
            "app_id": self.app_id,
            "app_secret": self.app_secret,
            "agent_id": self.agent_id,
            "bot_token": self.bot_token,
            "app_key": self.app_key,
            "receive_mode": self.receive_mode,
            "api_interval": self.api_interval
        }


class IMClient:
    """IM客户端基类"""
    
    def __init__(self, config: IMConfig):
        self.config = config
        self.platform = config.platform
        self.connected = False
    
    async def connect(self) -> bool:
        """连接IM平台"""
        raise NotImplementedError
    
    async def disconnect(self):
        """断开连接"""
        self.connected = False
    
    async def send_message(self, target: str, message: str, **kwargs) -> bool:
        """
        发送消息
        
        Args:
            target: 目标ID (群ID/用户ID/频道ID)
            message: 消息内容
            **kwargs: 附加参数
            
        Returns:
            bool: 是否发送成功
        """
        raise NotImplementedError
    
    async def get_messages(self, limit: int = 10) -> list 获取消息
        
       :
        """
        Args:
            limit: 获取数量限制
            
        Returns:
            list: 消息列表
        """
        raise NotImplementedError
    
    @classmethod
    def create_client(cls, config: Dict[str, Any]) -> 'IMClient':
        """创建IM客户端"""
        im_config = IMConfig.from_dict(config)
        
        if im_config.platform == IMPlatform.FEISHU:
            from .feishu import FeishuClient
            return FeishuClient(im_config)
        elif im_config.platform == IMPlatform.WECOM:
            from .wecom import WeComClient
            return WeComClient(im_config)
        elif im_config.platform == IMPlatform.DINGTALK:
            from .dingtalk import DingTalkClient
            return DingTalkClient(im_config)
        elif im_config.platform == IMPlatform.QQ:
            from .qq import QQClient
            return QQClient(im_config)
        else:
            raise ValueError(f"不支持的平台: {im_config.platform}")


# 消息模板
IM_MESSAGE_TEMPLATES = {
    "text": "◆ {message}",
    "code": "```\n{message}\n```",
    "rich": "📎 {title}\n\n{message}",
    "system": "🔔 系统通知\n\n{message}",
}

print("✅ IM基础模块已加载")
