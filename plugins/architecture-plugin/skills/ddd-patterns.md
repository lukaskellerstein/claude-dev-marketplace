---
name: ddd-patterns
description: Auto-invoked when working with domain models, aggregates, entities, or value objects to ensure proper DDD patterns
allowed-tools: Read, Grep, Glob
---

# Domain-Driven Design Patterns

This skill provides guidance on applying DDD patterns correctly when working with domain models.

## When Active

This skill activates when you:
- Create or modify domain models, entities, or value objects
- Design aggregates and aggregate roots
- Work with repositories or domain services
- Implement domain events

## DDD Building Blocks

### Entities
- Have unique identity that persists over time
- Identity is defined by ID, not attributes
- Mutable - attributes can change
- Example: User, Order, Product

```typescript
class Order {
  constructor(
    private readonly id: OrderId,  // Value object for type safety
    private items: OrderItem[],
    private status: OrderStatus
  ) {}

  // Business logic methods
  addItem(item: OrderItem): void { }
  cancel(): void { }
}
```

### Value Objects
- No identity - defined by attributes
- Immutable - create new instance for changes
- Interchangeable if attributes match
- Example: Money, Address, DateRange

```typescript
class Money {
  constructor(
    readonly amount: number,
    readonly currency: string
  ) {
    Object.freeze(this);
  }

  add(other: Money): Money {
    if (this.currency !== other.currency) {
      throw new Error('Currency mismatch');
    }
    return new Money(this.amount + other.amount, this.currency);
  }
}
```

### Aggregates
- Cluster of entities and value objects
- Aggregate root is the entry point
- Enforce invariants across the cluster
- Transactional boundary
- External references only through root ID

```typescript
class Order {  // Aggregate root
  private items: OrderItem[] = [];  // Internal entities
  private totalAmount: Money;        // Value object

  addItem(item: OrderItem): void {
    // Enforce invariant: max 20 items
    if (this.items.length >= 20) {
      throw new Error('Order cannot exceed 20 items');
    }
    this.items.push(item);
    this.recalculateTotal();
  }

  private recalculateTotal(): void {
    // Maintain consistency
  }
}
```

### Repositories
- Persist and retrieve aggregates
- Interface in domain layer, implementation in infrastructure
- Work with aggregate roots only
- Encapsulate storage details

```typescript
interface OrderRepository {
  save(order: Order): Promise<void>;
  findById(id: OrderId): Promise<Order | null>;
  findByCustomer(customerId: CustomerId): Promise<Order[]>;
}
```

### Domain Services
- Domain logic that doesn't belong to a single entity
- Stateless operations
- Coordinate between aggregates
- Named with verb (not noun)

```typescript
class TransferMoneyService {
  transfer(
    from: Account,
    to: Account,
    amount: Money
  ): void {
    from.debit(amount);
    to.credit(amount);
  }
}
```

### Domain Events
- Something that happened in the domain
- Named in past tense
- Immutable
- Contains necessary data for subscribers

```typescript
class OrderPlaced {
  constructor(
    readonly orderId: OrderId,
    readonly customerId: CustomerId,
    readonly orderDate: Date,
    readonly totalAmount: Money
  ) {}
}
```

## Best Practices

1. **Ubiquitous Language**: Use domain terms everywhere - code, docs, conversations
2. **Small Aggregates**: Keep aggregates as small as possible
3. **Reference by ID**: Aggregates reference each other by ID, not direct reference
4. **Consistency Boundaries**: Each aggregate is a consistency boundary
5. **Domain Logic in Domain Layer**: Business rules belong in entities/value objects
6. **Thin Controllers**: Controllers orchestrate, domain models decide

## Anti-Patterns to Avoid

- **Anemic Domain Model**: Entities with only getters/setters, logic in services
- **Large Aggregates**: Too many entities in one aggregate
- **Direct Aggregate References**: Aggregates holding references to other aggregates
- **Domain Logic in Services**: Putting business rules in application services
- **Violating Encapsulation**: Public setters exposing internal state

## Checklist

When creating/modifying domain code:
- [ ] Is this an entity (has identity) or value object (defined by attributes)?
- [ ] Does the aggregate enforce all invariants?
- [ ] Are aggregates small and focused?
- [ ] Do aggregates reference each other by ID only?
- [ ] Is domain logic in domain objects, not services?
- [ ] Are value objects immutable?
- [ ] Do domain events capture important business moments?
- [ ] Does code use ubiquitous language?

Use this guidance to ensure domain models follow DDD best practices.
