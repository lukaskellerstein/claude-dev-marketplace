---
description: Deploy LLMs for production inference using vLLM, Ollama, TGI with optimizations for performance, scalability, and cost
---

Design and implement a production-ready deployment pipeline for Large Language Model inference.

## Process

Follow these steps:

1. **Analyze Requirements**: Understand deployment needs and constraints
   - Latency requirements (TTFT, TPOT)
   - Throughput requirements (requests/sec, tokens/sec)
   - Cost constraints and budget
   - Infrastructure available (cloud, on-premise, edge)
   - Scaling needs
   - Review existing infrastructure if applicable

2. **Launch Deployment Expert**: Use the `llm-deployment-expert` agent to:
   - Select deployment platform (vLLM, Ollama, TGI, custom)
   - Configure inference optimizations
   - Design infrastructure setup
   - Plan quantization and optimization
   - Set up monitoring and observability
   - Design scaling strategy
   - Plan disaster recovery

3. **Optimize Performance**: Use the `model-optimization-expert` agent to:
   - Apply quantization for efficiency
   - Optimize inference speed
   - Reduce memory footprint
   - Configure hardware acceleration
   - Benchmark and profile performance

4. **Implementation Guide**: Provide:
   - Complete deployment configuration
   - Docker/Kubernetes manifests
   - Inference server setup
   - API integration code
   - Monitoring setup
   - Scaling configuration
   - Cost optimization strategies

## Output

Present a comprehensive deployment plan including:

### Deployment Strategy
- Platform selection (vLLM, Ollama, TGI)
- Infrastructure choice (cloud provider, on-premise)
- Deployment pattern (single instance, multi-GPU, distributed)
- Rationale for selections
- Trade-offs analysis
- Alternative approaches

### Model Preparation
- Quantization strategy (4-bit AWQ/GPTQ, 8-bit, none)
- Model format conversion (if needed)
- Optimization techniques applied
- Quality validation after optimization
- Model size and requirements
- Storage and loading strategy

### Infrastructure Configuration

#### vLLM Deployment
```bash
python -m vllm.entrypoints.openai.api_server \
    --model <model_name> \
    --tensor-parallel-size <num_gpus> \
    --dtype bfloat16 \
    --max-model-len 4096 \
    --gpu-memory-utilization 0.95
```

#### Ollama Deployment
```dockerfile
FROM llama3
PARAMETER temperature 0.7
PARAMETER num_ctx 4096
SYSTEM "Your system prompt"
```

#### TGI Deployment
```bash
docker run -d --gpus all \
    ghcr.io/huggingface/text-generation-inference \
    --model-id <model_name> \
    --num-shard <num_gpus> \
    --max-total-tokens 4096
```

### API Design
- Endpoint specification
- Request/response format
- Authentication mechanism
- Rate limiting strategy
- Error handling
- OpenAI-compatible API (if applicable)
- WebSocket support (if needed)
- Example API calls

### Performance Configuration
- Batch size optimization
- Max sequence length
- GPU memory utilization
- KV cache configuration
- Continuous batching settings
- Speculative decoding (if applicable)
- Generation parameters
- Timeout settings

### Container Configuration
- Docker image setup
- Environment variables
- Volume mounts
- Resource limits (CPU, memory, GPU)
- Health checks
- Startup probes
- Network configuration

### Kubernetes Deployment (if applicable)
```yaml
# Deployment manifest
# Service configuration
# HorizontalPodAutoscaler
# Ingress/LoadBalancer
# ConfigMaps and Secrets
# PersistentVolumeClaims
```

### Load Balancing
- Load balancer configuration
- Request routing strategy
- Session affinity (if needed)
- Health check endpoints
- Failover strategy
- Geographic distribution

### Scaling Strategy
- Horizontal scaling rules
- Vertical scaling considerations
- Autoscaling metrics and thresholds
- Scale-up/scale-down policies
- Cost optimization with scaling
- Request queuing strategy

### Monitoring and Observability
- Metrics to collect:
  - Latency (TTFT, TPOT, p50, p95, p99)
  - Throughput (requests/sec, tokens/sec)
  - GPU utilization and memory
  - Queue depth
  - Error rates
  - Cache hit rates
- Logging configuration
- Distributed tracing
- Dashboard templates
- Alert rules and thresholds

### Cost Optimization
- Quantization impact on costs
- Instance type optimization
- Spot instance strategy
- Autoscaling for cost reduction
- Request batching efficiency
- Multi-tenancy considerations
- Cost monitoring and alerts

### Security Configuration
- Authentication (API keys, OAuth)
- Authorization and access control
- Network security (VPC, security groups)
- Secrets management
- Input validation and sanitization
- Rate limiting and DDoS protection
- Audit logging

### Disaster Recovery
- Backup strategy
- Failover configuration
- Multi-region deployment (if applicable)
- Recovery time objectives (RTO)
- Recovery point objectives (RPO)
- Incident response plan

### Testing Strategy
- Load testing approach
- Performance benchmarking
- Stress testing
- Chaos engineering
- A/B testing setup
- Canary deployment strategy

### Performance Estimates
- Expected latency (TTFT, TPOT)
- Expected throughput
- Resource utilization
- Cost per 1M tokens
- Scaling capabilities
- Comparison with alternatives

## Examples

### High-Throughput vLLM Deployment
```
/deploy-model

Deploy Llama-3-8B with vLLM on 2x A100 GPUs for high-throughput
API service with <1s p95 latency and 100+ concurrent users
```

### Local Ollama Deployment
```
/deploy-model

Deploy Mistral-7B-Instruct locally with Ollama for development
and testing, optimized for MacBook Pro with M3 chip
```

### Edge Deployment with Quantization
```
/deploy-model

Deploy quantized Llama-3-8B (4-bit AWQ) on edge device with
limited resources, targeting <2s latency for chat application
```

### Multi-Model Serving
```
/deploy-model

Set up inference infrastructure for serving multiple fine-tuned
models (3x 7B models) with dynamic routing and load balancing
```

### Cost-Optimized Cloud Deployment
```
/deploy-model

Deploy Llama-2-13B on AWS with spot instances, autoscaling,
and aggressive quantization to minimize costs while maintaining quality
```

## Deployment Scenarios

### Production API Service
- vLLM with continuous batching
- Multi-GPU tensor parallelism
- Load balancer with autoscaling
- Comprehensive monitoring
- High availability setup
- Cost-performance optimization

### On-Premise/Private Cloud
- Custom infrastructure deployment
- Security and compliance requirements
- TGI or vLLM deployment
- Internal networking
- License management
- Audit trail

### Edge Deployment
- Ollama or llama.cpp
- Aggressive quantization (4-bit)
- Limited resource optimization
- Offline capability
- Low power consumption
- Fast startup time

### Multi-Tenant SaaS
- Model sharing across tenants
- Request isolation and quotas
- Per-tenant rate limiting
- Cost allocation tracking
- Security isolation
- Scalability for growth

### Real-time Chat Service
- Low latency optimization (p95 <500ms)
- WebSocket support
- Streaming responses
- User session management
- Context caching
- High concurrency handling

## Platform Comparison

### vLLM
**Best for**: High-throughput production APIs
- Pros: Best throughput, PagedAttention, continuous batching
- Cons: Complex setup, GPU-only
- Use when: Maximum performance needed

### Ollama
**Best for**: Local development and edge deployment
- Pros: Easy setup, multi-platform, great DX
- Cons: Limited production features
- Use when: Development, local, or edge deployment

### TGI (Text Generation Inference)
**Best for**: HuggingFace model serving
- Pros: Good performance, Docker-ready, HF integration
- Cons: Less flexible than vLLM
- Use when: HuggingFace models, Docker deployment

### Custom (FastAPI + Transformers)
**Best for**: Custom requirements and full control
- Pros: Maximum flexibility, custom logic
- Cons: Manual optimization, more development
- Use when: Special requirements, prototyping

## Best Practices Applied

- **Quantization**: Use 4-bit AWQ for optimal speed-quality trade-off
- **Batching**: Enable continuous batching for throughput
- **Monitoring**: Comprehensive metrics and alerting
- **Testing**: Load test before production
- **Scaling**: Horizontal scaling with autoscaling
- **Caching**: Cache system prompts and common prefixes
- **Security**: Authentication, rate limiting, input validation
- **Cost**: Right-size instances, use spot/preemptible
- **Reliability**: Health checks, failover, disaster recovery

## Integration with Other Components

- **Model Training**: Deploy trained models
- **Fine-tuning**: Deploy fine-tuned models
- **Optimization**: Use optimized/quantized models
- **Monitoring**: Integrate with observability stack

Provide production-ready deployment configurations with complete infrastructure code, security considerations, and cost optimization strategies.
