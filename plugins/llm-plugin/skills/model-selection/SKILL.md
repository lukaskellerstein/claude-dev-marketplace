---
name: model-selection
description: Master LLM model selection for specific tasks and hardware constraints. Use when choosing base models, comparing options, evaluating tradeoffs, planning deployment, optimizing for cost, selecting for inference, or matching models to requirements.
allowed-tools: Read
---

# Model Selection Skill

Recommend optimal LLM models based on task requirements, hardware constraints, and performance needs. Balance quality, speed, and cost for effective model deployment.

## When to Use This Skill

1. **Project Planning** - Choosing models for new projects
2. **Hardware Matching** - Fitting models to GPU capacity
3. **Task Optimization** - Selecting task-specific models
4. **Cost Analysis** - Balancing performance and cost
5. **Deployment Planning** - Choosing production models
6. **Inference Optimization** - Selecting efficient models
7. **Multi-Language Support** - Finding multilingual models
8. **Specialized Tasks** - Code, math, reasoning models
9. **Quantization Strategy** - Choosing quantized versions
10. **Comparison Analysis** - Evaluating model options
11. **Migration Planning** - Upgrading to better models
12. **Benchmark Review** - Understanding model capabilities
13. **License Compliance** - Checking usage terms
14. **Technology Stack** - Integrating with existing systems
15. **Scalability Planning** - Preparing for growth

## Quick Start

```python
def recommend_model(task: str, gpu_memory_gb: float):
    """Quick model recommendation"""
    
    if gpu_memory_gb < 12:
        # Consumer GPU
        if task == 'code':
            return 'codellama-7b-q4'
        return 'mistral-7b-q4'
    
    elif gpu_memory_gb < 24:
        # Professional GPU
        if task == 'code':
            return 'deepseek-coder-33b-q4'
        return 'mixtral-8x7b-q4'
    
    else:
        # Datacenter GPU
        if task == 'code':
            return 'codellama-34b'
        return 'llama-3-70b-int8'
```

## Model Categories

### Text Generation
```yaml
Quality-Focused:
  - llama-3-70b: Best overall performance
  - mixtral-8x22b: Excellent MoE architecture
  - qwen-72b: Strong multilingual support

Speed-Focused:
  - mistral-7b: Fastest 7B model
  - phi-3-mini: Ultra-fast 3.8B
  - llama-3-8b: Latest efficient model
```

### Code Generation
```yaml
Top-Tier:
  - codellama-34b: Best code model
  - deepseek-coder-33b: Excellent performance
  - starcoder-15b: Strong baseline
```

## Related Skills

- **hyperparameter-tuning**: Optimizes selected models
- **memory-management**: Ensures models fit in memory
- **gpu-optimization**: Maximizes model performance

This skill ensures optimal model selection for your specific requirements and constraints.
