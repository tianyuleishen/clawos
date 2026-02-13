#!/usr/bin/env python3
"""
🦞 ClawOS Enhanced Reasoning Engine v2.7.1
Phase 1 Complete: Memory-Augmented + Self-Verification Integration
"""

import sys
sys.path.insert(0, '/home/admin/.openclaw/workspace')

from typing import Dict, List, Any, Optional
from datetime import datetime
import json


class IntegratedReasoningEngine:
    """
    集成推理引擎 v2.7.1
    整合记忆增强推理 + 自我验证
    """
    
    VERSION = "2.7.1"
    
    def __init__(self):
        # 导入Phase 1模块
        from clawos.core.reasoning.memory_augmented import MemoryAugmentedReasoning, create_memory_augmented_reasoning
        from clawos.core.reasoning.self_verification import SelfVerificationEngine, create_self_verification
        
        self.memory_reasoning = create_memory_augmented_reasoning()
        self.self_verification = create_self_verification()
        
        # 统计数据
        self.stats = {
            "total_problems": 0,
            "memory_solved": 0,
            "verification_passed": 0,
            "verification_failed": 0,
            "avg_confidence": 0.0,
            "avg_verification_score": 0.0
        }
        
        print(f"\n✅ ClawOS Enhanced Engine v{self.VERSION} 已初始化")
        print("   整合模块:")
        print("   - Memory-Augmented Reasoning v1.0")
        print("   - Self-Verification v1.0")
    
    def solve(self, problem: Dict) -> Dict:
        """
        综合求解：记忆增强推理 + 自我验证
        """
        
        self.stats["total_problems"] += 1
        
        # 步骤1: 记忆增强推理
        memory_result = self.memory_reasoning.solve(problem)
        
        # 步骤2: 自我验证
        solution = memory_result.get("result", {})
        chain = memory_result.get("chain_state", {}).get("verified_nodes", 0)
        
        verification_result = self.self_verification.verify(
            problem,
            solution,
            [{"verified": i < chain} for i in range(chain)]
        )
        
        # 更新统计
        if verification_result["is_passed"]:
            self.stats["verification_passed"] += 1
        else:
            self.stats["verification_failed"] += 1
        
        # 计算综合置信度
        memory_conf = memory_result.get("confidence", 0.7)
        verify_conf = verification_result.get("confidence_factor", 0.7)
        overall_conf = memory_conf * verify_conf
        
        # 更新平均
        total = self.stats["total_problems"]
        self.stats["avg_confidence"] = (
            (self.stats["avg_confidence"] * (total - 1) + overall_conf) / total
        )
        self.stats["avg_verification_score"] = (
            (self.stats["avg_verification_score"] * (total - 1) + verification_result["overall_score"]) / total
        )
        
        # 构建最终结果
        final_result = {
            "problem_id": problem.get("id", "unknown"),
            "problem_type": problem.get("type", "unknown"),
            "question": problem.get("question", "")[:100],
            
            # 推理结果
            "reasoning_result": {
                "source": memory_result.get("source", "unknown"),
                "confidence": memory_conf,
                "chain_state": memory_result.get("chain_state", {})
            },
            
            # 验证结果
            "verification_result": {
                "passed": verification_result["is_passed"],
                "overall_score": verification_result["overall_score"],
                "confidence_factor": verify_conf,
                "multi_path": verification_result["multi_path_verification"]["summary"],
                "consistency": verification_result["consistency_checks"]["summary"],
                "recommendations": verification_result["recommendations"]
            },
            
            # 综合结果
            "final_answer": {
                "solution": solution,
                "confidence": overall_conf,
                "is_valid": verification_result["is_passed"]
            },
            
            "timestamp": datetime.now().isoformat()
        }
        
        return final_result
    
    def batch_solve(self, problems: List[Dict]) -> Dict:
        """批量求解"""
        results = []
        
        for problem in problems:
            result = self.solve(problem)
            results.append(result)
        
        # 汇总
        passed = sum(1 for r in results if r["final_answer"]["is_valid"])
        
        return {
            "total": len(results),
            "passed": passed,
            "failed": len(results) - passed,
            "pass_rate": f"{passed/len(results):.1%}" if results else "N/A",
            "avg_confidence": sum(r["final_answer"]["confidence"] for r in results) / len(results) if results else 0,
            "results": results
        }
    
    def get_statistics(self) -> Dict:
        """获取统计"""
        total = self.stats["total_problems"]
        pass_rate = self.stats["verification_passed"] / total if total > 0 else 0
        
        return {
            "version": self.VERSION,
            **self.stats,
            "pass_rate": f"{pass_rate:.2%}",
            "memory_stats": self.memory_reasoning.get_statistics(),
            "verification_stats": self.self_verification.get_statistics()
        }


def main():
    """测试集成引擎"""
    
    print("\n" + "="*100)
    print("🦞 ClawOS Phase 1 Complete: Memory-Augmented + Self-Verification")
    print("="*100)
    
    # 创建引擎
    engine = IntegratedReasoningEngine()
    
    # 测试问题
    test_problems = [
        {
            "id": "test-1",
            "type": "logic",
            "question": "如果A→B，B→C，C→D。那么A→D吗？"
        },
        {
            "id": "test-2",
            "type": "math", 
            "question": "求函数f(x)=x²+2x+1的导数"
        },
        {
            "id": "test-3",
            "type": "physics",
            "question": "量子纠缠中两个粒子的自旋关系是什么？"
        }
    ]
    
    print("\n🧪 测试集成推理:")
    for problem in test_problems:
        result = engine.solve(problem)
        print(f"\n  问题: {problem['question'][:30]}...")
        print(f"    通过: {'✅' if result['final_answer']['is_valid'] else '❌'}")
        print(f"    置信度: {result['final_answer']['confidence']:.1%}")
    
    # 批量测试
    print("\n📊 批量测试结果:")
    batch_result = engine.batch_solve(test_problems)
    print(f"  总问题: {batch_result['total']}")
    print(f"  通过: {batch_result['passed']}")
    print(f"  失败: {batch_result['failed']}")
    print(f"  通过率: {batch_result['pass_rate']}")
    print(f"  平均置信度: {batch_result['avg_confidence']:.1%}")
    
    # 统计
    stats = engine.get_statistics()
    print(f"\n📈 详细统计:")
    print(f"  版本: {stats['version']}")
    print(f"  总问题: {stats['total_problems']}")
    print(f"  验证通过: {stats['verification_passed']}")
    print(f"  验证失败: {stats['verification_failed']}")
    print(f"  平均置信度: {stats['avg_confidence']:.1%}")
    
    print("\n✅ Phase 1 集成测试完成！")


if __name__ == "__main__":
    main()
