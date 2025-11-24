# Database Plugin

Comprehensive database toolkit for designing, optimizing, and managing SQL and NoSQL databases. Covers PostgreSQL, Supabase, MongoDB, Redis, Elasticsearch, Qdrant, and MinIO (S3).

## Features

### Agents

- **sql-database-expert**: Expert in PostgreSQL and Supabase - schema design, query optimization, indexing strategies, RLS policies, and performance tuning
- **nosql-database-expert**: Expert in MongoDB, Redis, Elasticsearch, and Qdrant - document modeling, caching patterns, search optimization, and vector databases
- **data-modeling-expert**: Expert in data modeling patterns, database selection, migration strategies, and architectural decisions

### Commands

- `/design-database`: Design comprehensive database schema and architecture for a given domain
- `/optimize-queries`: Analyze and optimize existing database queries for better performance
- `/migrate-database`: Plan and execute database migrations with zero-downtime strategies

### Skills

- **sql-best-practices**: Auto-invoked when writing SQL to ensure security, performance, and maintainability
- **database-indexing**: Auto-invoked when designing schemas or optimizing queries to ensure proper indexing strategies

## Usage

### Design New Database Schema

```
/design-database

Design a database for a SaaS application with:
- Multi-tenant architecture
- User authentication and authorization
- Subscription management
- Usage tracking and analytics
- File storage for user uploads
```

The agents will analyze requirements and deliver:
- Entity relationship diagrams
- Complete schema definitions
- Migration scripts
- Indexing strategy
- Query examples
- Performance estimates

### Optimize Existing Queries

```
/optimize-queries

Analyze all queries in src/services/ and provide optimization recommendations
```

The agents will:
- Identify slow queries
- Detect N+1 query problems
- Recommend missing indexes
- Provide query rewrites
- Estimate performance improvements

### Plan Database Migration

```
/migrate-database

Migrate user authentication from MongoDB to PostgreSQL with zero downtime
```

The agents will create:
- Detailed migration plan
- Forward and rollback scripts
- Zero-downtime strategy
- Data validation queries
- Deployment runbook

### Use Agents Directly

Invoke specialized agents for focused work:

**SQL Database Work**:
- "Use sql-database-expert to design a schema for multi-tenant SaaS"
- "Use sql-database-expert to optimize this slow query"
- "Use sql-database-expert to add full-text search to articles"

**NoSQL Database Work**:
- "Use nosql-database-expert to design MongoDB schema for blog platform"
- "Use nosql-database-expert to implement rate limiting with Redis"
- "Use nosql-database-expert to set up vector search with Qdrant for RAG"

**Data Modeling**:
- "Use data-modeling-expert to choose between SQL and NoSQL for this use case"
- "Use data-modeling-expert to design a zero-downtime migration strategy"
- "Use data-modeling-expert to implement multi-tenancy patterns"

## Database Coverage

### PostgreSQL
- Schema design and normalization
- Advanced features (JSONB, full-text search, arrays, partitioning)
- Query optimization and EXPLAIN analysis
- Indexing strategies (B-tree, GIN, GiST, partial, covering)
- Row-level security
- Transactions and constraints
- Performance tuning

### Supabase
- Real-time subscriptions
- Row-level security (RLS) policies
- PostgREST API configuration
- Edge functions
- Storage buckets
- Auth integration
- Database migrations with Supabase CLI

### MongoDB
- Document schema design
- Embedded vs referenced documents
- Aggregation pipeline optimization
- Indexing strategies
- Sharding and replication
- Change streams
- Transactions
- Schema validation

### Redis
- Data structure selection (strings, hashes, lists, sets, sorted sets)
- Caching strategies (cache-aside, write-through, write-behind)
- Pub/Sub messaging
- Redis Streams
- Lua scripting
- Cluster mode
- Memory optimization
- Rate limiting and session management

### Elasticsearch
- Index mapping and schema design
- Full-text search with analyzers
- Query DSL optimization
- Aggregations for analytics
- Index lifecycle management
- Search relevance tuning
- Performance optimization

### Qdrant (Vector Database)
- Vector collection design
- Embedding strategies
- Vector search optimization
- Hybrid search (vector + keyword)
- Payload indexing and filtering
- RAG (Retrieval Augmented Generation) patterns
- Quantization for performance

### MinIO (S3-Compatible Storage)
- Bucket policies and access control
- Object versioning and lifecycle
- Event notifications
- Server-side encryption
- Multi-part uploads
- Pre-signed URLs
- Integration patterns

## Best Practices Covered

### Security
- SQL injection prevention
- Parameterized queries
- Principle of least privilege
- Row-level security (RLS)
- Data encryption
- Access control policies

### Performance
- Query optimization
- Indexing strategies
- Connection pooling
- Caching layers
- N+1 query prevention
- Query execution plan analysis
- Slow query monitoring

### Data Integrity
- Constraints (PRIMARY KEY, FOREIGN KEY, UNIQUE, CHECK)
- Transactions and ACID properties
- Data validation
- Referential integrity
- Idempotency patterns
- Audit trails

### Scalability
- Database sharding
- Replication strategies
- Read replicas
- Horizontal scaling
- Partitioning
- Connection pooling
- Caching strategies

### Maintainability
- Schema versioning
- Migration strategies
- Zero-downtime deployments
- Rollback procedures
- Documentation
- Monitoring and alerting

## Common Patterns

### Multi-Tenancy
- Shared schema with tenant_id
- Separate schema per tenant
- Separate database per tenant
- Row-level security implementation

### Temporal Data
- Bi-temporal patterns
- Valid time and transaction time
- Audit trails
- Soft deletes
- Historical data tracking

### Event Sourcing
- Event store design
- Event versioning
- Projections and read models
- Snapshots for performance
- CQRS pattern integration

### Full-Text Search
- PostgreSQL full-text search
- Elasticsearch integration
- Search relevance tuning
- Autocomplete patterns
- Faceted search

### Vector Search & RAG
- Embedding generation
- Vector storage with Qdrant
- Similarity search
- Hybrid search strategies
- Retrieval augmented generation

### Caching Strategies
- Cache-aside pattern
- Write-through cache
- Write-behind cache
- Cache invalidation
- Redis implementation

## Architecture Patterns

### Polyglot Persistence
- Use different databases for different requirements
- PostgreSQL for transactional data
- MongoDB for flexible documents
- Redis for caching and sessions
- Elasticsearch for search
- Qdrant for vector similarity
- MinIO for object storage

### Database per Service (Microservices)
- Each service owns its database
- No direct database access across services
- API-based communication
- Saga pattern for distributed transactions
- Event-driven integration

### CQRS (Command Query Responsibility Segregation)
- Separate read and write models
- Optimized read databases (denormalized)
- Event sourcing for commands
- Materialized views for queries
- Eventual consistency

## Examples

### E-Commerce Platform
```
/design-database

Design database for e-commerce with:
- User authentication
- Product catalog with categories
- Shopping cart
- Order processing
- Payment integration
- Inventory management
- Search functionality
- Product recommendations
```

### SaaS Multi-Tenant Application
```
/design-database

Design database for B2B SaaS with:
- Multi-tenant isolation
- Organizations and teams
- Role-based access control
- Usage metering
- Subscription billing
- API rate limiting
- Audit logging
```

### Real-Time Chat Application
```
/design-database

Design database for chat application with:
- User presence
- One-on-one messaging
- Group chats
- Message history
- File attachments
- Real-time updates
- Message search
```

### AI-Powered Application (RAG)
```
/design-database

Design database for RAG application with:
- Document storage
- Vector embeddings
- Semantic search
- User conversations
- Context management
- Metadata filtering
```

## Tips

1. **Start with Requirements**: Always analyze access patterns before choosing database technology
2. **Use the Right Tool**: Don't force SQL patterns on NoSQL or vice versa
3. **Index Strategically**: Index for reads, but consider write performance cost
4. **Monitor Performance**: Use EXPLAIN, slow query logs, and profiling tools
5. **Plan for Scale**: Design for 10x growth from day one
6. **Test Migrations**: Always test migrations on staging with production-like data
7. **Document Decisions**: Use ADRs (Architecture Decision Records) for key choices
8. **Security First**: Parameterize queries, use RLS, implement least privilege

## Resources

- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Supabase Documentation](https://supabase.com/docs)
- [MongoDB Manual](https://docs.mongodb.com/manual/)
- [Redis Documentation](https://redis.io/documentation)
- [Elasticsearch Guide](https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html)
- [Qdrant Documentation](https://qdrant.tech/documentation/)
- [MinIO Documentation](https://min.io/docs/minio/linux/index.html)
