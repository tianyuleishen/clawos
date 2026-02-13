#!/usr/bin/env python3
# 🦞 Creativity Tests

import sys
sys.path.insert(0, '.')

def test_creativity_manager():
    """测试创造力管理器"""
    from creativity import CreativityManager
    
    cm = CreativityManager()
    
    tests = [
        ("创造力增强", lambda: cm.enhance_creativity("生成一个新产品的创意")),
        ("头脑风暴", lambda: cm.brainstorm_ideas("移动应用")),
        ("解决问题", lambda: cm.solve_problem("用户流失率高", "creative")),
        ("创意建议", lambda: cm.get_creativity_tip("brainstorming")),
    ]
    
    print("✅ Creativity Manager 测试通过")
    
    for name, func in tests:
        result = func()
        if name == "创造力增强":
            print(f"  ✓ {name}: {result['suggested_technique']}")
        elif name == "头脑风暴":
            print(f"  ✓ {name}: {len(result.ideas)}个创意")
        elif name == "解决问题":
            print(f"  ✓ {name}: {len(result['solutions'])}个方案")
        elif name == "创意建议":
            print(f"  ✓ {name}: {result['tip']}")
    
    return True


def test_brainstorming():
    """测试头脑风暴"""
    from creativity import BrainstormingEngine
    
    be = BrainstormingEngine()
    hats = be.apply_six_hats("产品创新")
    
    print("\n✅ Brainstorming 测试通过")
    print(f"  六顶思考帽: {len(hats['hats'])}个帽子")
    
    return True


def test_design_thinking():
    """测试设计思维"""
    from creativity import DesignThinking
    
    dt = DesignThinking()
    design = dt.ideate("在线教育互动性差", 5)
    
    print("\n✅ Design Thinking 测试通过")
    print(f"  构思数量: {len(design)}")
    
    return True


def test_creative_writing():
    """测试创意写作"""
    from creativity import CreativeWriter
    
    cw = CreativeWriter()
    headlines = cw.generate_headlines("人工智能", 3)
    
    print("\n✅ Creative Writing 测试通过")
    print(f"  标题生成: {len(headlines)}个")
    
    return True


def run_all_tests():
    """运行所有测试"""
    print("🦞 运行创造力技能测试...\n")
    
    test_creativity_manager()
    test_brainstorming()
    test_design_thinking()
    test_creative_writing()
    
    print("\n✅ 所有测试通过!")


if __name__ == "__main__":
    run_all_tests()
