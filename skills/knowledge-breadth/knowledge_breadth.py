# 🦞 Knowledge Breadth Core - 知识广度核心

"""
知识广度增强模块

为推理引擎提供广泛的知识支持
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime


class KnowledgeDomain(Enum):
    """知识领域"""
    HISTORY = "history"
    SCIENCE = "science"
    TECHNOLOGY = "technology"
    CULTURE = "culture"
    GEOGRAPHY = "geography"
    HUMANITIES = "humanities"
    BUSINESS = "business"
    MEDICINE = "medicine"
    LAW = "law"
    ARTS = "arts"
    LITERATURE = "literature"
    PHILOSOPHY = "philosophy"
    RELIGION = "religion"
    SPORTS = "sports"
    ENTERTAINMENT = "entertainment"
    POLITICS = "politics"
    ECONOMICS = "economics"
    EDUCATION = "education"
    ENVIRONMENT = "environment"
    FOOD = "food"
    TRAVEL = "travel"
    ALL = "all"
    GENERAL_KNOWLEDGE = "general"


@dataclass
class KnowledgeResult:
    """知识检索结果"""
    query: str
    answer: str
    domain: str
    confidence: float
    sources: List[str] = field(default_factory=list)
    related_topics: List[str] = field(default_factory=list)
    timestamp: float = field(default_factory=datetime.now().timestamp)


@dataclass
class MultiDomainKnowledge:
    """多领域知识综合"""
    query: str
    answers: Dict[str, str] = field(default_factory=dict)
    best_domain: str = ""
    cross_domain_insights: List[str] = field(default_factory=list)
    confidence: float = 0.0


class KnowledgeBase:
    """知识库"""
    
    KNOWLEDGE_BASE = {
        "history": {
            "world_war_ii": {
                "query": ["二战", "World War II"],
                "answer": "第二次世界大战（1939-1945年）是人类历史上规模最大的全球性战争。",
                "key_events": ["1939年: 战争爆发", "1941年: 珍珠港事件", "1945年: 战争结束"]
            }
        },
        "science": {
            "relativity": {
                "query": ["相对论", "爱因斯坦"],
                "answer": "相对论是爱因斯坦1905年提出的物理理论，包括E=mc²等著名方程。",
                "key_points": ["E=mc²", "时间膨胀", "空间弯曲"]
            },
            "quantum_mechanics": {
                "query": ["量子力学", "quantum"],
                "answer": "量子力学是研究微观粒子运动规律的物理学分支。",
                "key_concepts": ["波粒二象性", "不确定性原理", "量子纠缠"]
            }
        },
        "technology": {
            "artificial_intelligence": {
                "query": ["人工智能", "AI"],
                "answer": "人工智能（AI）是研究模拟人类智能的科学。",
                "key_areas": ["机器学习", "深度学习", "NLP", "计算机视觉"]
            },
            "blockchain": {
                "query": ["区块链", "Blockchain"],
                "answer": "区块链是分布式账本技术，确保数据不可篡改。",
                "features": ["去中心化", "不可篡改", "透明可追溯"]
            }
        },
        "culture": {
            "chinese_culture": {
                "query": ["中华文化", "中国文化"],
                "answer": "中华文化是世界四大古文明之一，有5000多年历史。",
                "key_elements": ["儒家思想", "四大发明", "传统节日"]
            }
        },
        "geography": {
            "seven_wonders": {
                "query": ["世界七大奇迹", "Seven Wonders"],
                "answer": "世界七大奇迹是古代7座令人惊叹的建筑奇迹。",
                "wonders": ["吉萨金字塔", "空中花园", "宙斯神像"]
            }
        },
        "business": {
            "startup": {
                "query": ["创业", "Startup"],
                "answer": "创业是创建新企业的过程，涉及机会识别、资源整合等。",
                "key_steps": ["市场调研", "商业计划", "融资", "团队组建"]
            }
        },
        "philosophy": {
            "socratic_method": {
                "query": ["苏格拉底", "Socratic"],
                "answer": "苏格拉底方法是通过提问探究真理的哲学方法。",
                "principles": ["自知无知", "产婆术", "对话探究"]
            }
        }
    }
    
    def __init__(self):
        print("KnowledgeBase initialized")
    
    def query(self, domain: str, query: str) -> Optional[Dict]:
        domain_knowledge = self.KNOWLEDGE_BASE.get(domain, {})
        for key, data in domain_knowledge.items():
            for keyword in data.get("query", []):
                if keyword.lower() in query.lower():
                    return data
        return None


class DomainExpert:
    """领域专家"""
    
    EXPERTISE = {
        "history": ["世界史", "中国史", "古代史"],
        "science": ["物理", "化学", "生物"],
        "technology": ["AI", "编程", "区块链"],
        "culture": ["艺术", "宗教", "哲学"]
    }
    
    def __init__(self):
        print("DomainExpert initialized")
    
    def get_expertise(self, domain: str) -> List[str]:
        return self.EXPERTISE.get(domain, [])


class RealTimeKnowledge:
    """实时知识获取"""
    
    def __init__(self):
        print("RealTimeKnowledge initialized")
    
    def get_current_info(self, topic: str) -> Dict:
        return {"topic": topic, "note": "需要接入外部API"}


class MultiDomainKnowledgeEngine:
    """多领域知识综合"""
    
    def __init__(self):
        self.knowledge_base = KnowledgeBase()
        self.domain_expert = DomainExpert()
        self.realtime = RealTimeKnowledge()
        print("MultiDomainKnowledgeEngine initialized")
    
    def query_cross_domain(self, query: str) -> MultiDomainKnowledge:
        result = MultiDomainKnowledge(query=query)
        
        for domain in KnowledgeDomain:
            if domain.value == "all":
                continue
            knowledge = self.knowledge_base.query(domain.value, query)
            if knowledge:
                result.answers[domain.value] = knowledge.get("answer", "")
        
        if result.answers:
            result.best_domain = max(result.answers.keys(), 
                                   key=lambda x: len(result.answers[x]))
        
        if len(result.answers) > 1:
            result.cross_domain_insights = [
                f"涉及{len(result.answers)}个领域",
                f"主要涉及{result.best_domain}领域"
            ]
        
        result.confidence = min(0.95, len(result.answers) * 0.3)
        return result


class KnowledgeBreadth:
    """知识广度增强器"""
    
    def __init__(self):
        self.knowledge_base = KnowledgeBase()
        self.domain_expert = DomainExpert()
        self.realtime = RealTimeKnowledge()
        self.multi_domain = MultiDomainKnowledgeEngine()
        print("KnowledgeBreadth initialized")
    
    def enhance_reasoning(self, query: str) -> KnowledgeResult:
        domain = self._detect_domain(query)
        knowledge = self.knowledge_base.query(domain.value, query)
        
        if knowledge:
            return KnowledgeResult(
                query=query,
                answer=knowledge.get("answer", ""),
                domain=domain.value,
                confidence=0.85,
                sources=["内置知识库"],
                related_topics=knowledge.get("key_events", []) or knowledge.get("key_points", [])
            )
        
        return KnowledgeResult(
            query=query,
            answer="未找到相关知识",
            domain=domain.value,
            confidence=0.50,
            sources=["实时知识库"],
            related_topics=["需要接入外部知识库"]
        )
    
    def _detect_domain(self, query: str) -> KnowledgeDomain:
        query_lower = query.lower()
        
        if any(kw in query_lower for kw in ["战争", "历史", "朝代"]):
            return KnowledgeDomain.HISTORY
        if any(kw in query_lower for kw in ["科学", "物理", "化学", "相对论"]):
            return KnowledgeDomain.SCIENCE
        if any(kw in query_lower for kw in ["技术", "AI", "编程", "区块链"]):
            return KnowledgeDomain.TECHNOLOGY
        if any(kw in query_lower for kw in ["文化", "艺术", "节日"]):
            return KnowledgeDomain.CULTURE
        if any(kw in query_lower for kw in ["国家", "城市", "地理"]):
            return KnowledgeDomain.GEOGRAPHY
        if any(kw in query_lower for kw in ["商业", "创业", "经济"]):
            return KnowledgeDomain.BUSINESS
        if any(kw in query_lower for kw in ["哲学", "苏格拉底", "思想"]):
            return KnowledgeDomain.PHILOSOPHY
        
        return KnowledgeDomain.GENERAL_KNOWLEDGE
    
    def get_stats(self) -> Dict:
        return {
            "domains": len(KnowledgeDomain),
            "builtin_knowledge": len(self.knowledge_base.KNOWLEDGE_BASE)
        }


if __name__ == "__main__":
    kb = KnowledgeBreadth()
    
    tests = [
        "什么是相对论？",
        "二战有哪些重要事件？",
        "人工智能有哪些应用？",
        "中华文化有哪些特点？",
        "创业的步骤有哪些？"
    ]
    
    print("\nKnowledge Breadth Tests:\n")
    
    for query in tests:
        result = kb.enhance_reasoning(query)
        print(f"Q: {query}")
        print(f"  Domain: {result.domain}")
        print(f"  Confidence: {result.confidence:.0%}")
        print(f"  A: {result.answer[:50]}...")
        print()
