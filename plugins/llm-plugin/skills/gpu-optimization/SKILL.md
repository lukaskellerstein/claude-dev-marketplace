---
name: gpu-optimization
description: Master GPU utilization and performance for LLM training and inference. Use when optimizing training speed, maximizing throughput, enabling mixed precision, configuring multi-GPU, monitoring utilization, preventing thermal issues, or improving cost-efficiency.
allowed-tools: Bash, Read
---

# GPU Optimization Skill

Automatically optimize GPU usage during LLM training and inference through performance monitoring, resource optimization, and best practice enforcement for maximum efficiency.

## When to Use This Skill

1. **Training Acceleration** - Maximizing training speed
2. **Inference Optimization** - Improving throughput
3. **Multi-GPU Setup** - Distributing workloads
4. **Mixed Precision** - Enabling FP16/BF16
5. **Utilization Monitoring** - Tracking GPU usage
6. **Thermal Management** - Preventing throttling
7. **Cost Optimization** - Efficient resource use
8. **Batch Size Tuning** - Maximizing throughput
9. **Memory Efficiency** - Optimizing memory usage
10. **Performance Profiling** - Finding bottlenecks
11. **Production Deployment** - Scaling efficiently
12. **Hardware Selection** - Choosing GPUs
13. **Power Management** - Controlling power draw
14. **Cluster Management** - Multi-node optimization
15. **Continuous Monitoring** - Real-time tracking

## Quick Start

```bash
# Monitor GPU usage
nvidia-smi --query-gpu=utilization.gpu,memory.used,memory.total,temperature.gpu --format=csv

# Check for issues
nvidia-smi
```

```python
# Enable mixed precision
training_args = TrainingArguments(
    bf16=True,  # For A100/H100
    # or fp16=True for V100/T4
)

# Enable gradient checkpointing
model.gradient_checkpointing_enable()

# Multi-GPU
if torch.cuda.device_count() > 1:
    model = nn.DataParallel(model)
```

## Optimization Strategies

```yaml
1. Mixed Precision Training:
   - bf16 for A100/H100 (recommended)
   - fp16 for V100/T4
   - 2x speedup, 50% memory savings

2. Flash Attention:
   - 2-4x faster attention
   - 10x memory efficiency
   - Essential for long sequences

3. Gradient Checkpointing:
   - Trade compute for memory
   - ~30% slower, 50% less memory
   - Enable when memory-constrained

4. Optimal Batch Size:
   - Maximize GPU utilization
   - Start small, increase until OOM
   - Use gradient accumulation if needed

5. Multi-GPU Strategies:
   - Data Parallel: Simple, scales well
   - Model Parallel: For huge models
   - Pipeline Parallel: For very deep models
```

## Related Skills

- **memory-management**: Coordinates memory with GPU optimization
- **hyperparameter-tuning**: Optimizes training parameters
- **model-selection**: Chooses GPU-appropriate models

This skill ensures maximum GPU performance and efficiency for all LLM operations.
