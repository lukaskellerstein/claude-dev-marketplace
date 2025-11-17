---
description: Create migration strategy from one architecture to another
---

# Migrate Command

Plan and execute architecture migrations.

## Usage

`/migrate [from] [to] [strategy]`

## Migration Paths

- `monolith-to-microservices` - Strangler fig pattern
- `microservices-to-monolith` - Service consolidation
- `on-premise-to-cloud` - Cloud migration
- `sync-to-event` - Event-driven transformation

## Strategies

- `big-bang` - Complete rewrite (high risk)
- `strangler` - Gradual replacement (recommended)
- `parallel` - Run both systems simultaneously
- `phased` - Phase by phase migration

## Implementation

Parse migration parameters:
- $1 = from architecture
- $2 = to architecture
- $3 = strategy (default: strangler)

### Monolith to Microservices

Invoke the `microservices-architect` agent with migration context to:

#### Phase 1: Analysis
1. Analyze monolithic codebase
2. Identify bounded contexts using DDD
3. Map module dependencies
4. Identify database dependencies
5. Create service boundary map

#### Phase 2: Planning
1. Prioritize services to extract (start with edge services)
2. Design API contracts
3. Plan data migration strategy
4. Design service communication patterns
5. Create detailed migration roadmap

#### Phase 3: Implementation (Strangler Fig Pattern)
1. Create API Gateway/Proxy
2. Route traffic to proxy
3. Extract first service:
   - Create new service
   - Migrate data (if needed)
   - Implement API
   - Route proxy to new service for specific endpoints
4. Repeat for each service
5. Gradually retire monolith code
6. Decommission monolith when empty

#### Phase 4: Data Migration
1. Database per service pattern
2. Implement data sync mechanisms
3. Event sourcing for consistency
4. Gradual data migration

### Microservices to Monolith

Invoke the `monolith-specialist` agent with consolidation context to:

1. Analyze microservices landscape
2. Design modular monolith structure
3. Plan service consolidation:
   - Merge related services
   - Consolidate databases
   - Convert inter-service calls to method calls
   - Maintain module boundaries
4. Implement gradual consolidation
5. Migrate data to unified database
6. Maintain deployment simplicity

### On-Premise to Cloud

Invoke the `cloud-architect` agent to:

1. Assess current infrastructure
2. Choose cloud provider (AWS, GCP, Azure)
3. Design cloud architecture
4. Plan migration strategy:
   - Lift & Shift (quick)
   - Replatform (optimized)
   - Refactor (cloud-native)
5. Create Infrastructure as Code
6. Setup CI/CD pipelines
7. Implement security measures
8. Execute migration

### Sync to Event-Driven

Invoke the `event-architect` agent to:

1. Identify domain events
2. Design event store
3. Implement event sourcing
4. Setup message broker (Kafka, RabbitMQ)
5. Convert synchronous calls to events
6. Implement saga patterns for transactions
7. Create event schemas
8. Gradual conversion

## Risk Assessment

For each migration:
1. Identify risks
2. Plan mitigation strategies
3. Create rollback plan
4. Define success criteria
5. Plan monitoring and observability

## Deliverables

1. Detailed migration plan
2. Timeline and milestones
3. Risk assessment
4. Rollback procedures
5. Testing strategy
6. Documentation
7. Training materials
