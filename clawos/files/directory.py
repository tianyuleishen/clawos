# 🦞 Directory Manager - 文件夹管理器

"""
文件夹管理器 - 跨平台目录操作

功能:
- 目录遍历
- 目录创建/删除
- 目录复制/移动
- 目录搜索
- 批量操作
"""

import asyncio
import os
import shutil
import fnmatch
from pathlib import Path
from typing import List, Optional, Callable, Union, Set
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from .file import FileManager, FileInfo, FileType

class SortOrder(Enum):
    """排序方式"""
    NAME = "name"
    NAME_DESC = "name_desc"
    SIZE = "size"
    SIZE_DESC = "size_desc"
    DATE = "date"
    DATE_DESC = "date_desc"
    TYPE = "type"

class ListMode(Enum):
    """列表模式"""
    FLAT = "flat"  # 扁平列表
    TREE = "tree"  # 树形结构

@dataclass
class DirectoryEntry:
    """目录条目"""
    path: str
    name: str
    is_directory: bool
    is_file: bool
    children_count: int = 0
    depth: int = 0

class DirectoryManager:
    """文件夹管理器"""
    
    def __init__(self):
        self.file_manager = FileManager()
        print("✅ Directory Manager 已加载")
    
    # ============ 目录遍历 ============
    
    async def list_dir(
        self, 
        dir_path: str,
        sort_by: SortOrder = SortOrder.NAME,
        reverse: bool = False
    ) -> List[DirectoryEntry]:
        """列出目录内容
        
        Args:
            dir_path: 目录路径
            sort_by: 排序方式
            reverse: 是否反向排序
        
        Returns:
            List[DirectoryEntry]: 条目列表
        """
        loop = asyncio.get_event_loop()
        
        def _list():
            path = Path(dir_path)
            entries = []
            
            for item in path.iterdir():
                if item.name.startswith('.'):
                    continue  # 跳过隐藏文件
                
                is_dir = item.is_dir()
                children = 0
                
                if is_dir:
                    try:
                        children = len(list(item.iterdir()))
                    except:
                        children = 0
                
                entries.append(DirectoryEntry(
                    path=str(item.absolute()),
                    name=item.name,
                    is_directory=is_dir,
                    is_file=item.is_file(),
                    children_count=children
                ))
            
            # 排序
            if sort_by == SortOrder.NAME:
                entries.sort(key=lambda x: x.name.lower(), reverse=reverse)
            elif sort_by == SortOrder.NAME_DESC:
                entries.sort(key=lambda x: x.name.lower(), reverse=not reverse)
            
            return entries
        
        return await loop.run_in_executor(None, _list)
    
    async def list_files(
        self, 
        dir_path: str,
        extensions: List[str] = None,
        recursive: bool = False,
        sort_by: SortOrder = SortOrder.NAME
    ) -> List[DirectoryEntry]:
        """列出文件
        
        Args:
            dir_path: 目录路径
            extensions: 文件扩展名过滤
            recursive: 是否递归
            sort_by: 排序方式
        
        Returns:
            List[DirectoryEntry]: 文件列表
        """
        loop = asyncio.get_event_loop()
        
        def _list():
            path = Path(dir_path)
            files = []
            
            if recursive:
                for item in path.rglob("*"):
                    if item.is_file() and not item.name.startswith('.'):
                        if extensions:
                            if item.suffix.lower() in [e.lower() for e in extensions]:
                                files.append(DirectoryEntry(
                                    path=str(item.absolute()),
                                    name=str(item.relative_to(path)),
                                    is_directory=False,
                                    is_file=True
                                ))
                        else:
                            files.append(DirectoryEntry(
                                path=str(item.absolute()),
                                name=str(item.relative_to(path)),
                                is_directory=False,
                                is_file=True
                            ))
            else:
                for item in path.iterdir():
                    if item.is_file() and not item.name.startswith('.'):
                        if extensions:
                            if item.suffix.lower() in [e.lower() for e in extensions]:
                                files.append(DirectoryEntry(
                                    path=str(item.absolute()),
                                    name=item.name,
                                    is_directory=False,
                                    is_file=True
                                ))
                        else:
                            files.append(DirectoryEntry(
                                path=str(item.absolute()),
                                name=item.name,
                                is_directory=False,
                                is_file=True
                            ))
            
            # 排序
            files.sort(key=lambda x: x.name.lower())
            
            return files
        
        return await loop.run_in_executor(None, _list)
    
    async def list_dirs(
        self, 
        dir_path: str,
        recursive: bool = False
    ) -> List[DirectoryEntry]:
        """列出子目录
        
        Args:
            dir_path: 目录路径
            recursive: 是否递归
        
        Returns:
            List[DirectoryEntry]: 目录列表
        """
        loop = asyncio.get_event_loop()
        
        def _list():
            path = Path(dir_path)
            dirs = []
            
            if recursive:
                for item in path.rglob("*"):
                    if item.is_dir() and not item.name.startswith('.'):
                        dirs.append(DirectoryEntry(
                            path=str(item.absolute()),
                            name=str(item.relative_to(path)),
                            is_directory=True,
                            is_file=False,
                            depth=len(item.relative_to(path).parts) - 1
                        ))
            else:
                for item in path.iterdir():
                    if item.is_dir() and not item.name.startswith('.'):
                        dirs.append(DirectoryEntry(
                            path=str(item.absolute()),
                            name=item.name,
                            is_directory=True,
                            is_file=False
                        ))
            
            return dirs
        
        return await loop.run_in_executor(None, _list)
    
    async def walk(
        self, 
        dir_path: str,
        topdown: bool = True
    ):
        """遍历目录 (生成器)
        
        Args:
            dir_path: 目录路径
            topdown: 从上到下
        
        Yields:
            tuple: (当前目录, 子目录列表, 文件列表)
        """
        path = Path(dir_path)
        
        if not path.exists() or not path.is_dir():
            return
        
        dirs = []
        files = []
        
        for item in path.iterdir():
            if item.is_dir():
                dirs.append(item.name)
            else:
                files.append(item.name)
        
        yield (str(path), dirs, files)
        
        if topdown:
            for subdir in dirs:
                async for result in self.walk(str(path / subdir), topdown):
                    yield result
    
    # ============ 目录创建 ============
    
    async def create(
        self, 
        dir_path: str,
        parents: bool = True,
        exist_ok: bool = True
    ):
        """创建目录
        
        Args:
            dir_path: 目录路径
            parents: 是否创建父目录
            exist_ok: 目录存在时是否报错
        """
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            None,
            lambda: Path(dir_path).mkdir(parents=parents, exist_ok=exist_ok)
        )
    
    async def create_temp(self, prefix: str = "clawos_") -> str:
        """创建临时目录
        
        Args:
            prefix: 前缀
        
        Returns:
            str: 临时目录路径
        """
        import tempfile
        return tempfile.mkdtemp(prefix=prefix)
    
    # ============ 目录删除 ============
    
    async def delete(self, dir_path: str, recursive: bool = False):
        """删除目录
        
        Args:
            dir_path: 目录路径
            recursive: 是否递归删除
        """
        loop = asyncio.get_event_loop()
        
        if recursive:
            await loop.run_in_executor(
                None,
                lambda: shutil.rmtree(dir_path, ignore_errors=True)
            )
        else:
            await loop.run_in_executor(
                None,
                lambda: Path(dir_path).rmdir()
            )
    
    async def clean(self, dir_path: str):
        """清空目录 (保留目录本身)
        
        Args:
            dir_path: 目录路径
        """
        loop = asyncio.get_event_loop()
        
        def _clean():
            path = Path(dir_path)
            for item in path.iterdir():
                if item.is_dir():
                    shutil.rmtree(str(item))
                else:
                    item.unlink()
        
        await loop.run_in_executor(None, _clean)
    
    # ============ 目录复制/移动 ============
    
    async def copy(
        self, 
        src: str, 
        dst: str,
        overwrite: bool = False
    ):
        """复制目录
        
        Args:
            src: 源目录
            dst: 目标目录
            overwrite: 是否覆盖
        """
        loop = asyncio.get_event_loop()
        
        def _copy():
            shutil.copytree(src, dst, dirs_exist_ok=overwrite)
        
        await loop.run_in_executor(None, _copy)
    
    async def move(self, src: str, dst: str):
        """移动目录
        
        Args:
            src: 源目录
            dst: 目标目录
        """
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            None,
            lambda: shutil.move(src, dst)
        )
    
    async def rename(self, dir_path: str, new_name: str):
        """重命名目录
        
        Args:
            dir_path: 当前路径
            new_name: 新名称
        """
        loop = asyncio.get_event_loop()
        path = Path(dir_path)
        await loop.run_in_executor(
            None,
            lambda: path.rename(path.parent / new_name)
        )
    
    # ============ 目录搜索 ============
    
    async def find(
        self, 
        dir_path: str,
        pattern: str = "*",
        recursive: bool = True,
        file_type: str = "all"  # "file", "dir", "all"
    ) -> List[str]:
        """搜索文件和目录
        
        Args:
            dir_path: 搜索目录
            pattern: 匹配模式
            recursive: 是否递归
            file_type: 类型过滤
        
        Returns:
            List[str]: 匹配的文件路径列表
        """
        loop = asyncio.get_event_loop()
        
        def _find():
            path = Path(dir_path)
            results = []
            
            if recursive:
                iterator = path.rglob(pattern)
            else:
                iterator = path.glob(pattern)
            
            for item in iterator:
                if file_type == "file" and item.is_file():
                    results.append(str(item.absolute()))
                elif file_type == "dir" and item.is_dir():
                    results.append(str(item.absolute()))
                elif file_type == "all":
                    results.append(str(item.absolute()))
            
            return results
        
        return await loop.run_in_executor(None, _find)
    
    async def find_by_name(
        self, 
        dir_path: str,
        name: str,
        recursive: bool = True,
        case_sensitive: bool = False
    ) -> List[str]:
        """按名称搜索
        
        Args:
            dir_path: 搜索目录
            name: 名称
            recursive: 是否递归
            case_sensitive: 是否大小写敏感
        
        Returns:
            List[str]: 匹配的文件路径列表
        """
        loop = asyncio.get_event_loop()
        
        def _find():
            path = Path(dir_path)
            results = []
            
            if not case_sensitive:
                name = name.lower()
            
            def match(item_name):
                if case_sensitive:
                    return name in item_name
                return name.lower() in item_name
            
            if recursive:
                for item in path.rglob("*"):
                    if match(item.name):
                        results.append(str(item.absolute()))
            else:
                for item in path.iterdir():
                    if match(item.name):
                        results.append(str(item.absolute()))
            
            return results
        
        return await loop.run_in_executor(None, _find)
    
    async def find_by_extension(
        self, 
        dir_path: str,
        extensions: List[str],
        recursive: bool = True
    ) -> List[str]:
        """按扩展名搜索
        
        Args:
            dir_path: 搜索目录
            extensions: 扩展名列表
            recursive: 是否递归
        
        Returns:
            List[str]: 匹配的文件路径列表
        """
        patterns = [f"*{ext}" for ext in extensions]
        
        loop = asyncio.get_event_loop()
        results = []
        
        for pattern in patterns:
            found = await self.find(dir_path, pattern, recursive, "file")
            results.extend(found)
        
        return list(set(results))  # 去重
    
    async def find_by_size(
        self, 
        dir_path: str,
        min_size: int = 0,
        max_size: int = None,
        recursive: bool = True
    ) -> List[str]:
        """按大小搜索
        
        Args:
            dir_path: 搜索目录
            min_size: 最小大小 (字节)
            max_size: 最大大小 (字节)
            recursive: 是否递归
        
        Returns:
            List[str]: 匹配的文件路径列表
        """
        loop = asyncio.get_event_loop()
        
        def _find():
            path = Path(dir_path)
            results = []
            
            if recursive:
                iterator = path.rglob("*")
            else:
                iterator = path.glob("*")
            
            for item in iterator:
                if item.is_file():
                    size = item.stat().st_size
                    if size >= min_size:
                        if max_size is None or size <= max_size:
                            results.append(str(item.absolute()))
            
            return results
        
        return await loop.run_in_executor(None, _find)
    
    async def find_by_date(
        self, 
        dir_path: str,
        after: datetime = None,
        before: datetime = None,
        recursive: bool = True
    ) -> List[str]:
        """按日期搜索
        
        Args:
            dir_path: 搜索目录
            after: 之后
            before: 之前
            recursive: 是否递归
        
        Returns:
            List[str]: 匹配的文件路径列表
        """
        loop = asyncio.get_event_loop()
        
        def _find():
            path = Path(dir_path)
            results = []
            
            if recursive:
                iterator = path.rglob("*")
            else:
                iterator = path.glob("*")
            
            for item in iterator:
                if item.is_file():
                    mtime = datetime.fromtimestamp(item.stat().st_mtime)
                    
                    if after and mtime < after:
                        continue
                    if before and mtime > before:
                        continue
                    
                    results.append(str(item.absolute()))
            
            return results
        
        return await loop.run_in_executor(None, _find)
    
    # ============ 批量操作 ============
    
    async def copy_files(
        self, 
        files: List[str],
        dst_dir: str,
        overwrite: bool = False
    ):
        """批量复制文件
        
        Args:
            files: 文件路径列表
            dst_dir: 目标目录
            overwrite: 是否覆盖
        """
        loop = asyncio.get_event_loop()
        
        def _copy():
            Path(dst_dir).mkdir(parents=True, exist_ok=True)
            for src in files:
                dst = str(Path(dst_dir) / Path(src).name)
                if overwrite or not Path(dst).exists():
                    shutil.copy2(src, dst)
        
        await loop.run_in_executor(None, _copy)
    
    async def move_files(
        self, 
        files: List[str],
        dst_dir: str
    ):
        """批量移动文件
        
        Args:
            files: 文件路径列表
            dst_dir: 目标目录
        """
        loop = asyncio.get_event_loop()
        
        def _move():
            Path(dst_dir).mkdir(parents=True, exist_ok=True)
            for src in files:
                dst = str(Path(dst_dir) / Path(src).name)
                shutil.move(src, dst)
        
        await loop.run_in_executor(None, _move)
    
    async def delete_files(self, files: List[str]):
        """批量删除文件
        
        Args:
            files: 文件路径列表
        """
        loop = asyncio.get_event_loop()
        
        def _delete():
            for file_path in files:
                try:
                    Path(file_path).unlink()
                except:
                    pass
        
        await loop.run_in_executor(None, _delete)
    
    # ============ 统计信息 ============
    
    async def get_stats(self, dir_path: str) -> Dict:
        """获取目录统计信息
        
        Args:
            dir_path: 目录路径
        
        Returns:
            Dict: 统计信息
        """
        loop = asyncio.get_event_loop()
        
        def _stats():
            path = Path(dir_path)
            stats = {
                "total_files": 0,
                "total_dirs": 0,
                "total_size": 0,
                "file_types": {}
            }
            
            for item in path.rglob("*"):
                if item.is_file():
                    stats["total_files"] += 1
                    stats["total_size"] += item.stat().st_size
                    
                    ext = item.suffix.lower()
                    stats["file_types"][ext] = stats["file_types"].get(ext, 0) + 1
                elif item.is_dir():
                    stats["total_dirs"] += 1
            
            return stats
        
        return await loop.run_in_executor(None, _stats)
    
    # ============ 过滤 ============
    
    async def filter_files(
        self, 
        files: List[str],
        extensions: List[str] = None,
        min_size: int = None,
        max_size: int = None,
        patterns: List[str] = None
    ) -> List[str]:
        """过滤文件列表
        
        Args:
            files: 文件列表
            extensions: 扩展名过滤
            min_size: 最小大小
            max_size: 最大大小
            patterns: 名称模式
        
        Returns:
            List[str]: 过滤后的文件列表
        """
        result = []
        
        for file_path in files:
            path = Path(file_path)
            
            # 扩展名过滤
            if extensions:
                if path.suffix.lower() not in [e.lower() for e in extensions]:
                    continue
            
            # 大小过滤
            if min_size is not None or max_size is not None:
                size = path.stat().st_size
                if min_size is not None and size < min_size:
                    continue
                if max_size is not None and size > max_size:
                    continue
            
            # 模式过滤
            if patterns:
                matched = False
                for pattern in patterns:
                    if fnmatch.fnmatch(path.name, pattern):
                        matched = True
                        break
                if not matched:
                    continue
            
            result.append(file_path)
        
        return result
    
    # ============ 工具方法 ============
    
    async def get_tree(
        self, 
        dir_path: str,
        max_depth: int = 3,
        current_depth: int = 0,
        prefix: str = ""
    ) -> List[str]:
        """获取树形结构
        
        Args:
            dir_path: 目录路径
            max_depth: 最大深度
            current_depth: 当前深度
            prefix: 前缀
        
        Returns:
            List[str]: 树形结构字符串列表
        """
        lines = []
        path = Path(dir_path)
        
        # 当前目录
        if current_depth == 0:
            lines.append(f"📁 {path.name}/")
        else:
            lines.append(f"{prefix}📁 {path.name}/")
        
        if current_depth >= max_depth:
            return lines
        
        # 获取子项
        items = sorted([
            item for item in path.iterdir()
            if not item.name.startswith('.')
        ], key=lambda x: (not x.is_dir(), x.name.lower()))
        
        for i, item in enumerate(items):
            is_last = (i == len(items) - 1)
            new_prefix = prefix + ("    " if is_last else "│   ")
            
            if item.is_dir():
                lines.extend(await self.get_tree(
                    str(item), max_depth, current_depth + 1, new_prefix
                ))
            else:
                lines.append(f"{new_prefix}📄 {item.name}")
        
        return lines
    
    async def format_tree(self, dir_path: str, max_depth: int = 3) -> str:
        """格式化树形结构
        
        Args:
            dir_path: 目录路径
            max_depth: 最大深度
        
        Returns:
            str: 树形结构字符串
        """
        lines = await self.get_tree(dir_path, max_depth)
        return "\n".join(lines)
    
    async def is_empty(self, dir_path: str) -> bool:
        """检查目录是否为空"""
        path = Path(dir_path)
        if not path.exists() or not path.is_dir():
            return True
        
        return not any(path.iterdir())
    
    async def get_disk_usage(self, dir_path: str) -> Dict:
        """获取磁盘使用情况
        
        Args:
            dir_path: 目录路径
        
        Returns:
            Dict: 使用情况
        """
        loop = asyncio.get_event_loop()
        
        def _usage():
            path = Path(dir_path)
            total, used, free = shutil.disk_usage(str(path.parent))
            return {
                "total": total,
                "used": used,
                "free": free,
                "percent": (used / total) * 100
            }
        
        return await loop.run_in_executor(None, _usage)


# 便捷函数
async def list_dir(dir_path: str) -> List[DirectoryEntry]:
    """列出目录内容"""
    manager = DirectoryManager()
    return await manager.list_dir(dir_path)

async def find_files(dir_path: str, pattern: str = "*") -> List[str]:
    """搜索文件"""
    manager = DirectoryManager()
    return await manager.find(dir_path, pattern)

# 测试代码
if __name__ == "__main__":
    async def test():
        print("📂 文件夹管理器测试")
        
        manager = DirectoryManager()
        
        # 测试列出
        print("\n1. 测试列出目录...")
        entries = await manager.list_dir("/home/admin/.openclaw/workspace")
        print(f"   项目目录包含 {len(entries)} 个条目")
        
        # 测试搜索
        print("\n2. 测试搜索...")
        py_files = await manager.find_by_extension(
            "/home/admin/.openclaw/workspace", [".py"]
        )
        print(f"   Python文件: {len(py_files)} 个")
        
        # 测试树形结构
        print("\n3. 测试树形结构...")
        tree = await manager.format_tree("/home/admin/.openclaw/workspace/clawos", max_depth=2)
        print(tree[:500])
        
        # 测试统计
        print("\n4. 测试统计...")
        stats = await manager.get_stats("/home/admin/.openclaw/workspace")
        print(f"   文件数: {stats['total_files']}")
        print(f"   目录数: {stats['total_dirs']}")
        
        print("\n✅ 测试完成")
    
    asyncio.run(test())
