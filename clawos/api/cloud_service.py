# 🦞 Cloud Service - 云服务

"""
云服务 - ClawOS云端集成

功能:
- 云端同步
- 远程存储
- OTA更新
- 许可证管理
"""

import asyncio
import json
import os
import hashlib
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
import aiohttp
# import semver
import logging



class CloudProvider(Enum):
    """云服务提供商"""
    CLAUDOS = "clawos"  # 官方云
    AWS = "aws"
    AZURE = "azure"
    ALIBABA = "alibaba"
    TENCENT = "tencent"
    CUSTOM = "custom"


class SyncDirection(Enum):
    """同步方向"""
    PULL = "pull"  # 从云端拉取
    PUSH = "push"  # 推送到云端
    BIDirectional = "bidirectional"  # 双向


@dataclass
class CloudConfig:
    """云配置"""
    provider: CloudProvider
    endpoint: str = ""
    api_key: str = ""
    secret_key: str = ""
    region: str = "cn-hangzhou"
    bucket: str = ""
    timeout: int = 30
    retry_count: int = 3


@dataclass
class SyncItem:
    """同步项"""
    id: str
    local_path: str
    remote_path: str
    last_sync: datetime
    checksum: str
    size: int
    direction: SyncDirection = SyncDirection.BIDirectional
    enabled: bool = True


@dataclass
class UpdateInfo:
    """更新信息"""
    version: str
    download_url: str
    changelog: str
    file_size: int
    checksum: str
    release_date: datetime
    severity: str  # critical, major, minor, patch
    assets: List[Dict] = field(default_factory=list)


@dataclass
class LicenseInfo:
    """许可证信息"""
    license_key: str
    plan: str  # trial, personal, team, enterprise
    expires_at: datetime
    features: List[str]
    devices_limit: int
    devices_used: int
    status: str  # active, expired, revoked


class CloudService:
    """云服务"""
    
    def __init__(self, config: CloudConfig = None):
        self.config = config or CloudConfig(provider=CloudProvider.CLAUDOS)
        self.local_cache = Path("./data/cloud_cache")
        self.local_cache.mkdir(parents=True, exist_ok=True)
        
        self.sync_items: Dict[str, SyncItem] = {}
        self.sync_history: List[Dict] = []
        
        self.session: aiohttp.ClientSession = None
        
        self.logger = logging.getLogger("cloud_service")
        
        print(f"✅ Cloud Service 已初始化 ({self.config.provider.value})")
    
    # ============ HTTP客户端 ============
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """获取HTTP会话"""
        if self.session is None or self.session.closed:
            timeout = aiohttp.ClientTimeout(total=self.config.timeout)
            self.session = aiohttp.ClientSession(timeout=timeout)
        return self.session
    
    async def _request(
        self,
        method: str,
        url: str,
        data: Dict = None,
        headers: Dict = None
    ) -> Dict:
        """发送HTTP请求"""
        session = await self._get_session()
        
        req_headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.config.api_key}'
        }
        if headers:
            req_headers.update(headers)
        
        retry_count = self.config.retry_count
        
        for attempt in range(retry_count):
            try:
                async with session.request(
                    method, url, json=data, headers=req_headers
                ) as response:
                    result = await response.json()
                    
                    if response.status >= 400:
                        self.logger.error(f"请求失败: {result}")
                        raise Exception(f"HTTP {response.status}")
                    
                    return result
                    
            except Exception as e:
                if attempt < retry_count - 1:
                    await asyncio.sleep(2 ** attempt)  # 指数退避
                else:
                    raise
        
        return {}
    
    # ============ 云端同步 ============
    
    def add_sync_item(
        self,
        local_path: str,
        remote_path: str,
        direction: SyncDirection = SyncDirection.BIDirectional
    ) -> str:
        """添加同步项"""
        item_id = hashlib.md5(f"{local_path}{remote_path}".encode()).hexdigest()[:12]
        
        local_file = Path(local_path)
        checksum = ""
        size = 0
        
        if local_file.exists():
            checksum = self._calculate_checksum(local_path)
            size = local_file.stat().st_size
        
        self.sync_items[item_id] = SyncItem(
            id=item_id,
            local_path=local_path,
            remote_path=remote_path,
            last_sync=datetime.now() - timedelta(days=365),
            checksum=checksum,
            size=size,
            direction=direction
        )
        
        self.logger.info(f"同步项已添加: {local_path} -> {remote_path}")
        return item_id
    
    def remove_sync_item(self, item_id: str) -> bool:
        """移除同步项"""
        if item_id in self.sync_items:
            del self.sync_items[item_id]
            return True
        return False
    
    def list_sync_items(self) -> List[SyncItem]:
        """列出同步项"""
        return list(self.sync_items.values())
    
    async def sync_item(self, item_id: str) -> Dict:
        """同步单个项"""
        if item_id not in self.sync_items:
            return {'success': False, 'error': 'Item not found'}
        
        item = self.sync_items[item_id]
        
        try:
            if item.direction in [SyncDirection.PULL, SyncDirection.BIDirectional]:
                await self._pull_file(item)
            
            if item.direction in [SyncDirection.PUSH, SyncDirection.BIDirectional]:
                await self._push_file(item)
            
            item.last_sync = datetime.now()
            
            result = {
                'success': True,
                'item_id': item_id,
                'local_path': item.local_path,
                'remote_path': item.remote_path,
                'timestamp': item.last_sync.isoformat()
            }
            
            self.sync_history.append(result)
            
            return result
            
        except Exception as e:
            self.logger.error(f"同步失败: {item.local_path} - {e}")
            return {'success': False, 'error': str(e)}
    
    async def sync_all(self, direction: SyncDirection = None) -> Dict:
        """同步所有"""
        results = []
        errors = []
        
        for item_id in list(self.sync_items.keys()):
            if direction and self.sync_items[item_id].direction != direction:
                continue
            
            if not self.sync_items[item_id].enabled:
                continue
            
            result = await self.sync_item(item_id)
            
            if result['success']:
                results.append(result)
            else:
                errors.append({
                    'item_id': item_id,
                    'error': result.get('error')
                })
        
        return {
            'success': len(errors) == 0,
            'synced': len(results),
            'failed': len(errors),
            'results': results,
            'errors': errors
        }
    
    async def _pull_file(self, item: SyncItem):
        """拉取文件"""
        # 简化实现: 从本地缓存读取
        local_cache = self.local_cache / item.id
        if local_cache.exists():
            local_file = Path(item.local_path)
            local_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(local_cache, 'rb') as f:
                content = f.read()
            
            with open(item.local_path, 'wb') as f:
                f.write(content)
            
            item.checksum = self._calculate_checksum(item.local_path)
            item.size = Path(item.local_path).stat().st_size
    
    async def _push_file(self, item: SyncItem):
        """推送文件"""
        local_file = Path(item.local_path)
        if not local_file.exists():
            return
        
        # 保存到缓存
        cache_file = self.local_cache / item.id
        cache_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(item.local_path, 'rb') as f:
            content = f.read()
        
        with open(cache_file, 'wb') as f:
            f.write(content)
        
        item.checksum = self._calculate_checksum(item.local_path)
        item.size = len(content)
    
    def _calculate_checksum(self, file_path: str) -> str:
        """计算校验和"""
        hash_md5 = hashlib.md5()
        
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b''):
                hash_md5.update(chunk)
        
        return hash_md5.hexdigest()
    
    # ============ OTA更新 ============
    
    async def check_updates(self, current_version: str) -> Optional[UpdateInfo]:
        """检查更新"""
        try:
            url = f"{self.config.endpoint}/api/v1/updates/latest"
            
            data = {
                'version': current_version,
                'platform': self._get_platform()
            }
            
            result = await self._request('POST', url, data)
            
            if result.get('available'):
                return UpdateInfo(
                    version=result['version'],
                    download_url=result['download_url'],
                    changelog=result.get('changelog', ''),
                    file_size=result.get('file_size', 0),
                    checksum=result.get('checksum', ''),
                    release_date=datetime.fromisoformat(result.get('release_date', '')),
                    severity=result.get('severity', 'patch'),
                    assets=result.get('assets', [])
                )
            
            return None
            
        except Exception as e:
            self.logger.error(f"检查更新失败: {e}")
            return None
    
    async def download_update(self, update: UpdateInfo, progress_callback: Callable = None) -> str:
        """下载更新"""
        session = await self._get_session()
        
        update_file = self.local_cache / f"update_{update.version}.zip"
        
        try:
            async with session.get(update.download_url) as response:
                total_size = int(response.headers.get('Content-Length', 0))
                downloaded = 0
                
                with open(update_file, 'wb') as f:
                    async for chunk in response.content.iter_chunked(8192):
                        f.write(chunk)
                        downloaded += len(chunk)
                        
                        if progress_callback:
                            progress_callback(downloaded, total_size)
            
            # 验证校验和
            downloaded_checksum = self._calculate_checksum(str(update_file))
            
            if downloaded_checksum != update.checksum:
                raise Exception("校验和验证失败")
            
            return str(update_file)
            
        except Exception as e:
            self.logger.error(f"下载更新失败: {e}")
            raise
    
    async def apply_update(self, update_file: str) -> bool:
        """应用更新"""
        # 简化实现
        return True
    
    # ============ 许可证管理 ============
    
    async def validate_license(self, license_key: str) -> LicenseInfo:
        """验证许可证"""
        try:
            url = f"{self.config.endpoint}/api/v1/license/validate"
            
            data = {'license_key': license_key}
            result = await self._request('POST', url, data)
            
            return LicenseInfo(
                license_key=license_key,
                plan=result.get('plan', 'trial'),
                expires_at=datetime.fromisoformat(result.get('expires_at', '')),
                features=result.get('features', []),
                devices_limit=result.get('devices_limit', 1),
                devices_used=result.get('devices_used', 0),
                status=result.get('status', 'active')
            )
            
        except Exception as e:
            self.logger.error(f"验证许可证失败: {e}")
            return None
    
    async def activate_license(
        self,
        license_key: str,
        device_id: str
    ) -> Dict:
        """激活许可证"""
        try:
            url = f"{self.config.endpoint}/api/v1/license/activate"
            
            data = {
                'license_key': license_key,
                'device_id': device_id
            }
            
            result = await self._request('POST', url, data)
            
            return {
                'success': result.get('activated', False),
                'message': result.get('message', '')
            }
            
        except Exception as e:
            self.logger.error(f"激活许可证失败: {e}")
            return {'success': False, 'message': str(e)}
    
    async def deactivate_license(self, license_key: str, device_id: str) -> Dict:
        """停用许可证"""
        try:
            url = f"{self.config.endpoint}/api/v1/license/deactivate"
            
            data = {
                'license_key': license_key,
                'device_id': device_id
            }
            
            result = await self._request('POST', url, data)
            
            return {
                'success': result.get('deactivated', False),
                'message': result.get('message', '')
            }
            
        except Exception as e:
            self.logger.error(f"停用许可证失败: {e}")
            return {'success': False, 'message': str(e)}
    
    # ============ 远程存储 ============
    
    async def upload_file(
        self,
        file_path: str,
        remote_path: str,
        progress_callback: Callable = None
    ) -> Dict:
        """上传文件"""
        try:
            # 计算校验和
            checksum = self._calculate_checksum(file_path)
            file_size = Path(file_path).stat().st_size
            
            # 准备请求
            url = f"{self.config.endpoint}/api/v1/storage/upload"
            
            with open(file_path, 'rb') as f:
                content = f.read()
            
            files = {'file': (remote_path, content, 'application/octet-stream')}
            data = {'checksum': checksum, 'path': remote_path}
            
            session = await self._get_session()
            
            async with session.post(url, data=data, files=files) as response:
                result = await response.json()
                
                return {
                    'success': response.status == 200,
                    'path': remote_path,
                    'size': file_size,
                    'checksum': checksum
                }
                
        except Exception as e:
            self.logger.error(f"上传文件失败: {e}")
            return {'success': False, 'error': str(e)}
    
    async def download_file(
        self,
        remote_path: str,
        local_path: str,
        progress_callback: Callable = None
    ) -> Dict:
        """下载文件"""
        try:
            url = f"{self.config.endpoint}/api/v1/storage/download"
            
            params = {'path': remote_path}
            
            session = await self._get_session()
            
            async with session.get(url, params=params) as response:
                if response.status != 200:
                    return {'success': False, 'error': f'HTTP {response.status}'}
                
                local_file = Path(local_path)
                local_file.parent.mkdir(parents=True, exist_ok=True)
                
                total_size = int(response.headers.get('Content-Length', 0))
                downloaded = 0
                
                with open(local_file, 'wb') as f:
                    async for chunk in response.content.iter_chunked(8192):
                        f.write(chunk)
                        downloaded += len(chunk)
                        
                        if progress_callback:
                            progress_callback(downloaded, total_size)
                
                return {
                    'success': True,
                    'path': local_path,
                    'size': downloaded
                }
                
        except Exception as e:
            self.logger.error(f"下载文件失败: {e}")
            return {'success': False, 'error': str(e)}
    
    async def list_remote_files(self, path: str = "/") -> List[Dict]:
        """列出远程文件"""
        try:
            url = f"{self.config.endpoint}/api/v1/storage/list"
            
            data = {'path': path}
            result = await self._request('POST', url, data)
            
            return result.get('files', [])
            
        except Exception as e:
            self.logger.error(f"列出文件失败: {e}")
            return []
    
    async def delete_remote_file(self, remote_path: str) -> bool:
        """删除远程文件"""
        try:
            url = f"{self.config.endpoint}/api/v1/storage/delete"
            
            data = {'path': remote_path}
            result = await self._request('POST', url, data)
            
            return result.get('deleted', False)
            
        except Exception as e:
            self.logger.error(f"删除文件失败: {e}")
            return False
    
    # ============ 辅助方法 ============
    
    def _get_platform(self) -> str:
        """获取平台标识"""
        import platform
        return f"{platform.system().lower()}_{platform.machine()}"
    
    # ============ 统计 ============
    
    def get_stats(self) -> Dict:
        """获取统计"""
        return {
            'sync_items': len(self.sync_items),
            'sync_history': len(self.sync_history),
            'cache_size': sum(
                f.stat().st_size 
                for f in self.local_cache.rglob('*') 
                if f.is_file()
            ),
            'provider': self.config.provider.value,
            'endpoint': self.config.endpoint
        }
    
    # ============ 清理 ============
    
    async def close(self):
        """关闭"""
        if self.session and not self.session.closed:
            await self.session.close()
        
        self.logger.info("Cloud Service 已关闭")


# 便捷函数
def create_cloud_service(
    provider: CloudProvider = CloudProvider.CLAUDOS,
    endpoint: str = "",
    api_key: str = ""
) -> CloudService:
    """创建云服务"""
    config = CloudConfig(
        provider=provider,
        endpoint=endpoint or "https://api.clawos.ai",
        api_key=api_key
    )
    return CloudService(config)


# 测试代码
if __name__ == "__main__":
    print("☁️ Cloud Service 测试")
    
    cloud = create_cloud_service()
    
    # 测试统计
    print(f"统计: {cloud.get_stats()}")
    
    # 测试同步项
    item_id = cloud.add_sync_item(
        local_path="./test.json",
        remote_path="backup/test.json",
        direction=SyncDirection.BIDirectional
    )
    print(f"同步项ID: {item_id}")
    
    # 列出同步项
    items = cloud.list_sync_items()
    print(f"同步项数: {len(items)}")
    
    # 检查更新 (简化测试)
    update = asyncio.run(cloud.check_updates("0.8.0"))
    print(f"更新检查: {'无更新' if update is None else update.version}")
    
    # 许可证验证 (简化测试)
    # license = asyncio.run(cloud.validate_license("test_key"))
    # print(f"许可证: {license}")
    
    print("\n✅ 测试完成")
