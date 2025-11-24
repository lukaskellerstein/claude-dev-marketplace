---
name: efficient-caching
description: Auto-invoked when implementing caching to ensure proper cache strategies, invalidation, and optimal performance
allowed-tools: Read, Grep, Glob
---

# Efficient Caching Strategies

This skill provides guidance on implementing effective caching strategies to improve application performance while maintaining data consistency.

## When Active

This skill activates when you:
- Implement caching with Redis, Memcached, or in-memory caches
- Add HTTP caching headers
- Configure CDN caching
- Cache database query results
- Implement application-level caching
- Work with service workers and browser caching
- Design cache invalidation strategies

## Caching Strategies

### 1. Cache-Aside (Lazy Loading)

**Pattern**: Application checks cache first, loads from source if miss, then updates cache

```javascript
// ✅ GOOD: Cache-aside pattern
async function getUser(userId) {
  const cacheKey = `user:${userId}`;

  // Try cache first
  const cached = await redis.get(cacheKey);
  if (cached) {
    return JSON.parse(cached);
  }

  // Cache miss: fetch from database
  const user = await User.findByPk(userId);

  if (user) {
    // Update cache with TTL
    await redis.setex(cacheKey, 3600, JSON.stringify(user));
  }

  return user;
}

// Invalidate cache on update
async function updateUser(userId, data) {
  const user = await User.update(data, { where: { id: userId } });

  // Invalidate cache
  await redis.del(`user:${userId}`);

  return user;
}
```

**Best for**: Read-heavy workloads, data that doesn't change frequently

### 2. Write-Through

**Pattern**: Write to cache and database simultaneously

```javascript
// ✅ GOOD: Write-through pattern
async function updateUser(userId, data) {
  const cacheKey = `user:${userId}`;

  // Update database
  const user = await User.update(data, { where: { id: userId } });

  // Update cache immediately
  await redis.setex(cacheKey, 3600, JSON.stringify(user));

  return user;
}

async function getUser(userId) {
  const cacheKey = `user:${userId}`;

  const cached = await redis.get(cacheKey);
  if (cached) {
    return JSON.parse(cached);
  }

  // If not in cache, load and cache
  const user = await User.findByPk(userId);
  if (user) {
    await redis.setex(cacheKey, 3600, JSON.stringify(user));
  }

  return user;
}
```

**Best for**: Read-heavy with occasional writes, data consistency critical

### 3. Write-Behind (Write-Back)

**Pattern**: Write to cache immediately, persist to database asynchronously

```javascript
// ✅ GOOD: Write-behind pattern (use with caution)
const writeQueue = new Queue('database-writes');

async function updateUser(userId, data) {
  const cacheKey = `user:${userId}`;

  // Update cache immediately (fast)
  await redis.setex(cacheKey, 3600, JSON.stringify(data));

  // Queue database update (async)
  await writeQueue.add({
    operation: 'update',
    table: 'users',
    id: userId,
    data,
  });

  return data;
}

// Worker processes queue
writeQueue.process(async (job) => {
  const { operation, table, id, data } = job.data;

  try {
    await User.update(data, { where: { id } });
  } catch (error) {
    // Handle error: retry, log, alert
    console.error('Database write failed:', error);
    throw error; // Retry
  }
});
```

**Best for**: Write-heavy workloads, can tolerate eventual consistency

**Warning**: Risk of data loss if cache fails before persistence

### 4. Refresh-Ahead

**Pattern**: Automatically refresh cache before expiration

```javascript
// ✅ GOOD: Refresh-ahead pattern
class CacheManager {
  constructor(redis, refreshThreshold = 0.8) {
    this.redis = redis;
    this.refreshThreshold = refreshThreshold;
  }

  async get(key, loader, ttl = 3600) {
    const data = await this.redis.get(key);

    if (data) {
      // Check TTL
      const ttlRemaining = await this.redis.ttl(key);

      // Refresh if close to expiration
      if (ttlRemaining < ttl * this.refreshThreshold) {
        // Refresh asynchronously (don't wait)
        this.refreshCache(key, loader, ttl).catch(console.error);
      }

      return JSON.parse(data);
    }

    // Cache miss: load and cache
    const freshData = await loader();
    await this.redis.setex(key, ttl, JSON.stringify(freshData));
    return freshData;
  }

  async refreshCache(key, loader, ttl) {
    const freshData = await loader();
    await this.redis.setex(key, ttl, JSON.stringify(freshData));
  }
}

// Usage
const cacheManager = new CacheManager(redis);

async function getPopularProducts() {
  return cacheManager.get(
    'products:popular',
    async () => {
      return await Product.findAll({
        where: { featured: true },
        order: [['sales', 'DESC']],
        limit: 20,
      });
    },
    300 // 5 minutes
  );
}
```

**Best for**: Expensive computations, time-sensitive data

## Cache Invalidation Strategies

### 1. Time-Based Expiration (TTL)

```javascript
// Different TTL for different data types
const CACHE_TTL = {
  USER_PROFILE: 3600,        // 1 hour (changes infrequently)
  USER_SESSION: 1800,        // 30 minutes
  PRODUCT_LIST: 300,         // 5 minutes (changes frequently)
  STATIC_CONTENT: 86400,     // 24 hours
  API_RESPONSE: 60,          // 1 minute (frequently updated)
};

async function cacheData(key, data, type) {
  const ttl = CACHE_TTL[type] || 300;
  await redis.setex(key, ttl, JSON.stringify(data));
}
```

### 2. Event-Based Invalidation

```javascript
// ✅ GOOD: Invalidate cache on events
const EventEmitter = require('events');
const cacheInvalidator = new EventEmitter();

// Listen for invalidation events
cacheInvalidator.on('user:updated', async (userId) => {
  await redis.del(`user:${userId}`);
  await redis.del(`user:${userId}:posts`);
  await redis.del(`user:${userId}:profile`);
});

cacheInvalidator.on('post:created', async (userId) => {
  await redis.del(`user:${userId}:posts`);
  await redis.del('posts:recent');
});

// Emit events on updates
async function updateUser(userId, data) {
  const user = await User.update(data, { where: { id: userId } });

  // Trigger cache invalidation
  cacheInvalidator.emit('user:updated', userId);

  return user;
}
```

### 3. Tag-Based Invalidation

```javascript
// ✅ GOOD: Tag-based cache invalidation
class TaggedCache {
  constructor(redis) {
    this.redis = redis;
  }

  async set(key, data, ttl, tags = []) {
    // Store data
    await this.redis.setex(key, ttl, JSON.stringify(data));

    // Associate tags
    for (const tag of tags) {
      await this.redis.sadd(`tag:${tag}`, key);
    }
  }

  async invalidateByTag(tag) {
    // Get all keys with this tag
    const keys = await this.redis.smembers(`tag:${tag}`);

    if (keys.length > 0) {
      // Delete all associated keys
      await this.redis.del(...keys);
      await this.redis.del(`tag:${tag}`);
    }
  }
}

// Usage
const cache = new TaggedCache(redis);

// Cache with tags
await cache.set('user:123', userData, 3600, ['user', 'user:123']);
await cache.set('user:123:posts', posts, 3600, ['user', 'user:123', 'posts']);

// Invalidate all caches for user 123
await cache.invalidateByTag('user:123');
```

### 4. Pattern-Based Invalidation

```javascript
// ✅ GOOD: Invalidate by pattern
async function invalidateUserCaches(userId) {
  // Find all keys matching pattern
  const pattern = `user:${userId}:*`;
  const keys = await redis.keys(pattern);

  if (keys.length > 0) {
    await redis.del(...keys);
  }
}

// Better: Use SCAN instead of KEYS (non-blocking)
async function invalidateUserCachesSafe(userId) {
  const pattern = `user:${userId}:*`;
  const keysToDelete = [];

  let cursor = '0';
  do {
    const [nextCursor, keys] = await redis.scan(
      cursor,
      'MATCH',
      pattern,
      'COUNT',
      100
    );

    keysToDelete.push(...keys);
    cursor = nextCursor;
  } while (cursor !== '0');

  if (keysToDelete.length > 0) {
    await redis.del(...keysToDelete);
  }
}
```

## HTTP Caching

### Response Headers

```javascript
const express = require('express');
const app = express();

// Static assets: Long cache with immutable
app.use('/static', express.static('public', {
  maxAge: '365d',
  immutable: true,
}));

// API endpoints: Different cache strategies
app.get('/api/products', (req, res) => {
  // Public, can be cached by CDN and browsers
  res.set({
    'Cache-Control': 'public, max-age=300, s-maxage=600', // 5 min browser, 10 min CDN
    'ETag': generateETag(products),
  });
  res.json(products);
});

app.get('/api/user/profile', authenticate, (req, res) => {
  // Private, only browser cache
  res.set({
    'Cache-Control': 'private, max-age=300', // 5 minutes
    'Vary': 'Authorization', // Different cache per user
  });
  res.json(userProfile);
});

app.get('/api/user/balance', authenticate, (req, res) => {
  // No cache for sensitive/real-time data
  res.set({
    'Cache-Control': 'no-store, no-cache, must-revalidate',
    'Pragma': 'no-cache',
  });
  res.json(balance);
});

// Conditional requests with ETags
app.get('/api/data', (req, res) => {
  const etag = generateETag(data);

  if (req.headers['if-none-match'] === etag) {
    return res.status(304).send(); // Not Modified
  }

  res.set({
    'Cache-Control': 'public, max-age=300',
    'ETag': etag,
  });
  res.json(data);
});
```

### Cache-Control Directives

| Directive | Description | Use Case |
|-----------|-------------|----------|
| `public` | Can be cached by any cache | Public content |
| `private` | Only browser can cache | User-specific data |
| `no-cache` | Must revalidate with server | Frequently updated |
| `no-store` | Do not cache at all | Sensitive data |
| `max-age=N` | Cache for N seconds | Set expiration |
| `s-maxage=N` | CDN cache for N seconds | Longer CDN cache |
| `immutable` | Never changes | Versioned assets |
| `must-revalidate` | Validate before serving stale | Important accuracy |

## In-Memory Caching

### LRU Cache

```javascript
const LRU = require('lru-cache');

// Configure LRU cache
const cache = new LRU({
  max: 500, // Maximum items
  maxAge: 1000 * 60 * 60, // 1 hour
  updateAgeOnGet: true, // Reset TTL on access
  dispose: (key, value) => {
    // Cleanup when item is evicted
    console.log(`Evicted ${key}`);
  },
});

// Usage
function getExpensiveData(key) {
  const cached = cache.get(key);
  if (cached !== undefined) {
    return cached;
  }

  const data = performExpensiveComputation(key);
  cache.set(key, data);
  return data;
}

// Monitor cache performance
function getCacheStats() {
  return {
    itemCount: cache.itemCount,
    length: cache.length,
    max: cache.max,
    hitRate: cache.hits / (cache.hits + cache.misses),
  };
}
```

### Multi-Level Caching

```javascript
// ✅ GOOD: L1 (memory) + L2 (Redis) cache
class MultiLevelCache {
  constructor(redis) {
    this.l1 = new LRU({ max: 100, maxAge: 60000 }); // 1 minute
    this.l2 = redis;
  }

  async get(key) {
    // Try L1 (memory) first
    let data = this.l1.get(key);
    if (data !== undefined) {
      return data;
    }

    // Try L2 (Redis)
    const cached = await this.l2.get(key);
    if (cached) {
      data = JSON.parse(cached);
      // Promote to L1
      this.l1.set(key, data);
      return data;
    }

    return null;
  }

  async set(key, data, ttl = 3600) {
    // Set in both caches
    this.l1.set(key, data);
    await this.l2.setex(key, ttl, JSON.stringify(data));
  }

  async del(key) {
    this.l1.del(key);
    await this.l2.del(key);
  }
}
```

## Cache Performance Patterns

### 1. Stampede Prevention

**Problem**: Multiple requests for expired cache hit database simultaneously

```javascript
// ❌ BAD: Cache stampede
async function getData(key) {
  const cached = await redis.get(key);
  if (cached) return JSON.parse(cached);

  // All requests hit database simultaneously
  const data = await database.query();
  await redis.setex(key, 300, JSON.stringify(data));
  return data;
}

// ✅ GOOD: Use locks to prevent stampede
const locks = new Map();

async function getDataWithLock(key) {
  const cached = await redis.get(key);
  if (cached) return JSON.parse(cached);

  // Check if another request is loading
  if (locks.has(key)) {
    return locks.get(key);
  }

  // Create promise for loading
  const loadingPromise = (async () => {
    try {
      const data = await database.query();
      await redis.setex(key, 300, JSON.stringify(data));
      return data;
    } finally {
      locks.delete(key);
    }
  })();

  locks.set(key, loadingPromise);
  return loadingPromise;
}
```

### 2. Probabilistic Early Expiration

```javascript
// ✅ GOOD: Refresh before expiration with probability
async function getDataWithProbabilisticRefresh(key, ttl = 300) {
  const cached = await redis.get(key);

  if (cached) {
    const remaining = await redis.ttl(key);
    const delta = ttl - remaining;

    // Probability increases as expiration approaches
    const probability = delta / ttl;

    if (Math.random() < probability) {
      // Refresh asynchronously
      refreshData(key, ttl).catch(console.error);
    }

    return JSON.parse(cached);
  }

  // Cache miss
  const data = await loadData();
  await redis.setex(key, ttl, JSON.stringify(data));
  return data;
}
```

### 3. Stale-While-Revalidate

```javascript
// ✅ GOOD: Serve stale data while refreshing
async function getDataStaleWhileRevalidate(key, ttl = 300) {
  const cached = await redis.get(key);

  if (cached) {
    const remaining = await redis.ttl(key);

    if (remaining < 60) { // Less than 1 minute left
      // Serve stale data
      const staleData = JSON.parse(cached);

      // Refresh in background
      refreshData(key, ttl).catch(console.error);

      return staleData;
    }

    return JSON.parse(cached);
  }

  // Cache miss
  const data = await loadData();
  await redis.setex(key, ttl, JSON.stringify(data));
  return data;
}
```

## Monitoring Cache Performance

```javascript
class CacheMonitor {
  constructor(redis) {
    this.redis = redis;
    this.stats = {
      hits: 0,
      misses: 0,
      sets: 0,
      deletes: 0,
    };
  }

  async get(key) {
    const data = await this.redis.get(key);

    if (data) {
      this.stats.hits++;
    } else {
      this.stats.misses++;
    }

    return data;
  }

  async set(key, value, ttl) {
    this.stats.sets++;
    return this.redis.setex(key, ttl, value);
  }

  async del(key) {
    this.stats.deletes++;
    return this.redis.del(key);
  }

  getStats() {
    const total = this.stats.hits + this.stats.misses;
    const hitRate = total > 0 ? (this.stats.hits / total) * 100 : 0;

    return {
      ...this.stats,
      total,
      hitRate: hitRate.toFixed(2) + '%',
    };
  }

  reset() {
    this.stats = { hits: 0, misses: 0, sets: 0, deletes: 0 };
  }
}

// Usage
const cache = new CacheMonitor(redis);

// Log stats every minute
setInterval(() => {
  console.log('Cache stats:', cache.getStats());
  cache.reset();
}, 60000);
```

## Best Practices Checklist

- [ ] Choose appropriate caching strategy (cache-aside, write-through, etc.)
- [ ] Set appropriate TTL for different data types
- [ ] Implement cache invalidation strategy
- [ ] Prevent cache stampede with locks
- [ ] Use multi-level caching for hot data
- [ ] Monitor cache hit rate (aim for >80%)
- [ ] Set up cache size limits (LRU eviction)
- [ ] Use appropriate serialization (JSON, MessagePack, etc.)
- [ ] Implement graceful degradation if cache fails
- [ ] Use HTTP caching headers correctly
- [ ] Tag caches for easy invalidation
- [ ] Monitor cache memory usage
- [ ] Use compression for large cached values
- [ ] Document caching strategy and TTLs

## Common Pitfalls

1. **Caching everything**: Cache only frequently accessed data
2. **No expiration**: Always set TTL to prevent stale data
3. **Large cache values**: Compress or split large values
4. **Ignoring cache failures**: Always have fallback to database
5. **No monitoring**: Track hit rate and performance
6. **Complex invalidation**: Keep invalidation logic simple
7. **Cache stampede**: Use locks or probabilistic refresh
8. **Inconsistent data**: Invalidate properly on updates

## When to Cache

**Good candidates**:
- Expensive database queries
- API responses (especially third-party)
- Computed/aggregated data
- Static or infrequently changing data
- Session data
- Rate limiting counters

**Bad candidates**:
- Real-time data (stock prices, balances)
- Sensitive data (passwords, tokens)
- User-specific data (without proper isolation)
- Data that changes frequently
- Large objects (>1MB)

By following these caching strategies, you can significantly improve application performance while maintaining data consistency.
