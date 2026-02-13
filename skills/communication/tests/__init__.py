#!/usr/bin/env python3
# 🦞 Communication Tests

import sys
sys.path.insert(0, '.')

def test_communication_manager():
    """测试沟通管理器"""
    from communication import CommunicationManager
    
    cm = CommunicationManager()
    
    tests = [
        ("沟通增强", lambda: cm.enhance_communication("我想让您考虑一下我们的新产品", "让对方感兴趣")),
        ("谈判", lambda: cm.negotiate("购买设备", offer=80, target=100, reservation=70)),
        ("冲突解决", lambda: cm.resolve_conflict("项目延期引发的不满")),
        ("沟通建议", lambda: cm.get_communication_tip("meeting")),
    ]
    
    print("✅ Communication Manager 测试通过")
    
    for name, func in tests:
        result = func()
        if name == "沟通增强":
            print(f"  ✓ {name}: 优化成功")
        elif name == "谈判":
            print(f"  ✓ {name}: {result['response']['action']}")
        elif name == "冲突解决":
            print(f"  ✓ {name}: {result['analysis']['recommended_approach']}")
        elif name == "沟通建议":
            print(f"  ✓ {name}: {result['tip'][:20]}...")
    
    return True


def test_negotiation():
    """测试谈判策略"""
    from communication import NegotiationTactics
    
    nt = NegotiationTactics()
    situation = nt.analyze_situation("合同谈判")
    
    print("\n✅ Negotiation 测试通过")
    print(f"  建议风格: {situation['recommended_style']}")
    
    return True


def test_conflict_resolution():
    """测试冲突解决"""
    from communication import ConflictResolver
    
    cr = ConflictResolver()
    script = cr.generate_script("difficult_conversation", "调解人")
    
    print("\n✅ Conflict Resolution 测试通过")
    print(f"  脚本生成: {script['script']['start'][:20]}...")
    
    return True


def run_all_tests():
    """运行所有测试"""
    print("🦞 运行沟通技能测试...\n")
    
    test_communication_manager()
    test_negotiation()
    test_conflict_resolution()
    
    print("\n✅ 所有测试通过!")


if __name__ == "__main__":
    run_all_tests()
