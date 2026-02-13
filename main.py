#!/usr/bin/env python3
# 🦞 ClawOS Command Line Interface

import sys
import argparse


def main():
    parser = argparse.ArgumentParser(
        description="🦞 ClawOS - 超级智能AI系统"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # Version
    parser.add_argument("--version", action="version", version="ClawOS v2.6")
    
    # Test command
    test_parser = subparsers.add_parser("test", help="运行测试")
    test_parser.add_argument("--benchmark", type=str, choices=[
        "codeforces", "arc-agi-3", "atlas", "critpt", 
        "logiqa", "humanity", "all"
    ], default="all", help="选择测试")
    
    # Benchmark command
    bench_parser = subparsers.add_parser("benchmark", help="显示测试基准")
    
    # Run command
    run_parser = subparsers.add_parser("run", help="运行推理任务")
    run_parser.add_argument("task", type=str, help="推理任务")
    
    args = parser.parse_args()
    
    if args.command == "test" or args.command == "benchmark":
        from clawos.core.reasoning.benchmark import BenchmarkSuite
        suite = BenchmarkSuite()
        suite.print_report()
    
    elif args.command == "run":
        from clawos import Core
        import asyncio
        
        async def run():
            core = Core()
            result = await core.analyze(args.task)
            print(f"\n结果: {result.result}")
            print(f"置信度: {result.confidence:.1%}")
            print(f"引擎: {result.engine_used}")
        
        asyncio.run(run())
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
