---
name: memory-management
description: Manages memory efficiently during model operations
allowed-tools: Bash, Read
---

# Memory Management Skill

Prevents OOM errors and optimizes memory usage automatically throughout the ML workflow.

## Activation Triggers

This skill activates when:
- Before loading a model
- After each training epoch
- On OOM detection
- When switching models
- Memory usage exceeds 85%
- User requests memory optimization

## Responsibilities

1. **Monitor memory consumption**
2. **Prevent OOM crashes**
3. **Optimize memory allocation**
4. **Clean up unused resources**
5. **Provide memory usage guidance**

## Memory Monitoring

### Real-time Memory Stats

```python
import torch

def get_memory_stats():
    """Get comprehensive memory statistics"""
    if not torch.cuda.is_available():
        return {"error": "No CUDA device available"}

    stats = {}
    for i in range(torch.cuda.device_count()):
        torch.cuda.set_device(i)

        stats[f'gpu_{i}'] = {
            'allocated_gb': torch.cuda.memory_allocated(i) / 1024**3,
            'reserved_gb': torch.cuda.memory_reserved(i) / 1024**3,
            'free_gb': torch.cuda.mem_get_info(i)[0] / 1024**3,
            'total_gb': torch.cuda.mem_get_info(i)[1] / 1024**3,
            'utilization_%': (torch.cuda.memory_allocated(i) /
                            torch.cuda.mem_get_info(i)[1] * 100)
        }

    return stats

# Display stats nicely
def print_memory_stats():
    stats = get_memory_stats()
    print("\n📊 GPU Memory Status:")
    for gpu, info in stats.items():
        print(f"\n{gpu.upper()}:")
        print(f"  Allocated: {info['allocated_gb']:.2f} GB")
        print(f"  Reserved:  {info['reserved_gb']:.2f} GB")
        print(f"  Free:      {info['free_gb']:.2f} GB")
        print(f"  Total:     {info['total_gb']:.2f} GB")
        print(f"  Usage:     {info['utilization_%']:.1f}%")
```

### Memory Thresholds

```python
THRESHOLDS = {
    'WARNING': 85,    # Start warning at 85%
    'CRITICAL': 90,   # Critical at 90%
    'EMERGENCY': 95   # Emergency cleanup at 95%
}

def check_memory_threshold():
    """Check if memory usage exceeds thresholds"""
    stats = get_memory_stats()

    for gpu, info in stats.items():
        usage = info['utilization_%']

        if usage >= THRESHOLDS['EMERGENCY']:
            print(f"🚨 EMERGENCY: {gpu} at {usage:.1f}% memory!")
            emergency_cleanup()
        elif usage >= THRESHOLDS['CRITICAL']:
            print(f"⚠️ CRITICAL: {gpu} at {usage:.1f}% memory!")
            critical_cleanup()
        elif usage >= THRESHOLDS['WARNING']:
            print(f"⚠️ WARNING: {gpu} at {usage:.1f}% memory!")
            suggest_optimizations()
```

## Preventive Measures

### Pre-allocation Check

Before loading models or starting training:

```python
def check_available_memory(required_gb):
    """Check if sufficient memory available"""
    stats = get_memory_stats()

    for gpu, info in stats.items():
        free_gb = info['free_gb']

        if free_gb < required_gb:
            print(f"❌ Insufficient memory on {gpu}")
            print(f"   Required: {required_gb:.2f} GB")
            print(f"   Available: {free_gb:.2f} GB")
            print(f"   Shortfall: {required_gb - free_gb:.2f} GB")

            # Suggest solutions
            print("\n💡 Solutions:")
            print("   1. Clear CUDA cache")
            print("   2. Use model quantization")
            print("   3. Enable gradient checkpointing")
            print("   4. Reduce batch size")
            return False

    print(f"✅ Sufficient memory available ({stats['gpu_0']['free_gb']:.2f} GB free)")
    return True
```

### Automatic Cleanup

Periodic cleanup to prevent memory leaks:

```python
import torch
import gc

def automatic_cleanup():
    """Perform automatic memory cleanup"""
    print("🧹 Performing automatic cleanup...")

    # Clear CUDA cache
    torch.cuda.empty_cache()

    # Run garbage collection
    gc.collect()

    # Synchronize CUDA operations
    if torch.cuda.is_available():
        torch.cuda.synchronize()

    print("✅ Cleanup complete")

    # Show recovered memory
    stats = get_memory_stats()
    print(f"📊 Free memory: {stats['gpu_0']['free_gb']:.2f} GB")
```

### Batch Size Adjustment

Dynamically adjust batch size based on available memory:

```python
def suggest_batch_size(model_size_gb, max_seq_length=2048):
    """Suggest optimal batch size based on available memory"""
    stats = get_memory_stats()
    free_gb = stats['gpu_0']['free_gb']

    # Rule of thumb: model + activations + optimizer states
    # Activations ≈ batch_size * seq_length * hidden_size * layers * 4 (for bf16)
    # Reserve 20% buffer

    usable_memory = free_gb * 0.8  # 80% of free memory
    available_for_batch = usable_memory - model_size_gb

    # Rough estimate: 1 GB per batch of 2048 tokens for 7B model
    estimated_batch_size = int(available_for_batch / (max_seq_length / 2048))

    # Clamp to reasonable range
    suggested_batch_size = max(1, min(estimated_batch_size, 32))

    print(f"💡 Suggested batch size: {suggested_batch_size}")
    print(f"   Based on: {free_gb:.2f} GB free memory")
    print(f"   Model size: {model_size_gb:.2f} GB")

    return suggested_batch_size
```

## Recovery Actions

### Emergency Cleanup

When memory is critically low:

```python
def emergency_cleanup():
    """Aggressive cleanup when memory critical"""
    print("🚨 EMERGENCY CLEANUP INITIATED")

    # 1. Clear CUDA cache
    torch.cuda.empty_cache()
    print("✅ Cleared CUDA cache")

    # 2. Aggressive garbage collection
    gc.collect()
    torch.cuda.synchronize()
    print("✅ Garbage collection complete")

    # 3. Reset CUDA memory allocator
    torch.cuda.reset_peak_memory_stats()
    print("✅ Reset memory statistics")

    # 4. Show results
    stats = get_memory_stats()
    print(f"📊 Recovered to: {stats['gpu_0']['utilization_%']:.1f}% usage")

    # 5. Suggest actions if still critical
    if stats['gpu_0']['utilization_%'] > 90:
        print("\n⚠️ Memory still critical. Consider:")
        print("   1. Reducing batch size by 50%")
        print("   2. Enabling gradient checkpointing")
        print("   3. Using gradient accumulation")
        print("   4. Switching to QLoRA/4-bit quantization")
```

### Critical Cleanup

When approaching limits:

```python
def critical_cleanup():
    """Standard cleanup for critical memory"""
    print("⚠️ Critical memory cleanup...")

    torch.cuda.empty_cache()
    gc.collect()

    stats = get_memory_stats()
    print(f"📊 Current usage: {stats['gpu_0']['utilization_%']:.1f}%")

    if stats['gpu_0']['utilization_%'] > 85:
        suggest_optimizations()
```

### Suggest Optimizations

When memory is getting tight:

```python
def suggest_optimizations():
    """Suggest memory optimization strategies"""
    print("\n💡 Memory Optimization Suggestions:")

    suggestions = [
        "1. Enable gradient checkpointing:",
        "   model.gradient_checkpointing_enable()",
        "",
        "2. Use gradient accumulation:",
        "   gradient_accumulation_steps = 4",
        "",
        "3. Reduce batch size:",
        "   per_device_train_batch_size = 2",
        "",
        "4. Use mixed precision:",
        "   bf16 = True  # or fp16 = True",
        "",
        "5. Offload optimizer to CPU:",
        "   optim = 'adamw_bnb_8bit'",
        "",
        "6. Use QLoRA for fine-tuning:",
        "   load_in_4bit = True"
    ]

    for suggestion in suggestions:
        print(suggestion)
```

## Memory Optimization Techniques

### 1. Gradient Checkpointing

```python
def enable_gradient_checkpointing(model):
    """Enable gradient checkpointing to save memory"""
    if hasattr(model, 'gradient_checkpointing_enable'):
        model.gradient_checkpointing_enable()
        print("✅ Gradient checkpointing enabled")
        print("💡 Saves ~30% memory during training")
    else:
        print("❌ Model doesn't support gradient checkpointing")
```

### 2. Flash Attention

```python
def suggest_flash_attention():
    """Suggest Flash Attention for memory efficiency"""
    try:
        import flash_attn
        print("✅ Flash Attention available")
        print("💡 Benefits:")
        print("   - 10x memory efficiency")
        print("   - 2-4x speed improvement")
        print("   - Essential for long sequences")
        print("\nUsage:")
        print("   attn_implementation='flash_attention_2'")
    except ImportError:
        print("❌ Flash Attention not installed")
        print("💡 Install with: pip install flash-attn")
```

### 3. CPU Offloading

```python
def suggest_cpu_offloading(model_size_gb):
    """Suggest CPU offloading for large models"""
    stats = get_memory_stats()
    free_gb = stats['gpu_0']['free_gb']

    if model_size_gb > free_gb:
        print("💡 Model too large for GPU memory")
        print("   Consider CPU offloading:")
        print("\n   from accelerate import load_checkpoint_and_dispatch")
        print("   model = load_checkpoint_and_dispatch(")
        print("       model, checkpoint, device_map='auto'")
        print("   )")
```

### 4. Model Sharding

```python
def suggest_model_sharding(num_gpus):
    """Suggest model sharding across GPUs"""
    if num_gpus > 1:
        print(f"💡 {num_gpus} GPUs available")
        print("   Consider model sharding:")
        print("\n   device_map = 'auto'")
        print("   # Automatically distributes model across GPUs")
```

## Monitoring Schedule

### Continuous Monitoring

```python
# Check memory:
# - Before model loading
# - After each training step (every 10 steps)
# - After each epoch
# - When saving checkpoints
# - On user request

def periodic_memory_check(step):
    """Periodic memory monitoring"""
    if step % 10 == 0:  # Check every 10 steps
        stats = get_memory_stats()
        usage = stats['gpu_0']['utilization_%']

        if usage > 90:
            print(f"⚠️ Step {step}: High memory usage ({usage:.1f}%)")
            critical_cleanup()
        elif usage > 85:
            print(f"💡 Step {step}: Memory usage at {usage:.1f}%")
```

## Integration with Training

### Training Callbacks

```python
from transformers import TrainerCallback

class MemoryManagementCallback(TrainerCallback):
    """Custom callback for memory management during training"""

    def on_step_end(self, args, state, control, **kwargs):
        """Check memory after each step"""
        if state.global_step % 10 == 0:
            check_memory_threshold()

    def on_epoch_end(self, args, state, control, **kwargs):
        """Cleanup after each epoch"""
        print("\n🧹 End of epoch cleanup...")
        automatic_cleanup()

    def on_train_begin(self, args, state, control, **kwargs):
        """Check memory before training"""
        print("\n📊 Pre-training memory check...")
        print_memory_stats()
```

## Best Practices

1. **Monitor continuously**: Track memory throughout execution
2. **Clean proactively**: Don't wait for OOM
3. **Set conservative limits**: Act before reaching maximum
4. **Use optimization techniques**: Gradient checkpointing, mixed precision
5. **Plan ahead**: Estimate memory requirements before starting
6. **Test with small data first**: Validate memory usage patterns
7. **Keep buffer**: Don't use 100% of available memory
8. **Document limits**: Know your hardware constraints

## Warning Signs

Watch for these indicators of memory issues:

- Memory usage > 85%: Warning zone
- Memory usage > 90%: Critical zone
- Memory usage > 95%: Emergency zone
- Frequent cache clearing: Possible memory leak
- Increasing memory over time: Definite memory leak
- OOM errors: Immediate action needed

## Notes

- This skill works in tandem with `gpu-optimization`
- Activates automatically based on memory conditions
- Provides both reactive and proactive management
- Integrates seamlessly with training workflows
- Can be disabled if manual control preferred
