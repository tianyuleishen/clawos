# 🦞 ClawOS IM集成模块

"""
即时通讯集成 - 支持飞书、企业微信、钉钉、QQ

快速开始:
    from clawos.im import IMManager
    
    # 配置凭证
    manager = IMManager()
    manager.configure("feishu", {
        "app_id": "your_app_id",
        "app_secret": "your_app_secret"
    })
    
    # 发送消息
    await manager.connect("feishu")
    await manager.send_message("feishu", "user_id", "Hello!")
"""

from .base import IMClient, IMPlatform, IMConfig
from .feishu import FeishuClient
from .wecom import WeComClient
from .dingtalk import DingTalkClient
from .qq import QQClient
from .manager import IMManager

__all__ = [
    'IMClient',
    'IMPlatform',
    'IMConfig',
    'FeishuClient',
    'WeComClient',
    'DingTalkClient',
    'QQClient',
    'IMManager',
]

__version__ = "1.0.0"

# 快捷方式
def create_client(platform: str, **credentials) -> IMClient:
    """
    快速创建IM客户端
    
    Args:
        platform: 平台名称
        **credentials: 凭证信息
        
    Returns:
        IMClient: IM客户端实例
    """
    from .base import IMConfig
    
    config = IMConfig.from_dict({"platform": platform, **credentials})
    return IMClient.create_client(config)


# 平台配置帮助
PLATFORM_HELP = {
    "feishu": """
飞书配置:
    required: app_id, app_secret
    optional: webhook_url
    
    获取凭证:
    1. 登录 https://open.feishu.cn/
    2. 创建应用
    3. 获取app_id和app_secret
    """,
    
    "wecom": """
企业微信配置:
    required: app_id (corp_id), app_secret
    optional: agent_id
    
    获取凭证:
    1. 登录 https://work.weixin.qq.com/
    2. 创建应用
    3. 获取corp_id, agent_id, app_secret
    """,
    
    "dingtalk": """
钉钉配置:
    required: app_key/app_id, app_secret
    optional: agent_id
    
    获取凭证:
    1. 登录 https://open.dingtalk.com/
    2. 创建应用
    3. 获取appKey和appSecret
    """,
    
    "qq": """
QQ配置 (通过go-cqhttp):
    required: http_url
    optional: access_token
    
    配置步骤:
    1. 下载安装 go-cqhttp
    2. 配置HTTP API端口
    3. 启动服务
    """
}

print("✅ ClawOS IM模块已加载")
print("    支持平台: 飞书, 企业微信, 钉钉, QQ")
print("    使用: from clawos.im import IMManager")
