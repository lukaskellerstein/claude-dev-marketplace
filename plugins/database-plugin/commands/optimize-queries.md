---
description: Analyze and optimize database queries for better performance
---

Analyze existing database queries and provide optimization recommendations.

## Process

Follow these steps:

1. **Analyze Current Queries**: Search the codebase for database queries:
   - SQL queries (SELECT, INSERT, UPDATE, DELETE)
   - ORM queries (Prisma, TypeORM, SQLAlchemy, Mongoose, etc.)
   - NoSQL queries (MongoDB, Redis, Elasticsearch)
   - Vector searches (Qdrant)

2. **Identify Database Type**: Determine which database(s) are being used:
   - Check connection strings, configuration files
   - Identify database clients/libraries
   - Look for schema files or migrations

3. **Launch Appropriate Expert**:

   **For SQL Databases**:
   - Use the `sql-database-expert` agent to:
     - Analyze query execution plans
     - Identify missing indexes
     - Detect N+1 query problems
     - Recommend query rewrites
     - Suggest schema optimizations

   **For NoSQL Databases**:
   - Use the `nosql-database-expert` agent to:
     - Analyze query patterns
     - Review indexing strategy
     - Identify inefficient operations
     - Recommend caching strategies
     - Optimize aggregation pipelines

4. **Provide Optimization Plan**: Create actionable recommendations with:
   - Specific queries to optimize
   - Index creation scripts
   - Query rewrites with before/after examples
   - Expected performance improvements
   - Implementation priority

## Output

Present a comprehensive optimization report including:

### 1. Query Analysis Summary
- Total queries analyzed
- Performance bottlenecks identified
- Overall health score

### 2. Critical Issues (High Priority)
For each critical issue:
- **Location**: File path and line numbers
- **Current Query**: Existing implementation
- **Problem**: What's wrong and why it's slow
- **Optimized Query**: Improved version
- **Required Indexes**: Index creation scripts
- **Expected Impact**: Performance improvement estimate
- **Implementation**: Step-by-step instructions

### 3. Medium Priority Issues
Similar format to critical issues but less urgent

### 4. Best Practice Recommendations
- General optimization tips
- Code patterns to follow
- Patterns to avoid
- Configuration tuning suggestions

### 5. Monitoring Recommendations
- Slow query logging setup
- Performance metrics to track
- Alerting thresholds
- Query analysis tools

## Example Usage

```
/optimize-queries

Analyze all database queries in the src/ directory and provide optimization recommendations
```

Or for specific files:

```
/optimize-queries

Optimize the queries in src/services/user-service.ts
```

## Common Optimizations

The agents will look for and fix:

**SQL Optimization**
- Missing indexes on WHERE/JOIN columns
- SELECT * instead of specific columns
- N+1 queries (should use JOIN or batch loading)
- Subqueries that should be JOINs
- Inefficient JOIN orders
- Missing query limits
- Improper use of LIKE with leading wildcard

**MongoDB Optimization**
- Missing indexes on filter fields
- Fetching entire documents when only fields needed
- Inefficient aggregation pipelines
- Lack of covered queries
- Improper use of $lookup

**Redis Optimization**
- Inefficient data structures
- Missing pipeline usage
- Lack of key expiration
- Memory-intensive operations

**Elasticsearch Optimization**
- Missing index optimization
- Overly broad queries
- Missing filters on queries
- Improper aggregation bucket sizes

**Qdrant Optimization**
- Inefficient vector search parameters
- Missing payload indexes
- Lack of quantization
- Improper filtering strategies

The agents will provide specific, actionable recommendations with code examples and expected performance improvements.
