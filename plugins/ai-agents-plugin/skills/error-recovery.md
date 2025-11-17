---
name: error-recovery
description: Automatically handle and recover from agent errors with retry logic and fallbacks
allowed-tools: Read, Write, Bash
---

# Error Recovery Skill

This skill automatically handles errors and implements recovery strategies for robust agent execution.

## When This Activates

This skill activates when:
- Agent encounters an error
- Tool calls fail
- API rate limits are hit
- Network issues occur
- Timeouts happen

## What It Does

### 1. Automatic Retry

Implements exponential backoff:
- Retry failed operations
- Increase wait time between attempts
- Maximum retry limit
- Different strategies per error type

### 2. Fallback Strategies

Provides alternatives:
- Use backup models
- Simplify requests
- Cache responses
- Graceful degradation

### 3. Error Classification

Categorizes errors:
- Transient (retry)
- Permanent (fail fast)
- Rate limit (backoff)
- Invalid input (fix and retry)

## Implementation

```python
import asyncio
import time
from typing import Callable, Any, Optional
from anthropic import APIError, RateLimitError

class ErrorRecovery:
    def __init__(self, max_retries: int = 3, base_delay: float = 1.0):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.error_counts = {}

    async def retry_with_backoff(
        self,
        func: Callable,
        *args,
        **kwargs
    ) -> Any:
        """Retry function with exponential backoff"""
        last_exception = None

        for attempt in range(self.max_retries):
            try:
                result = await func(*args, **kwargs)
                return result

            except RateLimitError as e:
                # Rate limit - exponential backoff
                wait_time = self.base_delay * (2 ** attempt)
                print(f"Rate limit hit. Waiting {wait_time}s...")
                await asyncio.sleep(wait_time)
                last_exception = e

            except APIError as e:
                # API error - retry with backoff
                if attempt < self.max_retries - 1:
                    wait_time = self.base_delay * (1.5 ** attempt)
                    print(f"API error. Retrying in {wait_time}s...")
                    await asyncio.sleep(wait_time)
                last_exception = e

            except TimeoutError as e:
                # Timeout - retry with longer timeout
                if attempt < self.max_retries - 1:
                    print(f"Timeout. Retrying with extended timeout...")
                    kwargs['timeout'] = kwargs.get('timeout', 30) * 1.5
                last_exception = e

            except Exception as e:
                # Unknown error - fail fast
                print(f"Unexpected error: {e}")
                raise

        # All retries exhausted
        raise last_exception

    async def with_fallback(
        self,
        primary_func: Callable,
        fallback_func: Callable,
        *args,
        **kwargs
    ) -> Any:
        """Try primary function, fallback to alternative on failure"""
        try:
            return await primary_func(*args, **kwargs)
        except Exception as e:
            print(f"Primary failed: {e}. Using fallback...")
            return await fallback_func(*args, **kwargs)

    def track_error(self, error_type: str):
        """Track error frequency"""
        self.error_counts[error_type] = self.error_counts.get(error_type, 0) + 1

    def get_error_stats(self) -> dict:
        """Get error statistics"""
        return self.error_counts.copy()
```

## Usage Examples

### Basic Retry

```python
recovery = ErrorRecovery(max_retries=3)

async def call_agent(message):
    return await agent.ainvoke({
        "messages": [{"role": "user", "content": message}]
    })

# Automatically retries on failure
result = await recovery.retry_with_backoff(call_agent, "Hello")
```

### Fallback Model

```python
async def call_primary_model(message):
    return await client.messages.create(
        model="claude-sonnet-4-5-20250929",
        messages=[{"role": "user", "content": message}]
    )

async def call_fallback_model(message):
    return await client.messages.create(
        model="claude-haiku-3-5-20250222",
        messages=[{"role": "user", "content": message}]
    )

# Try Sonnet, fallback to Haiku if needed
result = await recovery.with_fallback(
    call_primary_model,
    call_fallback_model,
    "Hello"
)
```

### Circuit Breaker

```python
class CircuitBreaker:
    def __init__(self, failure_threshold: int = 5, timeout: float = 60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "closed"  # closed, open, half-open

    async def call(self, func: Callable, *args, **kwargs):
        """Call function with circuit breaker pattern"""

        # Check if circuit should reset
        if self.state == "open":
            if time.time() - self.last_failure_time > self.timeout:
                self.state = "half-open"
                self.failure_count = 0
            else:
                raise Exception("Circuit breaker is OPEN")

        try:
            result = await func(*args, **kwargs)

            # Success - reset circuit
            if self.state == "half-open":
                self.state = "closed"
            self.failure_count = 0

            return result

        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = time.time()

            # Open circuit if threshold exceeded
            if self.failure_count >= self.failure_threshold:
                self.state = "open"
                print("Circuit breaker opened!")

            raise
```

### Error Context

```python
class ErrorContext:
    """Provide context for error recovery"""

    def __init__(self):
        self.context = {}

    def add_context(self, key: str, value: Any):
        """Add context information"""
        self.context[key] = value

    def get_recovery_strategy(self, error: Exception) -> str:
        """Determine recovery strategy based on context"""

        if isinstance(error, RateLimitError):
            return "exponential_backoff"

        elif isinstance(error, TimeoutError):
            if self.context.get("is_large_request"):
                return "split_request"
            return "increase_timeout"

        elif "model" in str(error):
            return "fallback_model"

        return "retry"
```

## Best Practices

1. **Classify Errors**: Different recovery for different errors
2. **Exponential Backoff**: Prevent thundering herd
3. **Circuit Breaker**: Stop cascading failures
4. **Fallback Options**: Always have a Plan B
5. **Log Everything**: Track all errors
6. **Set Limits**: Don't retry forever
7. **Monitor Patterns**: Watch error trends
8. **Test Recovery**: Simulate failures
9. **Graceful Degradation**: Reduced functionality > no functionality
10. **User Communication**: Explain what's happening

## Integration with Workflows

```python
from langgraph.graph import StateGraph

# Add error recovery to workflow nodes
async def resilient_node(state):
    recovery = ErrorRecovery()

    result = await recovery.retry_with_backoff(
        process_with_llm,
        state["messages"]
    )

    return {"messages": result}
```

This skill ensures agents handle errors gracefully and continue operating even when issues occur.
