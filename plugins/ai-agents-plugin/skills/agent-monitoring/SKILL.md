---
name: agent-monitoring
description: Master AI agent performance monitoring, tracking token usage and response times. Use when setting up observability, tracking metrics, implementing alerts, analyzing performance trends, debugging issues, capacity planning, or ensuring agent SLA compliance.
allowed-tools: Read, Write, Bash
---

# Agent Monitoring Skill

Automatically monitor AI agent performance, track key metrics, and provide actionable insights through comprehensive observability including latency tracking, token usage, error rates, and cost analysis.

## When to Use This Skill

1. **Performance Tracking** - Monitoring agent response times
2. **Cost Analysis** - Tracking token usage and API costs
3. **Error Detection** - Identifying failure patterns
4. **SLA Compliance** - Ensuring performance targets
5. **Capacity Planning** - Predicting resource needs
6. **Debugging Issues** - Investigating performance problems
7. **Alert Configuration** - Setting up proactive alerts
8. **Trend Analysis** - Understanding usage patterns
9. **Production Deployment** - Real-time monitoring
10. **Optimization Validation** - Measuring improvement impact
11. **User Experience** - Tracking end-user satisfaction
12. **Resource Utilization** - Optimizing infrastructure
13. **Anomaly Detection** - Identifying unusual patterns
14. **Compliance Reporting** - Generating audit reports
15. **Continuous Improvement** - Data-driven optimization

## Quick Start

```python
# Quick monitoring setup
class AgentMonitor:
    def track_request(self, agent_name, response_time, tokens, success):
        self.metrics.append({
            "agent": agent_name,
            "timestamp": time.time(),
            "response_time": response_time,
            "tokens": tokens,
            "success": success
        })

    def get_stats(self):
        return {
            "avg_response_time": statistics.mean([m["response_time"] for m in self.metrics]),
            "p95_response_time": statistics.quantiles([m["response_time"] for m in self.metrics], n=20)[18],
            "success_rate": sum(1 for m in self.metrics if m["success"]) / len(self.metrics),
            "total_tokens": sum(m["tokens"] for m in self.metrics)
        }
```

## Integration with LangSmith

```python
# LangSmith automatically tracks:
# - All agent executions
# - Token usage
# - Latency
# - Errors
# - Tool calls

import os
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "your-key"

# Your agent automatically sends metrics to LangSmith
```

## Related Skills

- **performance-tuning**: Uses monitoring data for optimization
- **error-recovery**: Tracks error patterns and recovery success
- **security-validation**: Monitors security events

This skill ensures comprehensive visibility into agent performance, enabling data-driven optimization and reliable operation.
