# LLM Plugin

Comprehensive toolkit for Large Language Model training, fine-tuning, and deployment covering PyTorch, HuggingFace, Unsloth, vLLM, and Ollama.

## Features

### Agents

- **llm-training-expert**: Expert in training LLMs from scratch using PyTorch, HuggingFace Transformers, and distributed training strategies (FSDP, DeepSpeed)
- **llm-finetuning-expert**: Expert in fine-tuning LLMs using PEFT, LoRA, QLoRA, TRL, and Unsloth for efficient parameter-efficient training
- **llm-deployment-expert**: Expert in deploying LLMs for production inference using vLLM, Ollama, TGI with optimizations
- **model-optimization-expert**: Expert in optimizing LLMs for performance, memory efficiency, and quality using quantization, pruning, and distillation

### Commands

- `/train-model`: Design and implement complete LLM training pipeline from scratch
- `/fine-tune-model`: Fine-tune pre-trained LLMs using LoRA, QLoRA, PEFT, TRL, and Unsloth
- `/deploy-model`: Deploy LLMs for production inference with vLLM, Ollama, or TGI

### Skills

- **training-best-practices**: Auto-invoked when working on LLM training code to ensure stability, efficiency, and quality
- **model-optimization**: Auto-invoked when optimizing LLM inference to ensure best practices for performance

## Usage

### Train a Model from Scratch

```
/train-model

Train a 1B parameter GPT-style model on programming code dataset
with single GPU (A100 40GB), targeting code generation tasks
```

```
/train-model

Train a 7B Llama-style model from scratch on diverse text corpus
using 4x A100 GPUs with FSDP, targeting general language understanding
```

```
/train-model

Continue pre-training Llama-2-7B on legal documents corpus
to create legal domain expert model
```

### Fine-tune a Pre-trained Model

```
/fine-tune-model

Fine-tune Llama-3-8B on custom instruction dataset using LoRA
for task-specific question answering with 16GB GPU
```

```
/fine-tune-model

Create chat assistant by fine-tuning Mistral-7B with QLoRA
on conversational dataset, optimized for consumer GPU (24GB)
```

```
/fine-tune-model

Fine-tune Llama-2-7B on legal documents using Unsloth for 2x speedup,
create domain expert for legal contract analysis
```

```
/fine-tune-model

Apply DPO (Direct Preference Optimization) to fine-tune Llama-3-8B
using preference dataset for better alignment and safety
```

### Deploy a Model for Inference

```
/deploy-model

Deploy Llama-3-8B with vLLM on 2x A100 GPUs for high-throughput
API service with <1s p95 latency and 100+ concurrent users
```

```
/deploy-model

Deploy Mistral-7B-Instruct locally with Ollama for development
and testing, optimized for MacBook Pro with M3 chip
```

```
/deploy-model

Deploy quantized Llama-3-8B (4-bit AWQ) on edge device with
limited resources, targeting <2s latency for chat application
```

```
/deploy-model

Deploy Llama-2-13B on AWS with spot instances, autoscaling,
and aggressive quantization to minimize costs while maintaining quality
```

### Use Agents Directly

Invoke specialized agents for focused work:

- "Use llm-training-expert to design training pipeline for 3B parameter model"
- "Use llm-finetuning-expert to configure LoRA fine-tuning for code generation"
- "Use llm-deployment-expert to set up vLLM deployment with autoscaling"
- "Use model-optimization-expert to apply AWQ quantization and benchmark"

## Technologies Covered

### Training Frameworks
- **PyTorch**: Core training framework (torch.nn, torch.optim, torch.distributed)
- **HuggingFace Transformers**: Model architectures and training utilities
- **HuggingFace Datasets**: Dataset loading and preprocessing
- **HuggingFace Accelerate**: Distributed training abstraction

### Distributed Training
- **FSDP**: PyTorch native Fully Sharded Data Parallel
- **DeepSpeed**: Memory-efficient distributed training with ZeRO
- **DDP**: Basic Data Parallel training
- **Megatron-LM**: Large-scale model parallelism

### Fine-tuning Methods
- **PEFT**: Parameter-Efficient Fine-Tuning library
- **LoRA**: Low-Rank Adaptation for efficient fine-tuning
- **QLoRA**: 4-bit quantized LoRA for consumer GPUs
- **TRL**: Transformer Reinforcement Learning (SFT, DPO, PPO)
- **Unsloth**: 2x faster fine-tuning and inference

### Inference Servers
- **vLLM**: High-throughput serving with PagedAttention
- **Ollama**: Local deployment and easy model management
- **TGI**: HuggingFace's Text Generation Inference
- **TensorRT-LLM**: NVIDIA's optimized inference engine
- **llama.cpp**: Efficient CPU/Metal inference

### Optimization Techniques
- **Quantization**: GPTQ, AWQ, GGUF, bitsandbytes (4-bit, 8-bit)
- **Flash Attention**: Fast and memory-efficient attention
- **PagedAttention**: vLLM's memory management for KV cache
- **Gradient Checkpointing**: Memory optimization for training
- **Mixed Precision**: BF16/FP16 training and inference

### Model Architectures
- **Llama 2/3/4**: Meta's open-source models (7B, 13B, 70B)
- **Mistral/Mixtral**: High-performance open models
- **GPT-NeoX/Pythia**: Open-source GPT alternatives
- **Gemma**: Google's open models
- **Phi**: Microsoft's small language models
- **Qwen**: Alibaba's multilingual models

## Patterns & Best Practices

### Training from Scratch
- Model architecture design and selection
- Dataset preparation and quality control
- Distributed training strategies (FSDP, DeepSpeed)
- Mixed precision training (BF16)
- Gradient checkpointing and Flash Attention
- Learning rate scheduling with warmup
- Checkpoint management and resumption
- Monitoring with Weights & Biases / TensorBoard
- Validation and sample generation
- Troubleshooting OOM and training instabilities

### Fine-tuning
- LoRA configuration (rank, alpha, target modules)
- QLoRA for memory-constrained GPUs
- Instruction dataset formatting
- Chat template design
- SFTTrainer for supervised fine-tuning
- DPO/RLHF for alignment
- Unsloth for 2x speed improvement
- Preventing overfitting (1-3 epochs)
- Adapter merging and management
- Evaluation on benchmarks

### Deployment
- Model quantization (AWQ, GPTQ, GGUF)
- vLLM configuration and tuning
- Ollama Modelfile creation
- TGI deployment with Docker/Kubernetes
- API design (OpenAI-compatible)
- Continuous batching and request scheduling
- Streaming responses
- Autoscaling and load balancing
- Monitoring latency and throughput
- Cost optimization strategies

### Optimization
- Quantization method selection (AWQ > GPTQ for quality)
- Flash Attention integration
- KV cache optimization
- Speculative decoding
- Prefix caching for system prompts
- Hardware-specific optimizations
- Benchmarking and profiling
- Quality preservation techniques

## Example Workflows

### Train and Deploy a Custom Model

1. **Train from scratch**
   ```
   /train-model
   Train 3B parameter model on domain-specific corpus with 8x A100 GPUs
   ```

2. **Optimize for deployment**
   ```
   Use model-optimization-expert to apply 4-bit AWQ quantization
   ```

3. **Deploy with vLLM**
   ```
   /deploy-model
   Deploy quantized model with vLLM for high-throughput API service
   ```

### Fine-tune and Optimize for Edge

1. **Fine-tune with QLoRA**
   ```
   /fine-tune-model
   Fine-tune Llama-3-8B with QLoRA on custom instructions
   ```

2. **Convert to GGUF**
   ```
   Use model-optimization-expert to convert to GGUF Q4_K_M for edge deployment
   ```

3. **Deploy with Ollama**
   ```
   /deploy-model
   Deploy GGUF model with Ollama on edge device with 8GB RAM
   ```

### Build a Production Chat Service

1. **Fine-tune for chat**
   ```
   /fine-tune-model
   Create chat assistant by fine-tuning Mistral-7B with conversation dataset
   ```

2. **Optimize inference**
   ```
   Use model-optimization-expert to apply optimizations for low latency
   ```

3. **Deploy with scaling**
   ```
   /deploy-model
   Deploy with vLLM, autoscaling, and monitoring for chat service
   ```

## Integration with Other Plugins

- **infra-plugin**: Deploy training clusters and inference infrastructure on Kubernetes
- **cicd-plugin**: Automate model training, evaluation, and deployment pipelines
- **database-plugin**: Store training data, model metadata, and inference logs
- **backend-plugin**: Build APIs around LLM inference endpoints

## Best Practices

### Training
- Use BF16 mixed precision for stability
- Enable gradient checkpointing for large models
- Apply Flash Attention for memory efficiency
- Use FSDP or DeepSpeed for models >7B
- Implement proper warmup and learning rate scheduling
- Monitor gradient norms and losses
- Save frequent checkpoints
- Generate samples during training
- Validate on diverse examples

### Fine-tuning
- Start with smaller LoRA rank (8-16)
- Use QLoRA for limited GPU memory
- Curate high-quality datasets (1000+ examples)
- Avoid overfitting (1-3 epochs)
- Use appropriate learning rates (1e-4 to 5e-5)
- Test on held-out validation set
- Compare with base model performance
- Consider Unsloth for 2x speedup

### Deployment
- Apply quantization (4-bit AWQ recommended)
- Use vLLM for high-throughput services
- Enable continuous batching
- Configure appropriate context length
- Implement streaming responses
- Monitor latency (TTFT, TPOT) and throughput
- Set up autoscaling based on metrics
- Optimize cost with spot instances
- Implement proper error handling and retries

### Optimization
- Always enable Flash Attention
- Use AWQ over GPTQ for better quality
- Benchmark before and after optimization
- Test quality on downstream tasks
- Profile memory and compute usage
- Use prefix caching for system prompts
- Optimize generation parameters
- Monitor production metrics

## Advanced Topics

### Distributed Training Strategies
- Data Parallelism (DDP) for multi-GPU
- Fully Sharded Data Parallel (FSDP) for large models
- DeepSpeed ZeRO-1/2/3 stages
- Pipeline parallelism for very large models
- 3D parallelism (data + tensor + pipeline)
- Gradient accumulation strategies
- Communication optimization

### RLHF and Alignment
- Reward model training
- PPO (Proximal Policy Optimization)
- DPO (Direct Preference Optimization)
- Preference dataset creation
- KL divergence penalty tuning
- Safety and alignment evaluation
- Red teaming strategies

### Quantization Techniques
- Post-training quantization (PTQ)
- Quantization-aware training (QAT)
- GPTQ (4-bit GPU quantization)
- AWQ (activation-aware quantization)
- SmoothQuant (mixed precision)
- GGUF formats for CPU inference
- Calibration dataset selection

### Production Infrastructure
- Multi-region deployment
- Request routing and load balancing
- A/B testing frameworks
- Canary deployments
- Blue-green deployments
- Feature flags and gradual rollouts
- Cost allocation and tracking
- Compliance and audit trails

### Model Evaluation
- Perplexity and language modeling metrics
- Benchmark suites (MMLU, HellaSwag, TruthfulQA)
- Task-specific evaluations
- Human evaluation protocols
- A/B testing methodologies
- Quality monitoring in production
- Regression detection

## Compute Requirements

### Training from Scratch

**Small Model (1B parameters)**
- GPU: 1x A100 40GB or 4090 24GB
- Training time: 1-2 weeks
- Method: Single GPU with gradient accumulation

**Medium Model (7B parameters)**
- GPU: 4-8x A100 80GB
- Training time: 2-4 weeks
- Method: FSDP or DeepSpeed ZeRO-2

**Large Model (70B+ parameters)**
- GPU: 32-128x A100 80GB
- Training time: 1-3 months
- Method: DeepSpeed ZeRO-3 with 3D parallelism

### Fine-tuning

**LoRA Fine-tuning**
- GPU: 1x 16GB+ (e.g., V100, 4090)
- Training time: Hours to days
- Models: Up to 13B parameters

**QLoRA Fine-tuning**
- GPU: 1x 8-16GB (e.g., 3090, 4060 Ti)
- Training time: Hours to days
- Models: Up to 70B parameters

### Inference

**Production (vLLM)**
- 7B model: 1x A10G (24GB) or T4 (16GB) with quantization
- 13B model: 1x A100 (40GB) or 2x T4
- 70B model: 2-4x A100 (80GB) with tensor parallelism

**Local/Edge (Ollama)**
- 7B Q4 model: 6-8GB RAM
- 13B Q4 model: 10-12GB RAM
- Supports CPU, NVIDIA, AMD, and Apple Silicon

## Cost Optimization

### Training
- Use spot instances (60-80% savings)
- Optimize batch size for GPU utilization
- Use gradient accumulation vs larger GPUs
- Monitor and shut down idle resources
- Consider cloud vs on-premise cost analysis

### Fine-tuning
- Use LoRA/QLoRA instead of full fine-tuning
- Leverage Unsloth for 2x speed improvement
- Use smaller base models when possible
- Optimize dataset size (quality over quantity)
- Use spot instances for training

### Inference
- Apply aggressive quantization (4-bit)
- Right-size GPU instances (match model size)
- Use autoscaling to match demand
- Implement request batching
- Consider multi-tenancy
- Use spot/preemptible instances
- Optimize context length
- Monitor cost per token

## Getting Started

1. **Choose your workflow**:
   - Training from scratch? Use `/train-model`
   - Fine-tuning existing model? Use `/fine-tune-model`
   - Deploying model? Use `/deploy-model`

2. **Consult the experts**:
   - Training questions? Invoke `llm-training-expert`
   - Fine-tuning help? Invoke `llm-finetuning-expert`
   - Deployment guidance? Invoke `llm-deployment-expert`
   - Performance issues? Invoke `model-optimization-expert`

3. **Let skills guide you**:
   - Skills auto-activate when editing training or deployment code
   - Follow best practices automatically
   - Prevent common mistakes

4. **Iterate and optimize**:
   - Start with baseline implementation
   - Measure performance and quality
   - Apply optimizations incrementally
   - Benchmark and validate improvements

Start building, training, and deploying world-class Large Language Models with comprehensive expert guidance and best practices!
