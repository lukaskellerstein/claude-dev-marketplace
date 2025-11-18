---
description: Create and manage AI agents using LangChain 1.0
---

# Agent Command (LangChain 1.0)

Create, configure, and manage AI agents using LangChain's create_agent with middleware.

## Usage

`/agent [action] [name] [options]`

## Actions

- `create` - Create new agent with create_agent
- `list` - List existing agents
- `run` - Run agent with input
- `add-middleware` - Add middleware to agent
- `update` - Update agent configuration
- `delete` - Delete agent

## Key Changes in LangChain 1.0

- **No more chains**: Use `create_agent` instead
- **Built on LangGraph**: Agents use LangGraph runtime for durability
- **Middleware system**: Add custom behavior without rewriting logic
- **Legacy chains**: Available in `langchain-classic` package

## Implementation

!`
#!/bin/bash

ACTION=$1
NAME=$2
OPTIONS=$3

# Check LangChain version
check_version() {
    echo "Checking LangChain version..."
    python3 -c "import langchain; print(f'LangChain: {langchain.__version__}')" || {
        echo "Installing LangChain 1.0..."
        pip install --break-system-packages "langchain>=1.0.0" langchain-anthropic
    }
}

case $ACTION in
    create)
        check_version
        echo "Creating LangChain 1.0 agent: $NAME"
        mkdir -p "./agents/$NAME"

        # Create agent using create_agent
        cat > "./agents/$NAME/agent.py" << 'EOPYTHON'
from langchain.agents import create_agent
from langchain_anthropic import ChatAnthropic
from langchain_core.tools import tool

# Define tools
@tool
def search_tool(query: str) -> str:
    """Search for information."""
    return f"Search results for: {query}"

@tool
def calculator(expression: str) -> str:
    """Calculate mathematical expressions."""
    try:
        return str(eval(expression))
    except Exception as e:
        return f"Error: {e}"

# Create agent with middleware
agent = create_agent(
    model="anthropic:claude-sonnet-4-5-20250929",
    tools=[search_tool, calculator],
    system_prompt="You are a helpful assistant.",
    middleware=[],  # Add middleware here
)

# Run agent
if __name__ == "__main__":
    result = agent.invoke({
        "messages": [{"role": "user", "content": "What is 2+2?"}]
    })
    print(result["messages"][-1].content)
EOPYTHON

        echo "Agent created at ./agents/$NAME/agent.py"
        echo "Use 'add-middleware' to add custom behavior"
        ;;

    add-middleware)
        echo "Adding middleware to agent: $NAME"
        echo "Available middleware types:"
        echo "  - human-in-the-loop: Human approval before actions"
        echo "  - conversation-summary: Compress long conversations"
        echo "  - pii-redaction: Remove sensitive information"
        echo "  - custom: Your own middleware"

        # Example middleware addition
        cat >> "./agents/$NAME/agent.py" << 'EOPYTHON'

# Add middleware
from langchain.agents.middleware import (
    HumanInTheLoopMiddleware,
    ConversationSummaryMiddleware
)

# Update agent with middleware
agent = create_agent(
    model="anthropic:claude-sonnet-4-5-20250929",
    tools=[search_tool, calculator],
    system_prompt="You are a helpful assistant.",
    middleware=[
        HumanInTheLoopMiddleware(),
        ConversationSummaryMiddleware(),
    ]
)
EOPYTHON
        ;;

    list)
        echo "Listing all agents..."
        find . -name "agent.py" -path "*/agents/*" | while read agent; do
            dir=$(dirname $agent)
            echo "  - $(basename $dir)"
        done
        ;;

    run)
        if [ -z "$NAME" ]; then
            echo "Error: Agent name required"
            exit 1
        fi
        echo "Running agent: $NAME"
        echo "Input: $OPTIONS"
        python3 "./agents/$NAME/agent.py"
        ;;

    update)
        echo "Updating agent: $NAME"
        # Update agent configuration
        ;;

    delete)
        echo "Deleting agent: $NAME"
        rm -rf "./agents/$NAME"
        ;;

    *)
        echo "Usage: /agent [create|list|run|add-middleware|update|delete] [name]"
        exit 1
        ;;
esac
`
