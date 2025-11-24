---
name: prevent-n-plus-one
description: Auto-invoked when writing database queries to prevent N+1 query problems and ensure eager loading
allowed-tools: Read, Grep, Glob
---

# Prevent N+1 Query Problems

This skill provides guidance on avoiding N+1 query problems when working with ORMs and database queries.

## When Active

This skill activates when you:
- Write Sequelize, TypeORM, Prisma, or Mongoose queries
- Fetch related data or associations
- Implement API endpoints that return nested data
- Work with entity relationships (one-to-many, many-to-many)
- Write loops that include database queries
- Implement GraphQL resolvers

## What is N+1 Query Problem?

The N+1 query problem occurs when:
1. You execute 1 query to fetch N records
2. Then execute N additional queries to fetch related data for each record

**Example**:
```javascript
// 1 query to get users
const users = await User.findAll(); // 1 query

// N queries to get posts for each user
for (const user of users) {
  user.posts = await Post.findAll({ where: { userId: user.id } }); // N queries
}

// Total: 1 + N queries (e.g., 1 + 100 = 101 queries)
```

## Detection Patterns

### Pattern 1: Loop with Database Query
```javascript
// ❌ BAD: N+1 problem
for (const item of items) {
  item.related = await fetchRelated(item.id); // Query inside loop
}

// ❌ BAD: Using map with async
await Promise.all(items.map(async item => {
  item.related = await fetchRelated(item.id); // Still N queries
  return item;
}));
```

### Pattern 2: Accessing Relationship in Loop
```javascript
// ❌ BAD: Lazy loading in loop
const users = await User.findAll();

for (const user of users) {
  console.log(user.posts); // Triggers lazy load query
}
```

### Pattern 3: GraphQL Resolver Without DataLoader
```javascript
// ❌ BAD: Each user triggers separate query
const resolvers = {
  User: {
    posts: (user) => Post.findAll({ where: { userId: user.id } })
  }
};
```

## Solutions

### Solution 1: Eager Loading (Preferred for Most Cases)

#### Sequelize
```javascript
// ✅ GOOD: Eager loading with include
const users = await User.findAll({
  include: [
    {
      model: Post,
      as: 'posts',
    },
  ],
});

// ✅ GOOD: Nested includes
const users = await User.findAll({
  include: [
    {
      model: Post,
      as: 'posts',
      include: [
        {
          model: Comment,
          as: 'comments',
        },
      ],
    },
  ],
});

// ✅ GOOD: Multiple associations
const users = await User.findAll({
  include: [
    { model: Post, as: 'posts' },
    { model: Profile, as: 'profile' },
    { model: Role, as: 'roles' },
  ],
});
```

#### TypeORM
```javascript
// ✅ GOOD: Eager loading with relations
const users = await userRepository.find({
  relations: ['posts', 'profile', 'roles'],
});

// ✅ GOOD: Query builder with leftJoinAndSelect
const users = await userRepository
  .createQueryBuilder('user')
  .leftJoinAndSelect('user.posts', 'posts')
  .leftJoinAndSelect('user.profile', 'profile')
  .getMany();
```

#### Prisma
```javascript
// ✅ GOOD: Include related data
const users = await prisma.user.findMany({
  include: {
    posts: true,
    profile: true,
  },
});

// ✅ GOOD: Nested includes
const users = await prisma.user.findMany({
  include: {
    posts: {
      include: {
        comments: true,
      },
    },
  },
});
```

#### Mongoose
```javascript
// ✅ GOOD: Populate method
const users = await User.find().populate('posts');

// ✅ GOOD: Nested populate
const users = await User.find().populate({
  path: 'posts',
  populate: {
    path: 'comments',
  },
});
```

### Solution 2: DataLoader (Best for GraphQL)

```javascript
const DataLoader = require('dataloader');

// Create batch loader
const postLoader = new DataLoader(async (userIds) => {
  // Single query for all user IDs
  const posts = await Post.findAll({
    where: {
      userId: { [Op.in]: userIds },
    },
  });

  // Group posts by user ID
  const postsByUserId = posts.reduce((acc, post) => {
    if (!acc[post.userId]) acc[post.userId] = [];
    acc[post.userId].push(post);
    return acc;
  }, {});

  // Return posts in same order as userIds
  return userIds.map(userId => postsByUserId[userId] || []);
});

// Use in resolver
const resolvers = {
  User: {
    posts: (user, args, context) => {
      return context.loaders.postLoader.load(user.id);
    },
  },
};
```

### Solution 3: Batch Loading with IN Clause

```javascript
// ✅ GOOD: Single query with IN clause
async function getUsersWithPosts(userIds) {
  const users = await User.findAll({
    where: { id: { [Op.in]: userIds } },
  });

  const posts = await Post.findAll({
    where: { userId: { [Op.in]: userIds } },
  });

  // Group posts by user ID
  const postsByUserId = posts.reduce((acc, post) => {
    if (!acc[post.userId]) acc[post.userId] = [];
    acc[post.userId].push(post);
    return acc;
  }, {});

  // Attach posts to users
  return users.map(user => ({
    ...user.toJSON(),
    posts: postsByUserId[user.id] || [],
  }));
}
```

### Solution 4: Subqueries (For Specific Use Cases)

```javascript
// ✅ GOOD: Subquery for counts
const users = await User.findAll({
  attributes: {
    include: [
      [
        sequelize.literal(`(
          SELECT COUNT(*)
          FROM posts
          WHERE posts.user_id = User.id
        )`),
        'postCount',
      ],
    ],
  },
});
```

## Common Scenarios and Solutions

### Scenario 1: API Endpoint Returning Users with Posts

```javascript
// ❌ BAD
app.get('/api/users', async (req, res) => {
  const users = await User.findAll();

  for (const user of users) {
    user.posts = await Post.findAll({ where: { userId: user.id } });
  }

  res.json(users);
});

// ✅ GOOD
app.get('/api/users', async (req, res) => {
  const users = await User.findAll({
    include: [{ model: Post, as: 'posts' }],
  });

  res.json(users);
});
```

### Scenario 2: Conditional Loading

```javascript
// ❌ BAD: Loading in loop based on condition
const users = await User.findAll();

for (const user of users) {
  if (user.isPremium) {
    user.premiumFeatures = await fetchPremiumFeatures(user.id);
  }
}

// ✅ GOOD: Batch load all premium features
const users = await User.findAll({
  include: [
    {
      model: PremiumFeature,
      as: 'premiumFeatures',
      required: false, // LEFT JOIN instead of INNER JOIN
    },
  ],
});

// Or filter and batch load
const premiumUsers = users.filter(u => u.isPremium);
const premiumUserIds = premiumUsers.map(u => u.id);

const premiumFeatures = await PremiumFeature.findAll({
  where: { userId: { [Op.in]: premiumUserIds } },
});

const featuresByUserId = groupBy(premiumFeatures, 'userId');

users.forEach(user => {
  if (user.isPremium) {
    user.premiumFeatures = featuresByUserId[user.id] || [];
  }
});
```

### Scenario 3: Pagination with Related Data

```javascript
// ❌ BAD: Fetching related data after pagination
const users = await User.findAll({ limit: 20, offset: 0 });

for (const user of users) {
  user.posts = await Post.findAll({ where: { userId: user.id } });
}

// ✅ GOOD: Include with pagination
const users = await User.findAll({
  limit: 20,
  offset: 0,
  include: [{ model: Post, as: 'posts' }],
});

// ✅ BETTER: Use separate subquery
const users = await User.findAll({
  limit: 20,
  offset: 0,
  include: [
    {
      model: Post,
      as: 'posts',
      separate: true, // Separate query but efficient (2 queries total)
    },
  ],
});
```

### Scenario 4: Aggregation with Related Data

```javascript
// ❌ BAD: Counting in loop
const users = await User.findAll();

for (const user of users) {
  user.postCount = await Post.count({ where: { userId: user.id } });
}

// ✅ GOOD: Use subquery or group by
const users = await User.findAll({
  attributes: {
    include: [
      [
        sequelize.literal(`(
          SELECT COUNT(*)
          FROM posts
          WHERE posts.user_id = User.id
        )`),
        'postCount',
      ],
    ],
  },
});

// ✅ ALTERNATIVE: Group by
const usersWithCounts = await User.findAll({
  attributes: [
    'id',
    'name',
    [sequelize.fn('COUNT', sequelize.col('posts.id')), 'postCount'],
  ],
  include: [
    {
      model: Post,
      as: 'posts',
      attributes: [],
    },
  ],
  group: ['User.id'],
});
```

## Detection Tools

### Sequelize Logging
```javascript
// Enable query logging to detect N+1
const sequelize = new Sequelize('database', 'username', 'password', {
  logging: (sql) => {
    console.log('Query:', sql);
    // Count queries to detect N+1
  },
  benchmark: true,
});
```

### Custom Middleware
```javascript
// Express middleware to count queries per request
app.use((req, res, next) => {
  const startQueries = queryCounter.count;

  res.on('finish', () => {
    const totalQueries = queryCounter.count - startQueries;

    if (totalQueries > 10) {
      console.warn(`⚠️  N+1 detected: ${req.method} ${req.url} executed ${totalQueries} queries`);
    }
  });

  next();
});
```

### Automated Detection
```bash
# Use tools like bullet (Ruby) or nplusone (Python)
# For Node.js, use sequelize-query-logger

npm install sequelize-query-logger

# Alerts when N+1 is detected
```

## Performance Impact

### Example with 100 Users

**N+1 Problem**:
```
- 1 query to fetch users: 15ms
- 100 queries to fetch posts: 100 × 12ms = 1,200ms
- Total: 1,215ms
```

**With Eager Loading**:
```
- 1 query to fetch users with posts: 45ms
- Total: 45ms
- Improvement: 96% faster (1,215ms → 45ms)
```

### Example with 1,000 Users

**N+1 Problem**:
```
- 1 query to fetch users: 25ms
- 1,000 queries to fetch posts: 1,000 × 12ms = 12,000ms
- Total: 12,025ms (12 seconds!)
```

**With Eager Loading**:
```
- 1 query to fetch users with posts: 180ms
- Total: 180ms
- Improvement: 98.5% faster (12,025ms → 180ms)
```

## Checklist for Preventing N+1

When writing database queries:

- [ ] Check if you're fetching related data
- [ ] Avoid queries inside loops
- [ ] Use eager loading (include, relations, populate)
- [ ] Use DataLoader for GraphQL resolvers
- [ ] Enable query logging in development
- [ ] Monitor query count per request
- [ ] Use EXPLAIN to analyze query plans
- [ ] Set up alerts for high query counts
- [ ] Review API response times for regressions
- [ ] Test with realistic data volumes

## Red Flags to Watch For

1. **Query inside loop**: `for (const item of items) { await query() }`
2. **Promise.all with queries**: `Promise.all(items.map(item => query(item)))`
3. **Lazy loading in iteration**: `items.forEach(item => item.relation)`
4. **GraphQL resolver fetching**: Each field resolver triggering query
5. **High query count**: > 10 queries for single API request
6. **Linear scaling**: Response time grows linearly with result count

## Testing for N+1

```javascript
// Test that checks query count
describe('GET /api/users', () => {
  it('should not have N+1 query problem', async () => {
    const queryCountBefore = getQueryCount();

    await request(app).get('/api/users');

    const queryCount = getQueryCount() - queryCountBefore;

    // Should use eager loading (1-2 queries max)
    expect(queryCount).toBeLessThanOrEqual(2);
  });
});
```

## Always Remember

- **One query to rule them all**: Fetch related data in single query when possible
- **Eager loading is your friend**: Use include/relations/populate
- **DataLoader for GraphQL**: Essential for preventing N+1 in GraphQL
- **Batch operations**: Use IN clauses to fetch multiple records
- **Monitor in production**: Set up query count monitoring
- **Test with realistic data**: N+1 problems often appear at scale

By following these patterns, you can prevent N+1 query problems and ensure your database queries remain efficient even as your data grows.
