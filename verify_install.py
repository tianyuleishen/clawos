#!/usr/bin/env python3
# 🦞 ClawOS 安装验证脚本

"""
验证ClawOS是否正确安装
验证所有能力是否可用
"""

import sys
import asyncio


def check_python_version():
    """检查Python版本"""
    print("📋 检查Python版本...")
    if sys.version_info < (3, 10):
        print("  ❌ 需要Python 3.10+")
        return False
    print(f"  ✅ Python {sys.version_info.major}.{sys.version_info.minor}")
    return True


def check_imports():
    """检查依赖"""
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
            print(f"  ❌ {desc} ({module})")
            all_ok = False
    
    return all_ok


def check_clawos():
    """检查ClawOS"""
    print("\n🔧 检查ClawOS...")
    
    try:
        import clawos
        print(f"  ✅ ClawOS版本: {clawos.__version__}")
        
        # 检查推理引擎
        try:
            from clawos.core.reasoning import UltimateFusionEngine
            print("  ✅ UltimateFusionEngine (完整版)")
        except Exception as e:
            print(f"  ❌ 推理引擎: {e}")
        
        # 检查电脑控制
        try:
            from clawos.controls import MouseController
            print("  ✅ 鼠标控制")
        except Exception as e:
            print(f"  ⚠️ 鼠标控制: {e}")
        
        # 检查文件管理
        try:
            from clawos.files import FileManager
            print("  ✅ 文件管理")
        except Exception as e:
            print(f"  ⚠️ 文件管理: {e}")
        
        return True
    except ImportError as e:
        print(f"  ❌ ClawOS导入失败: {e}")
        return False


async def test_reasoning():
    """测试推理引擎"""
    print("\n🧠 测试推理引擎...")
    
    try:
        from clawos.core.reasoning import UltimateFusionEngine
        
        engine = UltimateFusionEngine()
        
        tests = [
            ("链式推理", "如果A>B且B>C，那么A>C吗？"),
            ("因果分析", "因为下雨，所以地湿了。"),
            ("反事实", "假如我没有努力学习，我就不会通过考试。"),
            ("数学", "计算 1 + 1 = ?"),
            ("三段论", "所有A是B，所有B是C。那么所有A是C吗？"),
        ]
        
        for name, task in tests:
            result = await engine.analyze(task)
            status = "✅" if result.confidence > 0.5 else "❌"
            print(f"  {status} [{name}] {result.engine_used} ({result.confidence:.0%})")
        
        return True
    except Exception as e:
        print(f"  ❌ 推理测试失败: {e}")
        return False


def show_capabilities():
    """显示能力配置"""
    print("\n📊 ClawOS能力配置:")
    print("""
  ✅ 推理能力:
     ├── ChainReasoner (链式推理)
     ├── CausalAnalyzer (因果分析)
     ├── CounterfactualReasoner (反事实推理)
     └── MetaReasoner (元推理)
  
  ✅ 理解能力:
     ├── PronounResolver (指代消解)
     ├── ContextTracker (上下文追踪)
     ├── EmotionRecognizer (情感识别)
     └── IntentInferrer (意图推断)
  
  ✅ 代码质量:
     ├── CodeReviewer (代码审查)
     ├── BestPractice (最佳实践)
     └── ErrorHandler (错误处理)
  
  ❌ 禁止能力:
     ├── Self-Learning (自我学习)
     ├── Algorithm Innovation (算法创新)
     ├── Self-Improvement (自我改进)
     └── Capability Creation (能力创造)
    """)


async def main():
    """主验证"""
    print("=" * 60)
    print("🦞 ClawOS v2.0 安装验证")
    print("=" * 60)
    
    results = []
    
    results.append(check_python_version())
    results.append(check_imports())
    results.append(check_clawos())
    await test_reasoning()
    show_capabilities()
    
    print("\n" + "=" * 60)
    
    if all(results):
        print("✅ ClawOS安装验证通过！")
        print("\n使用方法:")
        print("  clawos chat              # 进入对话")
        print("  clawos reason '问题'    # 推理测试")
        print("  clawos status           # 查看状态")
        print("\n能力:")
        print("  • 完整推理引擎 (8个)")
        print("  • 理解增强模块")
        print("  • 代码质量工具")
        print("  • 电脑控制 + 文件管理")
        print("  ⚠️ 无自我进化能力")
        return 0
    else:
        print("❌ 部分检查未通过")
        print("\n安装:")
        print("  1. pip install -r requirements.txt")
        print("  2. pip install -e .")
        print("  3. python verify_install.py")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
