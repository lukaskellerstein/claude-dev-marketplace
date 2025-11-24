---
name: database-indexing
description: Auto-invoked when designing schemas or optimizing queries to ensure proper indexing strategies across SQL and NoSQL databases
allowed-tools: Read, Grep, Glob
---

# Database Indexing Strategies

This skill provides guidance on creating effective indexes for various database types.

## When Active

This skill activates when you:
- Design database schemas
- Optimize query performance
- Review slow queries
- Create or modify indexes
- Analyze query execution plans

## Index Fundamentals

### What Are Indexes?
Indexes are data structures that improve query performance by allowing the database to find rows faster. Think of them like a book's index - instead of scanning every page, you can jump directly to the relevant section.

### Trade-offs
- **Pros**: Faster reads, improved query performance
- **Cons**: Slower writes, increased storage, maintenance overhead

**Rule of Thumb**: Index columns that appear in WHERE, JOIN, ORDER BY, and GROUP BY clauses.

## PostgreSQL Indexing

### B-Tree Indexes (Default)

Best for: equality and range queries on sortable data

```sql
-- Single column index
CREATE INDEX idx_users_email ON users(email);

-- Composite index (order matters!)
-- Good for: WHERE user_id = X AND status = Y
-- Good for: WHERE user_id = X
-- Bad for: WHERE status = Y (doesn't use index)
CREATE INDEX idx_orders_user_status ON orders(user_id, status);

-- Include additional columns (covering index)
-- Allows index-only scans
CREATE INDEX idx_users_email_covering
  ON users(email)
  INCLUDE (name, created_at);
```

**Query Pattern Analysis**:
```sql
-- This query benefits from composite index (user_id, status, created_at)
SELECT * FROM orders
WHERE user_id = 123
  AND status = 'pending'
ORDER BY created_at DESC
LIMIT 10;

-- Create optimal index
CREATE INDEX idx_orders_user_status_date
  ON orders(user_id, status, created_at DESC);
```

### Partial Indexes

Best for: queries that always filter on the same condition

```sql
-- Only index active users
CREATE INDEX idx_active_users
  ON users(email)
  WHERE status = 'active' AND deleted_at IS NULL;

-- Only index pending orders
CREATE INDEX idx_pending_orders
  ON orders(created_at)
  WHERE status = 'pending';

-- Benefits: smaller index size, faster queries for this specific filter
```

### Expression Indexes

Best for: queries that use functions on columns

```sql
-- For case-insensitive searches
CREATE INDEX idx_users_email_lower ON users(LOWER(email));
SELECT * FROM users WHERE LOWER(email) = LOWER($1);

-- For JSON field access
CREATE INDEX idx_users_metadata_name
  ON users((metadata->>'name'));
SELECT * FROM users WHERE metadata->>'name' = 'John';
```

### GIN Indexes

Best for: full-text search, JSONB, arrays

```sql
-- Full-text search
ALTER TABLE articles ADD COLUMN search_vector tsvector;
UPDATE articles SET search_vector =
  to_tsvector('english', title || ' ' || content);
CREATE INDEX idx_articles_search ON articles USING GIN(search_vector);

-- Query
SELECT * FROM articles
WHERE search_vector @@ to_tsquery('english', 'database & performance');

-- JSONB queries
CREATE INDEX idx_users_metadata ON users USING GIN(metadata);
SELECT * FROM users WHERE metadata @> '{"city": "New York"}';

-- Array queries
CREATE INDEX idx_posts_tags ON posts USING GIN(tags);
SELECT * FROM posts WHERE tags @> ARRAY['postgresql', 'performance'];
```

### GiST Indexes

Best for: geometric data, full-text search

```sql
-- Geometric queries
CREATE INDEX idx_locations_point ON locations USING GiST(coordinates);

-- Range queries
CREATE INDEX idx_events_daterange ON events USING GiST(daterange);
```

### Hash Indexes

Best for: simple equality comparisons (rarely used)

```sql
CREATE INDEX idx_users_id_hash ON users USING HASH(id);
-- Only useful for: WHERE id = X
-- Not useful for: WHERE id > X or ORDER BY id
```

### Unique Indexes

Enforce uniqueness and improve query performance

```sql
-- Single column unique
CREATE UNIQUE INDEX idx_users_email_unique ON users(email);

-- Composite unique
CREATE UNIQUE INDEX idx_users_org_email
  ON users(organization_id, email);

-- Partial unique (unique only for active users)
CREATE UNIQUE INDEX idx_active_users_email
  ON users(email)
  WHERE deleted_at IS NULL;
```

## MongoDB Indexing

### Single Field Index

```javascript
// Create index
db.users.createIndex({ email: 1 });  // 1 = ascending, -1 = descending

// Query that uses index
db.users.find({ email: "user@example.com" });
```

### Compound Index

```javascript
// Create compound index
db.orders.createIndex({ userId: 1, status: 1, createdAt: -1 });

// Good queries (use index)
db.orders.find({ userId: 123 });
db.orders.find({ userId: 123, status: "pending" });
db.orders.find({ userId: 123, status: "pending" }).sort({ createdAt: -1 });

// Bad query (doesn't use index efficiently)
db.orders.find({ status: "pending" });  // Missing userId prefix
```

### Text Index

```javascript
// Create text index
db.articles.createIndex({ title: "text", content: "text" });

// Search
db.articles.find({
  $text: { $search: "database performance" }
});

// With relevance score
db.articles.find(
  { $text: { $search: "database performance" } },
  { score: { $meta: "textScore" } }
).sort({ score: { $meta: "textScore" } });
```

### Geospatial Index

```javascript
// 2dsphere index for geo queries
db.places.createIndex({ location: "2dsphere" });

// Find nearby places
db.places.find({
  location: {
    $near: {
      $geometry: { type: "Point", coordinates: [-73.9667, 40.78] },
      $maxDistance: 5000  // meters
    }
  }
});
```

### Partial Index

```javascript
// Index only active users
db.users.createIndex(
  { email: 1 },
  { partialFilterExpression: { status: "active" } }
);
```

### Unique Index

```javascript
// Unique email
db.users.createIndex({ email: 1 }, { unique: true });

// Unique only when field exists (sparse)
db.users.createIndex(
  { socialSecurityNumber: 1 },
  { unique: true, sparse: true }
);
```

## Redis Indexing (with RedisJSON and RediSearch)

### RediSearch Indexes

```python
from redis import Redis
from redis.commands.search.field import TextField, NumericField, TagField

r = Redis()

# Create index
r.ft("idx:users").create_index([
    TextField("name"),
    TextField("email"),
    NumericField("age"),
    TagField("tags")
])

# Search
r.ft("idx:users").search("@name:john @age:[25 35]")
```

## Elasticsearch Indexing

Elasticsearch automatically indexes all fields, but you can optimize:

### Mapping Configuration

```json
PUT /products
{
  "mappings": {
    "properties": {
      "title": {
        "type": "text",
        "analyzer": "english",
        "fields": {
          "keyword": {
            "type": "keyword"
          }
        }
      },
      "price": {
        "type": "double",
        "index": true
      },
      "description": {
        "type": "text",
        "index": false
      },
      "tags": {
        "type": "keyword"
      },
      "created_at": {
        "type": "date"
      }
    }
  }
}
```

### Field Types
- `text`: Full-text search (analyzed)
- `keyword`: Exact matches, aggregations, sorting
- `date`: Date/time values
- `numeric`: Numbers with range queries
- `boolean`: True/false
- `object`: Nested objects
- `nested`: Array of objects with independent querying

## Qdrant Indexing

### Payload Indexing

```python
from qdrant_client import QdrantClient
from qdrant_client.models import PayloadSchemaType

client = QdrantClient("localhost", port=6333)

# Create payload indexes for filtering
client.create_payload_index(
    collection_name="documents",
    field_name="category",
    field_schema=PayloadSchemaType.KEYWORD
)

client.create_payload_index(
    collection_name="documents",
    field_name="price",
    field_schema=PayloadSchemaType.FLOAT
)

# Now filtering is fast
results = client.search(
    collection_name="documents",
    query_vector=embedding,
    query_filter={
        "must": [
            {"key": "category", "match": {"value": "electronics"}},
            {"key": "price", "range": {"lt": 1000}}
        ]
    }
)
```

## Index Optimization Patterns

### 1. Covering Index Pattern

**Problem**: Query accesses table after index lookup (expensive)

**Solution**: Include all needed columns in index

```sql
-- Query needs: email, name, created_at
SELECT name, created_at FROM users WHERE email = $1;

-- Create covering index
CREATE INDEX idx_users_email_covering
  ON users(email)
  INCLUDE (name, created_at);

-- Now it's an index-only scan (no table access needed)
```

### 2. Index Column Order

**Rule**: Most selective columns first in composite indexes

```sql
-- Assume: 100K users, 10 statuses, 2 types
-- Bad: status (10 values) first
CREATE INDEX idx_orders_bad ON orders(status, user_id, type);

-- Good: user_id (100K values) first
CREATE INDEX idx_orders_good ON orders(user_id, status, type);
```

### 3. Monitoring Index Usage

```sql
-- PostgreSQL: Find unused indexes
SELECT
    schemaname,
    tablename,
    indexname,
    idx_scan,
    pg_size_pretty(pg_relation_size(indexrelid)) AS size
FROM pg_stat_user_indexes
WHERE idx_scan = 0
  AND indexrelid NOT IN (
    SELECT indexrelid FROM pg_index WHERE indisprimary
  )
ORDER BY pg_relation_size(indexrelid) DESC;

-- Drop unused index
DROP INDEX CONCURRENTLY idx_unused_index;
```

```javascript
// MongoDB: Check index usage
db.users.aggregate([
  { $indexStats: {} }
]);

// Drop unused index
db.users.dropIndex("index_name");
```

## Index Anti-Patterns

### ❌ Over-Indexing

```sql
-- Too many indexes hurt write performance
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_name ON users(name);
CREATE INDEX idx_users_created ON users(created_at);
CREATE INDEX idx_users_updated ON users(updated_at);
CREATE INDEX idx_users_email_name ON users(email, name);
CREATE INDEX idx_users_name_email ON users(name, email);
-- 6 indexes on one table! Probably too many.
```

### ❌ Indexing Low-Cardinality Columns

```sql
-- Bad: boolean or enum with few values
CREATE INDEX idx_users_is_active ON users(is_active);
-- Better: use partial index if you query one value frequently
CREATE INDEX idx_active_users ON users(id) WHERE is_active = true;
```

### ❌ Wrong Column Order in Composite Index

```sql
-- Query: WHERE user_id = X AND status = Y
-- Bad: wrong order
CREATE INDEX idx_orders_bad ON orders(status, user_id);

-- Good: matching query order
CREATE INDEX idx_orders_good ON orders(user_id, status);
```

## Checklist

When designing indexes:
- [ ] Index foreign key columns
- [ ] Index columns in WHERE clauses
- [ ] Index columns in JOIN conditions
- [ ] Index columns in ORDER BY clauses
- [ ] Consider composite indexes for multi-column queries
- [ ] Put most selective columns first in composite indexes
- [ ] Use partial indexes for frequent filters
- [ ] Use covering indexes for frequently accessed columns
- [ ] Monitor index usage and remove unused indexes
- [ ] Use EXPLAIN to verify index is being used
- [ ] Consider index maintenance cost vs. query performance benefit
- [ ] Create indexes CONCURRENTLY in production (PostgreSQL)

Use this guidance to create optimal indexing strategies across different database systems.
