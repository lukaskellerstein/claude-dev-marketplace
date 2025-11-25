---
description: Design comprehensive database schema and architecture for a given domain or system
---

Design a complete database architecture for the specified domain or system.

## Process

Follow these steps:

1. **Analyze Requirements**: Understand the domain, data entities, relationships, and access patterns from the user's request and existing codebase

2. **Launch Data Modeling Expert**: Use the `database-plugin:data-modeling-expert` agent to:
   - Create conceptual ER diagram
   - Analyze access patterns
   - Recommend database technology selection
   - Design high-level data architecture
   - Consider scalability and performance requirements

3. **Database-Specific Design**: Based on recommended database type:

   **For SQL Databases (PostgreSQL, Supabase)**:
   - Use the `database-plugin:sql-database-expert` agent to:
     - Design normalized schema with tables, columns, types
     - Define constraints, indexes, and relationships
     - Create migration scripts
     - Design RLS policies (for Supabase)
     - Optimize query patterns

   **For NoSQL Databases (MongoDB, Redis, Elasticsearch, Qdrant)**:
   - Use the `database-plugin:nosql-database-expert` agent to:
     - Design document/data structures
     - Plan indexing strategy
     - Define query patterns
     - Design scaling architecture
     - Create code examples

4. **Validate Design**: Review the complete architecture for:
   - Performance at scale
   - Data integrity
   - Migration complexity
   - Cost efficiency

## Output

Present a comprehensive database architecture including:

### 1. Entity Relationship Diagram
- Visual representation using Mermaid
- All entities and relationships
- Cardinality notation

### 2. Database Selection Rationale
- Recommended database technology
- Trade-off analysis
- Alternative options considered

### 3. Detailed Schema Design
- Complete DDL scripts (for SQL)
- Document structures (for NoSQL)
- Data types and constraints
- Index definitions

### 4. Access Pattern Documentation
- Common queries with examples
- Expected query frequency
- Performance characteristics
- EXPLAIN plan analysis (for SQL)

### 5. Migration Strategy
- Step-by-step migration plan
- Initial schema creation
- Data seeding strategy
- Rollback procedures

### 6. Code Examples
- Database connection setup
- CRUD operations
- Complex queries
- Transaction handling
- Error handling

### 7. Performance Optimization
- Indexing strategy
- Caching recommendations
- Query optimization tips
- Scaling strategies

### 8. Security & Access Control
- Authentication setup
- Authorization rules
- RLS policies (if applicable)
- Data encryption

## Example Usage

```
/design-database

Design a database for an e-commerce platform with:
- User authentication and profiles
- Product catalog with categories
- Shopping cart and orders
- Payment processing
- Inventory management
- Order fulfillment tracking
```

The agents will analyze the requirements and deliver a complete, production-ready database design with all necessary documentation and implementation details.
