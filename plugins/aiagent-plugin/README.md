# AI Agent Plugin

Comprehensive toolkit for AI agent development and orchestration covering Claude Agent SDK, Langchain, LangGraph, Microsoft Agent Framework, and Temporal.io workflows.

## Features

### Agents

- **agent-orchestration-expert**: Expert in multi-agent systems, agent orchestration, and coordination patterns using Claude Agent SDK, Langchain, LangGraph, and Microsoft Agent Framework
- **workflow-automation-expert**: Expert in durable workflow orchestration and automation using Temporal.io for long-running processes and agent workflows
- **langchain-expert**: Expert in building advanced AI applications with Langchain and LangGraph including RAG systems, agent chains, and graph-based orchestration
- **claude-agent-expert**: Expert in building production agents with Claude Agent SDK including tool integration, streaming, context management, and advanced prompt engineering

### Commands

- `/design-agent-system`: Design and architect a complete AI agent system with multi-agent coordination, tool integration, and production patterns
- `/implement-workflow`: Design and implement durable workflows with Temporal.io for long-running processes, agent orchestration, and reliable automation
- `/build-rag-system`: Build a production-ready RAG (Retrieval Augmented Generation) system with Langchain, vector databases, and advanced retrieval strategies

### Skills

- **agent-reliability**: Auto-invoked when building or working with AI agents to ensure reliability, error handling, and production best practices
- **agent-memory-patterns**: Auto-invoked when implementing agent memory systems to ensure proper memory architecture, retrieval, and management

## Usage

### Design an AI Agent System

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

```
/design-agent-system

Create an autonomous research assistant that:
- Searches multiple sources
- Synthesizes information
- Generates reports with citations
- Uses Claude Opus for quality
- Handles 100 concurrent users
```

```
/design-agent-system

Build a coding agent system that:
- Understands requirements
- Generates code in multiple languages
- Tests generated code
- Iterates based on feedback
- Integrates with GitHub
```

### Implement Workflows with Temporal.io

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

### Build RAG Systems

```
/build-rag-system

Build a RAG system for technical documentation with:
- 1,000 markdown documents
- Semantic chunking for code blocks
- Hybrid search (vector + keyword)
- Claude Sonnet for generation
- Source citations with links
- Sub-second query response
```

```
/build-rag-system

Create an enterprise knowledge base with:
- 50,000 documents (PDF, Word, HTML)
- Multi-tenant with access control
- Metadata filtering by department
- Reranking for precision
- Streaming responses
- 1,000 concurrent users
```

```
/build-rag-system

Build a research assistant with:
- Academic papers (arXiv, PubMed)
- Multi-query retrieval for comprehensiveness
- Parent-document retrieval for context
- Claude Opus for analysis
- Citation tracking
- Export to bibliography format
```

### Use Agents Directly

Invoke specialized agents for focused work:

- "Use agent-orchestration-expert to design a multi-agent system for document processing"
- "Use workflow-automation-expert to create a Temporal workflow for ML training"
- "Use langchain-expert to build a RAG chain with custom retrieval"
- "Use claude-agent-expert to implement a Claude agent with tool calling"

## Technology Stack

### Agent Frameworks
- **Claude Agent SDK**: Official Anthropic SDK for Claude-powered agents
- **Langchain**: Comprehensive framework for LLM applications
- **LangGraph**: Graph-based orchestration for complex workflows
- **Microsoft Semantic Kernel**: Microsoft's AI orchestration SDK
- **AutoGen**: Microsoft's multi-agent conversation framework
- **CrewAI**: Role-based agent collaboration

### Workflow Orchestration
- **Temporal.io**: Durable workflow orchestration platform
- **Temporal SDKs**: Python, TypeScript, Go clients

### Vector Databases
- **Pinecone**: Managed vector database
- **Weaviate**: Open-source vector search
- **Qdrant**: High-performance vector database
- **Chroma**: Embedded vector database

### Supporting Tools
- **Vector Stores**: For semantic memory and RAG
- **Message Queues**: For agent communication
- **Databases**: For state persistence
- **Monitoring**: LangSmith, Datadog, Grafana

## Agent Architecture Patterns

### Single Agent with Tools
Best for simple, focused tasks:
- One Claude agent with multiple tools
- Conversation memory
- Streaming responses
- Cost-effective

**Use cases:**
- FAQ bots
- Simple assistants
- Single-domain experts

### Multi-Agent Collaboration (LangGraph)
Best for complex workflows requiring specialization:
- Multiple agents with distinct roles
- Graph-based coordination
- Conditional routing
- Shared state management

**Use cases:**
- Research pipelines
- Content generation workflows
- Data analysis systems

### Hierarchical Agent System
Best for enterprise workflows with approval:
- Manager agent coordinates workers
- Worker agents execute tasks
- Human-in-the-loop for approvals
- Audit logging

**Use cases:**
- Software development teams
- Document approval workflows
- Enterprise automation

### RAG-Enhanced Agents
Best for knowledge-intensive tasks:
- Vector database for knowledge
- Document retrieval
- Source citation
- Context-aware responses

**Use cases:**
- Documentation bots
- Research assistants
- Customer support with knowledge base

### Workflow-Based Agents (Temporal)
Best for long-running, reliable processes:
- Durable execution
- Retry and compensation logic
- Multi-day workflows
- State persistence

**Use cases:**
- Order processing
- Data pipelines
- ML training workflows
- Multi-step automation

## Workflow Patterns

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

### Event-Driven Workflows
- Triggered by external events
- Reactive processing
- Async handling
- High scalability

## Best Practices

### Agent Reliability
- Implement comprehensive error handling
- Use exponential backoff for retries
- Set appropriate timeouts
- Implement circuit breakers
- Design for graceful degradation
- Monitor all agent operations
- Test failure scenarios
- Log with proper context

### Memory Management
- Use appropriate memory types (short-term, long-term, semantic)
- Implement sliding window for bounded context
- Use prompt caching (Claude 3.5+)
- Store only important information in long-term memory
- Implement memory pruning and cleanup
- Monitor token usage and costs
- Test with long conversations

### Multi-Agent Coordination
- Define clear agent responsibilities
- Use message passing over shared state
- Implement idempotent operations
- Version agent APIs
- Design for failure and retries
- Use unique IDs for tracking
- Log all agent interactions
- Monitor coordination metrics

### Workflow Design
- Keep workflows deterministic
- Move non-deterministic code to activities
- Design activities to be idempotent
- Use signals for external communication
- Set appropriate timeouts and retry policies
- Implement compensation logic
- Test workflow replay
- Monitor workflow execution

### RAG System Design
- Use semantic chunking for better context
- Implement hybrid search (vector + keyword)
- Use reranking for improved precision
- Cache embeddings and responses
- Monitor retrieval quality metrics
- Implement query transformation
- Stream responses for better UX
- Test with diverse queries

### Cost Optimization
- Use Haiku for simple tasks, Sonnet for complex
- Implement prompt caching (Claude 3.5+)
- Cache tool results and embeddings
- Optimize prompt length
- Monitor token usage per interaction
- Set budget limits and alerts
- Batch operations when possible
- Use local models where appropriate

### Security
- Validate all inputs before processing
- Implement prompt injection detection
- Filter and validate agent outputs
- Use secure API key management
- Implement rate limiting
- Log security events
- Regular security audits
- Follow principle of least privilege

## Production Deployment

### Infrastructure
- Load balancing for agent endpoints
- Horizontal scaling of workers
- High availability setup
- Disaster recovery plan
- Monitoring and alerting
- CI/CD pipeline
- Configuration management

### Monitoring and Observability
- Request/response logging with IDs
- Latency tracking (p50, p95, p99)
- Error rate monitoring
- Token usage and cost tracking
- Agent decision logging
- Custom metrics and dashboards
- Alert rules for failures
- Distributed tracing for multi-agent systems

### Testing Strategy
- Unit tests for individual components
- Integration tests for agent interactions
- End-to-end scenario tests
- Performance and load tests
- Failure scenario tests
- Agent behavior evaluation
- Cost simulation tests
- Security penetration tests

### Scaling Considerations
- Horizontal scaling of agent workers
- Load balancing strategies
- Caching for performance
- Database connection pooling
- Rate limiting and quota management
- Geographic distribution
- Auto-scaling policies
- Cost monitoring and optimization

## Common Use Cases

### Customer Support
- Intent classification
- Knowledge base retrieval
- Response generation
- Escalation management
- Multi-language support
- Sentiment analysis

### Research and Analysis
- Information gathering from multiple sources
- Data synthesis and summarization
- Report generation with citations
- Trend analysis
- Competitive intelligence
- Market research

### Content Generation
- Blog posts and articles
- Marketing copy
- Social media content
- Documentation
- Product descriptions
- Email templates

### Software Development
- Code generation
- Code review and analysis
- Bug fixing
- Test generation
- Documentation generation
- Architecture design

### Data Processing
- ETL pipelines
- Data validation and cleaning
- Data transformation
- Report generation
- Scheduled batch processing
- Real-time stream processing

### Business Process Automation
- Document processing
- Approval workflows
- Order fulfillment
- Invoice processing
- Onboarding automation
- Compliance checking

## Learning Resources

### Claude Agent SDK
- [Anthropic Documentation](https://docs.anthropic.com/)
- [Agent SDK Examples](https://github.com/anthropics/anthropic-sdk-python)
- [Prompt Engineering Guide](https://docs.anthropic.com/claude/docs/prompt-engineering)

### Langchain & LangGraph
- [Langchain Documentation](https://python.langchain.com/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [LangSmith for Monitoring](https://smith.langchain.com/)

### Temporal.io
- [Temporal Documentation](https://docs.temporal.io/)
- [Temporal Python SDK](https://docs.temporal.io/python)
- [Temporal Patterns](https://docs.temporal.io/patterns)

### Microsoft Agent Framework
- [Semantic Kernel](https://github.com/microsoft/semantic-kernel)
- [AutoGen](https://github.com/microsoft/autogen)

### Vector Databases
- [Pinecone Docs](https://docs.pinecone.io/)
- [Weaviate Docs](https://weaviate.io/developers/weaviate)
- [Qdrant Docs](https://qdrant.tech/documentation/)

## Contributing

This plugin is designed to help developers build production-grade AI agent systems. For issues, suggestions, or contributions, please refer to the main marketplace repository.

## License

MIT
