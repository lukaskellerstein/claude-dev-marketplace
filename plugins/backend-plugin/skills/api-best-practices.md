---
name: api-best-practices
description: Automatically enforces API design best practices
allowed-tools: Read, Grep, Glob
---

# API Best Practices Skill

This skill automatically activates when working on API endpoints to ensure best practices are followed.

## Automatic Checks

### REST API Standards
- ✅ Proper HTTP methods (GET for read, POST for create, PUT for update, DELETE for remove)
- ✅ Consistent resource naming (plural nouns for collections)
- ✅ Appropriate status codes (200 OK, 201 Created, 204 No Content, 400 Bad Request, 401 Unauthorized, 404 Not Found)
- ✅ Pagination implemented for list endpoints
- ✅ Filtering and sorting parameters supported
- ✅ Consistent error response format

### Security Checks
- ✅ Authentication middleware present
- ✅ Authorization checks for protected resources
- ✅ Input validation on all endpoints
- ✅ SQL injection prevention (parameterized queries)
- ✅ Rate limiting configured
- ✅ CORS properly configured
- ✅ Sensitive data not exposed in responses

### Performance Optimization
- ✅ Database query optimization (N+1 query prevention)
- ✅ Proper caching headers (ETag, Cache-Control)
- ✅ Response compression enabled
- ✅ Connection pooling configured
- ✅ Async operations for I/O
- ✅ Pagination limits enforced

### Documentation Requirements
- ✅ OpenAPI/Swagger specification exists
- ✅ Request/response examples provided
- ✅ Error codes documented
- ✅ Authentication methods described
- ✅ Rate limits documented

## Validation Rules

When this skill detects API endpoint creation or modification, it automatically:

1. **Checks naming conventions**: Ensures endpoints follow RESTful naming
2. **Validates HTTP methods**: Confirms appropriate method usage
3. **Reviews status codes**: Ensures correct HTTP status codes
4. **Inspects security**: Looks for authentication and validation
5. **Suggests improvements**: Provides recommendations for optimization

## Common Issues Detected

- Missing input validation
- Incorrect HTTP status codes
- Missing error handling
- No pagination on list endpoints
- Exposed sensitive data
- Missing authentication
- SQL injection vulnerabilities
- N+1 query problems

## Automatic Suggestions

When issues are detected, this skill will suggest:

- Adding validation middleware
- Implementing proper error responses
- Adding pagination parameters
- Implementing caching strategies
- Adding rate limiting
- Improving query performance

This skill runs automatically and requires no manual invocation.