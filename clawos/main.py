# 🦞 ClawOS - AI操作系统
# 主入口文件

"""
ClawOS AI操作系统 - 主入口

功能:
- 世界级推理引擎
- L11意识系统
- 情感交互
- 电脑控制
- 首次引导配置
"""

import sys
import asyncio
from pathlib import Path

# 版本信息
__version__ = "1.0.0"
__author__ = "ClawOS Team"

# 导入核心模块
from .cli import main

def check_python_version():
    """检查Python版本"""
    if sys.version_info < (3, 10):
        print("❌ 错误: ClawOS需要Python 3.10+")
        print(f"当前版本: {sys.version}")
        sys.exit(1)
    print(f"✅ Python版本检查通过: {sys.version}")

def check_dependencies():
    """检查依赖"""
    try:
        import rich
        import click
        import pydantic
        import fastapi
        print("✅ 核心依赖检查通过")
    except ImportError as e:
        print(f"⚠️ 缺少依赖: {e}")
        print("请运行: pip install -r requirements.txt")

async def run_interactive():
    """运行交互模式"""
    from .onboarding import get_onboarding_manager
    
    # 检查首次运行
    onboarding = get_onboarding_manager()
    
    if onboarding.is_first_run():
        print("""
🦞 ClawOS AI操作系统 v1.0.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        """)
        print("👋 欢迎使用 ClawOS！")
        print("📝 首次运行需要进行一些基本配置...")
        
        await onboarding.run_onboarding()
        
        print("\n🚀 启动主界面...")
    else:
        status = onboarding.get_status()
        model_info = f" [{status.get('model', 'Unknown')}]" if status.get('model') else ""
        
        print(f"""
🦞 ClawOS AI操作系统 v1.0.0{model_info}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
输入"help"获取帮助
输入"quit"退出
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        """)
    
    while True:
        try:
            user_input = input("🦞 > ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit', '退出']:
                print("👋 再见！感谢使用ClawOS！")
                break
            
            if user_input.lower() in ['help', '帮助']:
                print("""
🦞 ClawOS 帮助

命令:
  help     - 显示帮助
  quit     - 退出
  chat     - 进入对话模式
  analyze  - 分析问题
  reason   - 逻辑推理
  control  - 电脑控制
  status   - 系统状态
  version  - 版本信息
  reconfigure - 重新配置模型
                """)
                continue
            
            if user_input.lower() == 'reconfigure':
                await onboarding.reconfigure()
                continue
            
            # 默认使用推理引擎
            from .core.reasoning import UltimateFusionEngine
            engine = UltimateFusionEngine()
            result = await engine.analyze(user_input)
            
            print(f"\n📊 结果: {result}")
            print(f"🤖 ClawOS > ", end="")
            
        except KeyboardInterrupt:
            print("\n👋 再见！")
            break
        except Exception as e:
            print(f"❌ 错误: {e}")

def main_entry():
    """主入口"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="🦞 ClawOS AI操作系统",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  clawos chat              # 进入对话模式
  clawos analyze "问题"    # 分析问题
  clawos reason "推理题"   # 逻辑推理
  clawos status           # 查看系统状态
  clawos --reconfigure    # 重新配置模型
  clawos --version        # 版本信息
        """
    )
    
    parser.add_argument(
        '--version', 
        action='version',
        version=f'🦞 ClawOS v{__version__}'
    )
    
    parser.add_argument(
        '--reconfigure',
        action='store_true',
        help='重新配置模型和设置'
    )
    
    parser.add_argument(
        'command',
        nargs='?',
        default='chat',
        help='命令: chat, analyze, reason, status'
    )
    
    parser.add_argument(
        'args',
        nargs='*',
        help='命令参数'
    )
    
    args = parser.parse_args()
    
    # 版本检查
    check_python_version()
    check_dependencies()
    
    # 重新配置
    if args.reconfigure:
        from .onboarding import get_onboarding_manager
        onboarding = get_onboarding_manager()
        asyncio.run(onboarding.reconfigure())
        return
    
    # 执行命令
    if args.command == 'chat':
        asyncio.run(run_interactive())
    elif args.command == 'analyze':
        if args.args:
            from .core.reasoning import UltimateFusionEngine
            engine = UltimateFusionEngine()
            result = asyncio.run(engine.analyze(' '.join(args.args)))
            print(f"\n📊 分析结果: {result}")
        else:
            print("❌ 请指定要分析的问题")
    elif args.command == 'reason':
        if args.args:
            from .core.reasoning import UltimateFusionEngine
            engine = UltimateFusionEngine()
            result = asyncio.run(engine.analyze(' '.join(args.args)))
            print(f"\n🔍 推理结果: {result}")
        else:
            print("❌ 请指定推理问题")
    elif args.command == 'status':
        from .onboarding import get_onboarding_manager
        onboarding = get_onboarding_manager()
        status = onboarding.get_status()
        
        model_info = f"  └── 模型: {status.get('model', '未配置')}\n"
        
        print(f"""
🦞 ClawOS 系统状态
━━━━━━━━━━━━━━━━━━━━━━━━━━
版本: {__version__}
状态: ✅ 正常运行
模型: {status.get('model', '未配置')} {'(🇨🇳 国内)' if status.get('is_cn') else '(🌏 国际)'}
用户: {status.get('user_name', '未设置')}
语言: {status.get('language', 'zh')}
主题: {status.get('theme', 'dark')}
━━━━━━━━━━━━━━━━━━━━━━━━━━
        """)
    else:
        print(f"❌ 未知命令: {args.command}")
        print("输入 'clawos --help' 获取帮助")

if __name__ == "__main__":
    main_entry()
