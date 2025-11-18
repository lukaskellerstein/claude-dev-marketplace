---
name: memory-management
description: Master GPU memory management for LLM operations, preventing OOM errors. Use when loading models, training, optimizing memory, enabling gradient checkpointing, implementing offloading, monitoring usage, or ensuring efficient resource utilization.
allowed-tools: Bash, Read
---

# Memory Management Skill

Prevent OOM errors and optimize GPU memory usage through comprehensive monitoring, automatic cleanup, and smart allocation strategies for LLM training and inference.

## When to Use This Skill

1. **Model Loading** - Checking memory before loading
2. **Training Setup** - Preventing OOM during training
3. **Memory Optimization** - Reducing memory footprint
4. **Gradient Checkpointing** - Trading compute for memory
5. **Multi-GPU Setup** - Distributing across GPUs
6. **Batch Size Selection** - Maximizing within limits
7. **OOM Recovery** - Handling memory errors
8. **Production Deployment** - Ensuring stability
9. **Memory Profiling** - Understanding usage patterns
10. **Resource Planning** - Capacity management
11. **Cost Optimization** - Efficient GPU utilization
12. **Model Sharding** - Splitting large models
13. **CPU Offloading** - Using system memory
14. **Flash Attention** - Memory-efficient attention
15. **Continuous Monitoring** - Tracking memory health

## Quick Start

```python
import torch

def check_gpu_memory():
    """Quick memory check"""
    if torch.cuda.is_available():
        allocated = torch.cuda.memory_allocated() / 1024**3
        reserved = torch.cuda.memory_reserved() / 1024**3
        total = torch.cuda.get_device_properties(0).total_memory / 1024**3
        free = total - allocated
        
        print(f"Allocated: {allocated:.2f} GB")
        print(f"Reserved: {reserved:.2f} GB")
        print(f"Free: {free:.2f} GB")
        print(f"Total: {total:.2f} GB")
        
        if allocated / total > 0.9:
            print("⚠️ High memory usage!")
            torch.cuda.empty_cache()
```

## Memory Optimization Techniques

```yaml
1. Gradient Checkpointing:
   model.gradient_checkpointing_enable()
   Saves ~30% memory during training

2. Flash Attention:
   attn_implementation='flash_attention_2'
   10x memory efficiency, 2-4x speed

3. Mixed Precision:
   bf16=True or fp16=True
   50% memory reduction

4. Batch Size Optimization:
   Start with batch_size=1
   Gradually increase until OOM

5. Gradient Accumulation:
   gradient_accumulation_steps=4
   Effective larger batch with less memory
```

## Related Skills

- **hyperparameter-tuning**: Optimizes batch sizes for memory
- **gpu-optimization**: Coordinates GPU resource usage
- **model-selection**: Chooses models fitting in memory

This skill ensures stable, efficient memory usage throughout LLM operations.
