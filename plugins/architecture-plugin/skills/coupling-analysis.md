---
name: coupling-analysis
description: Measures and reports coupling between components
allowed-tools: Read, Glob, Grep
---

# Coupling Analysis Skill

Automatically measures coupling between components and provides detailed analysis and recommendations. This skill triggers when analyzing architecture quality or refactoring codebases.

## Coupling Types

### 1. Content Coupling (Worst)

One module modifies or relies on internal workings of another.

**Detection**:
```typescript
// BAD: Service A accesses Service B's internal data
class ServiceA {
  processOrder(orderId: string) {
    const order = serviceB.internalOrderCache.get(orderId); // Accessing internals
    const data = serviceB.privateMethod(); // Calling private method
  }
}
```

**Impact**:
- Extremely fragile
- Any internal change breaks callers
- Impossible to maintain
- Cannot test independently

**Fix**:
```typescript
// GOOD: Use public API
class ServiceA {
  constructor(private serviceB: ServiceBInterface) {}

  processOrder(orderId: string) {
    const order = this.serviceB.getOrder(orderId); // Public API
  }
}
```

### 2. Common Coupling

Multiple modules share global data.

**Detection**:
```typescript
// BAD: Shared mutable global state
export const globalConfig = {
  database: { host: 'localhost', port: 5432 },
  api: { timeout: 5000 }
};

class ServiceA {
  connect() {
    db.connect(globalConfig.database); // Modifying shared state
    globalConfig.database.host = 'production-db';
  }
}

class ServiceB {
  connect() {
    db.connect(globalConfig.database); // Affected by ServiceA changes
  }
}
```

**Impact**:
- Side effects
- Hard to track changes
- Race conditions
- Testing difficulties

**Fix**:
```typescript
// GOOD: Dependency injection
class ServiceA {
  constructor(private config: DatabaseConfig) {}

  connect() {
    db.connect(this.config);
  }
}

class ServiceB {
  constructor(private config: DatabaseConfig) {}

  connect() {
    db.connect(this.config);
  }
}
```

### 3. External Coupling

Dependency on external format, protocol, or device.

**Detection**:
```typescript
// Coupling to external API structure
interface ExternalOrder {
  order_id: string;      // External format
  customer_info: {...};  // External structure
  line_items: [...];     // External naming
}

class OrderService {
  processOrder(externalOrder: ExternalOrder) {
    // Directly using external structure throughout codebase
  }
}
```

**Impact**:
- External changes ripple through system
- Hard to switch providers
- Integration difficulties

**Fix**:
```typescript
// GOOD: Anti-Corruption Layer
interface Order {
  id: string;           // Internal format
  customer: Customer;   // Internal structure
  items: OrderItem[];   // Internal naming
}

class ExternalOrderAdapter {
  toDomain(external: ExternalOrder): Order {
    return {
      id: external.order_id,
      customer: this.mapCustomer(external.customer_info),
      items: this.mapItems(external.line_items)
    };
  }
}

class OrderService {
  processOrder(order: Order) {
    // Uses internal domain model
  }
}
```

### 4. Control Coupling

One module controls flow of another by passing flags.

**Detection**:
```typescript
// BAD: Control flag coupling
function processPayment(payment: Payment, mode: string) {
  if (mode === 'credit-card') {
    // Process credit card
  } else if (mode === 'paypal') {
    // Process PayPal
  } else if (mode === 'bitcoin') {
    // Process Bitcoin
  }
}

// Caller controls internal logic
processPayment(payment, 'credit-card');
```

**Impact**:
- Caller knows too much about implementation
- Adding new payment types requires changing this function
- Violation of Open/Closed Principle

**Fix**:
```typescript
// GOOD: Strategy pattern
interface PaymentProcessor {
  process(payment: Payment): Promise<PaymentResult>;
}

class CreditCardProcessor implements PaymentProcessor {
  process(payment: Payment) { /* ... */ }
}

class PayPalProcessor implements PaymentProcessor {
  process(payment: Payment) { /* ... */ }
}

// Factory to create appropriate processor
class PaymentProcessorFactory {
  create(type: PaymentType): PaymentProcessor {
    switch (type) {
      case PaymentType.CREDIT_CARD: return new CreditCardProcessor();
      case PaymentType.PAYPAL: return new PayPalProcessor();
    }
  }
}

// Caller doesn't control flow
const processor = factory.create(payment.type);
const result = await processor.process(payment);
```

### 5. Stamp Coupling (Data Structure)

Modules share composite data structure, but only use part of it.

**Detection**:
```typescript
// BAD: Passing entire object when only need part
function calculateShipping(order: Order): Money {
  // Only uses order.weight and order.destination
  // But receives entire Order object with 50+ fields
  return shippingCalculator.calculate(order.weight, order.destination);
}
```

**Impact**:
- Unnecessary dependencies
- Hard to understand what's actually used
- Difficult to test
- Coupling to entire structure

**Fix**:
```typescript
// GOOD: Pass only what's needed
interface ShippingInfo {
  weight: Weight;
  destination: Address;
}

function calculateShipping(info: ShippingInfo): Money {
  return shippingCalculator.calculate(info.weight, info.destination);
}

// Or even better: specific parameters
function calculateShipping(weight: Weight, destination: Address): Money {
  return shippingCalculator.calculate(weight, destination);
}
```

### 6. Data Coupling (Best)

Modules share data through parameters.

```typescript
// GOOD: Data coupling - minimal and explicit
function calculateTax(amount: Money, taxRate: number): Money {
  return amount.multiply(taxRate);
}

// Clear what data is needed
// Easy to test
// No hidden dependencies
```

## Coupling Metrics

### Afferent Coupling (Ca)

Number of classes/modules that depend on this module.

**Calculation**:
```
Ca = Number of incoming dependencies

Example:
  ModuleA ─┐
  ModuleB ─┼─→ ModuleX
  ModuleC ─┘

  ModuleX.Ca = 3 (A, B, and C depend on X)
```

**Interpretation**:
- High Ca = Many modules depend on this
- Changes affect many modules
- Should be stable

### Efferent Coupling (Ce)

Number of classes/modules this module depends on.

**Calculation**:
```
Ce = Number of outgoing dependencies

Example:
  ModuleX ─┬─→ ModuleA
           ├─→ ModuleB
           └─→ ModuleC

  ModuleX.Ce = 3 (X depends on A, B, and C)
```

**Interpretation**:
- High Ce = Depends on many modules
- More reasons to change
- Less stable

### Instability (I)

Measure of module's susceptibility to change.

**Formula**:
```
I = Ce / (Ca + Ce)

Range: 0 to 1
  I = 0: Maximally stable (many depend on it, depends on none)
  I = 1: Maximally unstable (none depend on it, depends on many)
```

**Examples**:
```
Stable Core Module:
  Ca = 10 (many depend on it)
  Ce = 2 (depends on few)
  I = 2 / (10 + 2) = 0.167 (very stable)

Unstable UI Module:
  Ca = 0 (nothing depends on it)
  Ce = 15 (depends on many)
  I = 15 / (0 + 15) = 1.0 (very unstable)
```

**Best Practice**:
- Core/domain modules should have low I (0.0 - 0.3)
- Infrastructure/adapters can have higher I (0.7 - 1.0)
- High I + High Ca = Dangerous (unstable but many depend on it)

## Coupling Levels

### Tight Coupling

**Characteristics**:
- Direct dependencies
- Concrete implementations
- Shared state
- Synchronous communication

**Example**:
```typescript
// Tightly coupled
class OrderService {
  processOrder(order: Order) {
    const db = new MySQLDatabase('localhost', 3306); // Concrete dependency
    db.save(order);

    const payment = new StripePayment('api-key'); // Concrete dependency
    payment.charge(order.total);
  }
}
```

**Problems**:
- Hard to test (requires real MySQL and Stripe)
- Can't swap implementations
- Changes to MySQL/Stripe affect OrderService

### Loose Coupling

**Characteristics**:
- Abstract dependencies
- Dependency injection
- Message-based communication
- Independent deployability

**Example**:
```typescript
// Loosely coupled
interface OrderRepository {
  save(order: Order): Promise<void>;
}

interface PaymentGateway {
  charge(amount: Money): Promise<PaymentResult>;
}

class OrderService {
  constructor(
    private orderRepo: OrderRepository,
    private paymentGateway: PaymentGateway
  ) {}

  async processOrder(order: Order) {
    await this.orderRepo.save(order);
    await this.paymentGateway.charge(order.total);
  }
}

// Easy to test with mocks
// Can swap implementations
// Changes to impl don't affect OrderService
```

## Analysis Output Format

```json
{
  "module": "OrderService",
  "metrics": {
    "afferent": 5,
    "efferent": 8,
    "instability": 0.615,
    "coupling_level": "medium"
  },
  "dependencies": [
    {
      "module": "PaymentService",
      "type": "data",
      "strength": "low",
      "interface": true
    },
    {
      "module": "InventoryService",
      "type": "control",
      "strength": "high",
      "interface": false,
      "warning": "Direct coupling to concrete implementation"
    }
  ],
  "dependents": [
    {
      "module": "APIGateway",
      "type": "data",
      "strength": "low"
    },
    {
      "module": "OrderController",
      "type": "data",
      "strength": "low"
    }
  ],
  "issues": [
    {
      "severity": "high",
      "type": "tight_coupling",
      "description": "Direct dependency on InventoryService concrete class",
      "recommendation": "Introduce IInventoryService interface"
    },
    {
      "severity": "medium",
      "type": "high_instability",
      "description": "Instability 0.615 with 5 dependents",
      "recommendation": "Consider reducing outgoing dependencies"
    }
  ],
  "recommendations": [
    "Introduce interfaces for external dependencies",
    "Consider event-driven communication with InventoryService",
    "Split OrderService into smaller, focused services",
    "Reduce instability to below 0.5"
  ]
}
```

## Coupling Analysis Report

```markdown
## Coupling Analysis Report

### Executive Summary
- Total modules analyzed: 45
- Average instability: 0.42
- Modules with high coupling: 8
- Critical issues: 3

### High Coupling Modules

#### 1. OrderService (Critical)
**Metrics**:
- Afferent Coupling: 8
- Efferent Coupling: 15
- Instability: 0.652
- Coupling Level: High

**Dependencies** (15):
- InventoryService (tight, concrete)
- PaymentService (tight, concrete)
- ShippingService (tight, concrete)
- CustomerService (loose, interface)
- ProductService (tight, concrete)
- NotificationService (tight, concrete)
- ... 9 more

**Issues**:
1. Too many direct dependencies (15 > recommended 5)
2. Tight coupling to 10 concrete implementations
3. High instability (0.652) with many dependents (8)
4. Single responsibility principle violation

**Recommendations**:
1. Introduce interfaces for all dependencies
2. Split into smaller services:
   - OrderManagementService (CRUD)
   - OrderFulfillmentService (workflow)
   - OrderValidationService (business rules)
3. Use event-driven architecture for:
   - Inventory updates
   - Notifications
   - Analytics
4. Implement facade pattern for complex workflows

**Priority**: P0 - Critical

#### 2. InventoryService (High)
**Metrics**:
- Afferent Coupling: 12
- Efferent Coupling: 6
- Instability: 0.333
- Coupling Level: Medium

**Dependents** (12):
Many services depend on InventoryService, but instability is moderate.

**Issues**:
1. Too many direct dependents (12 > recommended 5)
2. Synchronous calls causing latency
3. Shared database access from multiple services

**Recommendations**:
1. Implement event-driven inventory updates
2. Introduce inventory snapshot pattern
3. Cache inventory levels
4. Rate limiting to prevent overload

**Priority**: P1 - High

### Coupling Improvement Plan

**Phase 1: Interface Extraction (Week 1-2)**
- Extract interfaces for all tightly coupled services
- Implement dependency injection
- Update tests to use interfaces

**Phase 2: Event-Driven Migration (Week 3-6)**
- Identify async candidates
- Implement message broker
- Migrate synchronous calls to events
- Maintain backward compatibility

**Phase 3: Service Decomposition (Week 7-12)**
- Split high-coupling services
- Implement API gateways
- Setup service mesh
- Monitor and optimize

### Metrics Tracking

Target Metrics:
- Average instability: < 0.4
- Max dependencies per service: 5
- Services with tight coupling: 0
- Code coverage: > 80%

Current vs Target:
| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| Avg Instability | 0.42 | 0.40 | ⚠️ Close |
| Max Dependencies | 15 | 5 | ❌ High |
| Tight Coupling | 10 | 0 | ❌ High |
| Coverage | 65% | 80% | ⚠️ Medium |
```

## Best Practices

1. **Depend on Abstractions**: Not concrete implementations
2. **Dependency Inversion**: High-level modules don't depend on low-level
3. **Interface Segregation**: Many specific interfaces > one general
4. **Minimize Dependencies**: Only depend on what you need
5. **Stable Dependencies**: Depend on stable abstractions
6. **Measure Regularly**: Track coupling metrics over time
7. **Refactor Incrementally**: Reduce coupling step by step

## Tools Integration

Integrate coupling analysis into:
- Pre-commit hooks (warn on high coupling)
- CI/CD pipeline (fail on coupling threshold)
- Code reviews (coupling metrics in PRs)
- Architecture reviews (quarterly coupling reports)
- Monitoring dashboards (track coupling trends)

Follow these guidelines to maintain loose coupling and high cohesion in your architecture.
