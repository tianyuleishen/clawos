# 🦞 Intent Inferrer - 意图推断

"""
意图推断模块

功能:
- 从用户输入推断真实意图
- 识别隐含需求
- 生成解决建议
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
from .emotion_recognizer import EmotionRecognizer, EmotionType


class IntentCategory(Enum):
    """意图类别"""
    MODIFICATION = "modification"      # 修改
    QUERY = "query"                   # 查询
    EXECUTION = "execution"           # 执行
    COMPLAINT = "complaint"           # 抱怨
    PRAISE = "praise"                 # 赞美
    CONFUSION = "confusion"           # 困惑
    UNKNOWN = "unknown"               # 未知


@dataclass
class IntentResult:
    """意图推断结果"""
    category: str          # 意图类别
    action: str            # 具体动作
    target: str            # 目标对象
    parameters: Dict       # 参数
    implied_needs: List[str]  # 隐含需求
    confidence: float      # 置信度
    suggestions: List[str]  # 建议


# 意图模式
INTENT_PATTERNS = {
    IntentCategory.MODIFICATION: [
        ("改成", "修改"),
        ("改为", "修改"),
        ("改", "修改"),
        ("换", "替换"),
        ("调整", "调整"),
        ("设置", "设置"),
        ("添加", "添加"),
        ("删除", "删除"),
        ("去掉", "删除"),
    ],
    IntentCategory.QUERY: [
        ("是什么", "查询定义"),
        ("怎么", "查询方法"),
        ("多少", "查询数量"),
        ("哪里", "查询位置"),
        ("谁", "查询身份"),
        ("什么时候", "查询时间"),
    ],
    IntentCategory.EXECUTION: [
        ("帮我", "执行操作"),
        ("做一个", "创建"),
        ("生成", "生成内容"),
        ("计算", "计算结果"),
        ("分析", "分析问题"),
    ],
    IntentCategory.COMPLAINT: [
        ("太慢", "性能抱怨"),
        ("太难", "难度抱怨"),
        ("不对", "错误抱怨"),
        ("不行", "失败抱怨"),
        ("错了", "错误抱怨"),
    ],
    IntentCategory.PRAISE: [
        ("不错", "正面评价"),
        ("很好", "正面评价"),
        ("厉害", "正面评价"),
        ("感谢", "感谢"),
    ],
    IntentCategory.CONFUSION: [
        ("不懂", "寻求解释"),
        ("什么意思", "寻求解释"),
        ("怎么用", "寻求指导"),
    ],
}


# 隐含需求模式
IMPLIED_NEED_PATTERNS = [
    (("太慢", "速度"), "性能", "优化响应速度"),
    (("太复杂", "麻烦"), "易用性", "简化操作流程"),
    (("不好看", "丑"), "UI", "改进界面设计"),
    (("不对", "错了"), "准确性", "提高准确度"),
    (("不会", "不懂"), "学习", "提供教程/帮助"),
    (("太贵", "价格"), "成本", "考虑性价比"),
    (("不安全", "担心"), "安全", "增强安全保障"),
]


class IntentInferrer:
    """意图推断器"""
    
    def __init__(self):
        self.patterns = INTENT_PATTERNS.copy()
        self.need_patterns = IMPLIED_NEED_PATTERNS.copy()
        self.emotion_recognizer = EmotionRecognizer()
    
    def infer(self, text: str) -> IntentResult:
        """
        推断意图
        
        Args:
            text: 用户输入
            
        Returns:
            IntentResult: 意图推断结果
        """
        text_lower = text.lower()
        
        # 1. 识别情绪
        emotion_result = self.emotion_recognizer.recognize(text)
        emotion = emotion_result.emotion
        
        # 2. 推断意图类别
        category = self._infer_category(text_lower)
        
        # 3. 提取动作和目标
        action, target = self._extract_action_target(text)
        
        # 4. 推断隐含需求
        implied_needs = self._infer_implied_needs(text, emotion)
        
        # 5. 生成建议
        suggestions = self._generate_suggestions(category, emotion, implied_needs)
        
        # 6. 计算置信度
        confidence = self._calculate_confidence(text, category, emotion)
        
        return IntentResult(
            category=category.value,
            action=action,
            target=target,
            parameters={},
            implied_needs=implied_needs,
            confidence=confidence,
            suggestions=suggestions
        )
    
    def _infer_category(self, text_lower: str) -> IntentCategory:
        """推断意图类别"""
        scores = {}
        
        for category, patterns in self.patterns.items():
            score = sum(1 for kw in patterns if any(k in text_lower for k in kw))
            if score > 0:
                scores[category] = score
        
        if scores:
            return max(scores, key=scores.get)
        
        return IntentCategory.UNKNOWN
    
    def _extract_action_target(self, text: str) -> Tuple[str, str]:
        """提取动作和目标"""
        # 常见动作
        actions = ["修改", "设置", "添加", "删除", "查询", "执行"]
        targets = ["颜色", "大小", "速度", "按钮", "界面", "输入框"]
        
        action = "未知"
        target = "未知"
        
        for a in actions:
            if a in text:
                action = a
                break
        
        for t in targets:
            if t in text:
                target = t
                break
        
        return action, target
    
    def _infer_implied_needs(self, text: str, emotion: str) -> List[str]:
        """推断隐含需求"""
        needs = []
        
        # 从文本模式推断
        for keywords, category, need in self.need_patterns:
            if all(kw in text for kw in keywords):
                needs.append(need)
        
        # 从情绪推断
        emotion_needs = self.emotion_recognizer.get_implied_needs(text)
        needs.extend(emotion_needs)
        
        return list(set(needs))  # 去重
    
    def _generate_suggestions(
        self,
        category: IntentCategory,
        emotion: str,
        needs: List[str]
    ) -> List[str]:
        """生成建议"""
        suggestions = []
        
        # 情绪相关建议
        if emotion in [EmotionType.FRUSTRATED.value, EmotionType.IMPATIENT.value]:
            suggestions.append("提供简化方案")
            suggestions.append("加快响应速度")
        
        if emotion == EmotionType.CONFUSED.value:
            suggestions.append("提供详细说明")
            suggestions.append("给出使用示例")
        
        # 需求相关建议
        for need in needs:
            if "性能" in need:
                suggestions.append("优化处理速度")
            elif "易用性" in need:
                suggestions.append("简化操作流程")
            elif "准确性" in need:
                suggestions.append("提高准确度")
            elif "学习" in need:
                suggestions.append("提供教程")
        
        return suggestions
    
    def _calculate_confidence(
        self,
        text: str,
        category: IntentCategory,
        emotion: str
    ) -> float:
        """计算置信度"""
        confidence = 0.5  # 基础置信度
        
        # 匹配关键词增加置信度
        for patterns in self.patterns.values():
            for kw in patterns:
                if any(k in text for k in kw):
                    confidence += 0.1
        
        # 有明确情绪增加置信度
        if emotion != EmotionType.NEUTRAL.value:
            confidence += 0.1
        
        return min(1.0, confidence)
    
    def add_pattern(self, category: IntentCategory, patterns: List[Tuple[str, str]]):
        """添加自定义模式"""
        if category not in self.patterns:
            self.patterns[category] = []
        self.patterns[category].extend(patterns)
    
    def get_stats(self) -> Dict:
        """获取统计"""
        return {
            "category_count": len(self.patterns),
            "need_patterns": len(self.need_patterns)
        }


# 测试
if __name__ == "__main__":
    inferrer = IntentInferrer()
    
    tests = [
        "把按钮颜色改成蓝色",
        "太慢了，受不了了",
        "怎么使用这个功能？",
        "不对啊，结果错了",
        "不错，挺好用的"
    ]
    
    for text in tests:
        result = inferrer.infer(text)
        
        print(f"输入: {text}")
        print(f"类别: {result.category}")
        print(f"动作: {result.action}")
        print(f"目标: {result.target}")
        print(f"隐含需求: {result.implied_needs}")
        print(f"置信度: {result.confidence:.0%}")
        print(f"建议: {result.suggestions}")
        print()
