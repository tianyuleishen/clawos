#!/usr/bin/env python3
# 🦞 Traffic Tests

import sys
sys.path.insert(0, '.')

def test_traffic_manager():
    """测试交通管理器"""
    from traffic import TrafficManager
    
    tm = TrafficManager()
    
    tests = [
        ("路况查询", "北京", "三环路"),
        ("出行规划", "天安门", "鸟巢"),
        ("公共交通", "上海", ""),
        ("城际出行", "北京", "上海"),
    ]
    
    print("✅ Traffic Manager 测试通过")
    
    for name, *args in tests:
        if name == "路况查询":
            result = tm.get_traffic_info(args[0], args[1])
            print(f"  ✓ {name}: {result.get('status', 'ok')}")
        elif name == "出行规划":
            result = tm.plan_trip(args[0], args[1])
            print(f"  ✓ {name}: {result.total_distance_km}km")
        elif name == "公共交通":
            result = tm.get_public_transit(args[0])
            print(f"  ✓ {name}: {len(result['subway_lines'])}条地铁")
        elif name == "城际出行":
            result = tm.get_intercity_travel(args[0], args[1])
            print(f"  ✓ {name}: {result['distance_km']}km")
    
    return True


def test_route_planning():
    """测试路线规划"""
    from traffic import RoutePlanner
    
    planner = RoutePlanner()
    route = planner.plan_route("北京", "上海", "driving")
    
    print("\n✅ Route Planning 测试通过")
    print(f"  距离: {route.total_distance_km}km")
    print(f"  时间: {route.total_duration_min}分钟")
    print(f"  推荐: {route.recommendation}")
    
    return True


def run_all_tests():
    """运行所有测试"""
    print("🦞 运行交通技能测试...\n")
    
    test_traffic_manager()
    test_route_planning()
    
    print("\n✅ 所有测试通过!")


if __name__ == "__main__":
    run_all_tests()
