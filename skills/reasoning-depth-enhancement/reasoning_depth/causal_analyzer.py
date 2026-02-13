# 🦞 Causal Analyzer - 因果分析器

"""
因果分析模块

功能:
- 识别因果关系
- 构建因果链
- 分析因果强度
- 发现间接因果
"""

from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime


class CausalStrength(Enum):
    """因果强度"""
    STRONG = "strong"     # 强因果
    MODERATE = "moderate"  # 中等因果
    WEAK = "weak"         # 弱因果
    CORRELATION = "correlation"  # 相关而非因果


@dataclass
class CausalLink:
    """因果链接"""
    cause: str
    effect: str
    strength: str
    mechanism: str  # 因果机制
    evidence: List[str] = field(default_factory=list)
    confidence: float = 0.0


@dataclass
class CausalChain:
    """因果链"""
    chain_id: str
    root_cause: str
    final_effect: str
    links: List[CausalLink] = field(default_factory=list)
    intermediates: List[str] = field(default_factory=list)
    total_strength: float = 0.0
    is_direct: bool = True


class CausalAnalyzer:
    """因果分析器"""
    
    # 因果表达模式
    CAUSAL_PATTERNS = [
        ("{A}导致{B}", "直接因果"),
        ("{A}引起{B}", "直接因果"),
        ("{A}使{B}", "直接因果"),
        ("{A}让{B}", "直接因果"),
        ("{A}是{B}的原因", "直接因果"),
        ("因为{A}，所以{B}", "因果链"),
        ("{A}影响{B}", "间接因果"),
        ("{A}作用于{B}", "间接因果"),
        ("{A}引起{B}的变化", "动态因果"),
        ("{A}是{B}的根本原因", "根本因果"),
    ]
    
    # 因果连接词
    CAUSAL_CONNECTORS = [
        "导致", "引起", "使得", "因为", "所以",
        "因此", "影响", "作用", "源于", "起因于"
    ]
    
    def __init__(self):
        self.chains: Dict[str, CausalChain] = {}
        self.chain_counter = 0
        
        print("✅ CausalAnalyzer 初始化完成")
    
    def extract_causes(self, text: str) -> List[Tuple[str, str, float]]:
        """
        从文本中提取因果关系
        
        Args:
            text: 文本
            
        Returns:
            [(原因, 结果, 置信度)]列表
        """
        causes = []
        
        # 匹配因果模式
        for pattern, mechanism in self.CAUSAL_PATTERNS:
            # 简化匹配
            for connector in self.CAUSAL_CONNECTORS:
                if connector in text:
                    parts = text.split(connector)
                    if len(parts) == 2:
                        cause = parts[0].strip()
                        effect = parts[1].strip()
                        confidence = self._calculate_confidence(cause, effect, mechanism)
                        
                        causes.append((cause, effect, confidence))
        
        # 提取隐含因果关系
        implicit = self._extract_implicit_causes(text)
        causes.extend(implicit)
        
        return causes
    
    def _extract_implicit_causes(self, text: str) -> List[Tuple[str, str, float]]:
        """提取隐含因果"""
        implicit = []
        
        # 时间顺序暗示因果
        if "之前" in text or "以后" in text:
            # 检查时间顺序
            implicit.append((text.split("之前")[0] if "之前" in text else text,
                           text.split("以后")[-1] if "以后" in text else text,
                           0.6))  # 较低置信度
        
        return implicit
    
    def _calculate_confidence(
        self,
        cause: str,
        effect: str,
        mechanism: str
    ) -> float:
        """计算因果置信度"""
        # 基础置信度
        if mechanism == "直接因果":
            base = 0.85
        elif mechanism == "间接因果":
            base = 0.70
        else:
            base = 0.75
        
        # 根据文本长度调整
        if len(cause) < 3 or len(effect) < 3:
            base *= 0.8  # 太短的可信度低
        
        # 检查是否有证据
        if "因为" in cause or "由于" in cause:
            base += 0.1
        
        return min(0.95, base)
    
    def build_chain(
        self,
        cause: str,
        effect: str,
        intermediate_causes: List[str] = None
    ) -> CausalChain:
        """
        构建因果链
        
        Args:
            cause: 原因
            effect: 结果
            intermediate_causes: 中间原因
            
        Returns:
            CausalChain: 因果链
        """
        self.chain_counter += 1
        chain_id = f"causal_{self.chain_counter}"
        
        intermediates = intermediate_causes or []
        
        # 构建链接
        links = []
        
        if intermediates:
            # 多步因果
            all_factors = [cause] + intermediates + [effect]
            for i in range(len(all_factors) - 1):
                link = CausalLink(
                    cause=all_factors[i],
                    effect=all_factors[i + 1],
                    strength=CausalStrength.MODERATE.value,
                    mechanism="多步因果",
                    confidence=0.80
                )
                links.append(link)
        else:
            # 直接因果
            links.append(CausalLink(
                cause=cause,
                effect=effect,
                strength=CausalStrength.STRONG.value,
                mechanism="直接因果",
                confidence=0.85
            ))
        
        # 计算整体强度
        total_strength = self._calculate_total_strength(links)
        
        chain = CausalChain(
            chain_id=chain_id,
            root_cause=cause,
            final_effect=effect,
            links=links,
            intermediates=intermediates,
            total_strength=total_strength,
            is_direct=len(intermediates) == 0
        )
        
        self.chains[chain_id] = chain
        
        return chain
    
    def _calculate_total_strength(self, links: List[CausalLink]) -> float:
        """计算因果链整体强度"""
        if not links:
            return 0.0
        
        # 多步因果会减弱
        if len(links) == 1:
            return links[0].confidence
        else:
            # 每增加一步，置信度衰减
            decay = 0.1 * (len(links) - 1)
            return max(0.5, links[0].confidence - decay)
    
    def analyze_effect_chain(self, effect: str) -> List[str]:
        """
        分析导致某结果的所有原因
        
        Args:
            effect: 结果
            
        Returns:
            原因链列表
        """
        causes = []
        
        for chain in self.chains.values():
            if chain.final_effect == effect:
                causes.append(self._format_chain(chain))
        
        return causes
    
    def analyze_cause_chain(self, cause: str) -> List[str]:
        """
        分析某原因导致的所有结果
        
        Args:
            cause: 原因
            
        Returns:
            结果链列表
        """
        effects = []
        
        for chain in self.chains.values():
            if chain.root_cause == cause:
                effects.append(self._format_chain(chain))
        
        return effects
    
    def _format_chain(self, chain: CausalChain) -> str:
        """格式化因果链"""
        if chain.is_direct:
            return f"{chain.root_cause} → {chain.final_effect}"
        else:
            return f"{chain.root_cause} → {' → '.join(chain.intermediates)} → {chain.final_effect}"
    
    def find_common_causes(self, effects: List[str]) -> List[str]:
        """
        查找多个结果的共同原因
        
        Args:
            effects: 结果列表
            
        Returns:
            共同原因列表
        """
        effect_chains = {}
        
        for effect in effects:
            chains = self.analyze_effect_chain(effect)
            for chain in chains:
                parts = chain.replace(" → ", " ").split()
                for part in parts:
                    if part not in effect_chains:
                        effect_chains[part] = 0
                    effect_chchains[part] += 1
        
        # 找到出现在多个结果中的原因
        common = [c for c, count in effect_chains.items() if count > 1]
        return common
    
    def counterfactual_analysis(
        self,
        cause: str,
        effect: str,
        prevented: bool = False
    ) -> Dict:
        """
        反事实分析：如果X没有发生，Y会怎样？
        
        Args:
            cause: 原因
            effect: 结果
            prevented: 是否被阻止
            
        Returns:
            反事实分析结果
        """
        if prevented:
            return {
                "question": f"如果{cause}被阻止，{effect}会发生吗？",
                "answer": f"如果{cause}被阻止，{effect}可能不会发生或减弱",
                "confidence": 0.70,
                "reasoning": "基于因果链分析，{cause}是{effect}的重要原因"
            }
        else:
            return {
                "question": f"如果{cause}没有发生，{effect}会怎样？",
                "answer": f"如果{cause}没有发生，{effect}可能不会发生",
                "confidence": 0.75,
                "reasoning": "基于{cause}→{effect}的因果关系"
            }
    
    def get_stats(self) -> Dict:
        """获取统计"""
        direct = sum(1 for c in self.chains.values() if c.is_direct)
        indirect = len(self.chains) - direct
        
        return {
            "total_chains": len(self.chains),
            "direct_chains": direct,
            "indirect_chains": indirect,
            "avg_strength": self._avg_strength()
        }
    
    def _avg_strength(self) -> float:
        """计算平均因果强度"""
        if not self.chains:
            return 0.0
        return sum(c.total_strength for c in self.chains.values()) / len(self.chains)


# 测试
if __name__ == "__main__":
    analyzer = CausalAnalyzer()
    
    texts = [
        "因为下雨，所以地湿了",
        "吸烟导致肺癌",
        "努力学习使人进步",
        "经济发展带来环境污染"
    ]
    
    print("🦞 因果分析测试\n")
    
    for text in texts:
        print(f"文本: {text}")
        causes = analyzer.extract_causes(text)
        print(f"  因果关系: {causes}")
        print()
    
    # 构建因果链
    chain = analyzer.build_chain(
        cause="下雨",
        effect="地湿了",
        intermediate_causes=["路面变湿"]
    )
    print(f"因果链: {analyzer._format_chain(chain)}")
    print(f"强度: {chain.total_strength:.0%}")
    print(f"直接: {chain.is_direct}")
    
    print(f"\n统计: {analyzer.get_stats()}")
