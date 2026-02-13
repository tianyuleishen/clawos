# 🦞 Reasoning Depth Enhancement - 推理深度提升

"""
推理深度提升技能

功能:
- 多步推理链
- 因果分析
- 反事实推理
- 元推理
- 归纳演绎结合
"""

__version__ = "1.0.0"
__author__ = "ClawOS Team"

from .chain_reasoner import ChainReasoner, ReasoningStep
from .causal_analyzer import CausalAnalyzer, CausalChain
from .counterfactual_reasoner import CounterfactualReasoner
from .meta_reasoner import MetaReasoner
from .enhanced_fusion import EnhancedFusionEngine

__all__ = [
    'ChainReasoner',
    'ReasoningStep',
    'CausalAnalyzer',
    'CausalChain',
    'CounterfactualReasoner',
    'MetaReasoner',
    'EnhancedFusionEngine',
    '__version__',
]
