---
name: coupling-analysis
description: Master coupling measurement and optimization in software systems. Use when analyzing module dependencies, refactoring codebases, designing interfaces, implementing dependency injection, measuring architecture quality, or ensuring loose coupling and high cohesion.
allowed-tools: Read, Glob, Grep
---

# Coupling Analysis Skill

Automatically measure, analyze, and optimize coupling between components to ensure maintainable, testable, and flexible software architecture. This skill provides comprehensive coupling metrics and actionable recommendations.

## When to Use This Skill

1. **Dependency Analysis** - Understanding component dependencies
2. **Refactoring Planning** - Identifying tightly coupled modules
3. **Interface Design** - Creating loosely coupled interfaces
4. **Module Extraction** - Safely extracting modules from monoliths
5. **Testing Strategy** - Improving testability through loose coupling
6. **Architecture Migration** - Planning service decomposition
7. **Code Review** - Assessing coupling quality
8. **Technical Debt** - Measuring architecture degradation
9. **Microservices Design** - Ensuring service independence
10. **API Design** - Creating minimal coupling between systems
11. **Plugin Architecture** - Designing extensible systems
12. **Library Updates** - Understanding impact of dependency changes
13. **Performance Optimization** - Reducing coupling overhead
14. **Security Analysis** - Identifying tight coupling vulnerabilities
15. **Continuous Architecture** - Monitoring coupling metrics over time

## Quick Start

```python
def analyze_coupling(codebase_path):
    """Quick coupling analysis"""

    analyzer = CouplingAnalyzer()

    # Calculate coupling metrics
    metrics = analyzer.calculate_metrics(codebase_path)

    # Find issues
    tight_coupling = [m for m in metrics if m['instability'] > 0.7 and m['dependents'] > 5]
    circular_deps = analyzer.find_circular_dependencies(codebase_path)

    return {
        'tight_coupling': tight_coupling,
        'circular_dependencies': circular_deps,
        'average_instability': sum(m['instability'] for m in metrics) / len(metrics)
    }
```

## Coupling Types

### 1. Content Coupling (Worst)
```python
# BAD: Accessing internals
class ServiceA:
    def process(self):
        order = serviceB._internalCache.get('order-123')  # Accessing private
        serviceB._privateMethod()  # Calling private method

# GOOD: Public API
class ServiceA:
    def process(self):
        order = serviceB.getOrder('order-123')  # Public API
```

### 2. Common Coupling
```python
# BAD: Global mutable state
global_config = {'db_host': 'localhost'}

class ServiceA:
    def connect(self):
        db.connect(global_config)
        global_config['db_host'] = 'production'  # Modifies shared state

# GOOD: Dependency injection
class ServiceA:
    def __init__(self, config: DatabaseConfig):
        self.config = config

    def connect(self):
        db.connect(self.config)
```

### 3. External Coupling
```python
# BAD: Direct coupling to external API structure
class OrderService:
    def process(self, stripe_charge_object):
        # Directly uses Stripe's structure
        amount = stripe_charge_object.amount
        currency = stripe_charge_object.currency

# GOOD: Anti-corruption layer
class OrderService:
    def process(self, payment: Payment):
        # Internal domain model
        amount = payment.amount
        currency = payment.currency

class StripeAdapter:
    def toDomain(self, stripe_obj) -> Payment:
        return Payment(stripe_obj.amount, stripe_obj.currency)
```

### 4. Control Coupling
```python
# BAD: Control flags
def processPayment(payment, mode: str):
    if mode == 'credit-card':
        # Process credit card
    elif mode == 'paypal':
        # Process PayPal

# GOOD: Strategy pattern
class PaymentProcessor(ABC):
    @abstractmethod
    def process(self, payment: Payment): pass

class CreditCardProcessor(PaymentProcessor):
    def process(self, payment): ...

class PayPalProcessor(PaymentProcessor):
    def process(self, payment): ...
```

### 5. Data Coupling (Best)
```python
# GOOD: Pure data coupling
def calculateTax(amount: Money, taxRate: float) -> Money:
    return amount.multiply(taxRate)

# Clear, explicit, minimal coupling
```

## Coupling Metrics

### Afferent & Efferent Coupling

```python
class CouplingMetrics:
    """Calculate coupling metrics"""

    def calculate_metrics(self, module):
        """Calculate Ca, Ce, and Instability"""

        # Afferent Coupling (Ca): Number of modules depending on this
        ca = len(self.find_dependents(module))

        # Efferent Coupling (Ce): Number of modules this depends on
        ce = len(self.find_dependencies(module))

        # Instability (I = Ce / (Ca + Ce))
        # I = 0: Maximally stable (many depend on it, it depends on few)
        # I = 1: Maximally unstable (few depend on it, it depends on many)
        instability = ce / (ca + ce) if (ca + ce) > 0 else 0

        return {
            'module': module.name,
            'afferent_coupling': ca,
            'efferent_coupling': ce,
            'instability': instability,
            'coupling_level': self.assess_coupling(ca, ce, instability)
        }

    def assess_coupling(self, ca, ce, instability):
        """Assess overall coupling health"""

        if instability > 0.7 and ca > 5:
            return 'Critical'  # Unstable but many depend on it
        elif ce > 10:
            return 'High'  # Depends on too many modules
        elif instability < 0.3 and ca > 3:
            return 'Good'  # Stable with dependents
        else:
            return 'Medium'
```

## Real-World Scenarios

### Scenario 1: Refactoring Tightly Coupled E-Commerce

**Current State**:
```yaml
OrderService:
  Afferent Coupling (Ca): 8 services depend on it
  Efferent Coupling (Ce): 15 services it depends on
  Instability: 0.652
  Assessment: CRITICAL (unstable but many depend on it)

  Dependencies (15):
    - InventoryService (tight, concrete)
    - PaymentService (tight, concrete)
    - ShippingService (tight, concrete)
    - CustomerService (loose, interface)
    - ProductService (tight, concrete)
    - NotificationService (tight, concrete)
    - AnalyticsService (tight, concrete)
    - TaxService (tight, concrete)
    - DiscountService (tight, concrete)
    - LoyaltyService (tight, concrete)
    - EmailService (tight, concrete)
    - SMSService (tight, concrete)
    - AuditService (tight, concrete)
    - LoggingService (tight, concrete)
    - CacheService (tight, concrete)
```

**Refactoring Plan**:
```yaml
Phase 1: Interface Extraction
  - Create interfaces for all dependencies
  - Implement dependency injection
  - Target Instability: 0.4

Phase 2: Service Decomposition
  - Split OrderService into:
    * OrderManagementService (CRUD)
    * OrderFulfillmentService (workflow)
    * OrderValidationService (business rules)
  - Reduce dependencies to 5 per service

Phase 3: Event-Driven Migration
  - Convert 8 dependencies to async events
  - Use message broker for notifications
  - Target Efferent Coupling: 5

Result:
  OrderManagementService:
    Ce: 5 (CustomerService, ProductService, InventoryService, PricingService, EventBus)
    Ca: 4 (API Gateway, OrderFulfillmentService, ReportingService, AdminUI)
    Instability: 0.357 (Good - stable with moderate dependencies)
```

## Best Practices

### 1. Depend on Abstractions
```python
# GOOD: Dependency Inversion Principle
class OrderService:
    def __init__(
        self,
        payment_gateway: PaymentGateway,  # Interface
        order_repo: OrderRepository  # Interface
    ):
        self.payment_gateway = payment_gateway
        self.order_repo = order_repo
```

### 2. Minimize Dependencies
```yaml
Guidelines:
  - Core modules: < 3 dependencies
  - Application services: < 5 dependencies
  - UI components: < 8 dependencies
  - If > 10 dependencies: Consider splitting module
```

### 3. Stable Dependencies Principle
```yaml
Rule: Depend in the direction of stability
  - Unstable modules depend on stable modules
  - Not the reverse

Example:
  UI (Unstable, I=1.0)
    ↓ depends on
  Application Services (Medium, I=0.5)
    ↓ depends on
  Domain Model (Stable, I=0.1)
```

## Related Skills

- **service-boundaries**: Defines proper service boundaries to reduce coupling
- **anti-patterns**: Identifies tight coupling anti-patterns
- **dependency-injection**: Implements loose coupling through DI
- **interface-design**: Creates minimal coupling interfaces
- **architecture-metrics**: Tracks coupling trends over time

## Metrics Dashboard

```yaml
Target Metrics:
  Average Instability: < 0.4
  Max Dependencies per Module: 5
  Modules with Tight Coupling: 0
  Circular Dependencies: 0

Current vs Target:
  Metric                  | Current | Target | Status
  ----------------------- | ------- | ------ | ------
  Avg Instability         | 0.42    | 0.40   | ⚠️
  Max Dependencies        | 15      | 5      | ❌
  Tight Coupling Count    | 10      | 0      | ❌
  Circular Dependencies   | 2       | 0      | ❌
```

This skill ensures your architecture maintains loose coupling for maximum flexibility, testability, and maintainability.
