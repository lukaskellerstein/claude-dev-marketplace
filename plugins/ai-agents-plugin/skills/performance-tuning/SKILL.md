---
name: performance-tuning
description: Master AI agent performance optimization, reducing latency and minimizing costs. Use when optimizing response times, reducing token usage, implementing caching, streaming responses, batching requests, selecting models, or improving agent efficiency and cost-effectiveness.
allowed-tools: Read, Write, Bash
---

# Performance Tuning Skill

Automatically optimize AI agent performance through latency reduction, token optimization, cost minimization, and efficient resource utilization using streaming, caching, and batching strategies.

## When to Use This Skill

1. **Latency Optimization** - Reducing agent response times
2. **Cost Reduction** - Minimizing API costs through efficient token usage
3. **Caching Strategy** - Implementing prompt and response caching
4. **Streaming Setup** - Enabling real-time response streaming
5. **Batch Processing** - Processing multiple requests efficiently
6. **Model Selection** - Choosing optimal models for tasks
7. **Token Management** - Reducing unnecessary token consumption
8. **Connection Pooling** - Reusing HTTP connections
9. **Parallel Execution** - Running tools concurrently
10. **Context Optimization** - Managing conversation context efficiently
11. **Load Testing** - Measuring and improving throughput
12. **Production Deployment** - Optimizing for scale
13. **Resource Utilization** - Maximizing infrastructure efficiency
14. **SLA Management** - Meeting performance targets
15. **Monitoring Setup** - Tracking performance metrics

## Quick Start

```python
# Quick performance optimization
async def optimized_agent_call(message: str):
    # 1. Check cache
    cache_key = hash(message)
    if cached := await redis.get(cache_key):
        return cached

    # 2. Stream response
    async with client.messages.stream(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1024,
        messages=[{"role": "user", "content": message}]
    ) as stream:
        response = ""
        async for text in stream.text_stream:
            response += text
            yield text  # Real-time streaming

    # 3. Cache result
    await redis.setex(cache_key, 3600, response)
```

## Real-World Scenarios

### Scenario 1: Reducing Latency from 3s to 500ms

**Problem**: Customer support agent takes 3+ seconds to respond.

**Analysis**:
```yaml
Current Performance:
  Average Latency: 3.2 seconds
  P95 Latency: 4.5 seconds
  P99 Latency: 6.0 seconds
  Throughput: 10 requests/second
  Cost: $0.15 per request

Bottleneck Analysis:
  - No caching (30% requests are similar)
  - No streaming (perceived latency)
  - Sequential tool calls (5 tools, 200ms each)
  - Large context windows (100K tokens)
  - Suboptimal model selection
```

**Optimization Plan**:
```yaml
Phase 1: Prompt Caching (Week 1):
  - Cache system prompts (90% savings)
  - Cache knowledge base content
  - 5-minute TTL for common queries

  Result: 2.1s latency (-34%), $0.08/request

Phase 2: Streaming (Week 1):
  - Enable response streaming
  - Improve perceived latency

  Result: 2.1s actual, 0.5s perceived (-84% perceived)

Phase 3: Parallel Tool Calls (Week 2):
  - Execute tools concurrently
  - Reduce sequential bottleneck

  Result: 1.2s latency (-42% from Phase 1)

Phase 4: Context Optimization (Week 2):
  - Summarize old messages
  - Keep only relevant context
  - Reduce to 20K tokens average

  Result: 0.8s latency (-33%), $0.05/request

Phase 5: Model Selection (Week 3):
  - Use Haiku for simple queries
  - Sonnet for complex queries
  - Route intelligently

  Result: 0.5s latency (-38%), $0.03/request

Final Results:
  Average Latency: 0.5s (-84%)
  Perceived Latency: 0.1s (-97%)
  Throughput: 50 requests/second (+400%)
  Cost: $0.03/request (-80%)
```

## Optimization Techniques

### 1. Prompt Caching

```python
# Cache large system prompts (90% discount)
system_prompt = "Large knowledge base content here..."

response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    system=[{
        "type": "text",
        "text": system_prompt,
        "cache_control": {"type": "ephemeral"}  # Cache for 5 minutes
    }],
    messages=[{"role": "user", "content": query}]
)

# Subsequent requests reuse cached prompt
# Input tokens: $3/MTok → $0.30/MTok (90% discount)
```

### 2. Streaming Responses

```python
async def stream_agent(message: str):
    """Stream for better perceived performance"""
    async with client.messages.stream(
        model="claude-sonnet-4-5-20250929",
        max_tokens=2048,
        messages=[{"role": "user", "content": message}]
    ) as stream:
        async for text in stream.text_stream:
            print(text, end="", flush=True)  # Real-time output
            yield text  # Stream to frontend
```

### 3. Parallel Tool Execution

```python
async def parallel_tools(tools: List[Tool], inputs: List[Dict]):
    """Execute multiple tools concurrently"""
    tasks = [
        tool.arun(input_data)
        for tool, input_data in zip(tools, inputs)
    ]

    # Execute in parallel
    results = await asyncio.gather(*tasks, return_exceptions=True)

    return results

# Before: 5 tools × 200ms = 1000ms
# After:  max(200ms) = 200ms (5x faster)
```

### 4. Connection Pooling

```python
# Reuse HTTP connections
async with httpx.AsyncClient(
    limits=httpx.Limits(
        max_keepalive_connections=20,
        keepalive_expiry=30
    )
) as http_client:
    client = AsyncAnthropic(http_client=http_client)

    # All requests reuse connections
    results = await asyncio.gather(*[
        client.messages.create(
            model="claude-sonnet-4-5-20250929",
            messages=[{"role": "user", "content": f"Query {i}"}]
        )
        for i in range(100)
    ])
```

## Best Practices

```yaml
1. Measure First:
   - Baseline performance before optimizing
   - Use profiling tools
   - Track key metrics

2. Optimize Hot Paths:
   - Focus on frequently used code
   - Profile to find bottlenecks
   - Measure improvements

3. Use Streaming:
   - Better perceived performance
   - Real-time user feedback
   - Reduced wait anxiety

4. Cache Aggressively:
   - System prompts (ephemeral caching)
   - Common queries (Redis)
   - Tool results (TTL-based)

5. Right-Size Models:
   - Haiku for simple tasks
   - Sonnet for balanced needs
   - Opus only when necessary

6. Manage Context:
   - Summarize old messages
   - Keep only relevant history
   - Use sliding windows

7. Batch When Possible:
   - Process similar requests together
   - Reduce API overhead
   - Amortize costs

8. Monitor Continuously:
   - Track latency percentiles
   - Monitor token usage
   - Alert on degradation
```

## Related Skills

- **security-validation**: Ensures performance optimizations maintain security
- **error-recovery**: Handles performance-related failures
- **agent-monitoring**: Tracks performance metrics
- **caching-strategy**: Implements effective caching layers
- **model-selection**: Chooses optimal models for performance

This skill ensures AI agents deliver fast, cost-effective responses while maintaining quality and user satisfaction.
