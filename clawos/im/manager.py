# 🦞 IM管理器

"""
IM平台统一管理器

功能:
- 统一配置管理
- 多平台支持
- 消息路由
"""

import asyncio
import json
import os
from typing import Dict, Any, List, Optional
from pathlib import Path

from .base import IMClient, IMPlatform, IMConfig


class IMManager:
    """IM管理器"""
    
    def __init__(self, config_dir: str = "~/.clawos/im"):
        self.config_dir = Path(config_dir).expanduser()
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.clients: Dict[str, IMClient] = {}
    
    def load_config(self, platform: str) -> Optional[Dict[str, Any]]:
        """加载配置文件"""
        config_file = self.config_dir / f"{platform}.json"
        if config_file.exists():
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None
    
    def save_config(self, platform: str, config: Dict[str, Any]) -> bool:
        """保存配置"""
        config_file = self.config_dir / f"{platform}.json"
        try:
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            print(f"✅ {platform}配置已保存: {config_file}")
            return True
        except Exception as e:
            print(f"❌ 配置保存失败: {e}")
            return False
    
    def configure(
        self,
        platform: str,
        credentials: Dict[str, Any],
        save: bool = True
    ) -> bool:
        """
        配置IM平台凭证
        
        Args:
            platform: 平台名称 (feishu/wecom/dingtalk/qq)
            credentials: 凭证信息
            save: 是否保存到文件
            
        Returns:
            bool: 是否成功
        """
        # 添加平台标识
        credentials["platform"] = platform
        
        # 验证必要字段
        if platform == "feishu":
            if not credentials.get("app_id") or not credentials.get("app_secret"):
                print("❌ 飞书需要app_id和app_secret")
                return False
                
        elif platform == "wecom":
            if not credentials.get("app_id") or not credentials.get("app_secret"):
                print("❌ 企业微信需要corp_id和app_secret")
                return False
                
        elif platform == "dingtalk":
            if not credentials.get("app_key") and not credentials.get("app_id"):
                print("❌ 钉钉需要app_key或app_id")
                return False
                
        elif platform == "qq":
            if not credentials.get("http_url"):
                print("❌ QQ需要http_url (CQHTTP API地址)")
                return False
        
        # 保存配置
        if save:
            self.save_config(platform, credentials)
        
        return True
    
    async def connect(self, platform: str) -> bool:
        """
        连接IM平台
        
        Args:
            platform: 平台名称
            
        Returns:
            bool: 是否成功
        """
        config = self.load_config(platform)
        if not config:
            print(f"❌ {platform}未配置，请先运行配置命令")
            return False
        
        try:
            client = IMClient.create_client(config)
            success = await client.connect()
            if success:
                self.clients[platform] = client
            return success
        except Exception as e:
            print(f"❌ {platform}连接失败: {e}")
            return False
    
    async def disconnect(self, platform: str):
        """断开连接"""
        if platform in self.clients:
            await self.clients[platform].disconnect()
            del self.clients[platform]
    
    async def send_message(
        self,
        platform: str,
        target: str,
        message: str,
        msg_type: str = "text"
    ) -> bool:
        """
        发送消息
        
        Args:
            platform: 平台
            target: 目标ID
            message: 消息内容
            msg_type: 消息类型
            
        Returns:
            bool: 是否发送成功
        """
        if platform not in self.clients:
            await self.connect(platform)
        
        if platform not in self.clients:
            return False
        
        client = self.clients[platform]
        return await client.send_message(target, message, msg_type)
    
    async def send_all(self, message: str) -> Dict[str, bool]:
        """
        发送到所有已配置的平台
        
        Args:
            message: 消息内容
            
        Returns:
            Dict: 各平台发送结果
        """
        results = {}
        for platform, client in self.clients.items():
            success = await client.send_message(
                client.config.webhook_url or "default",
                message
            )
            results[platform] = success
        return results
    
    def get_status(self) -> Dict[str, Any]:
        """获取连接状态"""
        status = {}
        for platform in ["feishu", "wecom", "dingtalk", "qq"]:
            config = self.load_config(platform)
            status[platform] = {
                "configured": config is not None,
                "connected": platform in self.clients
            }
        return status


# 配置命令示例
CONFIG_COMMANDS = """
# 🦞 IM平台配置命令

# 1. 配置飞书
clawos im configure feishu \\
    --app-id YOUR_APP_ID \\
    --app-secret YOUR_APP_SECRET

# 2. 配置企业微信
clawos im configure wecom \\
    --corp-id YOUR_CORP_ID \\
    --app-secret YOUR_APP_SECRET

# 3. 配置钉钉
clawos im configure dingtalk \\
    --app-key YOUR_APP_KEY \\
    --app-secret YOUR_APP_SECRET

# 4. 配置QQ (需要go-cqhttp)
clawos im configure qq \\
    --http-url http://localhost:5700

# 5. 查看连接状态
clawos im status

# 6. 发送测试消息
clawos im send feishu USER_ID "Hello!"
"""

print("✅ IM管理器已加载")
