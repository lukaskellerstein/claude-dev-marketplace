---
description: Design microservices architecture for a given domain or system
---

Design a comprehensive microservices architecture for the specified domain or system.

## Process

Follow these steps:

1. **Analyze Requirements**: Understand the domain, business capabilities, and constraints from the user's request and existing codebase

2. **Launch Microservices Architect**: Use the `microservices-architect` agent to:
   - Identify bounded contexts and service boundaries
   - Define service responsibilities and APIs
   - Design data management strategy
   - Plan communication patterns
   - Create context map showing service relationships

3. **Validate with Cloud Patterns**: Use the `cloud-patterns-expert` agent to:
   - Validate scalability of the design
   - Add reliability and resilience patterns
   - Recommend cloud services for deployment
   - Estimate costs and optimize

4. **Event-Driven Integration** (if applicable): If the system requires asynchronous communication, use the `event-sourcing-expert` agent to:
   - Design event schemas and message flows
   - Choose appropriate message broker
   - Define saga patterns for distributed transactions

## Output

Present a comprehensive microservices architecture including:
- Service boundaries with responsibilities
- API contracts (REST, GraphQL, or gRPC)
- Data architecture and consistency strategy
- Communication patterns and message flows
- Technology stack recommendations
- Deployment architecture
- Implementation roadmap

Make sure to create diagrams using Mermaid syntax to visualize:
- Service context map
- Deployment architecture
- Data flow diagrams
- Sequence diagrams for key interactions

Provide specific, actionable recommendations that can be immediately implemented.
