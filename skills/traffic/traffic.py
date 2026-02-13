# 🦞 Traffic Core - 交通核心模块

"""
交通能力增强模块

为推理引擎提供交通和出行支持
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta


class VehicleType(Enum):
    """交通工具类型"""
    CAR = "car"
    BUS = "bus"
    SUBWAY = "subway"
    TAXI = "taxi"
    BICYCLE = "bicycle"
    WALK = "walk"
    TRAIN = "train"
    PLANE = "plane"


class TrafficStatus(Enum):
    """交通状态"""
    SMOOTH = "smooth"           # 畅通
    MODERATE = "moderate"       # 基本畅通
    CONGESTED = "congested"    # 拥堵
    HEAVY = "heavy"            # 严重拥堵
    CLOSED = "closed"          # 封闭


@dataclass
class TrafficCondition:
    """路况信息"""
    road_name: str
    status: str
    speed_kmh: float
    congestion_level: float  # 0-1
    incident: bool = False
    incident_type: str = ""
    last_update: float = field(default_factory=datetime.now().timestamp)


@dataclass
class PublicTransitInfo:
    """公共交通信息"""
    route_name: str
    vehicle_type: str
    next_arrival: int  # minutes
    status: str
    delay: int = 0  # minutes
    capacity: str = "normal"


@dataclass
class RouteStep:
    """路线步骤"""
    step_id: int
    instruction: str
    distance_km: float
    duration_min: int
    vehicle_type: str
    road_name: str = ""


@dataclass
class RoutePlan:
    """出行规划"""
    origin: str
    destination: str
    total_distance_km: float
    total_duration_min: int
    steps: List[RouteStep]
    alternatives: List[Dict] = field(default_factory=list)
    recommendation: str = ""
    departure_time: str = ""


class TrafficDatabase:
    """交通数据库（内置数据）"""
    
    # 中国主要城市道路数据
    ROAD_DATA = {
        "北京": {
            "环路": {
                "二环路": {"status": TrafficStatus.MODERATE.value, "speed": 55, "congestion": 0.4},
                "三环路": {"status": TrafficStatus.CONGESTED.value, "speed": 35, "congestion": 0.7},
                "四环路": {"status": TrafficStatus.MODERATE.value, "speed": 65, "congestion": 0.3},
                "五环路": {"status": TrafficStatus.SMOOTH.value, "speed": 80, "congestion": 0.2},
            },
            "主要干道": {
                "长安街": {"status": TrafficStatus.MODERATE.value, "speed": 45, "congestion": 0.5},
                "中关村大街": {"status": TrafficStatus.CONGESTED.value, "speed": 25, "congestion": 0.75},
            }
        },
        "上海": {
            "高架": {
                "内环": {"status": TrafficStatus.CONGESTED.value, "speed": 30, "congestion": 0.8},
                "中环": {"status": TrafficStatus.MODERATE.value, "speed": 50, "congestion": 0.45},
                "外环": {"status": TrafficStatus.SMOOTH.value, "speed": 70, "congestion": 0.25},
            }
        },
        "广州": {
            "主要道路": {
                "天河路": {"status": TrafficStatus.HEAVY.value, "speed": 20, "congestion": 0.85},
                "环城高速": {"status": TrafficStatus.MODERATE.value, "speed": 55, "congestion": 0.4},
            }
        },
        "深圳": {
            "主要道路": {
                "深南大道": {"status": TrafficStatus.MODERATE.value, "speed": 48, "congestion": 0.5},
                "北环大道": {"status": TrafficStatus.SMOOTH.value, "speed": 65, "congestion": 0.3},
            }
        }
    }
    
    # 地铁线路
    SUBWAY_LINES = {
        "北京": ["1号线", "2号线", "4号线", "5号线", "6号线", "7号线", "8号线", "9号线", "10号线", "13号线", "14号线", "15号线", "16号线", "八通线", "昌平线", "亦庄线", "房山线"],
        "上海": ["1号线", "2号线", "3号线", "4号线", "5号线", "6号线", "7号线", "8号线", "9号线", "10号线", "11号线", "12号线", "13号线", "14号线", "15号线", "16号线", "17号线", "18号线"],
        "广州": ["1号线", "2号线", "3号线", "4号线", "5号线", "6号线", "7号线", "8号线", "9号线", "13号线", "14号线", "21号线", "广佛线"],
        "深圳": ["1号线", "2号线", "3号线", "4号线", "5号线", "6号线", "7号线", "8号线", "9号线", "10号线", "11号线", "12号线"]
    }
    
    # 城市间距离
    INTERCITY_DISTANCE = {
        ("北京", "上海"): 1213,
        ("北京", "广州"): 2266,
        ("北京", "深圳"): 2400,
        ("上海", "广州"): 1455,
        ("上海", "深圳"): 1400,
        ("广州", "深圳"): 120,
    }
    
    def __init__(self):
        print("TrafficDatabase initialized")
    
    def get_road_condition(self, city: str, road_name: str) -> Optional[Dict]:
        """获取道路状况"""
        city_data = self.ROAD_DATA.get(city, {})
        
        for category, roads in city_data.items():
            if road_name in roads:
                return roads[road_name]
        
        # 模糊匹配
        for category, roads in city_data.items():
            for road, info in roads.items():
                if road_name in road or road in road_name:
                    return info
        
        return None
    
    def get_subway_lines(self, city: str) -> List[str]:
        """获取地铁线路"""
        return self.SUBWAY_LINES.get(city, [])
    
    def get_distance(self, city1: str, city2: str) -> int:
        """获取城市间距离"""
        key = (city1, city2) if (city1, city2) in self.INTERCITY_DISTANCE else (city2, city1)
        return self.INTERCITY_DISTANCE.get(key, 0)


class PublicTransitSystem:
    """公共交通系统"""
    
    def __init__(self):
        self.db = TrafficDatabase()
        print("PublicTransitSystem initialized")
    
    def get_bus_info(self, city: str, route: str) -> List[PublicTransitInfo]:
        """获取公交信息"""
        return [
            PublicTransitInfo(
                route_name=route,
                vehicle_type="bus",
                next_arrival=5,
                status="正常运行",
                delay=0,
                capacity="normal"
            )
        ]
    
    def get_subway_info(self, city: str, line: str) -> Dict:
        """获取地铁信息"""
        lines = self.db.get_subway_lines(city)
        
        return {
            "city": city,
            "line": line,
            "status": "正常运行",
            "operating_hours": "05:30-23:30",
            "transfer_stations": 5 if line in lines else 0
        }
    
    def get_transit_schedule(self, city: str, route: str) -> List[Dict]:
        """获取公交/地铁时刻表"""
        return [
            {"time": "06:00", "status": "normal"},
            {"time": "07:00", "status": "normal"},
            {"time": "08:00", "status": "peak"},
            {"time": "09:00", "status": "normal"},
        ]


class RoutePlanner:
    """路线规划器"""
    
    def __init__(self):
        self.db = TrafficDatabase()
        self.transit = PublicTransitSystem()
        print("RoutePlanner initialized")
    
    def plan_route(self, origin: str, destination: str, 
                   mode: str = "driving") -> RoutePlan:
        """
        规划路线
        
        Args:
            origin: 起点
            destination: 终点
            mode: 出行方式 (driving, transit, cycling, walking)
        """
        # 估算距离和时间
        distance_km = self._estimate_distance(origin, destination)
        
        if mode == "driving":
            duration = int(distance_km * 3)  # 平均30km/h
            vehicle = VehicleType.CAR.value
        elif mode == "transit":
            duration = int(distance_km * 5)  # 地铁平均20km/h
            vehicle = VehicleType.SUBWAY.value
        elif mode == "cycling":
            duration = int(distance_km * 10)  # 骑行10km/h
            vehicle = VehicleType.BICYCLE.value
        else:  # walking
            duration = int(distance_km * 15)  # 步行4km/h
            vehicle = VehicleType.WALK.value
        
        # 生成路线步骤
        steps = [
            RouteStep(
                step_id=1,
                instruction=f"从{origin}出发",
                distance_km=0.5,
                duration_min=2,
                vehicle_type=vehicle,
                road_name="起点"
            ),
            RouteStep(
                step_id=2,
                instruction=f"沿主干道前往{destination}",
                distance_km=distance_km - 1,
                duration_min=duration - 5,
                vehicle_type=vehicle,
                road_name="主干道"
            ),
            RouteStep(
                step_id=3,
                instruction=f"到达{destination}",
                distance_km=0.5,
                duration_min=3,
                vehicle_type=vehicle,
                road_name="终点"
            )
        ]
        
        # 替代路线
        alternatives = [
            {"mode": "transit", "duration_min": duration * 1.5, "description": "公共交通"},
            {"mode": "cycling", "duration_min": duration * 3, "description": "骑行路线"}
        ]
        
        # 推荐
        if duration > 60:
            recommendation = "建议使用公共交通或错峰出行"
        elif distance_km > 50:
            recommendation = "建议走高速或高铁"
        else:
            recommendation = "当前路线较为顺畅"
        
        return RoutePlan(
            origin=origin,
            destination=destination,
            total_distance_km=distance_km,
            total_duration_min=duration,
            steps=steps,
            alternatives=alternatives,
            recommendation=recommendation,
            departure_time=datetime.now().strftime("%H:%M")
        )
    
    def _estimate_distance(self, origin: str, destination: str) -> float:
        """估算距离"""
        # 城市内默认10km
        if origin != destination:
            return 15.0
        return 0.5


class LocationService:
    """地理位置服务"""
    
    # 城市坐标
    CITY_COORDS = {
        "北京": (39.9042, 116.4074),
        "上海": (31.2304, 121.4737),
        "广州": (23.1291, 113.2644),
        "深圳": (22.5431, 114.0579),
        "杭州": (30.2741, 120.1551),
        "成都": (30.5728, 104.0668),
        "武汉": (30.5928, 114.3055),
        "南京": (32.0603, 118.7969),
        "西安": (34.3416, 108.9398),
        "重庆": (29.5630, 106.5516),
    }
    
    def __init__(self):
        print("LocationService initialized")
    
    def get_coordinates(self, city: str) -> Optional[tuple]:
        """获取城市坐标"""
        return self.CITY_COORDS.get(city)
    
    def calculate_distance(self, city1: str, city2: str) -> float:
        """计算城市间直线距离（估算）"""
        coord1 = self.get_coordinates(city1)
        coord2 = self.get_coordinates(city2)
        
        if not coord1 or not coord2:
            return 0
        
        # 简化的距离计算
        lat_diff = abs(coord1[0] - coord2[0])
        lon_diff = abs(coord1[1] - coord2[1])
        
        # 每度约111km
        return (lat_diff + lon_diff) * 111
    
    def get_nearby_places(self, city: str, place_type: str = "") -> List[Dict]:
        """获取附近地点"""
        return [
            {"name": f"附近的{place_type}1", "distance": "500m"},
            {"name": f"附近的{place_type}2", "distance": "1km"},
        ]


class TrafficManager:
    """交通管理器"""
    
    def __init__(self):
        self.db = TrafficDatabase()
        self.transit = PublicTransitSystem()
        self.planner = RoutePlanner()
        self.location = LocationService()
        print("TrafficManager initialized")
    
    def get_traffic_info(self, city: str, road: str = "") -> Dict:
        """
        获取交通信息
        
        Args:
            city: 城市名
            road: 道路名（可选）
        """
        if road:
            road_info = self.db.get_road_condition(city, road)
            if road_info:
                return {
                    "city": city,
                    "road": road,
                    "status": road_info["status"],
                    "speed_kmh": road_info["speed"],
                    "congestion_level": road_info["congestion"]
                }
        
        # 返回城市整体路况
        return {
            "city": city,
            "overall_status": "基本畅通",
            "congestion_index": 0.5,
            "suggestion": "当前路况良好，放心出行"
        }
    
    def plan_trip(self, origin: str, destination: str, 
                   mode: str = "driving") -> RoutePlan:
        """规划出行"""
        return self.planner.plan_route(origin, destination, mode)
    
    def get_public_transit(self, city: str, route: str = "") -> Dict:
        """获取公共交通信息"""
        if route:
            return self.transit.get_bus_info(city, route)
        
        return {
            "city": city,
            "subway_lines": self.db.get_subway_lines(city),
            "bus_routes": "多条线路",
            "tips": "建议使用地图APP获取实时信息"
        }
    
    def get_intercity_travel(self, from_city: str, to_city: str) -> Dict:
        """城际出行"""
        distance = self.db.get_distance(from_city, to_city)
        
        options = []
        
        if distance < 200:
            options.append({"mode": "driving", "duration": f"{int(distance/80)}小时", "price": "油费约100元"})
            options.append({"mode": "bus", "duration": f"{int(distance/60)}小时", "price": "50-80元"})
        
        if distance < 500:
            options.append({"mode": "train", "duration": f"{int(distance/100)}小时", "price": "150-300元"})
        
        if distance >= 300:
            options.append({"mode": "plane", "duration": "1-2小时(含安检)", "price": "400-1500元"})
        
        return {
            "from": from_city,
            "to": to_city,
            "distance_km": distance,
            "options": options,
            "recommendation": options[0] if options else "建议自驾"
        }
    
    def get_stats(self) -> Dict:
        """获取统计"""
        return {
            "supported_cities": len(self.db.ROAD_DATA),
            "subway_lines": sum(len(lines) for lines in self.db.SUBWAY_LINES.values()),
            "intercity_routes": len(self.db.INTERCITY_DISTANCE)
        }


# 测试
if __name__ == "__main__":
    tm = TrafficManager()
    
    print("\n🦞 Traffic Manager 测试\n")
    
    # 路况查询
    info = tm.get_traffic_info("北京", "三环路")
    print(f"路况查询: {info}")
    
    # 出行规划
    route = tm.plan_trip("北京天安门", "北京鸟巢", "driving")
    print(f"\n出行规划:")
    print(f"  起点: {route.origin}")
    print(f"  终点: {route.destination}")
    print(f"  距离: {route.total_distance_km}km")
    print(f"  时间: {route.total_duration_min}分钟")
    print(f"  推荐: {route.recommendation}")
    
    # 公共交通
    transit = tm.get_public_transit("北京")
    print(f"\n公共交通: {transit['subway_lines'][:3]}...")
    
    # 城际出行
    intercity = tm.get_intercity_travel("北京", "上海")
    print(f"\n城际出行:")
    print(f"  距离: {intercity['distance_km']}km")
    print(f"  选项: {[o['mode'] for o in intercity['options']]}")
    
    print(f"\n统计: {tm.get_stats()}")
