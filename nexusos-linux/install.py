#!/usr/bin/env python3
"""
🦞 NexusOS 安装脚本 (Linux)
"""

import os
import sys
import subprocess

def install():
    """安装NexusOS"""
    print("""
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║   🦞 NexusOS Linux 安装程序                              ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
""")
    
    # 创建目录
    home = os.path.expanduser("~")
    nexusos_dir = os.path.join(home, ".nexusos")
    
    print(f"📁 创建目录: {nexusos_dir}")
    os.makedirs(nexusos_dir, exist_ok=True)
    
    # 复制核心文件
    print("📦 复制核心文件...")
    core_src = "/home/admin/.openclaw/nexusos"
    core_dest = os.path.join(nexusos_dir, "core")
    
    if os.path.exists(core_src):
        os.system(f"cp -r {core_src} {core_dest}")
        print(f"✅ 核心文件已复制到: {core_dest}")
    
    # 创建命令链接
    print("🔗 创建命令链接...")
    bin_dir = os.path.join(home, "bin")
    os.makedirs(bin_dir, exist_ok=True)
    
    nexusos_cmd = os.path.join(home, "nexusos-linux", "nexusos")
    link_path = os.path.join(bin_dir, "nexusos")
    
    if os.path.exists(nexusos_cmd):
        if os.path.exists(link_path):
            os.remove(link_path)
        os.symlink(nexusos_cmd, link_path)
        os.chmod(link_path, 0o755)
        print(f"✅ 命令已创建: {link_path}")
    
    # 配置
    print("⚙️ 配置...")
    config_file = os.path.join(nexusos_dir, "config.json")
    config = {
        "version": "1.0.0",
        "data_dir": nexusos_dir,
        "log_level": "info"
    }
    
    import json
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)
    
    print("""
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║   ✅ 安装完成！                                          ║
║                                                           ║
║   使用方法:                                              ║
║   - nexusos start    启动服务                            ║
║   - nexusos stop    停止服务                            ║
║   - nexusos status  查看状态                            ║
║   - nexusos ask     提问问题                            ║
║   - nexusos help    查看帮助                            ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
""")

if __name__ == "__main__":
    install()
