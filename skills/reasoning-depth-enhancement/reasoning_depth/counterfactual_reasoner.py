# 🦞 Counterfactual Reasoner - 反事实推理

"""
反事实推理模块

功能:
- "如果...会怎样"分析
- 假设情景推理
- 替代方案评估
- 结果预测
"""

from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime


class CounterfactualType(Enum):
    """反事实类型"""
    REMOVAL = "removal"       # 移除某因素
    ADDITION = "addition"       # 添加新因素
    MODIFICATION = "modification"  # 修改某因素
    REPLACEMENT = "replacement"  # 替换某因素


@dataclass
class CounterfactualScenario:
    """反事实场景"""
    scenario_id: str
    original_fact: str       # 原始事实
    hypothetical_change: str  # 假设变化
    counterfactual_type: str  # 变化类型
    predicted_outcome: str   # 预测结果
    confidence: float        # 置信度
    reasoning: str           # 推理过程
    alternatives: List[str] = field(default_factory=list)


class CounterfactualReasoner:
    """反事实推理器"""
    
    # 反事实标记词
    COUNTERFACTUAL_MARKERS = [
        "如果", "假如", "要是", "假设",
        "假如说", "如果说", "若不是", "如果不是"
    ]
    
    # 结果预测模式
    OUTCOME_PATTERNS = [
        ("{X}不会发生", "Y会发生", "{X}不会发生，Y也不会发生"),
        ("{X}发生", "Y会发生", "{X}发生，Y会发生"),
        ("{X}增强", "Y增强", "{X}增强，Y会增强"),
        ("{X}减弱", "Y减弱", "{X}减弱，Y会减弱"),
    ]
    
    def __init__(self):
        self.scenarios: Dict[str, CounterfactualScenario] = {}
        self.scenario_counter = 0
        
        print("✅ CounterfactualReasoner 初始化完成")
    
    def identify_counterfactuals(self, question: str) -> List[str]:
        """
        识别问题中的反事实元素
        
        Args:
            question: 问题
            
        Returns:
            反事实元素列表
        """
        elements = []
        
        for marker in self.COUNTERFACTUAL_MARKERS:
            if marker in question:
                # 提取反事实部分
                parts = question.split(marker)
                if len(parts) == 2:
                    hypothetical = parts[1].strip()
                    elements.append({
                        "marker": marker,
                        "hypothesis": hypothetical,
                        "position": "after"
                    })
        
        return elements
    
    def analyze(
        self,
        fact: str,
        change: str,
        outcome_type: str = "removal"
    ) -> CounterfactualScenario:
        """
        分析反事实情景
        
        Args:
            fact: 原始事实
            change: 假设变化
            outcome_type: 变化类型
            
        Returns:
            CounterfactualScenario: 反事实场景
        """
        self.scenario_counter += 1
        scenario_id = f"cf_{self.scenario_counter}"
        
        scenario_type = self._identify_type(change)
        
        # 预测结果
        predicted_outcome, reasoning = self._predict_outcome(fact, change, scenario_type)
        
        # 生成替代方案
        alternatives = self._generate_alternatives(fact, change, scenario_type)
        
        scenario = CounterfactualScenario(
            scenario_id=scenario_id,
            original_fact=fact,
            hypothetical_change=change,
            counterfactual_type=scenario_type,
            predicted_outcome=predicted_outcome,
            confidence=0.70,
            reasoning=reasoning,
            alternatives=alternatives
        )
        
        self.scenarios[scenario_id] = scenario
        
        return scenario
    
    def _identify_type(self, change: str) -> str:
        """识别变化类型"""
        change_lower = change.lower()
        
        if "不" in change_lower or "没有" in change_lower:
            return CounterfactualType.REMOVAL.value
        elif "增加" in change_lower or "增强" in change_lower:
            return CounterfactualType.ADDITION.value
        elif "改变" in change_lower or "修改" in change_lower:
            return CounterfactualType.MODIFICATION.value
        elif "替换" in change_lower or "换成" in change_lower:
            return CounterfactualType.REPLACEMENT.value
        else:
            return CounterfactualType.MODIFICATION.value
    
    def _predict_outcome(
        self,
        fact: str,
        change: str,
        change_type: str
    ) -> Tuple[str, str]:
        """预测结果"""
        change_lower = change.lower()
        
        if change_type == CounterfactualType.REMOVAL.value:
            if "不" in change_lower:
                # 移除原因
                return (
                    f"原始结果可能不会发生",
                    f"因为{change}是导致结果的原因之一，移除后结果的可能性降低"
                )
            elif "没有" in change_lower:
                return (
                    f"结果可能完全不同",
                    f"如果{change}没有发生，整个因果链会断裂"
                )
        elif change_type == CounterfactualType.ADDITION.value:
            return (
                f"可能会产生新的结果",
                f"添加{change}可能会引入新的因果路径"
            )
        elif change_type == CounterfactualType.MODIFICATION.value:
            return (
                f"结果会相应改变",
                f"修改{change}会导致结果按比例变化"
            )
        else:
            return (
                f"结果会有条件地改变",
                f"替换{change}会改变因果机制"
            )
    
    def _generate_alternatives(
        self,
        fact: str,
        change: str,
        change_type: str
    ) -> List[str]:
        """生成替代方案"""
        alternatives = []
        
        if change_type == CounterfactualType.REMOVAL.value:
            alternatives = [
                f"保留{change}但改变其程度",
                f"用其他因素替代{change}",
                f"延迟{change}的发生时间"
            ]
        else:
            alternatives = [
                f"考虑{change}的不同程度",
                f"分析{change}的时机影响",
                f"探索{change}的替代实现方式"
            ]
        
        return alternatives
    
    def compare_scenarios(
        self,
        original: str,
        counterfactual: str
    ) -> Dict:
        """
        比较原始情景和反事实情景
        
        Args:
            original: 原始情景
            counterfactual: 反事实情景
            
        Returns:
            比较结果
        """
        return {
            "original": original,
            "counterfactual": counterfactual,
            "differences": self._identify_differences(original, counterfactual),
            "implications": self._analyze_implications(original, counterfactual)
        }
    
    def _identify_differences(
        self,
        original: str,
        counterfactual: str
    ) -> List[str]:
        """识别差异"""
        diffs = []
        
        # 简单词级别比较
        orig_words = set(original.split())
        cf_words = set(counterfactual.split())
        
        added = cf_words - orig_words
        removed = orig_words - cf_words
        
        if added:
            diffs.append(f"新增: {' '.join(list(added)[:5])}")
        if removed:
            diffs.append(f"移除: {' '.join(list(removed)[:5])}")
        
        return diffs
    
    def _analyze_implications(
        self,
        original: str,
        counterfactual: str
    ) -> List[str]:
        """分析影响"""
        return [
            f"原始情景和反事实情景存在显著差异",
            "需要进一步分析因果关系",
            "反事实推理可以帮助理解因果机制"
        ]
    
    def what_if_analysis(
        self,
        condition: str,
        consequence: str
    ) -> Dict:
        """
        "如果...会怎样"分析
        
        Args:
            condition: 条件
            consequence: 后果
            
        Returns:
            分析结果
        """
        return {
            "condition": condition,
            "consequence": consequence,
            "analysis": f"如果{condition}，则{consequence}",
            "confidence": 0.75,
            "reasoning": f"基于条件与后果的逻辑关系",
            "alternatives": [
                f"如果{condition}不成立",
                f"如果{condition}程度不同"
            ]
        }
    
    def get_scenario(self, scenario_id: str) -> Optional[CounterfactualScenario]:
        """获取场景"""
        return self.scenarios.get(scenario_id)
    
    def get_all_scenarios(self) -> List[CounterfactualScenario]:
        """获取所有场景"""
        return list(self.scenarios.values())
    
    def get_stats(self) -> Dict:
        """获取统计"""
        by_type = {}
        for scenario in self.scenarios.values():
            t = scenario.counterfactual_type
            by_type[t] = by_type.get(t, 0) + 1
        
        return {
            "total_scenarios": len(self.scenarios),
            "by_type": by_type,
            "avg_confidence": self._avg_confidence()
        }
    
    def _avg_confidence(self) -> float:
        """计算平均置信度"""
        if not self.scenarios:
            return 0.0
        return sum(s.confidence for s in self.scenarios.values()) / len(self.scenarios)


# 测试
if __name__ == "__main__":
    reasoner = CounterfactualReasoner()
    
    questions = [
        "如果天下雨，地会湿吗？",
        "假如我没有去，结果会怎样？",
        "要是当初努力学习，现在会怎样？"
    ]
    
    print("🦞 反事实推理测试\n")
    
    for q in questions:
        print(f"问题: {q}")
        elements = reasoner.identify_counterfactuals(q)
        print(f"  反事实元素: {elements}\n")
    
    # 分析具体场景
    scenario = reasoner.analyze(
        fact="努力学习",
        change="不努力学习",
        outcome_type="removal"
    )
    
    print(f"场景分析:")
    print(f"  原始: {scenario.original_fact}")
    print(f"  假设: {scenario.hypothetical_change}")
    print(f"  预测: {scenario.predicted_outcome}")
    print(f"  置信度: {scenario.confidence:.0%}")
    print(f"  替代: {scenario.alternatives}")
    
    print(f"\n统计: {reasoner.get_stats()}")
