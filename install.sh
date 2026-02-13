#!/bin/bash
# 🦞 ClawOS 安装脚本

set -e

echo "======================================"
echo "🦞 ClawOS AI操作系统安装"
echo "======================================"

# 检查Python版本
echo "📋 检查Python版本..."
python3 --version
if [ $(python3 -c 'import sys; print(sys.version_info.major)') -lt 3 ] || \
   [ $(python3 -c 'import sys; print(sys.version_info.minor)') -lt 10 ]; then
    echo "❌ 错误: 需要Python 3.10+"
    exit 1
fi
echo "✅ Python版本检查通过"

# 创建虚拟环境（可选）
if [ "$1" == "--venv" ]; then
    echo "📦 创建虚拟环境..."
    python3 -m venv venv
    source venv/bin/activate
    echo "✅ 虚拟环境已激活"
fi

# 升级pip
echo "⬆️ 升级pip..."
pip3 install --upgrade pip

# 安装依赖
echo "📦 安装依赖..."
pip3 install -r requirements.txt

# 安装ClawOS
echo "🔧 安装ClawOS..."
pip3 install -e .

# 验证安装
echo "✅ 验证安装..."
clawos --version

echo ""
echo "======================================"
echo "✅ 安装完成！"
echo "======================================"
echo ""
echo "下一步："
echo "  clawos chat          # 进入对话"
echo "  clawos --reconfigure # 配置模型"
echo ""
