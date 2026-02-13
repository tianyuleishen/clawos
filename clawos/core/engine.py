# 🦞 ClawOS Core Engine - 核心引擎

"""
核心引擎 - 统一所有模块

功能:
- 统一初始化
- 模块协调
- 性能优化
"""

import asyncio
import time
from typing import Dict, Any, Optional
from dataclasses import dataclass
from pathlib import Path

from ..storage.settings import SettingsStorage
from ..storage.memory import MemoryStorage
from ..storage.conversation import ConversationStorage
from ..onboarding import get_onboarding_manager


@dataclass
class EngineStats:
    """引擎统计"""
    startup_time: float = 0.0
    modules_loaded: int = 0
    memory_usage: float = 0.0
    last_active: float = 0.0


class ClawOSEngine:
    """ClawOS核心引擎"""
    
    def __init__(self):
        self.start_time = time.time()
        self.stats = EngineStats()
        
        self.settings = None
        self.memory = None
        self.conversation = None
        self.onboarding = None
        
        self.modules: Dict[str, Any] = {}
        self.running = False
        
        print("🦞 ClawOS 核心引擎初始化...")
    
    async def initialize(self) -> bool:
        """初始化所有模块"""
        try:
            start = time.time()
            
            # 加载存储
            self.settings = SettingsStorage()
            self.memory = MemoryStorage()
            self.conversation = ConversationStorage()
            self.onboarding = get_onboarding_manager()
            
            # 加载核心模块
            from .reasoning import UltimateFusionEngine
            self.modules['reasoning'] = UltimateFusionEngine()
            
            from .consciousness import L11Consciousness
            self.modules['consciousness'] = L11Consciousness()
            
            from .emotion import EmotionModule
            self.modules['emotion'] = EmotionModule()
            
            # 加载控制模块
            from ..controls.mouse import MouseController
            from ..controls.keyboard import KeyboardController
            self.modules['mouse'] = MouseController()
            self.modules['keyboard'] = KeyboardController()
            
            # 加载AI模块
            from ..ai.nlu import NaturalLanguageUnderstanding
            self.modules['nlu'] = NaturalLanguageUnderstanding()
            
            self.stats.startup_time = time.time() - start
            self.stats.modules_loaded = len(self.modules)
            
            self.running = True
            print(f"✅ 初始化完成 ({self.stats.startup_time:.2f}s)")
            return True
            
        except Exception as e:
            print(f"❌ 初始化失败: {e}")
            return False
    
    async def process(self, input_text: str) -> Dict[str, Any]:
        """处理输入"""
        if not self.running:
            return {'error': 'Engine not initialized'}
        
        start = time.time()
        
        # 获取当前模型
        model = self.onboarding.get_current_model()
        
        # NLU处理
        nlu_result = await self.modules['nlu'].understand(input_text)
        
        # 推理
        reasoning_result = await self.modules['reasoning'].analyze(input_text)
        
        # 意识处理
        consciousness_result = await self.modules['consciousness'].query(input_text)
        
        # 情感处理
        emotion_result = self.modules['emotion'].process(input_text)
        
        return {
            'input': input_text,
            'model': model.name if model else 'default',
            'nlu': nlu_result,
            'reasoning': reasoning_result,
            'consciousness': consciousness_result,
            'emotion': emotion_result,
            'processing_time': time.time() - start
        }
    
    def get_status(self) -> Dict:
        """获取状态"""
        return {
            'running': self.running,
            'modules': list(self.modules.keys()),
            'stats': self.stats.__dict__,
            'model': self.onboarding.get_current_model().name if self.onboarding.get_current_model() else None
        }
    
    async def shutdown(self):
        """关闭引擎"""
        self.running = False
        print("🦞 ClawOS 已关闭")


# 单例引擎
_engine: Optional[ClawOSEngine] = None

def get_engine() -> ClawOSEngine:
    """获取引擎单例"""
    global _engine
    if _engine is None:
        _engine = ClawOSEngine()
    return _engine
