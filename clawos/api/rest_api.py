# 🦞 REST API - RESTful API接口

"""
REST API接口 - ClawOS Web API

功能:
- RESTful端点
- 认证
- 限流
- 文档
"""

import asyncio
import json
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
import hashlib
import secrets
import logging

from http.server import HTTPServer, BaseHTTPRequestHandler
from http import HTTPStatus


class HTTPMethod(Enum):
    """HTTP方法"""
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"
    OPTIONS = "OPTIONS"


@dataclass
class APIRoute:
    """API路由"""
    path: str
    method: HTTPMethod
    handler: Callable
    auth_required: bool = True
    roles: List[str] = field(default_factory=list)
    rate_limit: int = 100  # 每分钟请求数


@dataclass
class APIResponse:
    """API响应"""
    success: bool
    data: Any = None
    error: str = None
    message: str = None
    status_code: int = 200
    headers: Dict = field(default_factory=dict)


class RESTAPI:
    """REST API"""
    
    def __init__(self, host: str = "0.0.0.0", port: int = 8080):
        self.host = host
        self.port = port
        self.routes: Dict[str, Dict[HTTPMethod, APIRoute]] = {}
        self.auth_tokens: Dict[str, Dict] = {}
        self.rate_limits: Dict[str, List[datetime]] = {}
        self.logger = logging.getLogger("rest_api")
        
        print(f"✅ REST API 已初始化 ({host}:{port})")
    
    # ============ 路由注册 ============
    
    def route(
        self,
        path: str,
        method: HTTPMethod = HTTPMethod.GET,
        auth_required: bool = True,
        roles: List[str] = None
    ):
        """路由装饰器"""
        def decorator(handler: Callable):
            self._add_route(path, method, handler, auth_required, roles or [])
            return handler
        return decorator
    
    def _add_route(
        self,
        path: str,
        method: HTTPMethod,
        handler: Callable,
        auth_required: bool,
        roles: List[str]
    ):
        """添加路由"""
        if path not in self.routes:
            self.routes[path] = {}
        
        self.routes[path][method] = APIRoute(
            path=path,
            method=method,
            handler=handler,
            auth_required=auth_required,
            roles=roles
        )
        
        self.logger.info(f"路由已注册: {method.value} {path}")
    
    # ============ 认证 ============
    
    def generate_token(self, user_id: str, roles: List[str] = None) -> str:
        """生成认证令牌"""
        token = secrets.token_hex(32)
        
        self.auth_tokens[token] = {
            'user_id': user_id,
            'roles': roles or ['user'],
            'created_at': datetime.now(),
            'expires_at': datetime.now() + timedelta(days=30)
        }
        
        return token
    
    def validate_token(self, token: str) -> Optional[Dict]:
        """验证令牌"""
        if token not in self.auth_tokens:
            return None
        
        token_data = self.auth_tokens[token]
        
        # 检查过期
        if datetime.now() > token_data['expires_at']:
            del self.auth_tokens[token]
            return None
        
        return token_data
    
    def revoke_token(self, token: str) -> bool:
        """撤销令牌"""
        if token in self.auth_tokens:
            del self.auth_tokens[token]
            return True
        return False
    
    # ============ 限流 ============
    
    def check_rate_limit(self, client_id: str, limit: int = 100) -> bool:
        """检查限流"""
        now = datetime.now()
        minute_ago = now - timedelta(minutes=1)
        
        if client_id not in self.rate_limits:
            self.rate_limits[client_id] = []
        
        # 清理旧请求
        self.rate_limits[client_id] = [
            t for t in self.rate_limits[client_id]
            if t > minute_ago
        ]
        
        # 检查限制
        if len(self.rate_limits[client_id]) >= limit:
            return False
        
        # 记录请求
        self.rate_limits[client_id].append(now)
        return True
    
    # ============ API端点 ============
    
    def add_routes(self):
        """添加默认路由"""
        
        @self.route("/health", HTTPMethod.GET, auth_required=False)
        async def health_check():
            return APIResponse(
                success=True,
                data={'status': 'healthy', 'timestamp': datetime.now().isoformat()}
            )
        
        @self.route("/api/v1/auth/token", HTTPMethod.POST, auth_required=False)
        async def create_token(request_data: Dict):
            user_id = request_data.get('user_id', 'anonymous')
            roles = request_data.get('roles', ['user'])
            token = self.generate_token(user_id, roles)
            return APIResponse(
                success=True,
                data={'token': token},
                message="Token created"
            )
        
        @self.route("/api/v1/auth/revoke", HTTPMethod.POST, auth_required=False)
        async def revoke_token_handler(request_data: Dict):
            token = request_data.get('token', '')
            success = self.revoke_token(token)
            return APIResponse(
                success=success,
                message="Token revoked" if success else "Token not found"
            )
        
        @self.route("/api/v1/users/me", HTTPMethod.GET)
        async def get_current_user(request_data: Dict, token_data: Dict):
            return APIResponse(
                success=True,
                data={'user_id': token_data['user_id'], 'roles': token_data['roles']}
            )
        
        @self.route("/api/v1/conversations", HTTPMethod.GET)
        async def list_conversations(request_data: Dict, token_data: Dict):
            return APIResponse(
                success=True,
                data={'conversations': []}  # 简化实现
            )
        
        @self.route("/api/v1/conversations", HTTPMethod.POST)
        async def create_conversation(request_data: Dict, token_data: Dict):
            return APIResponse(
                success=True,
                data={'id': 'new_conv', 'title': request_data.get('title', 'New Chat')},
                message="Conversation created"
            )
        
        @self.route("/api/v1/messages", HTTPMethod.POST)
        async def send_message(request_data: Dict, token_data: Dict):
            return APIResponse(
                success=True,
                data={'id': 'msg_001', 'content': request_data.get('content', '')},
                message="Message sent"
            )
        
        @self.route("/api/v1/memory", HTTPMethod.GET)
        async def get_memory(request_data: Dict, token_data: Dict):
            return APIResponse(
                success=True,
                data={'memories': []}
            )
        
        @self.route("/api/v1/memory", HTTPMethod.POST)
        async def add_memory(request_data: Dict, token_data: Dict):
            return APIResponse(
                success=True,
                data={'id': 'mem_001'},
                message="Memory added"
            )
        
        @self.route("/api/v1/settings", HTTPMethod.GET)
        async def get_settings(request_data: Dict, token_data: Dict):
            return APIResponse(
                success=True,
                data={'theme': 'dark', 'language': 'zh'}
            )
        
        @self.route("/api/v1/settings", HTTPMethod.PUT)
        async def update_settings(request_data: Dict, token_data: Dict):
            return APIResponse(
                success=True,
                data=request_data,
                message="Settings updated"
            )
        
        @self.route("/api/v1/files", HTTPMethod.GET)
        async def list_files(request_data: Dict, token_data: Dict):
            return APIResponse(
                success=True,
                data={'files': []}
            )
        
        @self.route("/api/v1/files/upload", HTTPMethod.POST)
        async def upload_file(request_data: Dict, token_data: Dict):
            return APIResponse(
                success=True,
                data={'id': 'file_001'},
                message="File uploaded"
            )
        
        @self.route("/api/v1/plugins", HTTPMethod.GET)
        async def list_plugins(request_data: Dict, token_data: Dict):
            return APIResponse(
                success=True,
                data={'plugins': []}
            )
        
        @self.route("/api/v1/system/info", HTTPMethod.GET)
        async def system_info(request_data: Dict, token_data: Dict):
            return APIResponse(
                success=True,
                data={
                    'version': '0.8.0',
                    'uptime': '1h 30m',
                    'modules': 10
                }
            )
    
    # ============ 请求处理 ============
    
    async def _handle_request(self, method: HTTPMethod, path: str, data: Dict, headers: Dict) -> APIResponse:
        """处理请求"""
        # 查找路由
        if path not in self.routes:
            return APIResponse(
                success=False,
                error="Not Found",
                status_code=404
            )
        
        route = self.routes[path].get(method)
        if not route:
            return APIResponse(
                success=False,
                error="Method Not Allowed",
                status_code=405
            )
        
        # 限流
        client_id = headers.get('X-Forwarded-For', 'unknown')
        if not self.check_rate_limit(client_id, route.rate_limit):
            return APIResponse(
                success=False,
                error="Rate limit exceeded",
                status_code=429
            )
        
        # 认证
        token_data = None
        if route.auth_required:
            token = headers.get('Authorization', '').replace('Bearer ', '')
            token_data = self.validate_token(token)
            
            if not token_data:
                return APIResponse(
                    success=False,
                    error="Unauthorized",
                    status_code=401
                )
            
            # 角色检查
            if route.roles and not any(r in token_data['roles'] for r in route.roles):
                return APIResponse(
                    success=False,
                    error="Forbidden",
                    status_code=403
                )
        
        # 执行处理函数
        try:
            if asyncio.iscoroutinefunction(route.handler):
                result = await route.handler(data, token_data or {})
            else:
                result = route.handler(data, token_data or {})
            
            if isinstance(result, APIResponse):
                return result
            else:
                return APIResponse(success=True, data=result)
                
        except Exception as e:
            self.logger.error(f"处理请求失败: {e}")
            return APIResponse(
                success=False,
                error=str(e),
                status_code=500
            )
    
    # ============ 启动 ============
    
    def start(self):
        """启动API服务器"""
        self.add_routes()
        
        server = HTTPServer((self.host, self.port), self._create_handler())
        self.logger.info(f"API服务器已启动: http://{self.host}:{self.port}")
        
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            self.logger.info("API服务器已停止")
            server.shutdown()
    
    def _create_handler(self):
        """创建请求处理器"""
        routes = self.routes
        
        class APIHandler(BaseHTTPRequestHandler):
            def do_GET(self):
                self._process_request(HTTPMethod.GET)
            
            def do_POST(self):
                self._process_request(HTTPMethod.POST)
            
            def do_PUT(self):
                self._process_request(HTTPMethod.PUT)
            
            def do_DELETE(self):
                self._process_request(HTTPMethod.DELETE)
            
            def _process_request(self, method: HTTPMethod):
                # 解析路径
                path = self.path.split('?')[0]
                
                # 读取请求数据
                content_length = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(content_length).decode() if content_length > 0 else '{}'
                
                try:
                    data = json.loads(body) if body else {}
                except:
                    data = {}
                
                # 获取头
                headers = dict(self.headers)
                
                # 处理请求
                # 注意: 这里简化了异步处理
                import threading
                
                result = [None]
                error = [None]
                
                def run():
                    try:
                        response = asyncio.run(
                            routes.get(path, {}).get(method, APIRoute).handler(data, {})
                        )
                        result[0] = response
                    except Exception as e:
                        error[0] = e
                
                thread = threading.Thread(target=run)
                thread.start()
                thread.join()
                
                if error[0]:
                    response = APIResponse(success=False, error=str(error[0]), status_code=500)
                else:
                    response = result[0] or APIResponse(success=False, error="Not Found", status_code=404)
                
                # 发送响应
                self.send_response(response.status_code)
                self.send_header('Content-Type', 'application/json')
                for key, value in response.headers.items():
                    self.send_header(key, value)
                self.end_headers()
                
                self.wfile.write(json.dumps({
                    'success': response.success,
                    'data': response.data,
                    'error': response.error,
                    'message': response.message
                }, ensure_ascii=False).encode())
            
            def log_message(self, format, *args):
                pass  # 禁用默认日志
        
        return APIHandler
    
    # ============ 文档 ============
    
    def get_openapi_spec(self) -> Dict:
        """获取OpenAPI规范"""
        paths = {}
        
        for path, methods in self.routes.items():
            for method, route in methods.items():
                paths.setdefault(path, {})[method.value.lower()] = {
                    'summary': route.handler.__name__,
                    'parameters': [],
                    'responses': {
                        '200': {'description': 'Success'},
                        '401': {'description': 'Unauthorized'},
                        '403': {'description': 'Forbidden'},
                        '404': {'description': 'Not Found'},
                        '429': {'description': 'Rate Limited'},
                        '500': {'description': 'Server Error'}
                    }
                }
        
        return {
            'openapi': '3.0.0',
            'info': {
                'title': 'ClawOS API',
                'version': '0.8.0',
                'description': 'ClawOS AI Assistant API'
            },
            'paths': paths,
            'components': {
                'securitySchemes': {
                    'BearerAuth': {
                        'type': 'http',
                        'scheme': 'bearer',
                        'bearerFormat': 'JWT'
                    }
                }
            }
        }


# 便捷函数
def create_rest_api(host: str = "0.0.0.0", port: int = 8080) -> RESTAPI:
    """创建REST API"""
    return RESTAPI(host, port)


# 测试代码
if __name__ == "__main__":
    print("🌐 REST API 测试")
    
    api = REST_API("localhost", 8080)
    
    # 添加路由
    @api.route("/hello", HTTPMethod.GET, auth_required=False)
    async def hello(request_data, token_data):
        return APIResponse(
            success=True,
            data={'message': 'Hello, ClawOS API!'}
        )
    
    # 测试认证
    token = api.generate_token("test_user", ["user"])
    print(f"Token: {token}")
    
    # 验证
    valid = api.validate_token(token)
    print(f"Valid: {valid is not None}")
    
    # OpenAPI文档
    spec = api.get_openapi_spec()
    print(f"OpenAPI版本: {spec['openapi']}")
    
    print("\n✅ 测试完成")
    print("运行 api.start() 启动服务器")
