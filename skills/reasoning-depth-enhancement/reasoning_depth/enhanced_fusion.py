# 🦞 Enhanced Fusion Engine - 增强融合推理引擎

"""
增强融合推理引擎

集成:
- 链式推理
- 因果分析
- 反事实推理
- 元推理

增强ClawOS终极融合推理引擎
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import asyncio


class EnhancedTaskType(Enum):
    """增强任务类型"""
    # 原有类型
    LOGIC = "logic"
    REASONING = "reasoning"
    MATH = "math"
    GENERAL = "general"
    
    # 新增类型
    CHAIN_REASONING = "chain_reasoning"      # 链式推理
    CAUSAL_ANALYSIS = "causal_analysis"    # 因果分析
    COUNTERFACTUAL = "counterfactual"       # 反事实推理
    META_REASONING = "meta_reasoning"        # 元推理
    MULTI_STEP = "multi_step"              # 多步推理
    ABDUCTIVE = "abductive"                # 溯因推理


@dataclass
class EnhancedAnalysisResult:
    """增强分析结果"""
    result: str
    confidence: float
    engine_used: str
    task_type: str
    processing_time: float
    
    # 新增字段
    reasoning_chain: List[Dict] = field(default_factory=list)
    causal_chain: Dict = field(default_factory=dict)
    counterfactual_analysis: Dict = field(default_factory=dict)
    meta_reasoning: Dict = field(default_factory=dict)
    
    # 质量指标
    depth: int = 0
    steps_count: int = 0
    alternatives_count: int = 0


class EnhancedFusionEngine:
    """增强融合推理引擎"""
    
    def __init__(self):
        self.version = "2.0.0"
        
        # 初始化子引擎
        from .chain_reasoner import ChainReasoner
        from .causal_analyzer import CausalAnalyzer
        from .counterfactual_reasoner import CounterfactualReasoner
        from .meta_reasoner import MetaReasoner
        
        self.chain_reasoner = ChainReasoner()
        self.causal_analyzer = CausalAnalyzer()
        self.counterfactual_reasoner = CounterfactualReasoner()
        self.meta_reasoner = MetaReasoner()
        
        # 初始化原有引擎
        self._init_original_engines()
        
        print("\n🦞 Enhanced Fusion Engine v2.0.0 初始化完成")
        print("融合增强推理引擎:")
        print("  ├── ChainReasoner (多步推理)")
        print("  ├── CausalAnalyzer (因果分析)")
        print("  ├── CounterfactualReasoner (反事实推理)")
        print("  └── MetaReasoner (元推理)")
    
    def _init_original_engines(self):
        """初始化原有引擎"""
        # 简化版原有引擎
        self.logic_engine = lambda x: (f"逻辑分析: {x}", 1.0)
        self.ruletaker = lambda x: (f"规则推理: {x}", 1.0)
        self.math_engine = lambda x: (f"数学求解: {x}", 0.83)
        self.reasoning_engine = lambda x: (f"推理分析: {x}", 0.688)
    
    async def analyze(self, task: str) -> EnhancedAnalysisResult:
        """
        综合分析任务
        
        Args:
            task: 任务描述
            
        Returns:
            EnhancedAnalysisResult: 分析结果
        """
        import time
        start_time = time.time()
        
        # 1. 元推理分析
        meta = self.meta_reasoner.analyze_question(task)
        
        # 2. 检测任务类型
        task_type = self._detect_task_type(task)
        
        # 3. 根据任务类型选择推理方法
        result = ""
        confidence = 0.0
        engine_used = "enhanced_fusion"
        
        if task_type in [
            EnhancedTaskType.CHAIN_REASONING,
            EnhancedTaskType.MULTI_STEP
        ]:
            # 链式推理
            chain = self.chain_reasoner.decompose(task)
            result = chain.final_conclusion
            confidence = chain.overall_confidence
            engine_used = "chain_reasoner"
            
            reasoning_chain = [
                {
                    "step_id": s.step_id,
                    "type": s.reasoning_type,
                    "premise": s.premise,
                    "inference": s.inference,
                    "conclusion": s.conclusion,
                    "confidence": s.confidence
                }
                for s in chain.steps
            ]
        
        elif task_type == EnhancedTaskType.CAUSAL_ANALYSIS:
            # 因果分析
            causes = self.causal_analyzer.extract_causes(task)
            if causes:
                cause, effect, conf = causes[0]
                chain = self.causal_analyzer.build_chain(cause, effect)
                
                result = f"因果关系: {cause} → {effect}"
                confidence = conf
                engine_used = "causal_analyzer"
                
                causal_chain = {
                    "root_cause": chain.root_cause,
                    "final_effect": chain.final_effect,
                    "total_strength": chain.total_strength,
                    "is_direct": chain.is_direct
                }
        
        elif task_type == EnhancedTaskType.COUNTERFACTUAL:
            # 反事实推理
            elements = self.counterfactual_reasoner.identify_counterfactuals(task)
            if elements:
                elem = elements[0]
                scenario = self.counterfactual_reasoner.analyze(
                    elem.get("hypothesis", ""),
                    "结果变化"
                )
                
                result = scenario.predicted_outcome
                confidence = scenario.confidence
                engine_used = "counterfactual_reasoner"
                
                counterfactual_analysis = {
                    "original_fact": scenario.original_fact,
                    "hypothetical_change": scenario.hypothetical_change,
                    "predicted_outcome": scenario.predicted_outcome,
                    "alternatives": scenario.alternatives
                }
        
        elif task_type == EnhancedTaskType.ABDUCTIVE:
            # 溯因推理
            best_strategy = meta.strategy
            result = f"最佳解释: {task}"
            confidence = 0.60
            engine_used = "abductive_reasoning"
        
        else:
            # 使用原有引擎
            result, confidence = self._use_original_engine(task_type, task)
            reasoning_chain = []
        
        # 4. 使用元推理增强结果
        meta_reasoning = {
            "selected_strategy": meta.strategy,
            "confidence": meta.confidence,
            "reflections": meta.reflections,
            "suggestions": meta.suggestions
        }
        
        processing_time = time.time() - start_time
        
        return EnhancedAnalysisResult(
            result=result,
            confidence=confidence,
            engine_used=engine_used,
            task_type=task_type.value,
            processing_time=processing_time,
            reasoning_chain=reasoning_chain if 'reasoning_chain' in dir() else [],
            causal_chain=causal_chain if 'causal_chain' in dir() else {},
            counterfactual_analysis=counterfactual_analysis if 'counterfactual_analysis' in dir() else {},
            meta_reasoning=meta_reasoning,
            depth=len(reasoning_chain) if 'reasoning_chain' in dir() else 0,
            steps_count=len(reasoning_chain) if 'reasoning_chain' in dir() else 0,
            alternatives_count=len(meta.alternatives)
        )
    
    def _detect_task_type(self, task: str) -> EnhancedTaskType:
        """检测任务类型"""
        task_lower = task.lower()
        
        # 反事实检测
        if any(kw in task_lower for kw in ["如果", "假如", "要是"]):
            return EnhancedTaskType.COUNTERFACTUAL
        
        # 因果检测
        if any(kw in task_lower for kw in ["因为", "所以", "导致", "原因"]):
            return EnhancedTaskType.CAUSAL_ANALYSIS
        
        # 链式推理检测
        if any(kw in task_lower for kw in ["如果", "那么", "推理"]):
            return EnhancedTaskType.CHAIN_REASONING
        
        # 多步推理检测
        if any(kw in task_lower for kw in ["首先", "然后", "最后", "步骤"]):
            return EnhancedTaskType.MULTI_STEP
        
        # 溯因检测
        if any(kw in task_lower for kw in ["可能", "解释", "为什么"]):
            return EnhancedTaskType.ABDUCTIVE
        
        # 数学检测
        if any(kw in task_lower for kw in ["计算", "等于", "+", "-", "*", "/"]):
            return EnhancedTaskType.MATH
        
        # 逻辑检测
        if any(kw in task_lower for kw in ["如果", "所有", "有些"]):
            return EnhancedTaskType.LOGIC
        
        return EnhancedTaskType.GENERAL
    
    def _use_original_engine(
        self,
        task_type: EnhancedTaskType,
        task: str
    ) -> Tuple[str, float]:
        """使用原有引擎"""
        if task_type == EnhancedTaskType.MATH:
            return self.math_engine(task)
        elif task_type == EnhancedTaskType.LOGIC:
            return self.logic_engine(task)
        else:
            return self.reasoning_engine(task)
    
    def get_engine_info(self) -> Dict:
        """获取引擎信息"""
        return {
            "version": self.version,
            "engines": {
                "chain_reasoner": self.chain_reasoner.get_stats(),
                "causal_analyzer": self.causal_analyzer.get_stats(),
                "counterfactual_reasoner": self.counterfactual_reasoner.get_stats(),
                "meta_reasoner": self.meta_reasoner.get_stats()
            }
        }


# 测试
if __name__ == "__main__":
    async def test():
        engine = EnhancedFusionEngine()
        
        tests = [
            "如果A大于B，B大于C，那么A大于C吗？",
            "因为下雨，所以地湿了",
            "假如地球是方的，会怎样？",
            "努力学习的步骤是什么？",
            "观察到这个现象，最好的解释是什么？",
        ]
        
        print("🦞 Enhanced Fusion Engine 测试\n")
        
        for task in tests:
            print(f"问题: {task}")
            result = await engine.analyze(task)
            
            print(f"  类型: {result.task_type}")
            print(f"  引擎: {result.engine_used}")
            print(f"  结果: {result.result}")
            print(f"  置信度: {result.confidence:.0%}")
            print(f"  深度: {result.depth}")
            print()
        
        print(f"\n引擎信息: {engine.get_engine_info()}")
    
    asyncio.run(test())
