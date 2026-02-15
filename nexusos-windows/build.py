#!/usr/bin/env python3
"""
🦞 NexusOS Windows 打包工具
在Windows上运行此脚本生成exe
"""

import os
import sys
import subprocess

def check_requirements():
    """检查依赖"""
    print("🔍 检查依赖...")
    
    # 检查Python
    try:
        v = sys.version_info
        print(f"✅ Python {v.major}.{v.minor}")
    except:
        print("❌ Python未安装")
        return False
    
    # 检查tkinter
    try:
        import tkinter
        print("✅ tkinter已安装")
    except ImportError:
        print("❌ tkinter未安装，请安装Python时勾选tkinter")
        return False
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller {PyInstaller.__version__}")
    except ImportError:
        print("📦 正在安装PyInstaller...")
        os.system("pip install pyinstaller")
        try:
            import PyInstaller
            print(f"✅ PyInstaller {PyInstaller.__version__}")
        except:
            print("❌ PyInstaller安装失败")
            return False
    
    return True

def build():
    """打包"""
    print("""
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║   🦞 NexusOS Windows 打包程序                        ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
""")
    
    if not check_requirements():
        print("\n❌ 依赖检查失败")
        return
    
    print("\n📦 开始打包...")
    print("="*50)
    
    # PyInstaller命令
    cmd = [
        "pyinstaller",
        "--onefile",           # 打包成单个文件
        "--windowed",          # 无控制台窗口
        "--name=NexusOS",      # 程序名
        "--icon=nexusos.ico",  # 图标(可选)
        "--add-data=.;.",     # 添加数据文件
        "nexusos_gui.py"
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print("\n" + "="*50)
        print("✅ 打包完成!")
        print("\n生成的文件:")
        print("  dist/NexusOS.exe")
        print("\n使用方法:")
        print("  双击 NexusOS.exe 即可运行")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ 打包失败: {e}")

def main():
    """主函数"""
    if len(sys.argv) > 1:
        if sys.argv[1] == "build":
            build()
        else:
            print("用法: python build.py")
    else:
        build()

if __name__ == "__main__":
    main()
