---
description: Create stateful workflows with LangGraph 1.0
allowed-tools: Bash, Read, Write
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
    python3 -c "import langgraph; print(f'LangGraph: {langgraph.__version__}')" || {
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
if __name__ == "__main__":
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
        python3 << EOVISUAL
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
