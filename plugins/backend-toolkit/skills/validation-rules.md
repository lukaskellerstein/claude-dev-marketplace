---
name: validation-rules
description: Automatically adds input validation to API endpoints
allowed-tools: Read, Edit, Grep
---

# Validation Rules Skill

Automatically detects and adds input validation to API endpoints.

## Validation Patterns

### Express Validation

Automatically adds express-validator when detected:

```javascript
import { body, validationResult } from 'express-validator';

// Auto-generated validation rules
const userValidation = [
  body('email')
    .isEmail()
    .normalizeEmail()
    .withMessage('Valid email required'),

  body('name')
    .trim()
    .isLength({ min: 2, max: 100 })
    .withMessage('Name must be 2-100 characters'),

  body('age')
    .optional()
    .isInt({ min: 18, max: 120 })
    .withMessage('Age must be between 18 and 120'),

  body('password')
    .isLength({ min: 8 })
    .matches(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/)
    .withMessage('Password must contain uppercase, lowercase, and number'),
];

// Validation middleware
const validate = (req, res, next) => {
  const errors = validationResult(req);
  if (!errors.isEmpty()) {
    return res.status(400).json({ errors: errors.array() });
  }
  next();
};
```

### Pydantic Validation (FastAPI)

Automatically creates Pydantic models:

```python
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    name: str = Field(..., min_length=2, max_length=100)
    age: Optional[int] = Field(None, ge=18, le=120)
    password: str = Field(..., min_length=8)

    @validator('password')
    def validate_password(cls, v):
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain uppercase')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain lowercase')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain digit')
        return v

    @validator('email')
    def validate_email(cls, v):
        if '+' in v:
            raise ValueError('Plus addressing not allowed')
        return v.lower()

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "name": "John Doe",
                "age": 25,
                "password": "SecurePass123"
            }
        }
```

### Go Validation

Adds struct tag validation:

```go
type CreateUserRequest struct {
    Email    string `json:"email" binding:"required,email"`
    Name     string `json:"name" binding:"required,min=2,max=100"`
    Age      int    `json:"age" binding:"omitempty,gte=18,lte=120"`
    Password string `json:"password" binding:"required,min=8"`
}

func ValidateStruct(s interface{}) error {
    validate := validator.New()
    return validate.Struct(s)
}

// Custom validator
func ValidatePassword(fl validator.FieldLevel) bool {
    password := fl.Field().String()
    hasUpper := regexp.MustCompile(`[A-Z]`).MatchString(password)
    hasLower := regexp.MustCompile(`[a-z]`).MatchString(password)
    hasDigit := regexp.MustCompile(`\d`).MatchString(password)

    return hasUpper && hasLower && hasDigit
}
```

## Common Validation Rules

### String Validation
- Required/Optional
- Min/Max length
- Pattern matching (regex)
- Email format
- URL format
- UUID format

### Number Validation
- Min/Max values
- Integer/Float types
- Positive/Negative
- Range validation

### Date Validation
- Date format
- Past/Future dates
- Age calculation
- Time zones

### Array Validation
- Min/Max items
- Unique items
- Item validation

### File Upload Validation
- File size limits
- MIME type checking
- Extension validation
- Virus scanning

## Sanitization

Automatically adds sanitization:

```javascript
// Auto-sanitization
body('input')
  .trim()           // Remove whitespace
  .escape()         // Escape HTML
  .normalizeEmail() // Normalize email
  .toInt()         // Convert to integer
  .toBoolean()     // Convert to boolean
```

## SQL Injection Prevention

Ensures parameterized queries:

```python
# Detects and fixes SQL injection vulnerabilities
# Before (vulnerable)
query = f"SELECT * FROM users WHERE email = '{email}'"

# After (safe)
query = "SELECT * FROM users WHERE email = %s"
cursor.execute(query, (email,))
```

## XSS Prevention

Automatically escapes output:

```javascript
// Adds XSS protection
const sanitizeHtml = require('sanitize-html');

const clean = sanitizeHtml(dirty, {
  allowedTags: ['b', 'i', 'em', 'strong', 'a'],
  allowedAttributes: {
    'a': ['href']
  }
});
```

This skill automatically applies when API endpoints are created or modified.