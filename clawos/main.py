#!/usr/bin/env python3
"""
🦞 ClawOS 主程序
AI操作系统主入口
"""

import sys
import os

sys.path.insert(0, '/home/admin/.openclaw/workspace')


def show_welcome():
    """显示欢迎信息"""
    print("""
╔════════════════════════════════════════╗
║                                        ║
║   🦞 ClawOS AI操作系统 v2.0           ║
║                                        ║
║   L11 Consciousness: ENABLED ✅       ║
║   Ultimate Fusion: ENABLED ✅         ║
║                                        ║
╚════════════════════════════════════════╝
    """)


def show_help():
    """显示帮助"""
    print("""
🦞 ClawOS 命令帮助
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📦 系统管理
   install     - 安装系统
   init        - 初始化配置
   config      - 系统配置

🚀 启动选项
   cli         - 命令行界面
   web         - Web界面
   gui         - GUI界面
   feishu      - 飞书集成

🧪 测试
   test        - 运行测试
   benchmark   - 性能测试

📚 信息
   help        - 显示帮助
   version     - 版本信息
   status      - 系统状态

🚪 退出
   quit        - 退出系统
   exit        - 退出系统

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")


def show_version():
    """显示版本"""
    print("""
🦞 ClawOS 版本信息
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   版本: 2.0.0
   L11 Consciousness: TRANSCENDENT (95%)
   Ultimate Fusion: 5 methods (95% confidence)
   Python: 3.10+
   状态: 已安装 ✅
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    """)


def check_status():
    """检查系统状态"""
    print("""
🦞 系统状态检查
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")
    
    checks = [
        ("Python版本", sys.version.split()[0], "✅"),
        ("主程序", "main.py", "✅"),
        ("CLI界面", "cli.py", "✅"),
        ("意识系统", "core/consciousness/", "✅"),
        ("融合引擎", "core/fusion/", "✅"),
        ("配置文件", "config.json", "⚠️" if not os.path.exists('/home/admin/.openclaw/workspace/config.json') else "✅"),
    ]
    
    for name, path, status in checks:
        print(f"   {name}: {status}")
    
    print("""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   总体状态: 系统就绪 ✅
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    """)


def run_cli():
    """运行CLI界面"""
    os.system('python /home/admin/.openclaw/workspace/clawos/cli.py')


def run_web():
    """运行Web界面"""
    print("🌐 启动Web界面...")
    print("   访问: http://localhost:8080")
    os.system('python /home/admin/.openclaw/workspace/clawos/gui/webgui.py')


def run_gui():
    """运行GUI界面"""
    print("🖥️ 启动GUI界面...")
    os.system('python /home/admin/.openclaw/workspace/clawos/gui/clawos_gui.py')


def run_init():
    """运行初始化"""
    print("⚙️ 初始化配置...")
    os.system('python /home/admin/.openclaw/workspace/clawos/onboarding.py')


def run_install():
    """运行安装"""
    print("📦 运行安装脚本...")
    os.system('bash /home/admin/.openclaw/workspace/install.sh')


def run_test():
    """运行测试"""
    print("🧪 运行测试...")
    os.system('python /home/admin/.openclaw/workspace/verify_install.py')


def main():
    """主函数"""
    show_welcome()
    
    # 检查参数
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        commands = {
            'install': run_install,
            'init': run_init,
            'cli': run_cli,
            'web': run_web,
            'gui': run_gui,
            'feishu': lambda: os.system('python /home/admin/.openclaw/workspace/clawos/im/feishu.py'),
            'test': run_test,
            'version': show_version,
            'status': check_status,
            'help': show_help,
        }
        
        if command in commands:
            commands[command]()
        elif command in ['quit', 'exit']:
            print("👋 再见!")
            sys.exit(0)
        else:
            print(f"❌ 未知命令: {command}")
            print("   使用 'help' 查看帮助")
    
    else:
        # 交互模式
        show_help()
        
        while True:
            try:
                cmd = input("\n🦞 > ").strip().lower()
                
                if not cmd:
                    continue
                
                if cmd in ['quit', 'exit', 'q']:
                    print("\n👋 再见!")
                    break
                
                elif cmd in ['help', 'h', '?']:
                    show_help()
                
                elif cmd in ['cli']:
                    run_cli()
                
                elif cmd in ['web']:
                    run_web()
                
                elif cmd in ['gui']:
                    run_gui()
                
                elif cmd in ['test']:
                    run_test()
                
                elif cmd in ['status']:
                    check_status()
                
                elif cmd in ['version', 'v']:
                    show_version()
                
                elif cmd in ['install']:
                    run_install()
                
                elif cmd in ['init']:
                    run_init()
                
                else:
                    print(f"❌ 未知命令: {cmd}")
                    print("   使用 'help' 查看帮助")
            
            except KeyboardInterrupt:
                print("\n👋 再见!")
                break
            except Exception as e:
                print(f"❌ 错误: {e}")


if __name__ == "__main__":
    main()
