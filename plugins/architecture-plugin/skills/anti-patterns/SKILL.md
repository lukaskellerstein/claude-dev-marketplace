---
name: anti-patterns
description: Master architectural anti-pattern detection and remediation. Use when reviewing system architecture, refactoring legacy code, preventing design issues, analyzing distributed systems, implementing microservices, or ensuring architectural quality and maintainability.
allowed-tools: Read, Glob, Grep
---

# Anti-Patterns Detection Skill

Automatically detect common architectural anti-patterns and provide actionable remediation strategies. This skill helps maintain clean, scalable architecture by identifying and preventing design problems before they become critical.

## When to Use This Skill

This skill activates and provides value in these scenarios:

1. **Architecture Reviews** - Conducting systematic architecture quality assessments
2. **Code Refactoring** - Identifying technical debt and design issues
3. **Microservices Migration** - Avoiding distributed system anti-patterns
4. **Legacy System Analysis** - Understanding and documenting existing problems
5. **New Project Setup** - Preventing anti-patterns from the start
6. **Performance Troubleshooting** - Finding architectural root causes
7. **Scalability Planning** - Identifying bottlenecks before scaling
8. **Team Onboarding** - Teaching architectural best practices
9. **Technical Debt Assessment** - Quantifying architecture quality issues
10. **Pre-Production Reviews** - Validating architecture before deployment
11. **Incident Post-Mortems** - Identifying architectural causes of failures
12. **Compliance Audits** - Ensuring architectural standards compliance
13. **Merger Integration** - Analyzing and harmonizing different architectures
14. **Technology Selection** - Avoiding technology-driven anti-patterns
15. **Continuous Architecture** - Ongoing architecture quality monitoring

## Quick Start

### Run Anti-Pattern Detection

```python
def quick_scan(codebase_path):
    """Quick scan for common anti-patterns"""

    detector = AntiPatternDetector()

    issues = []
    issues.extend(detector.detect_distributed_monolith(codebase_path))
    issues.extend(detector.detect_god_services(codebase_path))
    issues.extend(detector.detect_shared_database(codebase_path))
    issues.extend(detector.detect_chatty_interfaces(codebase_path))
    issues.extend(detector.detect_circular_dependencies(codebase_path))

    # Prioritize by severity
    critical = [i for i in issues if i['severity'] == 'Critical']
    high = [i for i in issues if i['severity'] == 'High']

    return {
        'critical': critical,
        'high': high,
        'total': len(issues)
    }
```

## Real-World Scenarios

### Scenario 1: Distributed Monolith Detection

**Context**: Company migrated to microservices but experiencing deployment issues.

**Detection**:
```yaml
Symptoms Observed:
  - All services must deploy together
  - Schema changes affect multiple services
  - Integration tests require all services running
  - No independent scaling possible

Analysis Results:
  ✗ Shared PostgreSQL database (12 services)
  ✗ Synchronous HTTP calls between all services
  ✗ No API versioning implemented
  ✗ Shared domain models in common library
  ✗ Deployment scripts deploy all services

Verdict: DISTRIBUTED MONOLITH
  - Has microservices structure
  - Maintains monolith coupling
  - Worst of both architectures
```

**Remediation**:
```yaml
Phase 1: Database Isolation (Weeks 1-4)
  - Identify data ownership per service
  - Create service-specific schemas
  - Implement database-per-service pattern
  - Setup CDC for data synchronization

Phase 2: API Versioning (Weeks 5-6)
  - Implement URI versioning (v1, v2)
  - Support multiple API versions
  - Create deprecation strategy
  - Update clients gradually

Phase 3: Event-Driven Migration (Weeks 7-10)
  - Setup Kafka/RabbitMQ message broker
  - Convert sync calls to async events
  - Implement saga pattern for workflows
  - Add circuit breakers

Phase 4: Independent Deployment (Weeks 11-12)
  - Separate CI/CD pipelines per service
  - Implement feature flags
  - Setup canary deployments
  - Enable independent scaling
```

### Scenario 2: God Service Refactoring

**Context**: ProductService has become unmaintainable monolith.

**Current State**:
```yaml
ProductService (45 endpoints, 25,000 LOC):
  Product Management:
    - CRUD operations
    - Category management
    - Product search
    - Bulk imports

  Inventory:
    - Stock level tracking
    - Warehouse management
    - Stock alerts
    - Inventory forecasting

  Pricing:
    - Price calculations
    - Discount rules
    - Dynamic pricing
    - Price history

  Reviews & Ratings:
    - Customer reviews
    - Rating aggregation
    - Review moderation
    - Sentiment analysis

  Recommendations:
    - ML-based recommendations
    - Cross-sell suggestions
    - Trending products
    - Personalization
```

**Refactoring Plan**:
```yaml
Target Architecture (5 Focused Services):

1. ProductCatalogService (10 endpoints):
   Responsibility: Product information
   Database: products_db (PostgreSQL)
   Endpoints:
     - GET/POST/PUT/DELETE /products
     - GET /products/search
     - GET /categories

2. InventoryService (8 endpoints):
   Responsibility: Stock management
   Database: inventory_db (PostgreSQL)
   Endpoints:
     - GET /stock/{productId}
     - POST /stock/reserve
     - POST /stock/release
     - GET /warehouses

3. PricingService (6 endpoints):
   Responsibility: Dynamic pricing
   Database: pricing_db (PostgreSQL)
   Endpoints:
     - GET /price/{productId}
     - POST /discounts
     - GET /price-history

4. ReviewService (8 endpoints):
   Responsibility: Reviews and ratings
   Database: reviews_db (MongoDB)
   Endpoints:
     - GET/POST /reviews
     - GET /ratings/{productId}
     - POST /moderate

5. RecommendationService (5 endpoints):
   Responsibility: ML recommendations
   Database: recommendations_db (Redis + PostgreSQL)
   Endpoints:
     - GET /recommend/{userId}
     - GET /trending
     - GET /similar/{productId}

Benefits Achieved:
  - Team autonomy (each team owns one service)
  - Independent scaling (recommendations need more resources)
  - Technology choice (MongoDB for reviews, Redis for caching)
  - Faster deployments (small services deploy quickly)
  - Better fault isolation (review failure doesn't affect catalog)
```

### Scenario 3: Chatty Interface Optimization

**Context**: E-commerce checkout takes 3+ seconds due to service chatter.

**Problem Analysis**:
```yaml
Current Flow (18 synchronous calls):
  Client → API Gateway
    ↓
  OrderService (200ms)
    ↓ GET /customer
  CustomerService (150ms)
    ↓ GET /customer/address
  AddressService (100ms)
    ↓ GET /customer/payment-methods
  PaymentService (120ms)
    ↓ GET /cart
  CartService (150ms)
    ↓ For each cart item (5 items):
      ├→ GET /product/{id} × 5
      │  ProductService (100ms each)
      ├→ GET /stock/{id} × 5
      │  InventoryService (80ms each)
      └→ GET /price/{id} × 5
         PricingService (90ms each)

  Total Sequential Latency: 2,550ms
  Total Network Roundtrips: 18
  P99 Latency: 3,200ms
```

**Solution 1: API Gateway Aggregation**:
```yaml
New Flow (Parallel Execution):
  Client → API Gateway
    ├→ OrderService (200ms)
    ├→ CustomerService (150ms) ┐
    ├→ AddressService (100ms)  ├ Parallel
    ├→ PaymentService (120ms)  ┘
    └→ CartService (150ms)
         ↓ Batch Request
       [ProductService + InventoryService + PricingService]
         Batch API (300ms for all 5 items)

  Total Latency: max(200, 150, 100, 120, 450) = 450ms
  Improvement: 5.6x faster
  P99 Latency: 650ms
```

**Solution 2: Backend for Frontend (BFF)**:
```yaml
CheckoutBFF Service:
  - Aggregates all checkout data
  - Caches frequently accessed data
  - Optimizes for checkout flow
  - Single API call from client

  Endpoint: POST /checkout/prepare
  Returns:
    - Customer details
    - Saved addresses
    - Payment methods
    - Cart with enriched product data
    - Total price with taxes

  Latency: 300ms (with caching)
  Improvement: 8.5x faster
```

## Detection Methods

### Automated Detection Rules

```python
class AntiPatternDetector:
    """Comprehensive anti-pattern detection"""

    RULES = {
        'distributed_monolith': {
            'checks': [
                'shared_database',
                'no_api_versioning',
                'synchronous_coupling',
                'shared_libraries'
            ],
            'severity': 'Critical',
            'threshold': 3  # 3+ checks = anti-pattern
        },
        'god_service': {
            'checks': [
                'endpoint_count > 20',
                'multiple_capabilities',
                'large_codebase > 10000_lines'
            ],
            'severity': 'High',
            'threshold': 2
        },
        'chatty_interface': {
            'checks': [
                'calls_per_request > 10',
                'sequential_calls > 5',
                'network_latency > 1000ms'
            ],
            'severity': 'High',
            'threshold': 2
        }
    }

    def detect_all(self, codebase_path):
        """Run all detection rules"""
        findings = []

        for pattern, rule in self.RULES.items():
            result = self.evaluate_rule(pattern, rule, codebase_path)
            if result['detected']:
                findings.append(result)

        return findings
```

## Best Practices

### Prevention Strategies

```yaml
1. Architecture Decision Records (ADRs):
   - Document all architectural decisions
   - Include context and consequences
   - Review regularly

2. Automated Quality Gates:
   - Dependency analysis in CI/CD
   - Code complexity metrics
   - Architecture conformance tests

3. Regular Architecture Reviews:
   - Monthly architecture health checks
   - Quarterly deep-dive reviews
   - Annual architecture refresh

4. Team Training:
   - Anti-patterns workshop
   - Code review guidelines
   - Architecture documentation

5. Monitoring & Alerting:
   - Track service dependencies
   - Monitor coupling metrics
   - Alert on threshold violations
```

## Related Skills

- **service-boundaries**: Proper service boundary design prevents anti-patterns
- **coupling-analysis**: Measures coupling to detect anti-patterns early
- **scalability-check**: Identifies scalability anti-patterns
- **code-quality**: Prevents code-level anti-patterns
- **architecture-review**: Systematic anti-pattern identification process

## Common Anti-Patterns Reference

### 1. Distributed Monolith
- **Detection**: Services must deploy together
- **Impact**: No microservices benefits
- **Fix**: Database-per-service, async communication, API versioning

### 2. God Service
- **Detection**: >20 endpoints, multiple capabilities
- **Impact**: Hard to maintain, slow deployments
- **Fix**: Split by business capability

### 3. Chatty Interface
- **Detection**: >10 calls per request
- **Impact**: High latency, poor UX
- **Fix**: API Gateway, BFF, caching

### 4. Shared Database
- **Detection**: Multiple services accessing same tables
- **Impact**: Tight coupling, can't scale independently
- **Fix**: Database-per-service, events for sync

### 5. Circular Dependencies
- **Detection**: Service A → B → C → A
- **Impact**: Can't deploy independently
- **Fix**: Event-driven architecture

### 6. Anemic Services
- **Detection**: Only CRUD operations
- **Impact**: Business logic in orchestration layer
- **Fix**: Move domain logic into services

### 7. Missing Abstraction
- **Detection**: Infrastructure code in domain layer
- **Impact**: Tight coupling to frameworks
- **Fix**: Repository pattern, domain interfaces

This skill ensures your architecture remains clean, maintainable, and free from common design problems.
