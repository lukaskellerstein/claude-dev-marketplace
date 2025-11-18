---
name: service-boundaries
description: Master service boundary design in microservices and modular architectures. Use when designing new services, refactoring monoliths, identifying bounded contexts, analyzing inter-service dependencies, or implementing domain-driven design patterns.
allowed-tools: Read, Glob, Grep
---

# Service Boundaries Skill

Master the art of defining, analyzing, and maintaining optimal service boundaries in microservices and modular architectures. This skill automatically detects boundary violations, suggests improvements, and ensures services follow domain-driven design principles.

## When to Use This Skill

This skill activates and provides value in these scenarios:

1. **Microservices Design** - Defining service boundaries for new microservices architectures
2. **Monolith Decomposition** - Breaking down monolithic applications into services
3. **Bounded Context Identification** - Identifying and implementing DDD bounded contexts
4. **Service Coupling Analysis** - Analyzing dependencies and coupling between services
5. **API Gateway Design** - Designing service exposure through API gateways
6. **Event-Driven Architecture** - Implementing service communication via events
7. **Database-Per-Service Pattern** - Migrating from shared database to isolated datastores
8. **Service Orchestration** - Designing workflows across multiple services
9. **Team Autonomy** - Aligning service boundaries with team ownership
10. **Scalability Planning** - Optimizing services for independent scaling
11. **Deployment Independence** - Ensuring services can deploy independently
12. **Anti-Corruption Layers** - Implementing boundaries between legacy and new systems
13. **CQRS Implementation** - Separating command and query responsibilities
14. **Saga Pattern Design** - Managing distributed transactions across services
15. **Service Mesh Configuration** - Setting up inter-service communication patterns

## Quick Start

### Analyze Current Service Boundaries

```bash
# Search for service boundary violations
grep -r "import.*otherservice" services/

# Check for shared database access
grep -r "SELECT.*FROM.*shared_table" services/

# Find direct service-to-service calls
grep -r "http://.*service" services/
```

### Detect Boundary Issues

```python
def analyze_service_boundaries(codebase_path):
    """Quick analysis of service boundary health"""

    issues = []

    # 1. Check for shared database access
    shared_db_accesses = find_shared_database_access(codebase_path)
    if shared_db_accesses:
        issues.append({
            "type": "Shared Database",
            "severity": "Critical",
            "count": len(shared_db_accesses),
            "recommendation": "Implement database-per-service pattern"
        })

    # 2. Check for circular dependencies
    circular_deps = detect_circular_dependencies(codebase_path)
    if circular_deps:
        issues.append({
            "type": "Circular Dependencies",
            "severity": "Critical",
            "count": len(circular_deps),
            "recommendation": "Introduce event-driven communication"
        })

    # 3. Check for god services
    god_services = find_god_services(codebase_path, endpoint_threshold=20)
    if god_services:
        issues.append({
            "type": "God Services",
            "severity": "High",
            "count": len(god_services),
            "recommendation": "Split by business capability"
        })

    return issues
```

## Real-World Scenarios

### Scenario 1: E-Commerce Service Decomposition

**Context**: Monolithic e-commerce application needs to be split into microservices.

**Analysis**:
```
Current Monolith:
- OrderManagement (150 classes)
- ProductCatalog (200 classes)
- CustomerManagement (100 classes)
- PaymentProcessing (80 classes)
- ShippingLogistics (120 classes)
- All sharing single database
```

**Solution**:
```yaml
Bounded Contexts Identified:
  1. Order Context:
     Services:
       - OrderService: Create, update, cancel orders
       - OrderHistoryService: Query order history
     Database: orders_db
     Events: OrderCreated, OrderShipped, OrderCancelled

  2. Product Context:
     Services:
       - ProductCatalogService: Product information
       - InventoryService: Stock management
       - PricingService: Dynamic pricing
     Database: products_db
     Events: ProductUpdated, StockChanged, PriceAdjusted

  3. Customer Context:
     Services:
       - CustomerService: Customer profiles
       - LoyaltyService: Rewards and points
     Database: customers_db
     Events: CustomerRegistered, PointsEarned

  4. Payment Context:
     Services:
       - PaymentService: Payment processing
       - RefundService: Refund handling
     Database: payments_db
     Events: PaymentProcessed, RefundIssued

  5. Fulfillment Context:
     Services:
       - ShippingService: Logistics management
       - TrackingService: Package tracking
     Database: fulfillment_db
     Events: ShipmentCreated, DeliveryCompleted

Communication Patterns:
  - Synchronous: API Gateway → Services (read operations)
  - Asynchronous: Event Bus for cross-context updates
  - CQRS: Separate read models for reporting
```

**Implementation Steps**:
1. Extract ProductCatalogService (minimal dependencies)
2. Extract PaymentService (clear boundary)
3. Extract ShippingService (independent workflow)
4. Extract CustomerService
5. Implement OrderService (orchestrates others via events)
6. Setup API Gateway for unified access
7. Migrate to event-driven communication
8. Implement saga patterns for distributed transactions

### Scenario 2: Banking System Bounded Contexts

**Context**: Digital banking platform needs clear service boundaries.

**Bounded Contexts**:
```yaml
1. Account Management Context:
   Entities: Account, AccountHolder, AccountType
   Services:
     - AccountService: CRUD operations
     - AccountStatementService: Generate statements
   Invariants:
     - Account balance consistency
     - Transaction atomicity

2. Transaction Processing Context:
   Entities: Transaction, TransactionType, TransactionStatus
   Services:
     - TransactionService: Process transactions
     - TransactionHistoryService: Query history
   Invariants:
     - Double-entry bookkeeping
     - Transaction idempotency

3. Fraud Detection Context:
   Entities: FraudRule, FraudScore, Alert
   Services:
     - FraudDetectionService: Real-time analysis
     - RuleEngineService: Manage fraud rules
   Invariants:
     - All transactions scanned
     - Real-time alerting

4. Customer Onboarding Context:
   Entities: Application, KYC, Document
   Services:
     - OnboardingService: Manage applications
     - KYCService: Verify identity
   Invariants:
     - Compliance requirements met
     - Document verification complete
```

### Scenario 3: SaaS Multi-Tenant Architecture

**Context**: SaaS platform with multi-tenant requirements.

**Service Boundaries**:
```yaml
Tenant Management:
  - TenantService: Tenant CRUD
  - SubscriptionService: Billing and plans
  - Isolation: Database per tenant

Core Application:
  - WorkflowService: Business workflows
  - DataService: User data management
  - Isolation: Schema per tenant

Platform Services:
  - AuthService: Authentication/authorization
  - NotificationService: Email/SMS
  - Isolation: Shared across tenants

Analytics:
  - ReportingService: Generate reports
  - MetricsService: Usage analytics
  - Isolation: Aggregated data warehouse
```

## Detection Patterns

### High Cohesion Indicators

Services that belong together:

```python
def detect_high_cohesion(services):
    """Identify services with high cohesion"""

    cohesion_signals = {
        "git_history": analyze_change_correlation(),
        "data_access": analyze_shared_data_patterns(),
        "business_concepts": analyze_domain_terminology(),
        "team_ownership": analyze_team_modifications(),
        "deployment_frequency": analyze_deployment_patterns()
    }

    # Services that frequently change together
    # should potentially be merged
    highly_cohesive_pairs = []
    for s1 in services:
        for s2 in services:
            if s1 != s2:
                correlation = calculate_cohesion(s1, s2, cohesion_signals)
                if correlation > 0.8:
                    highly_cohesive_pairs.append((s1, s2, correlation))

    return highly_cohesive_pairs
```

**Signs of High Cohesion**:
- Changes to Service A always require changes to Service B
- Both services access same core business entities
- Same team maintains both services
- Services deploy together frequently
- Shared vocabulary and domain language

### Low Coupling Indicators

Well-defined boundaries:

```python
def assess_coupling_level(service_a, service_b):
    """Assess coupling between two services"""

    coupling_factors = {
        "interface_coupling": has_well_defined_api(service_a, service_b),
        "data_coupling": shares_data(service_a, service_b),
        "temporal_coupling": requires_synchronous_calls(service_a, service_b),
        "deployment_coupling": must_deploy_together(service_a, service_b),
        "versioning": supports_api_versioning(service_a, service_b)
    }

    # Calculate coupling score (0 = loose, 1 = tight)
    coupling_score = sum([
        0.3 if not coupling_factors["interface_coupling"] else 0,
        0.3 if coupling_factors["data_coupling"] else 0,
        0.2 if coupling_factors["temporal_coupling"] else 0,
        0.1 if coupling_factors["deployment_coupling"] else 0,
        0.1 if not coupling_factors["versioning"] else 0
    ])

    return {
        "score": coupling_score,
        "level": "tight" if coupling_score > 0.5 else "loose",
        "factors": coupling_factors
    }
```

**Characteristics of Low Coupling**:
- Well-defined, versioned API contracts
- Asynchronous communication patterns
- Independent data stores
- No shared domain models across boundaries
- Services can deploy independently
- Clear ownership and responsibility

### Boundary Violations

Common problems to detect:

```python
class BoundaryViolationDetector:
    """Detect various service boundary violations"""

    def detect_direct_database_access(self, service_path):
        """Services accessing other services' databases"""
        violations = []

        # Find database connections
        db_connections = grep_pattern(
            service_path,
            r"db\.connect\(['\"](.+)['\"]\)"
        )

        # Check if accessing external service databases
        for conn in db_connections:
            if is_external_database(conn, service_path):
                violations.append({
                    "type": "Direct Database Access",
                    "severity": "Critical",
                    "location": conn.file,
                    "database": conn.database,
                    "recommendation": "Use service API instead of direct DB access"
                })

        return violations

    def detect_shared_domain_models(self, codebase_path):
        """Entity classes shared across services"""
        violations = []

        # Find entity/model classes
        model_files = glob_pattern(codebase_path, "**/models/*.py")

        # Check for duplicate entity definitions
        entity_map = defaultdict(list)
        for file in model_files:
            entities = extract_class_names(file)
            for entity in entities:
                entity_map[entity].append(file)

        # Report shared models
        for entity, files in entity_map.items():
            if len(files) > 1:
                violations.append({
                    "type": "Shared Domain Model",
                    "severity": "High",
                    "entity": entity,
                    "locations": files,
                    "recommendation": "Each service should have its own model"
                })

        return violations

    def detect_circular_dependencies(self, services):
        """Service A → B → C → A cycles"""
        graph = build_dependency_graph(services)
        cycles = find_cycles(graph)

        violations = []
        for cycle in cycles:
            violations.append({
                "type": "Circular Dependency",
                "severity": "Critical",
                "cycle": " → ".join(cycle),
                "services_involved": len(cycle),
                "recommendation": "Break cycle with event-driven architecture"
            })

        return violations

    def detect_chatty_interfaces(self, service_call_logs):
        """Too many inter-service calls"""
        violations = []

        # Analyze call patterns
        for endpoint, calls in service_call_logs.items():
            calls_per_request = analyze_call_chain(calls)

            if calls_per_request > 10:
                violations.append({
                    "type": "Chatty Interface",
                    "severity": "High",
                    "endpoint": endpoint,
                    "calls_per_request": calls_per_request,
                    "recommendation": "Introduce API Gateway or BFF pattern"
                })

        return violations

    def detect_god_services(self, services, endpoint_threshold=20):
        """Services with too many responsibilities"""
        violations = []

        for service in services:
            endpoint_count = count_endpoints(service)
            capabilities = identify_business_capabilities(service)

            if endpoint_count > endpoint_threshold or len(capabilities) > 3:
                violations.append({
                    "type": "God Service",
                    "severity": "High",
                    "service": service.name,
                    "endpoints": endpoint_count,
                    "capabilities": capabilities,
                    "recommendation": f"Split into {len(capabilities)} focused services"
                })

        return violations

    def detect_data_coupling(self, services):
        """Services sharing mutable data structures"""
        violations = []

        # Find shared caches, message queues, etc.
        shared_resources = find_shared_resources(services)

        for resource in shared_resources:
            if resource.is_mutable:
                violations.append({
                    "type": "Data Coupling",
                    "severity": "Medium",
                    "resource": resource.name,
                    "services": resource.accessing_services,
                    "recommendation": "Use immutable messages or events"
                })

        return violations
```

## Improvement Suggestions

### When Services Are Too Granular

**Problem**: Nano-services causing excessive overhead.

```yaml
Signs:
  - 50+ services for small application
  - Services with single method
  - Network latency dominates processing time
  - Complex orchestration for simple operations
  - High operational overhead

Example:
  Current (Too Granular):
    - UserCreateService
    - UserUpdateService
    - UserDeleteService
    - UserGetService
    - UserListService

  Recommended (Right-sized):
    - UserService
        - createUser()
        - updateUser()
        - deleteUser()
        - getUser()
        - listUsers()

Benefits of Consolidation:
  - Reduced network overhead
  - Simpler deployment pipeline
  - Easier transaction management
  - Better code reuse
  - Lower infrastructure costs
```

### When Services Have Multiple Responsibilities

**Problem**: God services violating single responsibility principle.

```yaml
Signs:
  - Service has >20 endpoints
  - Handles multiple unrelated business capabilities
  - Different teams need to modify same service
  - Inconsistent rate of change across features
  - Difficult to understand and maintain

Example:
  Current (God Service):
    OrderService (150 endpoints):
      - Order CRUD operations
      - Inventory management
      - Pricing calculations
      - Promotion engine
      - Order analytics
      - Customer notifications
      - Shipping coordination

  Recommended (Split by Capability):
    OrderManagementService (20 endpoints):
      - Create, read, update, delete orders
      - Order validation
      - Order status management

    InventoryService (15 endpoints):
      - Stock level checking
      - Reserve/release inventory
      - Inventory updates

    PricingService (10 endpoints):
      - Calculate prices
      - Apply discounts
      - Tax calculations

    FulfillmentService (12 endpoints):
      - Coordinate shipping
      - Track shipments
      - Handle returns

    AnalyticsService (8 endpoints):
      - Order metrics
      - Revenue reports
      - Trend analysis

Migration Strategy:
  1. Identify bounded contexts
  2. Extract InventoryService (Week 1-2)
  3. Extract PricingService (Week 3-4)
  4. Extract FulfillmentService (Week 5-6)
  5. Extract AnalyticsService (Week 7-8)
  6. Implement event-driven communication (Week 9-10)
  7. Remove coupling from original service (Week 11-12)
```

### When Direct Service Calls Are Too Frequent

**Problem**: Synchronous cascade causing latency and brittleness.

```yaml
Signs:
  - Request path: Client → A → B → C → D → E
  - High latency (>2 seconds p99)
  - Cascading failures
  - Tight temporal coupling
  - Poor fault isolation

Current Architecture:
  Client Request
    ↓
  OrderService (200ms)
    ↓
  InventoryService (150ms)
    ↓
  PricingService (100ms)
    ↓
  PaymentService (300ms)
    ↓
  ShippingService (250ms)

  Total Latency: 1000ms (1 second)
  Failure Rate: Multiplicative (99.9% × 99.9% × ... = 99.5%)

Solution 1: API Gateway with Parallel Calls
  Client Request
    ↓
  API Gateway (aggregates requests)
    ├→ OrderService (200ms)
    ├→ InventoryService (150ms) } In Parallel
    ├→ PricingService (100ms)   }
    └→ PaymentService (300ms)   }

  Total Latency: max(200, 150, 100, 300) = 300ms
  Improvement: 3.3x faster

Solution 2: Event-Driven Architecture
  OrderService:
    - Publishes OrderCreated event
    - Returns immediately to client (50ms)

  Event Consumers (async):
    - InventoryService listens → reserves stock
    - PricingService listens → calculates price
    - PaymentService listens → processes payment
    - ShippingService listens → schedules delivery

  Total Perceived Latency: 50ms
  Improvement: 20x faster perceived response
  Trade-off: Eventual consistency

Solution 3: Backend for Frontend (BFF)
  Mobile BFF:
    - Optimized for mobile screens
    - Minimal data transfer
    - Aggressive caching

  Web BFF:
    - Rich data for web UI
    - Server-side rendering support
    - Different caching strategy

  Each BFF aggregates backend services
  Benefits: Client-specific optimization
```

### When Services Share Database

**Problem**: Shared database anti-pattern preventing independent scaling.

```yaml
Signs:
  - Multiple services with direct database access
  - Schema changes affect multiple services
  - No clear data ownership
  - Coupling through database
  - Cannot scale databases independently

Current State:
  ┌─────────────┐
  │ OrderService │─┐
  └─────────────┘ │
  ┌─────────────┐ │
  │PaymentService│─┼→ Shared PostgreSQL Database
  └─────────────┘ │     - orders table
  ┌─────────────┐ │     - customers table
  │ShipService  │─┘     - payments table
  └─────────────┘       - products table

Problems:
  - Schema lock-in (can't evolve independently)
  - Performance contention (query competition)
  - Deployment coupling (migrations affect all)
  - No technology choice (all must use PostgreSQL)
  - Unclear ownership (who owns customers table?)

Target State:
  ┌─────────────┐      ┌──────────────────┐
  │ OrderService │─────→│ Orders PostgreSQL│
  └─────────────┘      └──────────────────┘
                         - orders
                         - order_items

  ┌─────────────┐      ┌──────────────────┐
  │PaymentService│─────→│Payments MongoDB  │
  └─────────────┘      └──────────────────┘
                         - transactions
                         - refunds

  ┌─────────────┐      ┌──────────────────┐
  │ShipService  │─────→│Shipping Neo4j    │
  └─────────────┘      └──────────────────┘
                         - routes
                         - tracking

Benefits:
  - Independent schema evolution
  - Technology choice per service
  - Clear data ownership
  - Independent scaling
  - Fault isolation

Migration Path:
  Phase 1: Identify Data Ownership
    - Map tables to services
    - Identify data relationships
    - Define bounded contexts

  Phase 2: Create Service APIs
    - Build APIs for data access
    - Implement read models
    - Add caching layers

  Phase 3: Migrate Callers to APIs
    - Update service A to call service B's API
    - Remove direct database access
    - Test thoroughly

  Phase 4: Split Databases
    - Create new database per service
    - Migrate data
    - Update connection strings

  Phase 5: Implement Data Sync
    - Use events for cross-service data
    - Implement CDC for read models
    - Setup eventual consistency patterns

Data Synchronization Patterns:
  1. Domain Events:
     OrderService publishes OrderCreated
     → ShippingService subscribes
     → Creates local shipping record

  2. Change Data Capture (CDC):
     Orders database changes
     → Debezium captures changes
     → Publishes to Kafka
     → Analytics service updates read model

  3. Saga Pattern:
     For distributed transactions
     OrderSaga orchestrates:
       - Reserve inventory
       - Process payment
       - Schedule shipping
     With compensation for failures
```

## Best Practices

### 1. Single Responsibility Principle

Each service should have one reason to change:

```yaml
Good Examples:
  - PaymentService: Process payments only
  - NotificationService: Send notifications only
  - AuthService: Authentication/authorization only

Bad Examples:
  - OrderService: Orders + Inventory + Shipping
  - UserService: Users + Analytics + Billing
  - ProductService: Products + Reviews + Recommendations
```

### 2. Autonomous Services

Services should be independently deployable:

```yaml
Requirements:
  - No shared libraries (except well-versioned SDKs)
  - API versioning for backward compatibility
  - Independent CI/CD pipelines
  - Separate databases
  - Isolated configuration

Verification:
  - Can service deploy without others updating?
  - Can service rollback independently?
  - Can service scale independently?
```

### 3. Business-Aligned Boundaries

Align with business capabilities, not technical layers:

```yaml
Good (Business-Aligned):
  - OrderManagement
  - CustomerManagement
  - ProductCatalog
  - PaymentProcessing

Bad (Technical Layers):
  - DatabaseService
  - APIService
  - CacheService
  - EmailService

Why: Business capabilities are stable, technical implementations change
```

### 4. Resilience Patterns

Implement fault tolerance:

```yaml
Circuit Breaker:
  - Prevent cascading failures
  - Fast fail when service down
  - Automatic recovery attempts

Retry with Backoff:
  - Handle transient failures
  - Exponential backoff
  - Maximum retry limit

Bulkhead:
  - Isolate thread pools
  - Prevent resource exhaustion
  - Contain failures

Timeout:
  - Set reasonable timeouts
  - Fail fast
  - Free up resources

Fallback:
  - Provide degraded functionality
  - Cache previous responses
  - Default values
```

### 5. Observable Services

Implement comprehensive observability:

```yaml
Logging:
  - Structured logging
  - Correlation IDs
  - Log aggregation (ELK, Splunk)

Metrics:
  - Response times
  - Error rates
  - Throughput
  - Resource utilization

Tracing:
  - Distributed tracing (Jaeger, Zipkin)
  - Request flow visualization
  - Bottleneck identification

Health Checks:
  - Liveness probes
  - Readiness probes
  - Dependency health
```

### 6. API Versioning

Maintain backward compatibility:

```yaml
Versioning Strategies:
  1. URI Versioning:
     /api/v1/orders
     /api/v2/orders

  2. Header Versioning:
     Accept: application/vnd.company.v1+json

  3. Query Parameter:
     /api/orders?version=1

Deprecation Process:
  1. Announce deprecation (6 months notice)
  2. Provide migration guide
  3. Monitor old version usage
  4. Gradually reduce support
  5. Finally remove (after 12+ months)
```

### 7. Documentation

Clear API contracts and integration guides:

```yaml
Documentation Needs:
  - OpenAPI/Swagger specifications
  - Architecture decision records (ADRs)
  - Service dependency maps
  - Runbooks for operations
  - Integration examples
  - Authentication guides
  - Rate limiting policies

Tools:
  - Swagger UI for API exploration
  - Postman collections
  - AsyncAPI for events
  - Architectural diagrams
```

## Metrics to Track

Monitor these metrics for each service:

```yaml
Coupling Metrics:
  - Number of dependencies: < 5 services
  - API call frequency: < 10 per user request
  - Circular dependencies: 0
  - Shared database tables: 0

Performance Metrics:
  - Response time p50: < 100ms
  - Response time p95: < 500ms
  - Response time p99: < 1000ms
  - Error rate: < 0.1%

Deployment Metrics:
  - Deployment frequency: Daily or weekly
  - Change failure rate: < 15%
  - Mean time to recovery: < 1 hour
  - Lead time for changes: < 1 day

Operational Metrics:
  - Service availability: > 99.9%
  - Database query time p95: < 100ms
  - Cache hit rate: > 90%
  - CPU utilization: < 70%
  - Memory utilization: < 80%
```

## Common Pitfalls to Avoid

1. **Over-fragmentation**: Too many tiny services increase complexity
2. **Under-fragmentation**: God services are hard to maintain and scale
3. **Shared databases**: Prevents independent deployment and scaling
4. **Synchronous chains**: Creates tight coupling and latency
5. **No API versioning**: Breaking changes affect all consumers
6. **Missing observability**: Can't debug distributed systems
7. **Ignoring data consistency**: Need patterns for eventual consistency
8. **Poor error handling**: Cascading failures bring down entire system
9. **Premature decomposition**: Start with modular monolith, split when needed
10. **Technology diversity**: Too many technologies increase operational burden

## Related Skills

- **anti-patterns**: Identifies architectural anti-patterns in service design
- **coupling-analysis**: Measures and analyzes coupling between services
- **scalability-check**: Ensures services can scale independently
- **cqrs-implementation**: Separates read and write concerns across services
- **event-driven-design**: Implements asynchronous service communication
- **api-gateway-design**: Designs unified entry point for microservices

## Advanced Topics

### Saga Pattern for Distributed Transactions

```python
class OrderSaga:
    """Manage distributed transaction across services"""

    def __init__(self):
        self.steps = [
            ("inventory", "reserve_stock", "release_stock"),
            ("payment", "process_payment", "refund_payment"),
            ("shipping", "schedule_shipment", "cancel_shipment")
        ]

    async def execute(self, order_data):
        """Execute saga with compensation"""
        completed_steps = []

        try:
            for service, action, compensation in self.steps:
                result = await self.call_service(service, action, order_data)
                completed_steps.append((service, compensation, result))

            return {"status": "success", "order_id": order_data["id"]}

        except Exception as e:
            # Compensate in reverse order
            for service, compensation, result in reversed(completed_steps):
                await self.call_service(service, compensation, result)

            return {"status": "failed", "reason": str(e)}
```

### Event Sourcing for Service State

```python
class OrderEventStore:
    """Store all state changes as events"""

    def __init__(self):
        self.events = []

    def apply_event(self, event):
        """Apply event and store"""
        self.events.append(event)
        self.persist(event)

    def rebuild_state(self, order_id):
        """Rebuild current state from events"""
        events = self.get_events(order_id)
        state = {}

        for event in events:
            state = self.apply(state, event)

        return state
```

This skill ensures your services have clear, maintainable boundaries that support scalability, team autonomy, and system reliability.
