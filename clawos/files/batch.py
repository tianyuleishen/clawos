# 🦞 Batch Operations - 批量操作
import fnmatch

"""
批量操作 - 文件和目录的批量处理

功能:
- 批量重命名
- 批量移动/复制
- 批量删除
- 批量压缩/解压
- 批量文本处理
"""

import asyncio
import os
import shutil
import zipfile
import tarfile
import gzip
import re
from pathlib import Path
from typing import List, Optional, Dict, Any, Callable, Union
from dataclasses import dataclass
from enum import Enum
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import multiprocessing

class OperationType(Enum):
    """操作类型"""
    COPY = "copy"
    MOVE = "move"
    DELETE = "delete"
    RENAME = "rename"
    COMPRESS = "compress"
    EXTRACT = "extract"
    REPLACE = "replace"

@dataclass
class BatchOperation:
    """批量操作配置"""
    type: OperationType
    source_patterns: List[str] = None
    source_dir: str = ""
    target_dir: str = ""
    recursive: bool = True
    
    # 重命名选项
    rename_pattern: str = ""
    rename_template: str = ""
    
    # 压缩选项
    archive_format: str = "zip"  # zip, tar, gz
    
    # 文本选项
    find_text: str = ""
    replace_text: str = ""
    encoding: str = "utf-8"
    
    # 过滤选项
    extensions: List[str] = None
    exclude_patterns: List[str] = None
    min_size: int = None
    max_size: int = None
    
    # 预览/执行
    dry_run: bool = True
    overwrite: bool = False
    
    # 并行
    parallel: bool = True
    max_workers: int = None

@dataclass
class OperationResult:
    """操作结果"""
    operation: OperationType
    total_files: int
    success_files: int
    failed_files: int
    total_size: int
    errors: List[Dict]
    details: List[Dict] = None

@dataclass
class RenamePreview:
    """重命名预览"""
    original: str
    new: str
    status: str  # "ok", "conflict", "error"


class BatchOperations:
    """批量操作管理器"""
    
    def __init__(self):
        self.executor = ThreadPoolExecutor(
            max_workers=multiprocessing.cpu_count()
        )
        print("✅ Batch Operations 已加载")
    
    # ============ 批量重命名 ============
    
    async def preview_rename(
        self,
        dir_path: str,
        pattern: str,
        template: str,
        extensions: List[str] = None,
        recursive: bool = True
    ) -> List[RenamePreview]:
        """预览重命名
        
        Args:
            dir_path: 目录路径
            pattern: 原文件名匹配模式
            template: 新文件名模板
            extensions: 文件扩展名
            recursive: 是否递归
        
        Returns:
            List[RenamePreview]: 预览列表
        """
        loop = asyncio.get_event_loop()
        
        def _preview():
            path = Path(dir_path)
            previews = []
            
            if recursive:
                iterator = path.rglob("*")
            else:
                iterator = path.glob("*")
            
            for item in iterator:
                if not item.is_file():
                    continue
                
                if extensions:
                    if item.suffix.lower() not in [e.lower() for e in extensions]:
                        continue
                
                if fnmatch.fnmatch(item.name, pattern):
                    # 生成新名称
                    new_name = self._apply_template(item.name, pattern, template)
                    new_path = item.parent / new_name
                    
                    status = "ok"
                    if new_path.exists() and new_path != item:
                        status = "conflict"
                    
                    previews.append(RenamePreview(
                        original=str(item.absolute()),
                        new=str(new_path.absolute()),
                        status=status
                    ))
            
            return previews
        
        return await loop.run_in_executor(None, _preview)
    
    async def rename(
        self,
        dir_path: str,
        pattern: str,
        template: str,
        extensions: List[str] = None,
        recursive: bool = True,
        dry_run: bool = True
    ) -> OperationResult:
        """执行批量重命名
        
        Args:
            dir_path: 目录路径
            pattern: 原文件名匹配模式
            template: 新文件名模板
            extensions: 文件扩展名
            recursive: 是否递归
            dry_run: 试运行
        
        Returns:
            OperationResult: 操作结果
        """
        # 先预览
        previews = await self.preview_rename(
            dir_path, pattern, template, extensions, recursive
        )
        
        # 过滤冲突
        valid_previews = [p for p in previews if p.status == "ok"]
        
        if dry_run:
            return OperationResult(
                type=OperationType.RENAME,
                total_files=len(previews),
                success_files=len(valid_previews),
                failed_files=len(previews) - len(valid_previews),
                total_size=0,
                errors=[],
                details=[{"original": p.original, "new": p.new} for p in previews]
            )
        
        # 执行
        loop = asyncio.get_event_loop()
        errors = []
        
        def _rename():
            for preview in valid_previews:
                try:
                    Path(preview.original).rename(preview.new)
                except Exception as e:
                    errors.append({
                        "file": preview.original,
                        "error": str(e)
                    })
        
        await loop.run_in_executor(None, _rename)
        
        return OperationResult(
            type=OperationType.RENAME,
            total_files=len(previews),
            success_files=len(valid_previews) - len(errors),
            failed_files=len(errors),
            total_size=0,
            errors=errors
        )
    
    def _apply_template(self, filename: str, pattern: str, template: str) -> str:
        """应用模板"""
        # 提取匹配组
        match = re.match(fnmatch.translate(pattern), filename)
        
        if not match:
            return filename
        
        groups = match.groups()
        
        # 替换模板中的占位符
        result = template
        for i, group in enumerate(groups, 1):
            result = result.replace(f"{{{i}}}", str(group))
            result = result.replace(f"${{{i}}}", str(group))
        
        # 保留扩展名
        path = Path(filename)
        if path.suffix and not result.endswith(path.suffix):
            result += path.suffix
        
        return result
    
    # ============ 批量移动/复制 ============
    
    async def batch_move(
        self,
        source_patterns: List[str],
        target_dir: str,
        dry_run: bool = True
    ) -> OperationResult:
        """批量移动文件
        
        Args:
            source_patterns: 源文件模式列表
            target_dir: 目标目录
            dry_run: 试运行
        
        Returns:
            OperationResult: 操作结果
        """
        # 收集文件
        files = []
        for pattern in source_patterns:
            path = Path(pattern)
            if path.exists():
                if path.is_file():
                    files.append(str(path.absolute()))
                elif path.is_dir():
                    for item in Path(path).rglob("*"):
                        if item.is_file():
                            files.append(str(item.absolute()))
        
        return await self._batch_move_files(files, target_dir, dry_run)
    
    async def batch_copy(
        self,
        source_patterns: List[str],
        target_dir: str,
        overwrite: bool = False,
        dry_run: bool = True
    ) -> OperationResult:
        """批量复制文件
        
        Args:
            source_patterns: 源文件模式列表
            target_dir: 目标目录
            overwrite: 是否覆盖
            dry_run: 试运行
        
        Returns:
            OperationResult: 操作结果
        """
        files = []
        for pattern in source_patterns:
            path = Path(pattern)
            if path.exists():
                if path.is_file():
                    files.append(str(path.absolute()))
        
        return await self._batch_copy_files(files, target_dir, overwrite, dry_run)
    
    async def _batch_move_files(
        self,
        files: List[str],
        target_dir: str,
        dry_run: bool = True
    ) -> OperationResult:
        """内部批量移动"""
        loop = asyncio.get_event_loop()
        errors = []
        total_size = 0
        
        def _move():
            Path(target_dir).mkdir(parents=True, exist_ok=True)
            
            success = 0
            for src in files:
                try:
                    dst = str(Path(target_dir) / Path(src).name)
                    size = Path(src).stat().st_size
                    total_size += size
                    
                    if not dry_run:
                        shutil.move(src, dst)
                    
                    success += 1
                except Exception as e:
                    errors.append({"file": src, "error": str(e)})
            
            return success
        
        success = await loop.run_in_executor(None, _move)
        
        return OperationResult(
            type=OperationType.MOVE,
            total_files=len(files),
            success_files=success,
            failed_files=len(files) - success,
            total_size=total_size,
            errors=errors
        )
    
    async def _batch_copy_files(
        self,
        files: List[str],
        target_dir: str,
        overwrite: bool,
        dry_run: bool
    ) -> OperationResult:
        """内部批量复制"""
        loop = asyncio.get_event_loop()
        errors = []
        total_size = 0
        
        def _copy():
            Path(target_dir).mkdir(parents=True, exist_ok=True)
            
            success = 0
            for src in files:
                try:
                    dst = str(Path(target_dir) / Path(src).name)
                    size = Path(src).stat().st_size
                    total_size += size
                    
                    if not dry_run:
                        if overwrite or not Path(dst).exists():
                            shutil.copy2(src, dst)
                    
                    success += 1
                except Exception as e:
                    errors.append({"file": src, "error": str(e)})
            
            return success
        
        success = await loop.run_in_executor(None, _copy)
        
        return OperationResult(
            type=OperationType.COPY,
            total_files=len(files),
            success_files=success,
            failed_files=len(files) - success,
            total_size=total_size,
            errors=errors
        )
    
    # ============ 批量删除 ============
    
    async def batch_delete(
        self,
        source_patterns: List[str],
        recursive: bool = True,
        dry_run: bool = True
    ) -> OperationResult:
        """批量删除文件
        
        Args:
            source_patterns: 源文件模式列表
            recursive: 是否递归
            dry_run: 试运行
        
        Returns:
            OperationResult: 操作结果
        """
        files = []
        for pattern in source_patterns:
            path = Path(pattern)
            if path.exists():
                if path.is_file():
                    files.append(str(path.absolute()))
                elif path.is_dir() and recursive:
                    for item in Path(path).rglob("*"):
                        if item.is_file():
                            files.append(str(item.absolute()))
        
        loop = asyncio.get_event_loop()
        errors = []
        total_size = 0
        
        def _delete():
            success = 0
            for src in files:
                try:
                    total_size += Path(src).stat().st_size
                    
                    if not dry_run:
                        Path(src).unlink()
                    
                    success += 1
                except Exception as e:
                    errors.append({"file": src, "error": str(e)})
            
            return success
        
        success = await loop.run_in_executor(None, _delete)
        
        return OperationResult(
            type=OperationType.DELETE,
            total_files=len(files),
            success_files=success,
            failed_files=len(files) - success,
            total_size=total_size,
            errors=errors
        )
    
    # ============ 批量压缩/解压 ============
    
    async def compress(
        self,
        source_path: str,
        archive_path: str,
        format: str = "zip",
        base_dir: str = None,
        dry_run: bool = True
    ) -> OperationResult:
        """压缩文件/目录
        
        Args:
            source_path: 源路径
            archive_path: 压缩包路径
            format: 压缩格式
            base_dir: 基础目录
            dry_run: 试运行
        
        Returns:
            OperationResult: 操作结果
        """
        loop = asyncio.get_event_loop()
        
        def _compress():
            if dry_run:
                return OperationResult(
                    type=OperationType.COMPRESS,
                    total_files=1,
                    success_files=1,
                    failed_files=0,
                    total_size=0,
                    errors=[]
                )
            
            if format == "zip":
                with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zf:
                    if Path(source_path).is_dir():
                        for root, dirs, files in os.walk(source_path):
                            for file in files:
                                file_path = os.path.join(root, file)
                                arcname = os.path.relpath(file_path, base_dir or source_path)
                                zf.write(file_path, arcname)
                    else:
                        zf.write(source_path, Path(source_path).name)
            
            elif format == "tar":
                with tarfile.open(archive_path, 'w') as tf:
                    if Path(source_path).is_dir():
                        for root, dirs, files in os.walk(source_path):
                            for file in files:
                                file_path = os.path.join(root, file)
                                arcname = os.path.relpath(file_path, base_dir or source_path)
                                tf.add(file_path, arcname)
                    else:
                        tf.add(source_path, Path(source_path).name)
            
            elif format == "gz":
                # 单文件 gzip
                with open(source_path, 'rb') as f_in:
                    with gzip.open(archive_path, 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
            
            return OperationResult(
                type=OperationType.COMPRESS,
                total_files=1,
                success_files=1,
                failed_files=0,
                total_size=0,
                errors=[]
            )
        
        return await loop.run_in_executor(None, _compress)
    
    async def extract(
        self,
        archive_path: str,
        target_dir: str = None,
        format: str = None,
        dry_run: bool = True
    ) -> OperationResult:
        """解压文件
        
        Args:
            archive_path: 压缩包路径
            target_dir: 目标目录
            format: 压缩格式 (自动检测)
            dry_run: 试运行
        
        Returns:
            OperationResult: 操作结果
        """
        loop = asyncio.get_event_loop()
        
        def _extract():
            path = Path(archive_path)
            
            if target_dir is None:
                target_dir = str(path.parent / path.stem)
            
            if dry_run:
                return OperationResult(
                    type=OperationType.EXTRACT,
                    total_files=1,
                    success_files=1,
                    failed_files=0,
                    total_size=0,
                    errors=[]
                )
            
            # 自动检测格式
            if format is None:
                if archive_path.endswith('.zip'):
                    format = 'zip'
                elif archive_path.endswith(('.tar.gz', '.tgz')):
                    format = 'tar'
                elif archive_path.endswith('.gz'):
                    format = 'gz'
            
            if format == "zip":
                with zipfile.ZipFile(archive_path, 'r') as zf:
                    zf.extractall(target_dir)
            
            elif format == "tar":
                with tarfile.open(archive_path, 'r') as tf:
                    tf.extractall(target_dir)
            
            elif format == "gz":
                with gzip.open(archive_path, 'rb') as gz:
                    with open(target_dir, 'wb') as f:
                        shutil.copyfileobj(gz, f)
            
            return OperationResult(
                type=OperationType.EXTRACT,
                total_files=1,
                success_files=1,
                failed_files=0,
                total_size=0,
                errors=[]
            )
        
        return await loop.run_in_executor(None, _extract)
    
    # ============ 批量文本处理 ============
    
    async def batch_replace(
        self,
        dir_path: str,
        find_text: str,
        replace_text: str,
        extensions: List[str] = None,
        recursive: bool = True,
        encoding: str = "utf-8",
        dry_run: bool = True
    ) -> OperationResult:
        """批量文本替换
        
        Args:
            dir_path: 目录路径
            find_text: 查找文本
            replace_text: 替换文本
            extensions: 文件扩展名
            recursive: 是否递归
            encoding: 编码
            dry_run: 试运行
        
        Returns:
            OperationResult: 操作结果
        """
        loop = asyncio.get_event_loop()
        
        def _replace():
            path = Path(dir_path)
            files = []
            
            if recursive:
                iterator = path.rglob("*")
            else:
                iterator = path.glob("*")
            
            for item in iterator:
                if item.is_file():
                    if extensions:
                        if item.suffix.lower() in [e.lower() for e in extensions]:
                            files.append(str(item.absolute()))
                    else:
                        files.append(str(item.absolute()))
            
            errors = []
            total_changes = 0
            
            for file_path in files:
                try:
                    with open(file_path, 'r', encoding=encoding) as f:
                        content = f.read()
                    
                    count = content.count(find_text)
                    
                    if count > 0:
                        if not dry_run:
                            new_content = content.replace(find_text, replace_text)
                            with open(file_path, 'w', encoding=encoding) as f:
                                f.write(new_content)
                        
                        total_changes += count
                
                except Exception as e:
                    errors.append({"file": file_path, "error": str(e)})
            
            return OperationResult(
                type=OperationType.REPLACE,
                total_files=len(files),
                success_files=len(files) - len(errors),
                failed_files=len(errors),
                total_size=total_changes,
                errors=errors
            )
        
        return await loop.run_in_executor(None, _replace)
    
    # ============ 批量处理 ============
    
    async def process_directory(
        self,
        dir_path: str,
        operation: Callable,
        extensions: List[str] = None,
        recursive: bool = True,
        parallel: bool = True
    ) -> Dict:
        """自定义批量处理
        
        Args:
            dir_path: 目录路径
            operation: 处理函数
            extensions: 文件扩展名
            recursive: 是否递归
            parallel: 是否并行
        
        Returns:
            Dict: 处理结果
        """
        path = Path(dir_path)
        files = []
        
        if recursive:
            iterator = path.rglob("*")
        else:
            iterator = path.glob("*")
        
        for item in iterator:
            if item.is_file():
                if extensions:
                    if item.suffix.lower() in [e.lower() for e in extensions]:
                        files.append(str(item.absolute()))
                else:
                    files.append(str(item.absolute()))
        
        if parallel:
            loop = asyncio.get_event_loop()
            
            tasks = [operation(f) for f in files]
            results = await asyncio.gather(*tasks)
            
            return {
                "total": len(files),
                "results": results
            }
        else:
            results = []
            for file_path in files:
                result = await operation(file_path)
                results.append(result)
            
            return {
                "total": len(files),
                "results": results
            }


# 便捷函数
async def batch_rename(dir_path: str, pattern: str, template: str):
    """批量重命名"""
    ops = BatchOperations()
    return await ops.rename(dir_path, pattern, template)

async def batch_delete(files: List[str]):
    """批量删除"""
    ops = BatchOperations()
    return await ops.batch_delete(files)

# 测试代码
if __name__ == "__main__":
    async def test():
        print("📦 批量操作测试")
        
        ops = BatchOperations()
        
        # 测试重命名预览
        print("\n1. 测试重命名预览...")
        previews = await ops.preview_rename(
            "/tmp", "*.txt", "backup_{1}"
        )
        print(f"   预览 {len(previews)} 个文件")
        
        print("\n✅ 测试完成")
    
    asyncio.run(test())
