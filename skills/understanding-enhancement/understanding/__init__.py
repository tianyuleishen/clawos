# 🦞 Understanding Enhancement Skill - 理解力提升技能

"""
理解力提升技能

功能:
- 指代词解析
- 上下文记忆
- 情绪识别
- 意图推断
"""

__version__ = "1.0.0"
__author__ = "ClawOS Team"

from .pronoun_resolver import PronounResolver
from .context_tracker import ContextTracker
from .emotion_recognizer import EmotionRecognizer
from .intent_inferrer import IntentInferrer
from .enhanced_understanding import EnhancedUnderstanding, UnderstandingResult

__all__ = [
    'PronounResolver',
    'ContextTracker',
    'EmotionRecognizer',
    'IntentInferrer',
    'EnhancedUnderstanding',
    'UnderstandingResult',
    '__version__',
]
