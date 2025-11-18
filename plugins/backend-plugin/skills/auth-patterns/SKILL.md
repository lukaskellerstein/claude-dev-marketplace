---
name: auth-patterns
description: Master authentication and authorization patterns including JWT, OAuth2, session management, and RBAC for secure backend applications. Use when implementing JWT token generation, adding OAuth2 integration, configuring session storage, implementing role-based access control, adding rate limiting for auth endpoints, or securing password storage with bcrypt/argon2.
allowed-tools: Read, Write, Edit
---

# Authentication Patterns Skill

Automatically implements secure authentication and authorization patterns.

## When to Use This Skill

- Implementing JWT authentication with token generation and verification
- Adding OAuth2 integration (Google, GitHub, Microsoft)
- Configuring secure session management with Redis or database storage
- Implementing role-based access control (RBAC) or attribute-based access control (ABAC)
- Adding rate limiting to authentication endpoints to prevent brute force attacks
- Securing password storage with bcrypt, argon2, or scrypt
- Implementing multi-factor authentication (MFA/2FA)
- Adding API key authentication for service-to-service communication
- Implementing refresh token rotation for enhanced security
- Configuring security headers (CSP, HSTS, X-Frame-Options)
- Adding password reset functionality with secure tokens
- Implementing social login (Facebook, Twitter, LinkedIn)
- Adding IP whitelisting or geolocation-based access control
- Implementing single sign-on (SSO) with SAML or OpenID Connect
- Adding account lockout mechanisms after failed login attempts

## Quick Start

### Minimal JWT Authentication Example

```typescript
// Express.js with JWT authentication
import express from 'express';
import jwt from 'jsonwebtoken';
import bcrypt from 'bcrypt';

const app = express();
const JWT_SECRET = process.env.JWT_SECRET || 'your-secret-key';

interface TokenPayload {
  userId: string;
  email: string;
  role: string;
}

// Generate JWT token
function generateToken(user: TokenPayload): string {
  return jwt.sign(
    { userId: user.userId, email: user.email, role: user.role },
    JWT_SECRET,
    { expiresIn: '24h', issuer: 'your-app' }
  );
}

// Verify JWT token
function verifyToken(token: string): TokenPayload {
  return jwt.verify(token, JWT_SECRET) as TokenPayload;
}

// Authentication middleware
const authenticate = (req, res, next) => {
  const authHeader = req.headers.authorization;
  if (!authHeader?.startsWith('Bearer ')) {
    return res.status(401).json({ error: 'No token provided' });
  }

  const token = authHeader.substring(7);
  try {
    const decoded = verifyToken(token);
    req.user = decoded;
    next();
  } catch (error) {
    return res.status(401).json({ error: 'Invalid or expired token' });
  }
};

// Login endpoint
app.post('/auth/login', async (req, res) => {
  const { email, password } = req.body;

  const user = await User.findOne({ where: { email } });
  if (!user) {
    return res.status(401).json({ error: 'Invalid credentials' });
  }

  const validPassword = await bcrypt.compare(password, user.password);
  if (!validPassword) {
    return res.status(401).json({ error: 'Invalid credentials' });
  }

  const token = generateToken({
    userId: user.id,
    email: user.email,
    role: user.role
  });

  res.json({ token, user: { id: user.id, email: user.email, role: user.role } });
});

// Protected route
app.get('/api/profile', authenticate, (req, res) => {
  res.json({ user: req.user });
});
```

## JWT Implementation

Automatically adds JWT authentication when detected:

```typescript
// Comprehensive JWT implementation
import jwt from 'jsonwebtoken';
import crypto from 'crypto';

const JWT_SECRET = process.env.JWT_SECRET;
const JWT_REFRESH_SECRET = process.env.JWT_REFRESH_SECRET;
const ACCESS_TOKEN_EXPIRY = '15m';
const REFRESH_TOKEN_EXPIRY = '7d';

interface TokenPair {
  accessToken: string;
  refreshToken: string;
}

// Generate access and refresh tokens
const generateTokenPair = (user: User): TokenPair => {
  const accessToken = jwt.sign(
    {
      userId: user.id,
      email: user.email,
      role: user.role,
      type: 'access'
    },
    JWT_SECRET,
    {
      expiresIn: ACCESS_TOKEN_EXPIRY,
      issuer: 'your-app',
      audience: 'your-app-api'
    }
  );

  const refreshToken = jwt.sign(
    {
      userId: user.id,
      type: 'refresh',
      jti: crypto.randomUUID() // Unique token ID for revocation
    },
    JWT_REFRESH_SECRET,
    {
      expiresIn: REFRESH_TOKEN_EXPIRY,
      issuer: 'your-app'
    }
  );

  return { accessToken, refreshToken };
};

// Verify access token
const verifyAccessToken = (token: string): any => {
  try {
    const decoded = jwt.verify(token, JWT_SECRET, {
      issuer: 'your-app',
      audience: 'your-app-api'
    });

    if (decoded.type !== 'access') {
      throw new Error('Invalid token type');
    }

    return decoded;
  } catch (error) {
    throw new Error('Invalid or expired access token');
  }
};

// Refresh token endpoint
app.post('/auth/refresh', async (req, res) => {
  const { refreshToken } = req.body;

  try {
    const decoded = jwt.verify(refreshToken, JWT_REFRESH_SECRET) as any;

    // Check if token is revoked
    const isRevoked = await RefreshToken.findOne({
      where: { jti: decoded.jti, revoked: true }
    });

    if (isRevoked) {
      return res.status(401).json({ error: 'Token has been revoked' });
    }

    // Get user
    const user = await User.findByPk(decoded.userId);
    if (!user) {
      return res.status(401).json({ error: 'User not found' });
    }

    // Generate new token pair
    const newTokens = generateTokenPair(user);

    // Revoke old refresh token
    await RefreshToken.update(
      { revoked: true },
      { where: { jti: decoded.jti } }
    );

    // Store new refresh token
    await RefreshToken.create({
      jti: jwt.decode(newTokens.refreshToken).jti,
      userId: user.id,
      expiresAt: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000)
    });

    res.json(newTokens);
  } catch (error) {
    res.status(401).json({ error: 'Invalid refresh token' });
  }
});

// Middleware with role check
const authorize = (...allowedRoles: string[]) => {
  return (req, res, next) => {
    const token = req.headers.authorization?.split(' ')[1];

    if (!token) {
      return res.status(401).json({ error: 'No token provided' });
    }

    try {
      const decoded = verifyAccessToken(token);
      req.user = decoded;

      if (allowedRoles.length && !allowedRoles.includes(decoded.role)) {
        return res.status(403).json({ error: 'Insufficient permissions' });
      }

      next();
    } catch (error) {
      return res.status(401).json({ error: error.message });
    }
  };
};

// Usage
app.get('/admin/users', authorize('admin', 'superadmin'), async (req, res) => {
  const users = await User.findAll();
  res.json(users);
});
```

## Session Management

Implements secure session handling:

```python
# Flask with Redis session management
from flask import Flask, session, request
from flask_session import Session
from redis import Redis
import secrets
import hashlib
from datetime import timedelta

app = Flask(__name__)

# Secure session configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_KEY_PREFIX'] = 'session:'
app.config['SESSION_REDIS'] = Redis(
    host=os.getenv('REDIS_HOST'),
    port=6379,
    password=os.getenv('REDIS_PASSWORD'),
    db=0,
    decode_responses=True
)

# Cookie security
app.config['SESSION_COOKIE_SECURE'] = True  # HTTPS only
app.config['SESSION_COOKIE_HTTPONLY'] = True  # No JavaScript access
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # CSRF protection
app.config['SESSION_COOKIE_NAME'] = '__Secure-session'

Session(app)

# Login with session
@app.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if not user or not bcrypt.check_password_hash(user.password, password):
        return jsonify({'error': 'Invalid credentials'}), 401

    # Create session
    session.clear()
    session['user_id'] = user.id
    session['email'] = user.email
    session['role'] = user.role
    session['login_time'] = datetime.utcnow().isoformat()
    session['ip_address'] = request.remote_addr
    session.permanent = True

    # Track active session
    session_id = session.sid
    redis_client.setex(
        f'active_session:{user.id}',
        86400,
        session_id
    )

    return jsonify({
        'message': 'Login successful',
        'user': {'id': user.id, 'email': user.email, 'role': user.role}
    })

# Session middleware
@app.before_request
def check_session():
    if request.endpoint in ['login', 'register', 'static']:
        return

    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401

    # Check session validity
    user_id = session['user_id']
    active_session = redis_client.get(f'active_session:{user_id}')

    if not active_session or active_session != session.sid:
        session.clear()
        return jsonify({'error': 'Session expired or invalid'}), 401

    # Extend session on activity
    redis_client.expire(f'active_session:{user_id}', 86400)

# Logout
@app.route('/auth/logout', methods=['POST'])
def logout():
    user_id = session.get('user_id')
    if user_id:
        redis_client.delete(f'active_session:{user_id}')
    session.clear()
    return jsonify({'message': 'Logged out successfully'})
```

## OAuth 2.0 Integration

Adds OAuth support when needed:

```typescript
// OAuth 2.0 with Passport.js
import passport from 'passport';
import { Strategy as GoogleStrategy } from 'passport-google-oauth20';
import { Strategy as GitHubStrategy } from 'passport-github2';

// Google OAuth configuration
passport.use(new GoogleStrategy({
    clientID: process.env.GOOGLE_CLIENT_ID,
    clientSecret: process.env.GOOGLE_CLIENT_SECRET,
    callbackURL: '/auth/google/callback',
    scope: ['profile', 'email']
  },
  async (accessToken, refreshToken, profile, done) => {
    try {
      // Find or create user
      let user = await User.findOne({
        where: { googleId: profile.id }
      });

      if (!user) {
        user = await User.create({
          googleId: profile.id,
          email: profile.emails[0].value,
          name: profile.displayName,
          avatar: profile.photos[0]?.value,
          provider: 'google'
        });
      }

      // Update last login
      await user.update({ lastLogin: new Date() });

      done(null, user);
    } catch (error) {
      done(error, null);
    }
  }
));

// GitHub OAuth configuration
passport.use(new GitHubStrategy({
    clientID: process.env.GITHUB_CLIENT_ID,
    clientSecret: process.env.GITHUB_CLIENT_SECRET,
    callbackURL: '/auth/github/callback',
    scope: ['user:email']
  },
  async (accessToken, refreshToken, profile, done) => {
    try {
      let user = await User.findOne({
        where: { githubId: profile.id }
      });

      if (!user) {
        user = await User.create({
          githubId: profile.id,
          email: profile.emails[0].value,
          name: profile.displayName || profile.username,
          avatar: profile.photos[0]?.value,
          provider: 'github'
        });
      }

      await user.update({ lastLogin: new Date() });
      done(null, user);
    } catch (error) {
      done(error, null);
    }
  }
));

// OAuth routes
app.get('/auth/google', passport.authenticate('google'));

app.get('/auth/google/callback',
  passport.authenticate('google', { session: false }),
  (req, res) => {
    const token = generateToken(req.user);
    res.redirect(`${process.env.FRONTEND_URL}/auth/callback?token=${token}`);
  }
);

app.get('/auth/github', passport.authenticate('github'));

app.get('/auth/github/callback',
  passport.authenticate('github', { session: false }),
  (req, res) => {
    const token = generateToken(req.user);
    res.redirect(`${process.env.FRONTEND_URL}/auth/callback?token=${token}`);
  }
);
```

## Security Headers

Automatically adds security headers:

```javascript
// Helmet for Express with comprehensive configuration
import helmet from 'helmet';

app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      styleSrc: ["'self'", "'unsafe-inline'", "https://fonts.googleapis.com"],
      scriptSrc: ["'self'", "https://apis.google.com"],
      imgSrc: ["'self'", "data:", "https:"],
      connectSrc: ["'self'", "https://api.example.com"],
      fontSrc: ["'self'", "https://fonts.gstatic.com"],
      objectSrc: ["'none'"],
      mediaSrc: ["'self'"],
      frameSrc: ["'none'"],
    },
  },
  hsts: {
    maxAge: 31536000, // 1 year
    includeSubDomains: true,
    preload: true,
  },
  frameguard: {
    action: 'deny' // Prevent clickjacking
  },
  noSniff: true, // Prevent MIME sniffing
  xssFilter: true, // Enable XSS filter
  referrerPolicy: {
    policy: 'strict-origin-when-cross-origin'
  }
}));

// Additional security headers
app.use((req, res, next) => {
  res.setHeader('Permissions-Policy', 'geolocation=(), microphone=(), camera=()');
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.setHeader('X-Frame-Options', 'DENY');
  res.setHeader('X-XSS-Protection', '1; mode=block');
  next();
});
```

## Rate Limiting

Implements rate limiting for authentication endpoints:

```typescript
import rateLimit from 'express-rate-limit';
import RedisStore from 'rate-limit-redis';
import { Redis } from 'ioredis';

const redis = new Redis(process.env.REDIS_URL);

// Strict rate limit for login attempts
const loginLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 5, // 5 attempts
  message: {
    error: 'Too many login attempts',
    retryAfter: '15 minutes'
  },
  standardHeaders: true,
  legacyHeaders: false,
  store: new RedisStore({
    client: redis,
    prefix: 'rate_limit:login:'
  }),
  skip: (req) => {
    // Skip rate limiting for whitelisted IPs
    const whitelistedIPs = process.env.WHITELISTED_IPS?.split(',') || [];
    return whitelistedIPs.includes(req.ip);
  }
});

// Moderate rate limit for registration
const registerLimiter = rateLimit({
  windowMs: 60 * 60 * 1000, // 1 hour
  max: 3, // 3 registrations
  message: 'Too many accounts created from this IP',
  store: new RedisStore({
    client: redis,
    prefix: 'rate_limit:register:'
  })
});

// Strict rate limit for password reset
const passwordResetLimiter = rateLimit({
  windowMs: 60 * 60 * 1000, // 1 hour
  max: 3, // 3 reset attempts
  message: 'Too many password reset attempts',
  store: new RedisStore({
    client: redis,
    prefix: 'rate_limit:password_reset:'
  })
});

app.post('/auth/login', loginLimiter, loginHandler);
app.post('/auth/register', registerLimiter, registerHandler);
app.post('/auth/password-reset', passwordResetLimiter, passwordResetHandler);

// Account lockout after failed attempts
const MAX_FAILED_ATTEMPTS = 5;
const LOCKOUT_DURATION = 30 * 60 * 1000; // 30 minutes

async function checkAccountLockout(userId: string): Promise<boolean> {
  const lockoutKey = `account_lockout:${userId}`;
  const failedKey = `failed_attempts:${userId}`;

  const isLocked = await redis.get(lockoutKey);
  if (isLocked) {
    return true;
  }

  return false;
}

async function recordFailedAttempt(userId: string): Promise<void> {
  const failedKey = `failed_attempts:${userId}`;
  const attempts = await redis.incr(failedKey);

  if (attempts === 1) {
    await redis.expire(failedKey, 3600); // Expire after 1 hour
  }

  if (attempts >= MAX_FAILED_ATTEMPTS) {
    const lockoutKey = `account_lockout:${userId}`;
    await redis.setex(lockoutKey, LOCKOUT_DURATION / 1000, '1');
    await redis.del(failedKey);

    // Send email notification
    await sendEmail(user.email, 'Account Locked', 'Your account has been locked due to multiple failed login attempts.');
  }
}

async function clearFailedAttempts(userId: string): Promise<void> {
  await redis.del(`failed_attempts:${userId}`);
}
```

## Password Security

Ensures secure password handling:

```typescript
import bcrypt from 'bcrypt';
import { z } from 'zod';

const SALT_ROUNDS = 12;

// Strong password validation
const passwordSchema = z.string()
  .min(8, 'Password must be at least 8 characters')
  .max(128, 'Password must not exceed 128 characters')
  .regex(/[a-z]/, 'Password must contain at least one lowercase letter')
  .regex(/[A-Z]/, 'Password must contain at least one uppercase letter')
  .regex(/[0-9]/, 'Password must contain at least one number')
  .regex(/[^a-zA-Z0-9]/, 'Password must contain at least one special character');

// Hash password
async function hashPassword(password: string): Promise<string> {
  // Validate password strength
  passwordSchema.parse(password);

  // Check against common passwords
  const isCommon = await checkCommonPassword(password);
  if (isCommon) {
    throw new Error('Password is too common, please choose a stronger password');
  }

  return bcrypt.hash(password, SALT_ROUNDS);
}

// Verify password
async function verifyPassword(password: string, hash: string): Promise<boolean> {
  return bcrypt.compare(password, hash);
}

// Password history (prevent reuse)
async function checkPasswordHistory(userId: string, newPassword: string): Promise<boolean> {
  const passwordHistory = await PasswordHistory.findAll({
    where: { userId },
    order: [['createdAt', 'DESC']],
    limit: 5 // Check last 5 passwords
  });

  for (const record of passwordHistory) {
    const matches = await bcrypt.compare(newPassword, record.passwordHash);
    if (matches) {
      return true; // Password was used before
    }
  }

  return false;
}

// Password reset with secure tokens
async function requestPasswordReset(email: string): Promise<void> {
  const user = await User.findOne({ where: { email } });
  if (!user) {
    // Don't reveal if email exists
    return;
  }

  // Generate secure random token
  const resetToken = crypto.randomBytes(32).toString('hex');
  const resetTokenHash = crypto.createHash('sha256').update(resetToken).digest('hex');

  // Store hashed token
  await user.update({
    resetTokenHash,
    resetTokenExpiry: new Date(Date.now() + 60 * 60 * 1000) // 1 hour
  });

  // Send email with reset link
  const resetUrl = `${process.env.FRONTEND_URL}/reset-password?token=${resetToken}`;
  await sendEmail(user.email, 'Password Reset', `Reset your password: ${resetUrl}`);
}

// Reset password
async function resetPassword(token: string, newPassword: string): Promise<void> {
  const tokenHash = crypto.createHash('sha256').update(token).digest('hex');

  const user = await User.findOne({
    where: {
      resetTokenHash: tokenHash,
      resetTokenExpiry: { [Op.gt]: new Date() }
    }
  });

  if (!user) {
    throw new Error('Invalid or expired reset token');
  }

  // Check password history
  const wasUsedBefore = await checkPasswordHistory(user.id, newPassword);
  if (wasUsedBefore) {
    throw new Error('Cannot reuse recent passwords');
  }

  // Hash new password
  const passwordHash = await hashPassword(newPassword);

  // Update user
  await user.update({
    password: passwordHash,
    resetTokenHash: null,
    resetTokenExpiry: null
  });

  // Store in password history
  await PasswordHistory.create({
    userId: user.id,
    passwordHash
  });

  // Revoke all active sessions
  await redis.del(`active_session:${user.id}`);
}
```

## Authorization Patterns

Implements role-based access control:

```python
# FastAPI with RBAC
from functools import wraps
from enum import Enum
from typing import List

class Role(str, Enum):
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"
    SUPERADMIN = "superadmin"

class Permission(str, Enum):
    READ_USERS = "read:users"
    WRITE_USERS = "write:users"
    DELETE_USERS = "delete:users"
    READ_POSTS = "read:posts"
    WRITE_POSTS = "write:posts"
    DELETE_POSTS = "delete:posts"

# Role-permission mapping
ROLE_PERMISSIONS = {
    Role.USER: [Permission.READ_POSTS, Permission.WRITE_POSTS],
    Role.MODERATOR: [
        Permission.READ_POSTS,
        Permission.WRITE_POSTS,
        Permission.DELETE_POSTS,
        Permission.READ_USERS
    ],
    Role.ADMIN: [
        Permission.READ_POSTS,
        Permission.WRITE_POSTS,
        Permission.DELETE_POSTS,
        Permission.READ_USERS,
        Permission.WRITE_USERS,
        Permission.DELETE_USERS
    ]
}

def require_role(*allowed_roles: Role):
    """Decorator to check if user has required role"""
    def decorator(f):
        @wraps(f)
        async def decorated_function(current_user: User = Depends(get_current_user), *args, **kwargs):
            if current_user.role not in allowed_roles:
                raise HTTPException(
                    status_code=403,
                    detail=f"Requires one of roles: {', '.join(allowed_roles)}"
                )
            return await f(current_user, *args, **kwargs)
        return decorated_function
    return decorator

def require_permission(*required_permissions: Permission):
    """Decorator to check if user has required permissions"""
    def decorator(f):
        @wraps(f)
        async def decorated_function(current_user: User = Depends(get_current_user), *args, **kwargs):
            user_permissions = ROLE_PERMISSIONS.get(current_user.role, [])

            for perm in required_permissions:
                if perm not in user_permissions:
                    raise HTTPException(
                        status_code=403,
                        detail=f"Missing required permission: {perm}"
                    )

            return await f(current_user, *args, **kwargs)
        return decorated_function
    return decorator

# Usage examples
@app.get("/admin/users")
@require_role(Role.ADMIN, Role.SUPERADMIN)
async def get_all_users(current_user: User):
    return await User.find_all()

@app.delete("/posts/{post_id}")
@require_permission(Permission.DELETE_POSTS)
async def delete_post(post_id: int, current_user: User):
    post = await Post.find_by_id(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    # Check ownership or moderator
    if post.author_id != current_user.id and current_user.role not in [Role.MODERATOR, Role.ADMIN]:
        raise HTTPException(status_code=403, detail="Cannot delete other users' posts")

    await post.delete()
    return {"message": "Post deleted successfully"}
```

## Real-World Applications

### Multi-Factor Authentication (MFA)

```typescript
// TOTP-based MFA implementation
import speakeasy from 'speakeasy';
import QRCode from 'qrcode';

// Enable MFA for user
app.post('/auth/mfa/enable', authenticate, async (req, res) => {
  const user = await User.findByPk(req.user.userId);

  // Generate secret
  const secret = speakeasy.generateSecret({
    name: `YourApp (${user.email})`,
    issuer: 'YourApp'
  });

  // Generate QR code
  const qrCode = await QRCode.toDataURL(secret.otpauth_url);

  // Store secret (encrypted)
  await user.update({
    mfaSecret: encrypt(secret.base32),
    mfaEnabled: false // Not enabled until verified
  });

  res.json({
    secret: secret.base32,
    qrCode
  });
});

// Verify and activate MFA
app.post('/auth/mfa/verify', authenticate, async (req, res) => {
  const { token } = req.body;
  const user = await User.findByPk(req.user.userId);

  const secret = decrypt(user.mfaSecret);
  const verified = speakeasy.totp.verify({
    secret,
    encoding: 'base32',
    token,
    window: 2 // Allow 2 time steps before/after
  });

  if (!verified) {
    return res.status(400).json({ error: 'Invalid MFA token' });
  }

  // Generate backup codes
  const backupCodes = Array.from({ length: 10 }, () =>
    crypto.randomBytes(4).toString('hex').toUpperCase()
  );

  await user.update({
    mfaEnabled: true,
    mfaBackupCodes: backupCodes.map(code => bcrypt.hashSync(code, 10))
  });

  res.json({
    message: 'MFA enabled successfully',
    backupCodes // Show once, user should save them
  });
});

// Login with MFA
app.post('/auth/login/mfa', async (req, res) => {
  const { email, password, mfaToken } = req.body;

  const user = await User.findOne({ where: { email } });
  if (!user || !await bcrypt.compare(password, user.password)) {
    return res.status(401).json({ error: 'Invalid credentials' });
  }

  if (!user.mfaEnabled) {
    return res.status(400).json({ error: 'MFA not enabled' });
  }

  const secret = decrypt(user.mfaSecret);
  const verified = speakeasy.totp.verify({
    secret,
    encoding: 'base32',
    token: mfaToken,
    window: 2
  });

  if (!verified) {
    // Check backup codes
    const backupCodeValid = user.mfaBackupCodes.some(hash =>
      bcrypt.compareSync(mfaToken, hash)
    );

    if (!backupCodeValid) {
      return res.status(401).json({ error: 'Invalid MFA token' });
    }

    // Remove used backup code
    await user.update({
      mfaBackupCodes: user.mfaBackupCodes.filter(hash =>
        !bcrypt.compareSync(mfaToken, hash)
      )
    });
  }

  const tokens = generateTokenPair(user);
  res.json(tokens);
});
```

## Best Practices Summary

- **Never store passwords in plain text** - Always use bcrypt, argon2, or scrypt
- **Use HTTPS everywhere** - Encrypt all traffic with TLS/SSL
- **Implement rate limiting** - Prevent brute force attacks
- **Use secure session storage** - Redis or database, not client-side
- **Validate all inputs** - Prevent injection attacks
- **Use secure random tokens** - For password reset, MFA, etc.
- **Implement account lockout** - After failed login attempts
- **Log security events** - Track authentication failures, lockouts
- **Use security headers** - CSP, HSTS, X-Frame-Options
- **Implement token rotation** - Refresh tokens should be rotated

## Common Pitfalls

### Pitfall 1: Weak Password Storage
```javascript
// ❌ Bad: Plain text or weak hashing
user.password = md5(password);

// ✅ Good: bcrypt with proper salt rounds
user.password = await bcrypt.hash(password, 12);
```

### Pitfall 2: Insecure Token Storage
```javascript
// ❌ Bad: Store tokens in localStorage (XSS vulnerable)
localStorage.setItem('token', accessToken);

// ✅ Good: Use httpOnly cookies
res.cookie('accessToken', token, {
  httpOnly: true,
  secure: true,
  sameSite: 'strict',
  maxAge: 15 * 60 * 1000
});
```

### Pitfall 3: Missing Rate Limiting
```python
# ❌ Bad: No protection against brute force
@app.post("/login")
async def login(credentials: LoginData):
    # Direct authentication without limits

# ✅ Good: Rate limiting on authentication
@app.post("/login")
@limiter.limit("5/15minutes")
async def login(credentials: LoginData):
    # Protected authentication
```

## Related Skills

- **api-best-practices**: Ensures proper HTTP methods and status codes
- **error-handling**: Handles authentication and authorization errors
- **validation-rules**: Validates authentication inputs
- **security-headers**: Implements comprehensive security headers

This skill automatically applies when authentication is detected in the codebase.
