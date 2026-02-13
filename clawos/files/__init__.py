# 🦞 ClawOS Files - 文件管理模块

"""
文件管理模块 - 文件、目录、搜索、批量操作

功能:
- File Manager (文件读写)
- Directory Manager (目录管理)
- File Searcher (文件搜索)
- Batch Operations (批量操作)
"""

from .file import FileManager, FileInfo, FileType
from .directory import DirectoryManager, DirectoryEntry, SortOrder, ListMode
from .search import FileSearcher, SearchResult, SearchOptions, SearchMode, SearchScope
from .batch import BatchOperations, BatchOperation, OperationType, OperationResult

__all__ = [
    # 文件管理
    'FileManager',
    'FileInfo',
    'FileType',
    
    # 目录管理
    'DirectoryManager',
    'DirectoryEntry',
    'SortOrder',
    'ListMode',
    
    # 文件搜索
    'FileSearcher',
    'SearchResult',
    'SearchOptions',
    'SearchMode',
    'SearchScope',
    
    # 批量操作
    'BatchOperations',
    'BatchOperation',
    'OperationType',
    'OperationResult',
]
