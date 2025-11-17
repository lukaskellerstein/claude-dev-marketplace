---
name: auth-patterns
description: Implements authentication and authorization patterns
allowed-tools: Read, Write, Edit
---

# Authentication Patterns Skill

Automatically implements secure authentication and authorization patterns.

## JWT Implementation

Automatically adds JWT authentication when detected:

```typescript
// Automatic JWT setup
import jwt from 'jsonwebtoken';

const generateToken = (user: User): string => {
  return jwt.sign(
    { id: user.id, email: user.email },
    process.env.JWT_SECRET,
    { expiresIn: '24h' }
  );
};

const verifyToken = (token: string): any => {
  return jwt.verify(token, process.env.JWT_SECRET);
};

// Middleware
const authMiddleware = (req, res, next) => {
  const token = req.headers.authorization?.split(' ')[1];

  if (!token) {
    return res.status(401).json({ error: 'No token provided' });
  }

  try {
    const decoded = verifyToken(token);
    req.user = decoded;
    next();
  } catch (error) {
    return res.status(401).json({ error: 'Invalid token' });
  }
};
```

## Session Management

Implements secure session handling:

```python
# Automatic session configuration
from flask import Flask, session
from flask_session import Session

app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_KEY_PREFIX'] = 'myapp:'
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
```

## OAuth 2.0 Integration

Adds OAuth support when needed:

```go
// OAuth middleware
func OAuthMiddleware() gin.HandlerFunc {
    return func(c *gin.Context) {
        token := c.GetHeader("Authorization")

        // Validate OAuth token
        claims, err := validateOAuthToken(token)
        if err != nil {
            c.JSON(401, gin.H{"error": "Invalid OAuth token"})
            c.Abort()
            return
        }

        c.Set("user", claims)
        c.Next()
    }
}
```

## Security Headers

Automatically adds security headers:

```javascript
// Helmet for Express
app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      styleSrc: ["'self'", "'unsafe-inline'"],
      scriptSrc: ["'self'"],
      imgSrc: ["'self'", "data:", "https:"],
    },
  },
  hsts: {
    maxAge: 31536000,
    includeSubDomains: true,
    preload: true,
  },
}));
```

## Rate Limiting

Implements rate limiting for authentication endpoints:

```typescript
import rateLimit from 'express-rate-limit';

const loginLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 5, // 5 requests
  message: 'Too many login attempts',
  standardHeaders: true,
  legacyHeaders: false,
});

app.post('/login', loginLimiter, loginHandler);
```

## Password Security

Ensures secure password handling:

- Uses bcrypt or argon2 for hashing
- Enforces minimum password requirements
- Implements password reset tokens
- Adds password history checking

## Authorization Patterns

Implements role-based access control:

```python
def require_role(*allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.role in allowed_roles:
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@app.route('/admin')
@require_role('admin', 'superuser')
def admin_panel():
    return render_template('admin.html')
```

This skill automatically applies when authentication is detected in the codebase.