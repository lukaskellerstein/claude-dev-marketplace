---
name: hyperparameter-tuning
description: Master hyperparameter optimization for LLM training and fine-tuning. Use when starting training, tuning learning rates, configuring batch sizes, selecting schedulers, preventing overfitting, optimizing convergence, or improving model performance through systematic parameter tuning.
allowed-tools: Read
---

# Hyperparameter Tuning Skill

Automatically suggest and validate optimal hyperparameters for LLM training based on model size, dataset characteristics, and hardware constraints. Ensures efficient training with proper convergence.

## When to Use This Skill

1. **Training Setup** - Configuring initial training parameters
2. **Fine-Tuning** - Optimizing LoRA/QLoRA parameters
3. **Convergence Issues** - Fixing training instability
4. **Overfitting Prevention** - Adjusting regularization
5. **Learning Rate Selection** - Choosing optimal LR
6. **Batch Size Optimization** - Maximizing GPU utilization
7. **Scheduler Configuration** - Setting up LR schedules
8. **Gradient Problems** - Fixing explosion/vanishing
9. **Memory Constraints** - Working within GPU limits
10. **Performance Tuning** - Improving training speed
11. **Multi-GPU Training** - Scaling hyperparameters
12. **Transfer Learning** - Adapting pretrained models
13. **Distributed Training** - Configuring for scale
14. **Early Stopping** - Preventing unnecessary training
15. **Hyperparameter Search** - Systematic optimization

## Quick Start

```python
def recommend_hyperparameters(model_size: float, available_memory: float, is_lora: bool):
    """Quick hyperparameter recommendations"""
    
    # Learning rate based on model size
    if model_size < 1e9:
        lr = 1e-3 if is_lora else 5e-4
    elif model_size < 10e9:
        lr = 5e-4 if is_lora else 2e-4
    else:
        lr = 2e-4 if is_lora else 1e-4
    
    # Batch size based on memory
    memory_per_sample = 2.0  # GB estimate
    batch_size = int((available_memory * 0.8) / memory_per_sample)
    batch_size = max(1, min(batch_size, 32))
    
    return {
        'learning_rate': lr,
        'batch_size': batch_size,
        'scheduler': 'cosine',
        'warmup_ratio': 0.1,
        'weight_decay': 0.01,
        'max_grad_norm': 1.0
    }
```

## Real-World Scenarios

### LLaMA-2 7B Fine-Tuning

```yaml
Model: LLaMA-2 7B (7 billion parameters)
Hardware: RTX 4090 24GB
Method: QLoRA

Recommended Hyperparameters:
  learning_rate: 2e-4
  per_device_train_batch_size: 4
  gradient_accumulation_steps: 4
  num_train_epochs: 3
  lr_scheduler_type: 'cosine'
  warmup_ratio: 0.03
  weight_decay: 0.01
  max_grad_norm: 1.0
  bf16: true
  optim: 'paged_adamw_8bit'

LoRA Configuration:
  r: 16
  lora_alpha: 32
  lora_dropout: 0.05
  target_modules: ['q_proj', 'v_proj']

Result:
  - Training time: 6 hours
  - Peak memory: 22GB
  - Final loss: 0.85
  - Validation perplexity: 12.3
```

## Related Skills

- **model-selection**: Chooses appropriate base models
- **memory-management**: Optimizes memory for batch sizes
- **gpu-optimization**: Ensures efficient GPU utilization

This skill ensures optimal hyperparameters for successful LLM training and fine-tuning.
