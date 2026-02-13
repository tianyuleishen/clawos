# 🦞 ClawOS API - 接口模块

"""
API接口模块 - REST/WebSocket/云服务

功能:
- REST API (RESTful接口)
- WebSocket API (实时通信)
- Cloud Service (云端集成)
"""

from .rest_api import (
    RESTAPI,
    HTTPMethod,
    APIResponse,
    APIRoute,
    create_rest_api
)

from .websocket_api import (
    WebSocketAPI,
    WSMessage,
    MessageType,
    Channel,
    create_websocket_api
)

from .cloud_service import (
    CloudService,
    CloudProvider,
    CloudConfig,
    SyncItem,
    SyncDirection,
    UpdateInfo,
    LicenseInfo,
    create_cloud_service
)

__all__ = [
    # REST API
    'RESTAPI',
    'HTTPMethod',
    'APIResponse',
    'APIRoute',
    'create_rest_api',
    
    # WebSocket API
    'WebSocketAPI',
    'WSMessage',
    'MessageType',
    'Channel',
    'create_websocket_api',
    
    # Cloud Service
    'CloudService',
    'CloudProvider',
    'CloudConfig',
    'SyncItem',
    'SyncDirection',
    'UpdateInfo',
    'LicenseInfo',
    'create_cloud_service',
]
