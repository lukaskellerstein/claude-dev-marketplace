---
description: Generate comprehensive architecture documentation with diagrams, component descriptions, and ADRs
---

Create detailed architecture documentation including visual diagrams, component descriptions, and architectural decision records.

## Process

Follow these steps:

1. **Analyze System**: Understand the architecture
   - Identify major components and services
   - Map dependencies and integrations
   - Review infrastructure and deployment
   - Analyze data flows and storage
   - Identify design patterns used
   - Review existing architecture docs

2. **Launch Architecture Documenter**: Use the `documentation-plugin:architecture-documenter` agent to:
   - Create system architecture diagrams
   - Generate component diagrams
   - Draw sequence diagrams for key flows
   - Create data flow diagrams
   - Document deployment architecture
   - Write component descriptions
   - Document integration patterns
   - Explain design decisions

3. **Create Visual Documentation**: Generate Mermaid diagrams for:
   - Overall system architecture
   - Component relationships (C4 model)
   - Sequence diagrams for critical flows
   - Data flow and transformations
   - Deployment topology
   - State machines (if applicable)
   - Entity relationships

4. **Document Decisions**: Create Architecture Decision Records (ADRs) for:
   - Technology choices
   - Design patterns selected
   - Integration strategies
   - Data architecture decisions
   - Security approach
   - Performance optimizations

## Output

Present comprehensive architecture documentation including:

### 1. Architecture Overview Document

**High-Level Architecture**
- System purpose and scope
- Key architectural principles
- Major components overview
- Technology stack
- System architecture diagram

**Component Catalog**
For each major component:
- Name and purpose
- Responsibilities
- Technology and frameworks
- APIs and interfaces
- Dependencies
- Scalability considerations
- Component diagram

**Integration Architecture**
- Integration patterns used
- Internal service communication
- External integrations
- Message formats
- API contracts
- Sequence diagrams

**Data Architecture**
- Data model (ERD)
- Data storage strategy
- Data flow diagrams
- Caching strategy
- Data consistency approach

**Security Architecture**
- Authentication mechanism
- Authorization model
- Data protection
- Network security
- Secrets management

**Deployment Architecture**
- Infrastructure overview
- Deployment diagram
- Scaling strategy
- High availability
- Disaster recovery

### 2. Architecture Decision Records (ADRs)

Create ADR files for key decisions:
- `docs/adr/001-microservices-architecture.md`
- `docs/adr/002-message-broker-choice.md`
- `docs/adr/003-database-selection.md`
- etc.

Each ADR includes:
- Status (Proposed/Accepted/Deprecated)
- Context and problem
- Decision made
- Rationale
- Consequences (positive/negative)
- Alternatives considered
- Implementation notes

### 3. Diagram Collection

Generate organized diagrams:
- `docs/architecture/system-overview.md` (Mermaid)
- `docs/architecture/components.md` (C4 diagrams)
- `docs/architecture/data-flow.md` (Flow diagrams)
- `docs/architecture/deployment.md` (Infrastructure)
- `docs/architecture/sequences/` (Sequence diagrams)

## Usage Scenarios

### Document Entire Architecture
```
/document-architecture

Create comprehensive architecture documentation for this
microservices application including all diagrams and ADRs
```

### Focus on Specific Area
```
/document-architecture

Document the data architecture with ERD, data flow diagrams,
and ADR for database selection
```

### Update Existing Documentation
```
/document-architecture

Update architecture docs to reflect the new event-driven
integration pattern we implemented
```

### Create ADR for Decision
```
/document-architecture

Create an ADR documenting our decision to use GraphQL
instead of REST for the public API
```

## Architecture Diagram Types

### System Architecture
Shows overall system structure:
- Components and services
- Communication patterns
- External integrations
- Infrastructure layers

### Component Diagram (C4 Model)
Shows detailed component structure:
- Containers and components
- Relationships and dependencies
- Interfaces and APIs
- Technology choices

### Sequence Diagram
Shows interactions over time:
- Request/response flows
- Multi-service transactions
- Authentication flows
- Error handling flows

### Data Flow Diagram
Shows data movement:
- Data sources and sinks
- Transformation steps
- Data processing pipelines
- Caching layers

### Deployment Diagram
Shows infrastructure:
- Cloud resources
- Network topology
- Load balancing
- Scaling groups
- Database clusters

### State Machine
Shows state transitions:
- Order lifecycle
- Workflow states
- Processing stages
- Status transitions

### Entity Relationship Diagram
Shows data model:
- Entities and attributes
- Relationships
- Cardinality
- Keys and indexes

## ADR Structure

Each ADR should follow this structure:

```markdown
# ADR-XXX: [Decision Title]

## Status
Accepted

Date: 2025-01-15

## Context
Why do we need to make this decision? What problem are we solving?

- Business drivers
- Technical constraints
- Time/budget limitations
- Team capabilities

## Decision
What are we going to do?

- Clear statement of decision
- Key implementation details
- Configuration/setup approach

## Rationale
Why this decision?

- How it solves the problem
- Why it's better than alternatives
- Supporting evidence/research

## Consequences

### Positive
- Benefit 1
- Benefit 2

### Negative
- Trade-off 1
- Technical debt introduced

### Neutral
- Migration requirements
- Learning curve

## Alternatives Considered

### Alternative 1
Pros, cons, and why rejected

### Alternative 2
Pros, cons, and why rejected

## Implementation
How will we implement this?

## Validation
How will we know this was the right decision?

## References
- Links to discussions
- External resources
- Related ADRs
```

## Documentation Structure

Recommended organization:

```
docs/
├── architecture/
│   ├── README.md (Overview)
│   ├── system-architecture.md
│   ├── components.md
│   ├── data-architecture.md
│   ├── deployment.md
│   ├── security.md
│   └── sequences/
│       ├── user-authentication.md
│       ├── order-processing.md
│       └── payment-flow.md
├── adr/
│   ├── README.md (ADR index)
│   ├── 001-microservices-architecture.md
│   ├── 002-message-broker-choice.md
│   ├── 003-database-selection.md
│   └── template.md
└── diagrams/
    └── (exported diagram images if needed)
```

## Best Practices Applied

- **Visual First**: Use diagrams extensively
- **Progressive Disclosure**: Start high-level, add detail
- **Consistent Notation**: Use standard diagram styles
- **Context**: Explain the "why" not just "what"
- **Current**: Keep documentation synchronized
- **Searchable**: Use descriptive titles and tags
- **Versioned**: Track in version control
- **Linked**: Cross-reference related docs
- **Accessible**: Clear language and structure

## Quality Checklist

Before finalizing:
- [ ] System architecture diagram is complete and accurate
- [ ] All major components are documented
- [ ] Key flows have sequence diagrams
- [ ] Data model is documented with ERD
- [ ] Deployment architecture is visualized
- [ ] ADRs exist for major decisions
- [ ] Diagrams use consistent notation
- [ ] All diagrams have clear labels
- [ ] Documentation is organized logically
- [ ] Cross-references are in place
- [ ] Technical terms are defined
- [ ] Diagrams match actual implementation

## Integration with Other Documentation

Ensure architecture docs link to:
- README for quick overview
- API documentation for interface details
- Deployment guides for operations
- Contributing guides for development
- Security documentation for compliance

Provide complete, production-ready architecture documentation with all necessary diagrams and decision records.
