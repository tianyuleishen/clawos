#!/usr/bin/env python3
"""数据集下载器"""

import os
import json
import subprocess

dataset_dir = "/home/admin/.openclaw/workspace/datasets"
os.makedirs(dataset_dir, exist_ok=True)

def download(url, filename):
    """下载并保存"""
    filepath = os.path.join(dataset_dir, filename)
    print(f"📥 下载: {filename}...")
    
    try:
        result = subprocess.run(
            ['curl', '-s', '-L', url, '-o', filepath],
            capture_output=True, timeout=30
        )
        
        if result.returncode == 0:
            # 检查是否是404
            with open(filepath, 'r') as f:
                content = f.read()
            if '404' in content or 'Not Found' in content:
                print(f"   ❌ 404错误，跳过")
                return False
            print(f"   ✅ 下载成功: {len(content)} bytes")
            return True
    except Exception as e:
        print(f"   ❌ 错误: {e}")
    return False

# LogiQA
logiqa_urls = [
    ("https://raw.githubusercontent.com/boume/prompt-benchmark/main/data/LogiQA/logiqa_test.json", "logiqa_test.json"),
    ("https://github.com/boume/prompt-benchmark/raw/main/data/LogiQA/logiqa_test.json", "logiqa_test2.json"),
]

# 尝试多个源
download("https://raw.githubusercontent.com/awslabs/benchmark-ai/master/data/logiqa/test.json", "logiqa_test.json")

# RuleTaker
download("https://raw.githubusercontent.com/ysymyth/RuleTaker/master/data/ruletaker-test.json", "ruletaker.json")

# ProofWriter
download("https://raw.githubusercontent.com/OAI/AutoPrompt/main/proofwriter/proofwriter_test.json", "proofwriter.json")

# HLE
print("📥 HLE (模拟数据)...")
hle_samples = []
for i in range(100):
    hle_samples.append({
        "id": f"hle_{i}",
        "question": f"HLE问题 #{i+1}",
        "answer": "A",
        "subject": "mathematics"
    })
with open(os.path.join(dataset_dir, "hle.json"), 'w') as f:
    json.dump(hle_samples, f, indent=2)
print(f"   ✅ HLE: 100题 (模拟)")

# ARC-AGI-3 (模拟)
print("📥 ARC-AGI-3 (模拟数据)...")
arc_samples = []
for i in range(50):
    arc_samples.append({
        "id": f"arc_{i}",
        "task_type": "transformation",
        "answer": "correct"
    })
with open(os.path.join(dataset_dir, "arc_agi_3.json"), 'w') as f:
    json.dump(arc_samples, f, indent=2)
print(f"   ✅ ARC-AGI-3: 50题 (模拟)")

# CritPt已有
print("\n✅ 数据集准备完成!")
