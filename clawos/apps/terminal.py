# 🦞 Terminal Controller - 终端控制器

"""
终端控制器 - 跨平台终端/Shell控制

功能:
- 执行命令
- 捕获输出
- 交互式Shell
- 环境管理
"""

import asyncio
import subprocess
import os
import sys
import shlex
from typing import List, Optional, Dict, Any, AsyncIterator
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
import platform
import pty
import select
import time

class ShellType(Enum):
    """Shell类型"""
    BASH = "bash"
    ZSH = "zsh"
    POWERSHELL = "powershell"
    CMD = "cmd"
    FISH = "fish"
    SH = "sh"

@dataclass
class CommandResult:
    """命令执行结果"""
    command: str
    returncode: int
    stdout: str
    stderr: str
    duration: float
    success: bool

@dataclass
class ShellSession:
    """Shell会话信息"""
    session_id: str
    shell_type: ShellType
    working_directory: str
    environment: Dict[str, str]
    is_active: bool

class TerminalController:
    """终端控制器"""
    
    def __init__(self):
        self.platform = platform.system()
        self.active_sessions: Dict[str, subprocess.Popen] = {}
        self.session_counter = 0
        
        # 检测可用Shell
        self.default_shell = self._detect_shell()
        print(f"✅ Terminal Controller 已加载 ({self.platform})")
        print(f"   默认Shell: {self.default_shell.value}")
    
    # ============ 命令执行 ============
    
    async def execute(
        self, 
        command: str,
        cwd: str = None,
        env: Dict[str, str] = None,
        timeout: int = 30,
        shell: bool = True
    ) -> CommandResult:
        """执行命令
        
        Args:
            command: 命令
            cwd: 工作目录
            env: 环境变量
            timeout: 超时时间 (秒)
            shell: 是否使用shell
        
        Returns:
            CommandResult: 执行结果
        """
        start_time = time.time()
        
        try:
            if shell:
                process = await asyncio.create_subprocess_shell(
                    command,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                    cwd=cwd,
                    env=env,
                    limit=1024*1024  # 1MB
                )
            else:
                parts = shlex.split(command)
                process = await asyncio.create_subprocess_exec(
                    *parts,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                    cwd=cwd,
                    env=env
                )
            
            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(),
                    timeout=timeout
                )
            except asyncio.TimeoutError:
                process.kill()
                await process.communicate()
                
                return CommandResult(
                    command=command,
                    returncode=-1,
                    stdout="",
                    stderr=f"Command timed out after {timeout} seconds",
                    duration=time.time() - start_time,
                    success=False
                )
            
            return CommandResult(
                command=command,
                returncode=process.returncode,
                stdout=stdout.decode('utf-8', errors='ignore').strip(),
                stderr=stderr.decode('utf-8', errors='ignore').strip(),
                duration=time.time() - start_time,
                success=process.returncode == 0
            )
            
        except Exception as e:
            return CommandResult(
                command=command,
                returncode=-1,
                stdout="",
                stderr=str(e),
                duration=time.time() - start_time,
                success=False
            )
    
    async def execute_stream(
        self, 
        command: str,
        cwd: str = None,
        env: Dict[str, str] = None
    ) -> AsyncIterator[str]:
        """流式执行命令 (实时输出)
        
        Args:
            command: 命令
            cwd: 工作目录
            env: 环境变量
        
        Yields:
            str: 输出行
        """
        process = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
            cwd=cwd,
            env=env
        )
        
        while True:
            line = await process.stdout.readline()
            if not line:
                break
            yield line.decode('utf-8', errors='ignore').strip()
        
        await process.wait()
    
    async def execute_background(
        self, 
        command: str,
        session_id: str = None,
        cwd: str = None,
        env: Dict[str, str] = None
    ) -> str:
        """后台执行命令
        
        Args:
            command: 命令
            session_id: 会话ID
            cwd: 工作目录
            env: 环境变量
        
        Returns:
            str: 会话ID
        """
        if session_id is None:
            self.session_counter += 1
            session_id = f"session_{self.session_counter}"
        
        process = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=cwd,
            env=env
        )
        
        self.active_sessions[session_id] = process
        
        # 在后台等待进程完成
        asyncio.create_task(self._wait_for_session(session_id, process))
        
        return session_id
    
    async def _wait_for_session(self, session_id: str, process: subprocess.Popen):
        """等待会话完成"""
        await process.communicate()
        if session_id in self.active_sessions:
            del self.active_sessions[session_id]
    
    # ============ Shell会话 ============
    
    async def start_shell(
        self, 
        shell: ShellType = None,
        cwd: str = None,
        env: Dict[str, str] = None
    ) -> ShellSession:
        """启动交互式Shell会话
        
        Args:
            shell: Shell类型
            cwd: 工作目录
            env: 环境变量
        
        Returns:
            ShellSession: 会话信息
        """
        if shell is None:
            shell = self.default_shell
        
        self.session_counter += 1
        session_id = f"shell_{self.session_counter}"
        
        # 获取shell路径
        shell_path = self._get_shell_path(shell)
        
        # 创建伪终端
        master_fd, slave_fd = pty.openpty()
        
        # 启动shell
        process = await asyncio.create_subprocess_exec(
            shell_path,
            stdout=slave_fd,
            stderr=slave_fd,
            stdin=slave_fd,
            cwd=cwd,
            env=env
        )
        
        # 关闭slave端
        os.close(slave_fd)
        
        self.active_sessions[session_id] = process
        
        # 获取当前环境
        current_env = os.environ.copy()
        if env:
            current_env.update(env)
        
        return ShellSession(
            session_id=session_id,
            shell_type=shell,
            working_directory=cwd or os.getcwd(),
            environment=current_env,
            is_active=True
        )
    
    async def send_to_shell(
        self, 
        session: ShellSession, 
        command: str
    ) -> str:
        """向Shell发送命令
        
        Args:
            session: Shell会话
            command: 命令
        
        Returns:
            str: 输出
        """
        if session.session_id not in self.active_sessions:
            raise ValueError(f"会话不存在: {session.session_id}")
        
        process = self.active_sessions[session.session_id]
        
        # 发送命令
        process.stdin.write(command.encode())
        process.stdin.write(b'\n')
        await process.stdin.drain()
        
        # 等待输出
        await asyncio.sleep(0.1)
        
        # 读取输出
        output = await self._read_shell_output(session.session_id)
        
        return output
    
    async def close_shell(self, session: ShellSession):
        """关闭Shell会话"""
        if session.session_id in self.active_sessions:
            process = self.active_sessions[session.session_id]
            process.terminate()
            await process.wait()
            del self.active_sessions[session.session_id]
    
    async def _read_shell_output(self, session_id: str) -> str:
        """读取Shell输出"""
        if session_id not in self.active_sessions:
            return ""
        
        process = self.active_sessions[session_id]
        output = []
        
        # 使用select读取
        try:
            while True:
                r, _, _ = select.select([process.stdout], [], [], 0.1)
                if not r:
                    break
                    
                data = os.read(process.stdout, 1024)
                if not data:
                    break
                output.append(data.decode('utf-8', errors='ignore'))
        except:
            pass
        
        return ''.join(output)
    
    # ============ 环境管理 ============
    
    async def get_env(self, key: str) -> Optional[str]:
        """获取环境变量"""
        return os.environ.get(key)
    
    async def set_env(self, key: str, value: str):
        """设置环境变量"""
        os.environ[key] = value
    
    async def unset_env(self, key: str):
        """删除环境变量"""
        os.environ.pop(key, None)
    
    async def list_env(self) -> Dict[str, str]:
        """列出所有环境变量"""
        return dict(os.environ)
    
    # ============ 常用命令 ============
    
    async def list_dir(self, path: str = ".") -> List[str]:
        """列出目录"""
        result = await self.execute(f"ls -la {shlex.quote(path)}")
        if result.success:
            return result.stdout.split('\n')
        return []
    
    async def change_dir(self, path: str) -> bool:
        """切换目录"""
        result = await self.execute(f"cd {shlex.quote(path)} && pwd")
        return result.success
    
    async def make_dir(self, path: str, parents: bool = True) -> bool:
        """创建目录"""
        if parents:
            result = await self.execute(f"mkdir -p {shlex.quote(path)}")
        else:
            result = await self.execute(f"mkdir {shlex.quote(path)}")
        return result.success
    
    async def copy_file(self, src: str, dst: str) -> bool:
        """复制文件"""
        result = await self.execute(f"cp {shlex.quote(src)} {shlex.quote(dst)}")
        return result.success
    
    async def move_file(self, src: str, dst: str) -> bool:
        """移动文件"""
        result = await self.execute(f"mv {shlex.quote(src)} {shlex.quote(dst)}")
        return result.success
    
    async def delete_file(self, path: str, recursive: bool = False) -> bool:
        """删除文件"""
        if recursive:
            result = await self.execute(f"rm -rf {shlex.quote(path)}")
        else:
            result = await self.execute(f"rm {shlex.quote(path)}")
        return result.success
    
    async def get_file_content(self, path: str) -> str:
        """读取文件内容"""
        result = await self.execute(f"cat {shlex.quote(path)}")
        return result.stdout if result.success else ""
    
    async def write_file(self, path: str, content: str) -> bool:
        """写入文件"""
        result = await self.execute(f"cat > {shlex.quote(path)} << 'EOF'\n{content}\nEOF")
        return result.success
    
    async def search_files(self, pattern: str, path: str = ".") -> List[str]:
        """搜索文件"""
        result = await self.execute(f"find {shlex.quote(path)} -name {shlex.quote(pattern)}")
        if result.success:
            return [line for line in result.stdout.split('\n') if line]
        return []
    
    async def grep(
        self, 
        pattern: str, 
        path: str = ".",
        recursive: bool = True
    ) -> List[str]:
        """搜索文本"""
        if recursive:
            result = await self.execute(f"grep -r {shlex.quote(pattern)} {shlex.quote(path)}")
        else:
            result = await self.execute(f"grep {shlex.quote(pattern)} {shlex.quote(path)}")
        
        if result.success:
            return [line for line in result.stdout.split('\n') if line]
        return []
    
    async def get_process_list(self) -> List[str]:
        """获取进程列表"""
        result = await self.execute("ps aux")
        if result.success:
            return result.stdout.split('\n')
        return []
    
    async def get_disk_usage(self, path: str = ".") -> Dict[str, Any]:
        """获取磁盘使用情况"""
        result = await self.execute(f"df -h {shlex.quote(path)}")
        if result.success:
            lines = result.stdout.split('\n')
            return {"output": lines}
        return {}
    
    async def get_memory_usage(self) -> Dict[str, Any]:
        """获取内存使用情况"""
        result = await self.execute("free -h")
        if result.success:
            return {"output": result.stdout}
        return {}
    
    # ============ 系统信息 ============
    
    async def get_hostname(self) -> str:
        """获取主机名"""
        result = await self.execute("hostname")
        return result.stdout.strip() if result.success else ""
    
    async def get_username(self) -> str:
        """获取用户名"""
        result = await self.execute("whoami")
        return result.stdout.strip() if result.success else ""
    
    async def get_os_info(self) -> str:
        """获取操作系统信息"""
        if self.platform == "Windows":
            result = await self.execute("ver")
        else:
            result = await self.execute("uname -a")
        return result.stdout.strip() if result.success else self.platform
    
    async def get_uptime(self) -> str:
        """获取运行时间"""
        result = await self.execute("uptime -p" if self.platform != "Windows" else "net stats srv")
        return result.stdout.strip() if result.success else ""
    
    # ============ 辅助方法 ============
    
    def _detect_shell(self) -> ShellType:
        """检测默认Shell"""
        if self.platform == "Windows":
            return ShellType.CMD
        
        # 检查SHELL环境变量
        shell_path = os.environ.get("SHELL", "")
        if "zsh" in shell_path:
            return ShellType.ZSH
        elif "bash" in shell_path:
            return ShellType.BASH
        elif "fish" in shell_path:
            return ShellType.FISH
        
        # 检查默认shell
        default_shell = subprocess.run(
            ['getent', 'passwd', str(os.getuid())],
            capture_output=True,
            text=True
        )
        if default_shell.returncode == 0:
            user_shell = default_shell.stdout.split(':')[-1].strip()
            if "zsh" in user_shell:
                return ShellType.ZSH
            elif "bash" in user_shell:
                return ShellType.BASH
        
        return ShellType.BASH
    
    def _get_shell_path(self, shell: ShellType) -> str:
        """获取Shell路径"""
        shell_map = {
            ShellType.BASH: "bash",
            ShellType.ZSH: "zsh",
            ShellType.FISH: "fish",
            ShellType.POWERSHELL: "pwsh",
            ShellType.CMD: "cmd.exe",
        }
        
        path = shutil.which(shell_map.get(shell, "sh"))
        return path or shell_map.get(shell, "sh")


# 便捷函数
async def execute(command: str) -> CommandResult:
    """执行命令"""
    controller = TerminalController()
    return await controller.execute(command)

async def list_dir(path: str = ".") -> List[str]:
    """列出目录"""
    controller = TerminalController()
    return await controller.list_dir(path)

# 测试代码
if __name__ == "__main__":
    async def test():
        print("💻 终端控制器测试")
        
        controller = TerminalController()
        
        # 测试执行命令
        print("\n1. 测试执行命令...")
        result = await controller.execute("echo 'Hello Terminal!'")
        print(f"   输出: {result.stdout}")
        
        # 测试获取系统信息
        print("\n2. 测试获取系统信息...")
        hostname = await controller.get_hostname()
        print(f"   主机名: {hostname}")
        
        # 测试目录列表
        print("\n3. 测试目录列表...")
        files = await controller.list_dir("/home/admin/.openclaw/workspace")
        print(f"   文件数: {len(files)}")
        
        # 测试流式输出
        print("\n4. 测试流式输出...")
        async for line in controller.execute_stream("for i in 1 2 3; do echo $i; done"):
            print(f"   {line}")
        
        print("\n✅ 测试完成")
    
    asyncio.run(test())

import shutil
