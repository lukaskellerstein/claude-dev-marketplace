---
name: input-validation
description: Auto-invoked when processing user input to ensure proper validation, sanitization, and injection prevention
allowed-tools: Read, Grep, Glob
---

# Input Validation Best Practices

This skill provides guidance on secure input validation and sanitization to prevent injection attacks.

## When Active

This skill activates when you:
- Process user input from HTTP requests, forms, or APIs
- Construct database queries with user data
- Execute system commands with user input
- Render user content in HTML/JavaScript
- Upload or process files from users
- Parse JSON/XML from untrusted sources
- Process URL parameters or path segments

## Core Principles

### 1. Validate All Input
- **Never trust user input**: Assume all input is malicious
- **Validate on server side**: Client-side validation is not security
- **Fail securely**: Reject invalid input, don't try to "fix" it
- **Whitelist > Blacklist**: Define what's allowed, not what's forbidden

### 2. Defense in Depth
- Input validation (first line)
- Parameterized queries (prevent SQL injection)
- Output encoding (prevent XSS)
- Security headers (defense layer)
- WAF/Rate limiting (network layer)

## Validation Strategies

### Type Validation
```javascript
// Validate data types
const { body } = require('express-validator');

body('age')
  .isInt({ min: 0, max: 150 })
  .withMessage('Age must be a number between 0 and 150');

body('email')
  .isEmail()
  .normalizeEmail()
  .withMessage('Invalid email address');

body('url')
  .isURL({ protocols: ['https'] })
  .withMessage('Must be a valid HTTPS URL');

body('date')
  .isISO8601()
  .withMessage('Invalid date format');
```

### Length Validation
```javascript
// Prevent buffer overflow and DoS
body('username')
  .isLength({ min: 3, max: 30 })
  .withMessage('Username must be 3-30 characters');

body('description')
  .isLength({ max: 5000 })
  .withMessage('Description too long');

// Check array/object sizes
body('tags')
  .isArray({ max: 10 })
  .withMessage('Maximum 10 tags allowed');
```

### Format Validation
```javascript
// Use regex for specific formats
body('phone')
  .matches(/^\+?[1-9]\d{1,14}$/)
  .withMessage('Invalid phone number format');

body('zipcode')
  .matches(/^\d{5}(-\d{4})?$/)
  .withMessage('Invalid ZIP code');

// Prevent dangerous characters
body('username')
  .matches(/^[a-zA-Z0-9_-]+$/)
  .withMessage('Username can only contain letters, numbers, hyphens, and underscores');

// NO special characters that could be used in injection
body('searchTerm')
  .matches(/^[a-zA-Z0-9\s]+$/)
  .withMessage('Search term contains invalid characters');
```

### Sanitization
```javascript
// Remove/escape dangerous content
const validator = require('validator');

// Escape HTML
const safeInput = validator.escape(userInput);

// Remove script tags
const cleanHtml = DOMPurify.sanitize(userInput, {
  ALLOWED_TAGS: ['p', 'br', 'strong', 'em'],
  ALLOWED_ATTR: []
});

// Trim whitespace
body('name').trim();

// Normalize email
body('email').normalizeEmail();

// Remove null bytes
const safe = input.replace(/\0/g, '');
```

## Prevention by Attack Type

### SQL Injection Prevention

```javascript
// VULNERABLE - String concatenation
const query = `SELECT * FROM users WHERE id = ${userId}`;

// VULNERABLE - Template literals
const query = `SELECT * FROM users WHERE name = '${userName}'`;

// SECURE - Parameterized queries (Node.js)
const query = 'SELECT * FROM users WHERE id = ?';
const result = await db.query(query, [userId]);

// SECURE - Named parameters
const query = 'SELECT * FROM users WHERE name = :name AND age > :age';
const result = await db.query(query, { name: userName, age: minAge });

// SECURE - ORM (Sequelize)
const user = await User.findOne({
  where: { email: userEmail }
});

// SECURE - Query builder (Knex)
const users = await knex('users')
  .where('email', userEmail)
  .select('id', 'name');
```

### NoSQL Injection Prevention

```javascript
// VULNERABLE - Direct object use
const user = await db.users.findOne({ username: req.body.username });

// Attack: { "username": { "$ne": null } } returns first user

// SECURE - Type validation
const username = String(req.body.username);
const user = await db.users.findOne({ username });

// SECURE - Whitelist operators
const allowedOperators = ['$eq', '$gt', '$lt'];
function sanitizeQuery(query) {
  for (const key in query) {
    if (key.startsWith('$') && !allowedOperators.includes(key)) {
      delete query[key];
    }
  }
  return query;
}
```

### Command Injection Prevention

```javascript
// VULNERABLE - String concatenation
exec(`convert ${userFile} output.pdf`);

// VULNERABLE - Shell injection via template
exec(`ffmpeg -i ${userInput} output.mp4`);

// SECURE - Use execFile with array arguments
const { execFile } = require('child_process');
execFile('convert', [userFile, 'output.pdf'], (error, stdout) => {
  // Process result
});

// SECURE - Validate and whitelist commands
const allowedCommands = ['convert', 'resize', 'rotate'];
if (!allowedCommands.includes(command)) {
  throw new Error('Invalid command');
}

// SECURE - Escape shell arguments
const { spawn } = require('child_process');
const child = spawn('convert', [userFile, '-resize', '800x600', 'output.pdf']);
```

### Path Traversal Prevention

```javascript
// VULNERABLE - Direct path construction
const filePath = `/uploads/${req.params.filename}`;
res.sendFile(filePath);

// Attack: ../../../etc/passwd

// SECURE - Use path.basename
const path = require('path');
const filename = path.basename(req.params.filename);
const filePath = path.join(__dirname, 'uploads', filename);
res.sendFile(filePath);

// SECURE - Whitelist allowed files
const allowedFiles = new Set(['avatar.jpg', 'cover.png']);
if (!allowedFiles.has(filename)) {
  return res.status(403).send('Forbidden');
}

// SECURE - Verify path stays within directory
const fs = require('fs');
const fullPath = path.resolve(uploadsDir, filename);
if (!fullPath.startsWith(uploadsDir)) {
  return res.status(403).send('Invalid path');
}
```

### XSS Prevention

```javascript
// VULNERABLE - Direct HTML insertion
element.innerHTML = userInput;

// VULNERABLE - Unescaped template
res.send(`<h1>Welcome ${username}</h1>`);

// SECURE - Use textContent
element.textContent = userInput;

// SECURE - Use template engine with auto-escaping
res.render('welcome', { username }); // EJS, Pug, etc. auto-escape

// SECURE - Manual escaping
function escapeHtml(unsafe) {
  return unsafe
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

// SECURE - Use DOMPurify for rich content
import DOMPurify from 'dompurify';
const clean = DOMPurify.sanitize(dirtyHtml, {
  ALLOWED_TAGS: ['p', 'b', 'i', 'em', 'strong'],
  ALLOWED_ATTR: []
});
```

### LDAP Injection Prevention

```javascript
// VULNERABLE
const filter = `(uid=${username})`;

// SECURE - Escape special characters
function escapeLDAP(input) {
  return input
    .replace(/\\/g, '\\5c')
    .replace(/\*/g, '\\2a')
    .replace(/\(/g, '\\28')
    .replace(/\)/g, '\\29')
    .replace(/\0/g, '\\00');
}

const filter = `(uid=${escapeLDAP(username)})`;
```

## File Upload Validation

### Complete File Upload Security

```javascript
const multer = require('multer');
const path = require('path');
const crypto = require('crypto');
const fileType = require('file-type');
const fs = require('fs').promises;

// Storage configuration
const storage = multer.diskStorage({
  destination: async (req, file, cb) => {
    const uploadDir = path.join(__dirname, '../uploads');
    await fs.mkdir(uploadDir, { recursive: true });
    cb(null, uploadDir);
  },
  filename: (req, file, cb) => {
    // Generate random filename (prevent path traversal)
    const randomName = crypto.randomBytes(16).toString('hex');
    const ext = path.extname(file.originalname).toLowerCase();
    cb(null, `${randomName}${ext}`);
  }
});

const upload = multer({
  storage: storage,
  limits: {
    fileSize: 5 * 1024 * 1024, // 5MB max
    files: 1, // Single file upload
  },
  fileFilter: async (req, file, cb) => {
    try {
      // 1. Check extension (whitelist)
      const allowedExts = ['.jpg', '.jpeg', '.png', '.pdf'];
      const ext = path.extname(file.originalname).toLowerCase();

      if (!allowedExts.includes(ext)) {
        return cb(new Error('Invalid file extension'));
      }

      // 2. Check MIME type
      const allowedMimes = ['image/jpeg', 'image/png', 'application/pdf'];
      if (!allowedMimes.includes(file.mimetype)) {
        return cb(new Error('Invalid MIME type'));
      }

      // 3. Validate filename (no special characters)
      const filename = path.basename(file.originalname);
      if (!/^[a-zA-Z0-9._-]+$/.test(filename)) {
        return cb(new Error('Invalid filename'));
      }

      cb(null, true);
    } catch (error) {
      cb(error);
    }
  }
});

// Additional validation after upload
app.post('/upload', upload.single('file'), async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({ error: 'No file uploaded' });
    }

    // 4. Verify actual file type (magic bytes)
    const buffer = await fs.readFile(req.file.path);
    const type = await fileType.fromBuffer(buffer);

    const allowedTypes = ['image/jpeg', 'image/png', 'application/pdf'];
    if (!type || !allowedTypes.includes(type.mime)) {
      await fs.unlink(req.file.path); // Delete invalid file
      return res.status(400).json({ error: 'Invalid file type' });
    }

    // 5. Scan for malware (integrate with antivirus)
    // await scanFileForMalware(req.file.path);

    // 6. Generate safe URL
    const fileUrl = `/uploads/${path.basename(req.file.path)}`;

    res.json({
      message: 'File uploaded successfully',
      url: fileUrl
    });

  } catch (error) {
    if (req.file) {
      await fs.unlink(req.file.path).catch(() => {});
    }
    res.status(500).json({ error: 'Upload failed' });
  }
});
```

## Validation Middleware Pattern

```javascript
// middleware/validators.js
const { body, param, query, validationResult } = require('express-validator');

// Reusable validation chains
const validators = {
  userId: param('id')
    .isUUID()
    .withMessage('Invalid user ID format'),

  email: body('email')
    .isEmail()
    .normalizeEmail()
    .withMessage('Invalid email address'),

  password: body('password')
    .isLength({ min: 8 })
    .withMessage('Password must be at least 8 characters')
    .matches(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/)
    .withMessage('Password must contain uppercase, lowercase, and number'),

  username: body('username')
    .isLength({ min: 3, max: 30 })
    .matches(/^[a-zA-Z0-9_-]+$/)
    .withMessage('Username can only contain alphanumeric characters, hyphens, and underscores'),

  pagination: [
    query('page')
      .optional()
      .isInt({ min: 1 })
      .withMessage('Page must be a positive integer'),
    query('limit')
      .optional()
      .isInt({ min: 1, max: 100 })
      .withMessage('Limit must be between 1 and 100'),
  ],

  searchQuery: query('q')
    .trim()
    .isLength({ min: 2, max: 100 })
    .matches(/^[a-zA-Z0-9\s-]+$/)
    .withMessage('Invalid search query'),
};

// Validation error handler
const handleValidationErrors = (req, res, next) => {
  const errors = validationResult(req);
  if (!errors.isEmpty()) {
    return res.status(400).json({
      error: 'Validation failed',
      details: errors.array()
    });
  }
  next();
};

// Export for use in routes
module.exports = {
  ...validators,
  handleValidationErrors,
};

// Usage in routes
const { validators, handleValidationErrors } = require('./middleware/validators');

app.post('/users',
  validators.email,
  validators.password,
  validators.username,
  handleValidationErrors,
  createUserController
);

app.get('/users/:id',
  validators.userId,
  handleValidationErrors,
  getUserController
);

app.get('/search',
  validators.searchQuery,
  validators.pagination,
  handleValidationErrors,
  searchController
);
```

## Validation Checklist

When processing user input, ensure:

- [ ] **Type validation**: Data is the expected type (string, number, date, etc.)
- [ ] **Length validation**: Within acceptable min/max bounds
- [ ] **Format validation**: Matches expected pattern (email, URL, phone, etc.)
- [ ] **Range validation**: Numbers within acceptable ranges
- [ ] **Whitelist validation**: Value is in list of allowed values
- [ ] **Character validation**: Only allowed characters present
- [ ] **Encoding validation**: Proper character encoding (UTF-8)
- [ ] **Size validation**: Files, arrays, objects within size limits
- [ ] **Sanitization**: Dangerous characters escaped or removed
- [ ] **Server-side validation**: Never rely on client-side only
- [ ] **Error handling**: Invalid input rejected with clear messages
- [ ] **Logging**: Invalid input attempts logged for security monitoring
- [ ] **Rate limiting**: Prevent brute force validation attacks

## Common Pitfalls to Avoid

### Don't Use Blacklists
```javascript
// BAD - Easy to bypass
if (input.includes('script') || input.includes('onclick')) {
  reject();
}
// Bypass: <scr<script>ipt>, on\u0000click

// GOOD - Whitelist allowed characters/patterns
if (!/^[a-zA-Z0-9\s]+$/.test(input)) {
  reject();
}
```

### Don't Trust Client-Side Validation
```javascript
// BAD - Only client validation
// <input type="email" required> // Can be bypassed

// GOOD - Server-side validation
app.post('/register', [
  body('email').isEmail(),
  handleValidationErrors
], registerHandler);
```

### Don't Try to "Fix" Invalid Input
```javascript
// BAD - Trying to sanitize malicious input
const cleaned = input.replace(/['";]/g, '');

// GOOD - Reject invalid input
if (!/^[a-zA-Z0-9]+$/.test(input)) {
  throw new Error('Invalid input');
}
```

### Don't Expose Validation Logic
```javascript
// BAD - Reveals validation logic
res.status(400).json({
  error: 'Password must be 8-20 chars with uppercase, lowercase, number, and special char'
});

// GOOD - Generic message
res.status(400).json({
  error: 'Invalid password format'
});
```

## Integration with Security Tools

### Static Analysis
```bash
# Semgrep rules for input validation
semgrep --config "p/sql-injection"
semgrep --config "p/command-injection"
semgrep --config "p/xss"
```

### Runtime Validation
```javascript
// Use JSON Schema for API validation
const Ajv = require('ajv');
const ajv = new Ajv();

const schema = {
  type: 'object',
  properties: {
    email: { type: 'string', format: 'email' },
    age: { type: 'integer', minimum: 0, maximum: 150 }
  },
  required: ['email'],
  additionalProperties: false
};

const validate = ajv.compile(schema);
if (!validate(data)) {
  console.log(validate.errors);
}
```

Apply these input validation practices to prevent injection attacks, data corruption, and security vulnerabilities. Always validate on the server side, use whitelisting, and fail securely when input is invalid.
