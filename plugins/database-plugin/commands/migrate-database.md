---
description: Plan and execute database migrations or schema changes with zero-downtime strategies
---

Plan and execute database migrations or schema changes safely.

## Process

Follow these steps:

1. **Analyze Current State**: Understand the current database schema:
   - Review existing schema files
   - Check migration history
   - Identify database type and version
   - Document current constraints and indexes

2. **Understand Target State**: Based on user's requirements:
   - New tables/collections to add
   - Schema modifications needed
   - Data transformations required
   - Relationships to create/modify

3. **Launch Data Modeling Expert**: Use the `database-plugin:data-modeling-expert` agent to:
   - Design migration strategy
   - Plan zero-downtime approach
   - Create rollback procedures
   - Define data validation steps
   - Estimate migration time and risk

4. **Create Migration Implementation**:

   **For SQL Databases**:
   - Use the `database-plugin:sql-database-expert` agent to:
     - Write forward migration scripts
     - Write rollback scripts
     - Create index migration strategy
     - Handle data backfills
     - Test migration on sample data

   **For NoSQL Databases**:
   - Use the `database-plugin:nosql-database-expert` agent to:
     - Plan schema evolution strategy
     - Write data transformation scripts
     - Handle backward compatibility
     - Plan index updates
     - Create validation queries

5. **Validation & Testing**: Ensure migration safety:
   - Data integrity checks
   - Performance impact assessment
   - Rollback testing
   - Deployment runbook

## Output

Present a comprehensive migration plan including:

### 1. Migration Overview
- Summary of changes
- Risk assessment (low/medium/high)
- Estimated downtime (if any)
- Affected systems/services

### 2. Pre-Migration Checklist
- [ ] Backup current database
- [ ] Test migration on staging
- [ ] Review rollback procedure
- [ ] Notify stakeholders
- [ ] Schedule maintenance window (if needed)
- [ ] Verify application compatibility

### 3. Migration Scripts

**Forward Migration**
```sql
-- Example for PostgreSQL
BEGIN;

-- Step 1: Add new column (nullable first)
ALTER TABLE users ADD COLUMN phone_number TEXT;

-- Step 2: Backfill data
UPDATE users SET phone_number = extract_phone(email) WHERE phone_number IS NULL;

-- Step 3: Add constraint
ALTER TABLE users ALTER COLUMN phone_number SET NOT NULL;

-- Step 4: Add index
CREATE INDEX CONCURRENTLY idx_users_phone ON users(phone_number);

COMMIT;
```

**Rollback Migration**
```sql
-- Rollback procedure
BEGIN;

DROP INDEX IF EXISTS idx_users_phone;
ALTER TABLE users DROP COLUMN IF EXISTS phone_number;

COMMIT;
```

### 4. Zero-Downtime Strategy

For breaking changes:
1. **Phase 1**: Add new schema alongside old
2. **Phase 2**: Deploy application supporting both schemas (dual-write)
3. **Phase 3**: Backfill data from old to new schema
4. **Phase 4**: Validate data consistency
5. **Phase 5**: Switch reads to new schema
6. **Phase 6**: Remove old schema after verification period

### 5. Data Validation Queries
- Queries to verify data integrity
- Row count comparisons
- Constraint validation
- Performance benchmarks

### 6. Rollback Procedure
- Step-by-step rollback instructions
- Data restoration steps
- Application rollback coordination
- Verification queries

### 7. Post-Migration Tasks
- [ ] Verify all data migrated correctly
- [ ] Run performance tests
- [ ] Monitor error rates
- [ ] Update documentation
- [ ] Remove dual-write code (if applicable)
- [ ] Archive old schema (if applicable)

## Example Usage

```
/migrate-database

Add a new 'phone_number' field to users table with validation
```

```
/migrate-database

Migrate from MongoDB to PostgreSQL while maintaining service availability
```

```
/migrate-database

Split the monolithic 'orders' table into 'orders' and 'order_items' tables
```

## Migration Patterns

### Additive Changes (Low Risk)
- Adding nullable columns
- Adding new tables/collections
- Adding indexes (use CONCURRENTLY in PostgreSQL)
- Adding optional fields

### Modification Changes (Medium Risk)
- Renaming columns (use view/alias pattern)
- Changing data types (requires transformation)
- Adding constraints to existing data
- Modifying relationships

### Destructive Changes (High Risk)
- Dropping columns/tables
- Removing constraints
- Data deletion
- Schema refactoring

## Database-Specific Guidance

**PostgreSQL**
- Use `CREATE INDEX CONCURRENTLY` for zero-downtime
- Utilize `ALTER TABLE` safely with locks awareness
- Consider partitioning for large tables
- Use `pg_dump` for backups

**MongoDB**
- Schema-less allows gradual migration
- Use versioned documents
- Leverage change streams for sync
- Plan collection rename strategy

**Supabase**
- Use Supabase CLI for migrations
- Update RLS policies atomically
- Consider PostgREST API impact
- Test edge function changes

**Redis**
- Plan key migration strategy
- Use DUMP/RESTORE for data
- Consider key expiration
- Handle cluster resharding

The agents will create production-ready migration scripts with safety checks, validation, and rollback procedures.
