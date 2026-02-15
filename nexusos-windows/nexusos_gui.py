#!/usr/bin/env python3
"""
NexusOS Windows 完整版 - 整合所有功能
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import sys, os, time, json, webbrowser, subprocess, re
from datetime import datetime
import random

# ==================== 配置 ====================

DEFAULT_LLM = {
    "provider": "minimax-portal",
    "model": "MiniMax-M2.1", 
    "api_key": "",
    "api_base": "https://api.minimax.chat/v1"
}

# ==================== 日志 ====================

class Log:
    def __init__(self, log_file=None):
        self.log_file = log_file or os.path.expanduser("~/.nexusos/logs/nexusos.log")
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
    
    def write(self, msg, level="INFO"):
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{ts}] [{level}] {msg}\n"
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(entry)
        except: pass
        return entry

logger = Log()

# ==================== 语音 ====================

class Voice:
    def __init__(self):
        self.enabled = False
        self.type = "xiaozhua"
        self.types = {"xiaozhua":1.0, "professional":0.9, "friendly":1.1, "energetic":1.2}
        try:
            import pyttsx3
            self.engine = pyttsx3.init()
            self.ok = True
        except: self.ok = False
    
    def speak(self, text):
        if not self.enabled or not self.ok: return
        try:
            self.engine.setProperty('rate', int(150*self.types[self.type]))
            self.engine.say(text)
            self.engine.runAndWait()
        except: pass

# ==================== 电脑控制 ====================

class Computer:
    def __init__(self):
        self.platform = sys.platform
    
    def open_app(self, name):
        try:
            if self.platform=="win32": subprocess.Popen(f"start {name}", shell=True)
            else: subprocess.Popen(name, shell=True)
            return True, f"已打开 {name}"
        except Exception as e: return False, str(e)
    
    def open_url(self, url):
        try:
            webbrowser.open(url)
            return True, f"已打开 {url}"
        except Exception as e: return False, str(e)
    
    def search(self, q):
        return self.open_url(f"https://www.baidu.com/s?wd={q}")
    
    def run_cmd(self, cmd):
        try:
            r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
            return True, r.stdout[:1000] or r.stderr[:500]
        except Exception as e: return False, str(e)
    
    def file_op(self, op, path):
        try:
            if op=="open":
                if os.path.isfile(path):
                    if self.platform=="win32": os.startfile(path)
                    else: subprocess.Popen(path, shell=True)
                return True, f"已打开 {path}"
            elif op=="list":
                if os.path.isdir(path):
                    return True, "\n".join(os.listdir(path)[:20])
                return False, "无效目录"
            return False, "未知操作"
        except Exception as e: return False, str(e)

# ==================== UI自动化 ====================

class UIAuto:
    def __init__(self):
        self.ok = False
        try:
            import pyautogui
            self.py = pyautogui
            self.py.FAILSAFE = True
            self.ok = True
        except: pass
    
    def click(self, x, y):
        if not self.ok: return False, "未安装pyautogui"
        try:
            self.py.click(x, y)
            return True, f"点击 ({x},{y})"
        except Exception as e: return False, str(e)
    
    def type(self, text):
        if not self.ok: return False, "未安装pyautogui"
        try:
            self.py.write(text)
            return True, f"输入: {text}"
        except Exception as e: return False, str(e)
    
    def press(self, *keys):
        if not self.ok: return False, "未安装pyautogui"
        try:
            self.py.press(*keys)
            return True, f"按键: {keys}"
        except Exception as e: return False, str(e)
    
    def screenshot(self, name=None):
        if not self.ok: return False, "未安装pyautogui"
        try:
            from PIL import ImageGrab
            img = ImageGrab.grab()
            n = name or datetime.now().strftime("%Y%m%d_%H%M%S")
            img.save(f"/tmp/nexusos_{n}.png")
            return True, f"/tmp/nexusos_{n}.png"
        except Exception as e: return False, str(e)

# ==================== AI理解 ====================

class AI:
    def __init__(self):
        self.cfg = DEFAULT_LLM.copy()
        self.load_cfg()
        self.patterns = {
            "open_app": ["打开", "启动", "运行"],
            "search": ["搜索", "找"],
            "url": ["http", "://", "网页"],
            "file": ["文件", "目录", "打开"],
            "cmd": ["命令", "执行"],
            "click": ["点击", "按"],
            "type": ["输入", "打字"],
            "screenshot": ["截图", "截屏"]
        }
    
    def load_cfg(self):
        p = os.path.expanduser("~/.nexusos/config/llm.json")
        if os.path.exists(p):
            try:
                with open(p) as f: self.cfg = json.load(f)
            except: pass
    
    def understand(self, msg):
        msg = msg.lower()
        
        # 提取实体
        urls = re.findall(r'https?://[^\s]+', msg)
        paths = re.findall(r'[A-Za-z]:\\[^\s]+|/[^\s]+', msg)
        
        # 识别意图
        for intent, pats in self.patterns.items():
            for p in pats:
                if p in msg:
                    return {"intent": intent, "urls": urls, "paths": paths}
        
        return {"intent": "chat", "msg": msg}

# ==================== 主GUI ====================

class NexusOS(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("NexusOS AI v2.9")
        self.geometry("1000x700")
        self.configure(bg="#0a0a1a")
        
        # 初始化模块
        self.voice = Voice()
        self.computer = Computer()
        self.uiauto = UIAuto()
        self.ai = AI()
        self.running = False
        
        # 加载配置
        self.load_config()
        
        # 构建界面
        self.build_ui()
        
        # 启动
        self.welcome()
        logger.write("NexusOS启动")
    
    def load_config(self):
        p = os.path.expanduser("~/.nexusos/config/llm.json")
        if not os.path.exists(p):
            os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, 'w') as f:
                json.dump(DEFAULT_LLM, f)
    
    def build_ui(self):
        # 标题
        title = tk.Frame(self, bg="#0a0a1a", height=50)
        title.pack(fill=tk.X)
        tk.Label(title, text="NexusOS AI", font=("Consolas",20,"bold"), 
                bg="#0a0a1a", fg="#00ffff").pack(side=tk.LEFT, padx=20)
        
        self.status = tk.Label(title, text="●", font=("Arial",14), bg="#0a0a1a", fg="#ff0000")
        self.status.pack(side=tk.RIGHT, padx=20)
        
        # 动画背景
        self.canvas = tk.Canvas(self, height=60, bg="#0a0a1a", highlightthickness=0)
        self.canvas.pack(fill=tk.X)
        self.animate_bg()
        
        # 主内容
        main = tk.Frame(self, bg="#0a0a1a")
        main.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 左侧 - 控制
        left = tk.Frame(main, bg="#0a0a1a", width=180)
        left.pack(side=tk.LEFT, fill=tk.Y)
        left.pack_propagate(False)
        
        tk.Label(left, text="控制面板", font=("Microsoft YaHei",11,"bold"), bg="#0a0a1a", fg="#00ffff").pack(pady=10)
        
        btns = [
            ("启动", self.start), ("停止", self.stop), ("状态", self.show_status),
            ("浏览器", self.open_browser), ("文件", self.open_file),
            ("命令", self.run_command), ("搜索", self.web_search),
            ("截图", self.do_screenshot), ("点击", self.do_click),
            ("输入", self.do_type), ("设置", self.open_settings),
            ("清除", self.clear)
        ]
        
        for t, c in btns:
            tk.Button(left, text=t, command=c, bg="#1a1a2a", fg="#00ffff",
                     relief=tk.FLAT, padx=10, pady=6).pack(fill=tk.X, padx=5, pady=2)
        
        # 情感
        tk.Label(left, text="情感", bg="#0a0a1a", fg="#00ffff").pack(pady=(15,5))
        for e, emo in [("😊","happy"),("😢","sad"),("🤔","thinking"),("😐","neutral")]:
            tk.Button(left, text=e, command=lambda x=emo:self.set_emo(x), 
                     bg="#1a1a2a", fg="#00ffff", width=4).pack(side=tk.LEFT, padx=2)
        
        # 语音
        tk.Label(left, text="语音", bg="#0a0a1a", fg="#00ffff").pack(pady=(10,5))
        self.voice_btn = tk.Button(left, text="关闭", command=self.toggle_voice,
                                 bg="#1a1a2a", fg="#888", width=10)
        self.voice_btn.pack()
        
        # 中间 - 对话
        mid = tk.Frame(main, bg="#0a0a1a")
        mid.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        
        tk.Label(mid, text="对话", font=("Microsoft YaHei",11,"bold"), bg="#0a0a1a", fg="#00ffff").pack(pady=5)
        
        self.chat = scrolledtext.ScrolledText(mid, font=("Microsoft YaHei",10), bg="#1a1a2a",
                                            fg="#fff", insertbackground="#00ffff")
        self.chat.pack(fill=tk.BOTH, expand=True)
        
        # 输入
        inp = tk.Frame(mid, bg="#0a0a1a")
        inp.pack(fill=tk.X, pady=10)
        
        self.input = tk.Entry(inp, font=("Microsoft YaHei",11), bg="#1a1a2a", fg="#fff",
                           insertbackground="#00ffff")
        self.input.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.input.bind("<Return>", self.send)
        
        tk.Button(inp, text="发送", command=self.send, bg="#00ffff", fg="#0a0a1a",
                 width=8).pack(side=tk.LEFT, padx=(10,0))
        
        # 右侧 - 能力
        right = tk.Frame(main, bg="#0a0a1a", width=180)
        right.pack(side=tk.LEFT, fill=tk.Y)
        right.pack_propagate(False)
        
        tk.Label(right, text="AI能力", font=("Microsoft YaHei",11,"bold"), bg="#0a0a1a", fg="#00ffff").pack(pady=10)
        
        caps = ["🧠 意图理解", "💻 电脑控制", "🎯 UI自动化", "🗣️ 语音合成", 
                "📝 日志系统", "⚙️ LLM配置", "🌐 网络操作", "📁 文件管理"]
        
        for c in caps:
            tk.Label(right, text=c, font=("Microsoft YaHei",9), bg="#0a0a1a", fg="#888").pack(anchor=tk.W, padx=20)
        
        # 底部
        tk.Label(self, text="NexusOS v2.9 | 完整版 | 懂你所说，做你所想",
               font=("Microsoft YaHei",8), bg="#0a0a1a", fg="#666").pack(side=tk.BOTTOM, pady=3)
    
    def animate_bg(self):
        self.canvas.delete("all")
        w, h = self.canvas.winfo_width() or 800, 60
        t = time.time()
        
        # 网格
        for i in range(0, w, 25): self.canvas.create_line(i,0,i,h,fill="#1a1a3a")
        for i in range(0, h, 25): self.canvas.create_line(0,i,w,i,fill="#1a1a3a")
        
        # 流动
        for i in range(3):
            y = (t*20 + i*50) % h
            self.canvas.create_line(0,y,w,y,fill="#00ffff",width=2,stipple="gray50")
        
        self.after(50, self.animate_bg)
    
    def log(self, msg, user=False):
        ts = datetime.now().strftime("%H:%M:%S")
        prefix = "👤" if user else "Nexus"
        color = "#ffaa00" if user else "#00ffff"
        self.chat.insert(tk.END, f"[{ts}] {prefix} {msg}\n")
        self.chat.see(tk.END)
        logger.write(f"{prefix} {msg}")
    
    def set_emo(self, e): self.log(f"情感: {e}")
    
    def toggle_voice(self):
        self.voice.enabled = not self.voice.enabled
        self.voice_btn.config(text="开启" if self.voice.enabled else "关闭",
                          bg="#00ff88" if self.voice.enabled else "#1a1a2a")
    
    def start(self):
        self.running = True
        self.status.config(fg="#00ff00")
        self.log("服务已启动")
        self.voice.speak("服务已启动")
    
    def stop(self):
        self.running = False
        self.status.config(fg="#ff0000")
        self.log("服务已停止")
    
    def show_status(self):
        self.log("状态:")
        self.log(f"  运行: {'是' if self.running else '否'}")
        self.log(f"  语音: {'开' if self.voice.enabled else '关'}")
        self.log(f"  UI自动化: {'可用' if self.uiauto.ok else '不可用'}")
        self.log(f"  日志: {logger.log_file}")
    
    def open_browser(self): self.computer.open_url("https://www.baidu.com")
    def web_search(self):
        q = self.input.get().strip()
        if q: self.computer.search(q); self.log(f"已搜索: {q}")
    
    def open_file(self):
        p = filedialog.askopenfilename()
        if p: self.computer.file_op("open", p)
    
    def run_command(self):
        cmd = self.input.get().strip()
        if cmd:
            ok, r = self.computer.run_cmd(cmd)
            self.log(r[:500])
    
    def do_screenshot(self):
        ok, r = self.uiauto.screenshot()
        self.log(f"截图: {r}" if ok else f"截图失败: {r}")
    
    def do_click(self):
        self.log("点击功能：输入坐标 x y")
    
    def do_type(self):
        self.log("输入功能：输入要发送的文字")
    
    def open_settings(self):
        p = os.path.expanduser("~/.nexusos/config/llm.json")
        os.makedirs(os.path.dirname(p), exist_ok=True)
        self.log(f"配置文件: {p}")
        self.log("请编辑该文件配置API")
    
    def clear(self):
        self.chat.delete(1.0, tk.END)
    
    def welcome(self):
        self.log("NexusOS AI 启动成功!")
        self.log("我可以帮你:")
        self.log("  🖥️ 打开应用/文件/网页")
        self.log("  🔍 搜索信息")
        self.log("  💻 执行命令")
        self.log("  🎯 UI自动化")
        self.log("直接告诉我你想做什么!")
    
    def send(self, e=None):
        msg = self.input.get().strip()
        if not msg: return
        self.input.delete(0, tk.END)
        self.log(msg, True)
        
        # AI理解
        result = self.ai.understand(msg)
        intent = result.get("intent", "chat")
        
        # 执行
        if intent == "open_app":
            ok, r = self.computer.open_app(msg.replace("打开","").strip())
            self.log(r)
        elif intent == "search":
            q = msg.replace("搜索","").strip()
            self.computer.search(q)
            self.log(f"已搜索: {q}")
        elif intent == "url" and result.get("urls"):
            self.computer.open_url(result["urls"][0])
            self.log("已打开网页")
        elif intent == "file" and result.get("paths"):
            ok, r = self.computer.file_op("open", result["paths"][0])
            self.log(r)
        elif intent == "cmd":
            ok, r = self.computer.run_cmd(msg.replace("执行","").replace("命令","").strip())
            self.log(r[:300])
        elif intent == "screenshot":
            self.do_screenshot()
        elif intent == "click":
            self.log("点击功能需要坐标")
        elif intent == "type":
            self.log("输入功能需要文字")
        else:
            self.log(f"我理解你想: {intent}")
            self.log("你可以: 打开应用/搜索/执行命令/截图等")

if __name__ == "__main__":
    app = NexusOS()
    app.mainloop()
