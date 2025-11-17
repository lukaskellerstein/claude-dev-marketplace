---
description: Create agents with Microsoft Agent Framework
allowed-tools: Bash, Read, Write
---

# Microsoft Agent Command

Create and manage agents using Microsoft Agent Framework (successor to AutoGen).

## Usage

`/microsoft-agent [action] [type] [name]`

## Actions

- `create` - Create new agent or workflow
- `add-tool` - Add tools to agent
- `workflow` - Create workflow orchestration
- `migrate-autogen` - Migrate from AutoGen
- `deploy` - Deploy to Azure AI Foundry

## Agent Types

- `chat` - Simple chat agent
- `multi-agent` - Multi-agent system
- `workflow` - Workflow-based orchestration
- `supervised` - Supervised agent team

## Key Features

- **Unified Framework**: Combines AutoGen + Semantic Kernel
- **Enterprise-Ready**: Production features built-in
- **Workflows**: Graph-based data flow orchestration
- **Python & .NET**: Full support for both platforms
- **Azure Integration**: Deploy to Azure AI Foundry

## Implementation

!`
#!/bin/bash

ACTION=$1
TYPE=$2
NAME=$3

check_agent_framework() {
    echo "Checking Microsoft Agent Framework..."
    python3 -c "import agent_framework; print('Agent Framework installed')" || {
        echo "Installing Microsoft Agent Framework..."
        pip install --break-system-packages agent-framework --pre
    }
}

case $ACTION in
    create)
        check_agent_framework
        echo "Creating Microsoft Agent Framework $TYPE: $NAME"
        mkdir -p "./microsoft-agents/$NAME"

        case $TYPE in
            chat)
                cat > "./microsoft-agents/$NAME/agent.py" << 'EOPYTHON'
import asyncio
from agent_framework.azure import AzureOpenAIResponsesClient
from azure.identity import DefaultAzureCredential

async def main():
    # Create simple chat agent
    agent = AzureOpenAIResponsesClient(
        credential=DefaultAzureCredential(),
    ).create_agent(
        name="ChatAgent",
        instructions="You are a helpful assistant.",
    )

    result = await agent.run("Hello! How can you help me?")
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
EOPYTHON
                ;;

            multi-agent)
                cat > "./microsoft-agents/$NAME/multi_agent.py" << 'EOPYTHON'
import asyncio
from agent_framework import Agent, Workflow
from agent_framework.tools import tool

@tool
async def research_tool(query: str) -> str:
    """Research information on a topic."""
    return f"Research results for: {query}"

@tool
async def write_tool(content: str) -> str:
    """Write content based on research."""
    return f"Written: {content}"

async def main():
    # Create specialized agents
    researcher = Agent(
        name="Researcher",
        instructions="Research topics thoroughly.",
        tools=[research_tool]
    )

    writer = Agent(
        name="Writer",
        instructions="Write clear, engaging content.",
        tools=[write_tool]
    )

    # Create workflow connecting agents
    workflow = Workflow()
    workflow.add_executor("research", researcher)
    workflow.add_executor("write", writer)
    workflow.add_edge("research", "write")

    # Run workflow
    result = await workflow.run({
        "task": "Research and write about AI agents"
    })
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
EOPYTHON
                ;;

            workflow)
                cat > "./microsoft-agents/$NAME/workflow.py" << 'EOPYTHON'
from agent_framework import Workflow, Agent
from agent_framework.middleware import LoggingMiddleware

# Create workflow-based orchestration
workflow = Workflow()

# Add agents as executors
analyst = Agent(
    name="Analyst",
    instructions="Analyze data and provide insights."
)

writer = Agent(
    name="Writer",
    instructions="Create reports from analysis."
)

# Build workflow graph
workflow.add_executor("analyze", analyst)
workflow.add_executor("write", writer)
workflow.add_edge("analyze", "write")

# Add middleware
workflow.add_middleware(LoggingMiddleware())

# Workflow supports:
# - Checkpointing
# - Human-in-the-loop
# - Parallel execution
# - Conditional routing
EOPYTHON
                ;;
        esac

        echo "Agent created at ./microsoft-agents/$NAME/"
        ;;

    migrate-autogen)
        echo "Migrating from AutoGen to Agent Framework..."
        echo "Migration Guide: https://learn.microsoft.com/agent-framework/migration-guide/from-autogen"
        echo ""
        echo "Key changes:"
        echo "  - GroupChat → Workflow"
        echo "  - AssistantAgent → Agent with create_agent"
        echo "  - Built-in middleware system"
        echo "  - Workflow-based orchestration"
        ;;

    deploy)
        echo "Deploying to Azure AI Foundry: $NAME"
        echo "Microsoft Agent Framework integrates with Azure AI Foundry"
        # Deploy to Azure
        ;;

    *)
        echo "Usage: /microsoft-agent [create|migrate-autogen|deploy] [type] [name]"
        exit 1
        ;;
esac
`
