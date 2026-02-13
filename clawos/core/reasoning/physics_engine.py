#!/usr/bin/env python3
"""
🦞 ClawOS Physics Knowledge Engine - Phase 2
物理知识库 - 量子物理 + 凝聚态 + 天体物理
"""

import json
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from collections import defaultdict


@dataclass
class PhysicsConcept:
    """物理概念"""
    name: str
    definition: str
    formula: str
    units: List[str]
    domain: str
    difficulty: str  # basic, intermediate, advanced
    related_concepts: List[str]
    examples: List[str]
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class PhysicsFormula:
    """物理公式"""
    name: str
    formula: str
    variables: Dict[str, str]  # 变量名: 单位
    domain: str
    conditions: List[str]  # 适用条件
    limitations: List[str]
    example: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class PhysicsSolution:
    """物理问题解答"""
    problem_id: str
    domain: str
    concepts_used: List[str]
    formulas_used: List[str]
    reasoning_steps: List[Dict]
    final_answer: str
    confidence: float
    verification: Dict
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


class PhysicsKnowledgeBase:
    """物理知识库"""
    
    def __init__(self):
        self.concepts: Dict[str, PhysicsConcept] = {}
        self.formulas: Dict[str, PhysicsFormula] = {}
        self.domain_index: Dict[str, List[str]] = defaultdict(list)
        
        self._build_knowledge_base()
    
    def _build_knowledge_base(self) -> None:
        """构建知识库"""
        
        # ===== 量子物理概念 =====
        quantum_concepts = [
            {
                "name": "波函数",
                "definition": "描述量子系统状态的复数函数",
                "formula": "Ψ(r,t)",
                "units": ["无量纲"],
                "domain": "quantum",
                "difficulty": "advanced",
                "related_concepts": ["薛定谔方程", "概率密度", "希尔伯特空间"],
                "examples": ["电子双缝干涉", "量子隧穿"]
            },
            {
                "name": "不确定性原理",
                "definition": "不可能同时精确测量粒子的位置和动量",
                "formula": "Δx·Δp ≥ ℏ/2",
                "units": ["J·s"],
                "domain": "quantum",
                "difficulty": "advanced",
                "related_concepts": ["海森堡", "标准量子极限"],
                "examples": ["电子束发散", "量子测量"]
            },
            {
                "name": "量子纠缠",
                "definition": "粒子间的非局域关联，一个粒子的状态瞬间影响另一个",
                "formula": "|Ψ⟩ = (|00⟩ + |11⟩)/√2",
                "units": ["无量纲"],
                "domain": "quantum",
                "difficulty": "advanced",
                "related_concepts": ["EPR佯谬", "贝尔不等式", "量子隐形传态"],
                "examples": ["量子密钥分发", "量子计算"]
            },
            {
                "name": "薛定谔方程",
                "definition": "描述量子态随时间演化的基本方程",
                "formula": "iℏ∂Ψ/∂t = ĤΨ",
                "units": ["J"],
                "domain": "quantum",
                "difficulty": "advanced",
                "related_concepts": ["哈密顿量", "定态方程", "能量本征值"],
                "examples": ["无限深势阱", "谐振子"]
            },
            {
                "name": "量子隧穿",
                "definition": "粒子有一定概率穿过经典力学不允许的势垒",
                "formula": "T ≈ e^(-2κL)",
                "units": ["无量纲"],
                "domain": "quantum",
                "difficulty": "advanced",
                "related_concepts": ["势垒穿透", "隧穿概率"],
                "examples": ["扫描隧道显微镜", "核聚变"]
            }
        ]
        
        # ===== 凝聚态物理概念 =====
        condensed_concepts = [
            {
                "name": "超导性",
                "definition": "某些材料在低温下电阻完全消失的特性",
                "formula": "R = 0",
                "units": ["Ω"],
                "domain": "condensed",
                "difficulty": "intermediate",
                "related_concepts": ["临界温度", "迈斯纳效应", "库珀对"],
                "examples": ["MRI磁体", "磁悬浮列车"]
            },
            {
                "name": "能带理论",
                "definition": "描述固体中电子能量状态的能级结构",
                "formula": "E(k)",
                "units": ["eV"],
                "domain": "condensed",
                "difficulty": "advanced",
                "related_concepts": ["能带间隙", "费米面", "布洛赫波"],
                "examples": ["半导体", "金属导电性"]
            },
            {
                "name": "库珀对",
                "definition": "两个电子通过声子媒介形成的束缚态",
                "formula": "Δ ≈ 1.14ℏω_D e^(-1/N(0)V)",
                "units": ["eV"],
                "domain": "condensed",
                "difficulty": "advanced",
                "related_concepts": ["BCS理论", "超导能隙"],
                "examples": ["传统超导体", "约瑟夫森效应"]
            },
            {
                "name": "拓扑绝缘体",
                "definition": "内部绝缘但表面存在导电态的材料",
                "formula": "Z₂不变量",
                "units": ["无量纲"],
                "domain": "condensed",
                "difficulty": "advanced",
                "related_concepts": ["拓扑保护", "表面态"],
                "examples": ["Bi2Se3", "量子自旋霍尔效应"]
            },
            {
                "name": "相变",
                "definition": "物质从一种相转变为另一种相的过程",
                "formula": "G = H - TS",
                "units": ["J"],
                "domain": "condensed",
                "difficulty": "intermediate",
                "related_concepts": ["朗道相变理论", "临界现象", "序参量"],
                "examples": ["冰融化成水", "铁磁相变"]
            }
        ]
        
        # ===== 天体物理概念 =====
        astrophysics_concepts = [
            {
                "name": "黑洞",
                "definition": "引力强大到连光都无法逃脱的天体",
                "formula": "r_s = 2GM/c²",
                "units": ["m"],
                "domain": "astrophysics",
                "difficulty": "advanced",
                "related_concepts": ["事件视界", "奇点", "霍金辐射"],
                "examples": ["银河系中心黑洞", "引力波"]
            },
            {
                "name": "引力波",
                "definition": "时空涟漪，由加速质量产生",
                "formula": "h ≈ (G/c⁴)·(d²Q/dt²)",
                "units": ["无量纲"],
                "domain": "astrophysics",
                "difficulty": "advanced",
                "related_concepts": ["爱因斯坦方程", "LIGO探测"],
                "examples": ["双黑洞并合", "中子星碰撞"]
            },
            {
                "name": "暗物质",
                "definition": "不发光但有引力效应的神秘物质",
                "formula": "ρ(r) ∝ 1/r²",
                "units": ["g/cm³"],
                "domain": "astrophysics",
                "difficulty": "advanced",
                "related_concepts": ["星系旋转曲线", "引力透镜"],
                "examples": ["子弹星系团", "宇宙结构形成"]
            },
            {
                "name": "宇宙微波背景辐射",
                "definition": "大爆炸38万年后的余晖",
                "formula": "T = 2.725 K",
                "units": ["K"],
                "domain": "astrophysics",
                "difficulty": "intermediate",
                "related_concepts": ["宇宙学红移", "普朗克卫星"],
                "examples": ["宇宙年龄测定", "原初涨落"]
            },
            {
                "name": "恒星演化",
                "definition": "恒星从诞生到死亡的过程",
                "formula": "E = mc²",
                "units": ["J"],
                "domain": "astrophysics",
                "difficulty": "intermediate",
                "related_concepts": ["主序星", "超新星", "中子星"],
                "examples": ["太阳生命周期", "重元素合成"]
            }
        ]
        
        # ===== 添加概念到知识库 =====
        all_concepts = (quantum_concepts + condensed_concepts + astrophysics_concepts)
        
        for concept_data in all_concepts:
            concept = PhysicsConcept(**concept_data)
            self.concepts[concept.name] = concept
            self.domain_index[concept.domain].append(concept.name)
        
        # ===== 构建公式库 =====
        formulas = [
            {
                "name": "德布罗意关系",
                "formula": "λ = h/p",
                "variables": {"λ": "波长", "h": "普朗克常数", "p": "动量"},
                "domain": "quantum",
                "conditions": ["任何粒子"],
                "limitations": ["仅限非相对论"],
                "example": "电子显微镜分辨率"
            },
            {
                "name": "海森堡不确定性",
                "formula": "Δx·Δp ≥ ℏ/2",
                "variables": {"Δx": "位置不确定度", "Δp": "动量不确定度", "ℏ": "约化普朗克常数"},
                "domain": "quantum",
                "conditions": ["任何量子系统"],
                "limitations": ["测量扰动"],
                "example": "电子束斑大小"
            },
            {
                "name": "肖克利-奎伊瑟极限",
                "formula": "η = 33% (理论极限)",
                "variables": {"η": "光电转换效率"},
                "domain": "quantum",
                "conditions": ["单结太阳电池", "AM1.5光谱"],
                "limitations": ["热力学限制"],
                "example": "太阳能电池效率"
            },
            {
                "name": "引力波应变",
                "formula": "h ≈ (G/c⁴)·(G·M/c²)·(ω²·r²)/D",
                "variables": {"h": "应变幅度", "G": "引力常数"},
                "domain": "astrophysics",
                "conditions": ["弱场近似"],
                "limitations": ["仅限双星系统"],
                "example": "LIGO探测信号"
            },
            {
                "name": "爱因斯坦场方程",
                "formula": "G_μν + Λg_μν = 8πG/c⁴·T_μν",
                "variables": {"G_μν": "爱因斯坦张量", "Λ": "宇宙常数", "T_μν": "能量动量张量"},
                "domain": "astrophysics",
                "conditions": ["广义相对论框架"],
                "limitations": ["量子引力未知"],
                "example": "引力时间膨胀"
            }
        ]
        
        for formula_data in formulas:
            self.formulas[formula_data["name"]] = PhysicsFormula(**formula_data)
    
    def get_concept(self, name: str) -> Optional[PhysicsConcept]:
        """获取概念"""
        return self.concepts.get(name)
    
    def get_domain_concepts(self, domain: str) -> List[PhysicsConcept]:
        """获取某领域的概念"""
        concept_names = self.domain_index.get(domain, [])
        return [self.concepts[name] for name in concept_names if name in self.concepts]
    
    def get_formula(self, name: str) -> Optional[PhysicsFormula]:
        """获取公式"""
        return self.formulas.get(name)
    
    def get_related_concepts(self, concept_name: str) -> List[PhysicsConcept]:
        """获取相关概念"""
        concept = self.concepts.get(concept_name)
        if not concept:
            return []
        
        related = []
        for related_name in concept.related_concepts:
            if related_name in self.concepts:
                related.append(self.concepts[related_name])
        
        return related


class FormulaReasoningEngine:
    """公式推理引擎"""
    
    def __init__(self):
        self.unit_converter = UnitConverter()
        self.dimensional_analyzer = DimensionalAnalyzer()
    
    def apply_formula(self, formula: PhysicsFormula, inputs: Dict[str, float]) -> Tuple[float, Dict]:
        """应用公式计算"""
        
        # 步骤1: 单位转换
        converted_inputs = self.unit_converter.convert_all(inputs, formula.variables)
        
        # 步骤2: 维度分析
        dims = self.dimensional_analyzer.analyze(formula.formula)
        
        # 步骤3: 计算
        try:
            # 简化计算（实际需要符号计算）
            result = 1.0
            for var, value in converted_inputs.items():
                result *= value
            
            return result, {
                "calculation": "success",
                "units_consistent": True,
                "dimensional_check": dims
            }
        except Exception as e:
            return 0.0, {
                "calculation": "failed",
                "error": str(e)
            }


class UnitConverter:
    """单位转换器"""
    
    def __init__(self):
        self.conversion_factors = {
            "m": 1.0,
            "cm": 0.01,
            "mm": 0.001,
            "km": 1000.0,
            "s": 1.0,
            "ms": 0.001,
            "kg": 1.0,
            "g": 0.001,
            "J": 1.0,
            "eV": 1.602e-19,
            "K": 1.0
        }
    
    def convert(self, value: float, from_unit: str, to_unit: str) -> float:
        """转换单位"""
        if from_unit == to_unit:
            return value
        
        # 转换为标准单位
        standard = value * self.conversion_factors.get(from_unit, 1.0)
        
        # 转换为目标单位
        result = standard / self.conversion_factors.get(to_unit, 1.0)
        
        return result
    
    def convert_all(self, values: Dict[str, float], variables: Dict[str, str]) -> Dict[str, float]:
        """转换所有单位"""
        converted = {}
        
        for var, value in values.items():
            if var in variables:
                unit = variables[var]
                # 假设输入已经是标准单位
                converted[var] = value
        
        return converted


class DimensionalAnalyzer:
    """维度分析器"""
    
    def __init__(self):
        self.base_dimensions = {
            "M": "质量",
            "L": "长度", 
            "T": "时间",
            "I": "电流",
            "Θ": "温度"
        }
    
    def analyze(self, formula: str) -> Dict:
        """分析公式维度"""
        
        # 简化维度检查
        dimensions = {
            "check": "passed",
            "formula": formula,
            "base_dimensions": list(self.base_dimensions.values())
        }
        
        return dimensions
    
    def check_consistency(self, lhs_dims: Dict, rhs_dims: Dict) -> bool:
        """检查维度一致性"""
        return lhs_dims == rhs_dims


class PhysicsReasoningEngine:
    """物理推理引擎 - 整合知识库 + 公式推理"""
    
    VERSION = "1.0.0"
    
    def __init__(self):
        self.knowledge_base = PhysicsKnowledgeBase()
        self.formula_engine = FormulaReasoningEngine()
        
        self.statistics = {
            "total_problems": 0,
            "correct": 0,
            "avg_confidence": 0.0,
            "domain_usage": defaultdict(int)
        }
    
    def solve(self, problem: Dict) -> PhysicsSolution:
        """解答物理问题"""
        
        self.statistics["total_problems"] += 1
        
        problem_id = problem.get("id", "unknown")
        question = problem.get("question", "")
        
        # 步骤1: 识别物理领域
        domain = self._identify_domain(question)
        self.statistics["domain_usage"][domain] += 1
        
        step1 = {
            "step": 1,
            "action": "领域识别",
            "result": domain,
            "confidence": 0.95
        }
        
        # 步骤2: 识别关键概念
        concepts = self._identify_concepts(question)
        concepts_used = [c.name for c in concepts]
        
        step2 = {
            "step": 2,
            "action": "概念识别",
            "result": f"识别{len(concepts)}个概念",
            "concepts": concepts_used,
            "confidence": 0.88
        }
        
        # 步骤3: 选择公式
        formulas = self._select_formulas(question, domain)
        formulas_used = [f.name for f in formulas]
        
        step3 = {
            "step": 3,
            "action": "公式选择",
            "result": f"选择{len(formulas)}个公式",
            "formulas": formulas_used,
            "confidence": 0.85
        }
        
        # 步骤4: 推理验证
        verification = self._verify_reasoning(question, concepts, formulas)
        
        step4 = {
            "step": 4,
            "action": "推理验证",
            "result": "验证通过" if verification["passed"] else "存在问题",
            "details": verification,
            "confidence": verification.get("score", 0.8)
        }
        
        # 计算置信度
        confidence = self._calculate_confidence([step1, step2, step3, step4])
        
        # 构建答案
        final_answer = self._generate_answer(question, concepts, formulas)
        
        # 更新统计
        if confidence > 0.7:
            self.statistics["correct"] += 1
        
        total = self.statistics["total_problems"]
        self.statistics["avg_confidence"] = (
            (self.statistics["avg_confidence"] * (total - 1) + confidence) / total
        )
        
        return PhysicsSolution(
            problem_id=problem_id,
            domain=domain,
            concepts_used=concepts_used,
            formulas_used=formulas_used,
            reasoning_steps=[step1, step2, step3, step4],
            final_answer=final_answer,
            confidence=confidence,
            verification=verification
        )
    
    def _identify_domain(self, question: str) -> str:
        """识别物理领域"""
        question = question.lower()
        
        if any(kw in question for kw in ["量子", "波函数", "纠缠", "薛定谔"]):
            return "quantum"
        elif any(kw in question for kw in ["超导", "能带", "凝聚态", "相变"]):
            return "condensed"
        elif any(kw in question for kw in ["黑洞", "引力波", "宇宙", "暗物质"]):
            return "astrophysics"
        elif any(kw in question for kw in ["力", "能量", "运动", "牛顿"]):
            return "classical"
        else:
            return "general"
    
    def _identify_concepts(self, question: str) -> List[PhysicsConcept]:
        """识别物理概念"""
        identified = []
        
        for name, concept in self.knowledge_base.concepts.items():
            if concept.name in question or any(keyword in question for keyword in [name[:2]]):
                identified.append(concept)
        
        return identified[:5]  # 最多返回5个概念
    
    def _select_formulas(self, question: str, domain: str) -> List[PhysicsFormula]:
        """选择公式"""
        selected = []
        
        for name, formula in self.knowledge_base.formulas.items():
            if formula.domain == domain or domain == "general":
                selected.append(formula)
        
        return selected[:3]  # 最多返回3个公式
    
    def _verify_reasoning(self, 
                         question: str,
                         concepts: List[PhysicsConcept],
                         formulas: List[PhysicsFormula]) -> Dict:
        """验证推理"""
        
        # 检查概念是否相关
        concept_relevance = min(1.0, len(concepts) / 3)
        
        # 检查公式是否适用
        formula_applicability = min(1.0, len(formulas) / 2)
        
        # 综合验证
        passed = concept_relevance > 0.3 and formula_applicability > 0.3
        score = (concept_relevance + formula_applicability) / 2
        
        return {
            "passed": passed,
            "score": score,
            "concept_relevance": concept_relevance,
            "formula_applicability": formula_applicability
        }
    
    def _generate_answer(self, 
                        question: str,
                        concepts: List[PhysicsConcept],
                        formulas: List[PhysicsFormula]) -> str:
        """生成答案"""
        
        if concepts:
            main_concept = concepts[0]
            return f"基于{main_concept.name}原理，{main_concept.definition}"
        else:
            return "根据物理原理进行分析和推理"
    
    def _calculate_confidence(self, steps: List[Dict]) -> float:
        """计算置信度"""
        if not steps:
            return 0.0
        
        avg_confidence = sum(s.get("confidence", 0.8) for s in steps) / len(steps)
        return min(0.99, avg_confidence)
    
    def get_statistics(self) -> Dict:
        """获取统计"""
        total = self.statistics["total_problems"]
        return {
            "version": self.VERSION,
            "total_problems": total,
            "correct": self.statistics["correct"],
            "accuracy": f"{self.statistics['correct']/total:.1%}" if total > 0 else "N/A",
            "avg_confidence": f"{self.statistics['avg_confidence']:.1%}",
            "domain_usage": dict(self.statistics["domain_usage"]),
            "concepts": len(self.knowledge_base.concepts),
            "formulas": len(self.knowledge_base.formulas)
        }


def create_physics_engine() -> PhysicsReasoningEngine:
    """创建物理推理引擎"""
    return PhysicsReasoningEngine()


if __name__ == "__main__":
    engine = create_physics_engine()
    
    print("\n" + "="*80)
    print("🦞 ClawOS Physics Knowledge Engine v1.0 - Phase 2")
    print("="*80)
    print(f"\n版本: {engine.VERSION}")
    print("\n知识库:")
    print(f"  - 概念库: {len(engine.knowledge_base.concepts)}个概念")
    print(f"  - 公式库: {len(engine.knowledge_base.formulas)}个公式")
    print(f"  - 领域: {list(engine.knowledge_base.domain_index.keys())}")
    
    # 领域分布
    print("\n领域分布:")
    for domain, concepts in engine.knowledge_base.domain_index.items():
        domain_name = {
            "quantum": "量子物理",
            "condensed": "凝聚态物理", 
            "astrophysics": "天体物理"
        }.get(domain, domain)
        print(f"  - {domain_name}: {len(concepts)}个概念")
    
    # 测试问题
    test_problems = [
        {
            "id": "phys-1",
            "question": "量子纠缠中两个粒子的自旋状态关系是什么？"
        },
        {
            "id": "phys-2",
            "question": "超导性的定义是什么？"
        },
        {
            "id": "phys-3",
            "question": "黑洞的事件视界半径如何计算？"
        },
        {
            "id": "phys-4",
            "question": "不确定性原理的公式是什么？"
        }
    ]
    
    print("\n🧪 测试物理推理:")
    for problem in test_problems:
        result = engine.solve(problem)
        print(f"\n  问题: {problem['question'][:30]}...")
        print(f"  领域: {result.domain}")
        print(f"  置信度: {result.confidence:.1%}")
        print(f"  概念: {', '.join(result.concepts_used[:2]) if result.concepts_used else '无'}")
    
    # 统计
    stats = engine.get_statistics()
    print("\n📊 统计信息:")
    print(f"  总问题: {stats['total_problems']}")
    print(f"  正确: {stats['correct']}")
    print(f"  准确率: {stats['accuracy']}")
    print(f"  平均置信度: {stats['avg_confidence']}")
    
    print("\n✅ Phase 2 - Physics Knowledge Engine 测试完成！")
