# 🦞 Onboarding - 首次安装引导

"""
首次安装引导 - ClawOS初始化配置

功能:
- 首次运行检测
- 模型选择界面
- API密钥配置
- 用户偏好设置
"""

import asyncio
import json
import os
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
import uuid
import getpass

from .storage.settings import UserSettings, SettingsStorage
from .storage.base import JSONStorage


# ============ 模型配置 ============

@dataclass
class ModelConfig:
    """模型配置"""
    name: str  # 显示名称
    provider: str  # 提供商
    model_id: str  # 模型ID
    api_base: str  # API地址
    is_cn: bool = False  # 是否国内模型
    features: List[str] = field(default_factory=list)  # 支持的功能
    default_params: Dict = field(default_factory=lambda: {
        "temperature": 0.7,
        "max_tokens": 4096,
        "top_p": 0.9
    })


# 预定义模型列表
AVAILABLE_MODELS = [
    # 国际模型
    ModelConfig(
        name="GPT-4o",
        provider="OpenAI",
        model_id="gpt-4o",
        api_base="https://api.openai.com/v1",
        is_cn=False,
        features=["reasoning", "chat", "function_call", "vision"],
        default_params={"temperature": 0.7, "max_tokens": 4096}
    ),
    ModelConfig(
        name="GPT-4o-mini",
        provider="OpenAI",
        model_id="gpt-4o-mini",
        api_base="https://api.openai.com/v1",
        is_cn=False,
        features=["reasoning", "chat", "function_call"],
        default_params={"temperature": 0.7, "max_tokens": 4096}
    ),
    ModelConfig(
        name="Claude 3.5 Sonnet",
        provider="Anthropic",
        model_id="claude-3-5-sonnet-20241022",
        api_base="https://api.anthropic.com/v1",
        is_cn=False,
        features=["reasoning", "chat", "long_context"],
        default_params={"temperature": 0.7, "max_tokens": 4096}
    ),
    ModelConfig(
        name="Claude 3 Haiku",
        provider="Anthropic",
        model_id="claude-3-haiku-20240307",
        api_base="https://api.anthropic.com/v1",
        is_cn=False,
        features=["chat", "fast"],
        default_params={"temperature": 0.7, "max_tokens": 4096}
    ),
    ModelConfig(
        name="Gemini 1.5 Pro",
        provider="Google",
        model_id="gemini-1.5-pro",
        api_base="https://generativelanguage.googleapis.com/v1beta",
        is_cn=False,
        features=["reasoning", "chat", "vision", "long_context"],
        default_params={"temperature": 0.7, "max_tokens": 4096}
    ),
    ModelConfig(
        name="Gemini 1.5 Flash",
        provider="Google",
        model_id="gemini-1.5-flash",
        api_base="https://generativelanguage.googleapis.com/v1beta",
        is_cn=False,
        features=["chat", "fast", "vision"],
        default_params={"temperature": 0.7, "max_tokens": 4096}
    ),
    
    # 🇨🇳 国内模型
    ModelConfig(
        name="通义千问 Qwen-Max",
        provider="阿里云",
        model_id="qwen-max",
        api_base="https://dashscope.aliyuncs.com/compatible-mode/v1",
        is_cn=True,
        features=["reasoning", "chat", "function_call"],
        default_params={"temperature": 0.7, "max_tokens": 4096}
    ),
    ModelConfig(
        name="通义千问 Qwen-Plus",
        provider="阿里云",
        model_id="qwen-plus",
        api_base="https://dashscope.aliyuncs.com/compatible-mode/v1",
        is_cn=True,
        features=["chat", "fast"],
        default_params={"temperature": 0.7, "max_tokens": 4096}
    ),
    ModelConfig(
        name="文心一言 ERNIE-4.5",
        provider="百度",
        model_id="ernie-4.5-8k-preview",
        api_base="https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop",
        is_cn=True,
        features=["reasoning", "chat"],
        default_params={"temperature": 0.7, "max_tokens": 4096}
    ),
    ModelConfig(
        name="文心一言 ERNIE-3.5",
        provider="百度",
        model_id="ernie-3.5-8k",
        api_base="https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop",
        is_cn=True,
        features=["chat", "fast"],
        default_params={"temperature": 0.7, "max_tokens": 4096}
    ),
    ModelConfig(
        name="智谱 GLM-4",
        provider="智谱AI",
        model_id="glm-4",
        api_base="https://open.bigmodel.cn/api/paas/v4",
        is_cn=True,
        features=["reasoning", "chat", "function_call"],
        default_params={"temperature": 0.7, "max_tokens": 4096}
    ),
    ModelConfig(
        name="智谱 GLM-4V (视觉)",
        provider="智谱AI",
        model_id="glm-4v",
        api_base="https://open.bigmodel.cn/api/paas/v4",
        is_cn=True,
        features=["chat", "vision"],
        default_params={"temperature": 0.7, "max_tokens": 4096}
    ),
    ModelConfig(
        name="Kimi (Moonshot)",
        provider="月之暗面",
        model_id="moonshot-v1-8k",
        api_base="https://api.moonshot.cn/v1",
        is_cn=True,
        features=["chat", "long_context"],
        default_params={"temperature": 0.7, "max_tokens": 4096}
    ),
    ModelConfig(
        name="Kimi-VL (视觉)",
        provider="月之暗面",
        model_id="moonshot-v1-vl-8k",
        api_base="https://api.moonshot.cn/v1",
        is_cn=True,
        features=["chat", "vision"],
        default_params={"temperature": 0.7, "max_tokens": 4096}
    ),
    ModelConfig(
        name="讯飞星火 Spark-4.0",
        provider="讯飞",
        model_id="spark-4.0",
        api_base="https://spark-api.xf-yun.com/v1",
        is_cn=True,
        features=["reasoning", "chat"],
        default_params={"temperature": 0.7, "max_tokens": 4096}
    ),
    ModelConfig(
        name="腾讯混元 Hunyuan",
        provider="腾讯云",
        model_id="hunyuan",
        api_base="https://hunyuan.tencentcloudapi.com/v1",
        is_cn=True,
        features=["chat", "reasoning"],
        default_params={"temperature": 0.7, "max_tokens": 4096}
    ),
    
    # MiniMax (用户指定)
    ModelConfig(
        name="MiniMax-ABAB",
        provider="MiniMax",
        model_id="abab6.5s-chat",
        api_base="https://api.minimax.chat/v1",
        is_cn=True,
        features=["chat", "fast"],
        default_params={"temperature": 0.7, "max_tokens": 4096}
    ),
]


@dataclass
class OnboardingSettings:
    """引导配置"""
    # 模型配置
    selected_model: str = ""
    api_key: str = ""
    api_base: str = ""
    
    # 用户信息
    user_name: str = ""
    
    # 偏好设置
    language: str = "zh"
    theme: str = "dark"
    
    # 元数据
    is_first_run: bool = True
    setup_completed_at: float = 0


class OnboardingManager:
    """引导管理器"""
    
    def __init__(self):
        self.data_dir = Path("./data")
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.config_file = self.data_dir / "onboarding.json"
        self.settings_storage = SettingsStorage()
        
        self.onboarding_settings = self._load_settings()
    
    def _load_settings(self) -> OnboardingSettings:
        """加载引导设置"""
        if self.config_file.exists() and self.config_file.stat().st_size > 0:
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return OnboardingSettings(**data)
            except (json.JSONDecodeError, KeyError):
                return OnboardingSettings()
        return OnboardingSettings()
    
    def _save_settings(self):
        """保存引导设置"""
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(asdict(self.onboarding_settings), f, ensure_ascii=False, indent=2)
    
    def is_first_run(self) -> bool:
        """检查是否是首次运行"""
        return self.onboarding_settings.is_first_run
    
    def mark_setup_complete(self):
        """标记设置完成"""
        self.onboarding_settings.is_first_run = False
        self.onboarding_settings.setup_completed_at = datetime.now().timestamp()
        self._save_settings()
    
    # ============ 模型管理 ============
    
    def get_models(self, region: str = "all") -> List[ModelConfig]:
        """获取模型列表"""
        if region == "cn":
            return [m for m in AVAILABLE_MODELS if m.is_cn]
        elif region == "international":
            return [m for m in AVAILABLE_MODELS if not m.is_cn]
        return AVAILABLE_MODELS
    
    def get_model_by_id(self, model_id: str) -> Optional[ModelConfig]:
        """根据ID获取模型"""
        for model in AVAILABLE_MODELS:
            if model.model_id == model_id:
                return model
        return None
    
    def set_model(self, model_id: str, api_key: str):
        """设置模型"""
        model = self.get_model_by_id(model_id)
        if model:
            self.onboarding_settings.selected_model = model_id
            self.onboarding_settings.api_key = api_key
            self.onboarding_settings.api_base = model.api_base
            self._save_settings()
            return True
        return False
    
    def get_current_model(self) -> Optional[ModelConfig]:
        """获取当前模型"""
        return self.get_model_by_id(self.onboarding_settings.selected_model)
    
    def get_api_key(self) -> str:
        """获取API密钥"""
        return self.onboarding_settings.api_key
    
    def get_api_base(self) -> str:
        """获取API地址"""
        return self.onboarding_settings.api_base
    
    # ============ 用户设置 ============
    
    def set_user_name(self, name: str):
        """设置用户名"""
        self.onboarding_settings.user_name = name
        self._save_settings()
    
    def set_language(self, lang: str):
        """设置语言"""
        self.onboarding_settings.language = lang
        self._save_settings()
    
    def set_theme(self, theme: str):
        """设置主题"""
        self.onboarding_settings.theme = theme
        self._save_settings()
    
    def apply_to_settings(self) -> UserSettings:
        """应用到用户设置"""
        settings = self.settings_storage.load()
        
        settings.language = self.onboarding_settings.language
        settings.theme = self.onboarding_settings.theme
        
        if self.onboarding_settings.user_name:
            settings.user_name = self.onboarding_settings.user_name
        
        self.settings_storage.save(settings)
        return settings
    
    # ============ 引导界面 ============
    
    def print_banner(self):
        """打印横幅"""
        print("""
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║              🦞 ClawOS AI 操作系统 - 首次设置                     ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
        """)
    
    def print_model_list(self, models: List[ModelConfig]):
        """打印模型列表"""
        print("\n📋 可用模型:")
        print("-" * 70)
        
        for i, model in enumerate(models, 1):
            region = "🇨🇳" if model.is_cn else "🌏"
            features = ", ".join(model.features[:3])
            print(f"  {i:2d}. {region} {model.name}")
            print(f"      提供商: {model.provider} | 功能: {features}")
        
        print("-" * 70)
    
    async def run_onboarding(self) -> bool:
        """运行引导流程"""
        self.print_banner()
        
        # 检查是否已设置
        if not self.is_first_run():
            print("✅ 您已完成初始设置，如需重新配置请使用 --reconfigure")
            return True
        
        # Step 1: 选择模型
        print("\n🚀 Step 1: 选择AI模型")
        print("   您可以从以下模型中选择（按编号选择）:")
        
        models = self.get_models()
        self.print_model_list(models)
        
        while True:
            try:
                choice = input("\n👉 请选择模型编号 (1-{}): ".format(len(models))).strip()
                idx = int(choice) - 1
                
                if 0 <= idx < len(models):
                    selected_model = models[idx]
                    print(f"\n✅ 已选择: {selected_model.name}")
                    break
                else:
                    print("❌ 编号无效，请重新选择")
            except ValueError:
                print("❌ 请输入数字")
        
        # Step 2: 输入API密钥
        print(f"\n🔑 Step 2: 配置API密钥")
        print(f"   请输入 {selected_model.provider} 的API密钥:")
        
        api_key = getpass.getpass("   API Key: ").strip()
        
        if not api_key:
            print("⚠️  未输入API密钥，将使用测试模式")
            api_key = ""
        
        # Step 3: 用户名
        print(f"\n👤 Step 3: 您的称呼")
        user_name = input("   请输入您的名字 (可选): ").strip()
        
        # Step 4: 语言偏好
        print(f"\n🌐 Step 4: 语言偏好")
        print("   1. 简体中文")
        print("   2. English")
        
        lang_choice = input("   请选择 (1-2, 默认1): ").strip() or "1"
        self.set_language("zh" if lang_choice == "1" else "en")
        
        # Step 5: 主题偏好
        print(f"\n🎨 Step 5: 主题偏好")
        print("   1. 深色主题")
        print("   2. 浅色主题")
        print("   3. 跟随系统")
        
        theme_choice = input("   请选择 (1-3, 默认1): ").strip() or "1"
        theme_map = {"1": "dark", "2": "light", "3": "auto"}
        self.set_theme(theme_map.get(theme_choice, "dark"))
        
        # Step 6: 保存配置
        print(f"\n💾 Step 6: 保存配置")
        self.set_model(selected_model.model_id, api_key)
        self.set_user_name(user_name)
        self.mark_setup_complete()
        self.apply_to_settings()
        
        print("\n" + "=" * 70)
        print("✅ 配置完成！")
        print(f"   模型: {selected_model.name}")
        print(f"   语言: {'中文' if self.onboarding_settings.language == 'zh' else 'English'}")
        print(f"   主题: {self.onboarding_settings.theme}")
        print("=" * 70)
        
        return True
    
    async def reconfigure(self):
        """重新配置"""
        self.onboarding_settings = OnboardingSettings()
        self._save_settings()
        await self.run_onboarding()
    
    def get_status(self) -> Dict:
        """获取状态"""
        model = self.get_current_model()
        
        return {
            'is_first_run': self.is_first_run(),
            'model': model.name if model else None,
            'provider': model.provider if model else None,
            'is_cn': model.is_cn if model else None,
            'user_name': self.onboarding_settings.user_name,
            'language': self.onboarding_settings.language,
            'theme': self.onboarding_settings.theme,
            'setup_completed_at': self.onboarding_settings.setup_completed_at
        }


# 便捷函数
def get_onboarding_manager() -> OnboardingManager:
    """获取引导管理器"""
    return OnboardingManager()


# 测试代码
if __name__ == "__main__":
    print("🦞 Onboarding 测试")
    
    manager = OnboardingManager()
    
    print(f"首次运行: {manager.is_first_run()}")
    
    # 测试模型列表
    cn_models = manager.get_models("cn")
    intl_models = manager.get_models("international")
    
    print(f"国内模型: {len(cn_models)} 个")
    print(f"国际模型: {len(intl_models)} 个")
    print(f"总计: {len(AVAILABLE_MODELS)} 个")
    
    # 获取状态
    status = manager.get_status()
    print(f"状态: {status}")
    
    print("\n✅ 测试完成")
