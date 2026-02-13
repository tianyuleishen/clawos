#!/usr/bin/env python3
"""
🦞 ClawOS GUI - Simple Interactive Interface
"""

import sys
import os

# Add project to path
sys.path.insert(0, '/home/admin/.openclaw/workspace')

from clawos.main import ClawOS
from comprehensive_test import run_test


class ClawOSGUI:
    def __init__(self):
        print("🦞 ClawOS GUI - Initializing...")
        self.system = ClawOS()
        print("✅ ClawOS Ready!")
        
        self.commands = {
            "help": self.show_help,
            "test": self.run_test,
            "reason": self.reason,
            "prove": self.prove,
            "analyze": self.analyze,
            "clear": self.clear_screen,
            "quit": self.quit,
            "exit": self.quit,
        }
    
    def show_help(self):
        print("""
🦞 ClawOS Commands:

  help          - Show this help message
  test          - Run benchmark tests
  reason [问题]  - Logical reasoning
  prove [问题]   - Mathematical proofs
  analyze [问题] - Analyze arguments
  clear         - Clear screen
  quit/exit     - Exit ClawOS

💡 Example:
  > reason 如果A>B，B>C，那么A>C吗？
  > prove 证明勾股定理
  > analyze 分析这个论证的逻辑谬误
        """)
    
    def run_test(self):
        print("\n🦞 Running benchmark tests...")
        run_test()
    
    def reason(self, query):
        if not query:
            print("❌ Please provide a question")
            return
        print(f"\n🔍 Reasoning: {query}")
        result = self.system.reason(query)
        print(f"\n📝 Answer: {result.answer}")
        print(f"🎯 Confidence: {result.confidence}")
    
    def prove(self, query):
        if not query:
            print("❌ Please provide a proof request")
            return
        print(f"\n🔬 Proving: {query}")
        result = self.system.prove(query)
        print(f"\n📝 Proof: {result.answer}")
        print(f"🎯 Confidence: {result.confidence}")
    
    def analyze(self, query):
        if not query:
            print("❌ Please provide an argument to analyze")
            return
        print(f"\n🔎 Analyzing: {query}")
        result = self.system.analyze(query)
        print(f"\n📝 Analysis: {result.answer}")
        print(f"🎯 Confidence: {result.confidence}")
    
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def quit(self):
        print("\n👋 Goodbye!")
        sys.exit(0)
    
    def parse_input(self, text):
        parts = text.strip().split(None, 1)
        cmd = parts[0].lower() if parts else ""
        args = parts[1] if len(parts) > 1 else ""
        
        if cmd in self.commands:
            self.commands[cmd](args)
        else:
            print(f"❌ Unknown command: {cmd}")
            print("💡 Type 'help' for available commands")
    
    def run(self):
        self.clear_screen()
        print("""
╔════════════════════════════════════════╗
║                                        ║
║   🦞 ClawOS - World-Class AI          ║
║                                        ║
║   Type 'help' for available commands   ║
║   Type 'quit' to exit                 ║
║                                        ║
╚════════════════════════════════════════╝
        """)
        
        while True:
            try:
                user_input = input("\n🦞 > ").strip()
                if user_input:
                    self.parse_input(user_input)
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")


def main():
    gui = ClawOSGUI()
    gui.run()


if __name__ == "__main__":
    main()
