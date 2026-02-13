#!/bin/bash
# IntelliCore Installation Script
# 企业级智能决策系统安装脚本

echo "=========================================="
echo "  IntelliCore 安装程序"
echo "  Enterprise Intelligent Decision System"
echo "=========================================="
echo ""

# 检查Python版本
echo "[1/5] 检查环境要求..."
python3 --version
if [ $? -ne 0 ]; then
    echo "❌ 错误: 未找到Python 3.10+"
    exit 1
fi
echo "✅ 环境检查通过"

# 创建虚拟环境
echo "[2/5] 创建虚拟环境..."
python3 -m venv venv
source venv/bin/activate
echo "✅ 虚拟环境创建成功"

# 安装依赖
echo "[3/5] 安装依赖包..."
pip install --upgrade pip
pip install -r requirements.txt
echo "✅ 依赖安装完成"

# 配置系统
echo "[4/5] 系统配置..."
cp config.example.yaml config.yaml
echo "✅ 配置完成"

# 完成安装
echo "[5/5] 安装完成！"
echo ""
echo "=========================================="
echo "  🎉 IntelliCore 安装成功！"
echo "=========================================="
echo ""
echo "启动服务:"
echo "  source venv/bin/activate"
echo "  python main.py"
echo ""
echo "访问地址: http://localhost:8000"
echo ""
