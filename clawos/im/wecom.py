# 🦞 企业微信客户端

"""
企业微信 (WeCom) IM集成

配置方法:
    config = {
        "platform": "wecom",
        "corp_id": "your_corp_id",
        "app_secret": "your_app_secret",
        "agent_id": "your_agent_id"
    }
"""

import asyncio
import httpx
from typing import Dict, Any, Optional
from datetime import datetime

from .base import IMClient, IMConfig, IMPlatform


class WeComClient(IMClient):
    """企业微信客户端"""
    
    def __init__(self, config: IMConfig):
        super().__init__(config)
        self.platform = IMPlatform.WECOM
        self.base_url = "https://qyapi.weixin.qq.com"
        self.client = httpx.AsyncClient(timeout=30.0)
        self._token_cache = {}
    
    async def _get_access_token(self) -> str:
        """获取access_token"""
        if "access_token" in self._token_cache:
            cached = self._token_cache["access_token"]
            if cached["expires_at"] > datetime.now().timestamp():
                return cached["token"]
        
        url = f"{self.base_url}/cgi-bin/gettoken"
        params = {
            "corpid": self.config.app_id,
            "corpsecret": self.config.app_secret
        }
        
        response = await self.client.get(url, params=params)
        result = response.json()
        
        if result.get("errcode") == 0:
            token = result["access_token"]
            self._token_cache["access_token"] = {
                "token": token,
                "expires_at": datetime.now().timestamp() + 7200
            }
            return token
        else:
            raise Exception(f"获取access_token失败: {result}")
    
    async def connect(self) -> bool:
        """连接企业微信"""
        try:
            if not self.config.app_id or not self.config.app_secret:
                raise ValueError("缺少corp_id或app_secret")
            
            await self._get_access_token()
            self.connected = True
            print("✅ 企业微信客户端已连接")
            return True
        except Exception as e:
            print(f"❌ 企业微信连接失败: {e}")
            return False
    
    async def disconnect(self):
        """断开连接"""
        await self.client.aclose()
        self.connected = False
        print("✅ 企业微信客户端已断开")
    
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
                content = {"content": message}
            else:
                content = {"content": message}
            
            url = f"{self.base_url}/cgi-bin/message/send"
            params = {"access_token": access_token}
            
            data = {
                "touser": user_id,
                "agentid": self.config.agent_id,
                "msgtype": msg_type,
                msg_type: content
            }
            
            response = await self.client.post(url, params=params, json=data)
            result = response.json()
            
            if result.get("errcode") == 0:
                print(f"✅ 企业微信消息已发送: {user_id}")
                return True
            else:
                print(f"❌ 企业微信消息发送失败: {result}")
                return False
                
        except Exception as e:
            print(f"❌ 企业微信发送错误: {e}")
            return False
    
    async def send_group_message(self, chat_id: str, message: str) -> bool:
        """发送群消息(群机器人)"""
        try:
            url = f"{self.base_url}/cgi-bin/webhook/send"
            data = {
                "chatid": chat_id,
                "msgtype": "text",
                "text": {"content": message}
            }
            
            response = await self.client.post(url, json=data)
            result = response.json()
            
            if result.get("errcode") == 0:
                print(f"✅ 企业微信群消息已发送: {chat_id}")
                return True
            else:
                print(f"❌ 企业微信群消息发送失败: {result}")
                return False
                
        except Exception as e:
            print(f"❌ 企业微信群发送错误: {e}")
            return False
    
    async def get_messages(self, limit: int = 10) -> list:
        """获取消息(需配置API权限)"""
        # 企业微信获取消息需要特定权限
        print("⚠️ 企业微信暂不支持主动获取消息")
        return []


# 配置示例
WECOM_CONFIG_SAMPLE = """
# 企业微信配置 (config.json)
{
    "platform": "wecom",
    "app_id": "your_corp_id",
    "app_secret": "your_app_secret",
    "agent_id": "your_agent_id"
}

# 获取凭证:
# 1. 登录 https://work.weixin.qq.com/
# 2. 创建应用
# 3. 获取corp_id, agent_id, app_secret
# 4. 配置应用权限
"""

print("✅ 企业微信客户端已加载")
