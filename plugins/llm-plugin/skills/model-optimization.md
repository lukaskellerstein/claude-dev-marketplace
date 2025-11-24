---
name: model-optimization
description: Auto-invoked when optimizing LLM inference or deployment to ensure best practices for performance and efficiency
allowed-tools: Read, Grep, Glob
---

# LLM Model Optimization Best Practices

This skill provides guidance on optimizing Large Language Models for inference, deployment, and production use to maximize performance and efficiency.

## When Active

This skill activates when you:
- Configure inference servers (vLLM, Ollama, TGI)
- Apply quantization to models
- Optimize model serving performance
- Set up production deployments
- Debug performance issues
- Configure hardware acceleration

## Quantization Best Practices

### Choosing Quantization Method

**4-bit Quantization** (Most Common)
- **AWQ (Activation-Aware Weight Quantization)**: Best quality-speed trade-off
- **GPTQ**: Good quality, slightly slower than AWQ
- **GGUF Q4**: Best for CPU/Metal inference

**When to Use Each:**
```python
# GPU Inference (vLLM, TGI) - Use AWQ
model = "casperhansen/llama-3-8b-instruct-awq"

# GPU Inference (alternative) - Use GPTQ
model = "TheBloke/Llama-3-8B-Instruct-GPTQ"

# CPU/Metal Inference - Use GGUF
model = "TheBloke/Llama-3-8B-Instruct-GGUF"  # Q4_K_M variant
```

### Quality vs Size Trade-offs
- **No quantization**: Full quality, 2x memory, baseline speed
- **8-bit**: 99% quality, 50% memory, 1.5x speed
- **4-bit AWQ**: 95-98% quality, 25% memory, 2-3x speed
- **4-bit GPTQ**: 94-97% quality, 25% memory, 2x speed
- **4-bit GGUF Q4_K_M**: 95% quality, 25% memory, CPU-optimized

**Always benchmark on your tasks** - quality impact varies by model and use case.

### Quantization Configuration

```python
# Good: AWQ Loading (vLLM)
from vllm import LLM

model = LLM(
    model="casperhansen/llama-3-8b-instruct-awq",
    quantization="awq",
    dtype="auto",
    max_model_len=4096,
    gpu_memory_utilization=0.95,
)

# Good: GPTQ Loading
from auto_gptq import AutoGPTQForCausalLM

model = AutoGPTQForCausalLM.from_quantized(
    "TheBloke/Llama-3-8B-Instruct-GPTQ",
    device="cuda:0",
    use_triton=True,  # Faster kernels
    use_safetensors=True,
)

# Good: GGUF with llama.cpp/Ollama
# Modelfile
FROM llama3:8b-instruct-q4_K_M
PARAMETER num_gpu 1  # Use GPU acceleration
```

## vLLM Optimization

### Configuration Best Practices

```python
# Good: High-throughput configuration
python -m vllm.entrypoints.openai.api_server \
    --model casperhansen/llama-3-8b-instruct-awq \
    --quantization awq \
    --dtype auto \
    --max-model-len 4096 \
    --gpu-memory-utilization 0.95 \  # Use 90-95% of GPU memory
    --max-num-batched-tokens 8192 \  # Higher for more throughput
    --max-num-seqs 256 \              # More concurrent sequences
    --tensor-parallel-size 2 \        # Use 2 GPUs if available
    --enable-prefix-caching \         # Cache system prompts
    --disable-log-requests            # Reduce overhead
```

### Performance Tuning
- **GPU memory utilization**: 0.90-0.95 (higher = more throughput)
- **Max model length**: Set to actual need (lower = more throughput)
- **Tensor parallelism**: Use for models >13B or latency requirements
- **Enable prefix caching**: For repeated system prompts
- **Max num seqs**: Increase for higher throughput (64-256)

```python
# Good: Latency-optimized (single user)
model = LLM(
    model="model_name",
    max_model_len=2048,        # Lower if possible
    gpu_memory_utilization=0.8,
    max_num_seqs=1,            # Single request at a time
    enforce_eager=False,       # Use CUDA graphs
)

# Good: Throughput-optimized (many users)
model = LLM(
    model="model_name",
    max_model_len=4096,
    gpu_memory_utilization=0.95,
    max_num_seqs=256,          # Many concurrent requests
    max_num_batched_tokens=16384,
    enable_prefix_caching=True,
)
```

## Ollama Optimization

### Modelfile Configuration

```dockerfile
# Good: Optimized Modelfile
FROM llama3:8b-instruct-q4_K_M

# Set context length (lower = faster)
PARAMETER num_ctx 4096

# GPU layers (all layers to GPU if possible)
PARAMETER num_gpu 99

# Thread count for CPU inference
PARAMETER num_thread 8

# Batch size
PARAMETER num_batch 512

# Generation parameters
PARAMETER temperature 0.7
PARAMETER top_p 0.9
PARAMETER top_k 40

# System prompt
SYSTEM """You are a helpful assistant."""
```

### Performance Settings
- **num_gpu**: Set to 99 to offload all layers to GPU
- **num_ctx**: Use minimum required (2048-4096)
- **num_thread**: Set to physical CPU cores for CPU inference
- **num_batch**: Higher for throughput (256-512)
- **mmap**: Enabled by default, keeps memory usage low

```bash
# Good: Ollama run with settings
ollama run llama3:8b-instruct-q4_K_M \
    --num-ctx 4096 \
    --num-gpu 1
```

## Text Generation Inference (TGI)

### Docker Configuration

```bash
# Good: TGI production deployment
docker run -d \
    --gpus all \
    --shm-size 1g \
    -p 8080:80 \
    -v $PWD/data:/data \
    ghcr.io/huggingface/text-generation-inference:latest \
    --model-id meta-llama/Llama-2-7b-chat-hf \
    --num-shard 2 \                    # Tensor parallelism
    --max-total-tokens 4096 \          # Total tokens in batch
    --max-input-length 3072 \          # Max input length
    --max-batch-prefill-tokens 8192 \  # Prefill batch size
    --quantize awq \                   # Enable AWQ quantization
    --dtype bfloat16
```

### Performance Parameters
- **num-shard**: Number of GPUs for tensor parallelism
- **max-total-tokens**: Total KV cache size (higher = more throughput)
- **max-batch-prefill-tokens**: Larger = better throughput
- **quantize**: Use "awq" or "gptq" for 4-bit

## Inference Optimization Techniques

### Flash Attention
**Always enable for 2-3x memory reduction**

```python
# Good: Enable Flash Attention
from transformers import AutoModelForCausalLM

model = AutoModelForCausalLM.from_pretrained(
    "model_name",
    torch_dtype=torch.bfloat16,
    attn_implementation="flash_attention_2",  # Enable Flash Attention 2
    device_map="auto"
)
```

### KV Cache Optimization
- **Reduce context length**: Use minimum required
- **PagedAttention (vLLM)**: Automatic memory management
- **Prefix caching**: Cache common prompts (system messages)
- **Sliding window**: For very long contexts

```python
# Good: Prefix caching in vLLM
model = LLM(
    model="model_name",
    enable_prefix_caching=True,  # Cache repeated prefixes
)

# System prompts will be cached automatically
```

### Batching Strategies

```python
# Good: Continuous batching (vLLM default)
# Automatically batches requests as they arrive
# No configuration needed - works out of the box

# Good: Dynamic batching for custom servers
class DynamicBatcher:
    def __init__(self, max_batch_size=32, max_wait_ms=10):
        self.max_batch_size = max_batch_size
        self.max_wait_ms = max_wait_ms

    async def batch_requests(self, requests):
        batch = []
        deadline = time.time() + (self.max_wait_ms / 1000)

        while len(batch) < self.max_batch_size:
            if time.time() >= deadline and batch:
                break
            batch.append(await self.get_next_request())

        return batch
```

## Generation Parameter Optimization

### Speed vs Quality Trade-offs

```python
# Good: Faster generation (less quality)
generation_params = {
    "max_new_tokens": 256,     # Limit output length
    "temperature": 0.7,         # Lower = more deterministic
    "top_p": 0.9,              # Nucleus sampling
    "top_k": 40,               # Limit vocabulary
    "repetition_penalty": 1.1,  # Prevent repetition
    "do_sample": True,         # Enable sampling
}

# Good: Higher quality (slower)
generation_params = {
    "max_new_tokens": 1024,
    "temperature": 0.8,
    "top_p": 0.95,
    "top_k": 50,
    "do_sample": True,
    "num_beams": 4,            # Beam search (slower)
}

# Good: Fastest (greedy)
generation_params = {
    "max_new_tokens": 256,
    "do_sample": False,        # Greedy decoding
    "temperature": 0,
}
```

### Streaming Responses
**Always enable for better user experience**

```python
# Good: Streaming with vLLM
from vllm import LLM, SamplingParams

model = LLM(model="model_name")
sampling_params = SamplingParams(temperature=0.7, max_tokens=256)

# Stream tokens as they're generated
for output in model.generate("prompt", sampling_params, stream=True):
    print(output.outputs[0].text, end="", flush=True)
```

## Hardware-Specific Optimizations

### NVIDIA GPUs
- **Use TensorRT-LLM**: Maximum performance on NVIDIA
- **Enable Tensor Cores**: Use BF16/FP16
- **Flash Attention**: Must-have for attention ops
- **Tensor parallelism**: For models >13B

```python
# Good: NVIDIA optimization
model = LLM(
    model="model_name",
    dtype="bfloat16",           # Tensor Core support
    quantization="awq",         # GPU-optimized quantization
    tensor_parallel_size=2,     # Multi-GPU
)
```

### AMD GPUs
- **Use ROCm builds**: Optimized for AMD
- **Flash Attention**: Available on ROCm
- **Check compatibility**: Not all models optimized

### Apple Silicon (M1/M2/M3)
- **Use GGUF format**: Optimized for Metal
- **llama.cpp or Ollama**: Best performance
- **Use Q4_K_M or Q5_K_M**: Good quality-speed balance

```bash
# Good: Apple Silicon deployment
ollama run llama3:8b-instruct-q4_K_M
# Automatically uses Metal acceleration
```

### CPUs
- **Use GGUF Q4/Q5**: Optimized for CPU
- **llama.cpp**: Best CPU inference
- **Enable AVX2/AVX512**: Hardware acceleration
- **Set thread count**: Match physical cores

```bash
# Good: CPU inference with llama.cpp
./llama-cpp-server \
    -m model.gguf \
    -t 8 \              # 8 threads
    -c 4096 \           # Context length
    --mlock             # Lock model in RAM
```

## Monitoring and Benchmarking

### Key Metrics to Track

```python
# Monitor these metrics
metrics = {
    # Latency
    "ttft": time_to_first_token,    # p50, p95, p99
    "tpot": time_per_output_token,  # p50, p95, p99
    "e2e_latency": end_to_end_time,

    # Throughput
    "tokens_per_second": tokens / time,
    "requests_per_second": requests / time,

    # Resources
    "gpu_memory_used": torch.cuda.memory_allocated(),
    "gpu_utilization": get_gpu_util(),
    "queue_depth": len(pending_requests),

    # Quality
    "cache_hit_rate": cache_hits / total_requests,
    "error_rate": errors / total_requests,
}
```

### Benchmarking
```bash
# Good: Load testing with locust or ab
# Test latency and throughput under load

# Latency test (single user)
for i in {1..100}; do
    time curl -X POST http://localhost:8000/v1/completions \
        -d '{"prompt": "Hello", "max_tokens": 100}'
done

# Throughput test (many users)
ab -n 1000 -c 50 -p request.json http://localhost:8000/v1/completions
```

## Common Performance Issues

### High Latency
1. Reduce context length (max_model_len)
2. Enable tensor parallelism
3. Use quantization (AWQ)
4. Enable Flash Attention
5. Optimize generation parameters
6. Check GPU utilization

### Low Throughput
1. Increase max_num_seqs
2. Increase gpu_memory_utilization
3. Enable continuous batching (vLLM)
4. Increase max_batch_size
5. Use prefix caching
6. Scale horizontally

### Out of Memory
1. Use quantization (4-bit)
2. Reduce max_model_len
3. Reduce max_num_seqs
4. Enable tensor parallelism
5. Use smaller model variant
6. Reduce batch size

### Poor Quality After Quantization
1. Use AWQ instead of GPTQ
2. Try 8-bit instead of 4-bit
3. Fine-tune after quantization
4. Use higher quality quantization (Q5 vs Q4)
5. Test different quantization methods

## Cost Optimization

### Techniques
- **Aggressive quantization**: 4-bit AWQ/GPTQ
- **Right-size instances**: Match GPU memory to model
- **Spot instances**: 60-80% cost reduction
- **Autoscaling**: Scale down during low traffic
- **Request batching**: Maximize GPU utilization
- **Multi-tenancy**: Share resources across models

```python
# Good: Cost-optimized deployment
# 4-bit quantization on smaller GPU instance
model = LLM(
    model="TheBloke/Llama-3-8B-Instruct-AWQ",
    quantization="awq",
    gpu_memory_utilization=0.95,  # Maximize usage
    max_num_seqs=128,              # Good throughput
)

# Deploy on T4 (16GB) instead of A100 (40GB)
# 4-5x cost reduction with acceptable performance
```

## Checklist

Before deployment:
- [ ] Quantization applied (4-bit AWQ/GPTQ)
- [ ] Flash Attention enabled
- [ ] Context length optimized
- [ ] GPU memory utilization >90%
- [ ] Batching enabled (continuous or dynamic)
- [ ] Streaming responses configured
- [ ] Monitoring and metrics set up
- [ ] Load testing completed

For production:
- [ ] Autoscaling configured
- [ ] Health checks implemented
- [ ] Alert thresholds set
- [ ] Backup/failover strategy
- [ ] Cost monitoring active
- [ ] Performance baselines established
- [ ] Documentation complete

Optimization priorities:
1. **Quantization**: Biggest impact on cost and speed
2. **Flash Attention**: Essential for attention efficiency
3. **Batching**: Critical for throughput
4. **Context length**: Reduce if possible
5. **Generation params**: Tune for use case
6. **Hardware**: Match to workload

Use this guidance to maximize LLM inference performance while minimizing costs.
