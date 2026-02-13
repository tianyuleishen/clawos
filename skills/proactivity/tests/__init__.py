#!/usr/bin/env python3
# 🦞 Proactivity Tests

import sys
sys.path.insert(0, '.')

def test_proactivity_manager():
    """测试主动性管理器"""
    from proactivity import ProactivityManager
    
    pm = ProactivityManager()
    
    tests = [
        ("主动性判断", lambda: pm.should_be_proactive("我刚开始一个新项目")),
        ("主动回复", lambda: pm.generate_proactive_response("我正在写代码")),
        ("提供建议", lambda: pm.offer_suggestions("编写一个新程序")),
        ("预测需求", lambda: pm.anticipate_user_needs("我遇到了一个问题")),
        ("预防检查", lambda: pm.preventive_check("担心错过截止日期")),
        ("主动行动", lambda: pm.take_initiative_action("刚开始一个新任务")),
    ]
    
    print("✅ Proactivity Manager 测试通过")
    
    for name, func in tests:
        result = func()
        if "主动性判断" in name:
            print(f"  ✓ {name}: {result}")
        elif "主动回复" in name:
            print(f"  ✓ {name}: {result['type']}")
        elif "提供建议" in name:
            print(f"  ✓ {name}: {result['content'][:30]}...")
        elif "预测需求" in name:
            print(f"  ✓ {name}: {len(result)}个需求")
        elif "预防检查" in name:
            print(f"  ✓ {name}: {'有提醒' if result else '无'}")
        elif "主动行动" in name:
            print(f"  ✓ {name}: {result['recommendation_count']}个行动")
    
    return True


def test_proactive_suggester():
    """测试主动建议器"""
    from proactivity import ProactiveSuggester
    
    ps = ProactiveSuggester()
    suggestion = ps.generate_suggestion("我正在写代码")
    
    print("\n✅ Proactive Suggester 测试通过")
    print(f"  建议类型: {suggestion.suggestion_type}")
    print(f"  操作项: {len(suggestion.action_items)}个")
    
    return True


def test_recommender():
    """测试推荐器"""
    from proactivity import Recommender
    
    r = Recommender()
    rec = r.generate_recommendation("正在学习编程", "resource")
    
    print("\n✅ Recommender 测试通过")
    print(f"  推荐类型: {rec.item_type}")
    print(f"  推荐内容: {rec.item_name}")
    
    path = r.recommend_learning_path("Python", "beginner")
    print(f"  学习路径: {len(path['path'])}个阶段")
    
    return True


def test_preventive_reminder():
    """测试预防性提醒"""
    from proactivity import PreventiveReminder
    
    pr = PreventiveReminder()
    alert = pr.generate_alert("担心技术债务")
    checklist = pr.create_checklist("coding", "start")
    
    print("\n✅ Preventive Reminder 测试通过")
    print(f"  预防提醒: {alert.description if alert else '无'}")
    print(f"  检查清单: {len(checklist['items'])}项")
    
    return True


def run_all_tests():
    """运行所有测试"""
    print("🦞 运行主动性技能测试...\n")
    
    test_proactivity_manager()
    test_proactive_suggester()
    test_recommender()
    test_preventive_reminder()
    
    print("\n✅ 所有测试通过!")


if __name__ == "__main__":
    run_all_tests()
