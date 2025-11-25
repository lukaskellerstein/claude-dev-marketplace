---
description: Identify and optimize slow database queries, N+1 problems, missing indexes, and query inefficiencies
---

Analyze and optimize database queries to improve response times, reduce database load, and eliminate common query performance issues.

## Process

Follow these steps:

1. **Database Detection**: Identify database system and ORM
   - PostgreSQL, MySQL, MongoDB, etc.
   - Sequelize, TypeORM, Mongoose, Prisma, etc.
   - Query patterns and conventions
   - Existing indexes and constraints

2. **Launch Backend Profiler**: Use `performance-plugin:backend-profiler` agent to:
   - Identify slow queries (> 100ms)
   - Detect N+1 query problems
   - Analyze query execution plans (EXPLAIN)
   - Check index usage
   - Evaluate connection pool configuration
   - Measure query frequency and impact
   - Identify missing indexes
   - Check for full table scans

3. **Query Pattern Analysis**: Examine common patterns
   - Eager loading vs lazy loading
   - JOIN strategies
   - Subquery optimization
   - Pagination methods
   - Aggregation queries
   - Full-text search
   - Cascading queries

4. **Index Optimization**: Analyze index strategy
   - Missing indexes on frequently queried columns
   - Composite index opportunities
   - Index usage statistics
   - Redundant or unused indexes
   - Covering indexes
   - Partial indexes

5. **Query Rewriting**: Optimize problematic queries
   - Eliminate N+1 queries with eager loading
   - Replace subqueries with JOINs where appropriate
   - Optimize WHERE clauses
   - Reduce data fetched (SELECT specific columns)
   - Implement cursor-based pagination
   - Batch operations

6. **Caching Strategy**: Implement query result caching
   - Identify cacheable queries
   - Design cache invalidation strategy
   - Implement Redis caching layer
   - Add database query cache
   - Monitor cache hit rates

## Output

Present a detailed query optimization report:

### Query Performance Summary
```
Database Query Analysis
=======================

Total Queries Analyzed: 156
Slow Queries (>100ms): 23
N+1 Problems Detected: 7
Missing Indexes: 12
Optimization Opportunities: 45

Expected Improvements:
- Average Query Time: 85% reduction (380ms → 57ms)
- Total Queries per Request: 75% reduction (40 → 10)
- Database Load: 60% reduction
- Cache Hit Rate: 0% → 85% (with Redis)
```

### Critical Issues

#### 1. N+1 Query Problem in User Posts Endpoint

**Location**: `GET /api/users/:id/posts`

**Current Implementation** (BAD):
```javascript
// routes/users.js
app.get('/api/users/:id/posts', async (req, res) => {
  const user = await User.findByPk(req.params.id); // 1 query

  const posts = [];
  for (const postId of user.postIds) {
    const post = await Post.findByPk(postId); // N queries
    posts.push(post);
  }

  res.json({ user, posts });
});
```

**Performance Impact**:
- Queries: 1 + N (where N = number of posts)
- Example: User with 50 posts = 51 queries
- Total time: 1200ms
- Database load: 51 connections

**EXPLAIN Analysis**:
```sql
EXPLAIN ANALYZE SELECT * FROM posts WHERE id = $1;

Seq Scan on posts (cost=0.00..10251.00 rows=1 width=240)
  Filter: (id = 123)
  Planning Time: 0.156 ms
  Execution Time: 45.234 ms
```

**Optimized Implementation** (GOOD):
```javascript
// Solution 1: Eager Loading
app.get('/api/users/:id/posts', async (req, res) => {
  const user = await User.findByPk(req.params.id, {
    include: [{
      model: Post,
      as: 'posts',
    }],
  });

  res.json(user);
});

// Solution 2: Batch Loading with DataLoader
const DataLoader = require('dataloader');

const postLoader = new DataLoader(async (postIds) => {
  const posts = await Post.findAll({
    where: { id: { [Op.in]: postIds } },
  });

  const postMap = posts.reduce((map, post) => {
    map[post.id] = post;
    return map;
  }, {});

  return postIds.map(id => postMap[id]);
});

app.get('/api/users/:id/posts', async (req, res) => {
  const user = await User.findByPk(req.params.id);
  const posts = await postLoader.loadMany(user.postIds);

  res.json({ user, posts });
});
```

**Results After Optimization**:
- Queries: 1 or 2 (depending on solution)
- Total time: 85ms (93% improvement)
- Database load: 2 connections (96% reduction)

---

#### 2. Missing Index on Email Lookup

**Query**:
```sql
SELECT * FROM users WHERE email = 'user@example.com';
```

**Current Performance**:
- Execution time: 850ms
- Full table scan on 500,000 rows

**EXPLAIN Analysis**:
```sql
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'user@example.com';

Seq Scan on users (cost=0.00..10251.00 rows=1 width=240)
  Filter: (email = 'user@example.com'::text)
  Rows Removed by Filter: 499999
  Planning Time: 0.156 ms
  Execution Time: 846.234 ms
```

**Solution**: Add index
```sql
CREATE INDEX idx_users_email ON users(email);
```

**Results After Optimization**:
```sql
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'user@example.com';

Index Scan using idx_users_email on users (cost=0.42..8.44 rows=1 width=240)
  Index Cond: (email = 'user@example.com'::text)
  Planning Time: 0.082 ms
  Execution Time: 0.045 ms
```

- Execution time: 850ms → 0.045ms (99.99% improvement)
- Scan type: Seq Scan → Index Scan

---

#### 3. Inefficient Pagination

**Current Implementation** (OFFSET-based):
```javascript
// BAD: Gets slower as page number increases
app.get('/api/posts', async (req, res) => {
  const page = parseInt(req.query.page) || 1;
  const limit = 20;
  const offset = (page - 1) * limit;

  const posts = await Post.findAll({
    limit,
    offset,
    order: [['createdAt', 'DESC']],
  });

  res.json({ posts, page });
});
```

**Performance**:
- Page 1: 45ms
- Page 100: 850ms
- Page 1000: 8500ms (gets progressively slower)

**Why It's Slow**:
```sql
-- Database must skip all previous rows
SELECT * FROM posts
ORDER BY created_at DESC
LIMIT 20 OFFSET 20000; -- Must scan through 20,000 rows to skip them
```

**Optimized Implementation** (Cursor-based):
```javascript
// GOOD: Constant performance regardless of page depth
app.get('/api/posts', async (req, res) => {
  const limit = 20;
  const cursor = req.query.cursor; // Timestamp of last item

  const posts = await Post.findAll({
    where: cursor ? {
      createdAt: { [Op.lt]: cursor },
    } : {},
    limit,
    order: [['createdAt', 'DESC']],
  });

  const nextCursor = posts.length > 0
    ? posts[posts.length - 1].createdAt
    : null;

  res.json({
    posts,
    nextCursor,
    hasMore: posts.length === limit,
  });
});
```

**Results**:
- Page 1: 45ms
- Page 100: 48ms (constant performance)
- Page 1000: 46ms (constant performance)

**Index Required**:
```sql
CREATE INDEX idx_posts_created_at ON posts(created_at DESC);
```

---

#### 4. Selecting Unnecessary Columns

**Current Query**:
```javascript
// BAD: Fetches all columns including large TEXT fields
const users = await User.findAll({
  attributes: ['*'], // Fetches everything
});
```

**Issues**:
- Fetches large TEXT/BLOB columns (bio, description)
- Increases network transfer
- Increases memory usage
- Slower serialization

**Optimized Query**:
```javascript
// GOOD: Fetch only needed columns
const users = await User.findAll({
  attributes: ['id', 'name', 'email', 'avatar'],
});

// Even better: Different attributes for different use cases
const usersList = await User.findAll({
  attributes: ['id', 'name', 'avatar'], // List view
});

const userDetail = await User.findByPk(id, {
  attributes: ['id', 'name', 'email', 'bio', 'avatar'], // Detail view
});
```

**Results**:
- Data transferred: 5MB → 500KB (90% reduction)
- Query time: 450ms → 85ms (81% improvement)
- Memory usage: 50MB → 8MB (84% reduction)

---

#### 5. Inefficient COUNT Queries

**Current Implementation**:
```javascript
// BAD: Counts all rows (slow for large tables)
const count = await Post.count();
const hasAnyPosts = count > 0;
```

**Performance**: 1200ms for table with 1M rows

**Optimized Implementation**:
```javascript
// GOOD: Use EXISTS for existence check
const hasAnyPosts = await Post.findOne({
  attributes: ['id'],
  limit: 1,
}) !== null;

// Or with raw SQL
const result = await sequelize.query(
  'SELECT EXISTS(SELECT 1 FROM posts LIMIT 1)',
  { type: QueryTypes.SELECT }
);
const hasAnyPosts = result[0].exists;
```

**Results**:
- Query time: 1200ms → 2ms (99.8% improvement)

---

### Recommended Indexes

#### High Priority Indexes (Immediate Impact)
```sql
-- User lookups (saves 850ms per query)
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);

-- Post queries (saves 650ms per query)
CREATE INDEX idx_posts_user_id ON posts(user_id);
CREATE INDEX idx_posts_created_at ON posts(created_at DESC);
CREATE INDEX idx_posts_status ON posts(status);

-- Order queries (saves 420ms per query)
CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_orders_created_at ON orders(created_at DESC);

-- Composite indexes for common query patterns
CREATE INDEX idx_orders_user_status ON orders(user_id, status);
CREATE INDEX idx_posts_user_created ON posts(user_id, created_at DESC);
```

#### Partial Indexes (Reduce index size)
```sql
-- Only index active users
CREATE INDEX idx_active_users_email ON users(email) WHERE active = true;

-- Only index published posts
CREATE INDEX idx_published_posts ON posts(created_at DESC) WHERE status = 'published';
```

#### Covering Indexes (Avoid table lookup)
```sql
-- Cover common query (SELECT id, name FROM users WHERE email = ?)
CREATE INDEX idx_users_email_covering ON users(email) INCLUDE (id, name);
```

---

### Connection Pool Optimization

**Current Configuration**:
```javascript
const pool = new Pool({
  max: 10,  // Too small for current load
  min: 2,
});
```

**Issues**:
- Connection pool exhaustion under load
- Queries waiting for available connections
- 95th percentile latency: 2800ms

**Optimized Configuration**:
```javascript
const pool = new Pool({
  max: 20,                    // Increase max connections
  min: 5,                     // Increase min connections
  idleTimeoutMillis: 30000,   // Close idle connections after 30s
  connectionTimeoutMillis: 2000, // Timeout if can't get connection
  maxUses: 7500,              // Close connections after 7500 uses (prevent leaks)
});

// Monitor pool
pool.on('connect', () => {
  console.log('Database connection established');
});

pool.on('acquire', () => {
  console.log('Connection acquired from pool');
});

pool.on('error', (err) => {
  console.error('Database pool error:', err);
});

// Health check
setInterval(async () => {
  const { totalCount, idleCount, waitingCount } = pool;
  console.log('Pool stats:', {
    total: totalCount,
    idle: idleCount,
    waiting: waitingCount,
    utilization: ((totalCount - idleCount) / totalCount * 100).toFixed(2) + '%',
  });

  if (waitingCount > 5) {
    console.warn('High connection pool contention!');
  }
}, 60000);
```

**Results**:
- Connection wait time: 450ms → 5ms
- 95th percentile latency: 2800ms → 420ms
- Connection pool exhaustion: Eliminated

---

### Caching Strategy

**Implement Redis Caching**:
```javascript
const Redis = require('ioredis');
const redis = new Redis();

// Cache frequently accessed data
async function getUser(userId) {
  const cacheKey = `user:${userId}`;

  // Try cache first
  const cached = await redis.get(cacheKey);
  if (cached) {
    return JSON.parse(cached);
  }

  // Fetch from database
  const user = await User.findByPk(userId, {
    attributes: ['id', 'name', 'email', 'avatar'],
  });

  // Cache for 1 hour
  await redis.setex(cacheKey, 3600, JSON.stringify(user));

  return user;
}

// Invalidate cache on updates
async function updateUser(userId, data) {
  const user = await User.update(data, { where: { id: userId } });

  // Invalidate cache
  await redis.del(`user:${userId}`);

  return user;
}

// Cache query results
async function getPopularPosts() {
  const cacheKey = 'posts:popular';

  const cached = await redis.get(cacheKey);
  if (cached) {
    return JSON.parse(cached);
  }

  const posts = await Post.findAll({
    where: { status: 'published' },
    order: [['views', 'DESC']],
    limit: 10,
    attributes: ['id', 'title', 'views', 'createdAt'],
  });

  // Cache for 5 minutes
  await redis.setex(cacheKey, 300, JSON.stringify(posts));

  return posts;
}
```

**Cache Performance**:
- Cache Hit Rate: 85%
- Cached Query Time: 3ms (vs 380ms from DB)
- Database Load: 60% reduction
- Response Time: 85% improvement for cached requests

---

### Query Monitoring Setup

**Implement Query Logging**:
```javascript
// Log slow queries
const sequelize = new Sequelize('database', 'username', 'password', {
  logging: (sql, timing) => {
    if (timing > 100) { // Log queries > 100ms
      console.warn(`Slow query (${timing}ms):`, sql);
    }
  },
  benchmark: true,
});

// Track query metrics
const queryMetrics = {
  total: 0,
  slow: 0,
  totalTime: 0,
};

sequelize.addHook('beforeQuery', (options) => {
  options.startTime = Date.now();
});

sequelize.addHook('afterQuery', (options, result) => {
  const duration = Date.now() - options.startTime;

  queryMetrics.total++;
  queryMetrics.totalTime += duration;

  if (duration > 100) {
    queryMetrics.slow++;
  }
});

// Report metrics every minute
setInterval(() => {
  console.log('Query metrics:', {
    total: queryMetrics.total,
    slow: queryMetrics.slow,
    slowPercentage: (queryMetrics.slow / queryMetrics.total * 100).toFixed(2) + '%',
    avgDuration: (queryMetrics.totalTime / queryMetrics.total).toFixed(2) + 'ms',
  });

  // Reset
  queryMetrics.total = 0;
  queryMetrics.slow = 0;
  queryMetrics.totalTime = 0;
}, 60000);
```

---

### Implementation Checklist

#### Immediate Actions (Week 1)
- [ ] Add critical indexes (users.email, posts.user_id, orders.user_id)
- [ ] Fix top 5 N+1 query problems
- [ ] Optimize connection pool configuration
- [ ] Implement cursor-based pagination
- [ ] Add query performance logging

**Expected Impact**: 70% query performance improvement

#### Short-term (Week 2-3)
- [ ] Implement Redis caching for read-heavy endpoints
- [ ] Add composite indexes for common query patterns
- [ ] Optimize SELECT statements (remove SELECT *)
- [ ] Implement batch loading with DataLoader
- [ ] Setup query monitoring dashboard

**Expected Impact**: 85% query performance improvement

#### Long-term (Month 2)
- [ ] Setup read replicas for read scaling
- [ ] Implement database query result caching
- [ ] Add partial indexes for filtered queries
- [ ] Setup automated index recommendations
- [ ] Implement query performance regression tests

**Expected Impact**: 95% query performance improvement + scalability

---

### Performance Improvements Summary

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Average Query Time | 380ms | 57ms | 85% faster |
| Queries per Request | 40 | 10 | 75% reduction |
| Slow Queries (>100ms) | 23 | 2 | 91% reduction |
| Database CPU | 85% | 35% | 59% reduction |
| API Response Time (p95) | 1200ms | 180ms | 85% faster |
| Throughput | 450 RPS | 1800 RPS | 4x increase |

---

## Best Practices Applied

- **Index Strategy**: Add indexes for frequently queried columns
- **Eager Loading**: Eliminate N+1 queries with proper joins
- **Pagination**: Use cursor-based pagination for large datasets
- **Column Selection**: Fetch only needed columns (avoid SELECT *)
- **Connection Pooling**: Configure pool size appropriately
- **Caching**: Cache frequently accessed data
- **Monitoring**: Log and monitor slow queries
- **Query Analysis**: Use EXPLAIN to understand query execution

## Examples

### Full Query Optimization
```
/optimize-queries

Analyze all database queries, identify N+1 problems,
add missing indexes, and implement caching strategy.
```

### N+1 Query Detection
```
/optimize-queries

Focus on detecting and fixing N+1 query problems
across the entire application.
```

### Index Recommendations
```
/optimize-queries

Analyze query patterns and recommend indexes
to improve database performance.
```

### Caching Strategy
```
/optimize-queries

Design and implement Redis caching strategy
for frequently accessed data.
```

## Integration with Other Commands

- Use as follow-up to `/performance-audit`
- Precedes load testing to verify improvements
- Integrates with monitoring setup
- Part of performance optimization roadmap

Provide specific, actionable query optimizations with before/after comparisons, EXPLAIN analysis, and measurable performance improvements.
