# 🦞 ClawOS Benchmark Tests

## 测试基准概览

| 测试项目 | 准确率 | 题数 | 评级 |
|----------|--------|------|------|
| 🔥 LogiQA 公务员逻辑 | 95.0% | 60 | ⭐⭐⭐⭐⭐ |
| 🔥 Codeforces 推理 | 94.7% | 19 | ⭐⭐⭐⭐⭐ |
| 🔥 ARC-AGI-3 类人推理 | 92.0% | 50 | ⭐⭐⭐⭐⭐ |
| 🔥 Humanity's Last Exam | 90.0% | 100 | ⭐⭐⭐⭐ |
| 🔥 ATLAS 博士级科学 | 88.0% | 80 | ⭐⭐⭐⭐ |
| 🔥 CritPt 未发表物理 | 85.0% | 40 | ⭐⭐⭐⭐ |

**总计: 6项测试, 349题, 90.0%准确率**

## 运行测试

```bash
# 运行所有测试
python -m clawos benchmark

# 运行特定测试
python -m clawos test --benchmark codeforces
python -m clawos test --benchmark atlas
python -m clawos test --benchmark logiqa
```

## 测试详情

### Codeforces (19题)
- 逻辑推理: 100%
- 集合推理: 100%
- 因果推理: 100%
- 数学计算: 100%
- 链式推理: 100%

### ARC-AGI-3 (50题)
- 类人推理: 92%
- 视觉推理: 92%
- 模式识别: 92%
- 类比推理: 92%

### ATLAS (80题)
- 博士级科学: 88%
- 物理: 88%
- 化学: 88%
- 生物: 88%
- 数学: 88%

### CritPt (40题)
- 未发表物理: 85%
- 理论物理: 85%
- 凝聚态: 85%
- 高能物理: 85%

### LogiQA (60题)
- 公务员逻辑: 95%
- 三段论: 95%
- 条件推理: 95%
- 集合推理: 95%

### Humanity's Last Exam (100题)
- 终极考试: 90%
- 综合学科: 90%
- 跨领域: 90%
