---
description: Design and implement complete LLM training pipeline from scratch with PyTorch, HuggingFace, and distributed training
---

Design and implement a comprehensive training pipeline for Large Language Models from scratch.

## Process

Follow these steps:

1. **Analyze Requirements**: Understand training goals and constraints
   - Model size and architecture requirements
   - Dataset availability and quality
   - Compute resources (GPUs, memory, time)
   - Target performance metrics
   - Budget constraints
   - Review existing codebase if applicable

2. **Launch Training Expert**: Use the `llm-plugin:llm-training-expert` agent to:
   - Design model architecture or select base architecture
   - Plan dataset preparation and preprocessing pipeline
   - Configure distributed training strategy (DDP, FSDP, DeepSpeed)
   - Design training loop with optimizations
   - Set up monitoring and checkpointing
   - Plan evaluation strategy
   - Design troubleshooting approaches

3. **Review and Optimize** (if needed): If optimization is required, use the `llm-plugin:model-optimization-expert` agent to:
   - Profile training performance
   - Identify bottlenecks
   - Optimize memory usage
   - Improve training speed
   - Reduce costs

4. **Implementation Guide**: Provide:
   - Complete training script with PyTorch/HuggingFace
   - Dataset preparation code
   - Distributed training configuration
   - Monitoring and logging setup
   - Checkpoint management
   - Evaluation scripts

## Output

Present a comprehensive training plan including:

### Model Architecture
- Architecture selection (GPT, Llama, custom)
- Model size and parameter count
- Architecture modifications
- Tokenizer configuration
- Initialization strategy
- Why this architecture fits the requirements

### Dataset Configuration
- Data sources and collection strategy
- Preprocessing and cleaning pipeline
- Tokenization approach
- Dataset statistics (size, tokens, diversity)
- Train/validation split strategy
- Data loading optimization
- Streaming vs in-memory strategy

### Training Configuration
- Distributed training strategy (DDP, FSDP, DeepSpeed)
- Number of GPUs and nodes
- Batch size (per-device and effective)
- Gradient accumulation steps
- Mixed precision settings (BF16/FP16)
- Optimizer (AdamW, Lion, etc.) and settings
- Learning rate and schedule
- Warmup steps and strategy
- Gradient clipping
- Training duration (steps/epochs)

### Training Script
Complete PyTorch training code including:
```python
# Model initialization
# DataLoader setup
# Distributed training setup
# Training loop with gradient accumulation
# Mixed precision training
# Checkpointing
# Logging and monitoring
# Evaluation
```

### Optimization Techniques
- Flash Attention integration
- Gradient checkpointing
- Memory optimization strategies
- Communication optimization
- Data loading optimization
- Checkpoint optimization

### Monitoring Setup
- Training metrics to track
- Logging configuration (TensorBoard, W&B)
- Sample generation during training
- Gradient and weight monitoring
- Resource utilization tracking
- Alert conditions

### Checkpoint Strategy
- Checkpoint frequency
- Checkpoint storage location
- Resume-from-checkpoint logic
- Checkpoint cleanup policy
- Best model saving criteria
- Storage requirements

### Evaluation Strategy
- Validation frequency
- Evaluation metrics (loss, perplexity, benchmarks)
- Sample generation for qualitative assessment
- Benchmark tasks (if applicable)
- Early stopping criteria

### Compute Requirements
- GPU/TPU requirements
- Memory requirements per GPU
- Storage requirements
- Network bandwidth needs
- Estimated training time
- Cost estimation
- Alternative configurations for different budgets

### Troubleshooting Guide
- OOM errors and solutions
- Training instability (NaN/Inf losses)
- Slow training speed
- Data loading bottlenecks
- Checkpoint issues
- Distributed training problems
- Debugging strategies

## Examples

### Train Small Language Model (1B)
```
/train-model

Train a 1B parameter GPT-style model on programming code dataset
with single GPU (A100 40GB), targeting code generation tasks
```

### Train Medium Model with Multi-GPU
```
/train-model

Train a 7B Llama-style model from scratch on diverse text corpus
using 4x A100 GPUs with FSDP, targeting general language understanding
```

### Train Domain-Specific Model
```
/train-model

Train a 3B parameter model specialized in medical literature
using custom medical corpus, multi-GPU setup with DeepSpeed
```

### Continued Pre-training
```
/train-model

Continue pre-training Llama-2-7B on legal documents corpus
to create legal domain expert model
```

## Training Configurations Applied

### Small Model (1B)
- Single GPU or 2-4 GPUs with DDP
- Batch size: 32-64 with gradient accumulation
- Mixed precision: BF16
- Flash Attention: Enabled
- Training time: 1-2 weeks on single A100

### Medium Model (7B)
- 4-8 GPUs with FSDP or DeepSpeed ZeRO-2
- Batch size: 256-512 (accumulated)
- Mixed precision: BF16
- Flash Attention: Required
- Gradient checkpointing: Enabled
- Training time: 2-4 weeks on 4-8 A100s

### Large Model (13B+)
- 8-32 GPUs with DeepSpeed ZeRO-3 or FSDP
- Batch size: 512-1024 (accumulated)
- 3D parallelism (data, tensor, pipeline)
- CPU offloading if needed
- Training time: Months on large clusters

## Best Practices Applied

- **Data Quality**: Clean, diverse, high-quality training data
- **Gradient Clipping**: Prevent training instabilities
- **Warmup**: Gradual learning rate increase
- **Monitoring**: Continuous metric tracking
- **Checkpointing**: Frequent saves for recovery
- **Evaluation**: Regular validation checks
- **Reproducibility**: Fixed seeds and documented configs
- **Documentation**: Clear training logs and notes

## Integration with Other Components

- **Data Pipeline**: Prepare datasets with proper preprocessing
- **Model Evaluation**: Test trained model on benchmarks
- **Fine-tuning**: Use trained model as base for fine-tuning
- **Deployment**: Export trained model for inference

Provide production-ready training implementations with complete code, configuration, and documentation.
