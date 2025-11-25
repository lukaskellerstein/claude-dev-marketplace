---
description: Conduct comprehensive performance audit covering frontend, backend, database, and infrastructure
---

Run a comprehensive performance audit to identify bottlenecks and optimization opportunities across the entire application stack.

## Process

Follow these steps:

1. **Identify Stack Components**: Detect application architecture
   - Frontend framework (React, Vue, Angular)
   - Backend framework (Express, FastAPI, Spring)
   - Database (PostgreSQL, MongoDB, MySQL)
   - Infrastructure (Docker, Kubernetes, serverless)
   - Caching layer (Redis, Memcached)
   - Message queues (RabbitMQ, Kafka, NATS)

2. **Frontend Performance Analysis**: Launch `performance-plugin:frontend-optimizer` agent to:
   - Analyze React component rendering performance
   - Check bundle size and identify large dependencies
   - Evaluate Core Web Vitals (LCP, FID/INP, CLS)
   - Review lazy loading and code splitting
   - Check image optimization
   - Analyze network waterfall
   - Identify JavaScript execution bottlenecks
   - Check for memory leaks in frontend code

3. **Backend Performance Analysis**: Launch `performance-plugin:backend-profiler` agent to:
   - Measure API response times
   - Detect N+1 query problems
   - Analyze database query performance
   - Review caching effectiveness
   - Check connection pooling configuration
   - Evaluate API payload sizes
   - Analyze request/response compression
   - Review rate limiting and throttling

4. **Memory & CPU Analysis**: Launch `performance-plugin:memory-cpu-analyst` agent to:
   - Profile memory usage and detect leaks
   - Analyze CPU hot paths
   - Review garbage collection behavior
   - Check for resource leaks (connections, file descriptors)
   - Analyze event loop health (Node.js)
   - Profile heap allocations
   - Check thread pool configuration

5. **Load Testing**: Launch `performance-plugin:load-testing-specialist` agent to:
   - Run baseline load tests
   - Identify capacity limits
   - Test auto-scaling behavior
   - Measure throughput and latency under load
   - Identify bottlenecks at scale
   - Calculate required resources for target load

6. **Prioritization & Recommendations**: Aggregate findings
   - Categorize issues by severity and impact
   - Prioritize optimizations by ROI
   - Create implementation roadmap
   - Estimate performance improvements
   - Provide code examples and configurations

## Output

Present a comprehensive performance audit report:

### Executive Summary
```
Performance Audit Summary
========================

Overall Performance Score: 72/100

Critical Issues: 5
High Priority: 12
Medium Priority: 23
Low Priority: 15

Estimated Improvement Potential:
- Response Time: 45% reduction (800ms → 440ms)
- Bundle Size: 60% reduction (2.5MB → 1MB)
- Database Queries: 75% reduction (40 queries → 10 queries)
- Memory Usage: 30% reduction (512MB → 358MB)
- Capacity: 200% increase (500 RPS → 1500 RPS)
```

### Frontend Performance

#### Core Web Vitals
```
Current Scores:
- LCP: 3.2s (Poor) ❌ Target: < 2.5s
- FID: 180ms (Poor) ❌ Target: < 100ms
- CLS: 0.15 (Needs Improvement) ⚠️ Target: < 0.1
- FCP: 2.1s (Needs Improvement) ⚠️ Target: < 1.8s
- TTFB: 650ms (Poor) ❌ Target: < 600ms

Lighthouse Score: 65/100
```

#### Critical Issues

**1. Large Bundle Size (2.5MB uncompressed)**
- **Impact**: Slow initial page load, high LCP
- **Root Cause**:
  - Moment.js (70KB) imported but only date formatting used
  - Lodash (70KB) entire library imported
  - Unused dependencies in bundle
- **Solution**:
  ```javascript
  // Replace moment.js with date-fns
  npm uninstall moment
  npm install date-fns

  // Use tree-shakeable lodash-es
  npm uninstall lodash
  npm install lodash-es

  // Import only what you need
  import { format } from 'date-fns';
  import { debounce } from 'lodash-es';
  ```
- **Expected Impact**: Bundle size reduced by 60% (2.5MB → 1MB)

**2. Excessive React Re-renders**
- **Location**: `Dashboard.js`, `ProductList.js`
- **Impact**: Slow interactions, high FID
- **Issue**: Missing memoization, component re-renders on every state change
- **Solution**:
  ```javascript
  // Dashboard.js
  const Dashboard = React.memo(({ data }) => {
    const filteredData = useMemo(() => {
      return data.filter(item => item.active);
    }, [data]);

    const handleClick = useCallback((id) => {
      // Handler logic
    }, []);

    return <ProductList items={filteredData} onClick={handleClick} />;
  });
  ```
- **Expected Impact**: 70% fewer re-renders, FID improved to < 100ms

**3. Images Not Optimized**
- **Issue**: Large PNG images (500KB-2MB each), no lazy loading
- **Impact**: Slow LCP, unnecessary bandwidth usage
- **Solution**:
  ```javascript
  // Convert to WebP format
  npm install sharp

  // Add lazy loading
  <img src="image.webp" loading="lazy" alt="Product" />

  // Use responsive images
  <img
    srcSet="image-320w.webp 320w, image-640w.webp 640w"
    sizes="(max-width: 640px) 100vw, 640px"
    src="image-640w.webp"
    loading="lazy"
    alt="Product"
  />
  ```
- **Expected Impact**: 80% image size reduction, LCP < 2.5s

### Backend Performance

#### API Response Times
```
Current Performance:
- p50: 450ms
- p95: 1200ms ❌ Target: < 500ms
- p99: 2800ms ❌ Target: < 1000ms
- Throughput: 450 RPS (at 70% CPU)
```

#### Critical Issues

**1. N+1 Query Problem in /api/users**
- **Impact**: 40 database queries per request, p95 response time 1200ms
- **Issue**:
  ```javascript
  // BAD: N+1 queries
  const users = await User.findAll(); // 1 query
  for (const user of users) {
    user.posts = await Post.findAll({ where: { userId: user.id } }); // N queries
  }
  ```
- **Solution**:
  ```javascript
  // GOOD: Single query with join
  const users = await User.findAll({
    include: [{ model: Post }]
  });
  ```
- **Expected Impact**: 40 queries → 1 query, p95 < 300ms

**2. Missing Indexes**
- **Issue**: Full table scans on users.email and posts.user_id
- **Evidence**: EXPLAIN ANALYZE shows Seq Scan (cost=0.00..10251.00)
- **Solution**:
  ```sql
  CREATE INDEX idx_users_email ON users(email);
  CREATE INDEX idx_posts_user_id ON posts(user_id);
  CREATE INDEX idx_posts_created_at ON posts(created_at DESC);
  ```
- **Expected Impact**: Query time 800ms → 15ms

**3. No Caching**
- **Issue**: Same data fetched repeatedly from database
- **Cache Hit Potential**: 85% of requests fetch same data
- **Solution**:
  ```javascript
  const redis = new Redis();

  async function getUser(userId) {
    const cacheKey = `user:${userId}`;
    const cached = await redis.get(cacheKey);

    if (cached) return JSON.parse(cached);

    const user = await User.findByPk(userId);
    await redis.setex(cacheKey, 3600, JSON.stringify(user));

    return user;
  }
  ```
- **Expected Impact**: 85% faster response times for cached requests

### Memory & CPU Performance

#### Current Resource Usage
```
Memory:
- Heap Used: 480MB / 512MB (94% utilized) ⚠️
- RSS: 620MB
- External: 45MB
- Heap growth: +15MB/hour (memory leak detected) ❌

CPU:
- Average: 55%
- Peak: 92%
- Hot path: JSON serialization (35% of CPU time)
```

#### Critical Issues

**1. Memory Leak in Event Listeners**
- **Location**: `WebSocket connection handler`
- **Issue**: Event listeners not removed on disconnect
- **Evidence**: Heap growth +15MB/hour, 2000+ orphaned listeners
- **Solution**:
  ```javascript
  // Add cleanup
  socket.on('disconnect', () => {
    socket.removeAllListeners();
    clearInterval(heartbeatInterval);
  });
  ```
- **Expected Impact**: Eliminate memory leak

**2. Inefficient JSON Serialization**
- **Issue**: Large objects serialized repeatedly (35% of CPU)
- **Solution**:
  ```javascript
  // Cache serialized responses
  const cache = new LRU({ max: 500 });

  function serializeResponse(data) {
    const key = hash(data);
    if (cache.has(key)) return cache.get(key);

    const serialized = JSON.stringify(data);
    cache.set(key, serialized);
    return serialized;
  }
  ```
- **Expected Impact**: 60% reduction in JSON serialization time

### Database Performance

#### Query Performance
```
Slow Queries (> 100ms):
1. SELECT * FROM posts JOIN users - 850ms (N+1 problem)
2. SELECT * FROM products WHERE category - 320ms (missing index)
3. SELECT COUNT(*) FROM orders - 180ms (full table scan)

Total Queries per Request: 40 ❌ Target: < 5
```

#### Optimization Opportunities

**1. Add Missing Indexes**
```sql
-- High impact indexes
CREATE INDEX idx_products_category ON products(category);
CREATE INDEX idx_orders_user_status ON orders(user_id, status);
CREATE INDEX idx_orders_created_at ON orders(created_at DESC);
```

**2. Implement Connection Pooling**
```javascript
const pool = new Pool({
  max: 20,
  min: 5,
  idleTimeoutMillis: 30000,
});
```

**3. Use Read Replicas**
```javascript
// Route read queries to replicas
const readPool = new Pool({ host: 'replica.db.local' });
const writePool = new Pool({ host: 'primary.db.local' });
```

### Load Testing Results

#### Capacity Analysis
```
Current Capacity:
- Maximum Throughput: 450 RPS
- Breaking Point: 500 RPS (CPU 100%, response time > 5s)
- Concurrent Users: 1000 max

Target Capacity:
- Required Throughput: 2000 RPS
- Target Concurrent Users: 5000

Gap: 4x capacity increase needed
```

#### Recommendations
1. **Optimize Application** (Expected: 2x capacity)
   - Fix N+1 queries
   - Add caching
   - Optimize bundle size

2. **Horizontal Scaling** (Expected: 2x capacity)
   - Add 3 more application servers
   - Configure load balancer
   - Setup auto-scaling (min: 3, max: 10)

3. **Database Optimization** (Expected: 3x capacity)
   - Add indexes
   - Setup read replicas
   - Implement connection pooling

**Total Expected Capacity**: 450 RPS → 2700 RPS (6x increase)

### Implementation Roadmap

#### Week 1: Quick Wins (High Impact, Low Effort)
- [ ] Add database indexes (2 hours)
- [ ] Fix N+1 queries (4 hours)
- [ ] Implement Redis caching (6 hours)
- [ ] Optimize bundle size (4 hours)
- [ ] Add React memoization (4 hours)

**Expected Impact**: 2x performance improvement

#### Week 2-3: Major Optimizations
- [ ] Image optimization pipeline (8 hours)
- [ ] Implement lazy loading (4 hours)
- [ ] Setup read replicas (6 hours)
- [ ] Fix memory leak (6 hours)
- [ ] Optimize JSON serialization (4 hours)
- [ ] Implement connection pooling (4 hours)

**Expected Impact**: 4x performance improvement

#### Week 4: Infrastructure & Monitoring
- [ ] Setup horizontal scaling (8 hours)
- [ ] Configure auto-scaling (4 hours)
- [ ] Implement performance monitoring (6 hours)
- [ ] Setup performance budgets in CI/CD (4 hours)
- [ ] Load testing automation (6 hours)

**Expected Impact**: 6x performance improvement + ongoing monitoring

### Cost Analysis

**Current Infrastructure**:
- 2 application servers: $200/month
- 1 database server: $150/month
- Total: $350/month

**Optimized Infrastructure** (after optimizations):
- 3 application servers: $300/month (2x capacity per server = 6x total)
- 1 primary + 2 read replicas: $300/month
- Redis cache: $50/month
- Load balancer: $50/month
- Total: $700/month

**Cost per Request**:
- Current: $0.026 per 1000 requests
- Optimized: $0.009 per 1000 requests (66% reduction)

## Best Practices Applied

- **Measure First**: Establish baseline before optimization
- **Focus on Impact**: Prioritize high-impact, low-effort improvements
- **Incremental Changes**: Optimize incrementally and measure results
- **Real-World Testing**: Load test with realistic traffic patterns
- **Continuous Monitoring**: Setup monitoring to catch regressions
- **Performance Budgets**: Enforce performance budgets in CI/CD
- **Capacity Planning**: Plan for future growth

## Examples

### Full Application Audit
```
/performance-audit

Analyze entire application stack including frontend, backend,
database, and infrastructure. Provide comprehensive report with
prioritized recommendations.
```

### Frontend-Only Audit
```
/performance-audit

Focus on frontend performance including React rendering,
bundle size, Core Web Vitals, and image optimization.
```

### Backend-Only Audit
```
/performance-audit

Focus on API performance, database queries, caching,
and resource utilization.
```

### Pre-Launch Audit
```
/performance-audit

Comprehensive pre-launch performance audit with load testing
and capacity planning for expected production traffic.
```

## Integration with Other Commands

- Start with `/performance-audit` for comprehensive analysis
- Use `/optimize-queries` for database-specific optimization
- Use `/reduce-bundle` for frontend bundle optimization
- Follow with load testing to validate improvements
- Setup continuous monitoring to prevent regressions

Provide actionable, prioritized performance recommendations with clear implementation steps, code examples, and expected impact metrics.
