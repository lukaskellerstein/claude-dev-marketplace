---
description: Design a comprehensive REST, GraphQL, or gRPC API for a given domain or feature
---

Design a production-ready API with complete specifications, documentation, and implementation guidance.

## Process

Follow these steps:

1. **Analyze Requirements**: Understand the domain, use cases, and existing codebase
   - Identify API consumers (web, mobile, internal services)
   - Review existing data models and business logic
   - Determine performance and scalability requirements
   - Check for existing API patterns in the codebase

2. **Launch API Designer**: Use the `api-designer` agent to:
   - Choose appropriate API style (REST, GraphQL, gRPC)
   - Design resource models and type system
   - Define endpoints/operations with clear semantics
   - Design request/response schemas
   - Plan error handling strategy
   - Design authentication and authorization
   - Create versioning strategy
   - Write comprehensive API specification

3. **Security Review**: Ensure security best practices:
   - Authentication mechanism (JWT, OAuth2, API keys)
   - Authorization rules (RBAC, ABAC)
   - Input validation and sanitization
   - Rate limiting strategy
   - CORS configuration

4. **Documentation**: Generate complete API documentation:
   - OpenAPI/Swagger for REST
   - GraphQL schema with descriptions
   - Protocol Buffers for gRPC
   - Example requests and responses
   - Client SDK examples
   - Postman/Insomnia collection

## Output

Present a comprehensive API design including:

### API Specification
- Complete OpenAPI 3.0 spec, GraphQL schema, or .proto files
- All endpoints/operations documented
- Request/response schemas with examples
- Error codes and messages

### Data Models
- Entity definitions with relationships
- Input/output type definitions
- Validation rules
- Default values and constraints

### Security Design
- Authentication flow diagram
- Authorization matrix (who can do what)
- API key management strategy
- Rate limiting rules

### Implementation Guide
- Recommended framework/library
- Code structure and organization
- Middleware/interceptor chain
- Database query optimization
- Caching strategy

### Documentation
- README with getting started guide
- API reference documentation
- Postman/Insomnia collection
- Client integration examples
- Migration guide (if refactoring existing API)

### Performance Considerations
- Pagination strategy
- Caching headers
- Compression settings
- Connection pooling
- Query optimization

## Examples

### Design REST API
```
/design-api

Design a REST API for user management with CRUD operations,
role-based access control, and profile picture upload
```

### Design GraphQL API
```
/design-api

Design a GraphQL API for an e-commerce catalog with products,
categories, reviews, and real-time inventory updates
```

### Design gRPC API
```
/design-api

Design a gRPC API for a payment service with transaction processing,
refunds, and webhook notifications
```

## Best Practices Applied

- **RESTful**: Resource-oriented URLs, proper HTTP methods, HATEOAS
- **GraphQL**: Schema-first design, proper nullable fields, DataLoader pattern
- **gRPC**: Efficient Protocol Buffers, streaming for large data, proper error codes
- **All**: Comprehensive error handling, versioning, pagination, filtering
- **Security**: Defense in depth, least privilege, input validation
- **Documentation**: Clear examples, edge cases, migration guides

Provide actionable, production-ready API designs that can be implemented immediately.
