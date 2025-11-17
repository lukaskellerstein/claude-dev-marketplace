---
name: model-selection
description: Helps select appropriate models for tasks
allowed-tools: Read
---

# Model Selection Skill

Recommends optimal models based on requirements and constraints.

## Activation Triggers

This skill activates when:
- User asks for model recommendations
- Starting a new project
- Resource constraints specified
- Task requirements defined
- Current model underperforming
- Deployment target specified

## Responsibilities

1. **Recommend models for specific tasks**
2. **Consider hardware constraints**
3. **Balance quality vs efficiency**
4. **Suggest alternatives**
5. **Explain tradeoffs**

## Model Categories by Task

### Text Generation (General Purpose)

**Quality-Focused (Best Performance):**
```yaml
High-End:
  - llama-3-70b: Best overall, instruction-following
  - mixtral-8x22b: Excellent reasoning, MoE architecture
  - qwen-72b: Strong multilingual, competitive with GPT-4

Mid-Tier:
  - llama-2-70b: Solid performance, well-tested
  - mixtral-8x7b: Great balance, efficient MoE
  - yi-34b: Good quality, efficient

Entry-Level:
  - llama-2-13b: Reliable, widely supported
  - mistral-7b: Excellent 7B model
  - llama-3-8b: Latest 8B, strong performance
```

**Speed-Focused (Fast Inference):**
```yaml
Fast:
  - llama-2-7b: Standard 7B, well-optimized
  - mistral-7b: Very efficient 7B
  - phi-3-mini: Extremely fast, 3.8B

Ultra-Fast:
  - phi-2: Fast 2.7B model
  - gemma-2b: Efficient small model
  - tinyllama-1.1b: Tiny but capable
```

**Balanced (Quality + Speed):**
```yaml
Recommended:
  - mistral-7b: Best 7B model overall
  - llama-3-8b: Latest, excellent balance
  - yi-6b: Efficient and capable

Alternatives:
  - llama-2-13b: More capable, still efficient
  - neural-chat-7b: Fine-tuned Mistral
  - zephyr-7b: Strong instruction following
```

### Code Generation

```yaml
Top-Tier:
  - codellama-34b: Best code model
  - deepseek-coder-33b: Excellent at code
  - starcoder-15b: Strong baseline

Specialized:
  - codellama-python-34b: Python-specific
  - codellama-instruct-34b: Interactive coding
  - wizardcoder-34b: Instruction-tuned

Efficient:
  - codellama-7b: Smallest CodeLlama
  - starcoder-3b: Very efficient
  - phi-2: Surprisingly good at code
```

### Math & Reasoning

```yaml
Best:
  - deepseek-math-7b: Math-specialized
  - llemma-34b: Math-focused LLM
  - wizardmath-70b: Strong reasoning

Good:
  - mistral-7b: Decent math capabilities
  - llama-2-70b: Good reasoning
  - mixtral-8x7b: Strong reasoning
```

### Multilingual

```yaml
Best:
  - qwen-72b: 20+ languages
  - yi-34b: Chinese + English strong
  - aya-101: 101 languages

Good:
  - llama-2-70b: Multilingual support
  - mistral-7b: Several languages
  - bloom-176b: Multilingual focus
```

## Selection by Hardware

### Consumer GPU (8-12GB VRAM)

**Full Precision (FP16/BF16):**
```yaml
Fits Comfortably:
  - phi-2 (2.7B): ~6 GB
  - gemma-2b: ~5 GB
  - tinyllama-1.1b: ~3 GB

Fits Barely:
  - llama-2-7b: ~14 GB (won't fit)
  - mistral-7b: ~14 GB (won't fit)

Recommendation: Use quantization or QLoRA
```

**Quantized (4-bit/8-bit):**
```yaml
Excellent Options:
  - llama-2-13b-gptq: ~8 GB
  - mistral-7b-awq: ~5 GB
  - llama-3-8b-gguf-q4: ~5 GB
  - yi-34b-int4: ~10 GB

Recommended for RTX 3060/4060:
  - mistral-7b-q4: Best quality/performance
  - llama-2-13b-q4: More capable
  - phi-2-q8: Maximum quality small model
```

### Professional GPU (24GB VRAM)

**Full Precision:**
```yaml
Fits Well:
  - llama-2-13b: ~26 GB (tight)
  - mistral-7b: ~14 GB
  - llama-3-8b: ~16 GB
  - codellama-13b: ~26 GB

Recommendation: Ideal for 13B models
```

**Quantized (More Capacity):**
```yaml
Excellent Options:
  - llama-2-70b-int8: ~38 GB (won't fit)
  - mixtral-8x7b-gptq: ~24 GB
  - yi-34b-awq: ~20 GB
  - llama-2-70b-int4: ~18 GB

Recommended for A10/RTX 4090:
  - mixtral-8x7b-q4: Excellent MoE
  - yi-34b-q4: Strong 34B model
  - llama-2-70b-q4: Maximum capability
```

### Datacenter GPU (40-80GB VRAM)

**Full Precision:**
```yaml
Fits on A100 40GB:
  - llama-2-70b: ~140 GB (need 2x)
  - mixtral-8x7b: ~48 GB
  - yi-34b: ~68 GB (need 2x)

Fits on A100 80GB:
  - llama-2-70b: ~140 GB (need 2x)
  - llama-3-70b: ~140 GB (need 2x)

Recommendation: Use tensor parallelism for 70B+
```

**Optimized:**
```yaml
Excellent Options:
  - llama-2-70b-int8: ~38 GB (single 80GB)
  - mixtral-8x7b-int8: ~24 GB
  - yi-34b-awq: ~20 GB

Recommended for A100:
  - llama-2-70b-int8: Best bang for buck
  - mixtral-8x22b-int4: Maximum capability
  - qwen-72b-int8: Multilingual powerhouse
```

## Decision Tree

```python
def recommend_model(task, quality_priority, hardware):
    """Intelligent model recommendation"""

    recommendations = []

    # Task-based filtering
    if task == 'code':
        base_models = ['codellama-34b', 'deepseek-coder-33b', 'codellama-7b']
    elif task == 'math':
        base_models = ['deepseek-math-7b', 'llemma-34b', 'mistral-7b']
    elif task == 'multilingual':
        base_models = ['qwen-72b', 'yi-34b', 'llama-2-70b']
    else:  # general text generation
        base_models = ['llama-3-70b', 'mixtral-8x7b', 'mistral-7b', 'llama-3-8b']

    # Hardware filtering
    if hardware == 'consumer_gpu':  # 8-12GB
        # Must use quantization
        if quality_priority == 'high':
            recommendations = [
                ('llama-2-13b-gptq', 'Best balance for consumer GPU'),
                ('mistral-7b-awq', 'Excellent quality, efficient'),
                ('yi-34b-int4', 'Maximum capability if memory allows')
            ]
        else:  # speed priority
            recommendations = [
                ('mistral-7b-q4', 'Fast and capable'),
                ('phi-2-q8', 'Very fast, good quality'),
                ('llama-3-8b-q4', 'Latest, efficient')
            ]

    elif hardware == 'professional_gpu':  # 24GB
        if quality_priority == 'high':
            recommendations = [
                ('mixtral-8x7b-gptq', 'Best for 24GB'),
                ('yi-34b-awq', 'Excellent 34B model'),
                ('llama-2-13b', 'Full precision option')
            ]
        else:
            recommendations = [
                ('mistral-7b', 'Full precision, very fast'),
                ('llama-3-8b', 'Latest, excellent speed'),
                ('codellama-13b', 'If code-focused')
            ]

    elif hardware == 'datacenter_gpu':  # 40-80GB
        if quality_priority == 'high':
            recommendations = [
                ('llama-3-70b', 'Best overall (needs 2x GPUs)'),
                ('mixtral-8x22b', 'Maximum capability MoE'),
                ('qwen-72b', 'Multilingual powerhouse')
            ]
        else:
            recommendations = [
                ('llama-2-70b-int8', 'Excellent on single 80GB'),
                ('mixtral-8x7b', 'Very efficient MoE'),
                ('yi-34b-awq', 'Strong and fast')
            ]

    return recommendations

def print_recommendations(task, quality, hardware):
    """Pretty print model recommendations"""

    recs = recommend_model(task, quality, hardware)

    print("\n" + "="*60)
    print("   MODEL RECOMMENDATIONS")
    print("="*60)
    print(f"\nTask: {task}")
    print(f"Quality Priority: {quality}")
    print(f"Hardware: {hardware}")
    print("\nRecommended Models:\n")

    for i, (model, reason) in enumerate(recs, 1):
        print(f"{i}. {model}")
        print(f"   → {reason}\n")
```

## Comparison Framework

```python
def compare_models(models, criteria=['quality', 'speed', 'memory']):
    """Compare multiple models across criteria"""

    # Model database (simplified)
    model_db = {
        'llama-2-7b': {
            'params': 7e9,
            'quality_score': 7.0,
            'speed_tokens_per_sec': 50,
            'memory_gb': 14,
            'license': 'Llama 2'
        },
        'mistral-7b': {
            'params': 7e9,
            'quality_score': 7.5,
            'speed_tokens_per_sec': 55,
            'memory_gb': 14,
            'license': 'Apache 2.0'
        },
        'llama-2-13b': {
            'params': 13e9,
            'quality_score': 7.8,
            'speed_tokens_per_sec': 30,
            'memory_gb': 26,
            'license': 'Llama 2'
        },
        'mixtral-8x7b': {
            'params': 47e9,
            'quality_score': 8.5,
            'speed_tokens_per_sec': 40,
            'memory_gb': 48,
            'license': 'Apache 2.0'
        },
        'llama-2-70b': {
            'params': 70e9,
            'quality_score': 9.0,
            'speed_tokens_per_sec': 15,
            'memory_gb': 140,
            'license': 'Llama 2'
        }
    }

    print("\n" + "="*80)
    print("   MODEL COMPARISON")
    print("="*80)

    print(f"\n{'Model':<20} {'Params':<12} {'Quality':<10} {'Speed':<15} {'Memory':<10}")
    print("-" * 80)

    for model in models:
        if model in model_db:
            info = model_db[model]
            print(f"{model:<20} "
                  f"{info['params']/1e9:<11.1f}B "
                  f"{info['quality_score']:<10.1f} "
                  f"{info['speed_tokens_per_sec']:<14} "
                  f"{info['memory_gb']:<10}GB")

    print("\nLegend:")
    print("  Quality: Benchmark score (higher = better)")
    print("  Speed: Tokens per second (approximate)")
    print("  Memory: VRAM required (FP16/BF16)")
```

## Optimization Suggestions

```python
def suggest_optimization(model_name, target_hardware):
    """Suggest optimizations for model on target hardware"""

    print(f"\n💡 Optimization Suggestions for {model_name}:")

    # Determine model size category
    if '70b' in model_name or '72b' in model_name:
        size = 'large'
    elif '13b' in model_name or '34b' in model_name:
        size = 'medium'
    else:
        size = 'small'

    # Suggest based on size and hardware
    if target_hardware == 'consumer_gpu':
        print("\n   Recommended:")
        if size == 'large':
            print("   ❌ Model too large for consumer GPU")
            print("   💡 Use int4 quantization (GPTQ/AWQ)")
            print("   💡 Or use smaller model (13B)")
        elif size == 'medium':
            print("   ✅ Use int4 quantization (GPTQ/AWQ)")
            print("   ✅ Enable CPU offloading if needed")
        else:
            print("   ✅ Should work with int8 quantization")
            print("   ✅ Or full precision if <7B")

    elif target_hardware == 'professional_gpu':
        if size == 'large':
            print("   ✅ Use int8 or int4 quantization")
            print("   ✅ Enable tensor parallelism if multiple GPUs")
        elif size == 'medium':
            print("   ✅ Full precision possible for 13B")
            print("   ✅ int4 for 34B models")
        else:
            print("   ✅ Full precision recommended")
            print("   ✅ Enable Flash Attention")

    print("\n   Additional Optimizations:")
    print("   - vLLM for serving")
    print("   - Flash Attention 2")
    print("   - Prefix caching")
    print("   - Continuous batching")
```

## Next Steps Guidance

```python
def guide_next_steps(selected_model, use_case):
    """Guide user on next steps after model selection"""

    print(f"\n" + "="*60)
    print(f"   NEXT STEPS FOR {selected_model}")
    print("="*60)

    print("\n1. Obtain the model:")
    print(f"   from transformers import AutoModelForCausalLM")
    print(f"   model = AutoModelForCausalLM.from_pretrained('{selected_model}')")

    print("\n2. Choose deployment approach:")
    if use_case == 'development':
        print("   → Use Ollama for local development")
        print("   → Quick iteration and testing")
    elif use_case == 'production':
        print("   → Use vLLM for high-throughput serving")
        print("   → Set up monitoring and scaling")

    print("\n3. Optimize for your hardware:")
    print("   → Quantize if memory constrained")
    print("   → Enable Flash Attention")
    print("   → Configure tensor parallelism")

    print("\n4. Fine-tune if needed:")
    print("   → Use LoRA for parameter-efficient tuning")
    print("   → Use QLoRA for memory efficiency")

    print("\n5. Evaluate performance:")
    print("   → Run benchmarks")
    print("   → Test on your specific use case")
    print("   → Compare with alternatives")
```

## Best Practices

1. **Start with proven models**: Use well-tested models first
2. **Match task to model**: Use specialized models when available
3. **Consider hardware**: Be realistic about constraints
4. **Test before committing**: Validate on your data
5. **Plan for scaling**: Think about production needs
6. **Monitor licensing**: Respect usage terms
7. **Benchmark thoroughly**: Measure actual performance
8. **Stay updated**: New models released frequently

## Common Mistakes to Avoid

1. **Picking largest model**: Not always best
2. **Ignoring hardware limits**: Leads to OOM
3. **Skipping quantization**: Wastes memory
4. **Not testing**: Assumptions may be wrong
5. **Forgetting licensing**: Legal issues
6. **Overlooking specialized models**: Task-specific often better
7. **Not considering inference cost**: Production costs matter

## Notes

- This skill provides intelligent recommendations
- Considers multiple factors simultaneously
- Balances tradeoffs automatically
- Updates with new model releases
- Can be customized for specific needs
