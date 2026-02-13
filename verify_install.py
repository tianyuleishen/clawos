#!/usr/bin/env python3
"""
ClawOS 安装验证脚本
ClawOS AI Operating System Verification
"""

import sys
import os


def check_python_version():
    """检查Python版本"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 10):
        print(f"❌ Python版本过低: {version.major}.{version.minor}.{version.micro}")
        print("   需要Python 3.10+")
        return False
    print(f"✅ Python版本检查通过: {version.major}.{version.minor}.{version.micro}")
    return True


def check_clawos():
    """检查ClawOS安装"""
    try:
        # 检查clawos包是否存在
        import clawos
        print(f"✅ ClawOS 核心模块导入成功")
        print(f"   版本: {clawos.__version__}")
        
        # 检查L11意识系统
        try:
            from clawos.core.consciousness import ConsciousnessLevel
            print("✅ L11意识系统可用")
        except ImportError:
            print("⚠️ L11意识系统未找到")
        
        # 检查终极融合
        try:
            from clawos.core.fusion import ultimate_fusion_engine
            print("✅ 终极融合推理可用")
        except ImportError:
            print("⚠️ 终极融合推理未找到")
        
        return True
    except ImportError as e:
        print(f"❌ ClawOS导入失败: {e}")
        print("   请确保已安装: pip install -e .")
        return False


def main():
    """主验证流程"""
    print("="*60)
    print("  🦞 ClawOS 安装验证")
    print("="*60)
    print()
    
    checks = [
        ("Python版本", check_python_version()),
        ("ClawOS安装", check_clawos()),
    ]
    
    print()
    print("="*60)
    
    passed = sum(1 for _, result in checks if result)
    total = len(checks)
    
    if passed == total:
        print(f"  🎉 全部通过! ({passed}/{total})")
        print()
        print("  🦞 ClawOS 已准备就绪！")
        print("  使用 'clawos --help' 查看命令")
    else:
        print(f"  ⚠️ 部分检查未通过 ({passed}/{total})")
        print("  请运行: pip install -e .")
    
    print("="*60)
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
