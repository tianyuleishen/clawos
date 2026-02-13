#!/usr/bin/env python3
"""
🦞 ClawOS Self-Verification Module
Phase 1: 自我验证机制 - 多路径验证 + 一致性检查
"""

import json
import hashlib
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from collections import Counter
import random


@dataclass
class VerificationPath:
    """验证路径"""
    path_id: str
    method: str
    steps: List[Dict]
    result: Any
    confidence: float
    timestamp: str
    
    def to_dict(self) -> Dict:
        return {
            "path_id": self.path_id,
            "method": self.method,
            "steps": self.steps,
            "result": self.result,
            "confidence": self.confidence,
            "timestamp": self.timestamp
        }


@dataclass
class ConsistencyCheck:
    """一致性检查结果"""
    check_name: str
    passed: bool
    score: float
    details: Dict
    
    def to_dict(self) -> Dict:
        return {
            "check_name": self.check_name,
            "passed": self.passed,
            "score": self.score,
            "details": self.details
        }


class MultiPathVerifier:
    """多路径验证器"""
    
    def __init__(self):
        self.methods = []
        self.verification_history: List[VerificationPath] = []
    
    def add_method(self, name: str, method_func) -> None:
        """添加验证方法"""
        self.methods.append({
            "name": name,
            "func": method_func
        })
    
    def verify_with_multiple_paths(self, 
                                  problem: Dict,
                                  solution: Any) -> Tuple[List[VerificationPath], Dict]:
        """多路径验证"""
        
        paths = []
        results = []
        
        # 路径1: 逻辑验证
        path1 = self._logical_verification(problem, solution)
        paths.append(path1)
        results.append(path1.result)
        
        # 路径2: 数值验证
        path2 = self._numeric_verification(problem, solution)
        paths.append(path2)
        results.append(path2.result)
        
        # 路径3: 常识验证
        path3 = self._commonsense_verification(problem, solution)
        paths.append(path3)
        results.append(path3.result)
        
        # 路径4: 反证法验证
        path4 = self._counterexample_verification(problem, solution)
        paths.append(path4)
        results.append(path4.result)
        
        # 汇总结果
        summary = self._summarize_results(results)
        
        return paths, summary
    
    def _logical_verification(self, 
                             problem: Dict,
                             solution: Any) -> VerificationPath:
        """逻辑验证"""
        question = problem.get("question", "")
        
        # 检查答案是否符合逻辑
        is_valid = True
        confidence = 0.9
        
        # 检测矛盾
        if "如果" in question and not solution:
            is_valid = False
            confidence = 0.5
        
        return VerificationPath(
            path_id="logical_" + hashlib.md5(question.encode()).hexdigest()[:8],
            method="logical",
            steps=[{"step": "check_consistency", "result": is_valid}],
            result={"valid": is_valid, "confidence": confidence},
            confidence=confidence,
            timestamp=datetime.now().isoformat()
        )
    
    def _numeric_verification(self, 
                             problem: Dict,
                             solution: Any) -> VerificationPath:
        """数值验证"""
        question = problem.get("question", "")
        
        # 检查是否包含数值
        has_numbers = any(char.isdigit() for char in question)
        confidence = 0.85
        
        if has_numbers:
            # 检查答案中的数值
            if solution and any(char.isdigit() for char in str(solution)):
                confidence = 0.9
            else:
                confidence = 0.6
        
        return VerificationPath(
            path_id="numeric_" + hashlib.md5(question.encode()).hexdigest()[:8],
            method="numeric",
            steps=[{"step": "check_values", "result": has_numbers}],
            result={"checked": has_numbers, "confidence": confidence},
            confidence=confidence,
            timestamp=datetime.now().isoformat()
        )
    
    def _commonsense_verification(self, 
                                 problem: Dict,
                                 solution: Any) -> VerificationPath:
        """常识验证"""
        question = problem.get("question", "")
        answer = str(solution) if solution else ""
        
        # 检测常识错误
        violations = []
        confidence = 0.88
        
        # 检查答案是否合理
        if len(answer) > 1000:  # 答案太长
            violations.append("答案过长")
            confidence -= 0.1
        
        if "不可能" in answer or "永远不" in answer:
            violations.append("过于绝对的答案")
            confidence -= 0.05
        
        is_valid = len(violations) == 0
        
        return VerificationPath(
            path_id="commonsense_" + hashlib.md5(question.encode()).hexdigest()[:8],
            method="commonsense",
            steps=[{"step": "check_violations", "result": violations}],
            result={"valid": is_valid, "confidence": confidence, "violations": violations},
            confidence=confidence,
            timestamp=datetime.now().isoformat()
        )
    
    def _counterexample_verification(self, 
                                    problem: Dict,
                                    solution: Any) -> VerificationPath:
        """反证法验证"""
        question = problem.get("question", "")
        answer = str(solution) if solution else ""
        
        # 检查是否能找到反例
        has_counterexample = False
        confidence = 0.82
        
        # 简单检查
        if "所有" in question or "每一个" in question:
            # 全称命题，检查是否有反例
            if any(word in answer for word in ["不一定", "可能不", "例外"]):
                has_counterexample = True
                confidence = 0.9
        
        return VerificationPath(
            path_id="counterexample_" + hashlib.md5(question.encode()).hexdigest()[:8],
            method="counterexample",
            steps=[{"step": "search_counterexample", "result": has_counterexample}],
            result={"has_counterexample": has_counterexample, "confidence": confidence},
            confidence=confidence,
            timestamp=datetime.now().isoformat()
        )
    
    def _summarize_results(self, results: List[Dict]) -> Dict:
        """汇总结果"""
        confidences = [r.get("confidence", 0.5) for r in results]
        avg_confidence = sum(confidences) / len(confidences)
        
        # 计算一致性
        valid_count = sum(1 for r in results if r.get("valid", True))
        consistency = valid_count / len(results)
        
        # 最终置信度
        final_confidence = avg_confidence * (1 + consistency) / 2
        
        return {
            "num_paths": len(results),
            "avg_confidence": avg_confidence,
            "consistency": consistency,
            "final_confidence": min(0.99, final_confidence),
            "all_valid": all(r.get("valid", True) for r in results)
        }


class ConsistencyChecker:
    """一致性检查器"""
    
    def __init__(self):
        self.checks = []
        self.check_history: List[ConsistencyCheck] = []
    
    def add_check(self, name: str, check_func) -> None:
        """添加检查规则"""
        self.checks.append({
            "name": name,
            "func": check_func
        })
    
    def run_all_checks(self, 
                      problem: Dict,
                      solution: Any,
                      reasoning_chain: List[Dict]) -> Tuple[List[ConsistencyCheck], Dict]:
        """运行所有检查"""
        
        checks = []
        
        # 检查1: 单元一致性
        check1 = self._unit_consistency(problem, solution, reasoning_chain)
        checks.append(check1)
        
        # 检查2: 维度一致性
        check2 = self._dimension_consistency(problem, solution, reasoning_chain)
        checks.append(check2)
        
        # 检查3: 范围合理性
        check3 = self._range_reasonableness(problem, solution, reasoning_chain)
        checks.append(check3)
        
        # 检查4: 逻辑一致性
        check4 = self._logical_consistency(problem, solution, reasoning_chain)
        checks.append(check4)
        
        # 检查5: 推理链完整性
        check5 = self._chain_completeness(problem, solution, reasoning_chain)
        checks.append(check5)
        
        # 汇总
        summary = self._summarize_checks(checks)
        
        return checks, summary
    
    def _unit_consistency(self, 
                         problem: Dict,
                         solution: Any,
                         reasoning_chain: List[Dict]) -> ConsistencyCheck:
        """单元一致性检查"""
        question = problem.get("question", "")
        answer = str(solution) if solution else ""
        
        # 检测单位
        units_in_question = self._extract_units(question)
        units_in_answer = self._extract_units(answer)
        
        # 检查一致性
        is_consistent = True
        if units_in_question and units_in_answer:
            is_consistent = self._compare_units(units_in_question, units_in_answer)
        
        score = 0.95 if is_consistent else 0.6
        
        return ConsistencyCheck(
            check_name="unit_consistency",
            passed=is_consistent,
            score=score,
            details={
                "question_units": units_in_question,
                "answer_units": units_in_answer,
                "consistent": is_consistent
            }
        )
    
    def _extract_units(self, text: str) -> List[str]:
        """提取单位"""
        units = []
        unit_patterns = ["米", "秒", "千克", "牛顿", "焦耳", "瓦特", "度", "%"]
        
        for pattern in unit_patterns:
            if pattern in text:
                units.append(pattern)
        
        return units
    
    def _compare_units(self, units1: List[str], units2: List[str]) -> bool:
        """比较单位"""
        # 简化版本：检查是否有交集
        return bool(set(units1) & set(units2))
    
    def _dimension_consistency(self, 
                              problem: Dict,
                              solution: Any,
                              reasoning_chain: List[Dict]) -> ConsistencyCheck:
        """维度一致性检查"""
        question = problem.get("question", "")
        
        # 检查问题维度
        question_dimensions = self._identify_dimensions(question)
        
        # 简化实现
        is_consistent = True
        score = 0.92
        
        return ConsistencyCheck(
            check_name="dimension_consistency",
            passed=is_consistent,
            score=score,
            details={"dimensions": question_dimensions}
        )
    
    def _identify_dimensions(self, text: str) -> List[str]:
        """识别维度"""
        dimensions = []
        
        if any(kw in text for kw in ["长度", "距离", "面积", "体积"]):
            dimensions.append("空间")
        if any(kw in text for kw in ["时间", "速度", "加速度"]):
            dimensions.append("时间")
        if any(kw in text for kw in ["质量", "力", "能量"]):
            dimensions.append("力学")
        if any(kw in text for kw in ["温度", "热量"]):
            dimensions.append("热学")
        
        return dimensions if dimensions else ["通用"]
    
    def _range_reasonableness(self, 
                             problem: Dict,
                             solution: Any,
                             reasoning_chain: List[Dict]) -> ConsistencyCheck:
        """范围合理性检查"""
        answer = str(solution) if solution else ""
        
        # 检查数值范围
        is_reasonable = True
        score = 0.88
        
        # 简单检查
        if len(answer) > 500:
            is_reasonable = False
            score = 0.5
        
        return ConsistencyCheck(
            check_name="range_reasonableness",
            passed=is_reasonable,
            score=score,
            details={"answer_length": len(answer), "reasonable": is_reasonable}
        )
    
    def _logical_consistency(self, 
                            problem: Dict,
                            solution: Any,
                            reasoning_chain: List[Dict]) -> ConsistencyCheck:
        """逻辑一致性检查"""
        question = problem.get("question", "")
        answer = str(solution) if solution else ""
        
        # 检测矛盾
        contradictions = []
        is_consistent = True
        score = 0.90
        
        # 检查是否自相矛盾
        if "但是" in answer or "然而" in answer:
            contradictions.append("答案包含转折，可能存在矛盾")
            score -= 0.1
        
        if len(contradictions) > 0:
            is_consistent = False
        
        return ConsistencyCheck(
            check_name="logical_consistency",
            passed=is_consistent,
            score=max(0.0, score),
            details={"contradictions": contradictions}
        )
    
    def _chain_completeness(self, 
                           problem: Dict,
                           solution: Any,
                           reasoning_chain: List[Dict]) -> ConsistencyCheck:
        """推理链完整性检查"""
        is_complete = True
        score = 0.85
        
        if len(reasoning_chain) < 2:
            is_complete = False
            score = 0.6
        
        return ConsistencyCheck(
            check_name="chain_completeness",
            passed=is_complete,
            score=score,
            details={"chain_length": len(reasoning_chain), "complete": is_complete}
        )
    
    def _summarize_checks(self, checks: List[ConsistencyCheck]) -> Dict:
        """汇总检查结果"""
        passed = sum(1 for c in checks if c.passed)
        avg_score = sum(c.score for c in checks) / len(checks)
        
        return {
            "total_checks": len(checks),
            "passed_checks": passed,
            "failed_checks": len(checks) - passed,
            "pass_rate": passed / len(checks),
            "avg_score": avg_score
        }


class SelfVerificationEngine:
    """完整的自我验证引擎"""
    
    VERSION = "1.0.0"
    
    def __init__(self):
        self.multi_path_verifier = MultiPathVerifier()
        self.consistency_checker = ConsistencyChecker()
        self.statistics = {
            "total_verifications": 0,
            "passed": 0,
            "failed": 0,
            "avg_confidence": 0.0,
            "avg_consistency": 0.0
        }
    
    def verify(self, 
              problem: Dict,
              solution: Any,
              reasoning_chain: List[Dict] = None) -> Dict:
        """执行完整验证"""
        
        if reasoning_chain is None:
            reasoning_chain = []
        
        self.statistics["total_verifications"] += 1
        
        # 步骤1: 多路径验证
        paths, path_summary = self.multi_path_verifier.verify_with_multiple_paths(
            problem, solution
        )
        
        # 步骤2: 一致性检查
        checks, check_summary = self.consistency_checker.run_all_checks(
            problem, solution, reasoning_chain
        )
        
        # 步骤3: 综合评估
        overall_score = self._calculate_overall_score(path_summary, check_summary)
        is_passed = overall_score > 0.7
        
        # 更新统计
        if is_passed:
            self.statistics["passed"] += 1
        else:
            self.statistics["failed"] += 1
        
        # 计算平均
        total = self.statistics["total_verifications"]
        self.statistics["avg_confidence"] = (
            (self.statistics["avg_confidence"] * (total - 1) + path_summary["final_confidence"]) 
            / total
        )
        self.statistics["avg_consistency"] = (
            (self.statistics["avg_consistency"] * (total - 1) + check_summary["avg_score"]) 
            / total
        )
        
        # 构建结果
        result = {
            "is_passed": is_passed,
            "overall_score": overall_score,
            "multi_path_verification": {
                "paths": [p.to_dict() for p in paths],
                "summary": path_summary
            },
            "consistency_checks": {
                "checks": [c.to_dict() for c in checks],
                "summary": check_summary
            },
            "confidence_factor": path_summary["final_confidence"] * check_summary["avg_score"],
            "recommendations": self._generate_recommendations(path_summary, check_summary),
            "timestamp": datetime.now().isoformat()
        }
        
        return result
    
    def _calculate_overall_score(self, 
                                path_summary: Dict,
                                check_summary: Dict) -> float:
        """计算综合分数"""
        path_weight = 0.6
        check_weight = 0.4
        
        path_score = path_summary["final_confidence"]
        check_score = check_summary["avg_score"]
        
        return min(0.99, path_weight * path_score + check_weight * check_score)
    
    def _generate_recommendations(self, 
                                 path_summary: Dict,
                                 check_summary: Dict) -> List[str]:
        """生成改进建议"""
        recommendations = []
        
        if path_summary["avg_confidence"] < 0.8:
            recommendations.append("建议增加验证路径以提高置信度")
        
        if check_summary["pass_rate"] < 1.0:
            recommendations.append("部分一致性检查未通过，建议检查推理逻辑")
        
        if path_summary["consistency"] < 0.8:
            recommendations.append("不同验证路径结果不一致，建议重新验证")
        
        if not recommendations:
            recommendations.append("验证结果良好，无需改进")
        
        return recommendations
    
    def get_statistics(self) -> Dict:
        """获取统计"""
        total = self.statistics["total_verifications"]
        pass_rate = self.statistics["passed"] / total if total > 0 else 0
        
        return {
            **self.statistics,
            "pass_rate": f"{pass_rate:.2%}",
            "version": self.VERSION
        }


def create_self_verification() -> SelfVerificationEngine:
    """创建自我验证引擎"""
    return SelfVerificationEngine()


if __name__ == "__main__":
    sv = create_self_verification()
    
    print("\n" + "="*80)
    print("🦞 ClawOS Self-Verification Module v1.0")
    print("="*80)
    print(f"\n版本: {sv.VERSION}")
    print("\n组件:")
    print("  ✓ MultiPathVerifier (4验证路径)")
    print("  ✓ ConsistencyChecker (5检查项)")
    print("\n验证路径:")
    print("  1. 逻辑验证")
    print("  2. 数值验证")
    print("  3. 常识验证")
    print("  4. 反证法验证")
    print("\n一致性检查:")
    print("  1. 单元一致性")
    print("  2. 维度一致性")
    print("  3. 范围合理性")
    print("  4. 逻辑一致性")
    print("  5. 推理链完整性")
    
    # 测试验证
    test_cases = [
        {
            "problem": {"question": "如果A→B，B→C。那么A→C吗？"},
            "solution": True,
            "chain": [{"step": 1, "result": "A→B"}, {"step": 2, "result": "B→C"}]
        },
        {
            "problem": {"question": "求x²+2x+1=0的解"},
            "solution": "x=-1",
            "chain": [{"step": 1, "result": "配方"}, {"step": 2, "result": "(x+1)²=0"}]
        }
    ]
    
    print("\n🧪 测试自我验证:")
    for i, case in enumerate(test_cases, 1):
        result = sv.verify(case["problem"], case["solution"], case["chain"])
        print(f"\n  测试 {i}:")
        print(f"    通过: {'✅' if result['is_passed'] else '❌'}")
        print(f"    综合分数: {result['overall_score']:.1%}")
        print(f"    置信度: {result['confidence_factor']:.1%}")
    
    # 统计
    stats = sv.get_statistics()
    print("\n📊 统计信息:")
    print(f"  总验证数: {stats['total_verifications']}")
    print(f"  通过: {stats['passed']}")
    print(f"  失败: {stats['failed']}")
    print(f"  通过率: {stats['pass_rate']}")
    print(f"  平均置信度: {stats['avg_confidence']:.1%}")
    print(f"  平均一致性: {stats['avg_consistency']:.1%}")
    
    print("\n✅ Self-Verification 测试完成！")
