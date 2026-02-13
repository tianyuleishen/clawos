# 🦞 Control Panel - 控制面板

"""
控制面板 - ClawOS系统控制

功能:
- 系统状态
- 快速操作
- 设置管理
- 模块控制
"""

import asyncio
import json
from typing import Dict, List, Callable, Any, Optional
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
import os

class ModuleStatus(Enum):
    """模块状态"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    LOADING = "loading"
    ERROR = "error"

@dataclass
class ControlItem:
    """控制项"""
    id: str
    name: str
    icon: str
    description: str
    status: ModuleStatus
    action: str  # 可执行的动作
    enabled: bool = True
    metadata: Dict = None

@dataclass
class SystemStatus:
    """系统状态"""
    cpu_usage: float = 0.0
    memory_usage: float = 0.0
    disk_usage: float = 0.0
    active_modules: int = 0
    total_modules: int = 0
    uptime: float = 0.0
    last_update: float = 0.0


class ControlPanel:
    """控制面板"""
    
    def __init__(self):
        self.items: Dict[str, ControlItem] = {}
        self.callbacks: Dict[str, Callable] = {}
        self.settings: Dict[str, Any] = {}
        self.start_time = datetime.now().timestamp()
        
        # 初始化默认控制项
        self._init_default_items()
        
        print("✅ Control Panel 已加载")
    
    def _init_default_items(self):
        """初始化默认控制项"""
        default_items = [
            # 核心模块
            ControlItem(
                id="consciousness",
                name="意识系统",
                icon="🧠",
                description="L11意识引擎",
                status=ModuleStatus.ACTIVE,
                action="toggle_consciousness"
            ),
            ControlItem(
                id="reasoning",
                name="推理引擎",
                icon="🧩",
                description="终极融合推理",
                status=ModuleStatus.ACTIVE,
                action="toggle_reasoning"
            ),
            ControlItem(
                id="emotion",
                name="情感模块",
                icon="❤️",
                description="情感感知与表达",
                status=ModuleStatus.ACTIVE,
                action="toggle_emotion"
            ),
            
            # 控制模块
            ControlItem(
                id="mouse",
                name="鼠标控制",
                icon="🖱️",
                description="鼠标自动化",
                status=ModuleStatus.ACTIVE,
                action="toggle_mouse"
            ),
            ControlItem(
                id="keyboard",
                name="键盘控制",
                icon="⌨️",
                description="键盘自动化",
                status=ModuleStatus.ACTIVE,
                action="toggle_keyboard"
            ),
            ControlItem(
                id="window",
                name="窗口管理",
                icon="🪟",
                description="窗口控制",
                status=ModuleStatus.ACTIVE,
                action="toggle_window"
            ),
            
            # 文件模块
            ControlItem(
                id="file_manager",
                name="文件管理",
                icon="📁",
                description="文件操作",
                status=ModuleStatus.ACTIVE,
                action="toggle_file"
            ),
            ControlItem(
                id="search",
                name="文件搜索",
                icon="🔍",
                description="全文搜索",
                status=ModuleStatus.ACTIVE,
                action="toggle_search"
            ),
            
            # AI模块
            ControlItem(
                id="speech",
                name="语音识别",
                icon="🎤",
                description="语音转文字",
                status=ModuleStatus.INACTIVE,
                action="toggle_speech"
            ),
            ControlItem(
                id="tts",
                name="语音合成",
                icon="🔊",
                description="文字转语音",
                status=ModuleStatus.INACTIVE,
                action="toggle_tts"
            ),
            ControlItem(
                id="nlu",
                name="意图理解",
                icon="🗣️",
                description="自然语言理解",
                status=ModuleStatus.ACTIVE,
                action="toggle_nlu"
            ),
            
            # 系统
            ControlItem(
                id="terminal",
                name="终端",
                icon="💻",
                description="命令执行",
                status=ModuleStatus.ACTIVE,
                action="toggle_terminal"
            ),
            ControlItem(
                id="browser",
                name="浏览器",
                icon="🌐",
                description="网页浏览",
                status=ModuleStatus.ACTIVE,
                action="toggle_browser"
            ),
        ]
        
        for item in default_items:
            self.items[item.id] = item
    
    # ============ 控制项管理 ============
    
    def get_item(self, item_id: str) -> Optional[ControlItem]:
        """获取控制项"""
        return self.items.get(item_id)
    
    def get_all_items(self) -> List[ControlItem]:
        """获取所有控制项"""
        return list(self.items.values())
    
    def get_items_by_category(self) -> Dict[str, List[ControlItem]]:
        """按类别获取控制项"""
        categories = {
            "core": ["consciousness", "reasoning", "emotion"],
            "control": ["mouse", "keyboard", "window"],
            "file": ["file_manager", "search"],
            "ai": ["speech", "tts", "nlu"],
            "system": ["terminal", "browser"]
        }
        
        result = {}
        for cat, ids in categories.items():
            result[cat] = [self.items[i] for i in ids if i in self.items]
        
        return result
    
    def update_item(self, item_id: str, **kwargs):
        """更新控制项"""
        if item_id in self.items:
            for key, value in kwargs.items():
                if hasattr(self.items[item_id], key):
                    setattr(self.items[item_id], key, value)
            
            # 回调
            if "update" in self.callbacks:
                self.callbacks["update"](self.items[item_id])
    
    def set_status(self, item_id: str, status: ModuleStatus):
        """设置状态"""
        self.update_item(item_id, status=status)
    
    def set_enabled(self, item_id: str, enabled: bool):
        """设置启用状态"""
        self.update_item(item_id, enabled=enabled)
    
    # ============ 动作执行 ============
    
    def execute_action(self, action: str) -> bool:
        """执行动作
        
        Args:
            action: 动作名称
        
        Returns:
            bool: 是否成功
        """
        action_map = {
            "toggle_consciousness": self._toggle_consciousness,
            "toggle_reasoning": self._toggle_reasoning,
            "toggle_emotion": self._toggle_emotion,
            "toggle_mouse": self._toggle_mouse,
            "toggle_keyboard": self._toggle_keyboard,
            "toggle_window": self._toggle_window,
            "toggle_file": self._toggle_file,
            "toggle_search": self._toggle_search,
            "toggle_speech": self._toggle_speech,
            "toggle_tts": self._toggle_tts,
            "toggle_nlu": self._toggle_nlu,
            "toggle_terminal": self._toggle_terminal,
            "toggle_browser": self._toggle_browser,
        }
        
        handler = action_map.get(action)
        if handler:
            handler()
            return True
        return False
    
    # 内部切换方法
    def _toggle_consciousness(self):
        item = self.items["consciousness"]
        new_status = ModuleStatus.INACTIVE if item.status == ModuleStatus.ACTIVE else ModuleStatus.ACTIVE
        self.set_status("consciousness", new_status)
    
    def _toggle_reasoning(self):
        item = self.items["reasoning"]
        new_status = ModuleStatus.INACTIVE if item.status == ModuleStatus.ACTIVE else ModuleStatus.ACTIVE
        self.set_status("reasoning", new_status)
    
    def _toggle_emotion(self):
        item = self.items["emotion"]
        new_status = ModuleStatus.INACTIVE if item.status == ModuleStatus.ACTIVE else ModuleStatus.ACTIVE
        self.set_status("emotion", new_status)
    
    def _toggle_mouse(self):
        item = self.items["mouse"]
        new_status = ModuleStatus.INACTIVE if item.status == ModuleStatus.ACTIVE else ModuleStatus.ACTIVE
        self.set_status("mouse", new_status)
    
    def _toggle_keyboard(self):
        item = self.items["keyboard"]
        new_status = ModuleStatus.INACTIVE if item.status == ModuleStatus.ACTIVE else ModuleStatus.ACTIVE
        self.set_status("keyboard", new_status)
    
    def _toggle_window(self):
        item = self.items["window"]
        new_status = ModuleStatus.INACTIVE if item.status == ModuleStatus.ACTIVE else ModuleStatus.ACTIVE
        self.set_status("window", new_status)
    
    def _toggle_file(self):
        item = self.items["file_manager"]
        new_status = ModuleStatus.INACTIVE if item.status == ModuleStatus.ACTIVE else ModuleStatus.ACTIVE
        self.set_status("file_manager", new_status)
    
    def _toggle_search(self):
        item = self.items["search"]
        new_status = ModuleStatus.INACTIVE if item.status == ModuleStatus.ACTIVE else ModuleStatus.ACTIVE
        self.set_status("search", new_status)
    
    def _toggle_speech(self):
        item = self.items["speech"]
        new_status = ModuleStatus.INACTIVE if item.status == ModuleStatus.ACTIVE else ModuleStatus.ACTIVE
        self.set_status("speech", new_status)
    
    def _toggle_tts(self):
        item = self.items["tts"]
        new_status = ModuleStatus.INACTIVE if item.status == ModuleStatus.ACTIVE else ModuleStatus.ACTIVE
        self.set_status("tts", new_status)
    
    def _toggle_nlu(self):
        item = self.items["nlu"]
        new_status = ModuleStatus.INACTIVE if item.status == ModuleStatus.ACTIVE else ModuleStatus.ACTIVE
        self.set_status("nlu", new_status)
    
    def _toggle_terminal(self):
        item = self.items["terminal"]
        new_status = ModuleStatus.INACTIVE if item.status == ModuleStatus.ACTIVE else ModuleStatus.ACTIVE
        self.set_status("terminal", new_status)
    
    def _toggle_browser(self):
        item = self.items["browser"]
        new_status = ModuleStatus.INACTIVE if item.status == ModuleStatus.ACTIVE else ModuleStatus.ACTIVE
        self.set_status("browser", new_status)
    
    # ============ 系统状态 ============
    
    def get_system_status(self) -> SystemStatus:
        """获取系统状态"""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        
        uptime = datetime.now().timestamp() - self.start_time
        
        active_count = sum(
            1 for item in self.items.values() 
            if item.status == ModuleStatus.ACTIVE
        )
        
        return SystemStatus(
            cpu_usage=psutil.cpu_percent(),
            memory_usage=process.memory_percent(),
            disk_usage=psutil.disk_usage('/').percent,
            active_modules=active_count,
            total_modules=len(self.items),
            uptime=uptime,
            last_update=datetime.now().timestamp()
        )
    
    def get_status_summary(self) -> Dict[str, Any]:
        """获取状态摘要"""
        active = sum(1 for i in self.items.values() if i.status == ModuleStatus.ACTIVE)
        inactive = sum(1 for i in self.items.values() if i.status == ModuleStatus.INACTIVE)
        error = sum(1 for i in self.items.values() if i.status == ModuleStatus.ERROR)
        
        return {
            "active": active,
            "inactive": inactive,
            "error": error,
            "total": len(self.items),
            "status": "healthy" if error == 0 else "degraded"
        }
    
    # ============ 设置管理 ============
    
    def load_settings(self, path: str = "settings.json"):
        """加载设置"""
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    self.settings = json.load(f)
                print(f"✅ 设置已加载: {path}")
            except Exception as e:
                print(f"⚠️ 设置加载失败: {e}")
    
    def save_settings(self, path: str = "settings.json"):
        """保存设置"""
        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, ensure_ascii=False, indent=2)
            print(f"✅ 设置已保存: {path}")
        except Exception as e:
            print(f"⚠️ 设置保存失败: {e}")
    
    def get_setting(self, key: str, default: Any = None) -> Any:
        """获取设置"""
        return self.settings.get(key, default)
    
    def set_setting(self, key: str, value: Any):
        """设置"""
        self.settings[key] = value
    
    def reset_settings(self):
        """重置设置"""
        self.settings = {}
        print("✅ 设置已重置")
    
    # ============ 回调 ============
    
    def on_update(self, callback: Callable[[ControlItem], None]):
        """更新回调"""
        self.callbacks["update"] = callback
    
    def on_action(self, callback: Callable[[str], None]):
        """动作回调"""
        self.callbacks["action"] = callback
    
    # ============ 导出 ============
    
    def export_config(self) -> Dict:
        """导出配置"""
        return {
            "items": [
                {
                    "id": item.id,
                    "status": item.status.value,
                    "enabled": item.enabled
                }
                for item in self.items.values()
            ],
            "settings": self.settings
        }
    
    def import_config(self, config: Dict):
        """导入配置"""
        for item_config in config.get("items", []):
            item_id = item_config.get("id")
            if item_id in self.items:
                if "status" in item_config:
                    self.set_status(item_id, ModuleStatus(item_config["status"]))
                if "enabled" in item_config:
                    self.set_enabled(item_id, item_config["enabled"])
        
        if "settings" in config:
            self.settings = config["settings"]
    
    # ============ UI渲染 ============
    
    def render_control_panel(self) -> str:
        """渲染控制面板HTML"""
        categories = self.get_items_by_category()
        category_names = {
            "core": "🧠 核心模块",
            "control": "🎮 控制模块",
            "file": "📁 文件模块",
            "ai": "🤖 AI模块",
            "system": "⚙️ 系统工具"
        }
        
        html_parts = []
        
        for cat, items in categories.items():
            html_parts.append(f'<div class="control-category">')
            html_parts.append(f'<h3>{category_names.get(cat, cat)}</h3>')
            html_parts.append('<div class="control-grid">')
            
            for item in items:
                status_class = item.status.value
                enabled_attr = "" if item.enabled else "disabled"
                status_icon = "✅" if item.status == ModuleStatus.ACTIVE else "⏸️"
                
                html_parts.append(f"""
<div class="control-item {status_class}" data-id="{item.id}" {enabled_attr}>
    <div class="item-icon">{item.icon}</div>
    <div class="item-name">{item.name}</div>
    <div class="item-status">{status_icon}</div>
</div>
                """)
            
            html_parts.append('</div></div>')
        
        return '\n'.join(html_parts)


# 测试代码
if __name__ == "__main__":
    print("🎛️ Control Panel 测试")
    
    panel = ControlPanel()
    
    # 获取所有项
    items = panel.get_all_items()
    print(f"\n📋 控制项数量: {len(items)}")
    
    # 按类别获取
    by_cat = panel.get_items_by_category()
    for cat, items in by_cat.items():
        active = sum(1 for i in items if i.status == ModuleStatus.ACTIVE)
        print(f"  {cat}: {active}/{len(items)} 激活")
    
    # 执行动作
    print("\n🔧 测试切换动作:")
    panel.execute_action("toggle_mouse")
    mouse = panel.get_item("mouse")
    print(f"  鼠标控制: {mouse.status.value}")
    
    # 状态摘要
    summary = panel.get_status_summary()
    print(f"\n📊 状态摘要: {summary}")
    
    print("\n✅ 测试完成")
