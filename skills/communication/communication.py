# 🦞 Communication Core - 沟通核心模块

"""
沟通能力增强模块

为推理引擎提供沟通和谈判支持
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime


class CommunicationStyle(Enum):
    """沟通风格"""
    FORMAL = "formal"           # 正式
    CASUAL = "casual"           # 随意
    DIPLOMATIC = "diplomatic"  # 外交
    ASSERTIVE = "assertive"     # 自信
    COLLABORATIVE = "collaborative"  # 合作
    EMPATHETIC = "empathetic"  # 共情


class NegotiationStyle(Enum):
    """谈判风格"""
    COMPETITIVE = "competitive"     # 竞争
    COLLABORATIVE = "collaborative"  # 合作
    COMPROMISING = "compromising"   # 妥协
    ACCOMMODATING = "accommodating"  # 迁就
    AVOIDING = "avoiding"          # 回避


@dataclass
class Message:
    """消息"""
    content: str
    style: str
    tone: str  # positive, neutral, negative
    intent: str
    sentiment_score: float  # -1 to 1
    suggestions: List[str] = field(default_factory=list)


@dataclass
class NegotiationOutcome:
    """谈判结果"""
    outcome: str
    satisfaction_score: float  # 0-1
    concessions_made: List[str] = field(default_factory=list)
    points_won: List[str] = field(default_factory=list)
    relationship_impact: str = "neutral"
    next_steps: List[str] = field(default_factory=list)


@dataclass
class ConflictAnalysis:
    """冲突分析"""
    root_cause: str
    parties_involved: List[str]
    conflict_type: str  # personal, professional, systemic
    intensity: float  # 0-1
    resolution_approaches: List[str] = field(default_factory=list)
    recommended_approach: str = ""


@dataclass
class ConversationContext:
    """对话上下文"""
    topic: str
    participants: List[str]
    goals: List[str] = field(default_factory=list)
    constraints: List[str] = field(default_factory=list)
    sentiment_trend: str = "neutral"  # improving, declining, stable
    key_points: List[str] = field(default_factory=list)


class CommunicationDatabase:
    """沟通知识库"""
    
    # 谈判策略
    NEGOTIATION_TACTICS = {
        "BATNA": {
            "name": "BATNA最佳替代方案",
            "description": "在谈判前确定最佳替代方案",
            "usage": "如果您不接受这个提议，您的替代方案是什么？"
        },
        "Anchoring": {
            "name": "锚定效应",
            "description": "首先提出一个有利于自己的数字作为参考点",
            "usage": "我们建议以100万作为起点..."
        },
        "Mirroring": {
            "name": "镜像法",
            "description": "重复对方最后几句话来建立 rapport",
            "usage": "您说我们需要尽快解决这个问题..."
        },
        "Labeling": {
            "name": "标签法",
            "description": "识别并说出对方的情绪",
            "usage": "听起来您对这个提议有些顾虑..."
        },
        "Silence": {
            "name": "沉默策略",
            "description": "在提出报价后保持沉默",
            "usage": "（提出报价后保持安静）"
        },
        "IKEA": {
            "name": "IKEA效应",
            "description": "让对方参与创造过程，增加价值感",
            "usage": "我们可以一起设计一个方案..."
        }
    }
    
    # 说服技巧
    PERSUASION_TECHNIQUES = {
        "Reciprocity": {
            "name": "互惠原则",
            "description": "给予对方好处，期望回报"
        },
        "SocialProof": {
            "name": "社会认同",
            "description": "展示其他人也在做同样的事"
        },
        "Authority": {
            "name": "权威效应",
            "description": "引用专家或权威观点"
        },
        "Consistency": {
            "name": "一致性原则",
            "description": "引导对方做出小承诺"
        },
        "Liking": {
            "name": "喜好原则",
            "description": "建立良好关系后再提请求"
        },
        "Scarcity": {
            "name": "稀缺原则",
            "description": "强调机会有限或时间紧迫"
        }
    }
    
    # 冲突解决策略
    CONFLICT_RESOLUTIONS = {
        "ActiveListening": {
            "name": "积极倾听",
            "steps": ["保持眼神接触", "不要打断", "复述对方观点", "确认理解"]
        },
        "IStatements": {
            "name": "使用'我'陈述",
            "format": "当...发生时，我感到...因为..."
        },
        "FindingCommonGround": {
            "name": "寻找共同点",
            "focus": "强调共同目标而非分歧"
        },
        "InterestBased": {
            "name": "利益导向",
            "focus": "问'为什么'而不是'是什么'"
        }
    }
    
    # 高效沟通模板
    COMMUNICATION_TEMPLATES = {
        "request": {
            "formal": "尊敬的{对象}，恳请您在{时间}前{具体请求}。感谢您的配合。",
            "casual": "{对象}，能不能在{时间}前{具体请求}？谢谢！",
            "diplomatic": "如果您方便的话，我们希望{对象}能够在{时间}前{具体请求}。"
        },
        "refusal": {
            "formal": "经过审慎考虑，我们遗憾地告知目前无法满足此请求。",
            "casual": "这次可能不太方便，下次有机会再说吧。",
            "diplomatic": "我理解您的情况，但目前我们有一些限制..."
        },
        "feedback": {
            "positive": "您的{具体表现}做得非常出色，期待您继续保持。",
            "constructive": "您的{方面}还有提升空间，建议{改进建议}。"
        }
    }
    
    def __init__(self):
        print("CommunicationDatabase initialized")
    
    def get_negotiation_tactic(self, tactic: str) -> Optional[Dict]:
        return self.NEGOTIATION_TACTICS.get(tactic)
    
    def get_persuasion_technique(self, technique: str) -> Optional[Dict]:
        return self.PERSUASION_TECHNIQUES.get(technique)
    
    def get_resolution(self, approach: str) -> Optional[Dict]:
        return self.CONFLICT_RESOLUTIONS.get(approach)
    
    def get_template(self, template_type: str, style: str) -> str:
        return self.COMMUNICATION_TEMPLATES.get(template_type, {}).get(style, "")


class NegotiationTactics:
    """谈判策略"""
    
    def __init__(self):
        self.db = CommunicationDatabase()
        print("NegotiationTactics initialized")
    
    def analyze_situation(self, context: str) -> Dict:
        """分析谈判情况"""
        return {
            "context": context,
            "recommended_style": NegotiationStyle.COLLABORATIVE.value,
            "key_principles": ["利益导向", "创造双赢", "保持冷静"],
            "preparation_steps": [
                "明确自己的目标",
                "了解对方需求",
                "准备替代方案",
                "设定底线"
            ]
        }
    
    def prepare_offer(self, item: str, target_value: float, 
                       anchor_value: float = None) -> Dict:
        """准备报价"""
        return {
            "item": item,
            "target_value": target_value,
            "suggested_anchor": anchor_value or target_value * 1.2,
            "strategy": "从高于目标值开始，留有余地",
            "justification_points": [
                "市场行情分析",
                "成本考虑",
                "附加价值"
            ]
        }
    
    def respond_to_offer(self, offer: float, target: float, 
                          reservation: float) -> Dict:
        """回应报价"""
        response = {}
        
        if offer >= target:
            response = {
                "action": "接受",
                "reason": "达到或超过目标",
                "response": "我们接受这个提议。"
            }
        elif offer >= reservation:
            response = {
                "action": "谈判",
                "reason": "在可接受范围内",
                "counter_offer": target,
                "response": "这个提议有吸引力，但我们的目标是..."
            }
        else:
            response = {
                "action": "拒绝",
                "reason": "低于底线",
                "response": "这个提议与我们预期差距较大。"
            }
        
        return response
    
    def evaluate_outcome(self, final_value: float, target: float,
                         reservation: float, relationship: str) -> NegotiationOutcome:
        """评估谈判结果"""
        satisfaction = (final_value - reservation) / (target - reservation) if target > reservation else 0.5
        
        return NegotiationOutcome(
            outcome="谈判完成",
            satisfaction_score=min(1.0, max(0.0, satisfaction)),
            concessions_made=["价格调整"],
            points_won=["主要条款"],
            relationship_impact=relationship,
            next_steps=["签署合同", "执行协议"]
        )


class PersuasionStrategy:
    """说服策略"""
    
    def __init__(self):
        self.db = CommunicationDatabase()
        print("PersuasionStrategy initialized")
    
    def analyze_target(self, audience: str, topic: str) -> Dict:
        """分析说服对象"""
        return {
            "audience": audience,
            "topic": topic,
            "key_motivations": ["利益", "认可", "安全感"],
            "potential_resistance": ["成本", "风险", "不确定性"],
            "recommended_approach": "先共情，后逻辑"
        }
    
    def build_argument(self, claim: str, evidence: List[str], 
                       audience_type: str) -> Dict:
        """构建论证"""
        return {
            "claim": claim,
            "evidence": evidence,
            "structure": "问题-解决方案-好处",
            "audience_type": audience_type,
            "key_points": [
                f"为什么{claim}对您很重要",
                "证据支持",
                "行动呼吁"
            ]
        }
    
    def overcome_objections(self, objection: str) -> Dict:
        """克服异议"""
        strategies = {
            "cost": "强调长期价值和ROI",
            "risk": "提供保障措施和案例",
            "time": "展示快速实施的好处",
            "uncertainty": "提供试用或小规模试点"
        }
        
        strategy = "倾听并理解，然后回应"
        for key, response in strategies.items():
            if key in objection.lower():
                strategy = response
                break
        
        return {
            "objection": objection,
            "strategy": strategy,
            "response_template": f"我理解您的顾虑关于{objection}。{strategy}。"
        }
    
    def create_cta(self, action: str, urgency: str = "") -> Dict:
        """创造行动呼吁"""
        return {
            "action": action,
            "urgency": urgency or "随时可以开始",
            "simplicity": "只需3步",
            "barrier_removal": "我们提供全程支持"
        }


class ConflictResolver:
    """冲突解决"""
    
    def __init__(self):
        self.db = CommunicationDatabase()
        print("ConflictResolver initialized")
    
    def analyze_conflict(self, description: str) -> ConflictAnalysis:
        """分析冲突"""
        return ConflictAnalysis(
            root_cause="沟通误解或利益冲突",
            parties_involved=["甲方", "乙方"],
            conflict_type="professional",
            intensity=0.5,
            resolution_approaches=["调解", "协商", "第三方介入"],
            recommended_approach="利益导向的协商"
        )
    
    def mediate(self, party1_view: str, party2_view: str) -> Dict:
        """调解冲突"""
        return {
            "party1_view": party1_view,
            "party2_view": party2_view,
            "common_interests": ["解决问题", "维护关系"],
            "proposed_solution": "双方各退一步",
            "steps": [
                "让双方表达观点",
                "确认共同利益",
                "提出解决方案",
                "达成共识"
            ]
        }
    
    def generate_script(self, situation: str, role: str) -> Dict:
        """生成沟通脚本"""
        templates = {
            "difficult_conversation": {
                "start": "我想和您讨论一个重要话题。",
                "middle": "我注意到...我感到...因为...",
                "end": "我们一起想办法解决吧。"
            },
            "giving_feedback": {
                "start": "我想分享一些观察。",
                "middle": "您的...表现很好，同时...可以改进。",
                "end": "我相信您可以做得更好。"
            },
            "apologizing": {
                "start": "我为...向您道歉。",
                "middle": "我理解这给您带来了...我感到抱歉。",
                "end": "我将采取措施确保不再发生。"
            }
        }
        
        return {
            "situation": situation,
            "role": role,
            "script": templates.get(situation, templates["difficult_conversation"]),
            "tips": ["保持冷静", "使用'我'陈述", "关注解决问题"]
        }


class ConversationManager:
    """对话管理"""
    
    def __init__(self):
        self.db = CommunicationDatabase()
        print("ConversationManager initialized")
    
    def start_conversation(self, topic: str, participants: List[str]) -> ConversationContext:
        """开始对话"""
        return ConversationContext(
            topic=topic,
            participants=participants,
            goals=["达成共识", "解决问题"],
            sentiment_trend="stable"
        )
    
    def analyze_message(self, message: str) -> Message:
        """分析消息"""
        return Message(
            content=message,
            style=CommunicationStyle.COLLABORATIVE.value,
            tone="neutral",
            intent="information",
            sentiment_score=0.0,
            suggestions=["保持当前风格", "继续深入话题"]
        )
    
    def generate_response(self, context: Message, style: str = "collaborative") -> str:
        """生成回应"""
        templates = {
            "collaborative": "我理解您的观点，让我们一起看看如何解决这个问题。",
            "assertive": "我的立场是明确的，我们需要采取行动。",
            "diplomatic": "这是一个有趣的观点，我们能否考虑其他可能性？",
            "empathetic": "我能感受到您的处境，让我们一起面对这个挑战。"
        }
        
        return templates.get(style, templates["collaborative"])
    
    def improve_expression(self, original: str, goal: str) -> Dict:
        """优化表达"""
        return {
            "original": original,
            "goal": goal,
            "improved": f"优化后的表达（更清晰、更有说服力）",
            "changes": ["简化句子", "增加逻辑连接", "强化行动呼吁"]
        }


class ExpressionOptimizer:
    """表达优化"""
    
    def __init__(self):
        self.db = CommunicationDatabase()
        print("ExpressionOptimizer initialized")
    
    def simplify_message(self, message: str) -> Dict:
        """简化信息"""
        return {
            "original": message,
            "simplified": "简化后的核心信息",
            "key_points": ["要点1", "要点2", "要点3"],
            "action_items": ["行动1", "行动2"]
        }
    
    def make_persuasive(self, message: str) -> Dict:
        """增强说服力"""
        return {
            "original": message,
            "enhanced": "更具说服力的表达",
            "techniques_used": ["互惠原则", "社会认同", "稀缺性"]
        }
    
    def adjust_tone(self, message: str, target_tone: str) -> Dict:
        """调整语气"""
        return {
            "original": message,
            "adjusted": f"调整为{target_tone}语气",
            "changes": ["词汇调整", "句式调整", "礼貌用语"]
        }
    
    def format_email(self, recipient: str, subject: str, 
                     main_points: List[str]) -> Dict:
        """格式化邮件"""
        return {
            "to": recipient,
            "subject": subject,
            "greeting": f"尊敬的{recipient}，",
            "body": "\n".join([f"1. {point}" for point in main_points]),
            "closing": "此致\n敬礼",
            "signature": "XXX"
        }


class CommunicationManager:
    """沟通管理器"""
    
    def __init__(self):
        self.db = CommunicationDatabase()
        self.negotiation = NegotiationTactics()
        self.persuasion = PersuasionStrategy()
        self.conflict = ConflictResolver()
        self.conversation = ConversationManager()
        self.expression = ExpressionOptimizer()
        print("CommunicationManager initialized")
    
    def enhance_communication(self, message: str, goal: str) -> Dict:
        """增强沟通"""
        analysis = self.conversation.analyze_message(message)
        improved = self.conversation.improve_expression(message, goal)
        
        return {
            "original": message,
            "analysis": analysis.__dict__,
            "improved": improved["improved"],
            "suggestions": [
                "简化表达",
                "增加逻辑性",
                "强化行动呼吁"
            ]
        }
    
    def negotiate(self, context: str, offer: float, target: float,
                  reservation: float) -> Dict:
        """谈判"""
        situation = self.negotiation.analyze_situation(context)
        response = self.negotiation.respond_to_offer(offer, target, reservation)
        outcome = self.negotiation.evaluate_outcome(offer, target, reservation, "neutral")
        
        return {
            "situation": situation,
            "response": response,
            "outcome": outcome.__dict__
        }
    
    def resolve_conflict(self, description: str) -> Dict:
        """解决冲突"""
        analysis = self.conflict.analyze_conflict(description)
        resolution = self.conflict.mediate("甲方观点", "乙方观点")
        
        return {
            "analysis": analysis.__dict__,
            "resolution": resolution
        }
    
    def get_communication_tip(self, situation: str) -> Dict:
        """获取沟通建议"""
        tips = {
            "meeting": "会前准备要点，明确目标",
            "presentation": "开场要吸引人，结论要有力",
            "email": "主题清晰，正文简洁",
            "phone": "微笑说话，注意节奏",
            "negotiation": "保持冷静，记录要点"
        }
        
        return {
            "situation": situation,
            "tip": tips.get(situation, "真诚沟通，尊重对方"),
            "do": ["保持眼神", "积极倾听", "确认理解"],
            "dont": ["打断对方", "过于激进", "忽视感受"]
        }
    
    def get_stats(self) -> Dict:
        """获取统计"""
        return {
            "negotiation_tactics": len(self.db.NEGOTIATION_TACTICS),
            "persuasion_techniques": len(self.db.PERSUASION_TECHNIQUES),
            "conflict_resolutions": len(self.db.CONFLICT_RESOLUTIONS),
            "communication_templates": len(self.db.COMMUNICATION_TEMPLATES)
        }


# 测试
if __name__ == "__main__":
    cm = CommunicationManager()
    
    print("\n🦞 Communication Manager 测试\n")
    
    # 沟通增强
    result = cm.enhance_communication(
        "我想让您考虑一下我们的新产品",
        "让对方感兴趣"
    )
    print(f"沟通增强: {result['improved']}")
    
    # 谈判
    negotiation = cm.negotiate(
        "购买设备",
        offer=80,
        target=100,
        reservation=70
    )
    print(f"\n谈判回应: {negotiation['response']['action']}")
    
    # 冲突解决
    conflict = cm.resolve_conflict("项目延期引发的不满")
    print(f"\n冲突分析: {conflict['analysis']['recommended_approach']}")
    
    # 沟通建议
    tip = cm.get_communication_tip("meeting")
    print(f"\n会议建议: {tip['tip']}")
    
    print(f"\n统计: {cm.get_stats()}")
