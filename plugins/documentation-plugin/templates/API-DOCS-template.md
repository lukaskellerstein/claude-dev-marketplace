# API Documentation

## Overview

Brief description of the API, its purpose, and key features.

**Base URL:** `https://api.example.com/v1`

**Version:** 1.0.0

**Protocol:** REST / GraphQL / gRPC

## Table of Contents

- [Authentication](#authentication)
- [Rate Limiting](#rate-limiting)
- [Error Handling](#error-handling)
- [Endpoints](#endpoints)
- [Data Models](#data-models)
- [Examples](#examples)
- [SDKs](#sdks)
- [Changelog](#changelog)

## Authentication

### Authentication Methods

This API supports the following authentication methods:

- **Bearer Token (JWT)**: Recommended for most use cases
- **API Key**: For server-to-server communication
- **OAuth 2.0**: For third-party applications

### Getting an Access Token

**Endpoint:** `POST /auth/token`

**Request:**
```bash
curl -X POST https://api.example.com/v1/auth/token \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123"
  }'
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "refresh_token": "refresh_token_here"
}
```

### Using the Access Token

Include the token in the Authorization header:

```bash
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  https://api.example.com/v1/users
```

### Refreshing Tokens

**Endpoint:** `POST /auth/refresh`

```bash
curl -X POST https://api.example.com/v1/auth/refresh \
  -H "Content-Type: application/json" \
  -d '{"refresh_token": "YOUR_REFRESH_TOKEN"}'
```

## Rate Limiting

### Limits

| Plan       | Requests/min | Requests/hour | Requests/day |
|------------|--------------|---------------|--------------|
| Free       | 20           | 1,000         | 10,000       |
| Basic      | 60           | 5,000         | 50,000       |
| Pro        | 300          | 30,000        | 500,000      |
| Enterprise | Custom       | Custom        | Custom       |

### Rate Limit Headers

All API responses include rate limit information:

```
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1640000000
```

### Rate Limit Exceeded

**Response (429 Too Many Requests):**
```json
{
  "error": "rate_limit_exceeded",
  "message": "Too many requests. Please retry after 60 seconds.",
  "retry_after": 60
}
```

## Error Handling

### Error Response Format

All errors follow this structure:

```json
{
  "error": "error_code",
  "message": "Human-readable error message",
  "details": [
    {
      "field": "email",
      "message": "Email is required"
    }
  ],
  "request_id": "req_abc123",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

### HTTP Status Codes

| Code | Description              | When It Occurs                    |
|------|--------------------------|-----------------------------------|
| 200  | OK                       | Request succeeded                 |
| 201  | Created                  | Resource created successfully     |
| 204  | No Content               | Request succeeded, no data        |
| 400  | Bad Request              | Invalid request data              |
| 401  | Unauthorized             | Missing or invalid authentication |
| 403  | Forbidden                | Insufficient permissions          |
| 404  | Not Found                | Resource not found                |
| 409  | Conflict                 | Resource conflict (e.g., duplicate) |
| 422  | Unprocessable Entity     | Validation error                  |
| 429  | Too Many Requests        | Rate limit exceeded               |
| 500  | Internal Server Error    | Server error                      |
| 503  | Service Unavailable      | Service temporarily unavailable   |

### Error Codes

| Code                 | Description                           |
|----------------------|---------------------------------------|
| `validation_error`   | Request validation failed             |
| `unauthorized`       | Invalid or missing authentication     |
| `forbidden`          | Insufficient permissions              |
| `not_found`          | Resource not found                    |
| `conflict`           | Resource already exists               |
| `rate_limit_exceeded`| Too many requests                     |
| `internal_error`     | Unexpected server error               |

## Endpoints

### Users

#### List Users

**GET** `/users`

Retrieve a paginated list of users.

**Query Parameters:**

| Parameter | Type   | Required | Default | Description           |
|-----------|--------|----------|---------|----------------------|
| limit     | number | No       | 20      | Items per page        |
| offset    | number | No       | 0       | Pagination offset     |
| sort      | string | No       | created_at | Sort field         |
| order     | string | No       | desc    | Sort order (asc/desc) |

**Example Request:**
```bash
curl -H "Authorization: Bearer TOKEN" \
  "https://api.example.com/v1/users?limit=10&offset=0"
```

**Response (200 OK):**
```json
{
  "data": [
    {
      "id": "usr_abc123",
      "email": "user@example.com",
      "name": "John Doe",
      "created_at": "2024-01-01T00:00:00Z"
    }
  ],
  "pagination": {
    "limit": 10,
    "offset": 0,
    "total": 100,
    "has_more": true
  }
}
```

#### Get User

**GET** `/users/{id}`

Retrieve a single user by ID.

**Path Parameters:**

| Parameter | Type   | Required | Description        |
|-----------|--------|----------|--------------------|
| id        | string | Yes      | User identifier    |

**Example Request:**
```bash
curl -H "Authorization: Bearer TOKEN" \
  https://api.example.com/v1/users/usr_abc123
```

**Response (200 OK):**
```json
{
  "id": "usr_abc123",
  "email": "user@example.com",
  "name": "John Doe",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

**Error (404 Not Found):**
```json
{
  "error": "not_found",
  "message": "User not found"
}
```

#### Create User

**POST** `/users`

Create a new user.

**Request Body:**
```json
{
  "email": "user@example.com",
  "name": "John Doe",
  "password": "SecurePassword123"
}
```

**Schema:**

| Field    | Type   | Required | Validation                |
|----------|--------|----------|---------------------------|
| email    | string | Yes      | Valid email format, unique |
| name     | string | Yes      | 1-100 characters          |
| password | string | Yes      | Min 8 characters          |

**Example Request:**
```bash
curl -X POST https://api.example.com/v1/users \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "name": "John Doe",
    "password": "SecurePassword123"
  }'
```

**Response (201 Created):**
```json
{
  "id": "usr_abc123",
  "email": "user@example.com",
  "name": "John Doe",
  "created_at": "2024-01-01T00:00:00Z"
}
```

**Error (400 Bad Request):**
```json
{
  "error": "validation_error",
  "message": "Validation failed",
  "details": [
    {
      "field": "email",
      "message": "Email is already registered"
    }
  ]
}
```

#### Update User

**PATCH** `/users/{id}`

Update an existing user.

**Request Body:**
```json
{
  "name": "Jane Doe",
  "email": "jane@example.com"
}
```

**Example Request:**
```bash
curl -X PATCH https://api.example.com/v1/users/usr_abc123 \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Jane Doe"}'
```

**Response (200 OK):**
```json
{
  "id": "usr_abc123",
  "email": "user@example.com",
  "name": "Jane Doe",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

#### Delete User

**DELETE** `/users/{id}`

Delete a user.

**Example Request:**
```bash
curl -X DELETE https://api.example.com/v1/users/usr_abc123 \
  -H "Authorization: Bearer TOKEN"
```

**Response (204 No Content)**

## Data Models

### User

```typescript
interface User {
  id: string;           // Unique identifier
  email: string;        // Email address (unique)
  name: string;         // Full name
  created_at: string;   // ISO 8601 timestamp
  updated_at: string;   // ISO 8601 timestamp
}
```

### Error

```typescript
interface Error {
  error: string;        // Error code
  message: string;      // Human-readable message
  details?: Array<{     // Optional validation details
    field: string;
    message: string;
  }>;
  request_id: string;   // Request identifier
  timestamp: string;    // ISO 8601 timestamp
}
```

## Examples

### Complete Example: User Management

```javascript
const API_BASE = 'https://api.example.com/v1';
let accessToken = '';

// 1. Authenticate
async function login() {
  const response = await fetch(`${API_BASE}/auth/token`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      email: 'user@example.com',
      password: 'password123'
    })
  });
  const data = await response.json();
  accessToken = data.access_token;
}

// 2. Create user
async function createUser() {
  const response = await fetch(`${API_BASE}/users`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${accessToken}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      email: 'new@example.com',
      name: 'New User',
      password: 'SecurePass123'
    })
  });
  return response.json();
}

// 3. List users
async function listUsers() {
  const response = await fetch(
    `${API_BASE}/users?limit=10&offset=0`,
    {
      headers: { 'Authorization': `Bearer ${accessToken}` }
    }
  );
  return response.json();
}

// Usage
await login();
const newUser = await createUser();
const users = await listUsers();
```

## SDKs

Official SDKs are available for:

- **JavaScript/TypeScript**: `npm install @example/api-client`
- **Python**: `pip install example-api`
- **Go**: `go get github.com/example/api-go`
- **Java**: Maven/Gradle package

## Changelog

### v1.0.0 (2024-01-01)
- Initial API release
- User management endpoints
- JWT authentication

See [full changelog](./CHANGELOG.md) for details.

## Support

- 📧 API Support: api@example.com
- 📖 Documentation: https://docs.example.com
- 🐛 Issues: https://github.com/example/api/issues
