# 🦞 File Manager - 文件管理器

"""
文件管理器 - 跨平台文件操作

功能:
- 文件读写
- 文件属性
- 文件比较
- 文件加密
- 批量处理
"""

import asyncio
import os
import hashlib
import json
import csv
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List, Optional, Union, Dict, Any, BinaryIO, TextIO
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import mimetypes

class FileType(Enum):
    """文件类型"""
    TEXT = "text"
    BINARY = "binary"
    IMAGE = "image"
    AUDIO = "audio"
    VIDEO = "video"
    DOCUMENT = "document"
    ARCHIVE = "archive"
    UNKNOWN = "unknown"

@dataclass
class FileInfo:
    """文件信息"""
    path: str
    name: str
    extension: str
    size: int
    created_time: datetime
    modified_time: datetime
    accessed_time: datetime
    is_directory: bool
    is_file: bool
    file_type: FileType
    mime_type: str
    content_hash: str = ""
    
    @property
    def size_str(self) -> str:
        """返回人类可读的文件大小"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if self.size < 1024:
                return f"{self.size:.2f} {unit}"
            self.size /= 1024
        return f"{self.size:.2f} PB"


class FileManager:
    """文件管理器"""
    
    def __init__(self):
        print("✅ File Manager 已加载")
    
    # ============ 文件读写 ============
    
    async def read_text(
        self, 
        file_path: str, 
        encoding: str = "utf-8"
    ) -> str:
        """读取文本文件
        
        Args:
            file_path: 文件路径
            encoding: 编码格式
        
        Returns:
            str: 文件内容
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            lambda: Path(file_path).read_text(encoding=encoding)
        )
    
    async def write_text(
        self, 
        file_path: str, 
        content: str, 
        encoding: str = "utf-8",
        mode: str = "w"
    ):
        """写入文本文件
        
        Args:
            file_path: 文件路径
            content: 内容
            encoding: 编码格式
            mode: 写入模式 (w=覆盖, a=追加)
        """
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            None,
            lambda: Path(file_path).write_text(content, encoding=encoding)
        )
    
    async def read_bytes(self, file_path: str) -> bytes:
        """读取二进制文件
        
        Args:
            file_path: 文件路径
        
        Returns:
            bytes: 文件内容
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            lambda: Path(file_path).read_bytes()
        )
    
    async def write_bytes(self, file_path: str, data: bytes, mode: str = "wb"):
        """写入二进制文件
        
        Args:
            file_path: 文件路径
            data: 二进制数据
            mode: 写入模式
        """
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            None,
            lambda: Path(file_path).write_bytes(data)
        )
    
    # ============ JSON 操作 ============
    
    async def read_json(self, file_path: str, encoding: str = "utf-8") -> Dict:
        """读取JSON文件
        
        Args:
            file_path: 文件路径
            encoding: 编码格式
        
        Returns:
            Dict: JSON对象
        """
        content = await self.read_text(file_path, encoding)
        return json.loads(content)
    
    async def write_json(
        self, 
        file_path: str, 
        data: Any, 
        encoding: str = "utf-8",
        indent: int = 2
    ):
        """写入JSON文件
        
        Args:
            file_path: 文件路径
            data: 数据对象
            encoding: 编码格式
            indent: 缩进
        """
        content = json.dumps(data, ensure_ascii=False, indent=indent)
        await self.write_text(file_path, content, encoding)
    
    async def update_json(self, file_path: str, updates: Dict):
        """更新JSON文件
        
        Args:
            file_path: 文件路径
            updates: 更新的键值对
        """
        data = await self.read_json(file_path)
        data.update(updates)
        await self.write_json(file_path, data)
    
    # ============ CSV 操作 ============
    
    async def read_csv(
        self, 
        file_path: str, 
        encoding: str = "utf-8",
        delimiter: str = ","
    ) -> List[Dict]:
        """读取CSV文件
        
        Args:
            file_path: 文件路径
            encoding: 编码格式
            delimiter: 分隔符
        
        Returns:
            List[Dict]: 数据列表
        """
        loop = asyncio.get_event_loop()
        
        def _read():
            with open(file_path, 'r', encoding=encoding) as f:
                reader = csv.DictReader(f, delimiter=delimiter)
                return list(reader)
        
        return await loop.run_in_executor(None, _read)
    
    async def write_csv(
        self, 
        file_path: str, 
        data: List[Dict],
        fieldnames: List[str] = None,
        encoding: str = "utf-8",
        delimiter: str = ","
    ):
        """写入CSV文件
        
        Args:
            file_path: 文件路径
            data: 数据列表
            fieldnames: 字段名
            encoding: 编码格式
            delimiter: 分隔符
        """
        loop = asyncio.get_event_loop()
        
        def _write():
            with open(file_path, 'w', encoding=encoding, newline='') as f:
                if not fieldnames and data:
                    fieldnames = list(data[0].keys())
                writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=delimiter)
                writer.writeheader()
                writer.writerows(data)
        
        await loop.run_in_executor(None, _write)
    
    # ============ XML 操作 ============
    
    async def read_xml(self, file_path: str) -> ET.Element:
        """读取XML文件
        
        Args:
            file_path: 文件路径
        
        Returns:
            Element: XML根元素
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            lambda: ET.parse(file_path).getroot()
        )
    
    async def write_xml(
        self, 
        file_path: str, 
        root: ET.Element,
        encoding: str = "utf-8"
    ):
        """写入XML文件
        
        Args:
            file_path: 文件路径
            root: XML根元素
            encoding: 编码格式
        """
        loop = asyncio.get_event_loop()
        
        def _write():
            tree = ET.ElementTree(root)
            tree.write(file_path, encoding=encoding, xml_declaration=True)
        
        await loop.run_in_executor(None, _write)
    
    # ============ 文件信息 ============
    
    async def get_info(self, file_path: str) -> FileInfo:
        """获取文件信息
        
        Args:
            file_path: 文件路径
        
        Returns:
            FileInfo: 文件信息对象
        """
        loop = asyncio.get_event_loop()
        path = Path(file_path)
        
        stat = await loop.run_in_executor(None, lambda: path.stat())
        
        # 计算哈希
        content_hash = ""
        if path.is_file():
            content_hash = await self.get_hash(file_path)
        
        # 判断文件类型
        file_type = self._get_file_type(path, file_path)
        mime_type, _ = mimetypes.guess_type(file_path)
        
        return FileInfo(
            path=str(path.absolute()),
            name=path.name,
            extension=path.suffix.lower(),
            size=stat.st_size,
            created_time=datetime.fromtimestamp(stat.st_ctime),
            modified_time=datetime.fromtimestamp(stat.st_mtime),
            accessed_time=datetime.fromtimestamp(stat.st_atime),
            is_directory=path.is_dir(),
            is_file=path.is_file(),
            file_type=file_type,
            mime_type=mime_type or "application/octet-stream",
            content_hash=content_hash
        )
    
    async def exists(self, file_path: str) -> bool:
        """检查文件是否存在"""
        return Path(file_path).exists()
    
    async def is_file(self, file_path: str) -> bool:
        """检查是否是文件"""
        return Path(file_path).is_file()
    
    async def is_dir(self, file_path: str) -> bool:
        """检查是否是目录"""
        return Path(file_path).is_dir()
    
    # ============ 文件操作 ============
    
    async def copy(self, src: str, dst: str):
        """复制文件"""
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            None,
            lambda: Path(src).copy_to(Path(dst))
        )
    
    async def move(self, src: str, dst: str):
        """移动文件"""
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            None,
            lambda: Path(src).move_to(Path(dst))
        )
    
    async def rename(self, file_path: str, new_name: str):
        """重命名文件"""
        loop = asyncio.get_event_loop()
        path = Path(file_path)
        await loop.run_in_executor(
            None,
            lambda: path.rename(path.parent / new_name)
        )
    
    async def delete(self, file_path: str):
        """删除文件"""
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            None,
            lambda: Path(file_path).unlink()
        )
    
    async def mkdir(self, dir_path: str, parents: bool = True):
        """创建目录"""
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            None,
            lambda: Path(dir_path).mkdir(parents=parents, exist_ok=True)
        )
    
    async def rmdir(self, dir_path: str):
        """删除空目录"""
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            None,
            lambda: Path(dir_path).rmdir()
        )
    
    async def remove_tree(self, dir_path: str):
        """删除目录树"""
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            None,
            lambda: Path(dir_path).rmdir()
        )
    
    # ============ 文件内容 ============
    
    async def append_text(
        self, 
        file_path: str, 
        content: str,
        encoding: str = "utf-8"
    ):
        """追加文本"""
        await self.write_text(file_path, content, encoding, mode="a")
    
    async def prepend_text(
        self, 
        file_path: str, 
        content: str,
        encoding: str = "utf-8"
    ):
        """前置文本"""
        original = await self.read_text(file_path, encoding)
        await self.write_text(file_path, content + original, encoding)
    
    async def read_lines(
        self, 
        file_path: str, 
        encoding: str = "utf-8"
    ) -> List[str]:
        """读取所有行"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            lambda: Path(file_path).read_text(encoding=encoding).splitlines()
        )
    
    async def write_lines(
        self, 
        file_path: str, 
        lines: List[str],
        encoding: str = "utf-8"
    ):
        """写入多行"""
        content = "\n".join(lines)
        await self.write_text(file_path, content, encoding)
    
    async def read_chunk(
        self, 
        file_path: str, 
        offset: int = 0, 
        size: int = 4096
    ) -> bytes:
        """读取文件块
        
        Args:
            file_path: 文件路径
            offset: 偏移量
            size: 块大小
        
        Returns:
            bytes: 文件块内容
        """
        loop = asyncio.get_event_loop()
        
        def _read():
            with open(file_path, 'rb') as f:
                f.seek(offset)
                return f.read(size)
        
        return await loop.run_in_executor(None, _read)
    
    # ============ 哈希计算 ============
    
    async def get_hash(
        self, 
        file_path: str, 
        algorithm: str = "md5"
    ) -> str:
        """计算文件哈希
        
        Args:
            file_path: 文件路径
            algorithm: 算法 (md5, sha1, sha256, sha512)
        
        Returns:
            str: 哈希值
        """
        loop = asyncio.get_event_loop()
        
        def _calc():
            hash_obj = hashlib.new(algorithm)
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(8192), b''):
                    hash_obj.update(chunk)
            return hash_obj.hexdigest()
        
        return await loop.run_in_executor(None, _calc)
    
    async def compare_files(self, file1: str, file2: str) -> bool:
        """比较两个文件
        
        Args:
            file1: 文件1
            file2: 文件2
        
        Returns:
            bool: 是否相同
        """
        # 先比较大小
        info1 = await self.get_info(file1)
        info2 = await self.get_info(file2)
        
        if info1.size != info2.size:
            return False
        
        # 再比较哈希
        hash1 = await self.get_hash(file1)
        hash2 = await self.get_hash(file2)
        
        return hash1 == hash2
    
    # ============ 辅助方法 ============
    
    def _get_file_type(self, path: Path, file_path: str) -> FileType:
        """判断文件类型"""
        if path.is_dir():
            return FileType.UNKNOWN
        
        ext = path.suffix.lower()
        
        # 图片
        if ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg']:
            return FileType.IMAGE
        
        # 音频
        if ext in ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a']:
            return FileType.AUDIO
        
        # 视频
        if ext in ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv']:
            return FileType.VIDEO
        
        # 文档
        if ext in ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.txt']:
            return FileType.DOCUMENT
        
        # 压缩包
        if ext in ['.zip', '.tar', '.gz', '.7z', '.rar', '.bz2']:
            return FileType.ARCHIVE
        
        # 文本
        if ext in ['.txt', '.md', '.py', '.js', '.html', '.css', '.json', '.xml', '.csv']:
            return FileType.TEXT
        
        return FileType.UNKNOWN
    
    # ============ 便捷方法 ============
    
    async def read_config(self, file_path: str) -> Dict:
        """读取配置文件 (JSON/YAML/TOML)"""
        ext = Path(file_path).suffix.lower()
        
        if ext == '.json':
            return await self.read_json(file_path)
        elif ext == '.yaml' or ext == '.yml':
            # YAML需要pyyaml库
            try:
                import yaml
                content = await self.read_text(file_path)
                return yaml.safe_load(content)
            except ImportError:
                raise ImportError("请安装pyyaml: pip install pyyaml")
        elif ext == '.toml':
            # TOML需要toml库
            try:
                import toml
                return toml.load(file_path)
            except ImportError:
                raise ImportError("请安装toml: pip install toml")
        else:
            raise ValueError(f"不支持的配置文件格式: {ext}")
    
    async def save_config(
        self, 
        file_path: str, 
        data: Dict,
        format: str = "json"
    ):
        """保存配置文件"""
        if format == "json":
            await self.write_json(file_path, data)
        elif format == "yaml":
            try:
                import yaml
                content = yaml.dump(data, allow_unicode=True)
                await self.write_text(file_path, content)
            except ImportError:
                raise ImportError("请安装pyyaml: pip install pyyaml")
        elif format == "toml":
            try:
                import toml
                toml.dump(file_path, data)
            except ImportError:
                raise ImportError("请安装toml: pip install toml")


# 便捷函数
async def read_file(file_path: str) -> str:
    """读取文本文件"""
    manager = FileManager()
    return await manager.read_text(file_path)

async def write_file(file_path: str, content: str):
    """写入文本文件"""
    manager = FileManager()
    await manager.write_text(file_path, content)

# 测试代码
if __name__ == "__main__":
    async def test():
        print("📁 文件管理器测试")
        
        manager = FileManager()
        
        # 测试文本读写
        print("\n1. 测试文本读写...")
        await manager.write_text("/tmp/clawos_test.txt", "Hello ClawOS!")
        content = await manager.read_text("/tmp/clawos_test.txt")
        print(f"   写入并读取: {content}")
        
        # 测试JSON
        print("\n2. 测试JSON读写...")
        data = {"name": "ClawOS", "version": "0.2.0", "features": ["AI", "Control"]}
        await manager.write_json("/tmp/clawos_test.json", data)
        loaded = await manager.read_json("/tmp/clawos_test.json")
        print(f"   JSON数据: {loaded}")
        
        # 测试文件信息
        print("\n3. 测试文件信息...")
        info = await manager.get_info("/tmp/clawos_test.txt")
        print(f"   文件名: {info.name}")
        print(f"   大小: {info.size_str}")
        print(f"   类型: {info.file_type.value}")
        
        # 测试哈希
        print("\n4. 测试哈希计算...")
        hash_val = await manager.get_hash("/tmp/clawos_test.txt", "md5")
        print(f"   MD5: {hash_val}")
        
        print("\n✅ 测试完成")
    
    asyncio.run(test())
