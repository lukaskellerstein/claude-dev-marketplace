---
description: Design and implement durable workflows with Temporal.io for long-running processes, agent orchestration, and reliable automation
---

Design and implement a durable workflow using Temporal.io with proper error handling, state management, and AI agent integration.

## Process

Follow these steps:

1. **Analyze Workflow Requirements**: Understand the workflow goals and constraints
   - Workflow steps and dependencies
   - Expected duration (minutes, hours, days, weeks)
   - Failure scenarios and compensation needs
   - External system integrations
   - Human-in-the-loop requirements
   - Scale requirements (concurrent workflows)
   - Review existing codebase if applicable

2. **Design Workflow**: Use the `aiagent-plugin:workflow-automation-expert` agent to:
   - Model workflow as state machine
   - Break down into activities
   - Design retry and timeout policies
   - Plan compensation logic
   - Design state management
   - Plan monitoring and observability
   - Consider versioning strategy

3. **AI Agent Integration** (if needed): If workflow includes AI agents, use:
   - `aiagent-plugin:claude-agent-expert` for Claude-powered activities
   - `aiagent-plugin:langchain-expert` for complex agent chains in activities
   - `aiagent-plugin:agent-orchestration-expert` for multi-agent coordination

4. **Implementation Guide**: Provide:
   - Complete Temporal workflow code
   - Activity implementations
   - Worker configuration
   - Testing strategy
   - Deployment guide

## Output

Present a comprehensive workflow implementation including:

### Workflow Overview
- Workflow purpose and business logic
- Step-by-step flow description
- State machine diagram
- Expected duration and SLAs
- Failure scenarios and handling
- Why Temporal is the right choice

### Workflow Definition
```python
# Temporal workflow class
# Workflow method with activities
# Signal handlers for external updates
# Query handlers for state inspection
# Workflow configuration (timeouts, retry policies)
```

### Activity Definitions
For each activity:
- Activity purpose and logic
- Input/output schemas
- Retry policy configuration
- Timeout configuration
- Heartbeat implementation (if long-running)
- Cancellation handling
- Error handling strategy
- Activity implementation code

### State Management
- Workflow state schema
- State transitions and conditions
- State persistence approach
- State querying mechanisms
- Workflow ID strategy
- Search attributes for querying

### Error Handling Strategy
- Retry policies per activity
- Timeout configurations
- Compensation logic for failures
- Dead letter queue setup
- Alert conditions
- Recovery procedures
- Circuit breakers for external services

### AI Agent Activities
(If workflow includes AI agents)
- Agent initialization in activities
- Prompt design for workflow context
- Agent timeout handling
- Result validation
- Cost tracking per workflow
- Rate limiting strategy
- Fallback logic for agent failures

### Workflow Configuration
```python
# Temporal client setup
# Worker configuration
# Task queue setup
# Namespace configuration
# Workflow options (ID, timeouts, retry)
# Activity options (scheduleToClose, startToClose)
```

### Testing Strategy
- Workflow replay tests
- Activity unit tests
- Integration tests
- Failure scenario tests
- Time-travel testing (Temporal feature)
- Load testing approach

### Monitoring and Observability
- Key workflow metrics
- Activity execution tracking
- Custom search attributes
- Logging strategy
- Alerting rules
- Temporal UI usage
- Custom dashboards

### Deployment Guide
- Temporal cluster setup (or Temporal Cloud)
- Worker deployment strategy
- Scaling workers (horizontal)
- Worker versioning
- Workflow versioning and migration
- Configuration management
- Secrets management

### Example Workflow Execution
```python
# How to start workflow
# How to signal workflow
# How to query workflow state
# How to cancel workflow
# How to handle results
```

### Cost and Performance
- Estimated workflow execution time
- Resource requirements per worker
- Temporal cluster costs (if self-hosted)
- API costs (if using AI agents)
- Optimization opportunities
- Scaling characteristics

## Examples

### Data Processing Pipeline
```
/implement-workflow

Create a data processing workflow that:
- Ingests data from S3
- Validates and cleans data
- Transforms with multiple steps
- Writes to database
- Sends notification on completion
- Runs daily on schedule
- Handles retries for transient failures
```

### AI-Powered Content Generation
```
/implement-workflow

Build a content generation workflow that:
- Receives content request
- Uses Claude to research topic
- Generates draft content
- Uses AI for editing and refinement
- Sends for human approval (signal)
- Publishes approved content
- Tracks workflow progress
```

### Order Fulfillment Workflow
```
/implement-workflow

Create order fulfillment with saga pattern:
- Reserve inventory
- Process payment
- Ship order
- Send notifications
- Compensating transactions on failure
- Human escalation for issues
- Multi-day execution window
```

### ML Training Pipeline
```
/implement-workflow

Build ML training workflow that:
- Prepares training data
- Trains model (long-running, with heartbeats)
- Validates model performance
- Deploys if metrics pass
- Rolls back if validation fails
- Notifies team on completion
- Runs on GPU worker pool
```

### Multi-Agent Research Workflow
```
/implement-workflow

Create research automation workflow:
- Research agent gathers information
- Analysis agent processes findings
- Writing agent creates report
- Review agent checks quality
- Human approval before publishing
- Retry failed agent activities
- Track cost and token usage
```

## Workflow Patterns Applied

### Sequential Execution
- Linear sequence of activities
- Each step depends on previous
- Simple retry and error handling

### Parallel Execution (Fan-out/Fan-in)
- Multiple activities run in parallel
- Aggregate results when all complete
- Optimal for independent operations

### Long-Running with Signals
- Workflow waits for external events
- Signal handlers update state
- Human-in-the-loop approvals
- Can run for days/weeks

### Saga Pattern
- Sequential execution with compensation
- Rollback on any failure
- Distributed transaction simulation
- Critical for financial workflows

### Child Workflows
- Complex workflows as children
- Better organization and versioning
- Independent retry policies
- Reusable sub-workflows

### Scheduled/Cron Workflows
- Periodic execution
- Automatic retries
- Overlap prevention
- Ideal for batch processing

## Best Practices Applied

- **Deterministic Workflows**: No random, no I/O in workflow code
- **Idempotent Activities**: Activities can be retried safely
- **Appropriate Timeouts**: Realistic time limits for each activity
- **Heartbeats**: For activities longer than 10 seconds
- **Signals for Updates**: External communication via signals
- **Queries for State**: Non-blocking state inspection
- **Versioning**: Safe workflow evolution
- **Monitoring**: Comprehensive observability
- **Testing**: Replay tests and scenarios
- **Documentation**: Clear workflow behavior

## Temporal Configuration Examples

### Retry Policy (Exponential Backoff)
```python
retry_policy = RetryPolicy(
    initial_interval=timedelta(seconds=1),
    backoff_coefficient=2.0,
    maximum_interval=timedelta(minutes=5),
    maximum_attempts=10,
)
```

### Activity Timeouts
```python
activity_options = {
    "schedule_to_close_timeout": timedelta(hours=1),  # Overall timeout
    "start_to_close_timeout": timedelta(minutes=30),   # Execution timeout
    "heartbeat_timeout": timedelta(seconds=30),        # Heartbeat timeout
    "retry_policy": retry_policy,
}
```

### Workflow Timeouts
```python
workflow_options = {
    "id": f"order-{order_id}",
    "task_queue": "order-processing",
    "execution_timeout": timedelta(days=7),  # Maximum workflow duration
    "workflow_id_reuse_policy": WorkflowIdReusePolicy.REJECT_DUPLICATE,
}
```

## Integration with Other Systems

- **Databases**: Store workflow data and results
- **Message Queues**: Trigger workflows from events
- **APIs**: Call external services in activities
- **AI Agents**: Integrate Claude, GPT, or custom agents
- **Monitoring**: Send metrics to Datadog, Grafana
- **Notification**: Email, Slack, webhooks

Provide production-ready, durable workflow implementations with comprehensive error handling, monitoring, and operational excellence.
