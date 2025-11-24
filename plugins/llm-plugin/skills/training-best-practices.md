---
name: training-best-practices
description: Auto-invoked when working on LLM training or fine-tuning code to ensure best practices and prevent common issues
allowed-tools: Read, Grep, Glob
---

# LLM Training Best Practices

This skill provides guidance on training and fine-tuning Large Language Models to ensure quality, stability, and efficiency.

## When Active

This skill activates when you:
- Write or modify training scripts
- Configure model training parameters
- Set up distributed training
- Implement data loading pipelines
- Debug training issues
- Configure optimization settings

## Training Stability

### Gradient Management
- **Always use gradient clipping**: Set `max_grad_norm` to 1.0 for LLM training
- **Monitor gradient norms**: Log gradient norms to detect instabilities
- **Check for NaN/Inf**: Implement checks in training loop
- **Use gradient accumulation**: For larger effective batch sizes

```python
# Good: Gradient clipping
torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)

# Good: Gradient monitoring
grad_norm = torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
wandb.log({"grad_norm": grad_norm})

# Good: NaN detection
if torch.isnan(loss):
    logger.error("NaN loss detected, skipping update")
    optimizer.zero_grad()
    continue
```

### Learning Rate Management
- **Use warmup**: 1000-10000 steps for training from scratch, 10-100 for fine-tuning
- **Appropriate learning rates**:
  - Training from scratch: 1e-4 to 3e-4
  - Fine-tuning: 5e-6 to 5e-5
  - LoRA fine-tuning: 1e-4 to 5e-5
- **Use cosine schedule**: Better than linear for most cases
- **Monitor learning rate**: Log current LR in each step

```python
# Good: Warmup + Cosine schedule
from transformers import get_cosine_schedule_with_warmup

scheduler = get_cosine_schedule_with_warmup(
    optimizer,
    num_warmup_steps=1000,
    num_training_steps=total_steps
)

# Good: Learning rate logging
wandb.log({"learning_rate": scheduler.get_last_lr()[0]})
```

### Mixed Precision Training
- **Prefer BF16 over FP16**: Better numerical stability
- **Use FP16 only if BF16 unavailable**: A100, H100, newer GPUs support BF16
- **Scale loss with FP16**: Use GradScaler for FP16 training
- **Monitor for underflow/overflow**: Check loss scale

```python
# Good: BF16 training
model = model.to(torch.bfloat16)
with torch.autocast(device_type="cuda", dtype=torch.bfloat16):
    loss = model(input_ids=batch["input_ids"], labels=batch["labels"]).loss

# Good: FP16 with scaler
scaler = torch.cuda.amp.GradScaler()
with torch.autocast(device_type="cuda", dtype=torch.float16):
    loss = model(input_ids=batch["input_ids"], labels=batch["labels"]).loss
scaler.scale(loss).backward()
scaler.step(optimizer)
scaler.update()
```

## Memory Optimization

### Always Enable These
- **Gradient checkpointing**: For models >1B parameters
- **Flash Attention**: 2-3x memory reduction for attention
- **Mixed precision**: BF16 reduces memory by 50%
- **Gradient accumulation**: Effective large batch without OOM

```python
# Good: Memory optimizations
model.gradient_checkpointing_enable()

# Flash Attention 2
from transformers import AutoModelForCausalLM
model = AutoModelForCausalLM.from_pretrained(
    "model_name",
    attn_implementation="flash_attention_2",
    torch_dtype=torch.bfloat16
)

# Gradient accumulation
for step, batch in enumerate(dataloader):
    loss = model(**batch).loss
    loss = loss / gradient_accumulation_steps
    loss.backward()

    if (step + 1) % gradient_accumulation_steps == 0:
        optimizer.step()
        optimizer.zero_grad()
```

### Distributed Training
- **Use FSDP for models >7B**: Better than DDP
- **DeepSpeed ZeRO-3 for very large models**: >70B parameters
- **Configure sharding strategy**: FULL_SHARD for maximum memory savings
- **CPU offload if needed**: Trade memory for speed

```python
# Good: FSDP configuration
from torch.distributed.fsdp import FullyShardedDataParallel as FSDP
from torch.distributed.fsdp import ShardingStrategy

model = FSDP(
    model,
    sharding_strategy=ShardingStrategy.FULL_SHARD,
    mixed_precision=mixed_precision_policy,
    device_id=torch.cuda.current_device(),
)
```

## Data Loading Best Practices

### Dataset Preparation
- **Tokenize offline when possible**: Faster training
- **Use streaming for large datasets**: Datasets >100GB
- **Shuffle thoroughly**: Use large buffer for streaming
- **Pack sequences efficiently**: Concatenate documents to max_length
- **Validate data quality**: Sample and inspect

```python
# Good: Offline tokenization
tokenized_dataset = dataset.map(
    tokenize_function,
    batched=True,
    num_proc=8,
    remove_columns=dataset.column_names,
)
tokenized_dataset.save_to_disk("tokenized_data")

# Good: Streaming large datasets
from datasets import load_dataset
dataset = load_dataset("large_dataset", streaming=True)
dataset = dataset.shuffle(buffer_size=10000)

# Good: Sequence packing
def pack_sequences(examples):
    concatenated = {k: sum(examples[k], []) for k in examples.keys()}
    total_length = len(concatenated[list(examples.keys())[0]])
    # Pack into max_length chunks
    return {
        k: [t[i:i+max_length] for i in range(0, total_length, max_length)]
        for k, t in concatenated.items()
    }
```

### DataLoader Configuration
- **Use multiple workers**: 4-8 workers for CPU preprocessing
- **Pin memory**: Faster GPU transfer
- **Prefetch**: Overlap data loading with computation
- **Monitor data loading time**: Should be <5% of step time

```python
# Good: DataLoader settings
dataloader = DataLoader(
    dataset,
    batch_size=batch_size,
    num_workers=8,
    pin_memory=True,
    prefetch_factor=2,
)
```

## Hyperparameter Selection

### Optimizer Configuration
```python
# Good: AdamW settings for LLMs
optimizer = torch.optim.AdamW(
    model.parameters(),
    lr=2e-4,              # 1e-4 to 3e-4 for training, lower for fine-tuning
    betas=(0.9, 0.95),    # Standard for LLMs
    weight_decay=0.1,     # L2 regularization
    eps=1e-8              # Numerical stability
)
```

### Batch Size Guidelines
- **Training from scratch**: As large as possible (256-2048 effective)
- **Fine-tuning**: 16-128 effective batch size
- **Use gradient accumulation**: Simulate larger batches
- **Consider micro-batch size**: 1-4 per GPU for large models

### Sequence Length
- **Use model's max context**: For training from scratch
- **Shorter for fine-tuning**: 512-2048 often sufficient
- **Pad efficiently**: Use DataCollator with padding
- **Monitor average length**: Avoid excessive padding

## Checkpoint Management

### Save Frequently
```python
# Good: Regular checkpointing
if (step + 1) % checkpoint_every == 0:
    checkpoint_dir = f"checkpoint-{step+1}"
    model.save_pretrained(checkpoint_dir)
    tokenizer.save_pretrained(checkpoint_dir)

    # Save optimizer and scheduler state
    torch.save({
        'optimizer': optimizer.state_dict(),
        'scheduler': scheduler.state_dict(),
        'step': step,
    }, os.path.join(checkpoint_dir, "training_state.pt"))
```

### Resume from Checkpoint
```python
# Good: Resume logic
if resume_from_checkpoint:
    model.load_pretrained(checkpoint_dir)
    state = torch.load(os.path.join(checkpoint_dir, "training_state.pt"))
    optimizer.load_state_dict(state['optimizer'])
    scheduler.load_state_dict(state['scheduler'])
    start_step = state['step'] + 1
```

### Best Model Saving
- **Track validation metric**: Save when metric improves
- **Keep best K checkpoints**: Delete older ones
- **Save separately from regular checkpoints**: Don't overwrite

## Monitoring and Logging

### Essential Metrics
```python
# Log these every step
metrics = {
    "train/loss": loss.item(),
    "train/perplexity": torch.exp(loss).item(),
    "train/learning_rate": scheduler.get_last_lr()[0],
    "train/grad_norm": grad_norm,
    "train/step": step,
}

# Log these periodically
if step % 100 == 0:
    metrics.update({
        "train/tokens_per_sec": tokens_per_second,
        "train/gpu_memory_allocated": torch.cuda.memory_allocated() / 1e9,
        "train/gpu_memory_reserved": torch.cuda.memory_reserved() / 1e9,
    })

wandb.log(metrics)
```

### Sample Generation
- **Generate samples during training**: Every 1000 steps
- **Use fixed prompts**: Compare quality over time
- **Log to experiment tracker**: WandB, TensorBoard
- **Inspect for degradation**: Quality check

```python
# Good: Sample generation
if (step + 1) % 1000 == 0:
    model.eval()
    with torch.no_grad():
        prompts = ["Once upon a time", "The meaning of life is"]
        for prompt in prompts:
            output = model.generate(
                tokenizer(prompt, return_tensors="pt").input_ids.cuda(),
                max_length=100,
                do_sample=True,
                top_p=0.9,
            )
            text = tokenizer.decode(output[0])
            wandb.log({f"samples/{prompt}": wandb.Html(text)})
    model.train()
```

## Common Issues and Solutions

### Out of Memory (OOM)
1. Enable gradient checkpointing
2. Reduce batch size, increase accumulation
3. Use FSDP or DeepSpeed
4. Reduce sequence length
5. Use quantization (8-bit optimizers)
6. CPU offload optimizer states

### NaN/Inf Losses
1. Check learning rate (may be too high)
2. Use gradient clipping
3. Switch to BF16 from FP16
4. Check data for NaN values
5. Reduce batch size
6. Add loss scaling (FP16)

### Slow Training
1. Profile data loading (should be <5% of time)
2. Enable Flash Attention
3. Use larger batch size
4. Increase num_workers for DataLoader
5. Check GPU utilization (should be >80%)
6. Use compiled model (torch.compile)
7. Optimize communication (NCCL, faster interconnect)

### Poor Quality
1. Check data quality and diversity
2. Increase training duration
3. Tune learning rate
4. Check for overfitting (validation loss)
5. Increase model size if underfitting
6. Verify data preprocessing
7. Check for label/attention mask errors

## LoRA/PEFT Best Practices

### Configuration
```python
# Good: LoRA config
from peft import LoraConfig, TaskType, get_peft_model

peft_config = LoraConfig(
    r=16,                              # 8-64, higher for complex tasks
    lora_alpha=32,                     # Typically 2x rank
    lora_dropout=0.05,                 # 0.05-0.1
    target_modules=["q_proj", "v_proj", "k_proj", "o_proj"],  # All attention
    bias="none",
    task_type=TaskType.CAUSAL_LM
)

model = get_peft_model(model, peft_config)
model.print_trainable_parameters()  # Verify trainable params
```

### QLoRA Settings
```python
# Good: QLoRA with 4-bit quantization
from transformers import BitsAndBytesConfig

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",          # Normal Float 4
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True      # Additional savings
)

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    quantization_config=bnb_config,
    device_map="auto"
)
```

## Checklist

Before training:
- [ ] Data is clean, diverse, and properly formatted
- [ ] Tokenization is correct (pad token, eos token)
- [ ] Gradient checkpointing enabled for large models
- [ ] Flash Attention enabled if available
- [ ] Mixed precision configured (BF16 preferred)
- [ ] Gradient clipping set (max_norm=1.0)
- [ ] Learning rate warmup configured
- [ ] Checkpointing strategy defined
- [ ] Monitoring and logging set up
- [ ] Validation set prepared

During training:
- [ ] Monitor loss for NaN/Inf
- [ ] Check gradient norms regularly
- [ ] Validate GPU utilization >80%
- [ ] Inspect generated samples
- [ ] Monitor validation metrics
- [ ] Check data loading time <5%
- [ ] Watch for OOM errors

After training:
- [ ] Evaluate on held-out test set
- [ ] Benchmark on standard tasks
- [ ] Compare quality with baseline
- [ ] Test edge cases
- [ ] Document hyperparameters
- [ ] Save final model properly
- [ ] Merge LoRA adapters if needed

Use this guidance to ensure stable, efficient, and high-quality LLM training.
