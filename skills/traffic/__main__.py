#!/usr/bin/env python3
# 🦞 Traffic Skill - Main Entry

import sys
sys.path.insert(0, '.')

def main():
    print("="*60)
    print("🦞 Traffic Enhancement Skill")
    print("="*60)
    
    from traffic import TrafficManager
    
    tm = TrafficManager()
    
    examples = [
        ("路况查询", lambda: tm.get_traffic_info("北京", "三环路")),
        ("出行规划", lambda: tm.plan_trip("天安门", "鸟巢", "driving")),
        ("公共交通", lambda: tm.get_public_transit("上海")),
        ("城际出行", lambda: tm.get_intercity_travel("北京", "上海")),
    ]
    
    print("\n🚗 Traffic Examples:\n")
    
    for name, func in examples:
        result = func()
        if name == "路况查询":
            print(f"Q: {name}")
            print(f"   Status: {result['status']}")
            print(f"   Speed: {result['speed_kmh']}km/h")
        elif name == "出行规划":
            print(f"Q: {name}")
            print(f"   Distance: {result.total_distance_km}km")
            print(f"   Duration: {result.total_duration_min}min")
        elif name == "公共交通":
            print(f"Q: {name}")
            print(f"   Subway lines: {len(result['subway_lines'])}")
        elif name == "城际出行":
            print(f"Q: {name}")
            print(f"   Distance: {result['distance_km']}km")
            print(f"   Options: {[o['mode'] for o in result['options']]}")
        print()
    
    print(f"Stats: {tm.get_stats()}")

if __name__ == "__main__":
    main()
