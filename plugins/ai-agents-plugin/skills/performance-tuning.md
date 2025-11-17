---
name: performance-tuning
description: Automatically optimize agent performance, reduce latency, and minimize costs
allowed-tools: Read, Write, Bash
---

# Performance Tuning Skill

This skill automatically identifies and applies performance optimizations to improve agent speed and reduce costs.

## When This Activates

This skill activates when:
- Creating new agents
- Agent response time is slow
- Token usage is high
- Testing agent performance
- Preparing for production deployment

## What It Does

### 1. Latency Optimization

Reduces response time:
- Parallel tool calls
- Streaming responses
- Request batching
- Connection pooling

### 2. Token Optimization

Reduces token usage:
- Prompt compression
- Response length limits
- Smart context management
- Caching strategies

### 3. Cost Optimization

Reduces operational costs:
- Model selection
- Request batching
- Prompt caching
- Result caching

## Implementation

```python
import asyncio
from typing import List, Dict, Any

class PerformanceOptimizer:
    def __init__(self):
        self.cache = {}
        self.metrics = []

    async def parallel_tool_calls(self, tools: List[Dict]) -> List[Any]:
        """Execute multiple tool calls in parallel"""
        tasks = [
            self._execute_tool(tool)
            for tool in tools
        ]

        results = await asyncio.gather(*tasks, return_exceptions=True)
        return results

    async def _execute_tool(self, tool: Dict) -> Any:
        """Execute single tool call"""
        # Tool execution logic
        pass

    def compress_prompt(self, prompt: str, max_tokens: int) -> str:
        """Compress prompt to fit token budget"""
        # Simple compression - could use more sophisticated methods
        words = prompt.split()
        estimated_tokens = len(words) * 1.3

        if estimated_tokens <= max_tokens:
            return prompt

        # Truncate to fit budget
        target_words = int(max_tokens / 1.3)
        return ' '.join(words[:target_words])

    def should_use_cache(self, request: str) -> bool:
        """Determine if request should use cache"""
        # Check if similar request exists in cache
        return request in self.cache

    def cache_response(self, request: str, response: Any, ttl: int = 3600):
        """Cache response with TTL"""
        import time
        self.cache[request] = {
            "response": response,
            "timestamp": time.time(),
            "ttl": ttl
        }

    def get_cached_response(self, request: str) -> Any:
        """Get cached response if valid"""
        import time

        if request not in self.cache:
            return None

        cached = self.cache[request]
        age = time.time() - cached["timestamp"]

        if age > cached["ttl"]:
            del self.cache[request]
            return None

        return cached["response"]
```

## Optimization Strategies

### 1. Streaming Responses

```python
# Stream for better perceived performance
async def stream_agent_response(message: str):
    async with client.messages.stream(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1024,
        messages=[{"role": "user", "content": message}]
    ) as stream:
        async for text in stream.text_stream:
            print(text, end="", flush=True)
            yield text
```

### 2. Prompt Caching

```python
# Cache large system prompts
response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    system=[
        {
            "type": "text",
            "text": "Large system prompt...",
            "cache_control": {"type": "ephemeral"}
        }
    ],
    messages=[{"role": "user", "content": "Query"}]
)

# Subsequent requests reuse cached prompt (5 min cache)
# 90% discount on cached tokens
```

### 3. Request Batching

```python
async def batch_requests(requests: List[str], batch_size: int = 5):
    """Process requests in batches"""
    results = []

    for i in range(0, len(requests), batch_size):
        batch = requests[i:i + batch_size]

        # Process batch in parallel
        batch_results = await asyncio.gather(*[
            call_agent(req) for req in batch
        ])

        results.extend(batch_results)

    return results
```

### 4. Model Selection

```python
def select_optimal_model(task_complexity: str) -> str:
    """Choose model based on task complexity"""

    if task_complexity == "simple":
        return "claude-haiku-3-5-20250222"  # Fast & cheap

    elif task_complexity == "medium":
        return "claude-sonnet-4-5-20250929"  # Balanced

    else:  # complex
        return "claude-opus-4-5-20250229"  # Best quality

# Example usage
model = select_optimal_model("simple")
response = client.messages.create(
    model=model,
    messages=[{"role": "user", "content": "What is 2+2?"}]
)
```

### 5. Context Management

```python
def optimize_context(messages: List[Dict], max_tokens: int = 100000):
    """Keep context within optimal range"""

    # Estimate tokens
    total_tokens = sum(
        len(msg["content"]) // 4
        for msg in messages
    )

    if total_tokens <= max_tokens:
        return messages

    # Strategies:
    # 1. Summarize old messages
    # 2. Remove least important messages
    # 3. Keep only recent context

    # Simple: Keep only recent messages
    while total_tokens > max_tokens:
        messages.pop(0)  # Remove oldest
        total_tokens = sum(len(msg["content"]) // 4 for msg in messages)

    return messages
```

### 6. Connection Pooling

```python
from anthropic import AsyncAnthropic
import httpx

# Reuse connections
async with httpx.AsyncClient(
    limits=httpx.Limits(max_keepalive_connections=20)
) as http_client:
    client = AsyncAnthropic(http_client=http_client)

    # All requests reuse connections
    results = await asyncio.gather(*[
        client.messages.create(
            model="claude-sonnet-4-5-20250929",
            messages=[{"role": "user", "content": f"Query {i}"}]
        )
        for i in range(10)
    ])
```

### 7. Response Length Control

```python
# Limit response length for faster responses
response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=256,  # Shorter = faster
    messages=[{
        "role": "user",
        "content": "Briefly explain quantum computing"
    }]
)
```

## Performance Benchmarks

```python
import time
import statistics

def benchmark_agent(agent_func, num_runs: int = 10):
    """Benchmark agent performance"""

    times = []
    tokens = []

    for i in range(num_runs):
        start = time.time()

        result = agent_func(f"Test query {i}")

        elapsed = time.time() - start
        times.append(elapsed)

        # Estimate tokens
        token_count = len(result["messages"][-1].content) // 4
        tokens.append(token_count)

    print(f"Performance Metrics:")
    print(f"  Average latency: {statistics.mean(times):.2f}s")
    print(f"  P95 latency: {statistics.quantiles(times, n=20)[18]:.2f}s")
    print(f"  Average tokens: {statistics.mean(tokens):.0f}")
    print(f"  Total tokens: {sum(tokens)}")
```

## Best Practices

1. **Measure First**: Baseline before optimizing
2. **Optimize Hot Paths**: Focus on frequently used code
3. **Use Streaming**: Better UX for long responses
4. **Cache Aggressively**: Especially system prompts
5. **Right-Size Models**: Match model to task complexity
6. **Batch Requests**: Reduce overhead
7. **Manage Context**: Don't send unnecessary tokens
8. **Pool Connections**: Reuse HTTP connections
9. **Monitor Continuously**: Track performance metrics
10. **Test at Scale**: Validate under load

## Cost Optimization

```python
def calculate_cost(tokens_used: int, model: str) -> float:
    """Calculate API cost"""

    pricing = {
        "claude-haiku-3-5-20250222": 0.25 / 1_000_000,
        "claude-sonnet-4-5-20250929": 3.0 / 1_000_000,
        "claude-opus-4-5-20250229": 15.0 / 1_000_000,
    }

    return tokens_used * pricing[model]

# Example: Compare costs
haiku_cost = calculate_cost(10000, "claude-haiku-3-5-20250222")
sonnet_cost = calculate_cost(10000, "claude-sonnet-4-5-20250929")

print(f"Haiku: ${haiku_cost:.4f}")
print(f"Sonnet: ${sonnet_cost:.4f}")
print(f"Savings with Haiku: {(1 - haiku_cost/sonnet_cost):.1%}")
```

This skill ensures agents run as fast and cost-effectively as possible.
