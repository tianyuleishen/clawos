#!/usr/bin/env python3
"""
IntelliCore 安装验证脚本
Enterprise Intelligent Decision System Verification
"""

import sys


def check_python_version():
    """检查Python版本"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 10):
        print(f"❌ Python版本过低: {version.major}.{version.minor}.{version.micro}")
        print("   需要Python 3.10+")
        return False
    print(f"✅ Python版本检查通过: {version.major}.{version.minor}.{version.micro}")
    return True


def check_dependencies():
    """检查依赖包"""
    required_packages = [
        "fastapi",
        "uvicorn",
        "pydantic",
        "redis",
        "sqlalchemy",
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} 已安装")
        except ImportError:
            missing.append(package)
            print(f"❌ {package} 未安装")
    
    return len(missing) == 0


def check_imports():
    """检查导入"""
    try:
        from intellicore import Core
        print("✅ IntelliCore 核心模块导入成功")
        return True
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        return False


def main():
    """主验证流程"""
    print("="*60)
    print("  IntelliCore 安装验证")
    print("  Enterprise Intelligent Decision System Verification")
    print("="*60)
    print()
    
    checks = [
        ("Python版本", check_python_version()),
        ("依赖包", check_dependencies()),
        ("系统导入", check_imports()),
    ]
    
    print()
    print("="*60)
    
    passed = sum(1 for _, result in checks if result)
    total = len(checks)
    
    if passed == total:
        print(f"  🎉 全部通过! ({passed}/{total})")
        print()
        print("  IntelliCore 已准备就绪！")
    else:
        print(f"  ⚠️ 部分检查未通过 ({passed}/{total})")
        print("  请根据错误信息进行修复")
    
    print("="*60)
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
