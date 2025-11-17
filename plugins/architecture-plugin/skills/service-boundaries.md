---
name: service-boundaries
description: Automatically detects and suggests service boundary improvements
allowed-tools: Read, Glob, Grep
---

# Service Boundaries Skill

Automatically analyzes code to identify service boundaries and coupling issues. This skill triggers when working with microservices or modular architectures.

## Detection Patterns

### High Cohesion Indicators

Look for classes and modules that:
- Frequently change together in git history
- Access the same data structures
- Implement related business concepts
- Share common vocabulary
- Have similar non-functional requirements

### Low Coupling Indicators

Identify good boundaries when:
- Services communicate through well-defined interfaces
- Minimal dependencies between services
- Asynchronous communication patterns used
- Each service has independent data store
- Clear API contracts exist

### Boundary Violations

Detect problems:
- **Direct Database Access**: Services accessing other services' databases
- **Shared Domain Models**: Using same entity classes across services
- **Circular Dependencies**: Service A → B → C → A
- **Chatty Interfaces**: Too many calls between services (>10 per user request)
- **God Service**: Service with too many responsibilities (>20 endpoints)
- **Data Coupling**: Services sharing mutable data structures

## Analysis Triggers

This skill automatically activates when:
- Creating new microservices
- Modifying service dependencies
- Adding inter-service communication
- Changing service interfaces
- Database schema changes
- Adding new endpoints to existing services

## Detection Implementation

### 1. Analyze Import/Dependency Patterns

```
Search for:
- Cross-service imports
- Shared database models
- Common utility classes
- Dependency injection patterns
```

### 2. Identify Communication Patterns

```
Look for:
- HTTP client calls
- gRPC stubs
- Message broker subscriptions
- Event handlers
- Direct database queries
```

### 3. Measure Coupling Metrics

```
Calculate:
- Afferent Coupling (Ca): Number of services depending on this service
- Efferent Coupling (Ce): Number of services this service depends on
- Instability (I = Ce / (Ca + Ce)): 0 = stable, 1 = unstable
- Coupling strength: Critical, High, Medium, Low
```

## Suggestions

### When Services Are Too Granular

**Signs**:
- Many tiny services with single methods
- Excessive network overhead
- Complex orchestration for simple tasks

**Suggestion**:
```
Consider merging related services:
- ServiceA (user-create) + ServiceB (user-update) + ServiceC (user-delete)
  → UserService (all user operations)

Benefits:
- Reduced network latency
- Simpler deployment
- Easier transaction management
- Less operational overhead
```

### When Services Have Multiple Responsibilities

**Signs**:
- Service handles multiple unrelated business capabilities
- Large number of endpoints (>20)
- Different teams want to modify the same service
- Inconsistent rate of change across functionality

**Suggestion**:
```
Split service by business capability:
- OrderService
  → OrderManagementService (CRUD orders)
  → OrderFulfillmentService (picking, packing, shipping)
  → OrderAnalyticsService (reporting, analytics)

Benefits:
- Independent scaling
- Team autonomy
- Easier to understand and maintain
- Different deployment cadences
```

### When Direct Service-to-Service Calls Are Too Frequent

**Signs**:
- Synchronous cascade calls
- High latency for user requests
- Tight coupling between services
- Brittle system (one service down affects others)

**Suggestion**:
```
Introduce Anti-Corruption Layer or API Gateway:
- Client → API Gateway → [Service A, Service B, Service C] (parallel)
  Instead of: Client → Service A → Service B → Service C (cascade)

Or convert to Event-Driven:
- Service A → Event Bus → Service B, Service C (async)
  Instead of: Service A → HTTP → Service B → HTTP → Service C

Benefits:
- Lower latency
- Better fault isolation
- Loose coupling
- Independent scalability
```

### When Services Share Database

**Signs**:
- Multiple services with direct database access
- Schema changes affect multiple services
- No clear data ownership
- Inconsistent data modifications

**Suggestion**:
```
Implement Database Per Service pattern:

Current state:
  ServiceA ─┐
  ServiceB ─┼─ Shared Database
  ServiceC ─┘

Target state:
  ServiceA → Database A
  ServiceB → Database B
  ServiceC → Database C

Data sync via:
  - Domain events
  - Change Data Capture (CDC)
  - Saga patterns for transactions

Benefits:
- Independent schema evolution
- Technology choice per service
- Clear data ownership
- Better isolation
```

### When Services Need Better Isolation

**Signs**:
- Services using synchronous HTTP for all communication
- Missing circuit breakers
- No retry logic
- Cascading failures

**Suggestion**:
```
Implement Resilience Patterns:

1. Circuit Breaker:
   - Prevent cascading failures
   - Fast fail when service is down
   - Automatic recovery

2. Retry with Backoff:
   - Handle transient failures
   - Exponential backoff
   - Max retry limit

3. Bulkhead:
   - Isolate thread pools
   - Prevent resource exhaustion
   - Contain failures

4. Timeout:
   - Set reasonable timeouts
   - Fail fast
   - Free up resources

5. Async Communication:
   - Use message queues
   - Event-driven architecture
   - Eventual consistency
```

## Output Format

When boundary issues are detected:

```markdown
## Service Boundary Analysis

### Detected Issues

1. **High Coupling: OrderService → InventoryService**
   - Severity: High
   - Issue: OrderService makes 15 synchronous calls to InventoryService per order
   - Impact: High latency, tight coupling
   - Recommendation: Introduce async event-driven communication

2. **Shared Database Violation**
   - Severity: Critical
   - Issue: OrderService and PaymentService both access `orders` table
   - Impact: No data ownership, difficult to scale independently
   - Recommendation: Split database, use events for data sync

3. **Circular Dependency**
   - Severity: Critical
   - Issue: ServiceA → ServiceB → ServiceC → ServiceA
   - Impact: Cannot deploy independently, tight coupling
   - Recommendation: Introduce message bus, remove sync dependencies

### Service Boundary Recommendations

**Current Structure:**
```
OrderService (150 endpoints)
├── Order Management
├── Inventory Management
├── Pricing
├── Promotions
└── Analytics
```

**Recommended Structure:**
```
OrderService (20 endpoints)
├── Create Order
├── Update Order
└── Cancel Order

InventoryService (15 endpoints)
├── Check Stock
├── Reserve Items
└── Release Items

PricingService (10 endpoints)
├── Calculate Price
└── Apply Discounts

AnalyticsService (5 endpoints)
├── Order Reports
└── Revenue Reports
```

### Migration Path

1. Extract InventoryService (Week 1-2)
2. Extract PricingService (Week 3-4)
3. Extract AnalyticsService (Week 5-6)
4. Implement event-driven communication (Week 7-8)
```

## Best Practices

1. **Single Responsibility**: Each service should have one reason to change
2. **Autonomous**: Services should be independently deployable
3. **Business-Aligned**: Align with business capabilities, not technical layers
4. **Resilient**: Implement circuit breakers, retries, timeouts
5. **Observable**: Distributed tracing, centralized logging
6. **Versioned**: API versioning for backward compatibility
7. **Documented**: Clear API contracts and integration guides

## Metrics to Track

Monitor these metrics for each service:
- Number of dependencies
- API call frequency between services
- Response time distribution
- Error rate
- Deployment frequency
- Change failure rate
- Mean time to recovery

Target thresholds:
- Dependencies: < 5 services
- API calls: < 10 per user request
- Response time: p99 < 500ms
- Error rate: < 0.1%
- Deployment: Daily or weekly
