---
description: Fine-tune pre-trained LLMs using LoRA, QLoRA, PEFT, TRL, and Unsloth for efficient task-specific adaptation
---

Design and implement an efficient fine-tuning pipeline for adapting pre-trained Large Language Models to specific tasks.

## Process

Follow these steps:

1. **Analyze Requirements**: Understand fine-tuning goals and constraints
   - Target task and dataset
   - Base model selection criteria
   - Compute resources available
   - Quality vs cost trade-offs
   - Timeline constraints
   - Review existing codebase if applicable

2. **Launch Fine-tuning Expert**: Use the `llm-finetuning-expert` agent to:
   - Select appropriate base model
   - Choose fine-tuning method (LoRA, QLoRA, full fine-tuning)
   - Configure PEFT parameters
   - Design dataset preparation pipeline
   - Set up training with TRL/Unsloth
   - Configure evaluation strategy
   - Plan inference and deployment

3. **Optimize if Needed**: If optimization is required, use the `model-optimization-expert` agent to:
   - Optimize memory usage with quantization
   - Speed up training with Unsloth
   - Optimize inference performance
   - Reduce deployment costs

4. **Implementation Guide**: Provide:
   - Complete fine-tuning script with PEFT/TRL
   - Dataset preparation and formatting
   - LoRA/QLoRA configuration
   - Training and evaluation code
   - Inference examples
   - Deployment preparation

## Output

Present a comprehensive fine-tuning plan including:

### Base Model Selection
- Model choice (Llama, Mistral, GPT, etc.)
- Model size (7B, 13B, 70B)
- Rationale for selection
- Pre-trained capabilities assessment
- License considerations
- Quantization requirements

### Fine-tuning Method
- Method selection (LoRA, QLoRA, full fine-tuning, Unsloth)
- Justification for the choice
- Expected outcomes
- Resource requirements
- Trade-offs analysis

### PEFT Configuration
For LoRA/QLoRA:
```python
lora_config = {
    "r": 16,                    # LoRA rank
    "lora_alpha": 32,           # LoRA scaling
    "lora_dropout": 0.05,       # Dropout
    "target_modules": [...],    # Layers to adapt
    "bias": "none",             # Bias training
    "task_type": "CAUSAL_LM"    # Task type
}
```
- Rationale for each parameter
- Alternative configurations
- Memory impact
- Performance impact

### Dataset Configuration
- Dataset source and format
- Task type (instruction, chat, completion)
- Data preprocessing steps
- Prompt template design
- Train/validation split
- Dataset statistics
- Quality assessment
- Example formatted samples

### Training Configuration
- Optimizer and learning rate
- Batch size and gradient accumulation
- Number of epochs
- Warmup steps
- Weight decay
- Learning rate schedule
- Mixed precision settings
- Gradient clipping
- Maximum sequence length

### Training Script
Complete fine-tuning code including:
```python
# Model loading (with quantization if QLoRA)
# PEFT configuration
# Dataset preparation
# Trainer setup (SFTTrainer, DPOTrainer, etc.)
# Training execution
# Model saving
# Evaluation
```

### Unsloth Optimization (if applicable)
- FastLanguageModel setup
- Memory savings estimation
- Speed improvement estimation
- Compatible optimizations
- Configuration for 2x speedup

### Evaluation Strategy
- Evaluation metrics
- Benchmark tasks
- Qualitative assessment
- Comparison with base model
- A/B testing approach
- Success criteria

### Inference Setup
- Loading fine-tuned model
- Merging LoRA weights (if needed)
- Quantization for deployment
- Generation parameters
- Example inference code
- API integration

### Adapter Management
- Saving LoRA adapters separately
- Adapter versioning
- Merging strategies
- Multi-adapter serving
- Storage requirements

### Compute Requirements
- GPU requirements (VRAM)
- Training time estimation
- Storage needs
- Cost estimation
- Alternative configurations

### Quality Assurance
- Validation approach
- Benchmark comparison
- Edge case testing
- Bias and safety checks
- Output quality review

### Deployment Guide
- Model export format
- Serving infrastructure
- Inference optimization
- Scaling strategy
- Monitoring setup

## Examples

### Instruction Fine-tuning with LoRA
```
/fine-tune-model

Fine-tune Llama-3-8B on custom instruction dataset using LoRA
for task-specific question answering with 16GB GPU
```

### Chat Model with QLoRA
```
/fine-tune-model

Create chat assistant by fine-tuning Mistral-7B with QLoRA
on conversational dataset, optimized for consumer GPU (24GB)
```

### Domain-Specific Model with Unsloth
```
/fine-tune-model

Fine-tune Llama-2-7B on legal documents using Unsloth for 2x speedup,
create domain expert for legal contract analysis
```

### Code Generation Fine-tuning
```
/fine-tune-model

Fine-tune CodeLlama-13B on proprietary codebase using QLoRA
for company-specific code generation and completion
```

### RLHF Alignment
```
/fine-tune-model

Apply DPO (Direct Preference Optimization) to fine-tune Llama-3-8B
using preference dataset for better alignment and safety
```

## Fine-tuning Methods Applied

### LoRA (Low-Rank Adaptation)
- Parameter-efficient (0.1-1% trainable parameters)
- Fast training (hours instead of days)
- Moderate GPU requirements (16GB+)
- Good quality preservation
- Easy adapter management
- Use cases: Most fine-tuning tasks

### QLoRA (Quantized LoRA)
- 4-bit base model quantization
- Minimal GPU requirements (8-16GB)
- Slight quality trade-off
- Can fine-tune 70B on consumer GPU
- Use cases: Limited GPU memory

### Unsloth
- 2x faster than standard LoRA
- 50% less memory usage
- Compatible with LoRA/QLoRA
- No quality degradation
- Use cases: Speed optimization

### Full Fine-tuning
- Train all parameters
- Best quality potential
- High GPU requirements
- Longer training time
- Use cases: Maximum performance needed

## Best Practices Applied

- **Start Small**: Begin with smaller models and LoRA rank
- **High-Quality Data**: 1000+ diverse, clean examples
- **Prevent Overfitting**: 1-3 epochs, monitor validation
- **Learning Rate**: Lower than pre-training (1e-4 to 5e-5)
- **Evaluation**: Test on held-out data and benchmarks
- **Prompt Engineering**: Consistent templates in training data
- **Gradient Clipping**: Stabilize training
- **Save Frequently**: Regular checkpoint saving
- **Document Everything**: Track configurations and results

## Fine-tuning Scenarios

### Task-Specific Adaptation
- Classification, summarization, extraction
- Custom instruction following
- Domain-specific language understanding
- Code generation for specific frameworks

### Chat and Instruction Models
- Conversational AI assistants
- Customer support bots
- Educational tutors
- Multi-turn dialogue systems

### Domain Specialization
- Medical, legal, financial domains
- Technical documentation
- Scientific literature
- Industry-specific knowledge

### Alignment and Safety
- RLHF for better alignment
- DPO for preference learning
- Safety filtering
- Bias reduction

## Integration with Other Components

- **Base Model Training**: Use custom pre-trained models
- **Deployment**: Deploy fine-tuned models with optimizations
- **Optimization**: Quantize and optimize for production
- **Evaluation**: Test on comprehensive benchmarks

Provide production-ready fine-tuning implementations with complete code, detailed configurations, and clear evaluation strategies.
