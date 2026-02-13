@echo off
chcp 65001 >nul
REM 🦞 ClawOS Windows 安装脚本

echo ======================================
echo 🦞 ClawOS AI操作系统安装 (Windows)
echo ======================================
echo.

REM 检查Python版本
echo 📋 检查Python版本...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误: 未找到Python
    echo 请从 https://python.org 下载Python 3.10+
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python -c "import sys; print(sys.version_info.minor)"') do set PY_MINOR=%%i
if %PY_MINOR% LSS 10 (
    echo ❌ 错误: 需要Python 3.10+
    python --version
    pause
    exit /b 1
)
echo ✅ Python版本检查通过

echo.
echo 📦 安装依赖...
pip install --upgrade pip >nul 2>&1

REM 安装核心依赖
pip install rich click pydantic fastapi uvicorn pyyaml pillow python-dotenv >nul 2>&1
if errorlevel 1 (
    echo ⚠️ 部分依赖安装失败，请手动安装
)

echo.
echo 🔧 安装ClawOS...
pip install -e . >nul 2>&1

REM 验证安装
echo.
echo ✅ 验证安装...
clawos --version >nul 2>&1
if errorlevel 1 (
    echo ⚠️ 命令未注册，尝试使用python运行...
    python -m clawos.main --version >nul 2>&1
    if errorlevel 1 (
        echo ❌ 验证失败
        pause
        exit /b 1
    )
)

echo.
echo ======================================
echo ✅ 安装完成！
echo ======================================
echo.
echo 下一步:
echo   clawos chat          ^# 进入对话
echo   clawos --reconfigure ^# 配置模型
echo   clawos --help        ^# 查看帮助
echo.
echo 或者直接运行:
echo   python -m clawos.main chat
echo.
pause
