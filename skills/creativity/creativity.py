# 🦞 Creativity Core - 创造力核心模块

"""
创造力增强模块

为推理引擎提供创意和创新支持
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import random


class CreativeStyle(Enum):
    """创意风格"""
    CONVENTIONAL = "conventional"       # 传统
    INNOVATIVE = "innovative"          # 创新
    BOLD = "bold"                       # 大胆
    MINIMALIST = "minimalist"           # 极简
    PLAYFUL = "playful"                 # 趣味
    SERIOUS = "serious"                 # 严肃
    ROMANTIC = "romantic"               # 浪漫
    TECHNICAL = "technical"              # 技术


class IdeaCategory(Enum):
    """创意类别"""
    PRODUCT = "product"                  # 产品
    SERVICE = "service"                  # 服务
    PROCESS = "process"                  # 流程
    MARKETING = "marketing"              # 营销
    CONTENT = "content"                  # 内容
    DESIGN = "design"                   # 设计
    TECHNOLOGY = "technology"            # 技术
    BUSINESS = "business"                # 商业


@dataclass
class CreativeIdea:
    """创意"""
    title: str
    description: str
    category: str
    novelty_score: float  # 0-1
    feasibility_score: float  # 0-1
    impact_score: float  # 0-1
    key_features: List[str] = field(default_factory=list)
    target_audience: str = ""
    implementation_steps: List[str] = field(default_factory=list)


@dataclass
class BrainstormResult:
    """头脑风暴结果"""
    topic: str
    ideas: List[CreativeIdea]
    themes: List[str] = field(default_factory=list)
    unconventional_ideas: List[CreativeIdea] = field(default_factory=list)
    combinations: List[Dict] = field(default_factory=list)


@dataclass
class DesignChallenge:
    """设计挑战"""
    problem: str
    constraints: List[str] = field(default_factory=list)
    user_needs: List[str] = field(default_factory=list)
    proposed_solutions: List[Dict] = field(default_factory=list)
    empathy_insights: List[str] = field(default_factory=list)


@dataclass
class CreativeContent:
    """创意内容"""
    content_type: str
    topic: str
    outline: List[str] = field(default_factory=list)
    key_messages: List[str] = field(default_factory=list)
    style_guide: str = ""
    suggested_length: str = ""


class CreativityDatabase:
    """创造力知识库"""
    
    # 创新技术
    INNOVATION_TECHNIQUES = {
        "SCAMPER": {
            "name": "SCAMPER创新法",
            "description": "通过替代、合并、改造、调整、修改、用途、反向思考",
            "steps": ["Substitute 替代", "Combine 合并", "Adapt 改造", 
                     "Modify 修改", "Put to other uses 用途", "Eliminate 消除", "Reverse 反向"]
        },
        "SixHats": {
            "name": "六顶思考帽",
            "description": "从6个不同角度思考问题",
            "hats": ["白帽（事实）", "红帽（情感）", "黑帽（风险）", 
                    "黄帽（利益）", "绿帽（创意）", "蓝帽（控制）"]
        },
        "Brainwriting": {
            "name": "头脑书写",
            "description": "安静地写下想法，比传统头脑风暴更高效"
        },
        "RandomEntry": {
            "name": "随机输入法",
            "description": "随机选择一个词，强制建立联系"
        },
        "AnalogyThinking": {
            "name": "类比思维",
            "description": "从自然界或其他领域寻找类比"
        },
        "ReverseThinking": {
            "name": "逆向思维",
            "description": "从相反角度思考问题"
        }
    }
    
    # 创意模板
    CREATIVE_TEMPLATES = {
        "elevator_pitch": {
            "name": "电梯演讲模板",
            "template": "为了帮助{目标人群}解决{问题}，我们提供{解决方案}，它不同于{竞品}，因为我们{独特价值}。"
        },
        "value_proposition": {
            "name": "价值主张模板",
            "template": "我们的产品帮助{用户}通过{方式}实现{收益}，区别于{现有方案}。"
        },
        "story_arc": {
            "name": "故事弧线模板",
            "template": "从前有一个{角色}，他/她遇到了{问题}。于是他/她决定{行动}。最终他/她{结果}。"
        },
        "pain_solution": {
            "name": "痛点-解决方案模板",
            "template": "许多人面临{痛点}的困扰。我们提供{解决方案}，让你/企业{收益}。"
        }
    }
    
    # 创意触发词
    CREATIVE_TRIGGERS = [
        "如果...会怎样",
        "为什么...不能",
        "假如...不存在",
        "如何让...更",
        "如果...和...结合",
        "在...背景下",
        "如果...反向",
        "如何用...解决"
    ]
    
    def __init__(self):
        print("CreativityDatabase initialized")
    
    def get_technique(self, name: str) -> Optional[Dict]:
        return self.INNOVATION_TECHNIQUES.get(name)
    
    def get_template(self, name: str) -> str:
        return self.CREATIVE_TEMPLATES.get(name, {}).get("template", "")
    
    def get_random_trigger(self) -> str:
        return random.choice(self.CREATIVE_TRIGGERS)


class IdeaGenerator:
    """创意生成器"""
    
    def __init__(self):
        self.db = CreativityDatabase()
        print("IdeaGenerator initialized")
    
    def generate_ideas(self, topic: str, count: int = 5) -> List[CreativeIdea]:
        """生成创意"""
        ideas = []
        
        for i in range(count):
            idea = CreativeIdea(
                title=f"{topic}创意{i+1}",
                description=f"关于{topic}的创新方案{i+1}",
                category=IdeaCategory.PRODUCT.value,
                novelty_score=random.uniform(0.6, 0.95),
                feasibility_score=random.uniform(0.5, 0.9),
                impact_score=random.uniform(0.5, 0.95),
                key_features=[f"特点{i+1}", f"优势{i+1}"],
                target_audience=f"对{topic}感兴趣的人群",
                implementation_steps=["步骤1", "步骤2", "步骤3"]
            )
            ideas.append(idea)
        
        return ideas
    
    def improve_idea(self, idea: str) -> Dict:
        """改进创意"""
        return {
            "original": idea,
            "suggested_improvements": [
                "增加用户互动功能",
                "优化用户体验流程",
                "考虑更多使用场景"
            ],
            "questions_to_answer": [
                "目标用户是谁？",
                "如何衡量成功？",
                "主要挑战是什么？"
            ]
        }
    
    def evaluate_idea(self, idea: str) -> Dict:
        """评估创意"""
        return {
            "idea": idea,
            "novelty": random.uniform(0.5, 0.95),
            "feasibility": random.uniform(0.5, 0.9),
            "impact": random.uniform(0.5, 0.95),
            "overall_score": 0.75,
            "strengths": ["创新性强", "市场需求大"],
            "weaknesses": ["实施难度中等", "需要资源支持"]
        }


class BrainstormingEngine:
    """头脑风暴引擎"""
    
    def __init__(self):
        self.db = CreativityDatabase()
        self.generator = IdeaGenerator()
        print("BrainstormingEngine initialized")
    
    def brainstorm(self, topic: str, mode: str = "classic") -> BrainstormResult:
        """头脑风暴"""
        # 生成基础创意
        ideas = self.generator.generate_ideas(topic, 10)
        
        # 生成非常规创意
        unconventional = self.generator.generate_ideas(f"逆向{topic}", 3)
        
        # 识别主题
        themes = [f"主题{i+1}" for i in range(3)]
        
        # 组合创意
        combinations = [
            {"combo": f"创意{i}+创意{j}", "synergy": f"协同效应{i+j}"}
            for i in range(1, 4) for j in range(1, 4) if i != j
        ]
        
        return BrainstormResult(
            topic=topic,
            ideas=ideas,
            themes=themes,
            unconventional_ideas=unconventional,
            combinations=combinations
        )
    
    def use_technique(self, topic: str, technique: str) -> Dict:
        """使用创新技术"""
        tech = self.db.get_technique(technique)
        
        if tech:
            return {
                "technique": tech["name"],
                "description": tech["description"],
                "application": f"将{tech['name']}应用于{topic}",
                "steps": tech.get("steps", tech.get("hats", []))
            }
        
        return {"error": f"未找到技术: {technique}"}
    
    def apply_six_hats(self, topic: str) -> Dict:
        """六顶思考帽"""
        hats = [
            {"hat": "白帽", "focus": "关于topic的事实和数据", "questions": ["有哪些已知信息？", "需要什么数据？"]},
            {"hat": "红帽", "focus": "对topic的情感和直觉", "questions": ["这个想法让您有什么感受？"]},
            {"hat": "黑帽", "focus": "风险和潜在问题", "questions": ["可能出什么错？", "有哪些缺点？"]},
            {"hat": "黄帽", "focus": "价值和利益", "questions": ["有什么好处？", "为什么值得做？"]},
            {"hat": "绿帽", "focus": "创意和可能性", "questions": ["有哪些替代方案？", "如何改进？"]},
            {"hat": "蓝帽", "focus": "过程控制", "questions": ["我们思考了什么？", "下一步做什么？"]}
        ]
        
        return {
            "topic": topic,
            "hats": hats
        }


class DesignThinking:
    """设计思维"""
    
    def __init__(self):
        self.db = CreativityDatabase()
        print("DesignThinking initialized")
    
    def empathize(self, problem: str) -> Dict:
        """同理心阶段"""
        return {
            "problem": problem,
            "user_personas": [
                {"name": "用户A", "needs": ["易用性", "快速上手"], "pain_points": ["复杂"]},
                {"name": "用户B", "needs": ["高级功能", "定制化"], "pain_points": ["限制太多"]},
            ],
            "empathy_questions": [
                "用户为什么有这个需求？",
                "用户在什么场景下会遇到这个问题？",
                "用户现在是如何解决这个问题的？"
            ],
            "insights": [
                "用户期望更简单的解决方案",
                "用户希望看到即时的价值"
            ]
        }
    
    def define(self, insights: List[str]) -> Dict:
        """定义问题"""
        return {
            "problem_statement": "如何帮助用户更高效地{目标}？",
            "point_of_view": "为{用户}提供{解决方案}",
            "design_challenge": "创造一个{产品/服务}来解决{问题}"
        }
    
    def ideate(self, challenge: str, count: int = 10) -> List[str]:
        """构思阶段"""
        return [
            f"方案{i+1}: {challenge}的创新解决方式"
            for i in range(count)
        ]
    
    def prototype(self, solution: str) -> Dict:
        """原型阶段"""
        return {
            "solution": solution,
            "prototype_type": "低保真原型",
            "key_elements": ["核心功能", "用户流程", "界面草图"],
            "testing_plan": "邀请3-5个用户进行测试"
        }
    
    def test(self, prototype: Dict, feedback: List[str]) -> Dict:
        """测试阶段"""
        return {
            "findings": feedback,
            "iterations_needed": 2,
            "key_learnings": [
                "某些功能需要简化",
                "用户期望更多的引导"
            ],
            "next_steps": ["优化原型", "进行下一轮测试"]
        }


class CreativeWriter:
    """创意写作"""
    
    def __init__(self):
        self.db = CreativityDatabase()
        print("CreativeWriter initialized")
    
    def generate_content(self, topic: str, content_type: str, 
                        style: str = "informative") -> CreativeContent:
        """生成内容"""
        templates = {
            "article": {"outline": ["引言", "主体1", "主体2", "结论"]},
            "story": {"outline": ["开端", "发展", "高潮", "结局"]},
            "email": {"outline": ["称呼", "正文", "结尾"]},
            "social": {"outline": ["开头吸引", "核心信息", "行动呼吁"]}
        }
        
        return CreativeContent(
            content_type=content_type,
            topic=topic,
            outline=templates.get(content_type, ["引言", "主体", "结论"]).get("outline", []),
            key_messages=[f"关键信息1: {topic}", "关键信息2: 价值主张"],
            style_guide=f"风格: {style}",
            suggested_length=f"{content_type}标准长度"
        )
    
    def improve_writing(self, text: str, goal: str) -> Dict:
        """改进写作"""
        return {
            "original": text,
            "goal": goal,
            "suggestions": [
                "简化长句",
                "增加具体例子",
                "强化主题句"
            ],
            "improved_version": f"改进后的{text[:50]}..."
        }
    
    def generate_headlines(self, topic: str, count: int = 5) -> List[str]:
        """生成标题"""
        triggers = [
            f"关于{topic}，你必须知道的{count}件事",
            f"如何用{topic}改变你的{random.choice(['生活', '工作', '事业'])}",
            f"{topic}的终极指南",
            f"为什么{topic}是2024的最大趋势",
            f"{topic}: 你需要知道的一切"
        ]
        return triggers[:count]
    
    def write_story(self, prompt: str, style: str = "engaging") -> Dict:
        """写故事"""
        return {
            "prompt": prompt,
            "style": style,
            "story_arc": {
                "setup": "设定背景和角色",
                "conflict": "引入问题和挑战",
                "resolution": "展示解决方案和成长"
            },
            "key_elements": ["吸引人的开头", "情感共鸣", "有力的结尾"]
        }


class ProblemInnovator:
    """问题创新解决"""
    
    def __init__(self):
        self.db = CreativityDatabase()
        print("ProblemInnovator initialized")
    
    def analyze_problem(self, problem: str) -> Dict:
        """分析问题"""
        return {
            "problem": problem,
            "root_causes": ["原因1", "原因2", "原因3"],
            "stakeholders": ["用户", "企业", "合作伙伴"],
            "impact_areas": ["用户体验", "业务效率", "成本"]
        }
    
    def generate_solutions(self, problem: str, approach: str = "creative") -> List[Dict]:
        """生成解决方案"""
        solutions = []
        
        approaches = {
            "creative": [f"创新方案{i}" for i in range(1, 6)],
            "practical": [f"实用方案{i}" for i in range(1, 6)],
            "radical": [f"颠覆方案{i}" for i in range(1, 4)]
        }
        
        for sol in approaches.get(approach, approaches["creative"]):
            solutions.append({
                "solution": sol,
                "novelty": random.uniform(0.6, 0.95),
                "feasibility": random.uniform(0.5, 0.9),
                "impact": random.uniform(0.5, 0.95)
            })
        
        return solutions
    
    def find_alternatives(self, current_solution: str) -> Dict:
        """寻找替代方案"""
        return {
            "current": current_solution,
            "alternatives": [
                "替代方案1: 采用新技术",
                "替代方案2: 改变商业模式",
                "替代方案3: 重新定义问题"
            ],
            "comparison": {
                "成本": {"当前": "高", "替代": "中"},
                "实施难度": {"当前": "中", "替代": "高"},
                "预期效果": {"当前": "好", "替代": "更好"}
            }
        }
    
    def apply_scamper(self, subject: str) -> Dict:
        """应用SCAMPER"""
        return {
            "subject": subject,
            "techniques": [
                {"method": "S-替代", "question": "什么可以替代当前方案？"},
                {"method": "C-合并", "question": "可以和什么合并？"},
                {"method": "A-改造", "question": "如何改造以改进？"},
                {"method": "M-修改", "question": "可以修改什么？"},
                {"method": "P-用途", "question": "还有其他用途吗？"},
                {"method": "E-消除", "question": "什么可以消除？"},
                {"method": "R-反向", "question": "反向会怎样？"}
            ],
            "answers": {
                "S": "使用AI替代人工",
                "C": "与竞品合作",
                "A": "增加自动化功能",
                "M": "修改用户界面",
                "P": "开放API给第三方",
                "E": "消除冗余流程",
                "R": "从用户变提供者"
            }
        }


class CreativityManager:
    """创造力管理器"""
    
    def __init__(self):
        self.db = CreativityDatabase()
        self.idea_generator = IdeaGenerator()
        self.brainstorming = BrainstormingEngine()
        self.design_thinking = DesignThinking()
        self.creative_writer = CreativeWriter()
        self.problem_innovator = ProblemInnovator()
        print("CreativityManager initialized")
    
    def enhance_creativity(self, task: str) -> Dict:
        """增强创造力"""
        result = {
            "task": task,
            "suggested_technique": "SCAMPER或六顶思考帽",
            "approaches": [
                "从不同角度思考问题",
                "寻找类比和灵感",
                "尝试逆向思维"
            ],
            "creative_triggers": [
                "如果...会怎样？",
                "为什么...不能？",
                "如何让...更...？"
            ]
        }
        
        # 根据任务类型推荐
        if "生成" in task or "创意" in task:
            ideas = self.idea_generator.generate_ideas(task.replace("生成", "").replace("创意", ""))
            result["ideas"] = [{"title": i.title, "novelty": i.novelty_score} for i in ideas]
        elif "头脑风暴" in task:
            topic = task.replace("头脑风暴", "")
            brainstorm = self.brainstorming.brainstorm(topic)
            result["ideas_count"] = len(brainstorm.ideas)
        elif "写作" in task or "写" in task:
            content = self.creative_writer.generate_content(task.replace("写", ""), "article")
            result["outline"] = content.outline
        
        return result
    
    def brainstorm_ideas(self, topic: str) -> BrainstormResult:
        """头脑风暴"""
        return self.brainstorming.brainstorm(topic)
    
    def solve_problem(self, problem: str, approach: str = "creative") -> Dict:
        """解决问题"""
        analysis = self.problem_innovator.analyze_problem(problem)
        solutions = self.problem_innovator.generate_solutions(problem, approach)
        
        return {
            "analysis": analysis,
            "solutions": solutions,
            "recommendation": "建议尝试创新方案3"
        }
    
    def apply_technique(self, task: str, technique: str) -> Dict:
        """应用技术"""
        if technique == "six_hats":
            return self.brainstorming.apply_six_hats(task)
        elif technique == "scamper":
            return self.problem_innovator.apply_scamper(task)
        else:
            return self.brainstorming.use_technique(task, technique)
    
    def write_creative_content(self, topic: str, content_type: str) -> CreativeContent:
        """创作内容"""
        return self.creative_writer.generate_content(topic, content_type)
    
    def design_solution(self, problem: str) -> Dict:
        """设计解决方案"""
        empathize = self.design_thinking.empathize(problem)
        define = self.design_thinking.define(empathize["insights"])
        ideate = self.design_thinking.ideate(problem)
        
        return {
            "empathize": empathize,
            "define": define,
            "ideate": ideate
        }
    
    def get_creativity_tip(self, situation: str) -> Dict:
        """获取创意建议"""
        tips = {
            "meeting": "使用六顶思考帽，确保全面考虑",
            "brainstorming": "先 quantity 后 quality，鼓励疯狂想法",
            "writer_block": "自由写作10分钟，打破僵局",
            "innovation": "从用户痛点出发，寻找蓝海"
        }
        
        return {
            "situation": situation,
            "tip": tips.get(situation, "尝试随机输入法，强制建立联系"),
            "exercise": "写下5个'如果...会怎样'的问题"
        }
    
    def get_stats(self) -> Dict:
        """获取统计"""
        return {
            "techniques": len(self.db.INNOVATION_TECHNIQUES),
            "templates": len(self.db.CREATIVE_TEMPLATES),
            "triggers": len(self.db.CREATIVE_TRIGGERS)
        }


# 测试
if __name__ == "__main__":
    cm = CreativityManager()
    
    print("\n🦞 Creativity Manager 测试\n")
    
    # 创造力增强
    result = cm.enhance_creativity("生成一个新产品的创意")
    print(f"创造力增强: {result['suggested_technique']}")
    
    # 头脑风暴
    brainstorm = cm.brainstorm_ideas("移动应用")
    print(f"\n头脑风暴: 产生{len(brainstorm.ideas)}个创意")
    
    # 解决问题
    solution = cm.solve_problem("用户流失率高", "creative")
    print(f"\n问题解决: {len(solution['solutions'])}个方案")
    
    # 应用技术
    hats = cm.apply_technique("产品定价", "six_hats")
    print(f"\n六顶思考帽: {len(hats['hats'])}个帽子")
    
    # 设计解决方案
    design = cm.design_solution("在线教育互动性差")
    print(f"\n设计思维: {len(design['ideate'])}个构思")
    
    # 创意建议
    tip = cm.get_creativity_tip("brainstorming")
    print(f"\n创意建议: {tip['tip']}")
    
    print(f"\n统计: {cm.get_stats()}")
