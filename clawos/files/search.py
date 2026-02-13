# 🦞 File Search - 文件搜索器

"""
文件搜索器 - 高级文件搜索功能

功能:
- 全文搜索
- 内容搜索
- 正则搜索
- 搜索结果高亮
"""

import asyncio
import re
import fnmatch
from pathlib import Path
from typing import List, Optional, Dict, Any, Pattern, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from concurrent.futures import ThreadPoolExecutor
import multiprocessing

class SearchMode(Enum):
    """搜索模式"""
    NORMAL = "normal"
    REGEX = "regex"
    GLOB = "glob"

class SearchScope(Enum):
    """搜索范围"""
    FILE_NAME = "name"
    FILE_CONTENT = "content"
    BOTH = "both"

class HighlightStyle(Enum):
    """高亮样式"""
    ANSI = "ansi"
    HTML = "html"
    MARKDOWN = "markdown"
    NONE = "none"

@dataclass
class SearchResult:
    """搜索结果"""
    file_path: str
    file_name: str
    line_number: int
    line_content: str
    match_start: int
    match_end: int
    match_text: str
    score: float = 0.0

@dataclass
class SearchOptions:
    """搜索选项"""
    # 基本选项
    patterns: List[str] = field(default_factory=list)
    search_text: str = ""
    search_regex: str = ""
    
    # 范围
    scope: SearchScope = SearchScope.BOTH
    recursive: bool = True
    
    # 文件过滤
    extensions: List[str] = field(default_factory=list)
    exclude_patterns: List[str] = field(default_factory=list)
    
    # 大小过滤
    min_size: int = None
    max_size: int = None
    
    # 日期过滤
    created_after: datetime = None
    created_before: datetime = None
    modified_after: datetime = None
    modified_before: datetime = None
    
    # 内容选项
    case_sensitive: bool = False
    whole_word: bool = False
    multiline: bool = False
    
    # 输出选项
    mode: SearchMode = SearchMode.NORMAL
    highlight: HighlightStyle = HighlightStyle.ANSI
    max_results: int = 1000
    context_lines: int = 0
    
    # 性能
    parallel: bool = True
    max_workers: int = None


class FileSearcher:
    """文件搜索器"""
    
    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=multiprocessing.cpu_count())
        print("✅ File Searcher 已加载")
    
    # ============ 基础搜索 ============
    
    async def search(
        self,
        dir_path: str,
        options: SearchOptions = None
    ) -> List[SearchResult]:
        """搜索文件
        
        Args:
            dir_path: 搜索目录
            options: 搜索选项
        
        Returns:
            List[SearchResult]: 搜索结果
        """
        if options is None:
            options = SearchOptions()
        
        # 获取文件列表
        files = await self._get_files(dir_path, options)
        
        if not files:
            return []
        
        # 搜索文件
        if options.parallel and len(files) > 1:
            results = await self._search_parallel(files, options)
        else:
            results = await self._search_sequential(files, options)
        
        # 限制结果数量
        return results[:options.max_results]
    
    async def search_by_name(
        self,
        dir_path: str,
        pattern: str,
        recursive: bool = True,
        case_sensitive: bool = False
    ) -> List[str]:
        """按名称搜索
        
        Args:
            dir_path: 搜索目录
            pattern: 匹配模式
            recursive: 是否递归
            case_sensitive: 是否大小写敏感
        
        Returns:
            List[str]: 匹配的文件路径列表
        """
        loop = asyncio.get_event_loop()
        
        def _search():
            path = Path(dir_path)
            results = []
            
            if recursive:
                iterator = path.rglob("*")
            else:
                iterator = path.glob("*")
            
            for item in iterator:
                if item.is_file():
                    name = item.name if case_sensitive else item.name.lower()
                    pat = pattern if case_sensitive else pattern.lower()
                    
                    if fnmatch.fnmatch(name, pat) or pat in name:
                        results.append(str(item.absolute()))
            
            return results
        
        return await loop.run_in_executor(None, _search)
    
    async def search_by_content(
        self,
        dir_path: str,
        search_text: str,
        extensions: List[str] = None,
        recursive: bool = True,
        case_sensitive: bool = False
    ) -> List[SearchResult]:
        """按内容搜索
        
        Args:
            dir_path: 搜索目录
            search_text: 搜索文本
            extensions: 文件扩展名
            recursive: 是否递归
            case_sensitive: 是否大小写敏感
        
        Returns:
            List[SearchResult]: 搜索结果
        """
        options = SearchOptions(
            search_text=search_text,
            scope=SearchScope.FILE_CONTENT,
            extensions=extensions or [".txt", ".py", ".md", ".json", ".html", ".css", ".js"],
            recursive=recursive,
            case_sensitive=case_sensitive
        )
        
        return await self.search(dir_path, options)
    
    async def search_regex(
        self,
        dir_path: str,
        regex: str,
        extensions: List[str] = None,
        recursive: bool = True
    ) -> List[SearchResult]:
        """正则搜索
        
        Args:
            dir_path: 搜索目录
            regex: 正则表达式
            extensions: 文件扩展名
            recursive: 是否递归
        
        Returns:
            List[SearchResult]: 搜索结果
        """
        options = SearchOptions(
            search_regex=regex,
            scope=SearchScope.FILE_CONTENT,
            extensions=extensions or [".txt", ".py", ".md", ".json", ".html", ".css", ".js"],
            recursive=recursive,
            mode=SearchMode.REGEX
        )
        
        return await self.search(dir_path, options)
    
    # ============ 高级搜索 ============
    
    async def search_multiple_patterns(
        self,
        dir_path: str,
        patterns: List[str],
        mode: SearchMode = SearchMode.NORMAL
    ) -> Dict[str, List[str]]:
        """多模式搜索
        
        Args:
            dir_path: 搜索目录
            patterns: 模式列表
            mode: 搜索模式
        
        Returns:
            Dict: {模式: [文件列表]}
        """
        loop = asyncio.get_event_loop()
        
        def _search():
            path = Path(dir_path)
            results = {}
            
            for pattern in patterns:
                matches = []
                
                for item in path.rglob("*"):
                    if item.is_file():
                        if mode == SearchMode.GLOB:
                            if fnmatch.fnmatch(item.name, pattern):
                                matches.append(str(item.absolute()))
                        else:  # NORMAL
                            if pattern in item.name:
                                matches.append(str(item.absolute()))
                
                results[pattern] = matches
            
            return results
        
        return await loop.run_in_executor(None, _search)
    
    async def find_duplicates(
        self,
        dir_path: str,
        by_content: bool = False
    ) -> Dict[str, List[str]]:
        """查找重复文件
        
        Args:
            dir_path: 搜索目录
            by_content: 是否按内容比较
        
        Returns:
            Dict: {文件哈希/大小: [文件列表]}
        """
        loop = asyncio.get_event_loop()
        
        def _find():
            path = Path(dir_path)
            groups = {}
            file_map = {}
            
            for item in path.rglob("*"):
                if item.is_file():
                    if by_content:
                        # 按内容哈希
                        key = item.stat().st_size  # 先按大小分组
                    else:
                        key = item.name  # 按名称
                    
                    if key not in file_map:
                        file_map[key] = []
                    file_map[key].append(str(item.absolute()))
            
            # 只保留有多个文件的组
            for key, files in file_map.items():
                if len(files) > 1:
                    groups[key] = files
            
            return groups
        
        return await loop.run_in_executor(None, _find)
    
    async def search_and_replace(
        self,
        dir_path: str,
        search_text: str,
        replace_text: str,
        extensions: List[str] = None,
        recursive: bool = True,
        dry_run: bool = True
    ) -> Dict:
        """搜索并替换
        
        Args:
            dir_path: 搜索目录
            search_text: 搜索文本
            replace_text: 替换文本
            extensions: 文件扩展名
            recursive: 是否递归
            dry_run: 试运行 (不实际修改)
        
        Returns:
            Dict: 操作结果
        """
        results = await self.search_by_content(
            dir_path, search_text, extensions, recursive
        )
        
        modified = []
        skipped = []
        
        # 按文件分组
        file_matches = {}
        for result in results:
            if result.file_path not in file_matches:
                file_matches[result.file_path] = []
            file_matches[result.file_path].append(result)
        
        for file_path, matches in file_matches.items():
            if dry_run:
                modified.append({
                    "file": file_path,
                    "count": len(matches),
                    "would_replace": True
                })
            else:
                try:
                    # 读取文件
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # 替换
                    new_content = content.replace(search_text, replace_text)
                    
                    # 写回
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    
                    modified.append({
                        "file": file_path,
                        "count": len(matches)
                    })
                except Exception as e:
                    skipped.append({
                        "file": file_path,
                        "error": str(e)
                    })
        
        return {
            "total_matches": len(results),
            "files_modified": len(modified),
            "files_skipped": len(skipped),
            "modified": modified,
            "skipped": skipped
        }
    
    # ============ 辅助方法 ============
    
    async def _get_files(self, dir_path: str, options: SearchOptions) -> List[str]:
        """获取搜索文件列表"""
        loop = asyncio.get_event_loop()
        
        def _get():
            path = Path(dir_path)
            files = []
            
            if options.recursive:
                iterator = path.rglob("*")
            else:
                iterator = path.glob("*")
            
            for item in iterator:
                if not item.is_file():
                    continue
                
                # 跳过隐藏文件
                if item.name.startswith('.'):
                    continue
                
                # 扩展名过滤
                if options.extensions:
                    if item.suffix.lower() not in [e.lower() for e in options.extensions]:
                        continue
                
                # 排除模式
                if options.exclude_patterns:
                    skip = False
                    for pattern in options.exclude_patterns:
                        if fnmatch.fnmatch(item.name, pattern):
                            skip = True
                            break
                    if skip:
                        continue
                
                # 大小过滤
                if options.min_size is not None:
                    if item.stat().st_size < options.min_size:
                        continue
                if options.max_size is not None:
                    if item.stat().st_size > options.max_size:
                        continue
                
                files.append(str(item.absolute()))
            
            return files
        
        return await loop.run_in_executor(None, _get)
    
    async def _search_sequential(
        self, 
        files: List[str], 
        options: SearchOptions
    ) -> List[SearchResult]:
        """顺序搜索"""
        results = []
        
        for file_path in files:
            file_results = await self._search_file(file_path, options)
            results.extend(file_results)
        
        return results
    
    async def _search_parallel(
        self, 
        files: List[str], 
        options: SearchOptions
    ) -> List[SearchResult]:
        """并行搜索"""
        loop = asyncio.get_event_loop()
        
        tasks = [
            self._search_file(file_path, options)
            for file_path in files
        ]
        
        all_results = await asyncio.gather(*tasks)
        
        # 合并结果
        results = []
        for file_results in all_results:
            results.extend(file_results)
        
        return results
    
    async def _search_file(
        self, 
        file_path: str, 
        options: SearchOptions
    ) -> List[SearchResult]:
        """搜索单个文件"""
        results = []
        path = Path(file_path)
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
        except Exception:
            return results
        
        for line_num, line in enumerate(lines, 1):
            match = self._find_match(line, options)
            
            if match:
                results.append(SearchResult(
                    file_path=file_path,
                    file_name=path.name,
                    line_number=line_num,
                    line_content=line.rstrip('\n\r'),
                    match_start=match.start(),
                    match_end=match.end(),
                    match_text=match.group()
                ))
        
        return results
    
    def _find_match(self, line: str, options: SearchOptions):
        """在行中查找匹配"""
        text = line
        
        flags = 0
        if not options.case_sensitive:
            flags |= re.IGNORECASE
        
        if options.search_text:
            pattern = re.escape(options.search_text)
            if options.whole_word:
                pattern = r'\b' + pattern + r'\b'
            
            return re.search(pattern, text, flags)
        
        elif options.search_regex:
            return re.search(options.search_regex, text, flags)
        
        elif options.patterns:
            for pattern in options.patterns:
                match = re.search(pattern, text, flags)
                if match:
                    return match
        
        return None
    
    # ============ 输出格式化 ============
    
    def format_result(
        self, 
        result: SearchResult,
        options: SearchOptions
    ) -> str:
        """格式化搜索结果"""
        if options.highlight == HighlightStyle.NONE:
            return f"{result.file_path}:{result.line_number}: {result.line_content}"
        
        elif options.highlight == HighlightStyle.ANSI:
            highlighted = self._highlight_text(
                result.line_content,
                result.match_text,
                options.case_sensitive
            )
            return f"{result.file_path}:{result.line_number}: {highlighted}"
        
        elif options.highlight == HighlightStyle.MARKDOWN:
            return f"`{result.file_path}:{result.line_number}`: {result.line_content}"
        
        return f"{result.file_path}:{result.line_number}: {result.line_content}"
    
    def _highlight_text(
        self, 
        text: str, 
        match_text: str,
        case_sensitive: bool
    ) -> str:
        """高亮文本"""
        # 简单实现
        replacement = f"\033[1;32m{match_text}\033[0m"
        
        if case_sensitive:
            return text.replace(match_text, replacement)
        else:
            return re.sub(
                re.escape(match_text),
                replacement,
                text,
                flags=re.IGNORECASE
            )
    
    def format_results(
        self, 
        results: List[SearchResult],
        options: SearchOptions
    ) -> str:
        """格式化所有搜索结果"""
        if not results:
            return "未找到匹配结果"
        
        lines = [f"找到 {len(results)} 个结果:\n"]
        
        for result in results[:options.max_results]:
            lines.append(self.format_result(result, options))
        
        return "\n".join(lines)


# 便捷函数
async def search_files(dir_path: str, pattern: str) -> List[str]:
    """搜索文件"""
    searcher = FileSearcher()
    return await searcher.search_by_name(dir_path, pattern)

async def search_content(dir_path: str, text: str) -> List[SearchResult]:
    """搜索内容"""
    searcher = FileSearcher()
    return await searcher.search_by_content(dir_path, text)

# 测试代码
if __name__ == "__main__":
    async def test():
        print("🔍 文件搜索器测试")
        
        searcher = FileSearcher()
        
        # 测试按名称搜索
        print("\n1. 测试按名称搜索...")
        files = await searcher.search_by_name(
            "/home/admin/.openclaw/workspace", "*.py"
        )
        print(f"   找到 {len(files)} 个Python文件")
        
        # 测试按内容搜索
        print("\n2. 测试按内容搜索...")
        results = await searcher.search_by_content(
            "/home/admin/.openclaw/workspace", "ClawOS"
        )
        print(f"   找到 {len(results)} 处匹配")
        
        # 打印结果
        for result in results[:5]:
            print(f"   {result.file_path}:{result.line_number}")
        
        print("\n✅ 测试完成")
    
    asyncio.run(test())
