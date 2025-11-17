---
description: Apply design patterns to solve specific problems
---

# Pattern Command

Apply design patterns to solve architectural problems.

## Usage

`/pattern [pattern] [context]`

## Patterns

### Data Access Patterns
- `repository` - Repository pattern for data access
- `unit-of-work` - Unit of Work pattern for transactions
- `data-mapper` - Data Mapper pattern

### Creational Patterns
- `factory` - Factory pattern for object creation
- `builder` - Builder pattern for complex objects
- `singleton` - Singleton pattern (use with caution)
- `prototype` - Prototype pattern for cloning

### Behavioral Patterns
- `strategy` - Strategy pattern for algorithms
- `observer` - Observer pattern for events
- `command` - Command pattern for operations
- `chain` - Chain of Responsibility

### Integration Patterns
- `saga` - Saga pattern for distributed transactions
- `cqrs` - Command Query Responsibility Segregation
- `event-sourcing` - Event sourcing for state
- `api-gateway` - API Gateway pattern
- `circuit-breaker` - Circuit Breaker for resilience

### Structural Patterns
- `adapter` - Adapter pattern for interface compatibility
- `facade` - Facade pattern for simplified interface
- `proxy` - Proxy pattern for access control
- `decorator` - Decorator pattern for extending functionality

## Implementation

Invoke the `patterns-expert` agent with the requested pattern.

### Repository Pattern
Create repository interfaces and implementations:

```typescript
// Domain Layer - Interface
interface OrderRepository {
  save(order: Order): Promise<void>;
  findById(id: string): Promise<Order | null>;
  findByCustomer(customerId: string): Promise<Order[]>;
}

// Infrastructure Layer - Implementation
class SqlOrderRepository implements OrderRepository {
  constructor(private db: Database) {}

  async save(order: Order): Promise<void> {
    // Implementation
  }

  async findById(id: string): Promise<Order | null> {
    // Implementation
  }
}
```

### Saga Pattern
Implement saga orchestrator or choreography:

**Orchestration** (centralized):
```typescript
class OrderSaga {
  private steps = [
    { service: 'order', action: 'create', compensate: 'cancel' },
    { service: 'payment', action: 'charge', compensate: 'refund' },
    { service: 'inventory', action: 'reserve', compensate: 'release' },
    { service: 'shipping', action: 'schedule', compensate: 'cancel' }
  ];

  async execute(orderData: any) {
    const completed = [];

    try {
      for (const step of this.steps) {
        await this.executeStep(step, orderData);
        completed.push(step);
      }
    } catch (error) {
      // Compensate in reverse order
      for (const step of completed.reverse()) {
        await this.compensateStep(step, orderData);
      }
      throw error;
    }
  }
}
```

**Choreography** (decentralized):
```typescript
// Order Service
async createOrder(data) {
  const order = await this.save(data);
  await this.eventBus.publish('OrderCreated', order);
}

// Payment Service listens to OrderCreated
async onOrderCreated(order) {
  try {
    await this.processPayment(order);
    await this.eventBus.publish('PaymentProcessed', { orderId: order.id });
  } catch (error) {
    await this.eventBus.publish('PaymentFailed', { orderId: order.id });
  }
}
```

### CQRS Pattern
Separate command and query models:

```typescript
// Command Side
interface CreateOrderCommand {
  customerId: string;
  items: OrderItem[];
}

class OrderCommandHandler {
  async handle(command: CreateOrderCommand) {
    const order = Order.create(command);
    await this.eventStore.append(order.getEvents());
  }
}

// Query Side
interface OrderQueryModel {
  id: string;
  customerId: string;
  total: number;
  status: string;
}

class OrderQueryService {
  async getOrder(id: string): Promise<OrderQueryModel> {
    return await this.readModel.findById(id);
  }

  async getOrdersByCustomer(customerId: string): Promise<OrderQueryModel[]> {
    return await this.readModel.findByCustomer(customerId);
  }
}
```

### Event Sourcing
Create event store and projections:

```typescript
// Event Store
class EventStore {
  async append(events: Event[]): Promise<void> {
    for (const event of events) {
      await this.db.query(
        'INSERT INTO events (aggregate_id, event_type, payload, timestamp) VALUES ($1, $2, $3, $4)',
        [event.aggregateId, event.type, JSON.stringify(event.payload), event.timestamp]
      );
    }

    await this.eventBus.publishBatch(events);
  }

  async getEvents(aggregateId: string): Promise<Event[]> {
    const result = await this.db.query(
      'SELECT * FROM events WHERE aggregate_id = $1 ORDER BY version',
      [aggregateId]
    );
    return result.rows.map(row => this.deserializeEvent(row));
  }
}

// Projection
class OrderProjection {
  async handleEvent(event: Event): Promise<void> {
    switch (event.type) {
      case 'OrderCreated':
        await this.db.query(
          'INSERT INTO order_view (id, customer_id, status) VALUES ($1, $2, $3)',
          [event.payload.orderId, event.payload.customerId, 'PENDING']
        );
        break;

      case 'OrderPaid':
        await this.db.query(
          'UPDATE order_view SET status = $1 WHERE id = $2',
          ['PAID', event.payload.orderId]
        );
        break;
    }
  }
}
```

### Circuit Breaker Pattern
Implement resilience pattern:

```typescript
class CircuitBreaker {
  private state: 'CLOSED' | 'OPEN' | 'HALF_OPEN' = 'CLOSED';
  private failureCount = 0;
  private successCount = 0;
  private lastFailureTime: number | null = null;

  constructor(
    private threshold: number = 5,
    private timeout: number = 60000,
    private successThreshold: number = 2
  ) {}

  async execute<T>(operation: () => Promise<T>): Promise<T> {
    if (this.state === 'OPEN') {
      if (Date.now() - this.lastFailureTime! > this.timeout) {
        this.state = 'HALF_OPEN';
        this.successCount = 0;
      } else {
        throw new Error('Circuit breaker is OPEN');
      }
    }

    try {
      const result = await operation();
      this.onSuccess();
      return result;
    } catch (error) {
      this.onFailure();
      throw error;
    }
  }

  private onSuccess() {
    this.failureCount = 0;

    if (this.state === 'HALF_OPEN') {
      this.successCount++;
      if (this.successCount >= this.successThreshold) {
        this.state = 'CLOSED';
      }
    }
  }

  private onFailure() {
    this.failureCount++;
    this.lastFailureTime = Date.now();

    if (this.failureCount >= this.threshold) {
      this.state = 'OPEN';
    }
  }
}
```

## Pattern Application Steps

1. Analyze the problem context
2. Validate pattern applicability
3. Generate pattern implementation
4. Create tests for pattern
5. Update documentation
6. Provide usage examples
7. Suggest related patterns

## Output

For each pattern:
1. Implementation code
2. Unit tests
3. Usage documentation
4. Benefits and trade-offs
5. Related patterns suggestions
