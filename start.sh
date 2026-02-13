#!/bin/bash
echo "
╔════════════════════════════════════════╗
║                                        ║
║   🦞 ClawOS - Quick Start              ║
║                                        ║
║   1. Web GUI    → Browser interface    ║
║   2. GUI        → Interactive CLI      ║
║   3. Tests      → Run benchmarks       ║
║   4. Simple     → Simple menu          ║
║   5. Verify     → Check installation   ║
║                                        ║
╚════════════════════════════════════════╝
"

read -p "Choose / 选择 (1-5): " choice

case $choice in
    1)
        echo "🚀 Starting Web GUI..."
        python3 /home/admin/.openclaw/workspace/webgui.py
        ;;
    2)
        echo "🚀 Starting GUI..."
        python3 /home/admin/.openclaw/workspace/clawos_gui.py
        ;;
    3)
        echo "🧪 Running benchmarks..."
        python3 /home/admin/.openclaw/workspace/comprehensive_test.py
        ;;
    4)
        echo "📋 Starting simple menu..."
        python3 /home/admin/.openclaw/workspace/simple_cli.py
        ;;
    5)
        echo "✅ Verifying installation..."
        python3 /home/admin/.openclaw/workspace/verify_install.py
        ;;
    *)
        echo "❌ Invalid choice"
        ;;
esac
