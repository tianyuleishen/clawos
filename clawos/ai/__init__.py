# 🦞 ClawOS AI - 智能模块

"""
智能模块 - 语音、NLU、任务规划

功能:
- Speech Recognition (语音识别)
- Text-to-Speech (语音合成)
- Natural Language Understanding (自然语言理解)
- Task Planner (任务规划)
"""

from .speech_recognition import SpeechRecognizer, TranscriptionResult, AudioInfo
from .text_to_speech import TextToSpeech, TTSResult, VoiceInfo
from .nlu import (
    NaturalLanguageUnderstanding, 
    NLUResult, 
    Intent, 
    IntentType,
    Entity
)
from .task_planner import (
    TaskPlanner, 
    TaskPlan, 
    Task, 
    TaskStatus, 
    TaskPriority,
    ExecutionResult
)

__all__ = [
    # 语音识别
    'SpeechRecognizer',
    'TranscriptionResult',
    'AudioInfo',
    
    # 语音合成
    'TextToSpeech',
    'TTSResult',
    'VoiceInfo',
    
    # 自然语言理解
    'NaturalLanguageUnderstanding',
    'NLUResult',
    'Intent',
    'IntentType',
    'Entity',
    
    # 任务规划
    'TaskPlanner',
    'TaskPlan',
    'Task',
    'TaskStatus',
    'TaskPriority',
    'ExecutionResult',
]
