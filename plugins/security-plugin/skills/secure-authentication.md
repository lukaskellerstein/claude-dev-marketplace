---
name: secure-authentication
description: Auto-invoked when implementing authentication, password handling, session management, or authorization to ensure secure practices
allowed-tools: Read, Grep, Glob
---

# Secure Authentication & Authorization

This skill provides guidance on implementing secure authentication and authorization systems.

## When Active

This skill activates when you:
- Implement user registration or login
- Handle passwords or credentials
- Implement session management
- Use JWT or OAuth tokens
- Implement authorization checks
- Design role-based access control (RBAC)
- Implement multi-factor authentication (MFA)
- Handle API key authentication

## Password Security

### Password Hashing (ALWAYS)

```javascript
const bcrypt = require('bcrypt');

// NEVER STORE PLAIN TEXT PASSWORDS
// BAD - Plain text
const user = { password: userPassword }; // NEVER DO THIS

// BAD - Simple hashing (reversible)
const user = { password: md5(userPassword) }; // INSECURE

// BAD - SHA without salt
const user = { password: sha256(userPassword) }; // INSECURE

// GOOD - bcrypt with automatic salt
async function hashPassword(password) {
  const saltRounds = 12; // Higher = more secure but slower
  return await bcrypt.hash(password, saltRounds);
}

async function verifyPassword(password, hash) {
  return await bcrypt.compare(password, hash);
}

// GOOD - Argon2 (even better than bcrypt)
const argon2 = require('argon2');

async function hashPassword(password) {
  return await argon2.hash(password, {
    type: argon2.argon2id,
    memoryCost: 65536, // 64 MB
    timeCost: 3,
    parallelism: 4
  });
}

async function verifyPassword(password, hash) {
  return await argon2.verify(hash, password);
}
```

### Password Policies

```javascript
// Enforce strong password requirements
function validatePassword(password) {
  const errors = [];

  // Minimum length
  if (password.length < 8) {
    errors.push('Password must be at least 8 characters');
  }

  // Maximum length (prevent DoS)
  if (password.length > 128) {
    errors.push('Password must be less than 128 characters');
  }

  // Require uppercase
  if (!/[A-Z]/.test(password)) {
    errors.push('Password must contain an uppercase letter');
  }

  // Require lowercase
  if (!/[a-z]/.test(password)) {
    errors.push('Password must contain a lowercase letter');
  }

  // Require number
  if (!/\d/.test(password)) {
    errors.push('Password must contain a number');
  }

  // Require special character
  if (!/[!@#$%^&*(),.?":{}|<>]/.test(password)) {
    errors.push('Password must contain a special character');
  }

  // Check against common passwords
  const commonPasswords = [
    'password', '12345678', 'qwerty', 'abc123',
    'monkey', '1234567', 'letmein', 'trustno1'
  ];
  if (commonPasswords.includes(password.toLowerCase())) {
    errors.push('Password is too common');
  }

  return errors;
}

// Check password against Have I Been Pwned
const crypto = require('crypto');
const axios = require('axios');

async function checkPwnedPassword(password) {
  const sha1 = crypto.createHash('sha1').update(password).digest('hex').toUpperCase();
  const prefix = sha1.substring(0, 5);
  const suffix = sha1.substring(5);

  const response = await axios.get(`https://api.pwnedpasswords.com/range/${prefix}`);
  const hashes = response.data.split('\n');

  for (const line of hashes) {
    const [hash, count] = line.split(':');
    if (hash === suffix) {
      return parseInt(count, 10); // Number of times password appeared in breaches
    }
  }

  return 0; // Password not found in breaches
}
```

### Secure Registration Flow

```javascript
const { body, validationResult } = require('express-validator');
const rateLimit = require('express-rate-limit');

// Rate limit registration to prevent abuse
const registrationLimiter = rateLimit({
  windowMs: 60 * 60 * 1000, // 1 hour
  max: 5, // 5 registrations per hour per IP
  message: 'Too many registration attempts, please try again later'
});

// Validation rules
const validateRegistration = [
  body('email')
    .isEmail()
    .normalizeEmail()
    .withMessage('Invalid email address'),

  body('password')
    .isLength({ min: 8, max: 128 })
    .matches(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])/)
    .withMessage('Password must meet requirements'),

  body('username')
    .isLength({ min: 3, max: 30 })
    .matches(/^[a-zA-Z0-9_-]+$/)
    .withMessage('Invalid username'),
];

app.post('/register',
  registrationLimiter,
  validateRegistration,
  async (req, res) => {
    try {
      const errors = validationResult(req);
      if (!errors.isEmpty()) {
        return res.status(400).json({ errors: errors.array() });
      }

      const { email, password, username } = req.body;

      // Check if user already exists
      const existingUser = await User.findOne({ email });
      if (existingUser) {
        return res.status(409).json({
          error: 'Email already registered'
        });
      }

      // Check password against pwned database
      const pwnedCount = await checkPwnedPassword(password);
      if (pwnedCount > 0) {
        return res.status(400).json({
          error: 'This password has been exposed in data breaches. Please choose a different password.'
        });
      }

      // Hash password
      const hashedPassword = await bcrypt.hash(password, 12);

      // Create user
      const user = await User.create({
        email,
        username,
        password: hashedPassword,
        verified: false
      });

      // Send verification email
      await sendVerificationEmail(user.email, user.verificationToken);

      // Don't return sensitive data
      res.status(201).json({
        message: 'Registration successful. Please check your email to verify your account.',
        userId: user.id
      });

    } catch (error) {
      logger.error('Registration error', { error: error.message });
      res.status(500).json({ error: 'Registration failed' });
    }
  }
);
```

## Session Management

### Secure Session Configuration

```javascript
const session = require('express-session');
const RedisStore = require('connect-redis').default;
const redis = require('redis');

// Create Redis client for session storage
const redisClient = redis.createClient({
  host: process.env.REDIS_HOST,
  port: process.env.REDIS_PORT,
  password: process.env.REDIS_PASSWORD,
});

app.use(session({
  store: new RedisStore({ client: redisClient }),
  secret: process.env.SESSION_SECRET, // Strong random secret
  name: 'sessionId', // Don't use default name (hides tech stack)
  resave: false,
  saveUninitialized: false,
  cookie: {
    secure: true, // HTTPS only
    httpOnly: true, // Not accessible via JavaScript
    sameSite: 'strict', // CSRF protection
    maxAge: 1000 * 60 * 60 * 2, // 2 hours
    domain: process.env.COOKIE_DOMAIN
  },
  rolling: true, // Reset expiration on each request
}));

// Session timeout middleware
app.use((req, res, next) => {
  if (req.session && req.session.user) {
    // Check for session timeout
    const now = Date.now();
    const lastActivity = req.session.lastActivity || now;
    const timeout = 30 * 60 * 1000; // 30 minutes

    if (now - lastActivity > timeout) {
      req.session.destroy();
      return res.status(401).json({ error: 'Session expired' });
    }

    req.session.lastActivity = now;
  }
  next();
});
```

### Login with Account Lockout

```javascript
const loginLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 5, // 5 failed attempts
  skipSuccessfulRequests: true, // Don't count successful logins
  message: 'Too many login attempts, please try again later'
});

app.post('/login',
  loginLimiter,
  [
    body('email').isEmail().normalizeEmail(),
    body('password').notEmpty(),
  ],
  async (req, res) => {
    try {
      const errors = validationResult(req);
      if (!errors.isEmpty()) {
        return res.status(400).json({ errors: errors.array() });
      }

      const { email, password } = req.body;

      // Find user
      const user = await User.findOne({ email });
      if (!user) {
        // Generic error message (don't reveal if user exists)
        return res.status(401).json({
          error: 'Invalid credentials'
        });
      }

      // Check if account is locked
      if (user.lockUntil && user.lockUntil > Date.now()) {
        const minutesLeft = Math.ceil((user.lockUntil - Date.now()) / 60000);
        return res.status(423).json({
          error: `Account locked. Try again in ${minutesLeft} minutes.`
        });
      }

      // Verify password
      const isValid = await bcrypt.compare(password, user.password);

      if (!isValid) {
        // Increment failed attempts
        user.failedLoginAttempts = (user.failedLoginAttempts || 0) + 1;

        // Lock account after 5 failed attempts
        if (user.failedLoginAttempts >= 5) {
          user.lockUntil = Date.now() + (30 * 60 * 1000); // Lock for 30 minutes
          await user.save();

          // Alert security team
          logger.warn('Account locked due to failed login attempts', {
            userId: user.id,
            email: user.email
          });

          return res.status(423).json({
            error: 'Account locked due to too many failed login attempts'
          });
        }

        await user.save();

        return res.status(401).json({
          error: 'Invalid credentials'
        });
      }

      // Reset failed attempts on successful login
      user.failedLoginAttempts = 0;
      user.lockUntil = null;
      user.lastLogin = new Date();
      await user.save();

      // Create session
      req.session.user = {
        id: user.id,
        email: user.email,
        role: user.role
      };

      // Log successful login
      logger.info('User logged in', {
        userId: user.id,
        ip: req.ip,
        userAgent: req.get('user-agent')
      });

      res.json({
        message: 'Login successful',
        user: {
          id: user.id,
          email: user.email,
          username: user.username,
          role: user.role
        }
      });

    } catch (error) {
      logger.error('Login error', { error: error.message });
      res.status(500).json({ error: 'Login failed' });
    }
  }
);
```

## JWT Authentication

### Secure JWT Implementation

```javascript
const jwt = require('jsonwebtoken');
const crypto = require('crypto');

// Generate JWT with secure options
function generateAccessToken(user) {
  return jwt.sign(
    {
      userId: user.id,
      email: user.email,
      role: user.role
    },
    process.env.JWT_SECRET,
    {
      expiresIn: '15m', // Short-lived access token
      issuer: 'myapp',
      audience: 'myapp-users',
      algorithm: 'HS256'
    }
  );
}

// Generate refresh token
function generateRefreshToken(user) {
  const token = crypto.randomBytes(64).toString('hex');

  // Store in database with expiration
  RefreshToken.create({
    userId: user.id,
    token,
    expiresAt: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000) // 7 days
  });

  return token;
}

// Verify JWT middleware
function authenticateToken(req, res, next) {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1]; // Bearer TOKEN

  if (!token) {
    return res.status(401).json({ error: 'Access token required' });
  }

  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET, {
      issuer: 'myapp',
      audience: 'myapp-users',
      algorithms: ['HS256']
    });

    req.user = decoded;
    next();
  } catch (error) {
    if (error.name === 'TokenExpiredError') {
      return res.status(401).json({ error: 'Token expired' });
    }
    if (error.name === 'JsonWebTokenError') {
      return res.status(403).json({ error: 'Invalid token' });
    }
    res.status(500).json({ error: 'Authentication failed' });
  }
}

// Refresh token endpoint
app.post('/refresh', async (req, res) => {
  const { refreshToken } = req.body;

  if (!refreshToken) {
    return res.status(401).json({ error: 'Refresh token required' });
  }

  try {
    // Find refresh token in database
    const storedToken = await RefreshToken.findOne({
      token: refreshToken,
      expiresAt: { $gt: new Date() }
    });

    if (!storedToken) {
      return res.status(403).json({ error: 'Invalid or expired refresh token' });
    }

    // Get user
    const user = await User.findById(storedToken.userId);
    if (!user) {
      return res.status(403).json({ error: 'User not found' });
    }

    // Generate new access token
    const accessToken = generateAccessToken(user);

    res.json({ accessToken });

  } catch (error) {
    logger.error('Token refresh error', { error: error.message });
    res.status(500).json({ error: 'Token refresh failed' });
  }
});

// Logout endpoint (invalidate refresh token)
app.post('/logout', authenticateToken, async (req, res) => {
  const { refreshToken } = req.body;

  try {
    // Delete refresh token
    await RefreshToken.deleteOne({ token: refreshToken });

    res.json({ message: 'Logout successful' });
  } catch (error) {
    logger.error('Logout error', { error: error.message });
    res.status(500).json({ error: 'Logout failed' });
  }
});
```

## Authorization

### Role-Based Access Control (RBAC)

```javascript
// Define roles and permissions
const ROLES = {
  ADMIN: 'admin',
  MODERATOR: 'moderator',
  USER: 'user'
};

const PERMISSIONS = {
  USER_CREATE: 'user:create',
  USER_READ: 'user:read',
  USER_UPDATE: 'user:update',
  USER_DELETE: 'user:delete',
  POST_CREATE: 'post:create',
  POST_UPDATE: 'post:update',
  POST_DELETE: 'post:delete',
};

// Role-permission mapping
const rolePermissions = {
  [ROLES.ADMIN]: Object.values(PERMISSIONS),
  [ROLES.MODERATOR]: [
    PERMISSIONS.USER_READ,
    PERMISSIONS.POST_CREATE,
    PERMISSIONS.POST_UPDATE,
    PERMISSIONS.POST_DELETE,
  ],
  [ROLES.USER]: [
    PERMISSIONS.USER_READ,
    PERMISSIONS.POST_CREATE,
  ]
};

// Check if role has permission
function hasPermission(role, permission) {
  const permissions = rolePermissions[role] || [];
  return permissions.includes(permission);
}

// Require role middleware
function requireRole(...allowedRoles) {
  return (req, res, next) => {
    if (!req.user) {
      return res.status(401).json({ error: 'Unauthorized' });
    }

    if (!allowedRoles.includes(req.user.role)) {
      return res.status(403).json({ error: 'Forbidden' });
    }

    next();
  };
}

// Require permission middleware
function requirePermission(permission) {
  return (req, res, next) => {
    if (!req.user) {
      return res.status(401).json({ error: 'Unauthorized' });
    }

    if (!hasPermission(req.user.role, permission)) {
      return res.status(403).json({ error: 'Insufficient permissions' });
    }

    next();
  };
}

// Usage
app.delete('/users/:id',
  authenticateToken,
  requireRole(ROLES.ADMIN),
  async (req, res) => {
    // Only admins can delete users
  }
);

app.post('/posts',
  authenticateToken,
  requirePermission(PERMISSIONS.POST_CREATE),
  async (req, res) => {
    // Users with post:create permission can create posts
  }
);
```

### Prevent Insecure Direct Object Reference (IDOR)

```javascript
// BAD - IDOR vulnerability
app.get('/orders/:id', authenticateToken, async (req, res) => {
  const order = await Order.findById(req.params.id);
  res.json(order); // Returns any order, even if not owned by user!
});

// GOOD - Check ownership
app.get('/orders/:id', authenticateToken, async (req, res) => {
  const order = await Order.findById(req.params.id);

  if (!order) {
    return res.status(404).json({ error: 'Order not found' });
  }

  // Verify user owns this order (or is admin)
  if (order.userId !== req.user.id && req.user.role !== ROLES.ADMIN) {
    return res.status(403).json({ error: 'Access denied' });
  }

  res.json(order);
});

// BETTER - Query with ownership filter
app.get('/orders/:id', authenticateToken, async (req, res) => {
  const order = await Order.findOne({
    _id: req.params.id,
    userId: req.user.id // Automatically filters by ownership
  });

  if (!order) {
    return res.status(404).json({ error: 'Order not found' });
  }

  res.json(order);
});

// Reusable ownership middleware
function requireOwnership(Model, userIdField = 'userId') {
  return async (req, res, next) => {
    try {
      const resource = await Model.findById(req.params.id);

      if (!resource) {
        return res.status(404).json({ error: 'Resource not found' });
      }

      // Check ownership (allow admins)
      if (resource[userIdField] !== req.user.id && req.user.role !== ROLES.ADMIN) {
        return res.status(403).json({ error: 'Access denied' });
      }

      req.resource = resource;
      next();
    } catch (error) {
      res.status(500).json({ error: 'Authorization check failed' });
    }
  };
}

// Usage
app.put('/orders/:id',
  authenticateToken,
  requireOwnership(Order),
  async (req, res) => {
    // req.resource is the verified order
    await req.resource.update(req.body);
    res.json(req.resource);
  }
);
```

## Multi-Factor Authentication (MFA)

### TOTP Implementation

```javascript
const speakeasy = require('speakeasy');
const QRCode = require('qrcode');

// Enable MFA - generate secret
app.post('/mfa/enable', authenticateToken, async (req, res) => {
  try {
    const user = await User.findById(req.user.id);

    // Generate secret
    const secret = speakeasy.generateSecret({
      name: `MyApp (${user.email})`,
      issuer: 'MyApp'
    });

    // Store secret (encrypted) in database
    user.mfaSecret = encrypt(secret.base32);
    user.mfaTempSecret = secret.base32; // Temporary until verified
    await user.save();

    // Generate QR code
    const qrCodeUrl = await QRCode.toDataURL(secret.otpauth_url);

    res.json({
      secret: secret.base32,
      qrCode: qrCodeUrl
    });
  } catch (error) {
    res.status(500).json({ error: 'MFA setup failed' });
  }
});

// Verify and activate MFA
app.post('/mfa/verify', authenticateToken, async (req, res) => {
  try {
    const { token } = req.body;
    const user = await User.findById(req.user.id);

    // Verify token
    const verified = speakeasy.totp.verify({
      secret: user.mfaTempSecret,
      encoding: 'base32',
      token,
      window: 2 // Allow 2 time steps before/after
    });

    if (!verified) {
      return res.status(400).json({ error: 'Invalid verification code' });
    }

    // Activate MFA
    user.mfaEnabled = true;
    user.mfaSecret = encrypt(user.mfaTempSecret);
    user.mfaTempSecret = null;
    await user.save();

    res.json({ message: 'MFA enabled successfully' });
  } catch (error) {
    res.status(500).json({ error: 'MFA verification failed' });
  }
});

// Login with MFA
app.post('/login/mfa', async (req, res) => {
  try {
    const { email, password, mfaToken } = req.body;

    // First verify password
    const user = await User.findOne({ email });
    if (!user || !(await bcrypt.compare(password, user.password))) {
      return res.status(401).json({ error: 'Invalid credentials' });
    }

    // If MFA enabled, verify token
    if (user.mfaEnabled) {
      const secret = decrypt(user.mfaSecret);
      const verified = speakeasy.totp.verify({
        secret,
        encoding: 'base32',
        token: mfaToken,
        window: 2
      });

      if (!verified) {
        return res.status(401).json({ error: 'Invalid MFA code' });
      }
    }

    // Generate tokens
    const accessToken = generateAccessToken(user);
    const refreshToken = generateRefreshToken(user);

    res.json({ accessToken, refreshToken });
  } catch (error) {
    res.status(500).json({ error: 'Login failed' });
  }
});
```

## API Key Authentication

```javascript
const crypto = require('crypto');

// Generate API key
function generateApiKey() {
  return crypto.randomBytes(32).toString('hex');
}

// Create API key endpoint
app.post('/api-keys', authenticateToken, async (req, res) => {
  try {
    const { name, permissions } = req.body;

    // Generate key
    const key = generateApiKey();
    const hashedKey = crypto.createHash('sha256').update(key).digest('hex');

    // Store hashed key
    const apiKey = await ApiKey.create({
      userId: req.user.id,
      name,
      keyHash: hashedKey,
      permissions,
      lastUsed: null
    });

    // Return key only once
    res.status(201).json({
      message: 'API key created. Save this key - it will not be shown again.',
      apiKey: key,
      id: apiKey.id
    });
  } catch (error) {
    res.status(500).json({ error: 'API key creation failed' });
  }
});

// API key authentication middleware
async function authenticateApiKey(req, res, next) {
  const apiKey = req.headers['x-api-key'];

  if (!apiKey) {
    return res.status(401).json({ error: 'API key required' });
  }

  try {
    // Hash provided key
    const keyHash = crypto.createHash('sha256').update(apiKey).digest('hex');

    // Find key in database
    const storedKey = await ApiKey.findOne({ keyHash });

    if (!storedKey) {
      return res.status(401).json({ error: 'Invalid API key' });
    }

    // Check if key is active
    if (!storedKey.active) {
      return res.status(401).json({ error: 'API key revoked' });
    }

    // Update last used
    storedKey.lastUsed = new Date();
    await storedKey.save();

    // Attach user and permissions to request
    req.apiKey = storedKey;
    req.user = await User.findById(storedKey.userId);

    next();
  } catch (error) {
    res.status(500).json({ error: 'Authentication failed' });
  }
}

// Usage
app.get('/api/data', authenticateApiKey, async (req, res) => {
  // Check API key permissions
  if (!req.apiKey.permissions.includes('data:read')) {
    return res.status(403).json({ error: 'Insufficient permissions' });
  }

  // Return data
});
```

## Security Checklist

When implementing authentication/authorization:

- [ ] Passwords hashed with bcrypt/Argon2 (never plain text)
- [ ] Strong password policy enforced
- [ ] Rate limiting on login/registration
- [ ] Account lockout after failed attempts
- [ ] Secure session configuration (HTTPOnly, Secure, SameSite)
- [ ] Session timeout implemented
- [ ] JWT with short expiration times
- [ ] Refresh token rotation
- [ ] Authorization checks on all protected endpoints
- [ ] IDOR prevention (verify ownership)
- [ ] Role-based access control implemented
- [ ] MFA available for sensitive accounts
- [ ] API keys hashed in database
- [ ] Logout invalidates sessions/tokens
- [ ] Security logging for auth events
- [ ] Generic error messages (don't reveal user existence)
- [ ] HTTPS enforced in production
- [ ] CSRF protection implemented

Apply these authentication and authorization practices to prevent unauthorized access, credential theft, and privilege escalation attacks.
