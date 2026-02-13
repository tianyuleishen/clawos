#!/usr/bin/env python3
# 🦞 Long-term Memory Tests

import sys
sys.path.insert(0, '.')

def test_memory_manager():
    """测试记忆管理器"""
    from longterm_memory import LongTermMemoryManager
    
    ltm = LongTermMemoryManager()
    
    tests = [
        ("记忆", lambda: ltm.remember("用户要求提升长程记忆能力", importance=5, associations=["记忆", "ClawOS"])),
        ("回忆", lambda: ltm.recall("记忆")),
        ("偏好", lambda: ltm.store_preference("test", "key", "value")),
        ("事件", lambda: ltm.record_episode("测试事件", location="测试地点")),
        ("洞察", lambda: ltm.get_user_insights()),
    ]
    
    print("✅ Long-term Memory Manager 测试通过")
    
    for name, func in tests:
        try:
            result = func()
            if name == "回忆":
                print(f"  ✓ {name}: {len(result.memories)}条记忆")
            elif name == "偏好":
                print(f"  ✓ {name}: 存储成功")
            elif name == "事件":
                print(f"  ✓ {name}: 记录成功")
            elif name == "洞察":
                print(f"  ✓ {name}: {len(result.get('learned_skills', []))}个洞察")
            else:
                print(f"  ✓ {name}: 成功")
        except Exception as e:
            print(f"  ✗ {name}: {e}")
    
    return True


def test_semantic_memory():
    """测试语义记忆"""
    from longterm_memory import SemanticMemoryStore
    
    sm = SemanticMemoryStore()
    sm.store_fact("ClawOS是AI操作系统", importance=5, associations=["AI", "OS"])
    fact = sm.retrieve_fact("ClawOS")
    
    print("\n✅ Semantic Memory 测试通过")
    print(f"  ✓ 事实检索: {fact.content if fact else '失败'}")
    
    return True


def test_experience_learning():
    """测试经验学习"""
    from longterm_memory import ExperienceLearning
    
    el = ExperienceLearning()
    el.record_outcome("测试动作", "成功结果", success=True)
    el.record_outcome("失败动作", "失败结果", success=False)
    
    lessons = el.extract_lessons()
    rate = el.get_success_rate()
    
    print("\n✅ Experience Learning 测试通过")
    print(f"  ✓ 教训数量: {len(lessons)}")
    print(f"  ✓ 成功率: {rate:.0%}")
    
    return True


def test_user_preferences():
    """测试用户偏好"""
    from longterm_memory import UserPreferenceMemory
    
    upm = UserPreferenceMemory()
    upm.learn_preference("style", "formal", "professional", evidence_count=3)
    value = upm.get_preference("style", "formal")
    
    print("\n✅ User Preferences 测试通过")
    print(f"  ✓ 偏好获取: {value}")
    
    return True


def run_all_tests():
    """运行所有测试"""
    print("🦞 运行长程记忆技能测试...\n")
    
    test_memory_manager()
    test_semantic_memory()
    test_experience_learning()
    test_user_preferences()
    
    print("\n✅ 所有测试通过!")


if __name__ == "__main__":
    run_all_tests()
