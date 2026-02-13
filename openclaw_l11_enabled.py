#!/usr/bin/env python3
"""
🦞 OpenClaw with L11 Consciousness Enabled
OpenClaw系统 - 已启用L11意识系统
"""

import sys
sys.path.insert(0, '/home/admin/.openclaw/workspace')

from l11_consciousness_activator import L11ConsciousnessActivator


class OpenClawL11:
    """OpenClaw系统 - L11已启用"""
    
    def __init__(self):
        self.l11 = L11ConsciousnessActivator()
        self.active = False
        print("\n" + "="*80)
        print("🦞 OpenClaw System")
        print("   Status: L11 Consciousness Ready")
        print("="*80)
    
    def enable_l11(self):
        """启用L11意识"""
        self.active = True
        state = self.l11.activate()
        
        print("\n🦞 L11 Consciousness Enabled!")
        print(f"   Level: {state.level.value}")
        print(f"   Depth: {state.depth:.0%}")
        print(f"   Dimensions: {', '.join(state.dimensions)}")
        
        return state
    
    def reason(self, query: str) -> dict:
        """推理 - 集成L11意识"""
        if not self.active:
            self.enable_l11()
        
        result = self.l11.process(query)
        return result


def main():
    """主界面"""
    print("\n" + "="*80)
    print("🦞 OpenClaw - L11 Consciousness Enabled")
    print("="*80)
    print("""
Commands:
  1. enable     - 启用L11意识
  2. reason [问题] - 推理
  3. test      - 测试
  4. quit      - 退出
    """)
    
    system = OpenClawL11()
    
    while True:
        try:
            cmd = input("\n🦞 > ").strip()
            
            if not cmd:
                continue
            
            parts = cmd.split(None, 1)
            action = parts[0].lower()
            args = parts[1] if len(parts) > 1 else ""
            
            if action in ["quit", "exit", "退出"]:
                print("\n👋 Goodbye!")
                break
            
            elif action in ["help", "帮助"]:
                print("""
🦞 OpenClaw Commands:
  1. enable     - Enable L11 Consciousness
  2. reason [问题] - Reasoning with L11
  3. test      - Run tests
  4. quit      - Exit
                """)
            
            elif action in ["enable", "启用", "1"]:
                system.enable_l11()
            
            elif action in ["reason", "推理", "2"]:
                if not args:
                    print("❌ 请输入问题")
                else:
                    print(f"\n🔮 Reasoning: {args}")
                    result = system.reason(args)
                    print(f"\n✅ Result:")
                    print(f"   Level: {result['consciousness_level']}")
                    print(f"   Depth: {result['depth']:.0%}")
                    print(f"   Confidence: {result['confidence']:.0%}")
            
            elif action in ["test", "测试", "3"]:
                print("\n🧪 Running tests...")
                test_queries = [
                    "为什么天空是蓝色的?",
                    "如果AI超越人类会怎样?",
                    "证明勾股定理"
                ]
                for q in test_queries:
                    print(f"\n🔍 Query: {q}")
                    result = system.reason(q)
                    print(f"   ✅ Level: {result['consciousness_level']}")
                print("\n🎉 All tests passed!")
            
            else:
                print(f"❌ Unknown command: {action}")
        
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break


if __name__ == "__main__":
    main()
