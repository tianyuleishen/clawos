# 🦞 QQ客户端

"""
QQ IM集成 (通过go-cqhttp或其他HTTP API)

配置方法:
    config = {
        "platform": "qq",
        "http_url": "http://localhost:5700",  # CQHTTP API地址
        "access_token": "your_access_token"     # 可选
    }
"""

import asyncio
import httpx
from typing import Dict, Any, Optional

from .base import IMClient, IMConfig, IMPlatform


class QQClient(IMClient):
    """QQ客户端 (基于CQHTTP API)"""
    
    def __init__(self, config: IMConfig):
        super().__init__(config)
        self.platform = IMPlatform.QQ
        self.base_url = config.webhook_url or "http://localhost:5700"
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def connect(self) -> bool:
        """连接QQ"""
        try:
            # 测试API连通性
            response = await self.client.get(f"{self.base_url}/get_version_info")
            if response.status_code == 200:
                self.connected = True
                print("✅ QQ客户端已连接")
                return True
            else:
                raise Exception("API响应异常")
        except Exception as e:
            print(f"❌ QQ连接失败: {e}")
            print("提示: 请确保go-cqhttp或其他CQHTTP服务已启动")
            return False
    
    async def disconnect(self):
        """断开连接"""
        await self.client.aclose()
        self.connected = False
        print("✅ QQ客户端已断开")
    
    async def send_message(
        self,
        user_id: str,
        message: str,
        msg_type: str = "private"
    ) -> bool:
        """
        发送消息
        
        Args:
            user_id: 目标ID (QQ号/群号)
            message: 消息内容
            msg_type: 消息类型 (private/group)
            
        Returns:
            bool: 是否发送成功
        """
        if not self.connected:
            await self.connect()
        
        try:
            if msg_type == "private":
                url = f"{self.base_url}/send_private_msg"
                data = {"user_id": int(user_id), "message": message}
            else:
                url = f"{self.base_url}/send_group_msg"
                data = {"group_id": int(user_id), "message": message}
            
            response = await self.client.post(url, json=data)
            result = response.json()
            
            if result.get("status") == "ok":
                print(f"✅ QQ消息已发送: {user_id} ({msg_type})")
                return True
            else:
                print(f"❌ QQ消息发送失败: {result}")
                return False
                
        except Exception as e:
            print(f"❌ QQ发送错误: {e}")
            return False
    
    async def send_group_message(self, group_id: str, message: str) -> bool:
        """发送群消息"""
        return await self.send_message(group_id, message, "group")
    
    async def get_messages(self, limit: int = 10) -> list:
        """获取消息(需要启用HTTP API)"""
        print("⚠️ QQ获取消息需要配置CQHTTP")
        return []
    
    async def get_friend_list(self) -> list:
        """获取好友列表"""
        try:
            response = await self.client.get(f"{self.base_url}/get_friend_list")
            result = response.json()
            return result.get("data", [])
        except Exception as e:
            print(f"❌ 获取好友列表失败: {e}")
            return []
    
    async def get_group_list(self) -> list:
        """获取群列表"""
        try:
            response = await self.client.get(f"{self.base_url}/get_group_list")
            result = response.json()
            return result.get("data", [])
        except Exception as e:
            print(f"❌ 获取群列表失败: {e}")
            return []


# 配置示例
QQ_CONFIG_SAMPLE = """
# QQ配置 (config.json)
{
    "platform": "qq",
    "http_url": "http://localhost:5700",
    "access_token": "your_access_token"
}

# 配置说明:
# 1. 下载go-cqhttp: https://github.com/Mrs4s/go-cqhttp
# 2. 配置config.yml:
#    - account: qq号
#    - servers: HTTP监听5700端口
# 3. 启动go-cqhttp
# 4. 配置ClawOS连接
"""

print("✅ QQ客户端已加载")
