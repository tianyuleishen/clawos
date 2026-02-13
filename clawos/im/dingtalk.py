# 🦞 钉钉客户端

"""
钉钉 (DingTalk) IM集成

配置方法:
    config = {
        "platform": "dingtalk",
        "app_key": "your_app_key",
        "app_secret": "your_app_secret",
        "agent_id": "your_agent_id"
    }
"""

import asyncio
import httpx
from typing import Dict, Any, Optional
from datetime import datetime

from .base import IMClient, IMConfig, IMPlatform


class DingTalkClient(IMClient):
    """钉钉客户端"""
    
    def __init__(self, config: IMConfig):
        super().__init__(config)
        self.platform = IMPlatform.DINGTALK
        self.base_url = "https://api.dingtalk.com"
        self.client = httpx.AsyncClient(timeout=30.0)
        self._token_cache = {}
    
    async def _get_access_token(self) -> str:
        """获取access_token"""
        if "access_token" in self._token_cache:
            cached = self._token_cache["access_token"]
            if cached["expires_at"] > datetime.now().timestamp():
                return cached["token"]
        
        url = f"{self.base_url}/v1.0/oauth2/access_token"
        data = {
            "appKey": self.config.app_key or self.config.app_id,
            "appSecret": self.config.app_secret
        }
        
        response = await self.client.post(url, json=data)
        result = response.json()
        
        if "accessToken" in result:
            token = result["accessToken"]
            self._token_cache["access_token"] = {
                "token": token,
                "expires_at": datetime.now().timestamp() + result.get("expireIn", 7200)
            }
            return token
        else:
            raise Exception(f"获取access_token失败: {result}")
    
    async def connect(self) -> bool:
        """连接钉钉"""
        try:
            if not (self.config.app_key or self.config.app_id) or not self.config.app_secret:
                raise ValueError("缺少app_key或app_secret")
            
            await self._get_access_token()
            self.connected = True
            print("✅ 钉钉客户端已连接")
            return True
        except Exception as e:
            print(f"❌ 钉钉连接失败: {e}")
            return False
    
    async def disconnect(self):
        """断开连接"""
        await self.client.aclose()
        self.connected = False
        print("✅ 钉钉客户端已断开")
    
    async def send_message(
        self,
        user_id: str,
        message: str,
        msg_type: str = "text"
    ) -> bool:
        """
        发送消息
        
        Args:
            user_id: 用户ID (userid)
            message: 消息内容
            msg_type: 消息类型
            
        Returns:
            bool: 是否发送成功
        """
        if not self.connected:
            await self.connect()
        
        try:
            access_token = await self._get_access_token()
            
            # 构建消息
            if msg_type == "text":
                content = {"text": {"content": message}}
            else:
                content = {"text": {"content": message}}
            
            url = f"{self.base_url}/v1.0/im/messages/to_userids"
            headers = {"x-acs-dingtalk-access-token": access_token}
            
            data = {
                "userid": user_id,
                "msghead": {"header": {"msgtype": msg_type}},
                "msgbody": content
            }
            
            response = await self.client.post(url, headers=headers, json=data)
            result = response.json()
            
            if result.get("errcode") == 0:
                print(f"✅ 钉钉消息已发送: {user_id}")
                return True
            else:
                print(f"❌ 钉钉消息发送失败: {result}")
                return False
                
        except Exception as e:
            print(f"❌ 钉钉发送错误: {e}")
            return False
    
    async def send_group_message(self, chat_id: str, message: str) -> bool:
        """发送群消息"""
        try:
            access_token = await self._get_access_token()
            
            url = f"{self.base_url}/v1.0/im/messages/to_conversation"
            headers = {"x-acs-dingtalk-access-token": access_token}
            
            data = {
                "conversationId": chat_id,
                "msgtype": "text",
                "text": {"content": message}
            }
            
            response = await self.client.post(url, headers=headers, json=data)
            result = response.json()
            
            if result.get("errcode") == 0:
                print(f"✅ 钉钉群消息已发送: {chat_id}")
                return True
            else:
                print(f"❌ 钉钉群消息发送失败: {result}")
                return False
                
        except Exception as e:
            print(f"❌ 钉钉群发送错误: {e}")
            return False
    
    async def get_messages(self, limit: int = 10) -> list:
        """获取消息"""
        print("⚠️ 钉钉暂不支持主动获取消息")
        return []


# 配置示例
DINGTALK_CONFIG_SAMPLE = """
# 钉钉配置 (config.json)
{
    "platform": "dingtalk",
    "app_key": "your_app_key",
    "app_secret": "your_app_secret"
}

# 获取凭证:
# 1. 登录 https://open.dingtalk.com/
# 2. 创建应用
# 3. 获取appKey, appSecret
# 4. 配置应用权限 (im:message)
# 5. 发布应用
"""

print("✅ 钉钉客户端已加载")
