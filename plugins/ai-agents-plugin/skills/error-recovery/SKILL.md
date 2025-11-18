---
name: error-recovery
description: Master error handling and recovery for AI agents with retry logic and fallbacks. Use when implementing resilience, handling API failures, managing timeouts, implementing circuit breakers, designing fault tolerance, or ensuring reliable agent operation under failure conditions.
allowed-tools: Read, Write, Bash
---

# Error Recovery Skill

Automatically handle errors and implement recovery strategies for robust agent execution through exponential backoff, circuit breakers, fallbacks, and graceful degradation.

## When to Use This Skill

1. **Resilience Design** - Building fault-tolerant agents
2. **API Failure Handling** - Recovering from API errors
3. **Timeout Management** - Handling slow operations
4. **Circuit Breaker Setup** - Preventing cascading failures
5. **Retry Logic** - Implementing smart retries
6. **Fallback Strategies** - Providing alternative responses
7. **Rate Limit Handling** - Recovering from rate limits
8. **Network Issues** - Handling connectivity problems
9. **Graceful Degradation** - Maintaining partial functionality
10. **Error Classification** - Categorizing errors for appropriate handling
11. **Monitoring Integration** - Tracking error patterns
12. **Production Deployment** - Ensuring reliability at scale
13. **Chaos Engineering** - Testing failure scenarios
14. **SLA Compliance** - Meeting availability requirements
15. **Incident Response** - Automated recovery procedures

## Quick Start

```python
# Quick error recovery setup
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=10)
)
async def resilient_agent_call(message: str):
    try:
        result = await agent.ainvoke({
            "messages": [{"role": "user", "content": message}]
        })
        return result
    except RateLimitError:
        # Wait longer for rate limits
        await asyncio.sleep(60)
        raise  # Retry
    except TimeoutError:
        # Use cached response if available
        return get_cached_response(message)
```

## Related Skills

- **security-validation**: Ensures error handling maintains security
- **performance-tuning**: Optimizes retry and fallback performance
- **agent-monitoring**: Tracks error rates and recovery success

This skill ensures AI agents handle errors gracefully and continue operating reliably even when issues occur.
