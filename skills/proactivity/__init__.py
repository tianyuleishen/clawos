# 🦞 Proactivity Enhancement Skill - 主动性增强

"""
主动性增强技能

功能:
- 主动建议
- 需求预测
- 推荐提供
- 主动帮助
- 预防性提醒
"""

from .proactivity import (
    ProactivityManager,
    ProactiveSuggester,
    NeedAnticipator,
    Recommender,
    PreventiveReminder,
    InitiativeTaker
)

__version__ = "1.0.0"
__all__ = [
    'ProactivityManager',
    'ProactiveSuggester',
    'NeedAnticipator',
    'Recommender',
    'PreventiveReminder',
    'InitiativeTaker',
]
