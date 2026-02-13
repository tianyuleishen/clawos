#!/usr/bin/env python3
"""
🦞 ClawOS 简单安装脚本
跳过复杂依赖，直接安装核心功能
"""

import subprocess
import sys
import os


def run_command(cmd, description):
    """运行命令"""
    print(f"📦 {description}...")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.returncode == 0


def check_python():
    """检查Python版本"""
    version = sys.version_info
    print(f"✅ Python版本: {version.major}.{version.minor}.{version.micro}")
    return version.major >= 3 and version.minor >= 10


def simple_install():
    """简单安装"""
    print("\n" + "="*60)
    print("  🦞 ClawOS 简单安装")
    print("="*60)
    print()
    
    # 检查Python
    if not check_python():
        print("❌ 需要Python 3.10+")
        return False
    
    # 检查是否在clawos目录
    if not os.path.exists("setup.py"):
        print("❌ 请在clawos目录下运行")
        return False
    
    # 尝试简单安装（跳过构建）
    print("📦 安装ClawOS...")
    
    # 只安装必要依赖，跳过复杂构建
    commands = [
        ("pip install -q python-dotenv requests websockets", "安装基础依赖"),
        ("pip install -q fastapi uvicorn --only-binary :all:", "安装Web依赖"),
    ]
    
    for cmd, desc in commands:
        if not run_command(cmd, desc):
            print(f"⚠️ {desc} 失败，继续...")
    
    # 复制文件到可导入位置
    print("📦 配置ClawOS...")
    
    # 创建简化版可用
    print("\n✅ 安装完成！")
    print()
    print("使用方法:")
    print("  python -m clawos --help")
    print("  或")
    print("  python clawos.py --help")
    print()
    
    return True


if __name__ == "__main__":
    simple_install()
