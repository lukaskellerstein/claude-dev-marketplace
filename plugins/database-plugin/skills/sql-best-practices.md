---
name: sql-best-practices
description: Auto-invoked when writing SQL queries or schema definitions to ensure best practices, security, and performance
allowed-tools: Read, Grep, Glob
---

# SQL Best Practices

This skill provides guidance on writing secure, performant, and maintainable SQL code.

## When Active

This skill activates when you:
- Write SQL queries (SELECT, INSERT, UPDATE, DELETE)
- Create or modify database schemas
- Design indexes or constraints
- Work with database migrations
- Review SQL code for optimization

## Security Best Practices

### SQL Injection Prevention

❌ **NEVER do this**:
```sql
-- Vulnerable to SQL injection
SELECT * FROM users WHERE email = '" + userInput + "'";
```

✅ **ALWAYS use parameterized queries**:
```sql
-- Safe parameterized query
SELECT * FROM users WHERE email = $1;
```

```javascript
// Node.js with pg
const result = await client.query(
  'SELECT * FROM users WHERE email = $1',
  [userEmail]
);

// Python with psycopg2
cursor.execute(
  'SELECT * FROM users WHERE email = %s',
  (user_email,)
)
```

### Principle of Least Privilege
```sql
-- Create read-only user
CREATE USER readonly_user WITH PASSWORD 'secure_password';
GRANT CONNECT ON DATABASE mydb TO readonly_user;
GRANT USAGE ON SCHEMA public TO readonly_user;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO readonly_user;

-- Create app user with limited permissions
CREATE USER app_user WITH PASSWORD 'secure_password';
GRANT CONNECT ON DATABASE mydb TO app_user;
GRANT SELECT, INSERT, UPDATE ON specific_tables TO app_user;
```

## Performance Best Practices

### 1. Use Specific Column Names

❌ **Avoid**:
```sql
SELECT * FROM users WHERE id = 123;
```

✅ **Prefer**:
```sql
SELECT id, name, email, created_at FROM users WHERE id = 123;
```

**Why**: Reduces data transfer, allows covering indexes, clearer intent

### 2. Use Appropriate Indexes

```sql
-- Index for WHERE clause columns
CREATE INDEX idx_users_email ON users(email);

-- Composite index for multiple columns (order matters!)
CREATE INDEX idx_orders_user_status ON orders(user_id, status);

-- Partial index for frequent filters
CREATE INDEX idx_active_users ON users(id) WHERE status = 'active';

-- Covering index (include extra columns)
CREATE INDEX idx_users_email_covering ON users(email) INCLUDE (name, created_at);
```

### 3. Avoid N+1 Queries

❌ **N+1 Query Problem**:
```javascript
// Fetches users (1 query)
const users = await db.query('SELECT * FROM users LIMIT 10');

// Then for each user, fetch orders (N queries)
for (const user of users) {
  const orders = await db.query(
    'SELECT * FROM orders WHERE user_id = $1',
    [user.id]
  );
}
```

✅ **Use JOIN or IN clause**:
```sql
-- Single query with JOIN
SELECT u.*, o.*
FROM users u
LEFT JOIN orders o ON o.user_id = u.id
WHERE u.id IN (1, 2, 3, 4, 5);

-- Or use IN clause
SELECT * FROM orders WHERE user_id IN (1, 2, 3, 4, 5);
```

### 4. Use LIMIT for Large Result Sets

```sql
-- Always limit results when you don't need all
SELECT * FROM users ORDER BY created_at DESC LIMIT 100;

-- For pagination, use OFFSET (but be aware of performance issues with large offsets)
SELECT * FROM users ORDER BY created_at DESC LIMIT 20 OFFSET 40;

-- Better pagination with cursor-based approach
SELECT * FROM users
WHERE created_at < $1
ORDER BY created_at DESC
LIMIT 20;
```

### 5. Use Appropriate JOINs

```sql
-- INNER JOIN (only matching rows)
SELECT u.name, o.order_date
FROM users u
INNER JOIN orders o ON o.user_id = u.id;

-- LEFT JOIN (all left rows, matching right rows)
SELECT u.name, o.order_date
FROM users u
LEFT JOIN orders o ON o.user_id = u.id;

-- Use WHERE vs JOIN condition appropriately
-- Filter on left table: use WHERE
-- Filter on right table in LEFT JOIN: use JOIN ON
SELECT u.name, o.order_date
FROM users u
LEFT JOIN orders o ON o.user_id = u.id AND o.status = 'completed'
WHERE u.status = 'active';
```

## Schema Design Best Practices

### 1. Use Appropriate Data Types

```sql
-- Use specific types, not generic TEXT
CREATE TABLE users (
  id BIGSERIAL PRIMARY KEY,                    -- Auto-incrementing big integer
  email TEXT NOT NULL UNIQUE,                  -- Text for variable length strings
  age INTEGER CHECK (age >= 0 AND age <= 150), -- Integer with constraint
  balance DECIMAL(10,2) NOT NULL DEFAULT 0.00, -- Exact decimal for money
  is_active BOOLEAN DEFAULT true,              -- Boolean not integer
  created_at TIMESTAMPTZ DEFAULT NOW(),        -- Timestamp with timezone
  metadata JSONB,                              -- JSONB for structured data
  tags TEXT[]                                  -- Array for multiple values
);
```

### 2. Use Constraints

```sql
-- Primary key
CREATE TABLE orders (
  id BIGSERIAL PRIMARY KEY,

  -- Foreign key with cascading
  user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,

  -- NOT NULL constraint
  status TEXT NOT NULL,

  -- CHECK constraint
  amount DECIMAL(10,2) CHECK (amount >= 0),

  -- UNIQUE constraint
  order_number TEXT UNIQUE,

  -- UNIQUE composite constraint
  UNIQUE(user_id, order_number)
);
```

### 3. Use Indexes Strategically

```sql
-- Index foreign keys
CREATE INDEX idx_orders_user_id ON orders(user_id);

-- Index frequently queried columns
CREATE INDEX idx_orders_status ON orders(status);

-- Composite index for common multi-column queries
CREATE INDEX idx_orders_user_status_date
  ON orders(user_id, status, created_at);

-- Partial index for specific queries
CREATE INDEX idx_pending_orders
  ON orders(created_at)
  WHERE status = 'pending';

-- Use CONCURRENTLY for zero-downtime
CREATE INDEX CONCURRENTLY idx_users_email ON users(email);
```

## Transaction Best Practices

### 1. Use Transactions for Multi-Step Operations

```sql
BEGIN;

INSERT INTO orders (user_id, amount) VALUES (123, 50.00) RETURNING id;
UPDATE users SET balance = balance - 50.00 WHERE id = 123;
INSERT INTO audit_log (action, user_id) VALUES ('purchase', 123);

COMMIT;
```

### 2. Keep Transactions Short

❌ **Avoid**:
```javascript
await client.query('BEGIN');
await processPayment();        // External API call - slow!
await client.query('INSERT INTO orders ...');
await sendEmail();             // External service - slow!
await client.query('COMMIT');
```

✅ **Prefer**:
```javascript
await client.query('BEGIN');
await client.query('INSERT INTO orders ...');
await client.query('COMMIT');

// Do external operations after commit
await processPayment();
await sendEmail();
```

### 3. Handle Transaction Errors

```javascript
try {
  await client.query('BEGIN');
  await client.query('INSERT INTO orders ...');
  await client.query('UPDATE users ...');
  await client.query('COMMIT');
} catch (error) {
  await client.query('ROLLBACK');
  throw error;
}
```

## Query Optimization

### 1. Use EXPLAIN to Analyze Queries

```sql
-- See execution plan
EXPLAIN SELECT * FROM users WHERE email = 'user@example.com';

-- See actual execution statistics
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'user@example.com';

-- Look for:
-- - Seq Scan (might need index)
-- - High cost values
-- - Large row counts
-- - Nested loops with high iterations
```

### 2. Use CTEs for Readability

```sql
-- Common Table Expression for complex queries
WITH active_users AS (
  SELECT id, name FROM users WHERE status = 'active'
),
recent_orders AS (
  SELECT user_id, COUNT(*) as order_count
  FROM orders
  WHERE created_at > NOW() - INTERVAL '30 days'
  GROUP BY user_id
)
SELECT u.name, COALESCE(o.order_count, 0) as orders
FROM active_users u
LEFT JOIN recent_orders o ON o.user_id = u.id
ORDER BY orders DESC;
```

### 3. Avoid Functions in WHERE Clauses

❌ **Avoid** (can't use index):
```sql
SELECT * FROM users WHERE LOWER(email) = 'user@example.com';
SELECT * FROM orders WHERE DATE(created_at) = '2024-01-01';
```

✅ **Prefer** (can use index):
```sql
-- Create expression index
CREATE INDEX idx_users_email_lower ON users(LOWER(email));
SELECT * FROM users WHERE LOWER(email) = 'user@example.com';

-- Or compare ranges
SELECT * FROM orders
WHERE created_at >= '2024-01-01'
  AND created_at < '2024-01-02';
```

## Maintenance Best Practices

### 1. Regular VACUUM and ANALYZE

```sql
-- Vacuum to reclaim space and update statistics
VACUUM ANALYZE users;

-- Full vacuum (requires table lock)
VACUUM FULL users;

-- Configure autovacuum (in postgresql.conf)
-- autovacuum = on
-- autovacuum_vacuum_scale_factor = 0.1
-- autovacuum_analyze_scale_factor = 0.05
```

### 2. Monitor Slow Queries

```sql
-- Enable slow query logging (postgresql.conf)
-- log_min_duration_statement = 1000  # Log queries > 1 second

-- Find slow queries from pg_stat_statements
SELECT
  query,
  calls,
  total_exec_time,
  mean_exec_time,
  max_exec_time
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 10;
```

## Checklist

When writing SQL code:
- [ ] Use parameterized queries (never string concatenation)
- [ ] Select only needed columns (avoid SELECT *)
- [ ] Add appropriate indexes for WHERE/JOIN columns
- [ ] Use transactions for multi-step operations
- [ ] Add constraints (NOT NULL, UNIQUE, CHECK, FK)
- [ ] Use appropriate data types
- [ ] Add LIMIT for potentially large result sets
- [ ] Handle NULL values explicitly
- [ ] Use EXPLAIN to verify query performance
- [ ] Document complex queries with comments

Use this guidance to ensure SQL code follows best practices for security, performance, and maintainability.
