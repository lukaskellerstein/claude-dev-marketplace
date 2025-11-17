# AI Agent Plugin v2.0

Comprehensive AI agent orchestration toolkit for building, deploying, and managing AI agents using Claude SDK, LangChain 1.0, LangGraph 1.0, and Microsoft Agent Framework.

## Overview

This plugin provides everything you need to build production-ready AI agents:

- **LangChain 1.0**: Fast agent development with `create_agent` and middleware
- **LangGraph 1.0**: Production-ready stateful workflows with durability
- **Microsoft Agent Framework**: Enterprise multi-agent orchestration
- **Claude-Optimized**: Best practices for Claude and Anthropic API
- **Production-Ready**: Security, monitoring, and deployment tools

## Installation

1. Install the plugin in Claude Code:
   ```bash
   # Plugin will be automatically loaded from marketplace
   ```

2. Install required Python packages (optional, will be installed on first use):
   ```bash
   pip install langchain>=1.0.0 langgraph>=1.0.0 langchain-anthropic
   pip install agent-framework --pre  # For Microsoft Agent Framework
   ```

## Quick Start

### Create a LangChain 1.0 Agent

```bash
/agent create my-assistant
```

This creates a new agent using LangChain's `create_agent` with tools and middleware support.

### Create a LangGraph Workflow

```bash
/workflow create my-workflow
```

This creates a stateful workflow with checkpointing and human-in-the-loop patterns.

### Create a Microsoft Agent

```bash
/microsoft-agent create multi-agent research-team
```

This creates a multi-agent system using Microsoft Agent Framework.

## Commands

### `/agent` - LangChain 1.0 Agent Management

```bash
/agent create <name>           # Create new agent
/agent list                    # List all agents
/agent run <name>              # Run agent
/agent add-middleware <name>   # Add middleware
/agent update <name>           # Update configuration
/agent delete <name>           # Delete agent
```

**Key Features:**
- Uses `create_agent` (no chains)
- Built on LangGraph runtime
- Middleware system for customization
- Memory and checkpointing support

### `/workflow` - LangGraph 1.0 Workflows

```bash
/workflow create <name>        # Create workflow
/workflow checkpoint <name>    # Enable checkpointing
/workflow visualize <name>     # Generate diagram
/workflow deploy <name>        # Deploy to production
```

**Key Features:**
- Durable execution
- Checkpointing and resume
- Human-in-the-loop patterns
- Time-travel debugging
- Battle-tested at scale

### `/microsoft-agent` - Microsoft Agent Framework

```bash
/microsoft-agent create <type> <name>   # Create agent
  Types: chat, multi-agent, workflow, supervised
/microsoft-agent migrate-autogen        # Migrate from AutoGen
/microsoft-agent deploy <name>          # Deploy to Azure
```

**Key Features:**
- Unified AutoGen + Semantic Kernel
- Enterprise features built-in
- Azure AI Foundry integration
- Python & .NET support

### `/deploy` - Production Deployment

```bash
/deploy docker <agent>         # Deploy as Docker container
/deploy kubernetes <agent>     # Deploy to Kubernetes
/deploy aws-lambda <agent>     # Deploy to AWS Lambda
/deploy azure <agent>          # Deploy to Azure AI Foundry
/deploy local <agent>          # Run as local service
```

**Key Features:**
- Automatic containerization
- Environment management
- Health checks
- Auto-scaling configuration

### `/test` - Agent Testing

```bash
/test unit <agent>             # Run unit tests
/test integration <agent>      # Run integration tests
/test performance <agent>      # Benchmark performance
/test security <agent>         # Security validation
/test all <agent>              # Run all tests
```

**Key Features:**
- Automated test generation
- Performance benchmarks
- Security validation
- Coverage reports

## Sub-Agents

Specialized agents that help you build better agents:

### `langchain-builder`
Expert in LangChain 1.0 patterns, `create_agent`, and middleware.

### `langgraph-designer`
Expert in LangGraph 1.0 workflows, checkpointing, and production patterns.

### `microsoft-orchestrator`
Expert in Microsoft Agent Framework, multi-agent systems, and Azure integration.

### `memory-specialist`
Expert in agent memory management, persistence, and context handling.

### `claude-architect`
Expert in Claude-specific optimizations and Anthropic best practices.

## Skills

Auto-activating skills that enhance agent development:

### `agent-monitoring`
Automatically monitors performance, token usage, and response times.

### `error-recovery`
Implements retry logic, fallbacks, and graceful error handling.

### `performance-tuning`
Optimizes latency, reduces token usage, and minimizes costs.

### `security-validation`
Validates security, prevents prompt injection, and protects sensitive data.

## Framework Updates (v2.0)

### LangChain 1.0
- ❌ **Removed**: Chains, `initialize_agent`, `AgentExecutor`
- ✅ **New**: `create_agent()` function
- ✅ **New**: Middleware system
- ✅ **New**: Built on LangGraph runtime
- 📦 **Legacy**: Old patterns in `langchain-classic`

### LangGraph 1.0
- ✅ **Production**: Battle-tested at Uber, LinkedIn, Klarna
- ✅ **Durable**: Checkpointing and persistence
- ✅ **Features**: Human-in-the-loop, time-travel, streaming
- ✅ **Stable**: No breaking changes until 2.0

### Microsoft Agent Framework
- ✅ **New**: Replaces AutoGen and Semantic Kernel
- ✅ **Unified**: Single framework for all patterns
- ✅ **Enterprise**: Security, observability, Azure
- ⚠️ **AutoGen**: Maintenance mode (bug fixes only)

## Examples

### Simple LangChain Agent

```python
from langchain.agents import create_agent
from langchain_anthropic import ChatAnthropic
from langchain_core.tools import tool

@tool
def search(query: str) -> str:
    """Search for information."""
    return f"Results for: {query}"

agent = create_agent(
    model="anthropic:claude-sonnet-4-5-20250929",
    tools=[search],
    system_prompt="You are a helpful assistant.",
)

result = agent.invoke({
    "messages": [{"role": "user", "content": "Hello!"}]
})
```

### LangGraph Workflow

```python
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.sqlite import SqliteSaver

workflow = StateGraph(MyState)
workflow.add_node("process", process_node)
workflow.add_edge("process", END)

checkpointer = SqliteSaver.from_conn_string("./checkpoints.db")
app = workflow.compile(checkpointer=checkpointer)
```

### Microsoft Multi-Agent

```python
from agent_framework import Agent, Workflow

researcher = Agent(
    name="Researcher",
    instructions="Research topics thoroughly."
)

writer = Agent(
    name="Writer",
    instructions="Write clear content."
)

workflow = Workflow()
workflow.add_executor("research", researcher)
workflow.add_executor("write", writer)
workflow.add_edge("research", "write")
```

## MCP Integration

The plugin includes MCP servers for:
- Filesystem access (agent code)
- Database access (checkpoints, memory)
- GitHub integration
- Web search
- LangSmith observability

## Best Practices

1. **Start with LangChain 1.0**: Use `create_agent` for new agents
2. **Add Middleware**: Include human-in-the-loop and PII redaction
3. **Enable Checkpointing**: Always use for production workflows
4. **Monitor Performance**: Track metrics from day one
5. **Test Security**: Run security validation before deployment
6. **Use Right Model**: Match model to task complexity
7. **Optimize Costs**: Monitor token usage and optimize
8. **Document Agents**: Clear documentation for maintenance

## Migration Guide

### From LangChain pre-1.0

```python
# OLD
from langchain.agents import initialize_agent
agent = initialize_agent(tools=tools, llm=llm)

# NEW
from langchain.agents import create_agent
agent = create_agent(
    model="anthropic:claude-sonnet-4-5-20250929",
    tools=tools
)
```

### From AutoGen

```python
# OLD
from autogen import AssistantAgent, GroupChat
assistant = AssistantAgent(name="assistant")
group_chat = GroupChat(agents=[assistant])

# NEW
from agent_framework import Agent, Workflow
assistant = Agent(name="assistant")
workflow = Workflow()
workflow.add_executor("assistant", assistant)
```

## Troubleshooting

### LangChain not installed
```bash
pip install langchain>=1.0.0 langchain-anthropic
```

### LangGraph not installed
```bash
pip install langgraph>=1.0.0
```

### Microsoft Agent Framework not installed
```bash
pip install agent-framework --pre
```

## Resources

- [LangChain 1.0 Docs](https://python.langchain.com/)
- [LangGraph Docs](https://langchain-ai.github.io/langgraph/)
- [Microsoft Agent Framework](https://learn.microsoft.com/agent-framework/)
- [Anthropic API Docs](https://docs.anthropic.com/)
- [Claude Code Docs](https://code.claude.com/docs)

## Support

For issues and feature requests, please use the plugin's GitHub repository.

## License

MIT

---

**Plugin Version**: 2.0.0
**Last Updated**: November 2025
**Maintained by**: Claude Code Team
