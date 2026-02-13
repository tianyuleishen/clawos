#!/usr/bin/env python3
# 🦞 ClawOS 安装验证

"""
验证ClawOS是否正确安装
"""

import sys
import subprocess


def check_python_version():
    """检查Python版本"""
    print("📋 检查Python版本...")
    if sys.version_info < (3, 10):
        print("  ❌ 需要Python 3.10+")
        return False
    print(f"  ✅ Python {sys.version_info.major}.{sys.version_info.minor}")
    return True


def check_imports():
    """检查关键依赖"""
    print("\n📦 检查依赖...")
    
    deps = [
        ('rich', 'Rich控制台'),
        ('click', '命令行'),
        ('pydantic', '数据验证'),
        ('fastapi', 'Web框架'),
    ]
    
    all_ok = True
    for module, desc in deps:
        try:
            __import__(module)
            print(f"  ✅ {desc} ({module})")
        except ImportError:
            print(f"  ❌ {desc} ({module}) - 请运行: pip install {module}")
            all_ok = False
    
    return all_ok


def check_clawos():
    """检查ClawOS安装"""
    print("\n🔧 检查ClawOS安装...")
    
    try:
        import clawos
        print(f"  ✅ ClawOS版本: {clawos.__version__}")
        
        # 检查模块
        modules = [
            'UltimateFusionEngine',
            'L11Consciousness',
            'EmotionModule',
            'MouseController',
            'SettingsStorage',
            'OnboardingManager',
        ]
        
        for mod in modules:
            if hasattr(clawos, mod):
                print(f"  ✅ {mod}")
            else:
                print(f"  ⚠️ {mod} (可选)")
        
        return True
        
    except ImportError as e:
        print(f"  ❌ ClawOS导入失败: {e}")
        return False


def test_functionality():
    """测试基本功能"""
    print("\n🧪 测试基本功能...")
    
    try:
        from clawos.onboarding import get_onboarding_manager
        manager = get_onboarding_manager()
        print(f"  ✅ Onboarding模块正常")
        
        from clawos.storage.settings import SettingsStorage
        storage = SettingsStorage()
        print(f"  ✅ Settings存储正常")
        
        return True
        
    except Exception as e:
        print(f"  ❌ 测试失败: {e}")
        return False


def main():
    """主验证函数"""
    print("=" * 60)
    print("🦞 ClawOS 安装验证")
    print("=" * 60)
    
    results = []
    
    # 1. Python版本
    results.append(check_python_version())
    
    # 2. 依赖检查
    results.append(check_imports())
    
    # 3. ClawOS安装
    results.append(check_clawos())
    
    # 4. 功能测试
    results.append(test_functionality())
    
    # 总结
    print("\n" + "=" * 60)
    
    if all(results):
        print("✅ 安装验证全部通过！")
        print("\n下一步:")
        print("  clawos chat          # 进入对话")
        print("  clawos --reconfigure # 配置模型")
        print("  clawos --help        # 查看帮助")
        return 0
    else:
        print("❌ 部分检查未通过")
        print("请安装缺失的依赖后重新运行此脚本")
        return 1


if __name__ == "__main__":
    sys.exit(main())
