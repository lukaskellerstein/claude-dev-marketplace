---
name: scalability-check
description: Master scalability analysis and optimization for distributed systems. Use when planning for growth, identifying bottlenecks, designing for scale, implementing caching, optimizing databases, load testing, capacity planning, or ensuring horizontal and vertical scalability.
allowed-tools: Read, Glob, Grep
---

# Scalability Analysis Skill

Automatically analyze architecture for scalability bottlenecks and provide comprehensive recommendations for scaling applications horizontally and vertically. This skill ensures systems can handle growth efficiently.

## When to Use This Skill

1. **Capacity Planning** - Preparing for traffic growth
2. **Performance Optimization** - Identifying bottlenecks
3. **Load Testing Analysis** - Interpreting load test results
4. **Architecture Review** - Assessing scalability readiness
5. **Database Scaling** - Planning database growth strategies
6. **Caching Strategy** - Implementing effective caching layers
7. **Auto-Scaling Setup** - Configuring dynamic scaling
8. **CDN Integration** - Optimizing content delivery
9. **API Rate Limiting** - Protecting against overload
10. **Queue Management** - Implementing async processing
11. **Microservices Scaling** - Independent service scaling
12. **Global Distribution** - Multi-region deployment
13. **Cost Optimization** - Efficient resource utilization
14. **SLA Planning** - Ensuring performance targets
15. **Black Friday Prep** - Preparing for traffic spikes

## Quick Start

```python
def quick_scalability_check(system):
    """Quick scalability assessment"""

    issues = []

    # Check for stateful components
    if has_in_memory_state(system):
        issues.append("Stateful services prevent horizontal scaling")

    # Check caching
    if not has_distributed_cache(system):
        issues.append("Missing distributed cache layer")

    # Check database
    if single_database_instance(system):
        issues.append("Single database is bottleneck")

    # Check async processing
    if not has_message_queue(system):
        issues.append("Synchronous processing limits throughput")

    return issues
```

## Scalability Dimensions

### Horizontal Scaling (Scale Out)

```yaml
Requirements for Horizontal Scaling:
  - Stateless services
  - Shared-nothing architecture
  - Load balancing
  - Session management (Redis/Memcached)
  - Distributed caching

Detection of Issues:
  ✗ In-memory session storage
  ✗ File system dependencies
  ✗ Local caching without distributed layer
  ✗ Sticky sessions required
  ✗ Singleton patterns with state

Solution:
  # BAD: Stateful service
  class OrderService:
      def __init__(self):
          self.processing_orders = {}  # In-memory state

  # GOOD: Stateless service
  class OrderService:
      def __init__(self, cache: RedisCache):
          self.cache = cache  # Distributed state

      async def processOrder(self, orderId):
          order = await self.cache.get(f"order:{orderId}")
```

### Vertical Scaling (Scale Up)

```yaml
When to Use Vertical Scaling:
  - Database servers (until sharding needed)
  - CPU-intensive workloads
  - Memory-intensive caching
  - Single-threaded applications

Limitations:
  - Hardware ceiling exists
  - Single point of failure
  - More expensive than horizontal
  - Downtime during upgrades

Recommendation:
  - Use vertical scaling for databases initially
  - Switch to horizontal when limits reached
  - Combine both strategies for optimal results
```

### Data Scaling

```yaml
Strategies:
  1. Database Sharding:
     - Horizontal partitioning by key
     - Geographic sharding
     - Functional sharding

  2. Read Replicas:
     - Route reads to replicas
     - Write to primary
     - Eventual consistency

  3. Caching Layers:
     - CDN for static content
     - Application-level cache (Redis)
     - Database query cache

  4. Data Partitioning:
     - Time-based (archive old data)
     - Geographic (regional databases)
     - Customer-based (multi-tenant isolation)
```

## Real-World Scenarios

### Scenario 1: E-Commerce Black Friday Preparation

**Current Capacity**: 5,000 requests/second
**Target Capacity**: 50,000 requests/second (10x growth)

**Bottleneck Analysis**:
```yaml
1. Database (CRITICAL):
   - Single PostgreSQL instance
   - Write capacity: 1,000 TPS (maxed at peak)
   - Read capacity: 5,000 QPS
   - Impact: Orders failing at peak

2. Application Servers (HIGH):
   - 10 instances, CPU at 85%
   - Insufficient auto-scaling
   - Impact: Slow response times

3. Caching (MEDIUM):
   - No distributed cache
   - Repeated product queries
   - Impact: Unnecessary DB load

4. Static Assets (LOW):
   - No CDN
   - Images served from app servers
   - Impact: Bandwidth usage
```

**Scaling Plan**:
```yaml
Phase 1: Quick Wins (Week 1):
  - Enable Redis caching for products
  - Setup CloudFront CDN
  - Configure auto-scaling (10-50 instances)
  - Expected: 15,000 req/s capacity

Phase 2: Database Scaling (Week 2-3):
  - Add 3 read replicas
  - Implement connection pooling
  - Optimize slow queries
  - Expected: 30,000 req/s capacity

Phase 3: Architecture Evolution (Week 4):
  - Implement CQRS for product catalog
  - Setup Kafka for async order processing
  - Add circuit breakers
  - Expected: 60,000 req/s capacity

Load Test Results:
  Baseline: 5,000 req/s (100% load)
  Phase 1: 15,000 req/s (60% load)
  Phase 2: 30,000 req/s (40% load)
  Phase 3: 60,000 req/s (20% load)

  Target Achieved: ✅ 50,000 req/s with headroom
```

### Scenario 2: SaaS Application Global Expansion

**Challenge**: Expand from US to Europe and Asia with <200ms latency.

**Solution**:
```yaml
Multi-Region Architecture:

Primary Region (US-East):
  - Application servers: 20 instances
  - Database: Primary PostgreSQL
  - Redis cluster: 3 nodes
  - S3: Primary storage

Secondary Region (EU-West):
  - Application servers: 15 instances
  - Database: Read replica + caching
  - Redis cluster: 3 nodes
  - S3: Cross-region replication

Tertiary Region (Asia-Pacific):
  - Application servers: 10 instances
  - Database: Read replica + caching
  - Redis cluster: 3 nodes
  - S3: Cross-region replication

Traffic Routing:
  - Route 53 geo-routing
  - Latency-based routing
  - Health checks and failover

Data Consistency:
  - Writes to US-East (primary)
  - Async replication to other regions
  - Eventual consistency model
  - Conflict resolution strategy

Result:
  US users: 50ms avg latency
  EU users: 80ms avg latency
  APAC users: 120ms avg latency
  Global availability: 99.99%
```

## Performance Patterns

### 1. Caching Strategy

```yaml
Multi-Layer Caching:

1. CDN (Cloudflare/CloudFront):
   Cache-Control: max-age=86400
   Content: Static assets, images, CSS, JS
   Hit Rate: >95%

2. Application Cache (Redis):
   TTL: 5-60 minutes
   Content: Product catalog, user sessions
   Hit Rate Target: >90%

3. Database Query Cache:
   TTL: 1-5 minutes
   Content: Frequently accessed queries
   Hit Rate Target: >80%

4. In-Memory Cache (Application):
   TTL: 1-60 seconds
   Content: Hot data, configuration
   Hit Rate Target: >85%

Implementation:
  async def getProduct(productId: str):
      # L1: In-memory
      if productId in memory_cache:
          return memory_cache[productId]

      # L2: Redis
      cached = await redis.get(f"product:{productId}")
      if cached:
          memory_cache[productId] = cached
          return cached

      # L3: Database
      product = await db.query("SELECT * FROM products WHERE id = $1", productId)

      # Populate caches
      await redis.setex(f"product:{productId}", 3600, product)
      memory_cache[productId] = product

      return product
```

### 2. Database Optimization

```yaml
Scaling Patterns:

1. Read Replicas:
   Primary: Writes only
   Replicas (3): Reads only
   Load balancer: Round-robin

2. Connection Pooling:
   Pool size: 20 connections
   Max wait: 5 seconds
   Reuse connections

3. Indexing Strategy:
   - Composite indexes for common queries
   - Partial indexes for filtered queries
   - Cover indexes for read-heavy tables

4. Query Optimization:
   - Avoid N+1 queries (use joins/eager loading)
   - Limit result sets
   - Use pagination
   - Analyze query plans

5. Database Sharding:
   Shard Key: customer_id
   Shards: 8 (per geographic region)
   Router: Vitess/ProxySQL
```

### 3. Async Processing

```yaml
Message Queue Pattern:

Producer (API):
  POST /orders → Validate → Queue → Return 202 Accepted

Message Broker (Kafka):
  Topic: order-processing
  Partitions: 10
  Retention: 7 days

Consumer Pool:
  Workers: 20 instances
  Parallel processing
  Retry logic
  Dead letter queue

Benefits:
  - Fast API response (50ms)
  - Scalable processing
  - Fault tolerance
  - Load smoothing
```

## Best Practices

```yaml
1. Design for Horizontal Scaling:
   - Stateless services
   - Distributed caching
   - Load balancing

2. Measure Everything:
   - Response times (p50, p95, p99)
   - Throughput (req/s)
   - Error rates
   - Resource utilization

3. Load Test Regularly:
   - Baseline tests weekly
   - Stress tests monthly
   - Chaos engineering quarterly

4. Capacity Planning:
   - Plan for 3x current load
   - Monitor growth trends
   - Automate scaling

5. Optimize Progressively:
   - Profile before optimizing
   - Focus on bottlenecks
   - Measure improvements

6. Cache Aggressively:
   - Multi-layer caching
   - Appropriate TTLs
   - Cache invalidation strategy

7. Async When Possible:
   - Background processing
   - Event-driven architecture
   - Message queues

8. Database Best Practices:
   - Indexes on query columns
   - Connection pooling
   - Read replicas
   - Query optimization
```

## Related Skills

- **service-boundaries**: Ensures services can scale independently
- **anti-patterns**: Identifies scalability anti-patterns
- **caching-strategy**: Implements effective caching layers
- **database-optimization**: Optimizes database for scale
- **load-testing**: Validates scalability improvements

This skill ensures your systems scale efficiently to meet growing demands while maintaining performance and cost-effectiveness.
