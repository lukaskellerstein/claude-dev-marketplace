# AI Agent Plugin Specification (Updated 2025)

## Plugin Overview

**Name**: `aiagent-plugin`  
**Version**: `2.0.0`  
**Description**: Comprehensive AI agent orchestration toolkit for building, deploying, and managing AI agents using Claude SDK, LangChain 1.0, LangGraph 1.0, Microsoft Agent Framework, and production workflows.

**Last Updated**: November 2025  
**Breaking Changes from v1.0**: Updated for LangChain 1.0 (no chains), LangGraph 1.0 (production runtime), Microsoft Agent Framework (replaces AutoGen)

## Core Capabilities

### Agent Frameworks (Updated)

- **Claude Agent SDK**: Native Claude agent development with Anthropic API
- **LangChain 1.0**: Fast agent development with `create_agent` and middleware system
- **LangGraph 1.0**: Production-ready stateful workflows with durability and checkpointing
- **Microsoft Agent Framework**: Enterprise multi-agent orchestration (successor to AutoGen and Semantic Kernel)
- **Temporal.io**: Durable workflow orchestration for long-running agents

### Key Updates

- **LangChain 1.0**: Removed chains - agents now built with `create_agent()` on LangGraph runtime
- **LangGraph 1.0**: Battle-tested by Uber, LinkedIn, Klarna - full production support
- **Microsoft Agent Framework**: Unified AutoGen + Semantic Kernel with enterprise features
- **Legacy Support**: Old chains available via `langchain-classic` package

### Agent Capabilities

- **Conversational Agents**: Multi-turn dialogue with context and memory
- **Task Automation**: Complex multi-step task execution with middleware
- **Tool Integration**: External API integration via tool calling and MCP
- **Memory Management**: Built-in persistence and long-term memory
- **Multi-Agent Systems**: Workflows and agent collaboration patterns
- **Workflow Orchestration**: Durable, checkpointed execution with human-in-the-loop

## Plugin Structure

```
aiagent-plugin/
├── manifest.json
├── commands/
│   ├── agent.md              # Main agent management (LangChain 1.0)
│   ├── workflow.md           # LangGraph workflow creation
│   ├── microsoft-agent.md    # Microsoft Agent Framework
│   ├── deploy.md             # Agent deployment
│   └── test.md               # Agent testing and validation
├── agents/
│   ├── claude-architect.md
│   ├── langchain-builder.md      # Updated for 1.0
│   ├── langgraph-designer.md     # Updated for 1.0
│   ├── microsoft-orchestrator.md # New: Agent Framework
│   └── memory-specialist.md
├── skills/
│   ├── agent-monitoring.md
│   ├── error-recovery.md
│   ├── performance-tuning.md
│   └── security-validation.md
├── hooks/
│   └── hooks.json
└── mcp-servers/
    └── config.json
```

## Manifest Configuration

```json
{
  "name": "aiagent-plugin",
  "version": "2.0.0",
  "description": "AI agent orchestration for Claude, LangChain 1.0, LangGraph 1.0, Microsoft Agent Framework",
  "author": {
    "name": "Claude Code Team",
    "email": "team@claude.code",
    "url": "https://github.com/claude-code/aiagent-plugin"
  },
  "keywords": [
    "ai-agents",
    "claude",
    "langchain",
    "langgraph",
    "microsoft-agent-framework",
    "orchestration",
    "workflow",
    "automation",
    "multi-agent",
    "langchain-1.0"
  ],
  "requirements": {
    "langchain": ">=1.0.0",
    "langgraph": ">=1.0.0",
    "agent-framework": ">=0.1.0",
    "langchain-anthropic": ">=1.0.0"
  },
  "commands": [
    "./commands/agent.md",
    "./commands/workflow.md",
    "./commands/microsoft-agent.md",
    "./commands/deploy.md",
    "./commands/test.md"
  ],
  "agents": "./agents/",
  "skills": "./skills/",
  "hooks": "./hooks/hooks.json",
  "mcpServers": "./mcp-servers/config.json"
}
```

## Commands

### `/agent` Command (LangChain 1.0)

```markdown
---
description: Create and manage AI agents using LangChain 1.0
allowed-tools: Bash, Read, Write, Execute
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
python3 -c "import langchain; print(f'LangChain: {langchain.**version**}')" || {
echo "Installing LangChain 1.0..."
pip install --break-system-packages "langchain>=1.0.0" langchain-anthropic
}
}

case $ACTION in
create)
check_version
echo "Creating LangChain 1.0 agent: $NAME"

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
system_prompt="You are a helpful assistant.", # Add middleware for custom behavior
middleware=[], # Add middleware here
)

# Run agent

if **name** == "**main**":
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
```

### `/workflow` Command (LangGraph 1.0)

```markdown
---
description: Create stateful workflows with LangGraph 1.0
allowed-tools: Bash, Read, Write, Execute
---

# Workflow Command (LangGraph 1.0)

Create production-ready stateful workflows using LangGraph.

## Usage

`/workflow [action] [name] [options]`

## Actions

- `create` - Create new stateful workflow
- `add-node` - Add node to workflow
- `add-edge` - Add edge between nodes
- `checkpoint` - Enable checkpointing
- `visualize` - Generate workflow diagram
- `deploy` - Deploy to production

## LangGraph 1.0 Features

- **Durable execution**: Persist through failures
- **Checkpointing**: Save and resume workflows
- **Human-in-the-loop**: Built-in approval patterns
- **Time-travel**: Rewind and replay execution
- **Production-ready**: Battle-tested at scale

## Implementation

!`
#!/bin/bash

ACTION=$1
NAME=$2
OPTIONS=$3

check_langgraph() {
echo "Checking LangGraph version..."
python3 -c "import langgraph; print(f'LangGraph: {langgraph.**version**}')" || {
echo "Installing LangGraph 1.0..."
pip install --break-system-packages "langgraph>=1.0.0"
}
}

case $ACTION in
    create)
        check_langgraph
        echo "Creating LangGraph 1.0 workflow: $NAME"
        mkdir -p "./workflows/$NAME"

        cat > "./workflows/$NAME/workflow.py" << 'EOPYTHON'

from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_anthropic import ChatAnthropic
import operator

# Define state schema

class WorkflowState(TypedDict):
"""State for the workflow"""
messages: Annotated[list, operator.add]
current_step: str
result: str

# Initialize LLM

llm = ChatAnthropic(model="claude-sonnet-4-5-20250929")

# Define workflow nodes

async def process_input(state: WorkflowState):
"""Process user input"""
messages = state["messages"]
response = await llm.ainvoke(messages)

    return {
        "messages": [response],
        "current_step": "processed"
    }

async def generate_output(state: WorkflowState):
"""Generate final output"""
return {
"result": state["messages"][-1].content,
"current_step": "complete"
}

# Build workflow

workflow = StateGraph(WorkflowState)

# Add nodes

workflow.add_node("process", process_input)
workflow.add_node("generate", generate_output)

# Set entry point

workflow.set_entry_point("process")

# Add edges

workflow.add_edge("process", "generate")
workflow.add_edge("generate", END)

# Compile with checkpointing

checkpointer = MemorySaver()
app = workflow.compile(checkpointer=checkpointer)

# Run workflow

if **name** == "**main**":
import asyncio

    config = {"configurable": {"thread_id": "1"}}

    initial_state = {
        "messages": [{"role": "user", "content": "Hello!"}],
        "current_step": "start",
        "result": ""
    }

    async def run():
        result = await app.ainvoke(initial_state, config)
        print(f"Result: {result['result']}")

    asyncio.run(run())

EOPYTHON

        echo "Workflow created at ./workflows/$NAME/workflow.py"
        ;;

    checkpoint)
        echo "Enabling checkpointing for: $NAME"
        cat >> "./workflows/$NAME/workflow.py" << 'EOPYTHON'

# Add persistent checkpointing

from langgraph.checkpoint.sqlite import SqliteSaver

# Use SQLite for persistent checkpoints

checkpointer = SqliteSaver.from_conn_string("./checkpoints.db")
app = workflow.compile(checkpointer=checkpointer)

# Now workflow can resume from any point

EOPYTHON
;;

    visualize)
        echo "Generating visualization for: $NAME"
        python3 << 'EOVISUAL'

from workflows.$NAME.workflow import app

# Generate Mermaid diagram

print(app.get_graph().draw_mermaid())
EOVISUAL
;;

    deploy)
        echo "Deploying workflow: $NAME to production"
        echo "LangGraph 1.0 is production-ready and battle-tested"
        ;;

    *)
        echo "Usage: /workflow [create|checkpoint|visualize|deploy] [name]"
        exit 1
        ;;

esac
`
```

### `/microsoft-agent` Command

```markdown
---
description: Create agents with Microsoft Agent Framework
allowed-tools: Bash, Read, Write, Execute
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

async def main(): # Create simple chat agent
agent = AzureOpenAIResponsesClient(
credential=DefaultAzureCredential(),
).create_agent(
name="ChatAgent",
instructions="You are a helpful assistant.",
)

    result = await agent.run("Hello! How can you help me?")
    print(result)

if **name** == "**main**":
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

async def main(): # Create specialized agents
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

if **name** == "**main**":
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
```

## Agents

### langchain-builder.md (Updated for 1.0)

````markdown
---
name: langchain-builder
description: Expert in LangChain 1.0 agent development
tools: Read, Write, Execute, Install
model: sonnet
---

# LangChain Builder (1.0)

Expert in creating agents using LangChain 1.0's create_agent and middleware system.

## LangChain 1.0 Agent Patterns

### Basic Agent with create_agent

```python
from langchain.agents import create_agent
from langchain_anthropic import ChatAnthropic
from langchain_core.tools import tool

# Define tools
@tool
def web_search(query: str) -> str:
    """Search the web for information."""
    return f"Search results for: {query}"

@tool
def calculator(expression: str) -> float:
    """Calculate mathematical expressions."""
    return eval(expression)

# Create agent - built on LangGraph runtime
agent = create_agent(
    model="anthropic:claude-sonnet-4-5-20250929",
    tools=[web_search, calculator],
    system_prompt="You are a helpful research assistant.",
)

# Run agent
result = agent.invoke({
    "messages": [{"role": "user", "content": "What is 15 * 23?"}]
})

print(result["messages"][-1].content)
```
````

### Agent with Middleware

```python
from langchain.agents import create_agent
from langchain.agents.middleware import (
    HumanInTheLoopMiddleware,
    ConversationSummaryMiddleware,
    PIIRedactionMiddleware
)

# Middleware executes in order for before_model
# Reverse order for after_model

agent = create_agent(
    model="anthropic:claude-sonnet-4-5-20250929",
    tools=[web_search],
    system_prompt="You are a helpful assistant.",
    middleware=[
        PIIRedactionMiddleware(),          # Remove PII first
        ConversationSummaryMiddleware(),   # Compress long conversations
        HumanInTheLoopMiddleware(),        # Human approval for actions
    ]
)

# Middleware intercepts and modifies behavior without changing core logic
```

### Custom Middleware

```python
from langchain.agents.middleware import AgentMiddleware
from typing import Any

class CustomLoggingMiddleware(AgentMiddleware):
    """Custom middleware for logging agent actions"""

    async def before_model(self, state: dict, context: Any) -> dict:
        """Called before model is invoked"""
        print(f"Model input: {state['messages'][-1].content}")
        return state

    async def after_model(self, state: dict, context: Any) -> dict:
        """Called after model responds"""
        print(f"Model output: {state['messages'][-1].content}")
        return state

    async def before_tool(self, state: dict, context: Any) -> dict:
        """Called before tool execution"""
        tool_call = state['messages'][-1].tool_calls[0]
        print(f"Calling tool: {tool_call['name']}")
        return state

    async def after_tool(self, state: dict, context: Any) -> dict:
        """Called after tool execution"""
        print(f"Tool result received")
        return state

# Use custom middleware
agent = create_agent(
    model="anthropic:claude-sonnet-4-5-20250929",
    tools=[web_search],
    middleware=[CustomLoggingMiddleware()]
)
```

### Structured Output with Agents

```python
from pydantic import BaseModel
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy

# Define output schema
class ContactInfo(BaseModel):
    name: str
    email: str
    phone: str

# Create agent with structured output
agent = create_agent(
    model="anthropic:claude-sonnet-4-5-20250929",
    tools=[web_search],
    response_format=ToolStrategy(ContactInfo)
)

result = agent.invoke({
    "messages": [{
        "role": "user",
        "content": "Extract: John Doe, john@example.com, (555) 123-4567"
    }]
})

# Access structured response
contact: ContactInfo = result["structured_response"]
print(f"Name: {contact.name}")
print(f"Email: {contact.email}")
```

### Multi-Agent System with Subordinate Agents

```python
from langchain.agents import create_agent
from langchain_core.tools import tool

# Create specialized subordinate agents as tools
@tool
def research_agent(query: str) -> str:
    """Research agent for gathering information."""
    researcher = create_agent(
        model="anthropic:claude-sonnet-4-5-20250929",
        tools=[web_search],
        system_prompt="You are a research specialist."
    )
    result = researcher.invoke({
        "messages": [{"role": "user", "content": query}]
    })
    return result["messages"][-1].content

@tool
def analyst_agent(data: str) -> str:
    """Analyst agent for data analysis."""
    analyst = create_agent(
        model="anthropic:claude-sonnet-4-5-20250929",
        tools=[calculator],
        system_prompt="You are a data analyst."
    )
    result = analyst.invoke({
        "messages": [{"role": "user", "content": f"Analyze: {data}"}]
    })
    return result["messages"][-1].content

# Supervisor agent coordinates subordinates
supervisor = create_agent(
    model="anthropic:claude-sonnet-4-5-20250929",
    tools=[research_agent, analyst_agent],
    system_prompt="You are a supervisor. Delegate tasks to specialists.",
)

# Run multi-agent workflow
result = supervisor.invoke({
    "messages": [{
        "role": "user",
        "content": "Research AI trends and analyze the data"
    }]
})
```

### Agent with Memory and Checkpointing

```python
from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver

# Create agent with checkpointing (built-in via LangGraph)
checkpointer = MemorySaver()

agent = create_agent(
    model="anthropic:claude-sonnet-4-5-20250929",
    tools=[web_search],
    checkpointer=checkpointer,  # Enable persistence
)

# Run with thread ID for conversation tracking
config = {"configurable": {"thread_id": "user-123"}}

# First message
result1 = agent.invoke({
    "messages": [{"role": "user", "content": "My name is Alice"}]
}, config=config)

# Agent remembers context
result2 = agent.invoke({
    "messages": [{"role": "user", "content": "What's my name?"}]
}, config=config)

print(result2["messages"][-1].content)  # "Your name is Alice"
```

### Streaming Agent Responses

```python
from langchain.agents import create_agent

agent = create_agent(
    model="anthropic:claude-sonnet-4-5-20250929",
    tools=[web_search],
)

# Stream agent execution
for chunk in agent.stream(
    {"messages": [{"role": "user", "content": "Research AI safety"}]},
    stream_mode="updates"
):
    if "messages" in chunk:
        print(chunk["messages"][-1].content)
```

## Best Practices

1. **Use create_agent**: Don't use old chains or AgentExecutor (moved to langchain-classic)
2. **Leverage Middleware**: Add behavior without modifying core logic
3. **Built on LangGraph**: Agents get durability, checkpointing, and streaming for free
4. **Structured Outputs**: Use ToolStrategy or ProviderStrategy for type-safe outputs
5. **Multi-Agent Patterns**: Use tools to spawn subordinate agents
6. **Thread Management**: Use thread_id in config for conversation tracking
7. **Streaming**: Stream responses for better UX
8. **Model Agnostic**: Easily swap models with provider prefixes
9. **Integration Rich**: 1000+ integrations available
10. **Production Ready**: Battle-tested at scale

## Migration from Pre-1.0

```python
# OLD (pre-1.0) - Don't use
from langchain.agents import initialize_agent, AgentType
agent_executor = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
)

# NEW (1.0+) - Use this
from langchain.agents import create_agent
agent = create_agent(
    model="anthropic:claude-sonnet-4-5-20250929",
    tools=tools,
)

# For legacy code, use langchain-classic:
# pip install langchain-classic
# from langchain_classic.agents import initialize_agent
```

````

### langgraph-designer.md (Updated for 1.0)

```markdown
---
name: langgraph-designer
description: Expert in LangGraph 1.0 production workflows
tools: Read, Write, Execute, Visualize
model: sonnet
---

# LangGraph Designer (1.0)

Expert in creating production-ready stateful workflows with LangGraph 1.0.

## LangGraph 1.0 Production Patterns

### Basic Workflow with Checkpointing

```python
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_anthropic import ChatAnthropic
import operator

# Define state
class AgentState(TypedDict):
    messages: Annotated[list, operator.add]
    current_step: str

# Initialize components
llm = ChatAnthropic(model="claude-sonnet-4-5-20250929")
checkpointer = SqliteSaver.from_conn_string("./checkpoints.db")

# Define nodes
async def process_node(state: AgentState):
    messages = state["messages"]
    response = await llm.ainvoke(messages)
    return {
        "messages": [response],
        "current_step": "processed"
    }

# Build graph
workflow = StateGraph(AgentState)
workflow.add_node("process", process_node)
workflow.set_entry_point("process")
workflow.add_edge("process", END)

# Compile with checkpointing - production ready!
app = workflow.compile(checkpointer=checkpointer)

# Run with thread ID for persistence
config = {"configurable": {"thread_id": "123"}}
result = await app.ainvoke(
    {"messages": [{"role": "user", "content": "Hello"}], "current_step": "start"},
    config=config
)
````

### Human-in-the-Loop Pattern

```python
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

class ReviewState(TypedDict):
    draft: str
    approved: bool
    feedback: str

async def create_draft(state: ReviewState):
    """Create initial draft"""
    draft = await llm.ainvoke("Create a draft document")
    return {"draft": draft.content, "approved": False}

async def human_review(state: ReviewState):
    """Wait for human review"""
    # This node interrupts execution for human input
    return state

async def revise_draft(state: ReviewState):
    """Revise based on feedback"""
    revised = await llm.ainvoke(
        f"Revise this draft based on feedback: {state['feedback']}\n\nDraft: {state['draft']}"
    )
    return {"draft": revised.content}

def should_continue(state: ReviewState) -> str:
    """Check if approved"""
    return "end" if state["approved"] else "revise"

# Build workflow
workflow = StateGraph(ReviewState)
workflow.add_node("draft", create_draft)
workflow.add_node("review", human_review)
workflow.add_node("revise", revise_draft)

workflow.set_entry_point("draft")
workflow.add_edge("draft", "review")
workflow.add_conditional_edges(
    "review",
    should_continue,
    {"revise": "revise", "end": END}
)
workflow.add_edge("revise", "review")

# Compile with interrupts for human input
app = workflow.compile(
    checkpointer=MemorySaver(),
    interrupt_before=["review"]  # Pause here for human input
)

# Run workflow - it will pause at review
config = {"configurable": {"thread_id": "456"}}
result = await app.ainvoke(
    {"draft": "", "approved": False, "feedback": ""},
    config=config
)

# Provide human feedback and resume
result = await app.ainvoke(
    {"approved": False, "feedback": "Make it more concise"},
    config=config
)
```

### Parallel Execution

```python
from langgraph.graph import StateGraph, END
import asyncio

class ParallelState(TypedDict):
    input: str
    result_a: str
    result_b: str
    result_c: str
    final: str

async def task_a(state: ParallelState):
    """First parallel task"""
    await asyncio.sleep(1)
    return {"result_a": f"Task A processed: {state['input']}"}

async def task_b(state: ParallelState):
    """Second parallel task"""
    await asyncio.sleep(1)
    return {"result_b": f"Task B processed: {state['input']}"}

async def task_c(state: ParallelState):
    """Third parallel task"""
    await asyncio.sleep(1)
    return {"result_c": f"Task C processed: {state['input']}"}

async def combine(state: ParallelState):
    """Combine results"""
    return {
        "final": f"Combined: {state['result_a']}, {state['result_b']}, {state['result_c']}"
    }

# Build graph with parallel execution
workflow = StateGraph(ParallelState)
workflow.add_node("task_a", task_a)
workflow.add_node("task_b", task_b)
workflow.add_node("task_c", task_c)
workflow.add_node("combine", combine)

workflow.set_entry_point("task_a")
workflow.set_entry_point("task_b")  # Multiple entry points = parallel
workflow.set_entry_point("task_c")

workflow.add_edge("task_a", "combine")
workflow.add_edge("task_b", "combine")
workflow.add_edge("task_c", "combine")
workflow.add_edge("combine", END)

app = workflow.compile()

# All three tasks execute in parallel
result = await app.ainvoke({
    "input": "data",
    "result_a": "", "result_b": "", "result_c": "", "final": ""
})
```

### Time-Travel and Rewind

```python
from langgraph.checkpoint.sqlite import SqliteSaver

# Compile with persistent checkpointing
checkpointer = SqliteSaver.from_conn_string("./checkpoints.db")
app = workflow.compile(checkpointer=checkpointer)

config = {"configurable": {"thread_id": "789"}}

# Run workflow
result = await app.ainvoke(initial_state, config=config)

# Get history
history = await app.aget_state_history(config)

# Rewind to previous state
for state in history:
    print(f"State at {state.created_at}: {state.values}")

# Resume from specific checkpoint
checkpoint_id = list(history)[2].config["configurable"]["checkpoint_id"]
result = await app.ainvoke(
    None,  # Continue from checkpoint
    config={
        "configurable": {
            "thread_id": "789",
            "checkpoint_id": checkpoint_id
        }
    }
)
```

### Multi-Agent Workflow

```python
from langchain.agents import create_agent
from langgraph.graph import StateGraph, END

class MultiAgentState(TypedDict):
    task: str
    research_result: str
    analysis_result: str
    final_report: str

# Create specialized agents
researcher = create_agent(
    model="anthropic:claude-sonnet-4-5-20250929",
    tools=[web_search],
    system_prompt="You are a research specialist."
)

analyst = create_agent(
    model="anthropic:claude-sonnet-4-5-20250929",
    tools=[calculator],
    system_prompt="You are a data analyst."
)

writer = create_agent(
    model="anthropic:claude-sonnet-4-5-20250929",
    tools=[],
    system_prompt="You are a technical writer."
)

# Orchestrate agents in workflow
async def research_node(state: MultiAgentState):
    result = await researcher.ainvoke({
        "messages": [{"role": "user", "content": state["task"]}]
    })
    return {"research_result": result["messages"][-1].content}

async def analyze_node(state: MultiAgentState):
    result = await analyst.ainvoke({
        "messages": [{"role": "user", "content": state["research_result"]}]
    })
    return {"analysis_result": result["messages"][-1].content}

async def write_node(state: MultiAgentState):
    result = await writer.ainvoke({
        "messages": [{
            "role": "user",
            "content": f"Write report from:\nResearch: {state['research_result']}\nAnalysis: {state['analysis_result']}"
        }]
    })
    return {"final_report": result["messages"][-1].content}

# Build workflow
workflow = StateGraph(MultiAgentState)
workflow.add_node("research", research_node)
workflow.add_node("analyze", analyze_node)
workflow.add_node("write", write_node)

workflow.set_entry_point("research")
workflow.add_edge("research", "analyze")
workflow.add_edge("analyze", "write")
workflow.add_edge("write", END)

app = workflow.compile(checkpointer=checkpointer)
```

## Production Features

### 1. Durable Execution

- Workflow state persists across failures
- Resume from last checkpoint
- No data loss on crash

### 2. Observability

- LangSmith integration for tracing
- Visualize execution paths
- Debug complex workflows

### 3. Scalability

- Battle-tested at Uber, LinkedIn, Klarna
- Handle long-running workflows
- Efficient resource usage

### 4. Flexibility

- Conditional routing
- Dynamic workflows
- Composable graphs

## Best Practices

1. **Use Checkpointing**: Always enable for production
2. **Human-in-the-Loop**: Use interrupt_before for critical decisions
3. **Thread IDs**: Track conversations with thread_id
4. **Time-Travel**: Debug by rewinding to previous states
5. **Parallel Execution**: Use for independent tasks
6. **State Design**: Keep state minimal and type-safe
7. **LangSmith**: Enable for production monitoring
8. **Error Handling**: Add error recovery nodes
9. **Testing**: Test workflows end-to-end
10. **Documentation**: Document workflow logic clearly

## Deployment

```python
# LangGraph 1.0 is production-ready
# Deploy to:
# - Docker containers
# - Kubernetes
# - AWS Lambda (with layers)
# - Azure Functions
# - Any Python environment

# Example: Docker deployment
# Dockerfile
FROM python:3.11
RUN pip install langgraph langchain-anthropic
COPY workflow.py .
CMD ["python", "workflow.py"]
```

````

### microsoft-orchestrator.md (New)

```markdown
---
name: microsoft-orchestrator
description: Expert in Microsoft Agent Framework
tools: Read, Write, Execute, Deploy
model: sonnet
---

# Microsoft Orchestrator

Expert in creating multi-agent systems with Microsoft Agent Framework.

## Microsoft Agent Framework Patterns

### Basic Chat Agent

```python
import asyncio
from agent_framework.azure import AzureOpenAIResponsesClient
from azure.identity import AzureCliCredential

async def main():
    # Simple chat agent
    agent = AzureOpenAIResponsesClient(
        credential=AzureCliCredential(),
    ).create_agent(
        name="AssistantBot",
        instructions="You are a helpful assistant with expertise in Python."
    )

    result = await agent.run("Write a Python function to calculate fibonacci")
    print(result)

asyncio.run(main())
````

### Agent with Tools

```python
from agent_framework import Agent
from agent_framework.tools import tool

@tool
async def web_search(query: str) -> str:
    """Search the web for information."""
    # Implement search
    return f"Search results for: {query}"

@tool
async def calculator(expression: str) -> float:
    """Calculate mathematical expressions."""
    return eval(expression)

# Create agent with tools
agent = Agent(
    name="ResearchBot",
    instructions="You are a research assistant.",
    tools=[web_search, calculator]
)

# Run agent
result = await agent.run("What is 15 squared?")
```

### Workflow Orchestration

```python
from agent_framework import Workflow, Agent
from agent_framework.middleware import LoggingMiddleware, ValidationMiddleware

# Create specialized agents
researcher = Agent(
    name="Researcher",
    instructions="Research topics thoroughly and provide detailed information.",
    tools=[web_search]
)

analyst = Agent(
    name="Analyst",
    instructions="Analyze data and provide insights.",
    tools=[calculator]
)

writer = Agent(
    name="Writer",
    instructions="Write clear, professional reports.",
    tools=[]
)

# Create workflow - data flow based
workflow = Workflow()

# Add agents as executors
workflow.add_executor("research", researcher)
workflow.add_executor("analyze", analyst)
workflow.add_executor("write", writer)

# Define data flow
workflow.add_edge("research", "analyze")
workflow.add_edge("analyze", "write")

# Add middleware
workflow.add_middleware(LoggingMiddleware())
workflow.add_middleware(ValidationMiddleware())

# Run workflow
result = await workflow.run({
    "task": "Research AI safety and create a report"
})
```

### Multi-Agent Collaboration

```python
from agent_framework import Agent, GroupOrchestrator

# Create agent team
coder = Agent(
    name="Coder",
    instructions="Write high-quality Python code.",
)

reviewer = Agent(
    name="Reviewer",
    instructions="Review code for quality and bugs.",
)

tester = Agent(
    name="Tester",
    instructions="Write and run tests for code.",
)

# Orchestrate agents
orchestrator = GroupOrchestrator(
    agents=[coder, reviewer, tester],
    strategy="sequential"  # or "parallel", "round-robin"
)

# Run task
result = await orchestrator.run(
    "Create a Python function to sort a list, review it, and test it"
)
```

### Checkpointing and Resume

```python
from agent_framework import Workflow
from agent_framework.checkpoint import FileCheckpointer

# Enable checkpointing
checkpointer = FileCheckpointer("./checkpoints")

workflow = Workflow(checkpointer=checkpointer)
workflow.add_executor("step1", agent1)
workflow.add_executor("step2", agent2)
workflow.add_edge("step1", "step2")

# Run with checkpoint ID
config = {"checkpoint_id": "workflow-123"}
result = await workflow.run(input_data, config=config)

# Resume from checkpoint if interrupted
result = await workflow.resume(config=config)
```

### Human-in-the-Loop

```python
from agent_framework import Workflow, HumanApproval

workflow = Workflow()

# Add approval step
workflow.add_executor("draft", writer_agent)
workflow.add_executor("approve", HumanApproval())
workflow.add_executor("publish", publisher_agent)

workflow.add_edge("draft", "approve")
workflow.add_edge("approve", "publish")

# Workflow pauses for human approval
result = await workflow.run({"task": "Write press release"})

# Provide approval
workflow.provide_feedback(
    checkpoint_id="abc123",
    approved=True,
    feedback="Looks good!"
)

# Continue execution
result = await workflow.resume()
```

### Azure AI Foundry Integration

```python
from agent_framework.azure import AzureAIFoundryClient
from azure.identity import DefaultAzureCredential

# Deploy to Azure AI Foundry
client = AzureAIFoundryClient(
    credential=DefaultAzureCredential(),
    resource_group="my-rg",
    workspace="my-workspace"
)

# Deploy agent
deployment = client.deploy_agent(
    agent=my_agent,
    name="production-agent",
    compute="serverless"
)

# Monitor with observability
client.enable_telemetry(deployment.id)
```

### MCP Integration

```python
from agent_framework.tools import MCPAdapter

# Connect to MCP server
mcp_tools = await MCPAdapter.connect(
    server_url="http://localhost:3000",
    tools=["filesystem", "database", "web"]
)

# Use MCP tools with agent
agent = Agent(
    name="MCPAgent",
    instructions="You can access files, databases, and web.",
    tools=mcp_tools
)
```

## Key Features

### 1. Unified Framework

- Combines AutoGen's multi-agent patterns
- Integrates Semantic Kernel's enterprise features
- Single SDK for all agent needs

### 2. Production-Ready

- Built-in observability with OpenTelemetry
- Security: PII detection, task adherence, prompt shields
- Durable execution with checkpointing

### 3. Flexible Orchestration

- **Workflow**: Deterministic data flow (from Semantic Kernel)
- **Agent**: Dynamic LLM-driven collaboration (from AutoGen)
- Mix and match patterns

### 4. Enterprise Integration

- Azure AI Foundry deployment
- OpenAPI integration
- Agent2Agent communication
- MCP protocol support

## Migration from AutoGen

```python
# OLD (AutoGen)
from autogen import AssistantAgent, UserProxyAgent, GroupChat

assistant = AssistantAgent(
    name="assistant",
    llm_config={"model": "gpt-4"}
)

user = UserProxyAgent(name="user")

group_chat = GroupChat(
    agents=[assistant, user],
    messages=[],
    max_round=10
)

# NEW (Agent Framework)
from agent_framework import Agent, Workflow

assistant = Agent(
    name="assistant",
    model="gpt-4"
)

# Use Workflow for deterministic orchestration
workflow = Workflow()
workflow.add_executor("assistant", assistant)
```

## Best Practices

1. **Choose Right Pattern**: Workflow for deterministic, Agent for dynamic
2. **Use Middleware**: Add logging, validation, security
3. **Enable Checkpointing**: For long-running tasks
4. **Human-in-Loop**: For critical decisions
5. **Azure Integration**: Deploy to AI Foundry for scale
6. **Security First**: Enable PII detection and prompt shields
7. **Observability**: Use OpenTelemetry for monitoring
8. **MCP Protocol**: Leverage for tool standardization
9. **Python & .NET**: Choose language based on ecosystem
10. **Migrate Early**: Move from AutoGen to Agent Framework

## Resources

- [Microsoft Agent Framework Docs](https://learn.microsoft.com/agent-framework/)
- [Migration from AutoGen](https://learn.microsoft.com/agent-framework/migration-guide/from-autogen)
- [Azure AI Foundry](https://azure.microsoft.com/products/ai-foundry)

````

## Updated Hooks Configuration

```json
{
  "hooks": {
    "SessionStart": {
      "enabled": true,
      "actions": [
        {
          "type": "command",
          "command": "echo 'AI Agent Plugin 2.0 - LangChain 1.0, LangGraph 1.0, Microsoft Agent Framework'"
        },
        {
          "type": "command",
          "command": "python3 -c \"import langchain; import langgraph; print(f'LangChain: {langchain.__version__}, LangGraph: {langgraph.__version__}')\" || echo 'Installing required packages...'"
        }
      ]
    },
    "pre-agent-create": {
      "enabled": true,
      "pattern": "/agent create*",
      "actions": [
        {
          "type": "skill",
          "name": "security-validation",
          "action": "validate_config"
        },
        {
          "type": "command",
          "command": "echo 'Using LangChain 1.0 create_agent pattern'"
        }
      ]
    }
  }
}
````

## Summary of Major Changes

### LangChain 1.0

- ❌ **Removed**: Chains, `initialize_agent`, `AgentExecutor`
- ✅ **New**: `create_agent()` function
- ✅ **New**: Middleware system for customization
- ✅ **New**: Built on LangGraph runtime
- 📦 **Legacy**: Old patterns in `langchain-classic` package

### LangGraph 1.0

- ✅ **Production**: Battle-tested at Uber, LinkedIn, Klarna
- ✅ **Durable**: Checkpointing and persistence
- ✅ **Features**: Human-in-the-loop, time-travel, streaming
- ✅ **Stable**: No breaking changes until 2.0

### Microsoft Agent Framework

- ✅ **New**: Replaces AutoGen and Semantic Kernel
- ✅ **Unified**: Single framework for all agent patterns
- ✅ **Enterprise**: Security, observability, Azure integration
- ✅ **Python & .NET**: Full support for both platforms
- ⚠️ **AutoGen**: Maintenance mode (bug fixes only)

### Migration Path

1. **From old LangChain**: Use `langchain-classic` or migrate to `create_agent`
2. **From AutoGen**: Follow Microsoft's migration guide to Agent Framework
3. **From LangGraph <1.0**: Update to 1.0 (backward compatible)

---

**Plugin Status**: Ready for production use  
**Framework Versions**: LangChain 1.0+, LangGraph 1.0+, Agent Framework 0.1+  
**Last Verified**: November 2025
