#!/usr/bin/env python3
# 🦞 ClawOS 安装验证脚本

"""
验证ClawOS是否正确安装

使用方法:
    python verify_install.py
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
    
    # 检查fastapi (可能使用不同的Python版本)
    try:
        import fastapi
        print(f"  ✅ Web框架 (fastapi)")
    except ImportError:
        print(f"  ⚠️ Web框架 (fastapi) - 可选，如需API功能请安装")
    
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
            print("  ✅ 推理引擎 (UltimateFusionEngine)")
        except Exception as e:
            print(f"  ⚠️ 推理引擎: {e}")
        
        try:
            from clawos.core.emotion import EmotionModule
            print("  ✅ 情感系统 (EmotionModule)")
        except Exception as e:
            print(f"  ⚠️ 情感系统: {e}")
        
        try:
            from clawos.core.consciousness import L11Consciousness
            print("  ✅ 意识系统 (L11Consciousness)")
        except Exception as e:
            print(f"  ⚠️ 意识系统: {e}")
        
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
            ("传递性", "如果A>B且B>C，那么A>C吗？"),
            ("因果", "因为下雨，所以地湿了。"),
            ("数学", "计算 1 + 1 = ?"),
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


def check_skills():
    """检查技能安装"""
    print("\n🎯 检查技能...")
    
    skills = [
        ("understanding-enhancement", "理解增强"),
        ("code-quality-enhancement", "代码质量"),
        ("reasoning-depth-enhancement", "推理深度"),
    ]
    
    for skill, desc in skills:
        try:
            __import__(skill.replace('-', '_'))
            print(f"  ✅ {desc} ({skill})")
        except ImportError:
            print(f"  ⚠️ {desc} ({skill}) - 可选技能")


async def main():
    """主验证函数"""
    print("=" * 60)
    print("🦞 ClawOS 安装验证 v2.0")
    print("=" * 60)
    
    results = []
    
    # 1. Python版本
    results.append(check_python_version())
    
    # 2. 依赖检查
    results.append(check_imports())
    
    # 3. ClawOS安装
    results.append(check_clawos())
    
    # 4. 推理测试
    await test_reasoning()
    
    # 5. 技能检查
    check_skills()
    
    # 总结
    print("\n" + "=" * 60)
    
    if all(results):
        print("✅ 安装验证通过！")
        print("\n使用方法:")
        print("  clawos chat              # 进入对话模式")
        print("  clawos reason '问题'     # 测试推理")
        print("  clawos status           # 查看状态")
        print("  clawos --reconfigure    # 重新配置")
        return 0
    else:
        print("❌ 部分检查未通过")
        print("\n安装步骤:")
        print("  1. pip install -r requirements.txt")
        print("  2. pip install -e .")
        print("  3. python verify_install.py")
        return 1


if __name__ == "__main__":
    import asyncio
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
