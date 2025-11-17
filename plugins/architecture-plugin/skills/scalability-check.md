---
name: scalability-check
description: Analyzes architecture for scalability issues
allowed-tools: Read, Glob, Grep
---

# Scalability Analysis Skill

Automatically analyzes architecture for scalability bottlenecks and provides recommendations for improving system scalability. This skill triggers when reviewing architecture or planning for growth.

## Scalability Dimensions

### Horizontal Scaling (Scale Out)

Ability to add more instances/servers to handle increased load.

**Requirements**:
- Stateless services
- Shared-nothing architecture
- Load balancing
- Session management
- Distributed caching

**Detection**:
```
Check for:
- In-memory state management
- File system dependencies
- Local caching
- Session affinity requirements
- Sticky sessions
```

**Issues Found**:
```typescript
// BAD: Stateful service
class OrderService {
  private processingOrders = new Map<string, Order>(); // In-memory state

  async processOrder(orderId: string) {
    const order = this.processingOrders.get(orderId);
    // Problem: state lost if instance dies or when load balanced
  }
}

// GOOD: Stateless service
class OrderService {
  constructor(private cache: RedisCache) {}

  async processOrder(orderId: string) {
    const order = await this.cache.get(`order:${orderId}`);
    // Distributed cache, can scale horizontally
  }
}
```

**Recommendations**:
- Move session state to Redis/Memcached
- Use distributed caching
- Implement sticky session-free design
- Store uploads in S3/object storage
- Use database for persistent state

### Vertical Scaling (Scale Up)

Ability to use more powerful hardware (CPU, RAM).

**Detection**:
```
Analyze:
- CPU intensive operations
- Memory usage patterns
- I/O operations
- Algorithm complexity
```

**Limitations**:
- Hardware ceiling (can't infinitely scale up)
- Single point of failure
- More expensive than horizontal scaling
- Downtime during upgrades

**When Vertical Scaling Makes Sense**:
- Database servers (until sharding needed)
- CPU-intensive workloads
- Memory-intensive caching
- Legacy applications that can't scale horizontally

### Data Scaling

Ability to handle growing data volumes.

**Strategies**:
- Database sharding
- Read replicas
- Caching layers
- Data partitioning
- Archival strategies

## Performance Patterns

### 1. Caching

**Levels of Caching**:
```
1. CDN (Content Delivery Network)
   - Static assets
   - HTML pages
   - API responses

2. Application-Level Cache (Redis, Memcached)
   - Database query results
   - Computed values
   - Session data

3. Database Query Cache
   - Frequently accessed data
   - Query result sets

4. Database Connection Pooling
   - Reuse connections
   - Reduce connection overhead
```

**Detection**:
```
Look for:
- Repeated database queries
- Expensive computations
- External API calls
- Static content without cache headers
```

**Anti-Patterns**:
```typescript
// BAD: No caching
app.get('/products/:id', async (req, res) => {
  const product = await db.query(
    'SELECT * FROM products WHERE id = $1',
    [req.params.id]
  );
  res.json(product);
});

// GOOD: With caching
app.get('/products/:id', async (req, res) => {
  const cacheKey = `product:${req.params.id}`;

  // Try cache first
  let product = await cache.get(cacheKey);

  if (!product) {
    // Cache miss, fetch from database
    product = await db.query(
      'SELECT * FROM products WHERE id = $1',
      [req.params.id]
    );

    // Store in cache for 1 hour
    await cache.setex(cacheKey, 3600, JSON.stringify(product));
  }

  res.json(product);
});
```

### 2. Circuit Breakers

Prevent cascading failures and provide fault tolerance.

**Detection**:
```
Look for:
- Direct service calls without protection
- No timeout handling
- No retry logic
- No fallback mechanisms
```

**Implementation**:
```typescript
// With circuit breaker
class PaymentService {
  private circuitBreaker = new CircuitBreaker({
    threshold: 5,        // Open after 5 failures
    timeout: 60000,      // Try again after 60 seconds
    resetTimeout: 10000  // Reset after 10 seconds of success
  });

  async processPayment(payment: Payment): Promise<PaymentResult> {
    return await this.circuitBreaker.execute(async () => {
      return await this.paymentGateway.charge(payment);
    });
  }
}
```

### 3. Rate Limiting

Protect services from overload.

**Detection**:
```
Check for:
- Missing rate limits on APIs
- No throttling mechanisms
- No queue management
- No backpressure handling
```

**Implementation Strategies**:
```
1. Fixed Window:
   - 100 requests per minute

2. Sliding Window:
   - Rolling window of last 60 seconds

3. Token Bucket:
   - Burst allowed, then throttled

4. Leaky Bucket:
   - Smooth rate limiting
```

### 4. Bulkheads

Isolate resources to prevent total failure.

**Pattern**:
```typescript
// Separate thread pools for different operations
class ResourceManager {
  private readonly criticalPool = new ThreadPool(50);  // Critical operations
  private readonly normalPool = new ThreadPool(200);   // Normal operations
  private readonly batchPool = new ThreadPool(100);    // Batch operations

  async executeCritical(task: Task) {
    return await this.criticalPool.execute(task);
  }

  async executeNormal(task: Task) {
    return await this.normalPool.execute(task);
  }

  async executeBatch(task: Task) {
    return await this.batchPool.execute(task);
  }
}
```

## Bottleneck Detection

### 1. Database N+1 Queries

**Detection**:
```sql
-- N+1 Problem
SELECT * FROM orders;  -- 1 query
-- For each order:
SELECT * FROM order_items WHERE order_id = ?;  -- N queries

-- Total: 1 + N queries
```

**Fix**:
```sql
-- Single query with JOIN
SELECT o.*, oi.*
FROM orders o
LEFT JOIN order_items oi ON oi.order_id = o.id;

-- Or use eager loading in ORM
const orders = await Order.findAll({
  include: [OrderItem]
});
```

### 2. Synchronous Cascade Calls

**Detection**:
```
Request → ServiceA → ServiceB → ServiceC → ServiceD
Total latency = A + B + C + D latencies
```

**Fix**:
```
Request → API Gateway → [ServiceA, ServiceB, ServiceC, ServiceD] (parallel)
Total latency = max(A, B, C, D)
```

### 3. Missing Indexes

**Detection**:
```sql
-- Analyze query plans
EXPLAIN SELECT * FROM orders WHERE customer_id = 123 AND status = 'pending';

-- Look for:
-- Seq Scan (bad - full table scan)
-- Index Scan (good - using index)
```

**Fix**:
```sql
-- Add composite index
CREATE INDEX idx_orders_customer_status
ON orders(customer_id, status);

-- Now query uses index
EXPLAIN SELECT * FROM orders WHERE customer_id = 123 AND status = 'pending';
-- Index Scan using idx_orders_customer_status
```

### 4. Inefficient Algorithms

**Detection**:
```typescript
// O(n²) complexity
function findDuplicates(items: Item[]): Item[] {
  const duplicates = [];
  for (let i = 0; i < items.length; i++) {
    for (let j = i + 1; j < items.length; j++) {
      if (items[i].id === items[j].id) {
        duplicates.push(items[i]);
      }
    }
  }
  return duplicates;
}
```

**Fix**:
```typescript
// O(n) complexity
function findDuplicates(items: Item[]): Item[] {
  const seen = new Set<string>();
  const duplicates = [];

  for (const item of items) {
    if (seen.has(item.id)) {
      duplicates.push(item);
    } else {
      seen.add(item.id);
    }
  }

  return duplicates;
}
```

### 5. Memory Leaks

**Detection**:
```
Monitor:
- Heap usage over time
- Event listener count
- Open file descriptors
- Database connections
```

**Common Causes**:
```typescript
// Memory leak: Event listeners not removed
class OrderProcessor {
  constructor(private eventBus: EventBus) {
    this.eventBus.on('order.created', this.handleOrder);
    // Problem: listener never removed
  }
}

// Fix: Remove listeners
class OrderProcessor {
  constructor(private eventBus: EventBus) {
    this.eventBus.on('order.created', this.handleOrder);
  }

  destroy() {
    this.eventBus.off('order.created', this.handleOrder);
  }
}
```

## Scalability Patterns

### 1. Database Sharding

**Horizontal partitioning of data**:
```
Users:
  Shard 1: users with ID 0-999999
  Shard 2: users with ID 1000000-1999999
  Shard 3: users with ID 2000000-2999999

Sharding Strategy:
  - Range-based (above)
  - Hash-based (hash(userId) % num_shards)
  - Geographic (US-East, US-West, EU)
```

### 2. Read Replicas

**Separate read and write databases**:
```
Write: Primary Database
Reads: Replica 1, Replica 2, Replica 3 (load balanced)

Benefits:
- Distribute read load
- Geographic distribution
- Backup/disaster recovery
```

### 3. CQRS (Command Query Responsibility Segregation)

**Separate models for reads and writes**:
```
Write Model: Optimized for consistency and business rules
Read Model: Optimized for queries and denormalized

Sync via events:
  Command → Write Model → Event → Read Model
```

### 4. Event Streaming

**Handle high-volume events**:
```
Producer → Kafka/Kinesis → Consumer Group 1 (parallel instances)
                         → Consumer Group 2 (parallel instances)
                         → Consumer Group 3 (parallel instances)

Benefits:
- High throughput
- Parallel processing
- Replay capability
- Decoupling
```

### 5. Async Processing

**Offload heavy work to background jobs**:
```
API Request → Queue Job → Return Response (immediate)

Background Worker Pool:
  Worker 1 → Process job
  Worker 2 → Process job
  Worker 3 → Process job

Benefits:
- Fast response times
- Resource isolation
- Retry capability
- Horizontal scaling of workers
```

## Monitoring and Metrics

### Key Scalability Metrics

```yaml
response_time:
  p50: < 100ms
  p95: < 500ms
  p99: < 1000ms

throughput:
  target: 10,000 requests/second
  current: 5,000 requests/second

error_rate:
  target: < 0.1%
  current: 0.05%

database:
  query_time_p95: < 100ms
  connection_pool_utilization: < 80%
  slow_queries: < 10/minute

cache:
  hit_rate: > 90%
  eviction_rate: < 5%

resource_usage:
  cpu: < 70%
  memory: < 80%
  disk_io: < 70%

horizontal_scaling:
  instances: 10
  auto_scaling: enabled
  scale_up_threshold: 70% CPU
  scale_down_threshold: 30% CPU
```

## Recommendations Output

```markdown
## Scalability Analysis Report

### Executive Summary
- System can currently handle 5,000 req/s
- Projected growth: 20,000 req/s in 6 months
- Critical bottlenecks identified: Database, API Gateway
- Estimated effort to scale: 8 weeks

### Bottlenecks Detected

1. **Database (Critical)**
   - Current: Single PostgreSQL instance
   - Bottleneck: Write capacity maxed at peak
   - Impact: Response time degradation (p99: 2.5s)
   - Recommendation: Implement read replicas, consider sharding
   - Effort: 3 weeks
   - Cost: +$500/month

2. **API Gateway (High)**
   - Current: 2 instances, CPU at 85%
   - Bottleneck: Insufficient horizontal scaling
   - Impact: Request queuing during peak
   - Recommendation: Auto-scaling from 2 to 10 instances
   - Effort: 1 week
   - Cost: +$200/month

3. **Caching (Medium)**
   - Current: No distributed cache
   - Bottleneck: Repeated database queries
   - Impact: Unnecessary database load
   - Recommendation: Implement Redis cluster
   - Effort: 2 weeks
   - Cost: +$150/month

### Scalability Roadmap

**Phase 1: Quick Wins (Weeks 1-2)**
- Implement Redis caching (30% query reduction)
- Add database indexes (50% query speed improvement)
- Enable CDN for static assets
- Configure auto-scaling for API Gateway

**Phase 2: Database Scaling (Weeks 3-5)**
- Setup read replicas (3 replicas)
- Implement connection pooling
- Optimize slow queries
- Consider query caching

**Phase 3: Architecture Evolution (Weeks 6-8)**
- Evaluate database sharding strategy
- Implement CQRS for high-read tables
- Setup event streaming for async processing
- Add circuit breakers and bulkheads

### Capacity Planning

Current capacity: 5,000 req/s
Target capacity: 20,000 req/s

With improvements:
- Phase 1: 8,000 req/s (+60%)
- Phase 2: 15,000 req/s (+200%)
- Phase 3: 25,000 req/s (+400%)

Cost analysis:
- Current: $1,000/month
- After improvements: $2,850/month
- Cost per 1,000 req/s: $114 (down from $200)
```

## Best Practices

1. **Design for Horizontal Scaling**: Assume you'll need to scale out
2. **Measure Everything**: Can't improve what you don't measure
3. **Load Test Regularly**: Find bottlenecks before users do
4. **Capacity Planning**: Plan for 3x current load
5. **Graceful Degradation**: System should degrade gracefully under load
6. **Cache Aggressively**: But invalidate correctly
7. **Async When Possible**: Offload heavy work
8. **Database Optimization**: Indexes, query optimization, connection pooling

Follow these guidelines to build systems that scale efficiently.
