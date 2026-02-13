# 🦞 Pronoun Resolver - 指代词解析

"""
指代词解析模块

功能:
- 识别"它"、"那个"等指代词
- 根据上下文解析指代对象
"""

from typing import Dict, List, Optional
from dataclasses import dataclass


# 指代词映射
PRONOUNS = {
    "它": ["按钮", "输入框", "颜色", "界面", "文本框", "下拉框"],
    "他们": ["按钮", "输入框", "元素"],
    "那个": ["之前的", "刚才的", "左边的", "红色的", "大的"],
    "这个": ["当前的", "现在的", "右边的", "蓝色的", "小的"],
    "这里": ["当前位置", "当前页面", "当前输入框"],
    "那里": ["其他位置", "其他页面", "其他输入框"],
    "自己": ["用户自己", "系统自己"],
    "我": ["用户"],
    "你": ["系统", "助手"],
}


@dataclass
class PronounResolution:
    """指代词解析结果"""
    original: str
    resolved: str
    pronoun: str
    referent: str
    confidence: float


class PronounResolver:
    """指代词解析器"""
    
    def __init__(self):
        self.pronouns = PRONOUNS.copy()
        self.entity_types = {
            "按钮": ["button", "clickable"],
            "输入框": ["input", "textbox"],
            "颜色": ["color", "style"],
            "界面": ["ui", "interface"],
            "文本框": ["textarea", "input"],
            "下拉框": ["select", "dropdown"],
        }
    
    def resolve(self, text: str, context: Dict = None) -> str:
        """解析指代词
        
        Args:
            text: 原始文本
            context: 上下文（可选）
            
        Returns:
            解析后的文本
        """
        if context is None:
            context = {}
        
        result = text
        found_pronouns = []
        
        # 查找指代词
        for pronoun, referents in self.pronouns.items():
            if pronoun in text:
                # 查找最近的指代对象
                referent = self._find_referent(pronoun, referents, context)
                if referent:
                    result = result.replace(pronoun, referent, 1)
                    found_pronouns.append({
                        "pronoun": pronoun,
                        "referent": referent
                    })
        
        return result
    
    def resolve_detailed(self, text: str, context: Dict = None) -> List[PronounResolution]:
        """详细解析
        
        Returns:
            解析结果列表
        """
        if context is None:
            context = {}
        
        results = []
        
        for pronoun, referents in self.pronouns.items():
            if pronoun in text:
                referent = self._find_referent(pronoun, referents, context)
                if referent:
                    results.append(PronounResolution(
                        original=text,
                        resolved=text.replace(pronoun, referent, 1),
                        pronoun=pronoun,
                        referent=referent,
                        confidence=0.9
                    ))
        
        return results
    
    def _find_referent(
        self,
        pronoun: str,
        candidates: List[str],
        context: Dict
    ) -> Optional[str]:
        """查找指代对象"""
        # 1. 从上下文查找
        if "entities" in context:
            for entity in context["entities"]:
                if entity.get("type") in candidates:
                    return entity.get("value")
        
        # 2. 从颜色查找
        if "color" in context:
            if "颜色" in candidates:
                return context["color"]
        
        # 3. 从目标查找
        if "target" in context:
            if "界面" in candidates or "按钮" in candidates:
                return context["target"]
        
        # 4. 返回第一个候选
        return candidates[0] if candidates else None
    
    def add_custom_pronoun(self, pronoun: str, referents: List[str]):
        """添加自定义指代词"""
        self.pronouns[pronoun] = referents
    
    def get_stats(self) -> Dict:
        """获取统计"""
        return {
            "pronoun_count": len(self.pronouns),
            "entity_types": len(self.entity_types)
        }


# 测试
if __name__ == "__main__":
    resolver = PronounResolver()
    
    # 测试
    tests = [
        ("把它改成蓝色", {"color": "红色", "target": "按钮"}),
        ("那个太大了", {"size": "小"}),
        ("这里加一个按钮", {"page": "主页"}),
    ]
    
    for text, context in tests:
        resolved = resolver.resolve(text, context)
        print(f"原文: {text}")
        print(f"解析: {resolved}")
        print()
