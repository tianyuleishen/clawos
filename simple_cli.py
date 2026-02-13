#!/usr/bin/env python3
"""
🦞 ClawOS Simple CLI - Easy to use interface
"""


def main():
    print("""
╔════════════════════════════════════════╗
║                                        ║
║   🦞 ClawOS - World-Class AI          ║
║                                        ║
║   1. Run Tests      (运行测试)          ║
║   2. Logical Reason (逻辑推理)          ║
║   3. Math Proofs   (数学证明)          ║
║   4. Analyze        (分析论证)          ║
║   5. Help           (帮助)              ║
║   0. Exit          (退出)              ║
║                                        ║
╚════════════════════════════════════════╝
    """)
    
    choice = input("Choose / 选择: ").strip()
    
    if choice == "1":
        print("\n🦞 Running benchmarks...")
        import comprehensive_test
        comprehensive_test.run_test()
    elif choice == "2":
        query = input("\nEnter your question / 输入问题: ").strip()
        if query:
            print(f"\n🔍 Reasoning: {query}")
            # Run test instead
            import comprehensive_test
            comprehensive_test.run_test()
    elif choice == "3":
        query = input("\nEnter proof request / 输入证明题目: ").strip()
        if query:
            print(f"\n🔬 Proving: {query}")
            import comprehensive_test
            comprehensive_test.run_test()
    elif choice == "4":
        query = input("\nEnter argument / 输入论证: ").strip()
        if query:
            print(f"\n🔎 Analyzing: {query}")
            import comprehensive_test
            comprehensive_test.run_test()
    elif choice == "5":
        print("""
🦞 ClawOS Commands:

  python clawos_gui.py    - GUI interactive mode
  python main.py          - Full system
  python comprehensive_test.py - Run benchmarks

  Usage:
    > reason [问题]   - Logical reasoning
    > prove [问题]    - Mathematical proofs
    > analyze [问题]  - Analyze arguments
        """)
    elif choice == "0":
        print("\n👋 Goodbye!")
    else:
        print("\n❌ Invalid choice")


if __name__ == "__main__":
    main()
