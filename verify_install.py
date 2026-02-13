#!/usr/bin/env python3
# 🦞 ClawOS 安装验证脚本

"""
验证ClawOS是否正确安装
"""

import sys


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
        
        # 检查核心模块
        try:
            from clawos.cli import main
            print("  ✅ CLI模块")
        except Exception as e:
            print(f"  ⚠️ CLI模块: {e}")
        
        try:
            from clawos.onboarding import get_onboarding_manager
            print("  ✅ Onboarding模块")
        except Exception as e:
            print(f"  ⚠️ Onboarding模块: {e}")
        
        try:
            from clawos.core.reasoning import UltimateFusionEngine
            print("  ✅ 基础推理引擎 (Logic/Math/Reasoning)")
        except Exception as e:
            print(f"  ❌ 推理引擎: {e}")
        
        try:
            from clawos.controls import MouseController
            print("  ✅ 鼠标控制")
        except Exception as e:
            print(f"  ⚠️ 鼠标控制: {e}")
        
        try:
            from clawos.files import FileManager
            print("  ✅ 文件管理")
        except Exception as e:
            print(f"  ⚠️ 文件管理: {e}")
        
        return True
        
    except ImportError as e:
        print(f"  ❌ ClawOS导入失败: {e}")
        print("  请运行: pip install -e .")
        return False


async def test_reasoning():
    """测试推理引擎"""
    print("\n🧠 测试推理引擎...")
    
    try:
        from clawos.core.reasoning import UltimateFusionEngine
        
        tests = [
            ("逻辑", "如果A>B且B>C，那么A>C吗？"),
            ("数学", "计算 1 + 1 = ?"),
            ("通用", "今天天气怎么样？"),
        ]
        
        engine = UltimateFusionEngine()
        
        for name, task in tests:
            result = await engine.analyze(task)
            status = "✅" if result.confidence > 0.5 else "⚠️"
            print(f"  {status} [{name}] {result.engine_used} ({result.confidence:.0%})")
        
        return True
    except Exception as e:
        print(f"  ❌ 推理测试失败: {e}")
        return False


def main():
    """主验证函数"""
    print("=" * 60)
    print("🦞 ClawOS 安装验证 v1.0 (简化版)")
    print("=" * 60)
    
    results = []
    
    # 1. Python版本
    results.append(check_python_version())
    
    # 2. 依赖检查
    results.append(check_imports())
    
    # 3. ClawOS安装
    results.append(check_clawos())
    
    # 4. 推理测试
    import asyncio
    asyncio.run(test_reasoning())
    
    # 总结
    print("\n" + "=" * 60)
    
    if all(results):
        print("✅ ClawOS安装验证通过！")
        print("\n使用说明:")
        print("  clawos chat              # 进入对话模式")
        print("  clawos reason '问题'     # 测试推理")
        print("  clawos status           # 查看状态")
        print("  clawos --reconfigure    # 重新配置")
        print("\n注意: 这是简化版ClawOS")
        print("高级推理能力请使用OpenClaw智能助手")
        return 0
    else:
        print("❌ 部分检查未通过")
        print("\n安装步骤:")
        print("  1. pip install -r requirements.txt")
        print("  2. pip install -e .")
        print("  3. python verify_install.py")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
