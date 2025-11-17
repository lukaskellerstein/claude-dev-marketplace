---
name: hyperparameter-tuning
description: Automatically suggests and validates hyperparameters
allowed-tools: Read
---

# Hyperparameter Tuning Skill

Optimizes training hyperparameters based on model and dataset characteristics.

## Activation Triggers

This skill activates when:
- Starting new training or fine-tuning
- Poor convergence detected
- Validation loss increasing (overfitting)
- Training plateau detected
- Gradient explosion or vanishing
- User requests hyperparameter suggestions

## Responsibilities

1. **Suggest optimal hyperparameters**
2. **Detect training issues**
3. **Recommend adjustments**
4. **Monitor convergence**
5. **Prevent common pitfalls**

## Hyperparameter Categories

### 1. Learning Rate

The most critical hyperparameter for training success.

**Base Learning Rates by Model Size:**
```python
BASE_LEARNING_RATES = {
    'small': 5e-4,    # <1B parameters
    'medium': 2e-4,   # 1-10B parameters
    'large': 1e-4,    # 10-30B parameters
    'xlarge': 5e-5,   # >30B parameters
}

# For LoRA/QLoRA fine-tuning (can be higher)
LORA_LEARNING_RATES = {
    'small': 1e-3,
    'medium': 5e-4,
    'large': 2e-4,
    'xlarge': 1e-4,
}
```

**Learning Rate Scaling:**
```python
def suggest_learning_rate(model_size, batch_size, is_lora=False):
    """Suggest learning rate based on model size and batch size"""

    # Determine model category
    if model_size < 1e9:
        category = 'small'
    elif model_size < 10e9:
        category = 'medium'
    elif model_size < 30e9:
        category = 'large'
    else:
        category = 'xlarge'

    # Get base learning rate
    base_lr = LORA_LEARNING_RATES[category] if is_lora else BASE_LEARNING_RATES[category]

    # Apply linear scaling rule (optional)
    # For batch sizes significantly different from 32
    if batch_size != 32:
        scaled_lr = base_lr * (batch_size / 32)
        # Cap maximum learning rate
        scaled_lr = min(scaled_lr, base_lr * 2)
    else:
        scaled_lr = base_lr

    print(f"\n💡 Suggested Learning Rate: {scaled_lr:.2e}")
    print(f"   Model size: {model_size/1e9:.1f}B parameters")
    print(f"   Batch size: {batch_size}")
    print(f"   Type: {'LoRA' if is_lora else 'Full fine-tuning'}")

    # Provide range for experimentation
    lr_min = scaled_lr * 0.5
    lr_max = scaled_lr * 2
    print(f"\n📊 Recommended range: {lr_min:.2e} to {lr_max:.2e}")

    return scaled_lr
```

### 2. Batch Size

**Optimal Batch Size Selection:**
```python
def suggest_batch_size(model_size_gb, available_memory_gb, seq_length=2048):
    """Suggest optimal batch size based on available memory"""

    # Rough memory estimation
    # Model + Activations + Gradients + Optimizer states
    memory_per_sample = (seq_length / 2048) * 2  # GB per sample (rough estimate)

    # Available memory for batching (after model and overhead)
    available_for_batch = available_memory_gb - model_size_gb - 2  # 2GB buffer

    # Calculate max batch size
    max_batch_size = int(available_for_batch / memory_per_sample)

    # Prefer power of 2 for efficiency
    suggested_batch_sizes = [1, 2, 4, 8, 16, 32]
    suggested = max([bs for bs in suggested_batch_sizes if bs <= max_batch_size], default=1)

    print(f"\n💡 Suggested Batch Size: {suggested}")
    print(f"   Available memory: {available_memory_gb:.1f} GB")
    print(f"   Model size: {model_size_gb:.1f} GB")
    print(f"   Max possible: {max_batch_size}")

    # If batch size is very small, suggest gradient accumulation
    if suggested < 4:
        accumulation_steps = 8 // suggested
        effective_batch = suggested * accumulation_steps
        print(f"\n💡 Batch size is small, use gradient accumulation:")
        print(f"   per_device_train_batch_size = {suggested}")
        print(f"   gradient_accumulation_steps = {accumulation_steps}")
        print(f"   Effective batch size = {effective_batch}")

    return suggested
```

### 3. Learning Rate Schedule

**Scheduler Selection:**
```python
SCHEDULER_GUIDE = {
    'cosine': {
        'description': 'Gradual decay with warm restarts',
        'best_for': 'General purpose, most common',
        'warmup_ratio': 0.1,
        'recommendation': 'Default choice for most training'
    },
    'linear': {
        'description': 'Linear decay to zero',
        'best_for': 'Fine-tuning, short training',
        'warmup_ratio': 0.05,
        'recommendation': 'Good for fine-tuning tasks'
    },
    'polynomial': {
        'description': 'Polynomial decay',
        'best_for': 'Smooth decay needed',
        'warmup_ratio': 0.1,
        'recommendation': 'Alternative to cosine'
    },
    'constant_with_warmup': {
        'description': 'Constant after warmup',
        'best_for': 'When LR is already optimal',
        'warmup_ratio': 0.05,
        'recommendation': 'For continued training'
    }
}

def suggest_scheduler(training_type='full', num_epochs=3):
    """Suggest learning rate scheduler"""

    if training_type == 'fine-tuning' or num_epochs <= 3:
        scheduler = 'linear'
    else:
        scheduler = 'cosine'

    guide = SCHEDULER_GUIDE[scheduler]

    print(f"\n💡 Suggested LR Scheduler: {scheduler}")
    print(f"   {guide['description']}")
    print(f"   Best for: {guide['best_for']}")
    print(f"\n   Configuration:")
    print(f"   lr_scheduler_type = '{scheduler}'")
    print(f"   warmup_ratio = {guide['warmup_ratio']}")

    return scheduler, guide['warmup_ratio']
```

### 4. Warmup Steps

```python
def calculate_warmup_steps(total_steps, warmup_ratio=0.1):
    """Calculate optimal warmup steps"""

    warmup_steps = int(total_steps * warmup_ratio)

    # Minimum warmup
    warmup_steps = max(warmup_steps, 100)

    # Maximum warmup (don't warm up for more than 10% of training)
    warmup_steps = min(warmup_steps, total_steps // 10)

    print(f"\n💡 Suggested Warmup Steps: {warmup_steps}")
    print(f"   Total training steps: {total_steps}")
    print(f"   Warmup ratio: {warmup_ratio:.1%}")
    print(f"\n   Purpose: Prevents early training instability")

    return warmup_steps
```

### 5. Weight Decay

```python
def suggest_weight_decay(model_type='decoder'):
    """Suggest weight decay for regularization"""

    # Standard weight decay values
    if model_type == 'decoder':
        weight_decay = 0.01  # Common for LLMs
    elif model_type == 'encoder':
        weight_decay = 0.01
    else:
        weight_decay = 0.01

    print(f"\n💡 Suggested Weight Decay: {weight_decay}")
    print(f"   Standard L2 regularization")
    print(f"   Helps prevent overfitting")
    print(f"\n   For less regularization: 0.001")
    print(f"   For more regularization: 0.1")

    return weight_decay
```

### 6. Gradient Clipping

```python
def suggest_gradient_clipping():
    """Suggest gradient clipping value"""

    max_grad_norm = 1.0  # Standard value

    print(f"\n💡 Suggested Max Gradient Norm: {max_grad_norm}")
    print(f"   Prevents gradient explosion")
    print(f"   Essential for training stability")
    print(f"\n   max_grad_norm = {max_grad_norm}")

    return max_grad_norm
```

## Training Issue Detection

### 1. Convergence Monitoring

```python
def check_convergence(loss_history, window=10):
    """Check if training is converging properly"""

    if len(loss_history) < window:
        return "insufficient_data"

    recent_losses = loss_history[-window:]
    trend = sum(recent_losses[-5:]) / 5 - sum(recent_losses[:5]) / 5

    if trend > 0.1:
        print("⚠️ Loss is increasing!")
        print("💡 Possible issues:")
        print("   - Learning rate too high")
        print("   - Overfitting starting")
        print("   - Data quality issues")
        return "diverging"

    elif abs(trend) < 0.001:
        print("⚠️ Training plateau detected")
        print("💡 Consider:")
        print("   - Reducing learning rate")
        print("   - Checking if converged")
        print("   - Adding more diverse data")
        return "plateau"

    else:
        print("✅ Training converging normally")
        return "converging"
```

### 2. Gradient Issues

```python
def check_gradients(grad_norm_history, threshold=10.0):
    """Detect gradient explosion or vanishing"""

    if not grad_norm_history:
        return "no_data"

    recent_norm = grad_norm_history[-1]

    if recent_norm > threshold:
        print("🚨 Gradient explosion detected!")
        print(f"   Gradient norm: {recent_norm:.2f}")
        print("\n💡 Solutions:")
        print("   1. Reduce learning rate by 50%")
        print("   2. Increase gradient clipping")
        print("   3. Check data for outliers")
        return "explosion"

    elif recent_norm < 0.001:
        print("⚠️ Gradient vanishing detected!")
        print(f"   Gradient norm: {recent_norm:.6f}")
        print("\n💡 Solutions:")
        print("   1. Increase learning rate")
        print("   2. Check model initialization")
        print("   3. Verify data preprocessing")
        return "vanishing"

    else:
        return "normal"
```

### 3. Overfitting Detection

```python
def check_overfitting(train_loss, val_loss, threshold=0.1):
    """Detect overfitting based on train/val gap"""

    gap = val_loss - train_loss

    if gap > threshold:
        print("⚠️ Overfitting detected!")
        print(f"   Train loss: {train_loss:.4f}")
        print(f"   Val loss: {val_loss:.4f}")
        print(f"   Gap: {gap:.4f}")
        print("\n💡 Solutions:")
        print("   1. Enable early stopping")
        print("   2. Increase weight decay")
        print("   3. Add dropout")
        print("   4. Get more training data")
        print("   5. Reduce model size/rank")
        return True

    return False
```

## Dynamic Adjustments

### Auto-Adjust Learning Rate

```python
def auto_adjust_learning_rate(current_lr, convergence_status):
    """Automatically adjust learning rate based on training status"""

    adjustments = {
        'diverging': current_lr * 0.5,  # Reduce by 50%
        'plateau': current_lr * 0.1,     # Reduce by 90%
        'converging': current_lr         # No change
    }

    new_lr = adjustments.get(convergence_status, current_lr)

    if new_lr != current_lr:
        print(f"\n🔧 Auto-adjusting learning rate:")
        print(f"   Old LR: {current_lr:.2e}")
        print(f"   New LR: {new_lr:.2e}")
        print(f"   Reason: {convergence_status}")

    return new_lr
```

### Early Stopping

```python
def suggest_early_stopping(patience=3, threshold=0.001):
    """Suggest early stopping configuration"""

    print("\n💡 Early Stopping Configuration:")
    print(f"   early_stopping_patience = {patience}")
    print(f"   early_stopping_threshold = {threshold}")
    print("\n   Stops training when validation loss doesn't improve")
    print(f"   for {patience} consecutive evaluations")

    return {
        'patience': patience,
        'threshold': threshold
    }
```

## Comprehensive Recommendation

```python
def comprehensive_recommendation(
    model_size,
    available_memory_gb,
    is_lora=False,
    training_type='full',
    num_epochs=3
):
    """Provide comprehensive hyperparameter recommendations"""

    print("\n" + "="*60)
    print("   HYPERPARAMETER RECOMMENDATIONS")
    print("="*60)

    # Learning rate
    batch_size = suggest_batch_size(model_size * 4, available_memory_gb)
    lr = suggest_learning_rate(model_size, batch_size, is_lora)

    # Scheduler
    scheduler, warmup_ratio = suggest_scheduler(training_type, num_epochs)

    # Other params
    weight_decay = suggest_weight_decay()
    max_grad_norm = suggest_gradient_clipping()

    # Early stopping
    early_stopping = suggest_early_stopping()

    print("\n" + "="*60)
    print("   CONFIGURATION SUMMARY")
    print("="*60)
    print(f"""
TrainingArguments(
    learning_rate={lr},
    per_device_train_batch_size={batch_size},
    gradient_accumulation_steps=4,
    num_train_epochs={num_epochs},

    # Learning rate schedule
    lr_scheduler_type='{scheduler}',
    warmup_ratio={warmup_ratio},

    # Optimization
    weight_decay={weight_decay},
    max_grad_norm={max_grad_norm},

    # Mixed precision
    bf16=True,  # or fp16=True

    # Evaluation
    evaluation_strategy='steps',
    eval_steps=100,
    save_strategy='steps',
    save_steps=500,
)
    """)

    return {
        'learning_rate': lr,
        'batch_size': batch_size,
        'scheduler': scheduler,
        'warmup_ratio': warmup_ratio,
        'weight_decay': weight_decay,
        'max_grad_norm': max_grad_norm,
        'early_stopping': early_stopping
    }
```

## Best Practices

1. **Start conservative**: Begin with proven defaults
2. **Adjust gradually**: Small changes, observe results
3. **Monitor closely**: Watch loss curves and metrics
4. **Use warmup**: Essential for training stability
5. **Enable early stopping**: Prevent overfitting
6. **Log everything**: Track all hyperparameters
7. **Compare systematically**: A/B test changes
8. **Document findings**: Build knowledge base

## Common Patterns

**For Full Training:**
- LR: 1e-4 to 5e-4
- Batch size: As large as memory allows
- Scheduler: Cosine
- Warmup: 10% of training

**For LoRA Fine-tuning:**
- LR: 1e-4 to 1e-3 (higher than full training)
- Batch size: 4-8
- Scheduler: Linear or Cosine
- Warmup: 5-10% of training

**For QLoRA:**
- LR: 2e-4 to 5e-4
- Batch size: 1-4 (memory constrained)
- Use gradient accumulation
- Scheduler: Cosine

## Notes

- This skill provides intelligent defaults
- Monitors training for issues
- Suggests adjustments dynamically
- Works with other optimization skills
- Can be overridden by user preferences
