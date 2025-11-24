---
name: api-best-practices
description: Auto-invoked when designing or implementing REST, GraphQL, or gRPC APIs to ensure best practices and consistency
allowed-tools: Read, Grep, Glob
---

# API Design Best Practices

This skill provides guidance on API design best practices across REST, GraphQL, and gRPC.

## When Active

This skill activates when you:
- Design new API endpoints or operations
- Modify existing API contracts
- Review API specifications
- Implement API handlers or resolvers
- Write API documentation

## REST API Best Practices

### Resource Design
- Use nouns for resources, not verbs
- Prefer plural resource names (`/users`, `/orders`)
- Use nested resources for relationships (`/users/{id}/orders`)
- Keep URLs shallow (max 3 levels)
- Use hyphens for multi-word resources (`/order-items`)

```
Good:
GET    /users/{id}
POST   /users
PUT    /users/{id}
DELETE /users/{id}
GET    /users/{id}/orders

Bad:
GET    /getUser/{id}
POST   /createUser
GET    /user/{id}
```

### HTTP Methods
- **GET**: Retrieve resource (idempotent, safe, cacheable)
- **POST**: Create resource (not idempotent)
- **PUT**: Replace entire resource (idempotent)
- **PATCH**: Partial update (not necessarily idempotent)
- **DELETE**: Remove resource (idempotent)

### Status Codes
Use appropriate HTTP status codes:
- **200 OK**: Successful GET, PUT, PATCH, DELETE
- **201 Created**: Successful POST
- **204 No Content**: Successful DELETE with no response body
- **400 Bad Request**: Invalid client input
- **401 Unauthorized**: Missing/invalid authentication
- **403 Forbidden**: Authenticated but not authorized
- **404 Not Found**: Resource doesn't exist
- **409 Conflict**: Resource conflict (e.g., duplicate)
- **422 Unprocessable Entity**: Validation errors
- **429 Too Many Requests**: Rate limit exceeded
- **500 Internal Server Error**: Server error
- **503 Service Unavailable**: Temporary unavailability

### Request/Response Format

```json
// Request body (POST/PUT/PATCH)
{
  "name": "John Doe",
  "email": "john@example.com",
  "role": "admin"
}

// Success response
{
  "id": "123",
  "name": "John Doe",
  "email": "john@example.com",
  "role": "admin",
  "createdAt": "2025-01-15T10:30:00Z",
  "updatedAt": "2025-01-15T10:30:00Z"
}

// Error response
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": [
      {
        "field": "email",
        "message": "Invalid email format"
      }
    ]
  }
}
```

### Pagination
Use cursor-based or offset-based pagination:

```
// Offset-based
GET /users?limit=20&offset=40

Response:
{
  "data": [...],
  "pagination": {
    "limit": 20,
    "offset": 40,
    "total": 150
  }
}

// Cursor-based (preferred for large datasets)
GET /users?limit=20&cursor=eyJpZCI6IjEyMyJ9

Response:
{
  "data": [...],
  "pagination": {
    "nextCursor": "eyJpZCI6IjE0MyJ9",
    "hasMore": true
  }
}
```

### Filtering and Sorting
```
GET /users?role=admin&status=active&sort=-createdAt,name
```

### Versioning
Choose one strategy consistently:
- **URI versioning**: `/v1/users` (most common)
- **Header versioning**: `Accept: application/vnd.api.v1+json`
- **Query parameter**: `/users?version=1` (not recommended)

## GraphQL Best Practices

### Schema Design
```graphql
# Use clear, descriptive names
type User {
  id: ID!
  name: String!
  email: String!
  createdAt: DateTime!

  # Relationships
  orders: [Order!]!

  # Computed fields
  fullName: String!
}

# Input types for mutations
input CreateUserInput {
  name: String!
  email: String!
  password: String!
}

# Mutations return useful data
type CreateUserPayload {
  user: User!
  errors: [UserError!]!
}

# Pagination with Relay Connection pattern
type UserConnection {
  edges: [UserEdge!]!
  pageInfo: PageInfo!
  totalCount: Int!
}

type UserEdge {
  node: User!
  cursor: String!
}
```

### Nullable vs Non-nullable
- Make fields nullable by default
- Use `!` only when field is guaranteed to exist
- Lists: `[Type!]!` means non-null list of non-null items
- Avoid making input fields required unless truly mandatory

### Mutations
```graphql
# Clear naming with verb + noun
mutation {
  createUser(input: $input) {
    user {
      id
      name
    }
    errors {
      field
      message
    }
  }
}
```

### Error Handling
```graphql
type UserError {
  field: String
  message: String!
  code: ErrorCode!
}

enum ErrorCode {
  VALIDATION_ERROR
  UNAUTHORIZED
  NOT_FOUND
  INTERNAL_ERROR
}
```

### N+1 Query Problem
Use DataLoader to batch and cache database queries:

```javascript
const userLoader = new DataLoader(async (userIds) => {
  const users = await db.users.findMany({
    where: { id: { in: userIds } }
  });
  return userIds.map(id => users.find(u => u.id === id));
});
```

## gRPC Best Practices

### Service Definition
```protobuf
syntax = "proto3";

package user.v1;

// Service definition
service UserService {
  // Unary RPC
  rpc GetUser(GetUserRequest) returns (GetUserResponse);

  // Server streaming
  rpc ListUsers(ListUsersRequest) returns (stream User);

  // Client streaming
  rpc CreateUsers(stream CreateUserRequest) returns (CreateUsersResponse);

  // Bidirectional streaming
  rpc Chat(stream ChatMessage) returns (stream ChatMessage);
}

// Message definitions
message GetUserRequest {
  string user_id = 1;
}

message GetUserResponse {
  User user = 1;
}

message User {
  string id = 1;
  string name = 2;
  string email = 3;
  google.protobuf.Timestamp created_at = 4;
}
```

### Message Design
- Use snake_case for field names
- Number fields sequentially starting from 1
- Use well-known types (Timestamp, Duration, Empty)
- Use `oneof` for variant fields
- Use `repeated` for lists
- Reserve field numbers for future use

### Error Handling
```protobuf
// Use standard gRPC status codes
// OK, CANCELLED, INVALID_ARGUMENT, DEADLINE_EXCEEDED,
// NOT_FOUND, ALREADY_EXISTS, PERMISSION_DENIED, etc.

// Include error details in metadata
message ErrorDetails {
  string code = 1;
  string message = 2;
  map<string, string> metadata = 3;
}
```

### Streaming Patterns
- **Unary**: Single request, single response
- **Server streaming**: Single request, stream of responses (e.g., large result set)
- **Client streaming**: Stream of requests, single response (e.g., bulk upload)
- **Bidirectional**: Stream both ways (e.g., chat)

## Common Best Practices (All APIs)

### Authentication
- Use Bearer tokens (JWT) in Authorization header
- Include token expiration and refresh mechanism
- Validate tokens on every request
- Use HTTPS in production

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

### Rate Limiting
- Implement per-user or per-IP rate limits
- Return 429 status code when exceeded
- Include rate limit headers:
  ```
  X-RateLimit-Limit: 1000
  X-RateLimit-Remaining: 999
  X-RateLimit-Reset: 1672531200
  ```

### CORS
- Configure appropriate CORS headers
- Whitelist allowed origins
- Handle preflight OPTIONS requests

### Documentation
- REST: OpenAPI/Swagger specification
- GraphQL: Schema descriptions and examples
- gRPC: Protobuf comments and documentation

### Versioning & Deprecation
- Never break existing clients without warning
- Use deprecation notices and sunset periods
- Maintain backward compatibility when possible
- Provide migration guides

## Checklist

When designing/implementing APIs:
- [ ] Is the API contract clear and well-documented?
- [ ] Are HTTP methods/operations used correctly?
- [ ] Are status codes/errors appropriate and informative?
- [ ] Is authentication and authorization implemented?
- [ ] Is input validation comprehensive?
- [ ] Is pagination implemented for list operations?
- [ ] Are rate limits configured?
- [ ] Is the API versioned?
- [ ] Are error messages helpful for debugging?
- [ ] Is the API tested (unit, integration, contract tests)?
- [ ] Is monitoring and logging configured?
- [ ] Is the API documented (OpenAPI, GraphQL schema, .proto)?

Use this guidance to ensure APIs are consistent, well-designed, and production-ready.
