#!/usr/bin/env python3
"""
🦞 ClawOS 快速启动菜单
"""

import os
import subprocess

def show_menu():
    print("""
╔════════════════════════════════════════╗
║                                        ║
║   🦞 ClawOS AI操作系统 v2.0           ║
║                                        ║
║   L11 Consciousness: ENABLED ✅       ║
║   Ultimate Fusion: ENABLED ✅         ║
║                                        ║
╚════════════════════════════════════════╝

请选择操作:

1. 📦 安装系统          python install.sh
2. ⚙️ 初始化配置        python clawos/onboarding.py
3. 💻 命令行界面        python clawos/cli.py
4. 🌐 Web界面           python clawos/gui/webgui.py
5. 🖥️ GUI界面           python clawos/gui/clawos_gui.py
6. 📱 飞书集成          python clawos/im/feishu.py
7. 🧪 运行测试          python verify_install.py
8. 📊 查看状态          python clawos_launcher.py status
9. ❌ 帮助              python clawos_launcher.py help

q. 退出
""")

def main():
    show_menu()
    
    while True:
        choice = input("\n请选择 (1-9, q): ").strip().lower()
        
        actions = {
            '1': ('📦 正在安装...', 'bash /home/admin/.openclaw/workspace/install.sh'),
            '2': ('⚙️ 正在初始化...', 'python /home/admin/.openclaw/workspace/clawos/onboarding.py'),
            '3': ('💻 启动命令行界面...', 'python /home/admin/.openclaw/workspace/clawos/cli.py'),
            '4': ('🌐 启动Web界面...', 'python /home/admin/.openclaw/workspace/clawos/gui/webgui.py'),
            '5': ('🖥️ 启动GUI界面...', 'python /home/admin/.openclaw/workspace/clawos/gui/clawos_gui.py'),
            '6': ('📱 启动飞书集成...', 'python /home/admin/.openclaw/workspace/clawos/im/feishu.py'),
            '7': ('🧪 运行测试...', 'python /home/admin/.openclaw/workspace/verify_install.py'),
            '8': ('📊 检查状态...', 'python /home/admin/.openclaw/workspace/clawos_launcher.py status'),
            '9': ('❌ 显示帮助...', 'python /home/admin/.openclaw/workspace/clawos_launcher.py help'),
        }
        
        if choice in actions:
            print(f"\n{actions[choice][0]}")
            os.system(actions[choice][1])
            print("\n" + "="*50)
            show_menu()
        
        elif choice in ['q', 'quit', 'exit']:
            print("\n👋 再见!")
            break
        
        else:
            print("\n❌ 无效选择，请输入 1-9 或 q")

if __name__ == "__main__":
    main()
