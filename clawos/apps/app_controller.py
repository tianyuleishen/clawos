# 🦞 Application Controller - 应用控制器

"""
应用控制器 - 跨平台应用管理

功能:
- 应用启动/关闭
- 应用状态查询
- 执行命令
- 进程管理
"""

import asyncio
import subprocess
import os
import sys
import signal
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
import platform

class Platform(Enum):
    """平台枚举"""
    WINDOWS = "Windows"
    MACOS = "Darwin"
    LINUX = "Linux"
    UNKNOWN = "Unknown"

@dataclass
class ProcessInfo:
    """进程信息"""
    name: str
    pid: int
    command: str
    status: str
    start_time: float
    cpu_percent: float = 0.0
    memory_percent: float = 0.0

@dataclass
class AppInfo:
    """应用信息"""
    name: str
    path: str
    executable: str
    is_running: bool
    pid: int = None

class AppController:
    """应用控制器"""
    
    def __init__(self):
        self.platform = platform.system()
        self.running_processes: Dict[str, subprocess.Popen] = {}
        self.process_history: List[ProcessInfo] = []
        print(f"✅ Application Controller 已加载 ({self.platform})")
    
    # ============ 应用启动 ============
    
    async def launch_app(
        self, 
        name: str, 
        path: str = None,
        args: List[str] = None,
        cwd: str = None,
        env: Dict[str, str] = None,
        shell: bool = False
    ) -> AppInfo:
        """启动应用
        
        Args:
            name: 应用名称
            path: 应用路径 (可选,自动查找)
            args: 命令行参数
            cwd: 工作目录
            env: 环境变量
            shell: 是否使用shell
        
        Returns:
            AppInfo: 应用信息
        """
        # 查找可执行文件
        executable = path or self._find_executable(name)
        
        if not executable:
            raise FileNotFoundError(f"找不到应用: {name}")
        
        # 构建命令
        cmd = [executable]
        if args:
            cmd.extend(args)
        
        # 创建进程
        try:
            if self.platform == "Windows" and shell:
                process = await asyncio.create_subprocess_shell(
                    " ".join(cmd),
                    cwd=cwd,
                    env=env,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
            else:
                process = await asyncio.create_subprocess_exec(
                    *cmd,
                    cwd=cwd,
                    env=env,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
            
            self.running_processes[name] = process
            
            return AppInfo(
                name=name,
                path=str(Path(executable).parent),
                executable=Path(executable).name,
                is_running=True,
                pid=process.pid
            )
            
        except Exception as e:
            raise RuntimeError(f"启动应用失败: {e}")
    
    async def launch_browser(self, url: str):
        """启动浏览器打开URL
        
        Args:
            url: URL地址
        """
        if self.platform == "Windows":
            await self.launch_app("browser", args=["start", url])
        elif self.platform == "Darwin":
            await self.launch_app("browser", args=["open", url])
        else:  # Linux
            await self.launch_app("browser", args=["xdg-open", url])
    
    async def open_file(self, file_path: str):
        """使用默认应用打开文件
        
        Args:
            file_path: 文件路径
        """
        if self.platform == "Windows":
            await self.launch_app("opener", args=["start", "", file_path], shell=True)
        elif self.platform == "Darwin":
            await self.launch_app("opener", args=["open", file_path])
        else:  # Linux
            await self.launch_app("opener", args=["xdg-open", file_path])
    
    # ============ 应用关闭 ============
    
    async def close_app(self, name: str, timeout: int = 5):
        """关闭应用
        
        Args:
            name: 应用名称
            timeout: 等待超时时间 (秒)
        """
        if name in self.running_processes:
            process = self.running_processes[name]
            
            # 尝试优雅关闭
            try:
                if self.platform == "Windows":
                    process.terminate()
                else:
                    process.terminate()
                
                try:
                    await asyncio.wait_for(process.wait(), timeout=timeout)
                except asyncio.TimeoutError:
                    # 强制终止
                    process.kill()
                    await process.wait()
                
                del self.running_processes[name]
                
            except Exception as e:
                raise RuntimeError(f"关闭应用失败: {e}")
        else:
            raise ValueError(f"应用未运行: {name}")
    
    async def kill_app(self, name: str):
        """强制终止应用
        
        Args:
            name: 应用名称
        """
        if name in self.running_processes:
            process = self.running_processes[name]
            process.kill()
            await process.wait()
            del self.running_processes[name]
        else:
            # 尝试查找并终止
            await self._kill_by_name(name)
    
    async def close_all_apps(self):
        """关闭所有运行中的应用"""
        for name in list(self.running_processes.keys()):
            try:
                await self.close_app(name)
            except Exception as e:
                print(f"关闭 {name} 失败: {e}")
    
    # ============ 状态查询 ============
    
    async def is_running(self, name: str) -> bool:
        """检查应用是否在运行"""
        if name in self.running_processes:
            process = self.running_processes[name]
            return process.returncode is None
        return False
    
    async def get_app_info(self, name: str) -> Optional[AppInfo]:
        """获取应用信息"""
        if name in self.running_processes:
            process = self.running_processes[name]
            return AppInfo(
                name=name,
                path="",
                executable=name,
                is_running=True,
                pid=process.pid
            )
        return None
    
    async def list_running_apps(self) -> List[AppInfo]:
        """列出所有运行中的应用"""
        apps = []
        for name, process in self.running_processes.items():
            if process.returncode is None:
                apps.append(AppInfo(
                    name=name,
                    path="",
                    executable=name,
                    is_running=True,
                    pid=process.pid
                ))
        return apps
    
    async def get_process_list(self) -> List[ProcessInfo]:
        """获取系统进程列表"""
        processes = []
        
        try:
            if self.platform == "Windows":
                result = subprocess.run(
                    ['tasklist', '/fo', 'csv', '/nh'],
                    capture_output=True,
                    text=True
                )
                for line in result.stdout.strip().split('\n'):
                    if line:
                        parts = line.split(',')
                        if len(parts) >= 2:
                            processes.append(ProcessInfo(
                                name=parts[0].strip('"'),
                                pid=int(parts[1].strip('"')),
                                command="",
                                status="running",
                                start_time=0
                            ))
            else:
                result = subprocess.run(
                    ['ps', '-eo', 'pid,comm,args'],
                    capture_output=True,
                    text=True
                )
                for line in result.stdout.strip().split('\n')[1:]:
                    if line:
                        parts = line.split(None, 2)
                        if len(parts) >= 2:
                            processes.append(ProcessInfo(
                                name=parts[1],
                                pid=int(parts[0]),
                                command=parts[2] if len(parts) > 2 else "",
                                status="running",
                                start_time=0
                            ))
        except Exception as e:
            print(f"获取进程列表失败: {e}")
        
        return processes
    
    # ============ 命令执行 ============
    
    async def execute_command(
        self, 
        command: str, 
        timeout: int = 30,
        shell: bool = True,
        cwd: str = None
    ) -> Dict[str, Any]:
        """执行命令
        
        Args:
            command: 命令
            timeout: 超时时间
            shell: 是否使用shell
            cwd: 工作目录
        
        Returns:
            Dict: 执行结果
        """
        try:
            if shell:
                process = await asyncio.create_subprocess_shell(
                    command,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                    cwd=cwd
                )
            else:
                parts = command.split()
                process = await asyncio.create_subprocess_exec(
                    *parts,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                    cwd=cwd
                )
            
            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(),
                    timeout=timeout
                )
            except asyncio.TimeoutError:
                process.kill()
                await process.communicate()
                return {
                    "success": False,
                    "returncode": -1,
                    "stdout": "",
                    "stderr": "Command timed out",
                    "timeout": True
                }
            
            return {
                "success": process.returncode == 0,
                "returncode": process.returncode,
                "stdout": stdout.decode('utf-8', errors='ignore').strip(),
                "stderr": stderr.decode('utf-8', errors='ignore').strip(),
                "timeout": False
            }
            
        except Exception as e:
            return {
                "success": False,
                "returncode": -1,
                "stdout": "",
                "stderr": str(e),
                "timeout": False
            }
    
    async def execute_python(
        self, 
        code: str, 
        timeout: int = 30
    ) -> Dict[str, Any]:
        """执行Python代码
        
        Args:
            code: Python代码
            timeout: 超时时间
        
        Returns:
            Dict: 执行结果
        """
        try:
            result = subprocess.run(
                [sys.executable, '-c', code],
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            return {
                "success": result.returncode == 0,
                "returncode": result.returncode,
                "stdout": result.stdout.strip(),
                "stderr": result.stderr.strip()
            }
            
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "returncode": -1,
                "stdout": "",
                "stderr": "Execution timed out"
            }
        except Exception as e:
            return {
                "success": False,
                "returncode": -1,
                "stdout": "",
                "stderr": str(e)
            }
    
    # ============ 辅助方法 ============
    
    def _find_executable(self, name: str) -> Optional[str]:
        """查找可执行文件路径"""
        # 检查是否在当前PATH中
        path = shutil.which(name)
        if path:
            return path
        
        # Windows常见位置
        if self.platform == "Windows":
            common_paths = [
                f"C:\\Program Files\\{name}\\{name}.exe",
                f"C:\\Program Files (x86)\\{name}\\{name}.exe",
                f"C:\\Windows\\System32\\{name}.exe",
            ]
            for p in common_paths:
                if os.path.exists(p):
                    return p
        
        # macOS常见位置
        elif self.platform == "Darwin":
            common_paths = [
                f"/Applications/{name}.app",
                f"/System/Applications/{name}.app",
            ]
            for p in common_paths:
                if os.path.exists(p):
                    return p
        
        return None
    
    async def _kill_by_name(self, name: str):
        """根据名称终止进程"""
        try:
            if self.platform == "Windows":
                await self.execute_command(f"taskkill /F /IM {name}.exe")
            else:
                await self.execute_command(f"pkill -f {name}")
        except Exception as e:
            print(f"终止进程失败: {e}")


# 便捷函数
async def launch_app(name: str, path: str = None) -> AppInfo:
    """启动应用"""
    controller = AppController()
    return await controller.launch_app(name, path)

async def execute_command(command: str) -> Dict[str, Any]:
    """执行命令"""
    controller = AppController()
    return await controller.execute_command(command)

# 测试代码
if __name__ == "__main__":
    async def test():
        print("📱 应用控制器测试")
        
        controller = AppController()
        
        # 测试列出运行中的应用
        print("\n1. 测试列出运行中的应用...")
        apps = await controller.list_running_apps()
        print(f"   正在运行: {len(apps)} 个")
        
        # 测试执行命令
        print("\n2. 测试执行命令...")
        result = await controller.execute_command("echo 'Hello ClawOS!'")
        print(f"   输出: {result['stdout']}")
        
        # 测试执行Python
        print("\n3. 测试执行Python代码...")
        result = await controller.execute_python("print('Python OK!')")
        print(f"   输出: {result['stdout']}")
        
        print("\n✅ 测试完成")
    
    asyncio.run(test())

import shutil
