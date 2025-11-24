---
description: Design and architect a complete AI agent system with multi-agent coordination, tool integration, and production patterns
---

Design and architect a comprehensive AI agent system with proper orchestration, tools, memory, and production considerations.

## Process

Follow these steps:

1. **Analyze Requirements**: Understand the agent system goals and constraints
   - Agent capabilities and responsibilities
   - Expected interactions and workflows
   - Scale requirements (users, requests, concurrency)
   - Budget constraints (cost per interaction)
   - Latency requirements
   - Integration requirements (external systems, databases)
   - Review existing codebase if applicable

2. **Choose Primary Framework**: Determine the best approach
   - Single agent vs multi-agent system
   - Claude Agent SDK for Claude-powered agents
   - Langchain/LangGraph for complex chains and graphs
   - Microsoft Agent Framework for enterprise scenarios
   - Hybrid approach combining multiple frameworks

3. **Launch Agent Orchestration Expert**: Use the `agent-orchestration-expert` agent to:
   - Design overall system architecture
   - Define agent roles and responsibilities
   - Design coordination patterns
   - Plan communication protocols
   - Design state management
   - Plan error handling and recovery
   - Design monitoring and observability

4. **Framework-Specific Design**: Depending on chosen framework, use:
   - `claude-agent-expert` for Claude Agent SDK implementation
   - `langchain-expert` for Langchain/LangGraph implementation
   - Both if using hybrid approach

5. **Review and Optimize** (if needed): Use appropriate expert to:
   - Optimize for cost and latency
   - Improve reliability and error handling
   - Enhance monitoring and observability
   - Scale for production load

## Output

Present a comprehensive agent system design including:

### System Architecture
- High-level architecture diagram
- Agent roles and responsibilities
- Communication flow between agents
- External system integrations
- Data flow and state management
- Why this architecture fits the requirements

### Agent Specifications
For each agent:
- Agent name and purpose
- Capabilities and limitations
- Tools available to the agent
- Memory and context strategy
- Prompt design approach
- Model selection (Opus, Sonnet, Haiku)
- Expected input/output formats

### Coordination Strategy
- How agents communicate (message passing, shared state, APIs)
- Orchestration pattern (hierarchical, peer-to-peer, event-driven)
- Workflow for typical interactions
- Conflict resolution mechanisms
- Load balancing strategy
- Scaling approach

### Tool Ecosystem
- List of tools required
- Tool schemas and interfaces
- Tool implementation approach
- External API integrations
- Tool error handling strategy
- Tool caching and optimization

### Memory and Context
- Short-term vs long-term memory strategy
- Vector database for semantic memory (if needed)
- Conversation history management
- Context passing between agents
- State persistence approach
- Memory pruning and optimization

### Implementation Plan
Complete implementation including:
```python
# Agent initialization
# Tool definitions
# Memory setup
# Orchestration logic
# Error handling
# Monitoring integration
```

### Error Handling and Reliability
- Retry strategies for each component
- Fallback mechanisms
- Circuit breakers for external services
- Graceful degradation approach
- Error logging and alerting
- Recovery procedures

### Monitoring and Observability
- Key metrics to track
- Logging strategy
- Distributed tracing (if multi-agent)
- Cost tracking per interaction
- Performance monitoring
- Alerting rules
- Dashboard design

### Production Deployment
- Infrastructure requirements
- Scaling strategy (horizontal, vertical)
- Load balancing approach
- High availability design
- Disaster recovery plan
- Deployment process
- Configuration management

### Cost Analysis
- Estimated token usage per interaction
- API costs (Claude, OpenAI, embeddings)
- Infrastructure costs
- Storage costs
- Total cost per interaction
- Cost optimization opportunities
- Budget recommendations

### Testing Strategy
- Unit tests for individual components
- Integration tests for agent interactions
- End-to-end scenario tests
- Performance tests
- Failure scenario tests
- Evaluation metrics and datasets

### Security Considerations
- Input validation and sanitization
- Output filtering and safety
- API key management
- Rate limiting
- User authentication/authorization
- Data privacy and compliance
- Prompt injection prevention

## Examples

### Design Customer Support Agent System
```
/design-agent-system

Design a multi-agent customer support system with:
- Intent classification agent
- Knowledge retrieval agent
- Response generation agent
- Escalation to human support
- 10,000 daily conversations
- <2 second response time
```

### Design Research Assistant
```
/design-agent-system

Create an autonomous research assistant that:
- Searches multiple sources
- Synthesizes information
- Generates reports with citations
- Uses Claude Opus for quality
- Handles 100 concurrent users
```

### Design Code Generation System
```
/design-agent-system

Build a coding agent system that:
- Understands requirements
- Generates code in multiple languages
- Tests generated code
- Iterates based on feedback
- Integrates with GitHub
```

### Design RAG-Enhanced Chatbot
```
/design-agent-system

Create a document-aware chatbot with:
- Vector database for 10,000 documents
- Retrieval-augmented generation
- Source citation
- Streaming responses
- Multi-turn conversations
- 1,000 concurrent users
```

## Agent System Patterns

### Single Agent with Tools
Best for: Simple, focused tasks
- One Claude agent with multiple tools
- Conversation memory
- Streaming responses
- Cost-effective

### Multi-Agent Collaboration (LangGraph)
Best for: Complex workflows requiring specialization
- Multiple agents with distinct roles
- Graph-based coordination
- Conditional routing
- Shared state management

### Hierarchical Agent System
Best for: Enterprise workflows with approval
- Manager agent coordinates workers
- Worker agents execute tasks
- Human-in-the-loop for approvals
- Audit logging

### Event-Driven Agent System
Best for: Real-time, reactive systems
- Agents triggered by events
- Message queue for coordination
- Async processing
- Horizontal scaling

## Best Practices Applied

- **Clear Responsibilities**: Each agent has a well-defined purpose
- **Loose Coupling**: Agents communicate via defined interfaces
- **Fault Tolerance**: Comprehensive error handling and retries
- **Observability**: Extensive logging and monitoring
- **Cost Optimization**: Right-sized models and caching
- **Security**: Input validation and output filtering
- **Scalability**: Designed for horizontal scaling
- **Testing**: Comprehensive test coverage
- **Documentation**: Clear architecture and API docs

## Integration with Other Systems

- **Databases**: For persistent storage and retrieval
- **Vector Stores**: For semantic search and memory
- **Message Queues**: For async agent communication
- **APIs**: External service integrations
- **Monitoring**: Observability platforms
- **CI/CD**: Automated testing and deployment

Provide production-ready agent system designs with complete architecture, implementation code, and operational guidelines.
