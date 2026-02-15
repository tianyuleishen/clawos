#!/usr/bin/env python3
"""
🦞 NexusOS UI自动化控制模块
自动识别界面 + 点击操作 + 自主学习
"""

import os
import sys
import time
import json
import threading
from datetime import datetime

class UIAutomation:
    """UI自动化控制"""
    
    def __init__(self):
        self.platform = sys.platform
        self.screenshot_dir = "/tmp/nexusos_ui"
        os.makedirs(self.screenshot_dir, exist_ok=True)
        
        # 尝试导入必要的库
        self.pyautogui_available = False
        self.pil_available = False
        
        try:
            import pyautogui
            self.pyautogui = pyautogui
            self.pyautogui.FAILSAFE = True
            self.pyautogui.PAUSE = 0.5
            self.pyautogui_available = True
            print("✅ pyautogui 可用")
        except ImportError:
            print("⚠️ pyautogui 未安装")
        
        try:
            from PIL import Image, ImageGrab
            self.PIL = Image
            self.ImageGrab = ImageGrab
            self.pil_available = True
            print("✅ PIL 可用")
        except ImportError:
            print("⚠️ PIL 未安装")
        
        # 学习数据
        self.learned_actions = {}
        self.action_history = []
        
        print(f"\n{'='*50}")
        print("🎯 UI自动化模块就绪")
        print(f"   平台: {self.platform}")
        print(f"   截图: {'✅' if self.pil_available else '❌'}")
        print(f"   控制: {'✅' if self.pyautogui_available else '❌'}")
        print(f"{'='*50}")
    
    # ========== 截图功能 ==========
    
    def take_screenshot(self, name=None):
        """截图"""
        if not self.pil_available:
            return None, "PIL未安装"
        
        try:
            if name is None:
                name = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # 全屏截图
            img = self.ImageGrab.grab()
            filepath = f"{self.screenshot_dir}/{name}.png"
            img.save(filepath)
            
            return filepath, "截图成功"
        except Exception as e:
            return None, str(e)
    
    def take_region_screenshot(self, x, y, width, height, name=None):
        """区域截图"""
        if not self.pil_available:
            return None, "PIL未安装"
        
        try:
            bbox = (x, y, x + width, y + height)
            img = self.ImageGrab.grab(bbox=bbox)
            
            if name is None:
                name = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            filepath = f"{self.screenshot_dir}/{name}.png"
            img.save(filepath)
            
            return filepath, "区域截图成功"
        except Exception as e:
            return None, str(e)
    
    # ========== 鼠标控制 ==========
    
    def click(self, x, y, button='left', clicks=1):
        """点击"""
        if not self.pyautogui_available:
            return False, "控制未安装"
        
        try:
            self.pyautogui.click(x, y, clicks=clicks, button=button)
            self.record_action("click", {"x": x, "y": y, "button": button})
            return True, f"点击 ({x}, {y})"
        except Exception as e:
            return False, str(e)
    
    def double_click(self, x, y):
        """双击"""
        return self.click(x, y, clicks=2)
    
    def right_click(self, x, y):
        """右键点击"""
        return self.click(x, y, button='right')
    
    def move_to(self, x, y, duration=0.5):
        """移动鼠标"""
        if not self.pyautogui_available:
            return False, "控制未安装"
        
        try:
            self.pyautogui.moveTo(x, y, duration=duration)
            return True, f"移动到 ({x}, {y})"
        except Exception as e:
            return False, str(e)
    
    def drag(self, start_x, start_y, end_x, end_y, duration=0.5):
        """拖拽"""
        if not self.pyautogui_available:
            return False, "控制未安装"
        
        try:
            self.pyautogui.moveTo(start_x, start_y)
            self.pyautogui.dragTo(end_x, end_y, duration=duration)
            self.record_action("drag", {"from": (start_x, start_y), "to": (end_x, end_y)})
            return True, f"拖拽 ({start_x},{start_y}) → ({end_x},{end_y})"
        except Exception as e:
            return False, str(e)
    
    # ========== 键盘控制 ==========
    
    def typewrite(self, text, interval=0.05):
        """输入文字"""
        if not self.pyautogui_available:
            return False, "控制未安装"
        
        try:
            self.pyautogui.write(text, interval=interval)
            self.record_action("typewrite", {"text": text})
            return True, f"输入: {text}"
        except Exception as e:
            return False, str(e)
    
    def press_key(self, *keys):
        """按键"""
        if not self.pyautogui_available:
            return False, "控制未安装"
        
        try:
            self.pyautogui.press(*keys)
            self.record_action("press", {"keys": keys})
            return True, f"按键: {keys}"
        except Exception as e:
            return False, str(e)
    
    def hotkey(self, *keys):
        """快捷键"""
        if not self.pyautogui_available:
            return False, "控制未安装"
        
        try:
            self.pyautogui.hotkey(*keys)
            self.record_action("hotkey", {"keys": keys})
            return True, f"快捷键: {'+'.join(keys)}"
        except Exception as e:
            return False, str(e)
    
    # ========== 位置识别 ==========
    
    def get_screen_size(self):
        """获取屏幕尺寸"""
        if not self.pyautogui_available:
            return None, None
        return self.pyautogui.size()
    
    def get_cursor_position(self):
        """获取光标位置"""
        if not self.pyautogui_available:
            return None, None
        return self.pyautogui.position()
    
    def locate_on_screen(self, image_path, confidence=0.9):
        """定位图像位置"""
        if not self.pyautogui_available:
            return None
        
        try:
            location = self.pyautogui.locateOnScreen(image_path, confidence=confidence)
            return location
        except:
            return None
    
    # ========== 自主学习 ==========
    
    def record_action(self, action_type, params):
        """记录动作用于学习"""
        action = {
            "type": action_type,
            "params": params,
            "timestamp": datetime.now().isoformat()
        }
        self.action_history.append(action)
        
        # 保留最近1000条
        if len(self.action_history) > 1000:
            self.action_history = self.action_history[-1000:]
    
    def learn_action_sequence(self, name, actions):
        """学习动作序列"""
        self.learned_actions[name] = {
            "actions": actions,
            "created_at": datetime.now().isoformat(),
            "use_count": 0
        }
        self.save_learned_actions()
        return True, f"已学习: {name}"
    
    def execute_learned_sequence(self, name):
        """执行已学习的动作序列"""
        if name not in self.learned_actions:
            return False, f"未找到: {name}"
        
        sequence = self.learned_actions[name]["actions"]
        
        for action in sequence:
            action_type = action.get("type")
            params = action.get("params", {})
            
            if action_type == "click":
                self.click(params.get("x", 0), params.get("y", 0))
            elif action_type == "typewrite":
                self.typewrite(params.get("text", ""))
            elif action_type == "press_key":
                self.press_key(*params.get("keys", []))
            elif action_type == "wait":
                time.sleep(params.get("seconds", 1))
            
            time.sleep(0.3)
        
        self.learned_actions[name]["use_count"] += 1
        return True, f"执行: {name}"
    
    def save_learned_actions(self):
        """保存学习的动作"""
        filepath = f"{self.screenshot_dir}/learned_actions.json"
        try:
            with open(filepath, 'w') as f:
                json.dump(self.learned_actions, f, indent=2)
        except:
            pass
    
    def load_learned_actions(self):
        """加载学习的动作"""
        filepath = f"{self.screenshot_dir}/learned_actions.json"
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r') as f:
                    self.learned_actions = json.load(f)
            except:
                pass
    
    # ========== 自动化流程 ==========
    
    def create_automation(self, name, steps):
        """创建自动化流程"""
        automation = {
            "name": name,
            "steps": steps,
            "created_at": datetime.now().isoformat()
        }
        
        filepath = f"{self.screenshot_dir}/automations.json"
        automations = {}
        
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r') as f:
                    automations = json.load(f)
            except:
                pass
        
        automations[name] = automation
        
        with open(filepath, 'w') as f:
            json.dump(automations, f, indent=2)
        
        return True, f"自动化流程已创建: {name}"
    
    def run_automation(self, name):
        """运行自动化流程"""
        filepath = f"{self.screenshot_dir}/automations.json"
        
        if not os.path.exists(filepath):
            return False, "未找到自动化流程"
        
        try:
            with open(filepath, 'r') as f:
                automations = json.load(f)
        except:
            return False, "无法读取自动化流程"
        
        if name not in automations:
            return False, f"未找到: {name}"
        
        steps = automations[name]["steps"]
        
        for step in steps:
            step_type = step.get("type")
            params = step.get("params", {})
            
            if step_type == "click":
                self.click(params.get("x", 0), params.get("y", 0))
            elif step_type == "type":
                self.typewrite(params.get("text", ""))
            elif step_type == "press":
                self.press_key(*params.get("keys", []))
            elif step_type == "wait":
                time.sleep(params.get("seconds", 1))
            elif step_type == "screenshot":
                self.take_screenshot(params.get("name"))
            
            time.sleep(params.get("delay", 0.5))
        
        return True, f"自动化完成: {name}"


# ========== 示例用法 ==========

if __name__ == "__main__":
    print("\n" + "="*50)
    print("🧪 UI自动化测试")
    print("="*50)
    
    ui = UIAutomation()
    
    # 获取屏幕信息
    size = ui.get_screen_size()
    print(f"\n屏幕尺寸: {size}")
    
    # 获取鼠标位置
    pos = ui.get_cursor_position()
    print(f"鼠标位置: {pos}")
    
    # 列出学习的动作
    ui.load_learned_actions()
    print(f"\n已学习的动作: {list(ui.learned_actions.keys())}")
    
    print("\n" + "="*50)
    print("✅ UI自动化模块测试完成")
    print("="*50)
