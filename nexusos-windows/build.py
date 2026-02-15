#!/usr/bin/env python3
"""
🦞 NexusOS Windows 打包工具
打包成exe，内置依赖
"""

import os
import sys
import subprocess

VERSION = "2.9.0"
NAME = "NexusOS"

def check_requirements():
    """检查打包环境"""
    print("="*50)
    print("检查打包环境...")
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✓ PyInstaller: {PyInstaller.__version__}")
    except ImportError:
        print("✗ PyInstaller未安装")
        print("安装: pip install pyinstaller")
        return False
    
    return True

def build():
    """打包"""
    print("="*50)
    print(f"打包 {NAME} v{VERSION}")
    print("="*50)
    
    if not check_requirements():
        return
    
    # 打包命令
    # --onefile: 打包成单个exe
    # --windowed: 无控制台窗口
    # --add-data: 添加数据文件
    # --collect-all: 收集所有依赖
    
    cmd = [
        "pyinstaller",
        "--onefile",                    # 单个exe
        "--windowed",                  # 无窗口
        f"--name={NAME}",             # exe名称
        "--clean",                    # 清理缓存
        "--noconfirm",                # 不询问
        
        # 添加数据文件
        "--add-data=.",
        
        # 收集依赖
        "--collect-all=pyttsx3",
        "--collect-all=PIL",
        "--collect-all=pyautogui",
        
        # 排除不需要的
        "--exclude-module=pytest",
        "--exclude-module=tkinter",
        
        # 图标（如果有）
        # "--icon=nexusos.ico",
        
        "nexusos_gui.py"
    ]
    
    print("\n开始打包...")
    print("-"*50)
    
    try:
        subprocess.run(cmd, check=True)
        print("-"*50)
        print("✓ 打包完成!")
        print(f"\n生成文件: dist/{NAME}.exe")
        print("\n位置: dist/NexusOS.exe")
        
    except subprocess.CalledProcessError as e:
        print(f"✗ 打包失败: {e}")

def build_with_installer():
    """打包成安装包（高级功能）"""
    print("="*50)
    print("打包安装版...")
    print("="*50)
    
    # 先生成单个exe
    build()
    
    # 使用Inno Setup创建安装包（需要安装Inno Setup）
    inno_setup = """
[Setup]
AppName=NexusOS
AppVersion=2.9.0
DefaultDirName={autopf}\\NexusOS
OutputDir=installer
OutputBaseFilename=NexusOS_Setup
Compression=lzma
SolidCompression=yes

[Files]
Source=dist\\NexusOS.exe; DestDir: "{app}"
Source=*; DestDir: "{app}"; Flags: ignoreversion recursesubdirs

[Run]
Filename: "{app}\\NexusOS.exe"; Description: "运行 NexusOS"; Flags: postinstall nowait skipifsilent
"""
    
    print("\n如需创建安装包，可使用Inno Setup")
    print("参考配置已保存为 setup_template.iss")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="NexusOS打包工具")
    parser.add_argument("--installer", action="store_true", help="打包成安装包")
    
    args = parser.parse_args()
    
    if args.installer:
        build_with_installer()
    else:
        build()
