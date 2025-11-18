---
name: api-best-practices
description: Master RESTful API design, GraphQL implementation, and HTTP best practices for production-ready backends. Use when designing REST endpoints, implementing GraphQL APIs, adding pagination, configuring rate limiting, optimizing API performance, or ensuring API security standards.
allowed-tools: Read, Grep, Glob
---

# API Best Practices Skill

This skill automatically activates when working on API endpoints to ensure best practices are followed.

## When to Use This Skill

- Designing new REST API endpoints with proper HTTP methods and status codes
- Implementing GraphQL schemas and resolvers with type safety
- Adding pagination, filtering, and sorting to list endpoints
- Configuring rate limiting and throttling for API protection
- Implementing versioning strategies (URL, header, or content negotiation)
- Optimizing API performance with caching (ETag, Cache-Control headers)
- Ensuring consistent error response formats across endpoints
- Adding CORS configuration for cross-origin requests
- Implementing HATEOAS (Hypermedia as the Engine of Application State)
- Setting up OpenAPI/Swagger documentation
- Preventing N+1 query problems in database operations
- Adding request/response compression (gzip, brotli)
- Implementing proper authentication middleware (JWT, OAuth2)
- Configuring connection pooling for database efficiency
- Adding API monitoring and metrics collection

## Quick Start

### Minimal REST API Example

```typescript
// Express.js REST API with best practices
import express from 'express';
import helmet from 'helmet';
import rateLimit from 'express-rate-limit';
import compression from 'compression';

const app = express();

// Security middleware
app.use(helmet());
app.use(express.json({ limit: '10mb' }));
app.use(compression());

// Rate limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // limit each IP to 100 requests per windowMs
  message: 'Too many requests from this IP'
});
app.use('/api/', limiter);

// Example endpoint with pagination
app.get('/api/v1/users', async (req, res) => {
  try {
    const page = parseInt(req.query.page) || 1;
    const limit = Math.min(parseInt(req.query.limit) || 20, 100);
    const offset = (page - 1) * limit;

    const users = await User.findAndCountAll({ limit, offset });

    res.json({
      data: users.rows,
      pagination: {
        page,
        limit,
        total: users.count,
        totalPages: Math.ceil(users.count / limit)
      }
    });
  } catch (error) {
    res.status(500).json({
      error: {
        code: 'INTERNAL_ERROR',
        message: 'Failed to fetch users'
      }
    });
  }
});

app.listen(3000);
```

## Automatic Checks

### REST API Standards
- ✅ Proper HTTP methods (GET for read, POST for create, PUT for update, DELETE for remove)
- ✅ Consistent resource naming (plural nouns for collections)
- ✅ Appropriate status codes (200 OK, 201 Created, 204 No Content, 400 Bad Request, 401 Unauthorized, 404 Not Found)
- ✅ Pagination implemented for list endpoints
- ✅ Filtering and sorting parameters supported
- ✅ Consistent error response format
- ✅ Idempotent operations for PUT and DELETE
- ✅ Proper use of PATCH for partial updates

### Security Checks
- ✅ Authentication middleware present
- ✅ Authorization checks for protected resources
- ✅ Input validation on all endpoints
- ✅ SQL injection prevention (parameterized queries)
- ✅ Rate limiting configured
- ✅ CORS properly configured
- ✅ Sensitive data not exposed in responses
- ✅ HTTPS enforcement in production
- ✅ API keys securely managed
- ✅ XSS and CSRF protection enabled

### Performance Optimization
- ✅ Database query optimization (N+1 query prevention)
- ✅ Proper caching headers (ETag, Cache-Control)
- ✅ Response compression enabled (gzip/brotli)
- ✅ Connection pooling configured
- ✅ Async operations for I/O
- ✅ Pagination limits enforced
- ✅ Query result caching (Redis/Memcached)
- ✅ Database indexes on frequently queried fields
- ✅ Lazy loading for large datasets
- ✅ CDN integration for static assets

### Documentation Requirements
- ✅ OpenAPI/Swagger specification exists
- ✅ Request/response examples provided
- ✅ Error codes documented
- ✅ Authentication methods described
- ✅ Rate limits documented
- ✅ Versioning strategy explained
- ✅ Deprecation notices included

## Real-World Applications

### Application 1: E-commerce Product API

```typescript
// Comprehensive product listing endpoint
import { Request, Response } from 'express';
import { Redis } from 'ioredis';

const redis = new Redis();

interface ProductQuery {
  page?: number;
  limit?: number;
  category?: string;
  minPrice?: number;
  maxPrice?: number;
  sortBy?: 'price' | 'name' | 'createdAt';
  order?: 'asc' | 'desc';
}

app.get('/api/v1/products', async (req: Request, res: Response) => {
  try {
    const {
      page = 1,
      limit = 20,
      category,
      minPrice,
      maxPrice,
      sortBy = 'createdAt',
      order = 'desc'
    } = req.query as unknown as ProductQuery;

    // Validate pagination
    const validatedLimit = Math.min(Number(limit), 100);
    const offset = (Number(page) - 1) * validatedLimit;

    // Build cache key
    const cacheKey = `products:${JSON.stringify(req.query)}`;

    // Check cache
    const cached = await redis.get(cacheKey);
    if (cached) {
      return res.json(JSON.parse(cached));
    }

    // Build query
    const where: any = {};
    if (category) where.category = category;
    if (minPrice) where.price = { ...where.price, gte: Number(minPrice) };
    if (maxPrice) where.price = { ...where.price, lte: Number(maxPrice) };

    // Execute query
    const [products, total] = await Promise.all([
      Product.findAll({
        where,
        limit: validatedLimit,
        offset,
        order: [[sortBy, order.toUpperCase()]]
      }),
      Product.count({ where })
    ]);

    const response = {
      data: products,
      pagination: {
        page: Number(page),
        limit: validatedLimit,
        total,
        totalPages: Math.ceil(total / validatedLimit),
        hasNext: offset + validatedLimit < total,
        hasPrev: Number(page) > 1
      },
      links: {
        self: `/api/v1/products?page=${page}&limit=${limit}`,
        next: offset + validatedLimit < total
          ? `/api/v1/products?page=${Number(page) + 1}&limit=${limit}`
          : null,
        prev: Number(page) > 1
          ? `/api/v1/products?page=${Number(page) - 1}&limit=${limit}`
          : null
      }
    };

    // Cache for 5 minutes
    await redis.setex(cacheKey, 300, JSON.stringify(response));

    // Set cache headers
    res.setHeader('Cache-Control', 'public, max-age=300');
    res.setHeader('ETag', `W/"${Buffer.from(JSON.stringify(response)).toString('base64')}"`);

    res.json(response);
  } catch (error) {
    console.error('Product fetch error:', error);
    res.status(500).json({
      error: {
        code: 'PRODUCT_FETCH_ERROR',
        message: 'Failed to retrieve products'
      }
    });
  }
});
```

### Application 2: GraphQL API with Best Practices

```typescript
// GraphQL implementation with proper patterns
import { ApolloServer } from '@apollo/server';
import { startStandaloneServer } from '@apollo/server/standalone';
import DataLoader from 'dataloader';

const typeDefs = `#graphql
  type User {
    id: ID!
    name: String!
    email: String!
    posts: [Post!]!
  }

  type Post {
    id: ID!
    title: String!
    content: String!
    author: User!
  }

  type Query {
    user(id: ID!): User
    users(page: Int, limit: Int): UserConnection!
  }

  type UserConnection {
    edges: [UserEdge!]!
    pageInfo: PageInfo!
  }

  type UserEdge {
    node: User!
    cursor: String!
  }

  type PageInfo {
    hasNextPage: Boolean!
    hasPreviousPage: Boolean!
    startCursor: String
    endCursor: String
  }
`;

// DataLoader to prevent N+1 queries
const createUserLoader = () => new DataLoader(async (userIds: readonly string[]) => {
  const users = await User.findAll({
    where: { id: { [Op.in]: userIds as string[] } }
  });

  const userMap = new Map(users.map(u => [u.id, u]));
  return userIds.map(id => userMap.get(id));
});

const createPostLoader = () => new DataLoader(async (userIds: readonly string[]) => {
  const posts = await Post.findAll({
    where: { userId: { [Op.in]: userIds as string[] } }
  });

  const postsByUser = new Map();
  posts.forEach(post => {
    if (!postsByUser.has(post.userId)) {
      postsByUser.set(post.userId, []);
    }
    postsByUser.get(post.userId).push(post);
  });

  return userIds.map(id => postsByUser.get(id) || []);
});

const resolvers = {
  Query: {
    user: async (_, { id }, { loaders }) => {
      return loaders.userLoader.load(id);
    },
    users: async (_, { page = 1, limit = 20 }) => {
      const validatedLimit = Math.min(limit, 100);
      const offset = (page - 1) * validatedLimit;

      const users = await User.findAll({
        limit: validatedLimit + 1, // Fetch one extra to check hasNextPage
        offset
      });

      const hasNextPage = users.length > validatedLimit;
      const edges = users.slice(0, validatedLimit).map((user, index) => ({
        node: user,
        cursor: Buffer.from(`${offset + index}`).toString('base64')
      }));

      return {
        edges,
        pageInfo: {
          hasNextPage,
          hasPreviousPage: page > 1,
          startCursor: edges[0]?.cursor,
          endCursor: edges[edges.length - 1]?.cursor
        }
      };
    }
  },
  User: {
    posts: async (user, _, { loaders }) => {
      return loaders.postLoader.load(user.id);
    }
  }
};

const server = new ApolloServer({
  typeDefs,
  resolvers,
  formatError: (error) => {
    console.error('GraphQL Error:', error);
    return {
      message: error.message,
      code: error.extensions?.code || 'INTERNAL_SERVER_ERROR',
      path: error.path
    };
  }
});

startStandaloneServer(server, {
  context: async () => ({
    loaders: {
      userLoader: createUserLoader(),
      postLoader: createPostLoader()
    }
  }),
  listen: { port: 4000 }
});
```

### Application 3: Versioned API with Deprecation

```python
# FastAPI versioned endpoints with deprecation handling
from fastapi import FastAPI, APIRouter, Header, HTTPException
from typing import Optional
from enum import Enum

app = FastAPI(title="Versioned API", version="2.0.0")

class APIVersion(str, Enum):
    V1 = "v1"
    V2 = "v2"

# V1 Router (deprecated)
v1_router = APIRouter(prefix="/api/v1", deprecated=True)

@v1_router.get("/users/{user_id}")
async def get_user_v1(user_id: int):
    """Deprecated: Use /api/v2/users/{user_id} instead"""
    return {
        "id": user_id,
        "name": "John Doe",
        "_deprecated": True,
        "_message": "This endpoint will be removed on 2024-12-31",
        "_migration_guide": "https://api.example.com/docs/v1-to-v2"
    }

# V2 Router (current)
v2_router = APIRouter(prefix="/api/v2")

@v2_router.get("/users/{user_id}")
async def get_user_v2(
    user_id: int,
    api_version: Optional[str] = Header(default="2.0.0", alias="X-API-Version")
):
    """Enhanced user endpoint with additional fields"""
    return {
        "id": user_id,
        "name": "John Doe",
        "email": "john@example.com",
        "created_at": "2024-01-01T00:00:00Z",
        "metadata": {
            "api_version": api_version
        }
    }

# Content negotiation based on Accept header
@app.get("/api/users/{user_id}")
async def get_user_negotiated(
    user_id: int,
    accept: Optional[str] = Header(default="application/vnd.api.v2+json")
):
    if "vnd.api.v1" in accept:
        return await get_user_v1(user_id)
    elif "vnd.api.v2" in accept:
        return await get_user_v2(user_id)
    else:
        raise HTTPException(
            status_code=406,
            detail="Acceptable content types: application/vnd.api.v1+json, application/vnd.api.v2+json"
        )

app.include_router(v1_router)
app.include_router(v2_router)
```

## Validation Rules

When this skill detects API endpoint creation or modification, it automatically:

1. **Checks naming conventions**: Ensures endpoints follow RESTful naming
2. **Validates HTTP methods**: Confirms appropriate method usage
3. **Reviews status codes**: Ensures correct HTTP status codes
4. **Inspects security**: Looks for authentication and validation
5. **Suggests improvements**: Provides recommendations for optimization
6. **Verifies idempotency**: Ensures PUT/DELETE operations are idempotent
7. **Checks versioning**: Validates API versioning strategy
8. **Reviews caching**: Ensures proper cache headers

## Common Issues Detected

- Missing input validation
- Incorrect HTTP status codes
- Missing error handling
- No pagination on list endpoints
- Exposed sensitive data (passwords, tokens, internal IDs)
- Missing authentication middleware
- SQL injection vulnerabilities
- N+1 query problems
- Missing rate limiting
- Improper CORS configuration
- Lack of API versioning
- Missing compression
- Inefficient database queries
- No request/response logging

## Best Practices Summary

### HTTP Method Usage
- **GET**: Retrieve resources (safe, cacheable, idempotent)
- **POST**: Create new resources (not idempotent)
- **PUT**: Replace entire resource (idempotent)
- **PATCH**: Partial resource update (idempotent)
- **DELETE**: Remove resource (idempotent)
- **HEAD**: Retrieve headers only (metadata check)
- **OPTIONS**: Check available methods (CORS preflight)

### Status Code Guidelines
- **2xx Success**: 200 OK, 201 Created, 202 Accepted, 204 No Content
- **3xx Redirection**: 301 Moved Permanently, 304 Not Modified
- **4xx Client Error**: 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 409 Conflict, 422 Unprocessable Entity, 429 Too Many Requests
- **5xx Server Error**: 500 Internal Server Error, 502 Bad Gateway, 503 Service Unavailable

### Resource Naming
- Use plural nouns: `/users`, `/products`, `/orders`
- Use hyphens for multi-word names: `/user-profiles`
- Avoid verbs in URLs: ❌ `/getUser`, ✅ `/users/{id}`
- Use nesting for relationships: `/users/{id}/posts`
- Keep URLs lowercase

### Pagination Patterns
- **Offset-based**: `?page=1&limit=20`
- **Cursor-based**: `?cursor=abc123&limit=20` (better for real-time data)
- **Keyset**: `?after_id=100&limit=20` (most efficient)

## Common Pitfalls

### Pitfall 1: Exposing Internal IDs
```javascript
// ❌ Bad: Exposes auto-increment IDs
app.get('/users/:id', async (req, res) => {
  const user = await User.findByPk(req.params.id);
  res.json(user);
});

// ✅ Good: Use UUIDs or obfuscated IDs
app.get('/users/:uuid', async (req, res) => {
  const user = await User.findOne({ where: { uuid: req.params.uuid } });
  res.json(user);
});
```

### Pitfall 2: Missing Pagination Limits
```python
# ❌ Bad: No limit enforcement
@app.get("/users")
async def get_users(limit: int = 20):
    return await User.find_all(limit=limit)

# ✅ Good: Enforce maximum limit
@app.get("/users")
async def get_users(limit: int = 20):
    validated_limit = min(limit, 100)
    return await User.find_all(limit=validated_limit)
```

### Pitfall 3: N+1 Query Problem
```typescript
// ❌ Bad: N+1 queries
app.get('/users', async (req, res) => {
  const users = await User.findAll();
  const usersWithPosts = await Promise.all(
    users.map(async user => ({
      ...user.toJSON(),
      posts: await Post.findAll({ where: { userId: user.id } })
    }))
  );
  res.json(usersWithPosts);
});

// ✅ Good: Eager loading
app.get('/users', async (req, res) => {
  const users = await User.findAll({
    include: [{ model: Post }]
  });
  res.json(users);
});
```

## Automatic Suggestions

When issues are detected, this skill will suggest:

- Adding validation middleware for input sanitization
- Implementing proper error responses with consistent format
- Adding pagination parameters (page, limit, cursor)
- Implementing caching strategies (Redis, in-memory)
- Adding rate limiting middleware
- Improving query performance (indexes, eager loading)
- Implementing API versioning (URL, header, or content negotiation)
- Adding compression middleware (gzip, brotli)
- Setting up monitoring and logging
- Implementing request tracing (correlation IDs)
- Adding health check endpoints
- Implementing circuit breakers for external services

## Related Skills

- **error-handling**: Ensures consistent error responses across all endpoints
- **auth-patterns**: Implements secure authentication and authorization
- **validation-rules**: Adds comprehensive input validation
- **database-optimization**: Optimizes database queries and indexing

## Additional Resources

- REST API Design Best Practices: https://restfulapi.net/
- GraphQL Best Practices: https://graphql.org/learn/best-practices/
- OpenAPI Specification: https://swagger.io/specification/
- HTTP Status Codes: https://httpstatuses.com/

This skill runs automatically and requires no manual invocation.
