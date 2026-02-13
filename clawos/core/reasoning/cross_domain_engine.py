#!/usr/bin/env python3
"""
🦞 ClawOS Cross-Domain Knowledge Graph Engine - Phase 3
跨学科知识图谱 - 学科关联 + 知识迁移
"""

import json
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from collections import defaultdict


@dataclass
class DomainNode:
    """学科节点"""
    domain_id: str
    domain_name: str
    parent_domains: List[str]
    child_domains: List[str]
    related_domains: List[str]
    key_concepts: List[str]
    difficulty: str
    prerequisites: List[str]
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class KnowledgeRelation:
    """知识关联"""
    relation_id: str
    source_domain: str
    target_domain: str
    relation_type: str
    relation_strength: float
    examples: List[str]
    transfer_mechanism: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class CrossDomainSolution:
    """跨学科解决方案"""
    problem_id: str
    domains_involved: List[str]
    reasoning_chain: List[Dict]
    knowledge_transfers: List[Dict]
    final_answer: str
    confidence: float
    transfer_count: int
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


class DomainAssociationGraph:
    """学科关联图"""
    
    def __init__(self):
        self.nodes: Dict[str, DomainNode] = {}
        self.relations: Dict[str, List[KnowledgeRelation]] = defaultdict(list)
        
        self._build_domain_graph()
    
    def _build_domain_graph(self) -> None:
        """构建学科关联图"""
        
        domains = [
            {
                "id": "mathematics", "name": "数学",
                "parents": [], "children": ["physics", "computer_science", "economics"],
                "related": ["physics", "computer_science", "statistics"],
                "concepts": ["微积分", "线性代数", "概率论", "优化理论"],
                "difficulty": "intermediate", "prerequisites": []
            },
            {
                "id": "physics", "name": "物理",
                "parents": ["mathematics"], "children": ["chemistry", "engineering"],
                "related": ["mathematics", "chemistry", "engineering"],
                "concepts": ["力学", "电磁学", "热力学", "量子物理"],
                "difficulty": "advanced", "prerequisites": ["mathematics"]
            },
            {
                "id": "computer_science", "name": "计算机科学",
                "parents": ["mathematics", "logic"], "children": ["ai", "software_engineering"],
                "related": ["mathematics", "ai", "statistics"],
                "concepts": ["算法", "数据结构", "计算理论", "机器学习"],
                "difficulty": "intermediate", "prerequisites": ["mathematics", "logic"]
            },
            {
                "id": "chemistry", "name": "化学",
                "parents": ["physics"], "children": ["materials_science", "biochemistry"],
                "related": ["physics", "materials_science", "biology"],
                "concepts": ["有机化学", "物理化学", "量子化学"],
                "difficulty": "advanced", "prerequisites": ["physics", "mathematics"]
            },
            {
                "id": "economics", "name": "经济学",
                "parents": ["mathematics", "psychology"], "children": ["finance", "game_theory"],
                "related": ["mathematics", "psychology", "game_theory"],
                "concepts": ["微观经济学", "宏观经济学", "计量经济学"],
                "difficulty": "intermediate", "prerequisites": ["mathematics"]
            },
            {
                "id": "statistics", "name": "统计学",
                "parents": ["mathematics"], "children": ["data_science", "machine_learning"],
                "related": ["mathematics", "computer_science", "economics"],
                "concepts": ["描述统计", "推断统计", "回归分析", "贝叶斯统计"],
                "difficulty": "intermediate", "prerequisites": ["mathematics"]
            },
            {
                "id": "ai", "name": "人工智能",
                "parents": ["computer_science", "statistics", "mathematics"],
                "children": ["deep_learning", "nlp"],
                "related": ["computer_science", "statistics", "mathematics"],
                "concepts": ["机器学习", "深度学习", "自然语言处理", "计算机视觉"],
                "difficulty": "advanced", "prerequisites": ["mathematics", "computer_science", "statistics"]
            },
            {
                "id": "biology", "name": "生物",
                "parents": ["chemistry"], "children": ["medicine", "biochemistry"],
                "related": ["chemistry", "medicine", "biochemistry"],
                "concepts": ["遗传学", "细胞生物学", "生态学", "进化论"],
                "difficulty": "intermediate", "prerequisites": ["chemistry"]
            },
            {
                "id": "engineering", "name": "工程学",
                "parents": ["physics", "mathematics"], "children": ["mechanical_engineering", "electrical_engineering"],
                "related": ["physics", "mathematics", "computer_science"],
                "concepts": ["力学", "热力学", "电路设计", "控制系统"],
                "difficulty": "intermediate", "prerequisites": ["physics", "mathematics"]
            },
            {
                "id": "medicine", "name": "医学",
                "parents": ["biology", "chemistry"], "children": ["clinical_medicine"],
                "related": ["biology", "chemistry", "psychology"],
                "concepts": ["解剖学", "生理学", "药理学", "临床医学"],
                "difficulty": "advanced", "prerequisites": ["biology", "chemistry"]
            }
        ]
        
        # 添加节点
        for domain_data in domains:
            node = DomainNode(
                domain_id=domain_data["id"],
                domain_name=domain_data["name"],
                parent_domains=domain_data["parents"],
                child_domains=domain_data["children"],
                related_domains=domain_data["related"],
                key_concepts=domain_data["concepts"],
                difficulty=domain_data["difficulty"],
                prerequisites=domain_data["prerequisites"]
            )
            self.nodes[domain_data["id"]] = node
        
        # 定义关联
        relations = [
            {"source": "mathematics", "target": "physics", "type": "foundation", "strength": 0.95,
             "examples": ["微积分用于描述运动", "微分方程用于电磁学"], "transfer": "数学工具直接应用于物理问题"},
            {"source": "mathematics", "target": "computer_science", "type": "foundation", "strength": 0.90,
             "examples": ["算法复杂度分析", "图论用于网络"], "transfer": "数学证明方法应用于算法正确性"},
            {"source": "mathematics", "target": "economics", "type": "application", "strength": 0.85,
             "examples": ["最优化理论用于资源配置", "微分用于边际分析"], "transfer": "数学建模应用于经济现象"},
            {"source": "physics", "target": "chemistry", "type": "foundation", "strength": 0.90,
             "examples": ["量子力学用于化学键", "热力学用于相变"], "transfer": "物理原理解释化学现象"},
            {"source": "physics", "target": "engineering", "type": "application", "strength": 0.95,
             "examples": ["电磁学用于电路", "力学用于结构设计"], "transfer": "物理定律应用于工程设计"},
            {"source": "computer_science", "target": "ai", "type": "foundation", "strength": 0.95,
             "examples": ["算法用于模型训练", "数据结构用于表示"], "transfer": "计算机技术实现AI算法"},
            {"source": "statistics", "target": "machine_learning", "type": "foundation", "strength": 0.95,
             "examples": ["统计推断用于模型评估", "概率论用于不确定性"], "transfer": "统计方法应用于机器学习"},
            {"source": "chemistry", "target": "biology", "type": "foundation", "strength": 0.85,
             "examples": ["分子生物学", "生物化学"], "transfer": "化学原理解释生物过程"},
            {"source": "biology", "target": "medicine", "type": "application", "strength": 0.90,
             "examples": ["生理学", "药理学"], "transfer": "生物知识应用于疾病治疗"},
            {"source": "economics", "target": "game_theory", "type": "integration", "strength": 0.85,
             "examples": ["博弈论用于竞争分析", "策略交互"], "transfer": "经济模型扩展到战略决策"}
        ]
        
        for rel_data in relations:
            relation = KnowledgeRelation(
                relation_id=f"{rel_data['source']}_{rel_data['target']}",
                source_domain=rel_data["source"],
                target_domain=rel_data["target"],
                relation_type=rel_data["type"],
                relation_strength=rel_data["strength"],
                examples=rel_data["examples"],
                transfer_mechanism=rel_data["transfer"]
            )
            self.relations[rel_data["source"]].append(relation)
    
    def get_domain(self, domain_id: str) -> Optional[DomainNode]:
        return self.nodes.get(domain_id)
    
    def find_path(self, source_domain: str, target_domain: str) -> List[str]:
        if source_domain == target_domain:
            return [source_domain]
        
        visited = set()
        queue = [[source_domain]]
        
        while queue:
            path = queue.pop(0)
            current = path[-1]
            
            if current == target_domain:
                return path
            
            if current in visited:
                continue
            
            visited.add(current)
            
            for relation in self.relations[current]:
                if relation.target_domain not in visited:
                    new_path = path + [relation.target_domain]
                    queue.append(new_path)
        
        return []
    
    def get_related_domains(self, domain_id: str) -> List[DomainNode]:
        node = self.nodes.get(domain_id)
        if not node:
            return []
        
        related = []
        for related_id in node.related_domains:
            if related_id in self.nodes:
                related.append(self.nodes[related_id])
        
        return related
    
    def get_transfer_paths(self, source_domain: str, target_domain: str) -> List[KnowledgeRelation]:
        relations = []
        for rel in self.relations.get(source_domain, []):
            if rel.target_domain == target_domain:
                relations.append(rel)
        return relations


class KnowledgeTransferEngine:
    """知识迁移引擎"""
    
    def __init__(self):
        self.domain_graph = DomainAssociationGraph()
        self.transfer_history: List[Dict] = []
    
    def analyze_transfer(self, 
                        problem: Dict,
                        source_domain: str,
                        target_domain: str) -> Dict:
        """分析知识迁移"""
        
        # 步骤1: 找到迁移路径
        path = self.domain_graph.find_path(source_domain, target_domain)
        
        # 步骤2: 获取迁移关联
        relations = self.domain_graph.get_transfer_paths(source_domain, target_domain)
        
        # 步骤3: 分析迁移机制
        transfer_mechanism = self._extract_transfer_mechanism(problem, relations)
        
        # 步骤4: 构建迁移链
        transfer_chain = []
        for i, domain in enumerate(path[:-1]):
            for rel in self.domain_graph.relations.get(domain, []):
                if rel.target_domain == path[i+1]:
                    transfer_chain.append({
                        "from": domain,
                        "to": path[i+1],
                        "type": rel.relation_type,
                        "strength": rel.relation_strength,
                        "mechanism": rel.transfer_mechanism
                    })
        
        transfer_record = {
            "problem_id": problem.get("id", "unknown"),
            "source_domain": source_domain,
            "target_domain": target_domain,
            "path": path,
            "mechanism": transfer_mechanism
        }
        self.transfer_history.append(transfer_record)
        
        return {
            "path": path,
            "relations": [r.__dict__ for r in relations],
            "transfer_chain": transfer_chain,
            "transfer_mechanism": transfer_mechanism,
            "confidence": self._calculate_confidence(relations, path)
        }
    
    def _extract_transfer_mechanism(self, 
                                 problem: Dict,
                                 relations: List[KnowledgeRelation]) -> str:
        """提取迁移机制"""
        for rel in relations:
            if rel.transfer_mechanism:
                return rel.transfer_mechanism
        return "基于学科关联进行知识迁移"
    
    def _calculate_confidence(self, 
                           relations: List[KnowledgeRelation],
                           path: List[str]) -> float:
        """计算置信度"""
        if not relations:
            return 0.5
        
        avg_strength = sum(r.relation_strength for r in relations) / len(relations)
        path_factor = 1.0 / (len(path) - 1) if len(path) > 1 else 1.0
        
        return min(0.99, avg_strength * path_factor)
    
    def get_statistics(self) -> Dict:
        return {
            "total_transfers": len(self.transfer_history),
            "domains": list(self.domain_graph.nodes.keys()),
            "relations_count": sum(len(r) for r in self.domain_graph.relations.values())
        }


class CrossDomainReasoningEngine:
    """跨学科推理引擎"""
    
    VERSION = "1.0.0"
    
    def __init__(self):
        self.domain_graph = DomainAssociationGraph()
        self.transfer_engine = KnowledgeTransferEngine()
        self.statistics = {
            "total_problems": 0,
            "cross_domain_solved": 0,
            "avg_transfer_count": 0.0,
            "avg_confidence": 0.0
        }
    
    def solve(self, problem: Dict) -> CrossDomainSolution:
        """跨学科问题求解"""
        
        self.statistics["total_problems"] += 1
        
        problem_id = problem.get("id", "unknown")
        question = problem.get("question", "")
        
        # 步骤1: 识别涉及的学科
        domains = self._identify_domains(question)
        
        # 步骤2: 分析知识迁移
        transfer_analysis = None
        if len(domains) >= 2:
            transfer_analysis = self.transfer_engine.analyze_transfer(
                problem, domains[0], domains[1]
            )
        
        # 步骤3: 构建推理链
        reasoning_chain = self._build_reasoning_chain(question, domains, transfer_analysis)
        
        # 步骤4: 生成答案
        final_answer = self._generate_answer(question, domains, reasoning_chain)
        
        # 步骤5: 计算置信度
        confidence = self._calculate_confidence(domains, reasoning_chain, transfer_analysis)
        
        # 更新统计
        if confidence > 0.7:
            self.statistics["cross_domain_solved"] += 1
        
        total = self.statistics["total_problems"]
        self.statistics["avg_confidence"] = (
            (self.statistics["avg_confidence"] * (total - 1) + confidence) / total
        )
        
        transfer_count = len(transfer_analysis["transfer_chain"]) if transfer_analysis else 0
        self.statistics["avg_transfer_count"] = (
            (self.statistics["avg_transfer_count"] * (total - 1) + transfer_count) / total
        )
        
        return CrossDomainSolution(
            problem_id=problem_id,
            domains_involved=domains,
            reasoning_chain=reasoning_chain,
            knowledge_transfers=transfer_analysis["transfer_chain"] if transfer_analysis else [],
            final_answer=final_answer,
            confidence=confidence,
            transfer_count=transfer_count
        )
    
    def _identify_domains(self, question: str) -> List[str]:
        """识别涉及的学科"""
        domains = []
        question = question.lower()
        
        keywords = {
            "mathematics": ["数学", "积分", "导数", "矩阵", "概率"],
            "physics": ["物理", "力", "能量", "量子", "黑洞"],
            "chemistry": ["化学", "分子", "反应", "原子"],
            "biology": ["生物", "细胞", "遗传", "进化"],
            "economics": ["经济", "价格", "市场", "博弈"],
            "computer_science": ["算法", "计算", "程序", "数据"],
            "statistics": ["统计", "回归", "方差", "置信"],
            "ai": ["机器学习", "深度学习", "神经网络", "AI"]
        }
        
        for domain, kws in keywords.items():
            for kw in kws:
                if kw in question:
                    domains.append(domain)
                    break
        
        return domains if domains else ["general"]
    
    def _build_reasoning_chain(self, 
                              question: str,
                              domains: List[str],
                              transfer_analysis: Dict) -> List[Dict]:
        """构建推理链"""
        
        chain = []
        
        chain.append({
            "step": 1,
            "action": "领域识别",
            "domains": domains,
            "confidence": 0.95
        })
        
        if transfer_analysis:
            chain.append({
                "step": 2,
                "action": "知识迁移分析",
                "path": transfer_analysis.get("path", []),
                "mechanism": transfer_analysis.get("transfer_mechanism", ""),
                "confidence": transfer_analysis.get("confidence", 0.8)
            })
        
        if len(domains) >= 2:
            chain.append({
                "step": 3,
                "action": "跨学科推理",
                "source_domain": domains[0],
                "target_domain": domains[1],
                "confidence": 0.85
            })
        
        chain.append({
            "step": 4,
            "action": "综合答案",
            "confidence": 0.80
        })
        
        return chain
    
    def _generate_answer(self, 
                       question: str,
                       domains: List[str],
                       chain: List[Dict]) -> str:
        """生成答案"""
        
        if len(domains) >= 2:
            domain_names = {
                "mathematics": "数学", "physics": "物理", "chemistry": "化学",
                "biology": "生物", "economics": "经济学", "computer_science": "计算机科学",
                "statistics": "统计学", "ai": "人工智能"
            }
            
            domain1 = domain_names.get(domains[0], domains[0])
            domain2 = domain_names.get(domains[1], domains[1])
            
            return f"基于{domain1}和{domain2}的跨学科分析"
        
        return "基于学科知识进行分析"
    
    def _calculate_confidence(self, 
                            domains: List[str],
                            chain: List[Dict],
                            transfer_analysis: Dict) -> float:
        """计算置信度"""
        
        if not chain:
            return 0.5
        
        step_confidence = min(0.9, len(chain) * 0.2)
        domain_confidence = min(0.95, len(domains) * 0.3) if len(domains) >= 2 else 0.6
        transfer_confidence = transfer_analysis.get("confidence", 0.7) if transfer_analysis else 0.7
        
        confidence = (step_confidence * 0.3 + domain_confidence * 0.4 + transfer_confidence * 0.3)
        
        return min(0.99, confidence)
    
    def get_statistics(self) -> Dict:
        """获取统计"""
        total = self.statistics["total_problems"]
        return {
            "version": self.VERSION,
            "total_problems": total,
            "cross_domain_solved": self.statistics["cross_domain_solved"],
            "avg_confidence": f"{self.statistics['avg_confidence']:.1%}",
            "avg_transfer_count": f"{self.statistics['avg_transfer_count']:.1f}",
            "domain_graph_stats": self.transfer_engine.get_statistics()
        }


def create_cross_domain_engine() -> CrossDomainReasoningEngine:
    """创建跨学科推理引擎"""
    return CrossDomainReasoningEngine()


if __name__ == "__main__":
    engine = create_cross_domain_engine()
    
    print("\n" + "="*80)
    print("🦞 ClawOS Cross-Domain Knowledge Graph Engine v1.0 - Phase 3")
    print("="*80)
    print(f"\n版本: {engine.VERSION}")
    print("\n组件:")
    print("  ✓ DomainAssociationGraph (学科关联图)")
    print("  ✓ KnowledgeTransferEngine (知识迁移引擎)")
    print("  ✓ CrossDomainReasoningEngine (跨学科推理)")
    
    # 统计
    stats = engine.transfer_engine.get_statistics()
    print("\n📊 知识库统计:")
    print(f"  - 学科节点: {len(stats['domains'])}个")
    print(f"  - 关联数量: {stats['relations_count']}个")
    
    # 测试问题
    test_problems = [
        {"id": "cross-1", "question": "如何用数学方法优化经济资源配置？"},
        {"id": "cross-2", "question": "量子力学如何解释化学键的形成？"},
        {"id": "cross-3", "question": "机器学习中的统计方法如何应用于数据分析？"},
        {"id": "cross-4", "question": "牛顿力学如何应用于工程设计？"}
    ]
    
    print("\n🧪 测试跨学科推理:")
    for problem in test_problems:
        result = engine.solve(problem)
        print(f"\n  问题: {problem['question'][:30]}...")
        print(f"  涉及学科: {', '.join(result.domains_involved)}")
        print(f"  迁移次数: {result.transfer_count}")
        print(f"  置信度: {result.confidence:.1%}")
    
    # 统计
    stats = engine.get_statistics()
    print("\n📊 统计信息:")
    print(f"  总问题: {stats['total_problems']}")
    print(f"  解决数: {stats['cross_domain_solved']}")
    print(f"  平均置信度: {stats['avg_confidence']}")
    print(f"  平均迁移次数: {stats['avg_transfer_count']}")
    
    print("\n✅ Phase 3 - Cross-Domain Engine 测试完成！")
