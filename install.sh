#!/bin/bash
# 🦞 ClawOS 安装脚本

echo "=========================================="
echo "  🦞 ClawOS AI操作系统安装程序"
echo "=========================================="
echo ""

# 检查Python版本
echo "[1/4] 检查环境要求..."
python3 --version
if [ $? -ne 0 ]; then
    echo "❌ 错误: 未找到Python 3.10+"
    exit 1
fi
echo "✅ 环境检查通过"

# 创建虚拟环境
echo "[2/4] 创建虚拟环境..."
python3 -m venv venv
source venv/bin/activate
echo "✅ 虚拟环境创建成功"

# 安装依赖
echo "[3/4] 安装依赖包..."
pip install --upgrade pip
pip install -r requirements.txt
echo "✅ 依赖安装完成"

# 初始化
echo "[4/4] 初始化配置..."
python3 clawos/onboarding.py

echo ""
echo "=========================================="
echo "  ✅ 安装完成！"
echo "=========================================="
echo ""
echo "下一步:"
echo "  python clawos/cli.py     # 开始使用"
echo "  python clawos/gui/webgui.py  # Web界面"
echo ""
