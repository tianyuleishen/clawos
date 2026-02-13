# 🦞 Long-term Memory Core - 长程记忆核心模块

"""
长程记忆增强模块

为推理引擎提供长期记忆和经验学习支持
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
from collections import defaultdict
import json


class MemoryType(Enum):
    """记忆类型"""
    SEMANTIC = "semantic"           # 事实记忆
    EPISODIC = "episodic"           # 事件记忆
    PROCEDURAL = "procedural"       # 程序性记忆
    EMOTIONAL = "emotional"         # 情感记忆
    PREFERENCE = "preference"       # 偏好记忆
    EXPERIENCE = "experience"       # 经验记忆


class MemoryImportance(Enum):
    """记忆重要性"""
    CRITICAL = 5    # 关键
    HIGH = 4        # 高
    MEDIUM = 3      # 中
    LOW = 2         # 低
    TRIVIAL = 1     # 琐碎


@dataclass
class MemoryItem:
    """记忆条目"""
    memory_id: str
    content: str
    memory_type: str
    importance: int
    timestamp: float
    last_accessed: float
    access_count: int
    associations: List[str] = field(default_factory=list)
    context: str = ""
    tags: List[str] = field(default_factory=list)
    confidence: float = 0.9
    source: str = "user_interaction"


@dataclass
class EpisodicMemory:
    """情景记忆"""
    event_id: str
    description: str
    timestamp: float
    location: str = ""
    participants: List[str] = field(default_factory=list)
    emotions: List[str] = field(default_factory=list)
    outcomes: List[str] = field(default_factory=list)
    lessons_learned: List[str] = field(default_factory=list)


@dataclass
class ProceduralMemory:
    """程序性记忆（技能/流程）"""
    skill_id: str
    name: str
    steps: List[str]
    prerequisites: List[str] = field(default_factory=list)
    best_practices: List[str] = field(default_factory=list)
    common_mistakes: List[str] = field(default_factory=list)
    performance_metrics: Dict = field(default_factory=dict)


@dataclass
class UserPreference:
    """用户偏好"""
    preference_id: str
    category: str
    key: str
    value: Any
    confidence: float
    evidence_count: int
    last_updated: float


@dataclass
class MemorySearchResult:
    """记忆搜索结果"""
    query: str
    memories: List[MemoryItem]
    related_concepts: List[str] = field(default_factory=list)
    confidence_score: float = 0.0
    suggested_recall: List[str] = field(default_factory=list)


class SemanticMemoryStore:
    """语义记忆存储器"""
    
    def __init__(self):
        self.facts: Dict[str, MemoryItem] = {}
        self.concept_graph: Dict[str, List[str]] = defaultdict(list)  # 概念关联图
        print("SemanticMemoryStore initialized")
    
    def store_fact(self, fact: str, importance: int = 3, 
                   associations: List[str] = None, tags: List[str] = None) -> str:
        """存储事实"""
        import hashlib
        memory_id = hashlib.md5(f"{fact}{datetime.now().timestamp()}".encode()).hexdigest()[:16]
        
        item = MemoryItem(
            memory_id=memory_id,
            content=fact,
            memory_type=MemoryType.SEMANTIC.value,
            importance=importance,
            timestamp=datetime.now().timestamp(),
            last_accessed=datetime.now().timestamp(),
            access_count=0,
            associations=associations or [],
            tags=tags or []
        )
        
        self.facts[memory_id] = item
        
        # 更新概念图
        for concept in associations or []:
            self.concept_graph[concept].append(memory_id)
        
        return memory_id
    
    def retrieve_fact(self, query: str) -> Optional[MemoryItem]:
        """检索事实"""
        for item in self.facts.values():
            if query.lower() in item.content.lower():
                item.last_accessed = datetime.now().timestamp()
                item.access_count += 1
                return item
        return None
    
    def search_facts(self, keywords: List[str]) -> List[MemoryItem]:
        """搜索事实"""
        results = []
        for item in self.facts.values():
            for kw in keywords:
                if kw.lower() in item.content.lower():
                    results.append(item)
                    break
        return results
    
    def get_concept_associations(self, concept: str) -> List[str]:
        """获取概念关联"""
        return self.concept_graph.get(concept, [])
    
    def consolidate_memory(self, critical_facts: List[str]) -> int:
        """巩固重要记忆"""
        consolidated = 0
        for fact in critical_facts:
            if fact in [f.content for f in self.facts.values()]:
                for item in self.facts.values():
                    if item.content == fact:
                        item.confidence = min(1.0, item.confidence + 0.05)
                        consolidated += 1
        return consolidated
    
    def get_stats(self) -> Dict:
        """获取统计"""
        return {
            "total_facts": len(self.facts),
            "concept_connections": sum(len(v) for v in self.concept_graph.values()),
            "high_importance_count": sum(1 for f in self.facts.values() if f.importance >= 4)
        }


class EpisodicMemoryStore:
    """情景记忆存储器"""
    
    def __init__(self):
        self.episodes: Dict[str, EpisodicMemory] = {}
        self.timeline: List[Dict] = []
        print("EpisodicMemoryStore initialized")
    
    def record_event(self, description: str, location: str = "",
                    participants: List[str] = None, emotions: List[str] = None) -> str:
        """记录事件"""
        import hashlib
        event_id = hashlib.md5(f"{description}{datetime.now().timestamp()}".encode()).hexdigest()[:16]
        
        episode = EpisodicMemory(
            event_id=event_id,
            description=description,
            timestamp=datetime.now().timestamp(),
            location=location,
            participants=participants or [],
            emotions=emotions or []
        )
        
        self.episodes[event_id] = episode
        self.timeline.append({
            "event_id": event_id,
            "timestamp": episode.timestamp,
            "description": description
        })
        
        return event_id
    
    def add_outcome(self, event_id: str, outcome: str, lesson: str):
        """添加结果和教训"""
        if event_id in self.episodes:
            self.episodes[event_id].outcomes.append(outcome)
            self.episodes[event_id].lessons_learned.append(lesson)
    
    def retrieve_event(self, event_id: str) -> Optional[EpisodicMemory]:
        """检索事件"""
        return self.episodes.get(event_id)
    
    def search_events(self, keyword: str) -> List[EpisodicMemory]:
        """搜索事件"""
        results = []
        for episode in self.episodes.values():
            if keyword.lower() in episode.description.lower():
                results.append(episode)
        return results
    
    def get_recent_events(self, count: int = 10) -> List[EpisodicMemory]:
        """获取最近事件"""
        sorted_episodes = sorted(
            self.episodes.values(),
            key=lambda x: x.timestamp,
            reverse=True
        )
        return sorted_episodes[:count]
    
    def get_stats(self) -> Dict:
        """获取统计"""
        return {
            "total_events": len(self.episodes),
            "events_with_lessons": sum(1 for e in self.episodes.values() if e.lessons_learned),
            "unique_locations": len(set(e.location for e in self.episodes.values() if e.location))
        }


class ProceduralMemoryStore:
    """程序性记忆存储器"""
    
    def __init__(self):
        self.skills: Dict[str, ProceduralMemory] = {}
        self.skill_graph: Dict[str, List[str]] = defaultdict(list)  # 技能依赖图
        print("ProceduralMemoryStore initialized")
    
    def learn_skill(self, name: str, steps: List[str],
                    prerequisites: List[str] = None,
                    best_practices: List[str] = None,
                    common_mistakes: List[str] = None) -> str:
        """学习技能"""
        import hashlib
        skill_id = hashlib.md5(f"{name}{datetime.now().timestamp()}".encode()).hexdigest()[:16]
        
        skill = ProceduralMemory(
            skill_id=skill_id,
            name=name,
            steps=steps,
            prerequisites=prerequisites or [],
            best_practices=best_practices or [],
            common_mistakes=common_mistakes or []
        )
        
        self.skills[skill_id] = skill
        
        # 更新技能图
        for prereq in prerequisites or []:
            self.skill_graph[prereq].append(skill_id)
        
        return skill_id
    
    def retrieve_skill(self, skill_name: str) -> Optional[ProceduralMemory]:
        """检索技能"""
        for skill in self.skills.values():
            if skill_name.lower() in skill.name.lower():
                return skill
        return None
    
    def update_performance(self, skill_id: str, metrics: Dict):
        """更新性能指标"""
        if skill_id in self.skills:
            self.skills[skill_id].performance_metrics.update(metrics)
    
    def get_learned_skills(self) -> List[str]:
        """获取已学技能"""
        return [s.name for s in self.skills.values()]
    
    def get_prerequisites(self, skill_name: str) -> List[str]:
        """获取前置技能"""
        skill = self.retrieve_skill(skill_name)
        return skill.prerequisites if skill else []
    
    def get_stats(self) -> Dict:
        """获取统计"""
        return {
            "total_skills": len(self.skills),
            "total_dependencies": sum(len(v) for v in self.skill_graph.values()),
            "avg_steps_per_skill": sum(len(s.steps) for s in self.skills.values()) / max(1, len(self.skills))
        }


class ExperienceLearning:
    """经验学习"""
    
    def __init__(self):
        self.success_patterns: List[Dict] = []
        self.failure_patterns: List[Dict] = []
        self.improvement_suggestions: List[Dict] = []
        print("ExperienceLearning initialized")
    
    def record_outcome(self, action: str, outcome: str, success: bool):
        """记录结果"""
        pattern = {
            "action": action,
            "outcome": outcome,
            "success": success,
            "timestamp": datetime.now().timestamp()
        }
        
        if success:
            self.success_patterns.append(pattern)
        else:
            self.failure_patterns.append(pattern)
    
    def extract_lessons(self) -> List[str]:
        """提取教训"""
        lessons = []
        
        # 从失败中学习
        for pattern in self.failure_patterns[-10:]:
            lessons.append(f"避免: {pattern['action']} 导致 {pattern['outcome']}")
        
        # 从成功中强化
        for pattern in self.success_patterns[-10:]:
            lessons.append(f"继续: {pattern['action']} 达成 {pattern['outcome']}")
        
        return lessons
    
    def generate_improvement(self, context: str) -> List[str]:
        """生成改进建议"""
        suggestions = []
        
        # 基于失败模式
        recent_failures = [p for p in self.failure_patterns if p['timestamp'] > 
                          datetime.now().timestamp() - 86400 * 7]  # 最近7天
        
        for failure in recent_failures:
            suggestions.append(f"改进: {failure['action']} -> {failure['outcome']}")
        
        return suggestions
    
    def get_success_rate(self, action_type: str = None) -> float:
        """获取成功率"""
        if action_type:
            actions = [p for p in self.success_patterns + self.failure_patterns 
                      if p['action'] == action_type]
        else:
            actions = self.success_patterns + self.failure_patterns
        
        if not actions:
            return 0.5
        
        successes = sum(1 for p in actions if p['success'])
        return successes / len(actions)
    
    def get_stats(self) -> Dict:
        """获取统计"""
        return {
            "success_patterns": len(self.success_patterns),
            "failure_patterns": len(self.failure_patterns),
            "overall_success_rate": self.get_success_rate()
        }


class UserPreferenceMemory:
    """用户偏好记忆"""
    
    def __init__(self):
        self.preferences: Dict[str, UserPreference] = {}
        self.preference_history: List[Dict] = []
        print("UserPreferenceMemory initialized")
    
    def learn_preference(self, category: str, key: str, value: Any, 
                        evidence_count: int = 1) -> str:
        """学习偏好"""
        pref_id = f"{category}:{key}"
        
        if pref_id in self.preferences:
            # 更新已有偏好
            pref = self.preferences[pref_id]
            pref.value = value
            pref.confidence = min(1.0, pref.confidence + 0.1)
            pref.evidence_count += evidence_count
            pref.last_updated = datetime.now().timestamp()
        else:
            # 创建新偏好
            pref = UserPreference(
                preference_id=pref_id,
                category=category,
                key=key,
                value=value,
                confidence=0.6,
                evidence_count=evidence_count,
                last_updated=datetime.now().timestamp()
            )
            self.preferences[pref_id] = pref
        
        # 记录历史
        self.preference_history.append({
            "category": category,
            "key": key,
            "value": value,
            "timestamp": datetime.now().timestamp()
        })
        
        return pref_id
    
    def get_preference(self, category: str, key: str) -> Optional[Any]:
        """获取偏好"""
        pref_id = f"{category}:{key}"
        pref = self.preferences.get(pref_id)
        return pref.value if pref else None
    
    def get_category_preferences(self, category: str) -> Dict[str, Any]:
        """获取类别偏好"""
        return {
            k.split(":")[1]: v.value 
            for k, v in self.preferences.items() 
            if v.category == category
        }
    
    def infer_preference(self, context: str) -> Dict:
        """推断偏好"""
        # 基于历史推断
        relevant = [p for p in self.preference_history if 
                   context.lower() in str(p.get('value', '')).lower()]
        
        return {
            "inferred_preferences": [p['value'] for p in relevant[-5:]],
            "confidence": min(0.9, len(relevant) * 0.1)
        }
    
    def get_stats(self) -> Dict:
        """获取统计"""
        categories = set(p.category for p in self.preferences.values())
        return {
            "total_preferences": len(self.preferences),
            "unique_categories": len(categories),
            "high_confidence_count": sum(1 for p in self.preferences.values() if p.confidence >= 0.8)
        }


class MemoryAssociator:
    """记忆关联器"""
    
    def __init__(self):
        self.associations: Dict[str, List[str]] = defaultdict(list)
        self.association_strength: Dict[tuple, float] = {}
        print("MemoryAssociator initialized")
    
    def create_association(self, concept1: str, concept2: str, strength: float = 0.5):
        """创建关联"""
        self.associations[concept1].append(concept2)
        self.associations[concept2].append(concept1)
        self.association_strength[(min(concept1, concept2), max(concept1, concept2))] = strength
    
    def find_associations(self, concept: str) -> List[str]:
        """查找关联"""
        return list(set(self.associations.get(concept, [])))
    
    def find_chain_associations(self, concept: str, depth: int = 2) -> List[List[str]]:
        """查找关联链"""
        chains = []
        direct = self.associations.get(concept, [])
        
        for d in direct:
            chain = [concept, d]
            if depth > 1:
                second = self.associations.get(d, [])
                for s in second:
                    if s != concept:
                        chain.append(s)
            chains.append(chain)
        
        return chains
    
    def strengthen_association(self, concept1: str, concept2: str):
        """强化关联"""
        key = (min(concept1, concept2), max(concept1, concept2))
        if key in self.association_strength:
            self.association_strength[key] = min(1.0, self.association_strength[key] + 0.1)
    
    def get_stats(self) -> Dict:
        """获取统计"""
        return {
            "total_concepts": len(self.associations),
            "total_associations": sum(len(v) for v in self.associations.values()),
            "avg_strength": sum(self.association_strength.values()) / max(1, len(self.association_strength))
        }


class LongTermMemoryManager:
    """长程记忆管理器"""
    
    def __init__(self):
        # 初始化各子系统
        self.semantic = SemanticMemoryStore()
        self.episodic = EpisodicMemoryStore()
        self.procedural = ProceduralMemoryStore()
        self.experience = ExperienceLearning()
        self.preferences = UserPreferenceMemory()
        self.associator = MemoryAssociator()
        
        # 初始化知识库
        self._init_knowledge_base()
        
        print("LongTermMemoryManager initialized")
    
    def _init_knowledge_base(self):
        """初始化基础知识"""
        # 自我认知
        self.semantic.store_fact(
            "我是ClawOS AI操作系统",
            importance=5,
            associations=["AI", "操作系统", "智能助手"],
            tags=["identity", "core"]
        )
        
        # 用户信息
        self.semantic.store_fact(
            "用户要求提升各项能力集成到ClawOS",
            importance=4,
            associations=["集成", "能力提升", "ClawOS"],
            tags=["user_request", "project"]
        )
        
        # 已集成的技能
        for skill in ["推理引擎", "知识广度", "交通能力", "沟通能力", "创造力", "长程记忆"]:
            self.semantic.store_fact(
                f"已集成{skill}能力",
                importance=3,
                associations=[skill, "能力集成"],
                tags=["capability", "integration"]
            )
    
    def remember(self, content: str, memory_type: str = "semantic",
                importance: int = 3, associations: List[str] = None,
                context: str = "") -> str:
        """记忆"""
        if memory_type == "semantic":
            return self.semantic.store_fact(content, importance, associations)
        elif memory_type == "episodic":
            return self.episodic.record_event(content, context=context)
        elif memory_type == "preference":
            self.preferences.learn_preference("general", content[:20], content)
            return content[:16]
        else:
            return self.semantic.store_fact(content, importance, associations)
    
    def recall(self, query: str) -> MemorySearchResult:
        """回忆"""
        # 搜索语义记忆
        semantic_results = self.semantic.search_facts(query.split())
        
        # 搜索情景记忆
        episodic_results = self.episodic.search_events(query)
        
        # 获取关联概念
        related = self.associator.find_associations(query)
        
        # 构建结果
        all_memories = [MemoryItem(
            memory_id=m.content[:16],
            content=m.content,
            memory_type=m.memory_type if hasattr(m, 'memory_type') else "mixed",
            importance=m.importance if hasattr(m, 'importance') else 3,
            timestamp=getattr(m, 'timestamp', datetime.now().timestamp()),
            last_accessed=datetime.now().timestamp(),
            access_count=0
        ) for m in semantic_results + list(episodic_results)]
        
        return MemorySearchResult(
            query=query,
            memories=all_memories,
            related_concepts=related,
            confidence_score=min(0.95, len(all_memories) * 0.2)
        )
    
    def learn_from_interaction(self, query: str, response: str, success: bool):
        """从交互中学习"""
        # 记录成功/失败
        self.experience.record_outcome(query, response, success)
        
        # 提取并存储重要信息
        if success and len(response) > 50:
            self.remember(response, importance=4)
        
        # 创建关联
        self.associator.create_association(query, response)
    
    def get_user_insights(self) -> Dict:
        """获取用户洞察"""
        return {
            "preferences": self.preferences.get_category_preferences("general"),
            "success_rate": self.experience.get_success_rate(),
            "learned_skills": self.procedural.get_learned_skills(),
            "recent_events": [e.description for e in self.episodic.get_recent_events(5)],
            "top_concepts": list(self.associator.associations.keys())[:10]
        }
    
    def consolidate_memories(self):
        """巩固重要记忆"""
        # 巩固高频访问的记忆
        frequent = [f for f in self.semantic.facts.values() if f.access_count > 5]
        critical_content = [f.content for f in frequent if f.importance >= 4]
        
        return self.semantic.consolidate_memory(critical_content)
    
    def store_preference(self, category: str, key: str, value: Any):
        """存储偏好"""
        self.preferences.learn_preference(category, key, value)
    
    def get_preference(self, category: str, key: str) -> Any:
        """获取偏好"""
        return self.preferences.get_preference(category, key)
    
    def remember_procedure(self, name: str, steps: List[str], 
                          prerequisites: List[str] = None):
        """记忆流程"""
        self.procedural.learn_skill(name, steps, prerequisites)
    
    def get_procedure(self, name: str) -> Optional[ProceduralMemory]:
        """获取流程"""
        return self.procedural.retrieve_skill(name)
    
    def record_episode(self, description: str, **kwargs):
        """记录事件"""
        return self.episodic.record_event(description, **kwargs)
    
    def get_stats(self) -> Dict:
        """获取统计"""
        return {
            "semantic": self.semantic.get_stats(),
            "episodic": self.episodic.get_stats(),
            "procedural": self.procedural.get_stats(),
            "experience": self.experience.get_stats(),
            "preferences": self.preferences.get_stats(),
            "associations": self.associator.get_stats()
        }


# 测试
if __name__ == "__main__":
    ltm = LongTermMemoryManager()
    
    print("\n🦞 Long-term Memory Manager 测试\n")
    
    # 记忆
    ltm.remember("用户希望ClawOS具备长程记忆能力", importance=5, associations=["记忆", "ClawOS"])
    ltm.remember_procedure("如何学习新技能", ["观察", "实践", "反馈", "改进"], ["基础知识"])
    
    # 回忆
    result = ltm.recall("记忆")
    print(f"回忆查询: {result.memories[0].content if result.memories else '未找到'}")
    
    # 偏好
    ltm.store_preference("communication", "style", "professional")
    preference = ltm.get_preference("communication", "style")
    print(f"偏好获取: {preference}")
    
    # 经验学习
    ltm.learn_from_interaction("测试问题", "测试回答", success=True)
    lessons = ltm.experience.extract_lessons()
    print(f"经验教训: {len(lessons)}条")
    
    # 洞察
    insights = ltm.get_user_insights()
    print(f"用户洞察: {len(insights['learned_skills'])}个技能, {insights['success_rate']:.0%}成功率")
    
    # 统计
    stats = ltm.get_stats()
    print(f"\n统计:")
    print(f"  语义记忆: {stats['semantic']['total_facts']}条")
    print(f"  情景记忆: {stats['episodic']['total_events']}条")
    print(f"  程序记忆: {stats['procedural']['total_skills']}条")
    print(f"  偏好数量: {stats['preferences']['total_preferences']}条")
