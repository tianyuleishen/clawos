#!/usr/bin/env python3
"""
🦞 NexusOS Windows 安装程序
自动检测环境 + 安装依赖
"""

import os
import sys
import subprocess
import platform

def log(msg, level="INFO"):
    """日志输出"""
    colors = {
        "INFO": "\033[94m",    # 蓝色
        "SUCCESS": "\033[92m",  # 绿色
        "WARNING": "\033[93m", # 黄色
        "ERROR": "\033[91m",   # 红色
        "END": "\033[0m"
    }
    color = colors.get(level, "")
    print(f"{color}[{level}] {msg}{colors['END']}")

def check_python():
    """检查Python版本"""
    log("检查Python环境...")
    version = sys.version_info
    log(f"Python版本: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        log("需要Python 3.7+", "ERROR")
        return False
    
    log("Python环境检查通过", "SUCCESS")
    return True

def get_pip_command():
    """获取pip命令"""
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        # 虚拟环境
        return [sys.executable, '-m', 'pip']
    else:
        # 系统Python - 尝试使用pip3
        return ['pip3']

def install_package(package_name):
    """安装单个包"""
    pip_cmd = get_pip_command()
    
    log(f"安装 {package_name}...", "INFO")
    
    try:
        # 尝试直接安装
        result = subprocess.run(
            pip_cmd + ['install', package_name, '--quiet'],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        if result.returncode == 0:
            log(f"✓ {package_name} 安装成功", "SUCCESS")
            return True
        else:
            # 尝试使用--user
            result = subprocess.run(
                pip_cmd + ['install', package_name, '--user', '--quiet'],
                capture_output=True,
                text=True,
                timeout=120
            )
            
            if result.returncode == 0:
                log(f"✓ {package_name} 安装成功 (--user)", "SUCCESS")
                return True
            else:
                log(f"✗ {package_name} 安装失败: {result.stderr}", "WARNING")
                return False
                
    except subprocess.TimeoutExpired:
        log(f"✗ {package_name} 安装超时", "ERROR")
        return False
    except Exception as e:
        log(f"✗ {package_name} 安装异常: {e}", "ERROR")
        return False

def check_package(package_name):
    """检查包是否已安装"""
    try:
        __import__(package_name)
        return True
    except ImportError:
        return False

def get_package_import_name(package_name):
    """获取包的导入名称（处理特殊情况）"""
    mapping = {
        "Pillow": "PIL",
        "pyyaml": "yaml",
        "opencv-python": "cv2",
        "python-dateutil": "dateutil",
        " protobuf": "google",
    }
    return mapping.get(package_name, package_name)

def install_dependencies():
    """自动检测并安装依赖"""
    log("=" * 50, "INFO")
    log("开始检测环境并安装依赖", "INFO")
    log("=" * 50, "INFO")
    
    # 核心依赖（必须）
    core_packages = [
        "pyinstaller",
    ]
    
    # 可选依赖（带备用方案）
    optional_packages = [
        ("pyttsx3", "pyttsx3"),
        ("Pillow", "PIL"),
        ("pyautogui", "pyautogui"),
        ("pyscreeze", "pyscreeze"),
        ("pygetwindow", "pygetwindow"),
        ("keyboard", "keyboard"),
    ]
    
    # 安装核心依赖
    log("\n--- 核心依赖 ---", "INFO")
    all_success = True
    
    for package in core_packages:
        if check_package(package):
            log(f"✓ {package} 已安装", "SUCCESS")
        else:
            if install_package(package):
                pass
            else:
                all_success = False
    
    # 安装可选依赖
    log("\n--- 可选依赖 ---", "INFO")
    
    installed_count = 0
    failed_count = 0
    
    for import_name, package_name in optional_packages:
        if check_package(import_name):
            log(f"✓ {package_name} 已安装", "SUCCESS")
            installed_count += 1
        else:
            log(f"○ {package_name} 未安装，尝试安装...", "INFO")
            if install_package(package_name):
                installed_count += 1
            else:
                log(f"✗ {package_name} 安装失败，将使用备用方案", "WARNING")
                failed_count += 1
    
    # 总结
    log("\n" + "=" * 50, "INFO")
    log("安装完成", "INFO")
    log(f"已安装: {installed_count} 个可选包", "INFO")
    log(f"失败: {failed_count} 个（将有备用方案）", "WARNING")
    
    if all_success:
        log("核心功能可用", "SUCCESS")
    else:
        log("部分功能可能不可用", "WARNING")
    
    log("=" * 50, "INFO")
    
    return all_success

def check_system():
    """检查系统信息"""
    log("\n--- 系统信息 ---", "INFO")
    log(f"系统: {platform.system()}", "INFO")
    log(f"版本: {platform.version()}", "INFO")
    log(f"架构: {platform.machine()}", "INFO")
    log(f"Python: {sys.version}", "INFO")

def main():
    """主函数"""
    print("""
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║   🦞 NexusOS Windows 安装程序                      ║
║   自动检测环境 + 安装依赖                          ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
""")
    
    # 检查系统
    check_system()
    
    # 检查Python
    if not check_python():
        log("Python环境检查失败", "ERROR")
        sys.exit(1)
    
    # 安装依赖
    install_dependencies()
    
    print("""
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║   ✅ 安装完成!                                      ║
║                                                          ║
║   运行: python nexusos_gui.py                        ║
║                                                          ║
║   打包: python build.py                              ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
""")

if __name__ == "__main__":
    main()
