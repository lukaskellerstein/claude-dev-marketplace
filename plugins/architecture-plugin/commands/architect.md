---
description: Design and implement architecture patterns
---

# Architect Command

Design system architecture with best practices and patterns.

## Usage

`/architect [pattern] [scope] [options]`

## Patterns

- `microservices` - Microservices architecture
- `monolith` - Monolithic architecture
- `event-driven` - Event-driven architecture
- `3-layer` - Three-layer architecture
- `serverless` - Serverless architecture
- `hybrid` - Hybrid approach

## Scope

- `new` - Design from scratch
- `refactor` - Refactor existing system
- `extend` - Extend current architecture

## Implementation

Parse the arguments provided by the user:
- $1 = pattern type (microservices, monolith, event-driven, 3-layer, serverless, hybrid)
- $2 = scope (new, refactor, extend)
- $3 = additional options

Based on the pattern selected:

### Microservices Pattern
Invoke the `microservices-architect` agent to:
1. Analyze current project structure
2. Identify bounded contexts using DDD principles
3. Define service boundaries
4. Create service templates with:
   - API Gateway configuration
   - Service discovery setup
   - Message broker configuration
   - Service templates with proper structure
5. Generate architecture documentation

### Monolith Pattern
Invoke the `monolith-specialist` agent to:
1. Analyze current codebase
2. Design clean architecture layers:
   - Presentation layer
   - Business logic layer
   - Data access layer
3. Define module boundaries
4. Create modular monolith structure
5. Generate architecture documentation

### Event-Driven Pattern
Invoke the `event-architect` agent to:
1. Identify domain events
2. Design event store
3. Create CQRS structure (if applicable)
4. Setup event streaming infrastructure
5. Generate event schemas and handlers

### 3-Layer Architecture
Create a traditional three-layer architecture:
1. Presentation Layer (UI/API)
2. Business Logic Layer (Services)
3. Data Access Layer (Repositories)

Generate folder structure and base files for each layer.

### Serverless Pattern
Invoke the `cloud-architect` agent with serverless context to:
1. Design function-based architecture
2. Setup API Gateway
3. Configure event triggers
4. Design database access patterns
5. Generate Infrastructure as Code templates

### Hybrid Pattern
Combine multiple patterns based on requirements:
1. Analyze requirements
2. Identify which parts benefit from which pattern
3. Design integrated architecture
4. Generate combined structure

## Post-Processing

After architecture design:
1. Run `service-boundaries` skill to validate boundaries
2. Run `anti-patterns` skill to detect potential issues
3. Generate C4 diagrams using `/visualize` command
4. Create Architecture Decision Records (ADRs)
5. Present summary to user with next steps
