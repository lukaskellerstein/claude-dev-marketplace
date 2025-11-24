# Performance Plugin for Claude Code

Comprehensive performance toolkit for monitoring, profiling, and optimizing applications. Covers frontend (React, bundle size, rendering), backend (API response times, database queries), memory profiling, CPU profiling, and load testing.

## Features

### Specialized Agents

- **Frontend Optimizer** - Expert in React performance, bundle size reduction, Core Web Vitals, and lazy loading
- **Backend Profiler** - Specialist in API optimization, database query tuning, N+1 query detection, and caching strategies
- **Memory & CPU Analyst** - Expert in memory leak detection, CPU profiling, garbage collection tuning, and resource optimization
- **Load Testing Specialist** - Specialist in load testing, stress testing, capacity planning, and performance benchmarking

### Commands

- **`/performance-audit`** - Comprehensive performance audit covering frontend, backend, database, and infrastructure
- **`/optimize-queries`** - Identify and optimize slow database queries, N+1 problems, and missing indexes
- **`/reduce-bundle`** - Analyze and reduce frontend bundle size through tree shaking and code splitting

### Auto-Invoked Skills

- **Prevent N+1 Queries** - Automatically suggests eager loading and batch loading when writing database queries
- **Optimize React Rendering** - Provides React performance best practices when writing components
- **Efficient Caching** - Guides proper caching strategies and invalidation patterns

## Installation

Add to your Claude Code configuration:

```bash
# Clone or install the performance-plugin
claude-code install performance-plugin
```

Or add to your `.claude-plugins` directory manually.

## Usage

### Full Performance Audit

```bash
/performance-audit
```

Conducts a comprehensive analysis of your entire application:
- Frontend performance (React, bundle size, Core Web Vitals)
- Backend performance (API response times, database queries)
- Memory and CPU profiling
- Load testing and capacity analysis
- Prioritized optimization recommendations

**Output includes**:
- Performance scores and metrics
- Identified bottlenecks with evidence
- Specific optimization recommendations
- Code examples ready to implement
- Expected performance improvements
- Implementation roadmap

### Database Query Optimization

```bash
/optimize-queries
```

Analyzes database queries and provides optimizations:
- Detects N+1 query problems
- Identifies missing indexes
- Analyzes slow queries with EXPLAIN
- Recommends connection pool configuration
- Designs caching strategies
- Provides before/after comparisons

**Example output**:
```
N+1 Query Problem Detected
Location: GET /api/users/:id/posts
Current: 51 queries (1200ms)
Optimized: 1 query (85ms)
Improvement: 93% faster

Solution:
const users = await User.findAll({
  include: [{ model: Post, as: 'posts' }]
});
```

### Bundle Size Reduction

```bash
/reduce-bundle
```

Analyzes and optimizes frontend bundle:
- Identifies large dependencies
- Finds tree-shaking opportunities
- Recommends dependency replacements
- Implements code splitting
- Sets up bundle size monitoring

**Example output**:
```
Bundle Analysis
Total: 2.5MB → 1.0MB (60% reduction)

Large Dependencies:
1. moment.js (288KB) → date-fns (14KB) = 274KB saved
2. lodash (531KB) → lodash-es (15KB) = 516KB saved
3. No code splitting → Route-based splitting = 1.2MB initial reduction

Expected: LCP 3.2s → 1.8s (44% faster)
```

## Auto-Invoked Skills

### Prevent N+1 Queries

Automatically activates when writing database queries to prevent N+1 problems.

**Detects patterns like**:
```javascript
// ❌ BAD: N+1 problem
const users = await User.findAll();
for (const user of users) {
  user.posts = await Post.findAll({ where: { userId: user.id } });
}

// ✅ GOOD: Eager loading suggested
const users = await User.findAll({
  include: [{ model: Post, as: 'posts' }]
});
```

### Optimize React Rendering

Automatically provides React performance guidance when writing components.

**Suggests optimizations like**:
```javascript
// ❌ BAD: Unnecessary re-renders
function List({ items, onClick }) {
  return items.map(item => (
    <Item key={item.id} item={item} onClick={() => onClick(item.id)} />
  ));
}

// ✅ GOOD: Memoization suggested
const Item = React.memo(({ item, onClick }) => {
  return <div onClick={() => onClick(item.id)}>{item.name}</div>;
});

function List({ items, onClick }) {
  const handleClick = useCallback((id) => onClick(id), [onClick]);

  return items.map(item => (
    <Item key={item.id} item={item} onClick={handleClick} />
  ));
}
```

### Efficient Caching

Guides proper caching implementation and invalidation.

**Provides patterns like**:
```javascript
// ✅ GOOD: Cache-aside pattern
async function getUser(userId) {
  const cacheKey = `user:${userId}`;

  const cached = await redis.get(cacheKey);
  if (cached) return JSON.parse(cached);

  const user = await User.findByPk(userId);
  await redis.setex(cacheKey, 3600, JSON.stringify(user));

  return user;
}
```

## Common Use Cases

### React Application Optimization

1. Run full audit: `/performance-audit`
2. Review frontend issues (bundle size, re-renders, Core Web Vitals)
3. Optimize bundle: `/reduce-bundle`
4. Apply React optimizations (auto-suggested by skills)
5. Re-test and measure improvements

### API Performance Issues

1. Run audit: `/performance-audit`
2. Identify slow endpoints and queries
3. Optimize queries: `/optimize-queries`
4. Implement caching (guided by skills)
5. Load test to verify improvements

### Pre-Launch Performance Check

1. Full audit: `/performance-audit`
2. Address critical issues (< 1 week)
3. Implement high-priority optimizations (2-3 weeks)
4. Load test with expected traffic
5. Setup monitoring and budgets

### Performance Regression Investigation

1. Run audit: `/performance-audit`
2. Compare with baseline metrics
3. Identify regressions
4. Apply targeted optimizations
5. Setup CI/CD performance checks

## Performance Metrics

### Frontend Metrics
- **LCP (Largest Contentful Paint)**: Target < 2.5s
- **FID/INP (First Input Delay/Interaction to Next Paint)**: Target < 100ms
- **CLS (Cumulative Layout Shift)**: Target < 0.1
- **Bundle Size**: Monitor trends, set budgets
- **JavaScript Execution Time**: Identify bottlenecks

### Backend Metrics
- **API Response Time**: p50, p95, p99
- **Database Query Time**: Monitor slow queries (>100ms)
- **Throughput**: Requests per second
- **Error Rate**: Target < 1%
- **Cache Hit Rate**: Target > 80%

### System Metrics
- **Memory Usage**: Monitor heap, detect leaks
- **CPU Usage**: Identify hot paths
- **GC Pause Time**: Tune garbage collection
- **Connection Pool Utilization**: Prevent exhaustion

## Best Practices

### Performance Culture
- Measure before optimizing
- Set performance budgets
- Monitor continuously
- Enforce in CI/CD
- Regular performance reviews

### Optimization Priority
1. Fix critical issues first (security, crashes)
2. Optimize high-impact, low-effort items
3. Address user-facing performance
4. Optimize for scale
5. Fine-tune for efficiency

### Testing
- Establish baselines
- Test with realistic data
- Use production-like environment
- Load test before launch
- Monitor in production

## Integration

### CI/CD Performance Checks

```yaml
# .github/workflows/performance.yml
- name: Run performance audit
  run: |
    claude-code /performance-audit

- name: Check bundle size
  run: |
    npm run build
    npm run check-bundle-size

- name: Run load tests
  run: |
    k6 run tests/load-test.js
```

### Monitoring Setup

The plugin can help set up:
- Application Performance Monitoring (APM)
- Real User Monitoring (RUM)
- Synthetic monitoring
- Performance dashboards
- Alert thresholds

## Requirements

### Frontend Optimization
- Node.js 16+
- React (for React-specific optimizations)
- Webpack or Vite bundle analyzer

### Backend Optimization
- Node.js, Python, Java, or Go
- Database (PostgreSQL, MySQL, MongoDB)
- Redis (for caching recommendations)

### Load Testing
- k6, Artillery, or JMeter
- Sufficient load generation capacity

## Examples

### Example 1: E-commerce Site

**Problem**: Slow product listing page

```bash
/performance-audit
```

**Findings**:
- N+1 query loading product images (40 queries)
- Large bundle size (3MB)
- Missing database indexes

**Solutions Applied**:
- Eager loading: 40 queries → 2 queries (95% faster)
- Bundle optimization: 3MB → 1.2MB (60% reduction)
- Added indexes: query time 800ms → 45ms

**Result**: Page load 5.2s → 1.8s (65% improvement)

### Example 2: Dashboard Application

**Problem**: Slow rendering with large datasets

**Findings**:
- Rendering 5,000 rows without virtualization
- Excessive React re-renders
- No memoization

**Solutions Applied**:
- Virtual scrolling with react-window
- React.memo and useMemo optimizations
- Debounced search input

**Result**: Initial render 8s → 0.3s (96% improvement)

### Example 3: API Service

**Problem**: High latency under load

**Findings**:
- No caching layer
- Inefficient database queries
- Connection pool exhaustion

**Solutions Applied**:
- Redis caching (85% hit rate)
- Query optimization and indexing
- Connection pool tuning

**Result**: p95 latency 2800ms → 180ms (93% improvement)

## Support

For issues, questions, or contributions:
- GitHub Issues: [Report an issue]
- Documentation: [Full docs]
- Examples: See `examples/` directory

## License

MIT License - See LICENSE file for details

## Credits

Created for the Claude Code ecosystem to help developers build high-performance applications.

---

**Start optimizing**: Run `/performance-audit` to get started with a comprehensive performance analysis of your application.
