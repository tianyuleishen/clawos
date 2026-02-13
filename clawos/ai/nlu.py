# 🦞 Natural Language Understanding - 自然语言理解

"""
自然语言理解 - 意图识别和实体提取

功能:
- 意图分类
- 实体识别
- 情感分析
- 关键词提取
"""

import asyncio
import re
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
from collections import Counter

# 尝试导入jieba，如果不可用则使用简单分词
try:
    import jieba
    import jieba.posseg as pseg
    JIEBA_AVAILABLE = True
except ImportError:
    JIEBA_AVAILABLE = False
    print("⚠️ jieba不可用，使用简单分词")


class IntentType(Enum):
    """意图类型"""
    GREETING = "greeting"
    GOODBYE = "goodbye"
    HELP = "help"
    LAUNCH_APP = "launch_app"
    CLOSE_APP = "close_app"
    SWITCH_APP = "switch_app"
    OPEN_FILE = "open_file"
    CREATE_FILE = "create_file"
    DELETE_FILE = "delete_file"
    SEARCH_FILE = "search_file"
    OPEN_URL = "open_url"
    SEARCH_WEB = "search_web"
    DOWNLOAD = "download"
    SHUTDOWN = "shutdown"
    RESTART = "restart"
    LOCK = "lock"
    WEATHER = "weather"
    TIME = "time"
    DATE = "date"
    CALCULATE = "calculate"
    CHAT = "chat"
    EXPLAIN = "explain"
    TRANSLATE = "translate"
    SUMMARY = "summary"
    PLAY_MUSIC = "play_music"
    PLAY_VIDEO = "play_video"
    SCREENSHOT = "screenshot"
    UNKNOWN = "unknown"


@dataclass
class Entity:
    text: str
    type: str
    value: str
    start: int
    end: int
    confidence: float


@dataclass
class Intent:
    type: IntentType
    confidence: float
    text: str
    entities: List[Entity] = field(default_factory=list)
    slots: Dict[str, str] = field(default_factory=dict)


@dataclass
class NLUResult:
    text: str
    language: str
    intents: List[Intent]
    primary_intent: Intent
    entities: List[Entity]
    sentiment: str
    keywords: List[str]
    success: bool


class NaturalLanguageUnderstanding:
    """自然语言理解"""
    
    def __init__(self):
        if JIEBA_AVAILABLE:
            jieba.initialize()
        
        self.intent_keywords = {
            IntentType.GREETING: ["你好", "hello", "hi", "嗨", "在吗", "早", "晚安"],
            IntentType.GOODBYE: ["再见", "拜拜", "bye", "晚安", "明天见"],
            IntentType.HELP: ["帮助", "help", "怎么用", "说明"],
            IntentType.LAUNCH_APP: ["打开", "启动", "运行", "开始", "开启"],
            IntentType.CLOSE_APP: ["关闭", "关掉", "退出", "停止", "结束"],
            IntentType.SWITCH_APP: ["切换", "转到", "去", "切到"],
            IntentType.OPEN_FILE: ["打开", "查看", "看", "阅读", "编辑"],
            IntentType.CREATE_FILE: ["创建", "新建", "生成", "写", "建立"],
            IntentType.DELETE_FILE: ["删除", "删掉", "移除", "去掉"],
            IntentType.SEARCH_FILE: ["搜索", "查找", "找"],
            IntentType.OPEN_URL: ["打开网址", "访问", "浏览"],
            IntentType.SEARCH_WEB: ["搜索", "百度", "谷歌", "上网查"],
            IntentType.DOWNLOAD: ["下载", "保存", "获取"],
            IntentType.SHUTDOWN: ["关机", "关闭电脑"],
            IntentType.RESTART: ["重启", "重新启动"],
            IntentType.LOCK: ["锁定", "锁屏", "锁电脑"],
            IntentType.WEATHER: ["天气", "气温", "温度"],
            IntentType.TIME: ["现在几点", "时间", "几点"],
            IntentType.DATE: ["今天几号", "日期", "今天"],
            IntentType.CALCULATE: ["计算", "等于", "多少"],
            IntentType.CHAT: ["聊天", "说话", "对话"],
            IntentType.EXPLAIN: ["解释", "说明", "是什么"],
            IntentType.TRANSLATE: ["翻译", "英文"],
            IntentType.SUMMARY: ["总结", "概括"],
            IntentType.PLAY_MUSIC: ["播放音乐", "听歌", "音乐"],
            IntentType.PLAY_VIDEO: ["播放视频", "看视频"],
            IntentType.SCREENSHOT: ["截图", "截屏"],
        }
        
        self.app_names = {
            "chrome": ["chrome", "谷歌", "谷歌浏览器", "浏览器"],
            "firefox": ["firefox", "火狐"],
            "vscode": ["vscode", "代码编辑器"],
            "notepad": ["notepad", "记事本"],
            "terminal": ["terminal", "终端", "命令行"],
            "calculator": ["calculator", "计算器"],
        }
        
        print("✅ Natural Language Understanding 已加载")
    
    async def understand(self, text: str) -> NLUResult:
        text = text.strip()
        if not text:
            return NLUResult(text="", language="unknown", intents=[], 
                           primary_intent=None, entities=[], sentiment="neutral", 
                           keywords=[], success=False)
        
        language = self._detect_language(text)
        words = self._tokenize(text)
        keywords = self._extract_keywords(words)
        sentiment = self._analyze_sentiment(text)
        intents = await self._recognize_intent(text, words)
        entities = await self._extract_entities(text, words)
        
        for intent in intents:
            await self._fill_slots(intent, entities)
        
        primary_intent = intents[0] if intents else Intent(
            type=IntentType.UNKNOWN, confidence=0.0, text=text
        )
        
        return NLUResult(
            text=text, language=language, intents=intents,
            primary_intent=primary_intent, entities=entities,
            sentiment=sentiment, keywords=keywords, success=True
        )
    
    def _detect_language(self, text: str) -> str:
        chinese_chars = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
        total_chars = len(text)
        if total_chars == 0:
            return "unknown"
        ratio = chinese_chars / total_chars
        if ratio > 0.5:
            return "zh"
        elif ratio > 0.3:
            return "mixed"
        return "en"
    
    def _tokenize(self, text: str) -> List[str]:
        if JIEBA_AVAILABLE:
            words = jieba.lcut(text)
        else:
            words = list(text)
        return [w.strip() for w in words if w.strip()]
    
    def _extract_keywords(self, words: List[str]) -> List[str]:
        stopwords = {'的', '了', '是', '在', '我', '有', '和', '就', '不', '都', '一', '什么'}
        keywords = [w for w in words if w not in stopwords and len(w) > 1]
        counter = Counter(keywords)
        return [word for word, _ in counter.most_common(10)]
    
    async def _recognize_intent(self, text: str, words: List[str]) -> List[Intent]:
        text_lower = text.lower()
        intents = []
        
        for intent_type, keywords in self.intent_keywords.items():
            confidence = 0.0
            for keyword in keywords:
                if keyword.lower() in text_lower:
                    confidence += 0.3
            
            for word in words:
                for keyword in keywords:
                    if keyword in word or word in keyword:
                        confidence += 0.2
            
            confidence = min(1.0, confidence)
            if confidence > 0.1:
                intents.append(Intent(type=intent_type, confidence=confidence, text=text))
        
        intents.sort(key=lambda x: x.confidence, reverse=True)
        return intents[:5]
    
    async def _extract_entities(self, text: str, words: List[str]) -> List[Entity]:
        entities = []
        
        for app_key, app_names in self.app_names.items():
            for name in app_names:
                if name in text.lower():
                    entities.append(Entity(text=name, type="APP", value=app_key,
                                           start=text.lower().find(name),
                                           end=text.lower().find(name) + len(name), confidence=0.9))
        
        urls = re.findall(r'https?://[^\s]+', text)
        for url in urls:
            entities.append(Entity(text=url, type="URL", value=url, start=text.find(url),
                                   end=text.find(url) + len(url), confidence=0.95))
        
        file_paths = re.findall(r'[A-Za-z]:\\[^"\n]+|/[^"\n]+', text)
        for path in file_paths:
            entities.append(Entity(text=path, type="FILE_PATH", value=path, start=text.find(path),
                                   end=text.find(path) + len(path), confidence=0.85))
        
        numbers = re.findall(r'\d+', text)
        for num in numbers:
            entities.append(Entity(text=num, type="NUMBER", value=num, start=text.find(num),
                                   end=text.find(num) + len(num), confidence=0.7))
        
        return entities
    
    async def _fill_slots(self, intent: Intent, entities: List[Entity]):
        for entity in entities:
            if entity.type == "APP":
                intent.slots["app_name"] = entity.value
            elif entity.type == "URL":
                intent.slots["url"] = entity.value
            elif entity.type == "FILE_PATH":
                intent.slots["file_path"] = entity.value
            elif entity.type == "NUMBER":
                intent.slots["number"] = entity.value
    
    def _analyze_sentiment(self, text: str) -> str:
        positive = ["好", "棒", "优秀", "完美", "喜欢", "开心", "感谢", "谢谢"]
        negative = ["坏", "差", "糟糕", "讨厌", "生气", "难过", "抱歉"]
        pos = sum(1 for w in positive if w in text)
        neg = sum(1 for w in negative if w in text)
        if pos > neg:
            return "positive"
        elif neg > pos:
            return "negative"
        return "neutral"


async def understand(text: str) -> NLUResult:
    nlu = NaturalLanguageUnderstanding()
    return await nlu.understand(text)


async def get_intent(text: str) -> Intent:
    nlu = NaturalLanguageUnderstanding()
    return await nlu.get_intent(text)


if __name__ == "__main__":
    async def test():
        print("🗣️ 自然语言理解测试")
        nlu = NaturalLanguageUnderstanding()
        
        tests = ["打开Chrome浏览器", "帮我搜索天气", "现在几点了"]
        for t in tests:
            r = await nlu.understand(t)
            print(f"{t} → {r.primary_intent.type.value}")
        
        print("\n✅ 测试完成")
    
    asyncio.run(test())
