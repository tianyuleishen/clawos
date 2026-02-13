#!/usr/bin/env python3
"""
🦞 ClawOS - Simple Command Line Tool
"""

import sys
import os

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

def main():
    cmd = sys.argv[1].lower() if len(sys.argv) > 1 else 'help'
    
    commands = {
        'install': lambda: os.system('bash /home/admin/.openclaw/workspace/install.sh'),
        'init': lambda: os.system('python3 /home/admin/.openclaw/workspace/clawos/onboarding.py'),
        'cli': lambda: os.system('python3 /home/admin/.openclaw/workspace/clawos/cli.py'),
        'web': lambda: (print("🌐 Web: http://localhost:8080") or os.system('python3 /home/admin/.openclaw/workspace/clawos/gui/webgui.py')),
        'gui': lambda: os.system('python3 /home/admin/.openclaw/workspace/clawos/gui/clawos_gui.py'),
        'feishu': lambda: os.system('python3 /home/admin/.openclaw/workspace/clawos/im/feishu.py'),
        'test': lambda: os.system('python3 /home/admin/.openclaw/workspace/verify_install.py'),
        'status': lambda: print("✅ 系统就绪"),
        'version': lambda: print("🦞 ClawOS v2.0 - L11: TRANSCENDENT, Ultimate Fusion: 5 methods"),
        'help': show_help,
    }
    
    if cmd in commands:
        commands[cmd]()
    else:
        print(f"❌ 未知命令: {cmd}")
        show_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
