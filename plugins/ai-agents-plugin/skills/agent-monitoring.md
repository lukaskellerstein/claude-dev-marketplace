---
name: agent-monitoring
description: Automatically monitor agent performance, token usage, and response times
allowed-tools: Read, Write, Bash
---

# Agent Monitoring Skill

This skill automatically monitors agent performance metrics during development and execution.

## When This Activates

This skill activates when:
- Creating new agents
- Running agent workflows
- Deploying agents to production
- Testing agent performance

## What It Does

### 1. Performance Tracking

Monitors key metrics:
- Response time
- Token usage
- Success rate
- Error rate
- Tool call frequency

### 2. Real-Time Alerts

Alerts when:
- Response time exceeds threshold
- Token usage is high
- Error rate increases
- Tool calls fail

### 3. Usage Analytics

Tracks:
- Total requests
- Average response time
- Token consumption
- Cost estimates
- Peak usage times

## Implementation

```python
import time
import statistics
from typing import Dict, List

class AgentMonitor:
    def __init__(self):
        self.metrics: List[Dict] = []

    def track_request(self, agent_name: str, response_time: float,
                     tokens_used: int, success: bool):
        """Track individual request metrics"""
        self.metrics.append({
            "agent": agent_name,
            "timestamp": time.time(),
            "response_time": response_time,
            "tokens": tokens_used,
            "success": success
        })

    def get_statistics(self, agent_name: str = None):
        """Get performance statistics"""
        metrics = self.metrics
        if agent_name:
            metrics = [m for m in metrics if m["agent"] == agent_name]

        if not metrics:
            return {}

        response_times = [m["response_time"] for m in metrics]
        tokens = [m["tokens"] for m in metrics]
        success_count = sum(1 for m in metrics if m["success"])

        return {
            "total_requests": len(metrics),
            "success_rate": success_count / len(metrics),
            "avg_response_time": statistics.mean(response_times),
            "p95_response_time": statistics.quantiles(response_times, n=20)[18],
            "total_tokens": sum(tokens),
            "avg_tokens": statistics.mean(tokens),
        }

    def check_alerts(self):
        """Check for performance alerts"""
        stats = self.get_statistics()

        alerts = []

        if stats.get("avg_response_time", 0) > 5.0:
            alerts.append("⚠️ High response time detected")

        if stats.get("success_rate", 1.0) < 0.95:
            alerts.append("⚠️ Low success rate detected")

        return alerts
```

## Usage Example

```python
# Wrap agent calls with monitoring
monitor = AgentMonitor()

start = time.time()
try:
    result = agent.invoke({"messages": [message]})
    response_time = time.time() - start

    tokens_used = len(result["messages"][-1].content) // 4

    monitor.track_request(
        agent_name="my-agent",
        response_time=response_time,
        tokens_used=tokens_used,
        success=True
    )
except Exception as e:
    response_time = time.time() - start
    monitor.track_request(
        agent_name="my-agent",
        response_time=response_time,
        tokens_used=0,
        success=False
    )

# Check for alerts
alerts = monitor.check_alerts()
for alert in alerts:
    print(alert)

# Get statistics
stats = monitor.get_statistics("my-agent")
print(f"Average response time: {stats['avg_response_time']:.2f}s")
print(f"Success rate: {stats['success_rate']:.2%}")
```

## Best Practices

1. **Monitor Early**: Start tracking from first agent run
2. **Set Baselines**: Establish performance expectations
3. **Alert on Anomalies**: Catch issues before users do
4. **Track Costs**: Monitor token usage and costs
5. **Analyze Trends**: Look for performance degradation
6. **Export Metrics**: Send to monitoring systems
7. **Dashboard**: Visualize key metrics
8. **Set SLOs**: Define service level objectives

## Integration with LangSmith

```python
from langsmith import Client

client = Client()

# LangSmith automatically tracks:
# - All LangChain/LangGraph executions
# - Token usage
# - Latency
# - Errors
# - Tool calls

# Enable tracing
import os
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "your-key"

# Your agent automatically sends metrics to LangSmith
result = agent.invoke(messages)
```

This skill ensures agents are performing well and alerts you to issues proactively.
