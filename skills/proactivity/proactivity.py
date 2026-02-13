# 🦞 Proactivity Core - 主动性核心模块

"""
主动性增强模块

为推理引擎提供主动交互能力
（注意：主动性≠自我进化，仅是交互风格）
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta


class ProactivityLevel(Enum):
    """主动性级别"""
    LOW = 1         # 低 - 仅回答问题
    MEDIUM = 2      # 中 - 适度建议
    HIGH = 3        # 高 - 频繁主动
    ADAPTIVE = 4    # 自适应 - 根据上下文调整


class SuggestionType(Enum):
    """建议类型"""
    RESOURCE = "resource"           # 资源推荐
    OPTIMIZATION = "optimization"  # 优化建议
    PREVENTION = "prevention"       # 预防提醒
    OPPORTUNITY = "opportunity"     # 机会发现
    IMPROVEMENT = "improvement"     # 改进建议


@dataclass
class ProactiveSuggestion:
    """主动建议"""
    suggestion_id: str
    suggestion_type: str
    content: str
    trigger_context: str
    urgency_level: float  # 0-1
    confidence: float
    action_items: List[str] = field(default_factory=list)
    benefits: List[str] = field(default_factory=list)
    related_topic: str = ""


@dataclass
class UserNeed:
    """用户需求预测"""
    need_id: str
    need_type: str
    description: str
    probability: float
    trigger_events: List[str] = field(default_factory=list)
    suggested_response: str = ""
    timing_hint: str = ""


@dataclass
class Recommendation:
    """推荐"""
    recommendation_id: str
    item_type: str
    item_name: str
    reason: str
    relevance_score: float
    authority_score: float = 0.0
    context_match: float = 0.0
    alternatives: List[str] = field(default_factory=list)


@dataclass
class PreventiveAlert:
    """预防性提醒"""
    alert_id: str
    alert_type: str
    description: str
    risk_level: float
    prevention_tip: str
    related_context: str = ""
    follow_up_time: str = ""


class ProactiveKnowledgeBase:
    """主动性知识库"""
    
    # 常见场景的主动建议
    SCENARIO_SUGGESTIONS = {
        "coding": {
            "resources": ["查看文档", "搜索示例", "参考最佳实践"],
            "optimizations": ["考虑性能优化", "添加错误处理", "写单元测试"],
            "preventions": ["备份代码", "版本控制", "代码审查"]
        },
        "writing": {
            "resources": ["查阅相关资料", "参考范文", "使用写作工具"],
            "optimizations": ["结构化内容", "添加图表", "优化标题"],
            "preventions": ["检查拼写", "语法检查", "原创性检测"]
        },
        "learning": {
            "resources": ["推荐课程", "学习路径", "练习题库"],
            "optimizations": ["间隔重复", "实践应用", "总结归纳"],
            "preventions": ["避免过度学习", "保持休息", "多元化学习"]
        },
        "meeting": {
            "resources": ["议程文档", "参会人员", "历史记录"],
            "optimizations": ["提前准备", "明确目标", "分配任务"],
            "preventions": ["发送提醒", "准备备选方案", "记录要点"]
        }
    }
    
    # 主动触发词
    TRIGGER_KEYWORDS = {
        "start": ["开始", "启动", "着手", "第一次"],
        "progress": ["进度", "进展", "进行", "状态"],
        "problem": ["问题", "困难", "挑战", "卡住"],
        "completion": ["完成", "结束", "成功", "搞定"],
        "planning": ["计划", "安排", "准备", "打算"]
    }
    
    # 预防性主题
    PREVENTIVE_TOPICS = {
        "deadline": {"risk": "错过截止日期", "tip": "提前规划，设置里程碑"},
        "burnout": {"risk": "工作倦怠", "tip": "适当休息，保持平衡"},
        "miscommunication": {"risk": "沟通误解", "tip": "确认理解，主动反馈"},
        "scope_creep": {"risk": "范围蔓延", "tip": "明确边界，定期审查"},
        "technical_debt": {"risk": "技术债务", "tip": "及时重构，避免捷径"}
    }
    
    def __init__(self):
        print("ProactiveKnowledgeBase initialized")
    
    def get_suggestions(self, scenario: str, suggestion_type: str) -> List[str]:
        """获取建议"""
        return self.SCENARIO_SUGGESTIONS.get(scenario, {}).get(suggestion_type, [])
    
    def get_preventive_tip(self, topic: str) -> Optional[Dict]:
        """获取预防提醒"""
        return self.PREVENTIVE_TOPICS.get(topic)


class ProactiveSuggester:
    """主动建议器"""
    
    def __init__(self):
        self.db = ProactiveKnowledgeBase()
        print("ProactiveSuggester initialized")
    
    def generate_suggestion(self, context: str, level: str = "medium") -> ProactiveSuggestion:
        """生成主动建议"""
        import hashlib
        suggestion_id = hashlib.md5(f"{context}{datetime.now().timestamp()}".encode()).hexdigest()[:16]
        
        # 检测场景
        scenario = self._detect_scenario(context)
        suggestion_type = self._map_to_type(context)
        
        # 生成内容
        suggestions = self.db.get_suggestions(scenario, suggestion_type.value)
        
        return ProactiveSuggestion(
            suggestion_id=suggestion_id,
            suggestion_type=suggestion_type.value,
            content=f"建议: {suggestions[0] if suggestions else '继续当前工作'}",
            trigger_context=context,
            urgency_level=0.5 if level == "medium" else (0.3 if level == "low" else 0.7),
            confidence=0.8,
            action_items=suggestions[:3] if suggestions else ["继续当前任务"],
            benefits=["提高效率", "优化结果", "降低风险"]
        )
    
    def _detect_scenario(self, context: str) -> str:
        """检测场景"""
        context_lower = context.lower()
        
        if any(kw in context_lower for kw in ["代码", "编程", "开发", "实现"]):
            return "coding"
        elif any(kw in context_lower for kw in ["写作", "文档", "文章", "报告"]):
            return "writing"
        elif any(kw in context_lower for kw in ["学习", "课程", "培训", "掌握"]):
            return "learning"
        elif any(kw in context_lower for kw in ["会议", "讨论", "会议"]):
            return "meeting"
        
        return "general"
    
    def _map_to_type(self, context: str) -> SuggestionType:
        """映射到建议类型"""
        context_lower = context.lower()
        
        if any(kw in context_lower for kw in ["需要", "应该", "可以"]):
            return SuggestionType.RESOURCE
        elif any(kw in context_lower for kw in ["优化", "改进", "更好"]):
            return SuggestionType.OPTIMIZATION
        elif any(kw in context_lower for kw in ["预防", "避免", "担心"]):
            return SuggestionType.PREVENTION
        elif any(kw in context_lower for kw in ["机会", "发现", "找到"]):
            return SuggestionType.OPPORTUNITY
        
        return SuggestionType.IMPROVEMENT
    
    def get_milestone_suggestions(self, task_type: str, progress: str) -> List[str]:
        """获取里程碑建议"""
        milestones = {
            "start": {
                "coding": ["规划架构", "设置开发环境", "创建基本结构"],
                "writing": ["确定主题", "收集素材", "列出大纲"],
                "learning": ["设定目标", "选择资源", "制定计划"],
                "general": ["明确目标", "分解任务", "设定时间"]
            },
            "progress": {
                "coding": ["编写核心逻辑", "添加测试", "代码审查"],
                "writing": ["完成初稿", "添加引用", "优化结构"],
                "learning": ["完成章节", "做练习", "总结要点"],
                "general": ["检查进度", "调整计划", "寻求反馈"]
            },
            "completion": {
                "coding": ["最终测试", "文档完善", "部署准备"],
                "writing": ["校对修改", "格式调整", "发布准备"],
                "learning": ["复习总结", "实践应用", "分享知识"],
                "general": ["回顾总结", "归档整理", "规划下一步"]
            }
        }
        
        return milestones.get(progress, milestones["progress"]).get(task_type, [])
    
    def get_contextual_tips(self, context: str) -> List[str]:
        """获取上下文提示"""
        tips = []
        
        # 检测是否刚开始
        if any(kw in context for kw in self.db.TRIGGER_KEYWORDS.get("start", [])):
            tips.append("开始新任务时，建议先制定清晰的目标和计划。")
        
        # 检测是否有问题
        if any(kw in context for kw in self.db.TRIGGER_KEYWORDS.get("problem", [])):
            tips.append("遇到困难时，可以尝试分解问题或寻求帮助。")
        
        # 检测是否需要优化
        tips.append("定期回顾进度，有助于及时调整方向。")
        
        return tips


class NeedAnticipator:
    """需求预测器"""
    
    def __init__(self):
        self.db = ProactiveKnowledgeBase()
        print("NeedAnticipator initialized")
    
    def anticipate_needs(self, current_context: str) -> List[UserNeed]:
        """预测需求"""
        needs = []
        
        # 基于当前上下文预测
        if "开始" in current_context or "着手" in current_context:
            needs.append(UserNeed(
                need_id="start_resources",
                need_type="资源",
                description="可能需要相关资源和资料",
                probability=0.8,
                trigger_events=["开始新任务"],
                suggested_response="我可以帮您查找相关资料和资源。",
                timing_hint="任务开始时"
            ))
        
        if "问题" in current_context or "困难" in current_context:
            needs.append(UserNeed(
                need_id="problem_help",
                need_type="帮助",
                description="可能需要解决问题的帮助",
                probability=0.9,
                trigger_events=["遇到困难", "卡住"],
                suggested_response="让我帮您分析和解决这个问题。",
                timing_hint="遇到问题时"
            ))
        
        if "完成" in current_context or "结束" in current_context:
            needs.append(UserNeed(
                need_id="completion_check",
                need_type="检查",
                description="可能需要收尾和检查",
                probability=0.7,
                trigger_events=["接近完成"],
                suggested_response="快完成了，建议进行最终检查。",
                timing_hint="任务收尾时"
            ))
        
        return needs
    
    def get_timing_recommendation(self, task: str, phase: str) -> str:
        """获取时机建议"""
        recommendations = {
            "coding": {
                "start": "开始编码前，建议先完成设计文档。",
                "progress": "遇到难题时，先搜索类似解决方案。",
                "completion": "提交前，运行完整测试套件。"
            },
            "writing": {
                "start": "动笔前，先收集足够素材。",
                "progress": "写不下去时，先休息或换个角度。",
                "completion": "完成后，请他人审阅效果更好。"
            },
            "learning": {
                "start": "学习前，明确要达到的目标。",
                "progress": "定期复习，效果更持久。",
                "completion": "学完后，实际应用是最好的巩固。"
            }
        }
        
        return recommendations.get(task, {}).get(phase, "保持当前节奏，继续前进。")


class Recommender:
    """推荐器"""
    
    def __init__(self):
        print("Recommender initialized")
    
    def generate_recommendation(self, context: str, item_type: str) -> Recommendation:
        """生成推荐"""
        import hashlib
        rec_id = hashlib.md5(f"{context}{datetime.now().timestamp()}".encode()).hexdigest()[:16]
        
        # 基于上下文生成推荐
        item_map = {
            "tool": {"name": "相关工具", "reason": "提高效率"},
            "resource": {"name": "学习资源", "reason": "加深理解"},
            "method": {"name": "方法建议", "reason": "优化流程"},
            "example": {"name": "参考案例", "reason": "借鉴经验"}
        }
        
        item = item_map.get(item_type, item_map["method"])
        
        return Recommendation(
            recommendation_id=rec_id,
            item_type=item_type,
            item_name=item["name"],
            reason=item["reason"],
            relevance_score=0.85,
            context_match=0.8,
            alternatives=[f"其他{item_type}选项"]
        )
    
    def recommend_learning_path(self, topic: str, level: str) -> Dict:
        """推荐学习路径"""
        paths = {
            "beginner": ["基础概念", "入门教程", "简单练习", "项目实践"],
            "intermediate": ["进阶内容", "专项训练", "项目实战", "反馈改进"],
            "advanced": ["深入原理", "高级特性能", "复杂项目", "经验分享"]
        }
        
        return {
            "topic": topic,
            "level": level,
            "path": paths.get(level, paths["beginner"]),
            "estimated_time": f"{len(paths.get(level, paths['beginner']))}周",
            "key_milestones": ["完成基础", "独立项目", "指导他人"]
        }
    
    def get_best_practices(self, domain: str) -> List[str]:
        """获取最佳实践"""
        practices = {
            "coding": ["代码审查", "单元测试", "文档编写", "版本控制"],
            "writing": ["大纲先行", "读者视角", "反复修改", "获取反馈"],
            "communication": ["积极倾听", "清晰表达", "及时反馈", "换位思考"],
            "productivity": ["番茄工作法", "GTD", "时间块", "精力管理"]
        }
        
        return practices.get(domain, ["明确目标", "分解任务", "定期回顾"])


class PreventiveReminder:
    """预防性提醒器"""
    
    def __init__(self):
        self.db = ProactiveKnowledgeBase()
        print("PreventiveReminder initialized")
    
    def generate_alert(self, context: str) -> Optional[PreventiveAlert]:
        """生成预防提醒"""
        context_lower = context.lower()
        
        for topic, info in self.db.PREVENTIVE_TOPICS.items():
            if topic in context_lower:
                return PreventiveAlert(
                    alert_id=f"prevent_{topic}",
                    alert_type=topic,
                    description=info["risk"],
                    risk_level=0.6,
                    prevention_tip=info["tip"],
                    related_context=context
                )
        
        return None
    
    def get_common_pitfalls(self, task_type: str) -> List[Dict]:
        """获取常见陷阱"""
        pitfalls = {
            "coding": [
                {"pitfall": "过度设计", "tip": "先实现核心功能"},
                {"pitfall": "忽略错误处理", "tip": "考虑所有边界情况"},
                {"pitfall": "不做测试", "tip": "写测试保护代码"}
            ],
            "writing": [
                {"pitfall": "完美主义", "tip": "先完成初稿"},
                {"pitfall": "偏离主题", "tip": "时刻关注核心论点"},
                {"pitfall": "忽略读者", "tip": "考虑目标受众"}
            ],
            "project": [
                {"pitfall": "范围蔓延", "tip": "明确并坚守范围"},
                {"pitfall": "沟通不足", "tip": "保持团队同步"},
                {"pitfall": "低估时间", "tip": "增加缓冲时间"}
            ]
        }
        
        return pitfalls.get(task_type, [{"pitfall": "缺乏计划", "tip": "先制定计划"}])
    
    def create_checklist(self, task: str, checklist_type: str) -> Dict:
        """创建检查清单"""
        checklists = {
            "start": {
                "coding": ["需求确认", "环境准备", "架构设计", "版本控制"],
                "writing": ["主题确定", "大纲完成", "素材收集", "目标读者"],
                "project": ["目标明确", "资源到位", "时间计划", "责任分配"]
            },
            "review": {
                "coding": ["代码审查", "测试通过", "文档完成", "性能检查"],
                "writing": ["语法检查", "逻辑清晰", "格式规范", "原创性"],
                "project": ["目标达成", "质量达标", "风险控制", "文档归档"]
            }
        }
        
        return {
            "task": task,
            "type": checklist_type,
            "items": checklists.get(checklist_type, {}).get(task, []),
            "tip": "完成后逐项确认"
        }


class InitiativeTaker:
    """主动发起者"""
    
    def __init__(self):
        self.suggester = ProactiveSuggester()
        self.anticipator = NeedAnticipator()
        self.recommender = Recommender()
        self.reminder = PreventiveReminder()
        print("InitiativeTaker initialized")
    
    def take_initiative(self, context: str, user_profile: Dict = None) -> Dict:
        """主动采取行动"""
        initiatives = []
        
        # 1. 提供上下文建议
        tips = self.suggester.get_contextual_tips(context)
        if tips:
            initiatives.append({
                "type": "tip",
                "content": tips[0],
                "timing": "now"
            })
        
        # 2. 预测下一步需求
        needs = self.anticipator.anticipate_needs(context)
        if needs:
            initiatives.append({
                "type": "need_prediction",
                "content": needs[0].suggested_response,
                "timing": needs[0].timing_hint
            })
        
        # 3. 预防性提醒
        alert = self.reminder.generate_alert(context)
        if alert:
            initiatives.append({
                "type": "preventive_alert",
                "content": f"提醒: {alert.prevention_tip}",
                "urgency": alert.risk_level
            })
        
        return {
            "context": context,
            "initiatives": initiatives,
            "recommendation_count": len(initiatives),
            "proactivity_level": "high" if len(initiatives) > 2 else "medium"
        }
    
    def offer_help(self, current_task: str) -> Dict:
        """主动提供帮助"""
        helps = {
            "coding": "需要我帮您审查代码、解释概念或提供示例吗？",
            "writing": "需要我帮您优化结构、检查语法或提供写作建议吗？",
            "learning": "需要我帮您总结要点、解答疑问或推荐学习资源吗？",
            "planning": "需要我帮您分解任务、设定里程碑或制定计划吗？",
            "general": "有需要我帮忙的地方，请随时告诉我！"
        }
        
        task_key = current_task.lower() if current_task else "general"
        matched_key = next((k for k in helps.keys() if k in task_key), "general")
        
        return {
            "offer": helps[matched_key],
            "available_help": ["解答问题", "提供建议", "查找资料", "生成内容"],
            "follow_up": "请告诉我具体需要什么帮助。"
        }
    
    def suggest_next_step(self, current_activity: str, progress: str) -> Dict:
        """建议下一步"""
        next_steps = self.suggester.get_milestone_suggestions(current_activity, progress)
        
        return {
            "current_activity": current_activity,
            "progress": progress,
            "suggested_next": next_steps[0] if next_steps else "继续当前任务",
            "alternatives": next_steps[1:3] if len(next_steps) > 1 else ["休息一下", "寻求反馈"],
            "motivation": "您已经做得很好了，继续加油！"
        }


class ProactivityManager:
    """主动性管理器"""
    
    def __init__(self):
        self.suggester = ProactiveSuggester()
        self.anticipator = NeedAnticipator()
        self.recommender = Recommender()
        self.reminder = PreventiveReminder()
        self.initiative = InitiativeTaker()
        
        print("ProactivityManager initialized")
    
    def should_be_proactive(self, context: str, user_preference: str = "adaptive") -> bool:
        """判断是否应该主动"""
        if user_preference == "low":
            return False
        elif user_preference == "adaptive":
            # 根据上下文判断
            return any(kw in context.lower() for kw in 
                       ["开始", "帮助", "建议", "需要", "怎么办", "如何", "应该", "起步", "刚", "下一步", "下一步"])
        else:  # medium or high
            return True
    
    def generate_proactive_response(self, context: str, 
                                  user_preference: str = "adaptive") -> Dict:
        """生成主动回复"""
        if not self.should_be_proactive(context, user_preference):
            return {"type": "passive", "response": None}
        
        # 采取主动
        initiative = self.initiative.take_initiative(context)
        
        return {
            "type": "proactive",
            "initiatives": initiative["initiatives"],
            "suggestion": initiative["initiatives"][0] if initiative["initiatives"] else None,
            "proactivity_level": initiative["proactivity_level"]
        }
    
    def offer_suggestions(self, task: str) -> Dict:
        """提供建议"""
        suggestion = self.suggester.generate_suggestion(task)
        
        return {
            "suggestion_id": suggestion.suggestion_id,
            "content": suggestion.content,
            "type": suggestion.suggestion_type,
            "urgency": suggestion.urgency_level,
            "actions": suggestion.action_items,
            "benefits": suggestion.benefits
        }
    
    def anticipate_user_needs(self, context: str) -> List[UserNeed]:
        """预测用户需求"""
        return self.anticipator.anticipate_needs(context)
    
    def give_recommendation(self, context: str, item_type: str) -> Recommendation:
        """给出推荐"""
        return self.recommender.generate_recommendation(context, item_type)
    
    def preventive_check(self, context: str) -> Optional[PreventiveAlert]:
        """预防性检查"""
        return self.reminder.generate_alert(context)
    
    def take_initiative_action(self, context: str, user_profile: Dict = None) -> Dict:
        """主动行动"""
        return self.initiative.take_initiative(context, user_profile)
    
    def get_proactivity_stats(self) -> Dict:
        """获取主动性统计"""
        return {
            "active_modules": 5,
            "suggestion_types": len(SuggestionType),
            "proactivity_levels": len(ProactivityLevel),
            "preventive_topics": 5,
            "scenario_categories": 4
        }


# 测试
if __name__ == "__main__":
    pm = ProactivityManager()
    
    print("\n🦞 Proactivity Manager 测试\n")
    
    # 主动性判断
    should_proactive = pm.should_be_proactive("我刚开始一个新项目")
    print(f"应该主动: {should_proactive}")
    
    # 生成主动回复
    response = pm.generate_proactive_response("我正在写代码")
    print(f"\n主动回复类型: {response['type']}")
    
    # 提供建议
    suggestion = pm.offer_suggestions("编写一个新程序")
    print(f"\n建议内容: {suggestion['content']}")
    print(f"建议类型: {suggestion['type']}")
    print(f"操作项: {suggestion['actions']}")
    
    # 预测需求
    needs = pm.anticipate_user_needs("我遇到了一个问题")
    print(f"\n预测需求数: {len(needs)}")
    
    # 预防性检查
    alert = pm.preventive_check("担心错过截止日期")
    print(f"\n预防提醒: {alert.description if alert else '无'}")
    
    # 主动行动
    initiative = pm.take_initiative_action("刚开始一个新任务")
    print(f"\n主动行动数: {initiative['recommendation_count']}")
    
    # 统计
    stats = pm.get_proactivity_stats()
    print(f"\n统计: {stats}")
