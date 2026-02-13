# 🦞 ClawOS Unit Tests - 核心测试

import asyncio
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


class TestResult:
    def __init__(self, name: str, passed: bool, message: str = ""):
        self.name = name
        self.passed = passed
        self.message = message


class TestSuite:
    def __init__(self):
        self.results = []
        self.passed = 0
        self.failed = 0
    
    def add(self, result):
        self.results.append(result)
        if result.passed:
            self.passed += 1
        else:
            self.failed += 1
    
    def print_summary(self):
        print("\n" + "=" * 60)
        print(f"✅ 通过: {self.passed} | ❌ 失败: {self.failed}")
        print("=" * 60)


def test_onboarding():
    from clawos.onboarding import get_onboarding_manager, AVAILABLE_MODELS
    manager = get_onboarding_manager()
    cn = len([m for m in AVAILABLE_MODELS if m.is_cn])
    intl = len([m for m in AVAILABLE_MODELS if not m.is_cn])
    return TestResult("onboarding", True, f"国内:{cn} 国际:{intl}")


def test_settings():
    from clawos.storage.settings import SettingsStorage
    storage = SettingsStorage()
    settings = storage.load()
    return TestResult("settings", True, "加载成功")


async def test_reasoning():
    from clawos.core.reasoning import UltimateFusionEngine
    engine = UltimateFusionEngine()
    result = await engine.analyze("如果A>B，B>C，那么A>C吗？")
    return TestResult("reasoning", True, f"引擎:{result.engine_used}")


def test_performance():
    from clawos.core.performance import CacheManager
    cache = CacheManager()
    for i in range(100):
        cache.set(f"k{i}", f"v{i}")
    for i in range(100):
        cache.get(f"k{i}")
    stats = cache.get_stats()
    return TestResult("performance", True, f"命中:{stats['hits']}")


async def run_all_tests():
    suite = TestSuite()
    
    print("=" * 60)
    print("🦞 ClawOS 单元测试")
    print("=" * 60)
    
    # 同步测试
    tests_sync = [
        ("Onboarding", test_onboarding),
        ("Settings", test_settings),
        ("Performance", test_performance),
    ]
    
    for name, func in tests_sync:
        try:
            result = func()
            suite.add(result)
            print(f"{'✅' if result.passed else '❌'} {name}: {result.message}")
        except Exception as e:
            suite.add(TestResult(name, False, str(e)))
            print(f"❌ {name}: {e}")
    
    # 异步测试
    try:
        result = await test_reasoning()
        suite.add(result)
        print(f"{'✅' if result.passed else '❌'} reasoning: {result.message}")
    except Exception as e:
        suite.add(TestResult("reasoning", False, str(e)))
        print(f"❌ reasoning: {e}")
    
    suite.print_summary()
    return suite.failed == 0


if __name__ == "__main__":
    success = asyncio.run(run_all_tests())
    sys.exit(0 if success else 1)
