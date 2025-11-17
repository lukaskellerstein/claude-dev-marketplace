---
name: gpu-optimization
description: Automatically optimizes GPU usage and memory management
allowed-tools: Bash, Read
---

# GPU Optimization Skill

Automatically monitors and optimizes GPU usage during training and inference.

## Activation Triggers

This skill activates automatically when:
- GPU memory usage > 90%
- OOM errors detected
- Training speed below expected
- Multi-GPU imbalance detected
- GPU temperature > 80°C
- User starts training or inference

## Responsibilities

1. **Monitor GPU health and utilization**
2. **Detect and prevent OOM errors**
3. **Optimize memory usage automatically**
4. **Balance load across multiple GPUs**
5. **Suggest performance improvements**

## Automatic Interventions

### Memory Optimization

When memory usage is critical (>90%):

```python
# Clear CUDA cache
import torch
torch.cuda.empty_cache()

# Suggest enabling gradient checkpointing
print("💡 Suggestion: Enable gradient checkpointing to reduce memory usage")
print("   model.gradient_checkpointing_enable()")

# Suggest reducing batch size
print("💡 Suggestion: Reduce batch size")
print("   Current batch size might be too large for available GPU memory")
```

### Performance Monitoring

Continuously check:
- GPU utilization percentage
- Memory usage (allocated vs reserved vs free)
- Temperature
- Power draw
- Clock speeds

```bash
# Monitor GPU stats
nvidia-smi --query-gpu=utilization.gpu,memory.used,memory.total,temperature.gpu,power.draw --format=csv
```

### Multi-GPU Load Balancing

For multi-GPU training:
- Monitor load distribution across GPUs
- Detect imbalanced workloads
- Suggest tensor parallelism adjustments
- Recommend better data parallelism settings

## Optimization Strategies

### 1. Mixed Precision Training

Automatically suggest when not enabled:
```python
# Enable mixed precision
print("💡 Enable mixed precision for faster training:")
print("   training_args.bf16 = True  # For A100/H100")
print("   training_args.fp16 = True  # For V100/T4")
```

### 2. Flash Attention

Check if Flash Attention is available and suggest:
```python
try:
    import flash_attn
    print("✅ Flash Attention available")
    print("💡 Use: attn_implementation='flash_attention_2' when loading model")
except ImportError:
    print("❌ Flash Attention not available")
    print("💡 Install with: pip install flash-attn")
```

### 3. Gradient Accumulation

When batch size is limited:
```python
print("💡 Use gradient accumulation to increase effective batch size:")
print("   gradient_accumulation_steps = 4")
print("   Effective batch size = batch_size * gradient_accumulation_steps")
```

### 4. CPU Offloading

For large models:
```python
print("💡 Consider CPU offloading for very large models:")
print("   from accelerate import infer_auto_device_map")
print("   device_map = infer_auto_device_map(model)")
```

### 5. Tensor Parallelism

For multi-GPU scenarios:
```python
import torch
num_gpus = torch.cuda.device_count()
if num_gpus > 1:
    print(f"✅ {num_gpus} GPUs detected")
    print("💡 Enable tensor parallelism:")
    print(f"   tensor_parallel_size = {num_gpus}")
```

## Alerts and Warnings

### Critical (🚨)
- Memory usage > 95%: Risk of OOM crash
- Temperature > 85°C: Thermal throttling imminent
- Power limit hit: Performance degraded

### Warning (⚠️)
- Memory usage > 85%: High memory pressure
- Temperature > 80°C: Monitor thermal conditions
- GPU utilization < 50%: Underutilization (check bottlenecks)

### Info (💡)
- Optimization suggestions
- Best practice recommendations
- Performance tips

## Diagnostic Commands

When issues detected, run diagnostics:

```bash
# Full GPU status
nvidia-smi

# Memory breakdown
nvidia-smi --query-gpu=memory.total,memory.used,memory.free --format=csv

# Process-specific usage
nvidia-smi --query-compute-apps=pid,used_memory --format=csv

# Real-time monitoring
watch -n 1 nvidia-smi
```

## Recovery Actions

### On OOM Error

1. Clear CUDA cache immediately
2. Reduce batch size by 50%
3. Enable gradient checkpointing
4. Suggest gradient accumulation
5. Consider model quantization

```python
# Emergency cleanup
import torch
import gc

torch.cuda.empty_cache()
gc.collect()

print("🔧 Recovering from OOM error...")
print("✅ Cleared CUDA cache")
print("💡 Reducing batch size and retrying...")
```

### On Slow Training

1. Check GPU utilization
2. Verify data loading isn't bottleneck
3. Suggest optimization flags
4. Check for CPU bottlenecks

```python
print("🔍 Diagnosing slow training...")
print("Checking:")
print("  - GPU utilization")
print("  - Data loading speed")
print("  - CPU usage")
print("  - I/O wait time")
```

## Best Practices Enforcement

Automatically remind users of best practices:

1. **Use mixed precision**: 2x speedup with minimal quality loss
2. **Enable Flash Attention**: 10x memory efficiency for long contexts
3. **Gradient checkpointing**: Essential for large models
4. **Optimize data loading**: Use multiple workers, pin memory
5. **Monitor actively**: Watch for anomalies
6. **Save frequently**: Checkpoint every N steps
7. **Profile code**: Find bottlenecks with PyTorch profiler
8. **Update drivers**: Keep CUDA/drivers current

## Proactive Suggestions

Based on context, proactively suggest:

**Before Training:**
- Verify GPU is detected
- Check available memory
- Suggest optimal batch size
- Recommend training arguments

**During Training:**
- Monitor for issues
- Alert on anomalies
- Suggest optimizations
- Track performance metrics

**After Training:**
- Report GPU utilization stats
- Highlight any issues encountered
- Suggest improvements for next run

## Integration with Other Skills

Works together with:
- **memory-management**: Coordinate memory strategies
- **hyperparameter-tuning**: Adjust batch size/learning rate
- **model-selection**: Recommend appropriate model sizes

## Examples

### Startup Check
```
🔍 GPU Optimization Check...
✅ GPU detected: NVIDIA A100 (40GB)
✅ Available memory: 39.2 GB
✅ CUDA version: 12.1
💡 Recommendations:
   - Enable bf16 mixed precision
   - Use Flash Attention 2
   - Suggested batch size: 4-8
```

### During Training Warning
```
⚠️ High GPU memory usage detected (92%)
🔧 Automatic interventions:
   - Cleared CUDA cache
   - Freed 2.3 GB
💡 Consider:
   - Enabling gradient checkpointing
   - Reducing batch size if issues persist
```

### Multi-GPU Imbalance
```
⚠️ GPU load imbalance detected
   GPU 0: 95% utilization, 38GB used
   GPU 1: 45% utilization, 18GB used
💡 Suggestion:
   - Check data parallelism configuration
   - Ensure even batch distribution
   - Consider tensor parallelism instead
```

## Notes

- This skill runs passively in the background
- Activates automatically based on conditions
- Does not require explicit user invocation
- Provides real-time monitoring and suggestions
- Integrates seamlessly with training workflows
