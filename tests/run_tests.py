#!/usr/bin/env python3
# 🦞 ClawOS 综合测试

"""
运行所有测试
"""

import sys
from pathlib import Path
import subprocess


def run_test_file(test_file: str) -> bool:
    """运行单个测试文件"""
    print(f"\n🧪 运行: {test_file}")
    try:
        result = subprocess.run(
            [sys.executable, test_file],
            capture_output=True,
            text=True
        )
        print(result.stdout)
        if result.returncode != 0:
            print(result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ 运行失败: {e}")
        return False


def main():
    """主测试函数"""
    print("=" * 60)
    print("🦞 ClawOS 综合测试")
    print("=" * 60)
    
    test_dir = Path(__file__).parent
    results = []
    
    # 核心测试
    results.append(run_test_file(str(test_dir / "test_core.py")))
    
    # 总结
    print("\n" + "=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"✅ 通过: {passed}/{total}")
    
    if passed == total:
        print("🎉 所有测试通过！")
        return 0
    else:
        print("⚠️ 部分测试失败")
        return 1


if __name__ == "__main__":
    sys.exit(main())
