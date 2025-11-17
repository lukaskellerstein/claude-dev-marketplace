---
name: anti-patterns
description: Detects architectural anti-patterns and suggests fixes
allowed-tools: Read, Glob, Grep
---

# Anti-Patterns Detection Skill

Automatically detects common architectural anti-patterns and provides actionable fixes. This skill triggers during code analysis, refactoring, and architecture reviews.

## Common Anti-Patterns

### 1. Distributed Monolith

**Detection Criteria**:
- Microservices that must deploy together
- Shared database across services
- Tight coupling via synchronous calls
- Breaking changes ripple across services
- No independent scalability

**Detection Method**:
```
Analyze:
- Deployment dependencies (does Service A require Service B update?)
- Database access patterns (shared tables?)
- API coupling (breaking changes affect multiple services?)
- Version dependencies (must versions stay in sync?)
```

**Indicators**:
- Services share database schema
- Deployment scripts deploy multiple services together
- Integration tests require all services running
- API versioning not implemented
- No backward compatibility

**Fix**:
```
1. Implement API Versioning:
   - Support multiple API versions
   - Gradual deprecation strategy
   - Backward compatibility

2. Database Per Service:
   - Each service owns its data
   - Communicate via APIs or events
   - Use saga pattern for transactions

3. Decouple Services:
   - Async communication where possible
   - Event-driven architecture
   - Anti-corruption layers

4. Independent Deployment:
   - CI/CD per service
   - Feature flags for gradual rollout
   - Contract testing
```

### 2. Chatty Services

**Detection Criteria**:
- More than 10 inter-service calls per user request
- Sequential synchronous calls (A → B → C → D)
- N+1 query problem across services
- High network latency
- Poor performance under load

**Detection Method**:
```
Trace request paths:
- Count service hops
- Measure total latency
- Identify sequential vs parallel calls
- Check for repeated calls to same service
```

**Indicators**:
- Distributed tracing shows long chains
- High P99 latency
- Network I/O dominates processing time
- Service mesh metrics show excessive traffic

**Fix**:
```
1. Introduce API Gateway:
   - Aggregate calls in gateway
   - Parallel requests to backend services
   - Single round trip for client

2. Backend for Frontend (BFF):
   - Optimize API per client type
   - Reduce roundtrips
   - Client-specific aggregation

3. Caching Layer:
   - Cache frequently accessed data
   - Reduce redundant calls
   - Appropriate TTL settings

4. Event-Driven Architecture:
   - Replace sync calls with events
   - Eventual consistency
   - Reduce coupling

5. Data Denormalization:
   - Duplicate data across services
   - Optimize for reads
   - Event-driven sync
```

### 3. Shared Database

**Detection Criteria**:
- Multiple services accessing same tables
- No clear data ownership
- Schema changes affect multiple services
- Direct database access from multiple codebases

**Detection Method**:
```
Analyze:
- Database connection strings across services
- SQL queries accessing same tables
- Migration scripts affecting multiple services
- ORM models in multiple services
```

**Indicators**:
```sql
-- Service A
SELECT * FROM orders WHERE customer_id = ?

-- Service B (different codebase)
SELECT * FROM orders WHERE status = 'pending'

-- Both accessing same table = Shared Database Anti-Pattern
```

**Fix**:
```
1. Database Per Service:

   Before:
   ServiceA ─┐
   ServiceB ─┼─ Shared Database
   ServiceC ─┘

   After:
   ServiceA → Database A
   ServiceB → Database B
   ServiceC → Database C

2. Data Synchronization:
   - Domain events for updates
   - Change Data Capture (CDC)
   - Event sourcing

3. Service Ownership:
   - OrderService owns orders table
   - CustomerService owns customers table
   - Other services call APIs, not DB

4. Migration Strategy:
   - Identify data ownership
   - Create service APIs
   - Migrate callers to APIs
   - Split databases
```

### 4. God Service

**Detection Criteria**:
- More than 20 endpoints
- Handles multiple unrelated business capabilities
- Multiple teams want to modify it
- Large codebase (>10,000 LOC)
- Too many dependencies

**Detection Method**:
```
Count:
- Number of REST endpoints
- Lines of code
- Number of database tables accessed
- Number of business capabilities
- Number of teams working on it
```

**Indicators**:
- ProductService handling: products, inventory, pricing, reviews, recommendations, search
- Single service > 20 endpoints
- Deployment takes multiple hours
- Different parts change at different rates

**Fix**:
```
Split by Business Capability:

God Service → Focused Services:
ProductService
├── ProductCatalogService (product info, categories)
├── InventoryService (stock management)
├── PricingService (pricing rules, discounts)
├── ReviewService (customer reviews, ratings)
├── RecommendationService (ML recommendations)
└── SearchService (product search, filtering)

Benefits:
- Independent scaling
- Team autonomy
- Easier to understand
- Faster deployments
- Better fault isolation
```

### 5. Anemic Services

**Detection Criteria**:
- Services with only CRUD operations
- No business logic in services
- All logic in orchestration layer
- Services are just database wrappers

**Detection Method**:
```
Analyze endpoints:
- GET /users/:id
- POST /users
- PUT /users/:id
- DELETE /users/:id

If ALL endpoints are simple CRUD = Anemic Service
```

**Indicators**:
```typescript
// Anemic Service - Just CRUD
class UserService {
  getUser(id) { return db.query(...); }
  createUser(data) { return db.insert(...); }
  updateUser(id, data) { return db.update(...); }
  deleteUser(id) { return db.delete(...); }
}

// All business logic in orchestrator
class OrderOrchestrator {
  async placeOrder(orderData) {
    const user = await userService.getUser(orderData.userId);
    const product = await productService.getProduct(orderData.productId);

    // Business logic here instead of in domain services
    if (user.credits < product.price) {
      throw new Error('Insufficient credits');
    }

    await userService.updateUser(user.id, {
      credits: user.credits - product.price
    });
    await orderService.createOrder(orderData);
  }
}
```

**Fix**:
```
Move Business Logic to Services:

// Rich Domain Service
class UserService {
  async deductCredits(userId: string, amount: Money): Promise<void> {
    const user = await this.findById(userId);

    // Business logic in service
    if (user.credits.isLessThan(amount)) {
      throw new InsufficientCreditsError(user.credits, amount);
    }

    user.deductCredits(amount);
    await this.userRepo.save(user);

    // Emit domain event
    await this.eventBus.publish(new CreditsDeductedEvent(userId, amount));
  }
}

// Simpler orchestrator
class OrderService {
  async placeOrder(orderData: PlaceOrderDto): Promise<Order> {
    // Services handle business rules
    await this.userService.deductCredits(orderData.userId, orderData.total);
    await this.inventoryService.reserveItems(orderData.items);

    const order = await this.orderRepo.create(orderData);
    return order;
  }
}
```

### 6. Big Ball of Mud

**Detection Criteria**:
- No clear architecture pattern
- Spaghetti code
- No separation of concerns
- Everything depends on everything
- Difficult to understand or modify

**Detection Method**:
```
Analyze:
- Cyclomatic complexity
- Dependency graph
- Module cohesion
- Code duplication
- Test coverage
```

**Indicators**:
- Can't explain architecture in 5 minutes
- New features take weeks
- High bug rate
- Difficult to onboard new developers
- Fear of making changes

**Fix**:
```
1. Identify Modules:
   - Group related functionality
   - Define module boundaries
   - Create module interfaces

2. Refactor Incrementally:
   - Strangler fig pattern
   - Module by module
   - Don't rewrite everything

3. Introduce Architecture:
   - Layered architecture
   - Clean architecture
   - Modular monolith
   - Or microservices if needed

4. Add Tests:
   - Characterization tests
   - Unit tests
   - Integration tests

5. Document:
   - Architecture decision records
   - Component diagrams
   - API documentation
```

### 7. Missing Abstraction Layer

**Detection Criteria**:
- Infrastructure code in domain logic
- Direct database calls in controllers
- No repository pattern
- Tight coupling to frameworks
- Hard to test

**Detection Method**:
```
Search for:
- Database queries in business logic
- HTTP clients in domain models
- Framework imports in domain layer
- SQL in service classes
```

**Indicators**:
```typescript
// BAD: No abstraction
class OrderService {
  async createOrder(data: any) {
    // Direct database access
    const result = await db.query(
      'INSERT INTO orders (customer_id, total) VALUES ($1, $2)',
      [data.customerId, data.total]
    );

    // Direct HTTP call
    await axios.post('http://payment-service/charge', {
      amount: data.total
    });

    return result;
  }
}
```

**Fix**:
```typescript
// GOOD: With abstractions

// Domain layer
interface OrderRepository {
  save(order: Order): Promise<void>;
  findById(id: OrderId): Promise<Order | null>;
}

interface PaymentGateway {
  processPayment(payment: Payment): Promise<PaymentResult>;
}

// Application layer
class OrderService {
  constructor(
    private orderRepo: OrderRepository,
    private paymentGateway: PaymentGateway
  ) {}

  async createOrder(dto: CreateOrderDto): Promise<Order> {
    const order = Order.create(dto);

    const paymentResult = await this.paymentGateway.processPayment(
      order.payment
    );

    if (!paymentResult.success) {
      throw new PaymentFailedError();
    }

    await this.orderRepo.save(order);
    return order;
  }
}

// Infrastructure layer
class SqlOrderRepository implements OrderRepository {
  async save(order: Order): Promise<void> {
    await this.db.query('INSERT INTO orders...');
  }
}

class StripePaymentGateway implements PaymentGateway {
  async processPayment(payment: Payment): Promise<PaymentResult> {
    return await this.stripeClient.charge(...);
  }
}
```

## Auto-Detection Rules

```yaml
rules:
  - name: circular_dependency
    condition: "service A → B → C → A"
    severity: critical
    message: "Circular dependency detected between services"
    fix: "Introduce message bus or event-driven architecture"

  - name: excessive_coupling
    condition: "service depends on >5 other services"
    severity: high
    message: "Service has too many dependencies"
    fix: "Review service boundaries, consider splitting or aggregating"

  - name: chatty_interface
    condition: ">10 service calls per user request"
    severity: high
    message: "Too many inter-service calls"
    fix: "Introduce API gateway, caching, or BFF pattern"

  - name: shared_database
    condition: "multiple services access same tables"
    severity: critical
    message: "Shared database anti-pattern detected"
    fix: "Implement database per service pattern"

  - name: god_service
    condition: ">20 endpoints in single service"
    severity: high
    message: "Service has too many responsibilities"
    fix: "Split by business capability"

  - name: missing_abstraction
    condition: "infrastructure code in domain layer"
    severity: medium
    message: "Missing abstraction layer"
    fix: "Introduce repository pattern and domain interfaces"

  - name: anemic_services
    condition: "only CRUD operations, no business logic"
    severity: medium
    message: "Anemic service detected"
    fix: "Move business logic into services"

  - name: distributed_monolith
    condition: "services must deploy together"
    severity: critical
    message: "Distributed monolith anti-pattern"
    fix: "Implement API versioning, decouple services"
```

## Output Format

```markdown
## Anti-Pattern Detection Results

### Critical Issues

1. **Distributed Monolith**
   - Services: OrderService, PaymentService, ShippingService
   - Problem: Must deploy together, shared database
   - Impact: Cannot scale independently, deployment risk
   - Fix: Implement database per service, API versioning
   - Priority: P0 - Address immediately

2. **Circular Dependency**
   - Path: ServiceA → ServiceB → ServiceC → ServiceA
   - Problem: Cannot deploy independently
   - Impact: Tight coupling, deployment issues
   - Fix: Introduce event bus, remove synchronous dependencies
   - Priority: P0 - Address immediately

### High Priority Issues

3. **God Service: ProductService**
   - Endpoints: 45
   - Responsibilities: catalog, inventory, pricing, reviews, search
   - Problem: Too many responsibilities
   - Impact: Hard to maintain, slow deployments
   - Fix: Split into 5 focused services
   - Priority: P1 - Address this quarter

4. **Chatty Communication**
   - Path: Client → API Gateway → OrderService → (15 calls) → Other Services
   - Problem: Excessive service-to-service calls
   - Impact: High latency (p99: 2.5s), poor UX
   - Fix: Implement BFF pattern, introduce caching
   - Priority: P1 - Address this quarter

### Recommendations

- Focus on critical issues first (distributed monolith, circular dependencies)
- Create migration plan for God Service refactoring
- Implement monitoring for inter-service calls
- Add circuit breakers for resilience
```

## Best Practices

1. **Regular Audits**: Run anti-pattern detection monthly
2. **Metrics**: Track coupling and cohesion metrics
3. **Code Reviews**: Check for anti-patterns during reviews
4. **Training**: Educate team on architectural patterns
5. **Documentation**: Document architecture decisions
6. **Automated Detection**: Integrate into CI/CD pipeline

Follow these guidelines to maintain clean, scalable architecture.
