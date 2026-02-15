#!/usr/bin/env python3
"""
🦞 NexusOS Windows GUI Version
带UI界面的Windows桌面应用
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import subprocess
import sys
import os

VERSION = "1.0.0"
NAME = "NexusOS Windows GUI"

class NexusOSGUI:
    """NexusOS图形界面"""
    
    def __init__(self, root):
        self.root = root
        self.root.title(f"🦞 {NAME} v{VERSION}")
        self.root.geometry("800x600")
        
        # 状态
        self.running = False
        
        self.setup_ui()
        self.check_status()
    
    def setup_ui(self):
        """设置UI"""
        # 标题栏
        title_frame = tk.Frame(self.root, bg="#1a1a2e", height=60)
        title_frame.pack(fill=tk.X)
        
        title_label = tk.Label(
            title_frame, 
            text="🦞 NexusOS Windows GUI",
            font=("Microsoft YaHei", 18, "bold"),
            bg="#1a1a2e",
            fg="white"
        )
        title_label.pack(pady=15)
        
        # 控制栏
        control_frame = tk.Frame(self.root)
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        btn_start = tk.Button(
            control_frame, 
            text="🚀 启动", 
            command=self.start_service,
            bg="#4CAF50",
            fg="white",
            width=10
        )
        btn_start.pack(side=tk.LEFT, padx=5)
        
        btn_stop = tk.Button(
            control_frame, 
            text="🛑 停止", 
            command=self.stop_service,
            bg="#f44336",
            fg="white",
            width=10
        )
        btn_stop.pack(side=tk.LEFT, padx=5)
        
        btn_status = tk.Button(
            control_frame, 
            text="📊 状态", 
            command=self.check_status,
            width=10
        )
        btn_status.pack(side=tk.LEFT, padx=5)
        
        btn_clear = tk.Button(
            control_frame, 
            text="🗑️ 清除", 
            command=self.clear_log,
            width=10
        )
        btn_clear.pack(side=tk.LEFT, padx=5)
        
        # 状态标签
        self.status_label = tk.Label(
            control_frame, 
            text="❌ 未运行",
            font=("Microsoft YaHei", 10),
            fg="red"
        )
        self.status_label.pack(side=tk.RIGHT, padx=10)
        
        # 输入区
        input_frame = tk.Frame(self.root)
        input_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(input_frame, text="💬 输入问题:").pack(anchor=tk.W)
        
        self.input_entry = tk.Entry(input_frame, font=("Microsoft YaHei", 12))
        self.input_entry.pack(fill=tk.X, pady=5)
        self.input_entry.bind("<Return>", self.send_message)
        
        btn_send = tk.Button(
            input_frame, 
            text="发送", 
            command=self.send_message,
            bg="#2196F3",
            fg="white",
            width=10
        )
        btn_send.pack()
        
        # 聊天区
        chat_frame = tk.Frame(self.root)
        chat_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        tk.Label(chat_frame, text="📝 对话历史:").pack(anchor=tk.W)
        
        self.chat_area = scrolledtext.ScrolledText(
            chat_frame, 
            font=("Microsoft YaHei", 11),
            wrap=tk.WORD
        )
        self.chat_area.pack(fill=tk.BOTH, expand=True)
        
        # 底部信息
        info_label = tk.Label(
            self.root, 
            text=f"{NAME} v{VERSION} | 简单 • 方便 • 快速",
            font=("Microsoft YaHei", 9),
            bg="#f0f0f0"
        )
        info_label.pack(side=tk.BOTTOM, fill=tk.X)
    
    def log(self, message):
        """添加日志"""
        self.chat_area.insert(tk.END, f"{message}\n")
        self.chat_area.see(tk.END)
    
    def clear_log(self):
        """清除日志"""
        self.chat_area.delete(1.0, tk.END)
    
    def start_service(self):
        """启动服务"""
        self.log("🚀 启动NexusOS服务...")
        # 这里调用启动命令
        self.running = True
        self.status_label.config(text="✅ 运行中", fg="green")
        self.log("✅ 服务已启动")
    
    def stop_service(self):
        """停止服务"""
        self.log("🛑 停止NexusOS服务...")
        self.running = False
        self.status_label.config(text="❌ 已停止", fg="red")
        self.log("✅ 服务已停止")
    
    def check_status(self):
        """检查状态"""
        try:
            result = subprocess.run(
                ["ps", "aux"], 
                capture_output=True, 
                text=True
            )
            if "nexusos" in result.stdout:
                self.running = True
                self.status_label.config(text="✅ 运行中", fg="green")
            else:
                self.running = False
                self.status_label.config(text="❌ 未运行", fg="red")
        except:
            self.running = False
            self.status_label.config(text="❌ 未运行", fg="red")
    
    def send_message(self, event=None):
        """发送消息"""
        message = self.input_entry.get().strip()
        if not message:
            return
        
        self.log(f"❓ 你: {message}")
        self.input_entry.delete(0, tk.END)
        
        # 模拟回复
        self.log("🤔 NexusOS: 思考中...")
        self.root.after(500, lambda: self.log("💡 NexusOS: 请先启动服务"))


def main():
    """主函数"""
    root = tk.Tk()
    app = NexusOSGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
