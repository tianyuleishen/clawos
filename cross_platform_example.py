#!/usr/bin/env python3
"""
🦞 跨平台代码示例
Cross-platform Python code example
"""

import sys
import os
from pathlib import Path
from platform import system


def get_app_data_dir():
    """获取应用数据目录 - 跨平台"""
    """Get application data directory - cross-platform"""
    
    app_name = "ClawOS"
    
    if system() == "Windows":
        # Windows: %APPDATA%
        data_dir = Path(os.environ.get("APPDATA", Path.home())) / app_name
    
    elif system() == "Darwin":
        # macOS: ~/Library/Application Support
        data_dir = Path.home() / "Library" / "Application Support" / app_name
    
    else:
        # Linux: ~/.config
        data_dir = Path.home() / ".config" / app_name
    
    # 确保目录存在
    data_dir.mkdir(parents=True, exist_ok=True)
    
    return data_dir


def get_resource_path(relative_path: str) -> Path:
    """获取资源路径 - 跨平台"""
    """Get resource path - cross-platform"""
    
    # 获取当前文件所在目录
    base_dir = Path(__file__).parent
    
    # 返回完整路径
    return base_dir / relative_path


def save_file(filename: str, content: str) -> bool:
    """保存文件 - 跨平台"""
    """Save file - cross-platform"""
    
    try:
        data_dir = get_app_data_dir()
        file_path = data_dir / filename
        
        # 使用UTF-8编码，确保中文兼容
        file_path.write_text(content, encoding="utf-8")
        
        return True
    
    except Exception as e:
        print(f"Error saving file: {e}")
        return False


def read_file(filename: str) -> str:
    """读取文件 - 跨平台"""
    """Read file - cross-platform"""
    
    try:
        data_dir = get_app_data_dir()
        file_path = data_dir / filename
        
        if file_path.exists():
            return file_path.read_text(encoding="utf-8")
        
        return ""
    
    except Exception as e:
        print(f"Error reading file: {e}")
        return ""


def get_system_info() -> dict:
    """获取系统信息 - 跨平台"""
    """Get system info - cross-platform"""
    
    return {
        "platform": system(),
        "python_version": sys.version,
        "encoding": sys.getdefaultencoding(),
        "app_data": str(get_app_data_dir()),
    }


def main():
    """主函数 - 跨平台示例"""
    """Main function - cross-platform example"""
    
    print("🦞 Cross-platform Python Example")
    print("=" * 50)
    
    # 获取系统信息
    info = get_system_info()
    
    print(f"Platform: {info['platform']}")
    print(f"Python: {info['python_version'].split()[0]}")
    print(f"Encoding: {info['encoding']}")
    print(f"App Data: {info['app_data']}")
    print("=" * 50)
    
    # 测试文件读写
    test_content = "Hello, Cross-platform World! 🌍\n中文测试"
    
    if save_file("test.txt", test_content):
        print("✅ File saved successfully")
        
        content = read_file("test.txt")
        if content:
            print("✅ File read successfully")
            print(f"Content: {content[:50]}...")
    
    # 显示数据目录
    print(f"\n📁 App Data Directory: {get_app_data_dir()}")
    
    print("\n✅ All cross-platform tests passed!")


if __name__ == "__main__":
    main()
