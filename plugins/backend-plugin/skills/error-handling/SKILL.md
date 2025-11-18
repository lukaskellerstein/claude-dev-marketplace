---
name: error-handling
description: Master consistent error handling patterns across Node.js, Python, Go, and Java backends. Use when implementing global error handlers, adding try-catch blocks, creating custom error classes, logging errors with structured formats, implementing retry logic, or ensuring proper error responses for REST/GraphQL APIs.
allowed-tools: Read, Grep, Edit
---

# Error Handling Skill

Automatically reviews and improves error handling in backend code.

## When to Use This Skill

- Implementing global error handlers in Express, FastAPI, or Spring Boot
- Adding comprehensive try-catch blocks to async/await functions
- Creating custom error classes with specific error codes
- Implementing structured error logging with Winston, Bunyan, or Loguru
- Adding retry logic for transient failures (network, database timeouts)
- Implementing circuit breakers for external service calls
- Ensuring consistent error response formats across all endpoints
- Adding error tracking integration (Sentry, Rollbar, DataDog)
- Implementing graceful degradation for non-critical failures
- Adding correlation IDs for distributed tracing
- Handling validation errors with detailed field-level messages
- Implementing error recovery strategies for critical operations
- Adding error metrics and monitoring dashboards
- Handling database transaction rollbacks on errors
- Implementing proper error propagation in microservices

## Quick Start

### Minimal Error Handling Example

```typescript
// Express.js with comprehensive error handling
import express, { Request, Response, NextFunction } from 'express';

// Custom error class
class AppError extends Error {
  constructor(
    public statusCode: number,
    public code: string,
    message: string,
    public isOperational = true
  ) {
    super(message);
    Error.captureStackTrace(this, this.constructor);
  }
}

// Global error handler
app.use((err: Error, req: Request, res: Response, next: NextFunction) => {
  if (err instanceof AppError) {
    return res.status(err.statusCode).json({
      error: {
        code: err.code,
        message: err.message,
        timestamp: new Date().toISOString(),
        path: req.path
      }
    });
  }

  // Unexpected error
  console.error('Unexpected error:', err);
  res.status(500).json({
    error: {
      code: 'INTERNAL_ERROR',
      message: 'An unexpected error occurred'
    }
  });
});

// Usage in route
app.get('/users/:id', async (req, res, next) => {
  try {
    const user = await User.findByPk(req.params.id);
    if (!user) {
      throw new AppError(404, 'USER_NOT_FOUND', 'User not found');
    }
    res.json(user);
  } catch (error) {
    next(error);
  }
});
```

## Pattern Detection

This skill automatically detects and enhances error handling patterns in your code.

### Error Categories

The skill ensures proper handling of these error types:

- **Validation Errors (400)**: Invalid input data, schema violations
- **Authentication Errors (401)**: Missing or invalid credentials, expired tokens
- **Authorization Errors (403)**: Insufficient permissions, role mismatch
- **Not Found Errors (404)**: Resource doesn't exist, invalid ID
- **Conflict Errors (409)**: Resource state conflict, duplicate entries
- **Unprocessable Entity (422)**: Semantic errors, business logic violations
- **Too Many Requests (429)**: Rate limit exceeded
- **Server Errors (500)**: Internal server errors, uncaught exceptions
- **Service Unavailable (503)**: Database down, external service timeout
- **Gateway Timeout (504)**: Upstream service timeout

## Automatic Enhancements

### Global Error Handler

Ensures a centralized error handler exists:

```javascript
// Express example with detailed error handling
app.use((err, req, res, next) => {
  const status = err.status || 500;
  const message = err.message || 'Internal Server Error';

  // Log error with context
  logger.error({
    error: {
      message: err.message,
      stack: err.stack,
      code: err.code
    },
    request: {
      method: req.method,
      url: req.url,
      headers: req.headers,
      body: req.body,
      ip: req.ip
    },
    timestamp: new Date().toISOString()
  });

  // Don't expose stack traces in production
  const response = {
    error: {
      code: err.code || 'UNKNOWN_ERROR',
      message,
      timestamp: new Date().toISOString(),
      path: req.path,
      requestId: req.id
    }
  };

  if (process.env.NODE_ENV === 'development') {
    response.error.stack = err.stack;
  }

  res.status(status).json(response);
});
```

### Try-Catch Blocks

Adds missing try-catch blocks:

```typescript
// Before
async function handler(req, res) {
  const user = await userService.create(req.body);
  res.json(user);
}

// After (automatically enhanced)
async function handler(req, res, next) {
  try {
    const user = await userService.create(req.body);
    res.json(user);
  } catch (error) {
    next(error);
  }
}

// Even better: async error wrapper
const asyncHandler = (fn) => (req, res, next) => {
  Promise.resolve(fn(req, res, next)).catch(next);
};

// Usage
app.get('/users', asyncHandler(async (req, res) => {
  const users = await userService.getAll();
  res.json(users);
}));
```

### Error Logging

Ensures errors are properly logged:

```python
# Python with structured logging
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(
        "Unhandled exception",
        extra={
            "error": {
                "type": type(exc).__name__,
                "message": str(exc),
                "traceback": traceback.format_exc()
            },
            "request": {
                "method": request.method,
                "url": str(request.url),
                "client": request.client.host
            },
            "timestamp": datetime.utcnow().isoformat()
        },
        exc_info=True
    )

    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "An internal error occurred",
                "timestamp": datetime.utcnow().isoformat()
            }
        }
    )
```

## Real-World Applications

### Application 1: Microservice Error Handling with Retry Logic

```typescript
// Resilient external service calls with retries
import axios, { AxiosError } from 'axios';

class ExternalServiceError extends Error {
  constructor(
    public service: string,
    public statusCode: number,
    message: string,
    public retryable: boolean = false
  ) {
    super(message);
  }
}

async function callExternalService<T>(
  url: string,
  options: {
    maxRetries?: number;
    retryDelay?: number;
    timeout?: number;
  } = {}
): Promise<T> {
  const { maxRetries = 3, retryDelay = 1000, timeout = 5000 } = options;
  let lastError: Error;

  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      const response = await axios.get<T>(url, {
        timeout,
        headers: { 'X-Request-ID': generateRequestId() }
      });

      // Log successful call
      logger.info({
        message: 'External service call succeeded',
        service: url,
        attempt,
        duration: response.headers['x-response-time']
      });

      return response.data;
    } catch (error) {
      lastError = error as Error;

      if (axios.isAxiosError(error)) {
        const axiosError = error as AxiosError;
        const statusCode = axiosError.response?.status || 0;

        // Determine if error is retryable
        const retryableStatuses = [408, 429, 500, 502, 503, 504];
        const isRetryable = retryableStatuses.includes(statusCode) ||
                           error.code === 'ECONNABORTED' ||
                           error.code === 'ETIMEDOUT';

        // Log attempt
        logger.warn({
          message: 'External service call failed',
          service: url,
          attempt,
          maxRetries,
          statusCode,
          errorCode: error.code,
          isRetryable,
          willRetry: attempt < maxRetries && isRetryable
        });

        // Don't retry if error is not retryable or max retries reached
        if (!isRetryable || attempt >= maxRetries) {
          throw new ExternalServiceError(
            url,
            statusCode,
            `External service failed: ${error.message}`,
            isRetryable
          );
        }

        // Exponential backoff
        const delay = retryDelay * Math.pow(2, attempt - 1);
        await new Promise(resolve => setTimeout(resolve, delay));
      } else {
        throw error;
      }
    }
  }

  throw lastError!;
}

// Circuit breaker implementation
class CircuitBreaker {
  private failures = 0;
  private lastFailTime = 0;
  private state: 'CLOSED' | 'OPEN' | 'HALF_OPEN' = 'CLOSED';

  constructor(
    private threshold: number = 5,
    private timeout: number = 60000,
    private resetTimeout: number = 30000
  ) {}

  async call<T>(fn: () => Promise<T>): Promise<T> {
    if (this.state === 'OPEN') {
      if (Date.now() - this.lastFailTime > this.resetTimeout) {
        this.state = 'HALF_OPEN';
      } else {
        throw new Error('Circuit breaker is OPEN');
      }
    }

    try {
      const result = await fn();
      this.onSuccess();
      return result;
    } catch (error) {
      this.onFailure();
      throw error;
    }
  }

  private onSuccess() {
    this.failures = 0;
    this.state = 'CLOSED';
  }

  private onFailure() {
    this.failures++;
    this.lastFailTime = Date.now();

    if (this.failures >= this.threshold) {
      this.state = 'OPEN';
      logger.error({
        message: 'Circuit breaker opened',
        failures: this.failures,
        threshold: this.threshold
      });
    }
  }
}
```

### Application 2: Database Transaction Error Handling

```python
# FastAPI with database transaction management
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, OperationalError
from contextlib import contextmanager
import logging

logger = logging.getLogger(__name__)

class DatabaseError(Exception):
    def __init__(self, message: str, original_error: Exception = None):
        self.message = message
        self.original_error = original_error
        super().__init__(self.message)

@contextmanager
def transaction_scope(db: Session):
    """Context manager for database transactions with automatic rollback."""
    try:
        yield db
        db.commit()
        logger.info("Transaction committed successfully")
    except IntegrityError as e:
        db.rollback()
        logger.error(f"Integrity error, transaction rolled back: {str(e)}")
        raise HTTPException(
            status_code=409,
            detail={
                "code": "DUPLICATE_ENTRY",
                "message": "Resource already exists",
                "field": extract_field_from_error(e)
            }
        )
    except OperationalError as e:
        db.rollback()
        logger.error(f"Database operational error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=503,
            detail={
                "code": "DATABASE_UNAVAILABLE",
                "message": "Database service is temporarily unavailable"
            }
        )
    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error, transaction rolled back: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail={
                "code": "TRANSACTION_ERROR",
                "message": "Failed to complete database transaction"
            }
        )

@app.post("/users")
async def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    with transaction_scope(db):
        # Check if user exists
        existing = db.query(User).filter(User.email == user_data.email).first()
        if existing:
            raise HTTPException(
                status_code=409,
                detail={
                    "code": "USER_EXISTS",
                    "message": "User with this email already exists",
                    "field": "email"
                }
            )

        # Create user
        user = User(**user_data.dict())
        db.add(user)
        db.flush()  # Get ID without committing

        # Create related records
        profile = UserProfile(user_id=user.id)
        db.add(profile)

        # Transaction auto-commits if no exception

    logger.info(f"User created successfully: {user.id}")
    return user
```

### Application 3: GraphQL Error Handling

```typescript
// Apollo Server with custom error handling
import { ApolloServer, ApolloError } from '@apollo/server';
import { GraphQLError } from 'graphql';

// Custom error classes
class ValidationError extends ApolloError {
  constructor(message: string, fields?: Record<string, string>) {
    super(message, 'VALIDATION_ERROR', { fields });
  }
}

class AuthenticationError extends ApolloError {
  constructor(message: string = 'Not authenticated') {
    super(message, 'UNAUTHENTICATED');
  }
}

class AuthorizationError extends ApolloError {
  constructor(message: string = 'Not authorized') {
    super(message, 'FORBIDDEN');
  }
}

const server = new ApolloServer({
  typeDefs,
  resolvers,
  formatError: (formattedError, error) => {
    // Log all errors
    logger.error({
      message: formattedError.message,
      code: formattedError.extensions?.code,
      path: formattedError.path,
      locations: formattedError.locations,
      stacktrace: error instanceof Error ? error.stack : undefined
    });

    // Don't expose internal errors
    if (formattedError.extensions?.code === 'INTERNAL_SERVER_ERROR') {
      return {
        message: 'An internal error occurred',
        extensions: {
          code: 'INTERNAL_SERVER_ERROR',
          timestamp: new Date().toISOString()
        }
      };
    }

    // Add timestamp to all errors
    return {
      ...formattedError,
      extensions: {
        ...formattedError.extensions,
        timestamp: new Date().toISOString()
      }
    };
  },
  plugins: [
    {
      async requestDidStart() {
        return {
          async didEncounterErrors(requestContext) {
            // Send errors to monitoring service
            requestContext.errors?.forEach(error => {
              if (!(error instanceof ApolloError)) {
                // Unexpected error - send to Sentry
                Sentry.captureException(error, {
                  contexts: {
                    graphql: {
                      query: requestContext.request.query,
                      variables: requestContext.request.variables,
                      operationName: requestContext.request.operationName
                    }
                  }
                });
              }
            });
          }
        };
      }
    }
  ]
});

// Resolver with error handling
const resolvers = {
  Mutation: {
    createPost: async (_, { input }, { user, dataSources }) => {
      // Authentication check
      if (!user) {
        throw new AuthenticationError();
      }

      // Authorization check
      if (!user.permissions.includes('CREATE_POST')) {
        throw new AuthorizationError('You do not have permission to create posts');
      }

      // Validation
      const validationErrors: Record<string, string> = {};
      if (!input.title || input.title.length < 5) {
        validationErrors.title = 'Title must be at least 5 characters';
      }
      if (!input.content || input.content.length < 10) {
        validationErrors.content = 'Content must be at least 10 characters';
      }
      if (Object.keys(validationErrors).length > 0) {
        throw new ValidationError('Validation failed', validationErrors);
      }

      try {
        return await dataSources.posts.create({
          ...input,
          authorId: user.id
        });
      } catch (error) {
        if (error.code === '23505') { // Unique constraint violation
          throw new ValidationError('A post with this title already exists', {
            title: 'Must be unique'
          });
        }
        throw error;
      }
    }
  }
};
```

## Error Response Format

Enforces consistent error response structure:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Validation failed",
    "details": [
      {
        "field": "email",
        "message": "Invalid email format",
        "value": "invalid-email"
      },
      {
        "field": "age",
        "message": "Must be at least 18",
        "value": 15
      }
    ],
    "timestamp": "2024-01-01T00:00:00Z",
    "requestId": "abc-123-def-456",
    "path": "/api/v1/users"
  }
}
```

## Best Practices Summary

### Error Classification
- **Operational Errors**: Expected errors that should be handled (validation, not found)
- **Programmer Errors**: Bugs that should crash the application (syntax errors, null references)

### Error Handling Strategy
1. **Catch operational errors** and return appropriate HTTP responses
2. **Let programmer errors crash** and restart the application
3. **Log everything** with proper context and severity
4. **Monitor error rates** and set up alerts
5. **Use correlation IDs** for distributed tracing

### Custom Error Classes
```typescript
class BaseError extends Error {
  constructor(
    public statusCode: number,
    public code: string,
    message: string,
    public isOperational = true
  ) {
    super(message);
    Error.captureStackTrace(this, this.constructor);
  }
}

class NotFoundError extends BaseError {
  constructor(resource: string) {
    super(404, 'NOT_FOUND', `${resource} not found`);
  }
}

class ValidationError extends BaseError {
  constructor(message: string, public fields?: Record<string, string>) {
    super(400, 'VALIDATION_ERROR', message);
  }
}
```

## Common Pitfalls

### Pitfall 1: Swallowing Errors
```javascript
// ❌ Bad: Error is silently ignored
try {
  await riskyOperation();
} catch (error) {
  // Do nothing
}

// ✅ Good: Error is logged and re-thrown
try {
  await riskyOperation();
} catch (error) {
  logger.error('Operation failed', { error });
  throw error;
}
```

### Pitfall 2: Exposing Sensitive Information
```python
# ❌ Bad: Exposes database details
except Exception as e:
    return {"error": str(e)}  # May expose SQL, file paths, etc.

# ✅ Good: Generic message for client, detailed log for developers
except Exception as e:
    logger.error(f"Database error: {str(e)}", exc_info=True)
    raise HTTPException(status_code=500, detail="Internal server error")
```

### Pitfall 3: Not Using Error Codes
```typescript
// ❌ Bad: Only human-readable message
throw new Error('User not found');

// ✅ Good: Machine-readable code + human message
throw new AppError(404, 'USER_NOT_FOUND', 'User not found');
```

## Improvements Suggested

- Add correlation IDs for tracing requests across services
- Implement error recovery strategies (fallbacks, defaults)
- Add retry logic for transient failures (exponential backoff)
- Create custom error classes for different error types
- Implement circuit breakers for external service calls
- Add error metrics and monitoring (Prometheus, DataDog)
- Set up error tracking (Sentry, Rollbar)
- Implement graceful shutdown on critical errors
- Add error rate limiting to prevent abuse
- Implement dead letter queues for failed messages

## Related Skills

- **api-best-practices**: Ensures proper HTTP status codes and error responses
- **validation-rules**: Validates input to prevent validation errors
- **auth-patterns**: Handles authentication and authorization errors
- **logging-monitoring**: Implements structured logging for errors

This skill runs automatically when API endpoints are created or modified.
