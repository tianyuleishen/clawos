# 🦞 飞书客户端

"""
飞书 (Feishu/Lark) IM集成

配置方法:
    config = {
        "platform": "feishu",
        "app_id": "your_app_id",
        "app_secret": "your_app_secret",
        "webhook_url": "your_webhook_url"  # 可选
    }
"""

import asyncio
import httpx
from typing import Dict, Any, Optional
from datetime import datetime

from .base import IMClient, IMConfig, IMPlatform


class FeishuClient(IMClient):
    """飞书客户端"""
    
    def __init__(self, config: IMConfig):
        super().__init__(config)
        self.platform = IMPlatform.FEISHU
        self.base_url = "https://open.feishu.cn/open-apis"
        self.client = httpx.AsyncClient(timeout=30.0)
        self._token_cache = {}
    
    async def _get_app_access_token(self) -> str:
        """获取app_access_token"""
        # 检查缓存
        if "app_access_token" in self._token_cache:
            cached = self._token_cache["app_access_token"]
            if cached["expires_at"] > datetime.now().timestamp():
                return cached["token"]
        
        # 获取新token
        url = f"{self.base_url}/auth/v3/app_access_token"
        data = {
            "app_id": self.config.app_id,
            "app_secret": self.config.app_secret
        }
        
        response = await self.client.post(url, json=data)
        result = response.json()
        
        if result.get("code") == 0:
            token = result["app_access_token"]
            self._token_cache["app_access_token"] = {
                "token": token,
                "expires_at": datetime.now().timestamp() + result.get("expire", 7200)
            }
            return token
        else:
            raise Exception(f"获取access_token失败: {result}")
    
    async def connect(self) -> bool:
        """连接飞书"""
        try:
            # 验证配置
            if not self.config.app_id or not self.config.app_secret:
                raise ValueError("缺少app_id或app_secret")
            
            # 获取token
            await self._get_app_access_token()
            self.connected = True
            print("✅ 飞书客户端已连接")
            return True
        except Exception as e:
            print(f"❌ 飞书连接失败: {e}")
            return False
    
    async def disconnect(self):
        """断开连接"""
        await self.client.aclose()
        self.connected = False
        print("✅ 飞书客户端已断开")
    
    async def send_message(
        self,
        receive_id: str,
        message: str,
        msg_type: str = "text"
    ) -> bool:
        """
        发送消息
        
        Args:
            receive_id: 接收者ID (open_id/user_id/chat_id)
            message: 消息内容
            msg_type: 消息类型 (text/post/image/card)
            
        Returns:
            bool: 是否发送成功
        """
        if not self.connected:
            await self.connect()
        
        try:
            access_token = await self._get_app_access_token()
            
            # 构建消息
            if msg_type == "text":
                content = {"text": message}
            elif msg_type == "post":
                content = {
                    "post": {
                        "zh_cn": {
                            "title": "ClawOS通知",
                            "content": [[{"tag": "text", "text": message}]]
                        }
                    }
                }
            else:
                content = {"text": message}
            
            url = f"{self.base_url}/im/v1/messages"
            params = {"receive_id_type": "open_id"}
            
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            
            data = {
                "receive_id": receive_id,
                "msg_type": msg_type if msg_type != "post" else "text",
                "content": str(content)
            }
            
            response = await self.client.post(url, params=params, json=data, headers=headers)
            result = response.json()
            
            if result.get("code") == 0:
                print(f"✅ 飞书消息已发送: {receive_id}")
                return True
            else:
                print(f"❌ 飞书消息发送失败: {result}")
                return False
                
        except Exception as e:
            print(f"❌ 飞书发送错误: {e}")
            return False
    
    async def send_group_message(self, chat_id: str, message: str) -> bool:
        """发送群消息"""
        return await self.send_message(chat_id, message, "text")
    
    async def get_messages(
        self,
        start_time: Optional[str] = None,
        limit: int = 10
    ) -> list:
        """
        获取消息列表
        
        Args:
            start_time: 开始时间 (ISO格式)
            limit: 数量限制
            
        Returns:
            list: 消息列表
        """
        if not self.connected:
            await self.connect()
        
        try:
            access_token = await self._get_app_access_token()
            
            url = f"{self.base_url}/im/v1/messages"
            params = {
                "container_id_type": "chat",
                "limit": limit
            }
            
            headers = {"Authorization": f"Bearer {access_token}"}
            
            response = await self.client.get(url, params=params, headers=headers)
            result = response.json()
            
            if result.get("code") == 0:
                return result.get("items", [])
            else:
                print(f"❌ 获取消息失败: {result}")
                return []
                
        except Exception as e:
            print(f"❌ 飞书获取消息错误: {e}")
            return []
    
    async def create_webhook(
        self,
        name: str,
        url: str,
        event_types: list = ["message"]
    ) -> Dict[str, Any]:
        """创建Webhook"""
        try:
            access_token = await self._get_app_access_token()
            
            url = f"{self.base_url}/webhook/v3"
            data = {
                "name": name,
                "url": url,
                "event_types": event_types
            }
            
            headers = {"Authorization": f"Bearer {access_token}"}
            
            response = await self.client.post(url, json=data, headers=headers)
            return response.json()
            
        except Exception as e:
            print(f"❌ 创建飞书Webhook失败: {e}")
            return {"code": -1, "msg": str(e)}


# 配置示例
FEISHU_CONFIG_SAMPLE = """
# 飞书配置 (config.json)
{
    "platform": "feishu",
    "app_id": "your_app_id",
    "app_secret": "your_app_secret"
}

# 获取凭证:
# 1. 登录 https://open.feishu.cn/
# 2. 创建企业应用
# 3. 获取app_id和app_secret
# 4. 配置应用权限 (im:message)
# 5. 发布应用
"""

print("✅ 飞书客户端已加载")
