---
name: error-handling
description: Ensures consistent error handling across all endpoints
allowed-tools: Read, Grep, Edit
---

# Error Handling Skill

Automatically reviews and improves error handling in backend code.

## Pattern Detection

This skill automatically detects and enhances error handling patterns in your code.

### Error Categories

The skill ensures proper handling of these error types:

- **Validation Errors (400)**: Invalid input data
- **Authentication Errors (401)**: Missing or invalid credentials
- **Authorization Errors (403)**: Insufficient permissions
- **Not Found Errors (404)**: Resource doesn't exist
- **Conflict Errors (409)**: Resource state conflict
- **Server Errors (500)**: Internal server errors

## Automatic Enhancements

### Global Error Handler

Ensures a centralized error handler exists:

```javascript
// Express example
app.use((err, req, res, next) => {
  const status = err.status || 500;
  const message = err.message || 'Internal Server Error';

  res.status(status).json({
    error: {
      code: err.code || 'UNKNOWN_ERROR',
      message,
      timestamp: new Date().toISOString(),
      path: req.path,
      requestId: req.id
    }
  });
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
```

### Error Logging

Ensures errors are properly logged:

```python
# Automatically adds logging
except Exception as e:
    logger.error(f"Error in {__name__}: {str(e)}", exc_info=True)
    raise
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
        "message": "Invalid email format"
      }
    ],
    "timestamp": "2024-01-01T00:00:00Z",
    "requestId": "abc-123"
  }
}
```

## Improvements Suggested

- Add correlation IDs for tracing
- Implement error recovery strategies
- Add retry logic for transient failures
- Create custom error classes
- Implement circuit breakers
- Add error metrics and monitoring

This skill runs automatically when API endpoints are created or modified.