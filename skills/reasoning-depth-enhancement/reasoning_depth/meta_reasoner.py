# 🦞 Meta Reasoner - 元推理

"""
元推理模块

功能:
- 推理策略选择
- 推理质量评估
- 推理过程反思
- 自适应推理
"""

from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime


class ReasoningStrategy(Enum):
    """推理策略"""
    DIRECT = "direct"           # 直接推理
    CHAIN = "chain"             # 链式推理
    CAUSAL = "causal"          # 因果推理
    COUNTERFACTUAL = "counterfactual"  # 反事实推理
    ANALOGICAL = "analogical"    # 类比推理
    ABDUCTIVE = "abductive"     # 溯因推理


@dataclass
class MetaReasoning:
    """元推理结果"""
    strategy: str                # 选择的策略
    confidence: float            # 策略置信度
    reasoning_quality: float     # 推理质量评估
    alternatives: List[str] = field(default_factory=list)
    reflections: List[str] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)


@dataclass
class ReasoningAttempt:
    """推理尝试"""
    attempt_id: str
    strategy: str
    reasoning: str
    result: str
    quality: float
    feedback: str = ""


class MetaReasoner:
    """元推理器"""
    
    # 问题复杂度指标
    COMPLEXITY_INDICATORS = {
        "high": ["如果", "那么", "因为", "所以", "但是", "或者", "多步", "为什么"],
        "medium": ["是否", "能不能", " 어떻게"],
        "low": ["是什么", "哪个", "多少"]
    }
    
    # 策略适用场景
    STRATEGY_SUITABILITY = {
        ReasoningStrategy.DIRECT: ["是什么", "定义", "简单"],
        ReasoningStrategy.CHAIN: ["如果", "那么", "推理"],
        ReasoningStrategy.CAUSAL: ["因为", "所以", "导致"],
        ReasoningStrategy.COUNTERFACTUAL: ["如果", "假如", "要是"],
        ReasoningStrategy.ANALOGICAL: ["像", "类似", "如同"],
        ReasoningStrategy.ABDUCTIVE: ["可能", "最好的解释"],
    }
    
    def __init__(self):
        self.attempts: Dict[str, ReasoningAttempt] = {}
        self.attempt_counter = 0
        self.strategy_success_rates: Dict[str, float] = {}
        
        print("✅ MetaReasoner 初始化完成")
    
    def analyze_question(self, question: str) -> MetaReasoning:
        """
        分析问题并选择推理策略
        
        Args:
            question: 问题
            
        Returns:
            MetaReasoning: 元推理结果
        """
        # 1. 评估问题复杂度
        complexity = self._assess_complexity(question)
        
        # 2. 评估推理质量要求
        quality_requirement = self._assess_quality_requirement(question)
        
        # 3. 选择最佳策略
        best_strategy, strategy_confidence = self._select_strategy(question)
        
        # 4. 生成替代策略
        alternatives = self._generate_alternatives(question, best_strategy)
        
        # 5. 生成反思
        reflections = self._generate_reflections(question, best_strategy)
        
        # 6. 生成建议
        suggestions = self._generate_suggestions(question, best_strategy)
        
        return MetaReasoning(
            strategy=best_strategy.value,
            confidence=strategy_confidence,
            reasoning_quality=quality_requirement,
            alternatives=alternatives,
            reflections=reflections,
            suggestions=suggestions
        )
    
    def _assess_complexity(self, question: str) -> str:
        """评估问题复杂度"""
        question_lower = question.lower()
        
        high_count = sum(1 for kw in self.COMPLEXITY_INDICATORS["high"] if kw in question_lower)
        medium_count = sum(1 for kw in self.COMPLEXITY_INDICATORS["medium"] if kw in question_lower)
        
        if high_count >= 2:
            return "high"
        elif medium_count >= 1:
            return "medium"
        return "low"
    
    def _assess_quality_requirement(self, question: str) -> float:
        """评估推理质量要求"""
        question_lower = question.lower()
        
        # 因果关系需要高质量
        if any(kw in question_lower for kw in ["为什么", "原因", "导致"]):
            return 0.90
        # 预测类问题
        elif any(kw in question_lower for kw in ["会怎样", "如果"]):
            return 0.85
        # 解释类问题
        elif any(kw in question_lower for kw in ["解释", "说明"]):
            return 0.80
        # 简单问题
        else:
            return 0.70
    
    def _select_strategy(
        self,
        question: str
    ) -> Tuple[ReasoningStrategy, float]:
        """选择推理策略"""
        question_lower = question.lower()
        
        # 评分各策略
        scores = {}
        
        for strategy in ReasoningStrategy:
            score = 0.0
            
            # 匹配关键词
            for keyword in self.STRATEGY_SUITABILITY.get(strategy, []):
                if keyword in question_lower:
                    score += 0.3
            
            # 复杂度匹配
            complexity = self._assess_complexity(question)
            if complexity == "high" and strategy in [
                ReasoningStrategy.CHAIN,
                ReasoningStrategy.CAUSAL
            ]:
                score += 0.2
            elif complexity == "low" and strategy == ReasoningStrategy.DIRECT:
                score += 0.2
            
            # 记录分数
            scores[strategy] = min(0.95, score)
        
        # 选择最高分
        best_strategy = max(scores, key=scores.get)
        
        return best_strategy, scores.get(best_strategy, 0.5)
    
    def _generate_alternatives(
        self,
        question: str,
        selected: ReasoningStrategy
    ) -> List[str]:
        """生成替代策略"""
        alternatives = []
        
        for strategy in ReasoningStrategy:
            if strategy != selected:
                alternatives.append(strategy.value)
        
        # 排序：优先推荐直接替代
        return alternatives[:3]
    
    def _generate_reflections(
        self,
        question: str,
        selected: ReasoningStrategy
    ) -> List[str]:
        """生成推理反思"""
        reflections = []
        
        reflections.append(
            f"选择{selected.value}推理，因为问题涉及{self._assess_complexity(question)}复杂度"
        )
        
        if self._assess_complexity(question) == "high":
            reflections.append(
                "这个问题可能需要多步推理，建议分解为子问题"
            )
        
        reflections.append(
            f"推理过程中应关注{selected.value}推理的关键前提"
        )
        
        return reflections
    
    def _generate_suggestions(
        self,
        question: str,
        selected: ReasoningStrategy
    ) -> List[str]:
        """生成推理建议"""
        suggestions = []
        
        if selected == ReasoningStrategy.CHAIN:
            suggestions = [
                "将问题分解为多个推理步骤",
                "验证每步推理的有效性",
                "确保步骤间的逻辑连贯性"
            ]
        elif selected == ReasoningStrategy.CAUSAL:
            suggestions = [
                "明确因果关系的方向",
                "寻找因果机制的证据",
                "考虑因果关系的强度"
            ]
        elif selected == ReasoningStrategy.COUNTERFACTUAL:
            suggestions = [
                "明确假设的变化点",
                "分析因果链的断裂点",
                "预测替代结果"
            ]
        elif selected == ReasoningStrategy.ANALOGICAL:
            suggestions = [
                "明确类比的前提",
                "分析类比的相似性",
                "评估类比的可迁移性"
            ]
        else:
            suggestions = [
                "直接给出答案",
                "必要时提供解释"
            ]
        
        return suggestions
    
    def evaluate_attempt(
        self,
        strategy: str,
        reasoning: str,
        result: str
    ) -> ReasoningAttempt:
        """
        评估推理尝试
        
        Args:
            strategy: 使用的策略
            reasoning: 推理过程
            result: 推理结果
            
        Returns:
            ReasoningAttempt: 推理尝试
        """
        self.attempt_counter += 1
        attempt_id = f"attempt_{self.attempt_counter}"
        
        # 评估质量
        quality = self._evaluate_quality(reasoning, result)
        
        # 生成反馈
        feedback = self._generate_feedback(strategy, quality)
        
        attempt = ReasoningAttempt(
            attempt_id=attempt_id,
            strategy=strategy,
            reasoning=reasoning,
            result=result,
            quality=quality,
            feedback=feedback
        )
        
        self.attempts[attempt_id] = attempt
        
        # 更新策略成功率
        if strategy not in self.strategy_success_rates:
            self.strategy_success_rates[strategy] = quality
        else:
            # 移动平均
            self.strategy_success_rates[strategy] = (
                0.7 * self.strategy_success_rates[strategy] +
                0.3 * quality
            )
        
        return attempt
    
    def _evaluate_quality(self, reasoning: str, result: str) -> float:
        """评估推理质量"""
        quality = 0.5  # 基础分
        
        # 推理长度
        if len(reasoning) > 50:
            quality += 0.1
        if len(reasoning) > 100:
            quality += 0.1
        
        # 包含推理标志词
        reasoning_markers = ["因为", "所以", "如果", "那么", "因此"]
        for marker in reasoning_markers:
            if marker in reasoning:
                quality += 0.05
        
        # 结果合理性
        if len(result) > 5:
            quality += 0.1
        
        return min(0.95, quality)
    
    def _generate_feedback(self, strategy: str, quality: float) -> str:
        """生成反馈"""
        if quality >= 0.85:
            return f"使用{strategy}策略的推理质量优秀"
        elif quality >= 0.70:
            return f"使用{strategy}策略的推理质量良好"
        elif quality >= 0.50:
            return f"使用{strategy}策略的推理质量一般，建议改进推理过程"
        else:
            return f"使用{strategy}策略的推理质量较低，建议尝试其他策略"
    
    def learn_from_attempts(self) -> Dict:
        """从尝试中学习"""
        if not self.attempts:
            return {"message": "没有足够的尝试记录"}
        
        # 找出最佳策略
        best_strategy = max(
            self.strategy_success_rates.items(),
            key=lambda x: x[1]
        )
        
        # 分析失败模式
        failed_attempts = [
            a for a in self.attempts.values()
            if a.quality < 0.60
        ]
        
        return {
            "best_strategy": best_strategy[0],
            "best_confidence": best_strategy[1],
            "total_attempts": len(self.attempts),
            "failed_attempts": len(failed_attempts),
            "success_rate": len(self.attempts) / (len(failed_attempts) + 1)
        }
    
    def get_stats(self) -> Dict:
        """获取统计"""
        return {
            "total_attempts": len(self.attempts),
            "strategy_success_rates": self.strategy_success_rates,
            "learning_result": self.learn_from_attempts()
        }


# 测试
if __name__ == "__main__":
    reasoner = MetaReasoner()
    
    questions = [
        "如果A大于B，B大于C，那么A大于C吗？",
        "因为下雨，所以地湿了，这是为什么？",
        "假如地球是方的，会怎样？",
        "什么是人工智能？",
    ]
    
    print("🦞 元推理测试\n")
    
    for q in questions:
        print(f"问题: {q}")
        result = reasoner.analyze_question(q)
        
        print(f"  策略: {result.strategy} ({result.confidence:.0%})")
        print(f"  质量要求: {result.reasoning_quality:.0%}")
        print(f"  反思: {result.reflections[0]}")
        print(f"  建议: {result.suggestions[0] if result.suggestions else '无'}")
        print()
    
    print(f"\n统计: {reasoner.get_stats()}")
