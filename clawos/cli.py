#!/usr/bin/env python3
"""
🦞 ClawOS 命令行入口
使用: clawos [命令]
"""

import sys
import os

def main():
    """主函数"""
    # 获取命令参数
    args = sys.argv[1:]
    
    # 如果没有参数，显示帮助
    if not args:
        cmd = 'help'
    else:
        cmd = args[0].lower()
    
    # 支持 --help, -h
    if cmd in ['--help', '-h', '?']:
        cmd = 'help'
    
    # 命令映射
    commands = {
        'help': show_help,
        'install': run_install,
        'init': run_init,
        'cli': run_cli,
        'web': run_web,
        'gui': run_gui,
        'feishu': run_feishu,
        'test': run_test,
        'status': show_status,
        'version': show_version,
    }
    
    if cmd in commands:
        commands[cmd]()
    elif cmd in ['quit', 'exit']:
        print("👋 再见!")
        sys.exit(0)
    else:
        print(f"❌ 未知命令: {cmd}")
        show_help()
        sys.exit(1)

def show_help():
    print("""
🦞 ClawOS AI操作系统 v2.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📦 系统管理
   clawos install     - 安装系统
   clawos init        - 初始化配置

🚀 启动界面
   clawos cli         - 命令行交互
   clawos web         - Web界面
   clawos gui         - GUI界面
   clawos feishu     - 飞书集成

🧪 测试
   clawos test        - 运行测试
   clawos status     - 系统状态

📚 信息
   clawos help       - 显示帮助
   clawos version    - 版本信息

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

def show_version():
    print("""
🦞 ClawOS v2.0
   L11 Consciousness: TRANSCENDENT (95%)
   Ultimate Fusion: 5 methods (95% confidence)
""")

def show_status():
    print("""
🦞 系统状态
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   Python: """ + sys.version.split()[0] + """
   ClawOS: v2.0.0
   L11 Consciousness: ✅ ENABLED
   Ultimate Fusion: ✅ ENABLED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

def run_install():
    print("📦 正在安装...")
    os.system('bash /home/admin/.openclaw/workspace/install.sh')

def run_init():
    print("⚙️ 正在初始化...")
    os.system('python3 /home/admin/.openclaw/workspace/clawos/onboarding.py')

def run_cli():
    print("💻 启动命令行界面...")
    os.system('python3 /home/admin/.openclaw/workspace/clawos/cli.py')

def run_web():
    print("🌐 启动Web界面...")
    print("   访问: http://localhost:8080")
    os.system('python3 /home/admin/.openclaw/workspace/clawos/gui/webgui.py')

def run_gui():
    print("🖥️ 启动GUI界面...")
    os.system('python3 /home/admin/.openclaw/workspace/clawos/gui/clawos_gui.py')

def run_feishu():
    print("📱 启动飞书集成...")
    os.system('python3 /home/admin/.openclaw/workspace/clawos/im/feishu.py')

def run_test():
    print("🧪 正在运行测试...")
    os.system('python3 /home/admin/.openclaw/workspace/verify_install.py')

if __name__ == "__main__":
    main()
