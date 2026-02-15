@echo off
REM ============================================================
REM 🦞 NexusOS Windows 安装程序
REM ============================================================

echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║                                                           ║
echo ║   🦞 NexusOS Windows 安装程序                           ║
echo ║                                                           ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.

REM 创建目录
echo 📁 创建目录...
set NEXUSOS_DIR=%USERPROFILE%\.nexusos
if not exist "%NEXUSOS_DIR%" mkdir "%NEXUSOS_DIR%"

REM 复制文件
echo 📦 复制核心文件...
xcopy /E /Y "%~dp0core" "%NEXUSOS_DIR%\core\" >nul 2>&1

REM 创建快捷方式
echo 🔗 创建快捷方式...
powershell -Command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('%USERPROFILE%\Desktop\NexusOS.lnk'); $s.TargetPath = 'pythonw.exe'; $s.Arguments = '%~dp0nexusos_gui.py'; $s.WorkingDirectory = '%~dp0'; $s.IconLocation = '%~dp0nexusos.ico'; $s.Save()"

echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║                                                           ║
echo ║   ✅ 安装完成！                                          ║
echo ║                                                           ║
echo ║   使用方法:                                              ║
echo ║   - 双击桌面"NexusOS"图标启动                          ║
echo ║   - 或运行 nexusos_gui.py                               ║
echo ║                                                           ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.

pause
