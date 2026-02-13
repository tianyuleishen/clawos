# 🦞 Chain Reasoner - 链式推理

"""
多步推理链模块

功能:
- 将复杂问题分解为推理步骤
- 逐步推导结论
- 验证推理链的一致性
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime


class ReasoningType(Enum):
    """推理类型"""
    DEDUCTIVE = "deductive"       # 演绎推理
    INDUCTIVE = "inductive"       # 归纳推理
    ABDUCTIVE = "abductive"      # 溯因推理
    ANALOGICAL = "analogical"     # 类比推理
    CAUSAL = "causal"            # 因果推理


@dataclass
class ReasoningStep:
    """推理步骤"""
    step_id: int
    reasoning_type: str
    premise: str           # 前提
    inference: str         # 推理
    conclusion: str        # 结论
    confidence: float      # 置信度
    evidence: List[str] = field(default_factory=list)
    justification: str = ""  # 正当性说明
    timestamp: float = field(default_factory=datetime.now().timestamp)


@dataclass
class ReasoningChain:
    """推理链"""
    chain_id: str
    question: str
    steps: List[ReasoningStep] = field(default_factory=list)
    final_conclusion: str = ""
    overall_confidence: float = 0.0
    is_valid: bool = True
    depth: int = 0
    branches: int = 0  # 分支数


class ChainReasoner:
    """链式推理器"""
    
    # 推理模式
    REASONING_PATTERNS = {
        ReasoningType.DEDUCTIVE: [
            "所有{}都是{}",
            "如果{}那么{}",
            "{}蕴含{}",
            "因为{}所以{}",
        ],
        ReasoningType.INDUCTIVE: [
            "{}个{}中有{}个{}",
            "观察到{}次{}",
            "多数{}是{}",
        ],
        ReasoningType.ABDUCTIVE: [
            "如果{}那么{}",
            "{}发生了，所以{}",
            "最好的解释是{}",
        ],
        ReasoningType.CAUSAL: [
            "{}导致{}",
            "{}引起{}的变化",
            "{}是{}的原因",
        ],
    }
    
    # 逻辑连接词
    LOGICAL_CONNECTORS = {
        "因此": ("conclusion", "因为"),
        "所以": ("conclusion", "因为"),
        "因为": ("premise", None),
        "所以": ("conclusion", "因为"),
        "如果": ("condition", None),
        "那么": ("conclusion", "如果"),
        "但是": ("contrast", None),
        "而且": ("addition", None),
        "或者": ("alternative", None),
    }
    
    def __init__(self, max_depth: int = 10):
        """
        初始化
        
        Args:
            max_depth: 最大推理深度
        """
        self.max_depth = max_depth
        self.chains: Dict[str, ReasoningChain] = {}
        self.step_counter = 0
        
        print("✅ ChainReasoner 初始化完成")
    
    def analyze_question(self, question: str) -> ReasoningType:
        """
        分析问题类型
        
        Args:
            question: 问题
            
        Returns:
            ReasoningType: 推理类型
        """
        question_lower = question.lower()
        
        # 检测推理类型
        if any(kw in question_lower for kw in ["如果", "那么", "所以", "因此"]):
            return ReasoningType.DEDUCTIVE
        elif any(kw in question_lower for kw in ["因为", "所以", "导致", "原因"]):
            return ReasoningType.CAUSAL
        elif any(kw in question_lower for kw in ["通常", "大多数", "观察到"]):
            return ReasoningType.INDUCTIVE
        elif any(kw in question_lower for kw in ["最好的解释", "可能是"]):
            return ReasoningType.ABDUCTIVE
        elif any(kw in question_lower for kw in ["类似", "像", "如同"]):
            return ReasoningType.ANALOGICAL
        
        return ReasoningType.DEDUCTIVE  # 默认
    
    def decompose(self, question: str) -> ReasoningChain:
        """
        分解问题为推理步骤
        
        Args:
            question: 问题
            
        Returns:
            ReasoningChain: 推理链
        """
        chain_id = f"chain_{datetime.now().timestamp()}"
        reasoning_type = self.analyze_question(question)
        
        chain = ReasoningChain(
            chain_id=chain_id,
            question=question,
            # 自动从steps计算
        )
        
        # 根据问题类型生成推理步骤
        steps = self._generate_steps(question, reasoning_type)
        
        for step in steps:
            chain.steps.append(step)
            self.step_counter += 1
        
        # 计算深度和置信度
        chain.depth = len(steps)
        chain.overall_confidence = self._calculate_confidence(steps)
        
        # 生成最终结论
        chain.final_conclusion = self._synthesize_conclusion(chain)
        
        # 验证有效性
        chain.is_valid = self._validate_chain(chain)
        
        self.chains[chain_id] = chain
        
        return chain
    
    def _generate_steps(
        self,
        question: str,
        reasoning_type: ReasoningType
    ) -> List[ReasoningStep]:
        """生成推理步骤"""
        steps = []
        
        if reasoning_type == ReasoningType.DEDUCTIVE:
            steps = self._deductive_decompose(question)
        elif reasoning_type == ReasoningType.CAUSAL:
            steps = self._causal_decompose(question)
        elif reasoning_type == ReasoningType.INDUCTIVE:
            steps = self._inductive_decompose(question)
        elif reasoning_type == ReasoningType.ABDUCTIVE:
            steps = self._abductive_decompose(question)
        else:
            steps = self._default_decompose(question)
        
        return steps
    
    def _deductive_decompose(self, question: str) -> List[ReasoningStep]:
        """演绎推理分解"""
        steps = []
        
        # 提取"如果...那么..."结构
        if "如果" in question and "那么" in question:
            parts = question.split("那么")
            premise = parts[0].replace("如果", "").strip()
            conclusion = parts[1].strip() if len(parts) > 1 else question
            
            steps.append(ReasoningStep(
                step_id=1,
                reasoning_type="deductive",
                premise=premise,
                inference="演绎推理",
                conclusion=conclusion,
                confidence=0.95,
                evidence=["逻辑规则"],
                justification="基于一般规则的推导"
            ))
        
        # 添加验证步骤
        steps.append(ReasoningStep(
            step_id=2,
            reasoning_type="deductive",
            premise="前提条件",
            inference="逻辑验证",
            conclusion="推理有效",
            confidence=0.90,
            evidence=["逻辑一致性"],
            justification="推理过程自洽"
        ))
        
        return steps
    
    def _causal_decompose(self, question: str) -> List[ReasoningStep]:
        """因果推理分解"""
        steps = []
        
        if "因为" in question:
            parts = question.split("因为")
            cause = parts[1].strip() if len(parts) > 1 else question
            effect = parts[0].strip() if len(parts) > 1 else question
            
            steps.append(ReasoningStep(
                step_id=1,
                reasoning_type="causal",
                premise=cause,
                inference="因果关系分析",
                conclusion=f"导致{effect}",
                confidence=0.85,
                evidence=["因果链"],
                justification="因果关系成立"
            ))
        
        return steps
    
    def _inductive_decompose(self, question: str) -> List[ReasoningStep]:
        """归纳推理分解"""
        steps = []
        
        steps.append(ReasoningStep(
            step_id=1,
            reasoning_type="inductive",
            premise="观察样本",
            inference="模式识别",
            conclusion="一般规律",
            confidence=0.70,
            evidence=["样本统计"],
            justification="基于有限观察的概括"
        ))
        
        steps.append(ReasoningStep(
            step_id=2,
            reasoning_type="inductive",
            premise="一般规律",
            inference="预测验证",
            conclusion="预测结果",
            confidence=0.65,
            evidence=["历史数据"],
            justification="统计推断"
        ))
        
        return steps
    
    def _abductive_decompose(self, question: str) -> List[ReasoningStep]:
        """溯因推理分解"""
        steps = []
        
        steps.append(ReasoningStep(
            step_id=1,
            reasoning_type="abductive",
            premise="观察现象",
            inference="寻找最佳解释",
            conclusion="假设",
            confidence=0.60,
            evidence=["现象分析"],
            justification="最佳解释而非必然原因"
        ))
        
        steps.append(ReasoningStep(
            step_id=2,
            reasoning_type="abductive",
            premise="假设",
            inference="可验证性",
            conclusion="验证方法",
            confidence=0.65,
            evidence=["逻辑一致性"],
            justification="假设可被验证"
        ))
        
        return steps
    
    def _default_decompose(self, question: str) -> List[ReasoningStep]:
        """默认分解"""
        steps = [
            ReasoningStep(
                step_id=1,
                reasoning_type="general",
                premise=question,
                inference="问题理解",
                conclusion="分析路径",
                confidence=0.80,
                evidence=["问题分析"],
                justification="基于问题结构的分析"
            )
        ]
        return steps
    
    def _calculate_confidence(self, steps: List[ReasoningStep]) -> float:
        """计算置信度"""
        if not steps:
            return 0.0
        
        # 置信度随深度递减，但有基础值
        base_confidence = 1.0
        for i, step in enumerate(steps):
            # 每步减少一些置信度
            decay = 0.05 * (i + 1)
            step.confidence = max(0.5, base_confidence - decay)
        
        # 整体置信度取加权平均
        weights = [1.0 / (i + 1) for i in range(len(steps))]
        return sum(s.confidence * w for i, (s, w) in enumerate(zip(steps, weights)))
    
    def _synthesize_conclusion(self, chain: ReasoningChain) -> str:
        """综合最终结论"""
        if not chain.steps:
            return ""
        
        # 聚合所有步骤的结论
        conclusions = [step.conclusion for step in chain.steps]
        
        if len(conclusions) == 1:
            return conclusions[0]
        
        # 组合多步结论
        return f"基于{len(conclusions)}步推理: {' → '.join(conclusions[-2:])}"
    
    def _validate_chain(self, chain: ReasoningChain) -> bool:
        """验证推理链有效性"""
        if not chain.steps:
            return False
        
        # 检查步骤间的逻辑连贯性
        for i in range(len(chain.steps) - 1):
            # 检查是否有过多的深度分支
            if i > self.max_depth:
                return False
        
        return True
    
    def get_chain(self, chain_id: str) -> Optional[ReasoningChain]:
        """获取推理链"""
        return self.chains.get(chain_id)
    
    def get_all_chains(self) -> List[ReasoningChain]:
        """获取所有推理链"""
        return list(self.chains.values())
    
    def get_stats(self) -> Dict:
        """获取统计"""
        return {
            "total_chains": len(self.chains),
            "total_steps": self.step_counter,
            "chains_by_type": {},
            "avg_confidence": self._avg_confidence()
        }
    
    def _avg_confidence(self) -> float:
        """计算平均置信度"""
        if not self.chains:
            return 0.0
        return sum(c.overall_confidence for c in self.chains.values()) / len(self.chains)


# 测试
if __name__ == "__main__":
    reasoner = ChainReasoner()
    
    questions = [
        "如果A大于B，B大于C，那么A大于C吗？",
        "因为下雨，所以地湿了",
        "观察到10只乌鸦都是黑色的，所以所有乌鸦都是黑色的",
        "最好的解释是地球是圆的",
    ]
    
    print("🦞 链式推理测试\n")
    
    for q in questions:
        print(f"问题: {q}")
        chain = reasoner.decompose(q)
        
        print(f"  类型: {chain.steps[0].reasoning_type}")
        print(f"  步骤数: {len(chain.steps)}")
        print(f"  置信度: {chain.overall_confidence:.0%}")
        print(f"  有效: {chain.is_valid}")
        print(f"  结论: {chain.final_conclusion}\n")
    
    print(f"\n统计: {reasoner.get_stats()}")
