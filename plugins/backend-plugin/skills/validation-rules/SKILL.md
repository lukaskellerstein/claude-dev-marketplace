---
name: validation-rules
description: Master comprehensive input validation patterns for Express, FastAPI, Spring Boot, and Go backends including Zod, Pydantic, and struct tags. Use when implementing request validation, sanitizing user inputs, preventing SQL injection, adding custom validators, validating file uploads, or ensuring XSS protection across API endpoints.
allowed-tools: Read, Edit, Grep
---

# Validation Rules Skill

Automatically detects and adds input validation to API endpoints.

## When to Use This Skill

- Implementing request validation with express-validator, Zod, or Joi
- Creating Pydantic models for FastAPI with custom validators
- Adding struct tag validation in Go with validator package
- Sanitizing user inputs to prevent XSS attacks
- Preventing SQL injection with parameterized queries
- Adding custom validation functions for business logic rules
- Validating file uploads (size, type, content)
- Implementing email, URL, and UUID format validation
- Adding password strength validation with regex patterns
- Validating date ranges and time zone handling
- Implementing array and nested object validation
- Adding conditional validation based on other fields
- Validating JSON schemas for complex request bodies
- Implementing phone number and credit card validation
- Adding geolocation coordinate validation

## Quick Start

### Minimal Validation Example

```typescript
// Express.js with Zod validation
import express from 'express';
import { z } from 'zod';

const app = express();

// Validation schema
const createUserSchema = z.object({
  email: z.string().email('Invalid email format'),
  name: z.string().min(2, 'Name must be at least 2 characters').max(100),
  age: z.number().int().min(18, 'Must be at least 18').max(120).optional(),
  password: z.string().min(8).regex(
    /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/,
    'Password must contain uppercase, lowercase, and number'
  )
});

// Validation middleware
const validate = (schema: z.ZodSchema) => {
  return (req, res, next) => {
    try {
      schema.parse(req.body);
      next();
    } catch (error) {
      if (error instanceof z.ZodError) {
        return res.status(400).json({
          error: 'Validation failed',
          details: error.errors.map(err => ({
            field: err.path.join('.'),
            message: err.message
          }))
        });
      }
      next(error);
    }
  };
};

// Usage
app.post('/users', validate(createUserSchema), async (req, res) => {
  const user = await User.create(req.body);
  res.status(201).json(user);
});
```

## Validation Patterns

### Express Validation

Automatically adds express-validator when detected:

```javascript
import { body, param, query, validationResult } from 'express-validator';

// Comprehensive validation rules
const userValidationRules = [
  body('email')
    .isEmail()
    .normalizeEmail()
    .withMessage('Valid email required')
    .custom(async (email) => {
      const exists = await User.findOne({ where: { email } });
      if (exists) {
        throw new Error('Email already in use');
      }
    }),

  body('name')
    .trim()
    .isLength({ min: 2, max: 100 })
    .withMessage('Name must be 2-100 characters')
    .matches(/^[a-zA-Z\s'-]+$/)
    .withMessage('Name can only contain letters, spaces, hyphens, and apostrophes'),

  body('age')
    .optional()
    .isInt({ min: 18, max: 120 })
    .withMessage('Age must be between 18 and 120')
    .toInt(),

  body('password')
    .isLength({ min: 8, max: 128 })
    .withMessage('Password must be 8-128 characters')
    .matches(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])/)
    .withMessage('Password must contain uppercase, lowercase, number, and special character'),

  body('confirmPassword')
    .custom((value, { req }) => value === req.body.password)
    .withMessage('Passwords do not match'),

  body('role')
    .optional()
    .isIn(['user', 'moderator', 'admin'])
    .withMessage('Invalid role'),

  body('website')
    .optional()
    .isURL({ protocols: ['http', 'https'], require_protocol: true })
    .withMessage('Invalid URL format'),

  body('birthDate')
    .optional()
    .isISO8601()
    .toDate()
    .custom((date) => {
      const age = Math.floor((Date.now() - date.getTime()) / (365.25 * 24 * 60 * 60 * 1000));
      if (age < 18) {
        throw new Error('Must be at least 18 years old');
      }
      return true;
    }),

  body('tags')
    .optional()
    .isArray({ min: 1, max: 10 })
    .withMessage('Tags must be an array with 1-10 items'),

  body('tags.*')
    .trim()
    .isLength({ min: 2, max: 20 })
    .withMessage('Each tag must be 2-20 characters')
];

// Query parameter validation
const listUsersValidation = [
  query('page')
    .optional()
    .isInt({ min: 1 })
    .toInt()
    .withMessage('Page must be a positive integer'),

  query('limit')
    .optional()
    .isInt({ min: 1, max: 100 })
    .toInt()
    .withMessage('Limit must be between 1 and 100'),

  query('sortBy')
    .optional()
    .isIn(['name', 'email', 'createdAt'])
    .withMessage('Invalid sort field'),

  query('order')
    .optional()
    .isIn(['asc', 'desc'])
    .toLowerCase()
    .withMessage('Order must be asc or desc'),

  query('search')
    .optional()
    .trim()
    .escape()
    .isLength({ max: 100 })
    .withMessage('Search query too long')
];

// URL parameter validation
const getUserValidation = [
  param('id')
    .isUUID(4)
    .withMessage('Invalid user ID format')
];

// Validation middleware
const validate = (req, res, next) => {
  const errors = validationResult(req);
  if (!errors.isEmpty()) {
    return res.status(400).json({
      error: {
        code: 'VALIDATION_ERROR',
        message: 'Validation failed',
        details: errors.array().map(err => ({
          field: err.path,
          message: err.msg,
          value: err.value
        }))
      }
    });
  }
  next();
};

// Usage
app.post('/users', userValidationRules, validate, createUser);
app.get('/users', listUsersValidation, validate, listUsers);
app.get('/users/:id', getUserValidation, validate, getUser);
```

### Pydantic Validation (FastAPI)

Automatically creates Pydantic models:

```python
from pydantic import BaseModel, EmailStr, Field, validator, root_validator
from typing import Optional, List
from datetime import datetime, date
from enum import Enum
import re

class UserRole(str, Enum):
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"

class UserCreate(BaseModel):
    email: EmailStr
    name: str = Field(..., min_length=2, max_length=100)
    age: Optional[int] = Field(None, ge=18, le=120)
    password: str = Field(..., min_length=8, max_length=128)
    confirm_password: str
    role: Optional[UserRole] = UserRole.USER
    website: Optional[str] = None
    birth_date: Optional[date] = None
    tags: Optional[List[str]] = Field(None, min_items=1, max_items=10)
    phone: Optional[str] = None

    @validator('name')
    def validate_name(cls, v):
        if not re.match(r'^[a-zA-Z\s\'-]+$', v):
            raise ValueError('Name can only contain letters, spaces, hyphens, and apostrophes')
        return v.strip()

    @validator('password')
    def validate_password(cls, v):
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one digit')
        if not re.search(r'[@$!%*?&]', v):
            raise ValueError('Password must contain at least one special character')
        return v

    @root_validator
    def check_passwords_match(cls, values):
        password = values.get('password')
        confirm_password = values.get('confirm_password')
        if password != confirm_password:
            raise ValueError('Passwords do not match')
        return values

    @validator('email')
    def validate_email(cls, v):
        # Reject plus addressing
        if '+' in v.split('@')[0]:
            raise ValueError('Plus addressing not allowed')
        return v.lower()

    @validator('website')
    def validate_website(cls, v):
        if v is None:
            return v
        if not v.startswith(('http://', 'https://')):
            raise ValueError('URL must start with http:// or https://')
        return v

    @validator('birth_date')
    def validate_birth_date(cls, v):
        if v is None:
            return v
        age = (date.today() - v).days / 365.25
        if age < 18:
            raise ValueError('Must be at least 18 years old')
        if age > 120:
            raise ValueError('Invalid birth date')
        return v

    @validator('tags')
    def validate_tags(cls, v):
        if v is None:
            return v
        validated_tags = []
        for tag in v:
            tag = tag.strip()
            if len(tag) < 2 or len(tag) > 20:
                raise ValueError(f'Tag "{tag}" must be 2-20 characters')
            validated_tags.append(tag)
        # Check for duplicates
        if len(validated_tags) != len(set(validated_tags)):
            raise ValueError('Tags must be unique')
        return validated_tags

    @validator('phone')
    def validate_phone(cls, v):
        if v is None:
            return v
        # E.164 format validation
        if not re.match(r'^\+[1-9]\d{1,14}$', v):
            raise ValueError('Phone must be in E.164 format (e.g., +1234567890)')
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "name": "John Doe",
                "age": 25,
                "password": "SecurePass123!",
                "confirm_password": "SecurePass123!",
                "role": "user",
                "website": "https://example.com",
                "birth_date": "1998-01-01",
                "tags": ["developer", "python"],
                "phone": "+12025550123"
            }
        }

# Query parameter validation
class UserQueryParams(BaseModel):
    page: int = Field(1, ge=1)
    limit: int = Field(20, ge=1, le=100)
    sort_by: Optional[str] = Field(None, regex='^(name|email|created_at)$')
    order: Optional[str] = Field('desc', regex='^(asc|desc)$')
    search: Optional[str] = Field(None, max_length=100)
    role: Optional[UserRole] = None

    @validator('search')
    def sanitize_search(cls, v):
        if v is None:
            return v
        # Remove special characters for security
        return re.sub(r'[^\w\s-]', '', v).strip()

# Usage in FastAPI
from fastapi import FastAPI, HTTPException, Query, Depends

app = FastAPI()

@app.post("/users", status_code=201)
async def create_user(user_data: UserCreate):
    # Check if email exists
    existing = await User.find_one(email=user_data.email)
    if existing:
        raise HTTPException(
            status_code=409,
            detail={
                "code": "EMAIL_EXISTS",
                "message": "User with this email already exists",
                "field": "email"
            }
        )

    # Create user (password already validated)
    user = await User.create(**user_data.dict(exclude={'confirm_password'}))
    return user

@app.get("/users")
async def list_users(params: UserQueryParams = Depends()):
    users = await User.find_all(
        skip=(params.page - 1) * params.limit,
        limit=params.limit,
        sort_by=params.sort_by,
        order=params.order,
        search=params.search,
        role=params.role
    )
    return users
```

### Go Validation

Adds struct tag validation:

```go
package main

import (
    "regexp"
    "time"
    "github.com/go-playground/validator/v10"
    "github.com/gin-gonic/gin"
)

// Custom validator instance
var validate *validator.Validate

type CreateUserRequest struct {
    Email           string    `json:"email" binding:"required,email"`
    Name            string    `json:"name" binding:"required,min=2,max=100,alpha_space"`
    Age             int       `json:"age" binding:"omitempty,gte=18,lte=120"`
    Password        string    `json:"password" binding:"required,min=8,max=128,strong_password"`
    ConfirmPassword string    `json:"confirm_password" binding:"required,eqfield=Password"`
    Role            string    `json:"role" binding:"omitempty,oneof=user moderator admin"`
    Website         string    `json:"website" binding:"omitempty,url"`
    BirthDate       time.Time `json:"birth_date" binding:"omitempty,adult"`
    Tags            []string  `json:"tags" binding:"omitempty,min=1,max=10,dive,min=2,max=20"`
    Phone           string    `json:"phone" binding:"omitempty,e164"`
}

type UserQueryParams struct {
    Page    int    `form:"page" binding:"omitempty,gte=1"`
    Limit   int    `form:"limit" binding:"omitempty,gte=1,lte=100"`
    SortBy  string `form:"sort_by" binding:"omitempty,oneof=name email created_at"`
    Order   string `form:"order" binding:"omitempty,oneof=asc desc"`
    Search  string `form:"search" binding:"omitempty,max=100"`
    Role    string `form:"role" binding:"omitempty,oneof=user moderator admin"`
}

func init() {
    validate = validator.New()

    // Register custom validators
    validate.RegisterValidation("strong_password", validateStrongPassword)
    validate.RegisterValidation("alpha_space", validateAlphaSpace)
    validate.RegisterValidation("adult", validateAdult)
}

// Custom validator: strong password
func validateStrongPassword(fl validator.FieldLevel) bool {
    password := fl.Field().String()

    hasUpper := regexp.MustCompile(`[A-Z]`).MatchString(password)
    hasLower := regexp.MustCompile(`[a-z]`).MatchString(password)
    hasDigit := regexp.MustCompile(`\d`).MatchString(password)
    hasSpecial := regexp.MustCompile(`[@$!%*?&]`).MatchString(password)

    return hasUpper && hasLower && hasDigit && hasSpecial
}

// Custom validator: alphabetic with spaces
func validateAlphaSpace(fl validator.FieldLevel) bool {
    name := fl.Field().String()
    return regexp.MustCompile(`^[a-zA-Z\s'-]+$`).MatchString(name)
}

// Custom validator: at least 18 years old
func validateAdult(fl validator.FieldLevel) bool {
    birthDate := fl.Field().Interface().(time.Time)
    age := time.Since(birthDate).Hours() / 24 / 365.25
    return age >= 18 && age <= 120
}

// Validation error response
type ValidationError struct {
    Field   string `json:"field"`
    Message string `json:"message"`
}

type ErrorResponse struct {
    Code    string            `json:"code"`
    Message string            `json:"message"`
    Details []ValidationError `json:"details"`
}

// Validation middleware
func validateRequest(c *gin.Context, req interface{}) bool {
    if err := c.ShouldBindJSON(req); err != nil {
        var errors []ValidationError

        if validationErrors, ok := err.(validator.ValidationErrors); ok {
            for _, fieldError := range validationErrors {
                errors = append(errors, ValidationError{
                    Field:   fieldError.Field(),
                    Message: getErrorMessage(fieldError),
                })
            }
        } else {
            errors = append(errors, ValidationError{
                Field:   "request",
                Message: err.Error(),
            })
        }

        c.JSON(400, ErrorResponse{
            Code:    "VALIDATION_ERROR",
            Message: "Validation failed",
            Details: errors,
        })
        return false
    }
    return true
}

// Get user-friendly error message
func getErrorMessage(fe validator.FieldError) string {
    switch fe.Tag() {
    case "required":
        return "This field is required"
    case "email":
        return "Invalid email format"
    case "min":
        return fmt.Sprintf("Must be at least %s characters", fe.Param())
    case "max":
        return fmt.Sprintf("Must not exceed %s characters", fe.Param())
    case "gte":
        return fmt.Sprintf("Must be at least %s", fe.Param())
    case "lte":
        return fmt.Sprintf("Must not exceed %s", fe.Param())
    case "eqfield":
        return fmt.Sprintf("Must match %s", fe.Param())
    case "oneof":
        return fmt.Sprintf("Must be one of: %s", fe.Param())
    case "url":
        return "Invalid URL format"
    case "e164":
        return "Must be in E.164 format (e.g., +1234567890)"
    case "strong_password":
        return "Password must contain uppercase, lowercase, digit, and special character"
    case "alpha_space":
        return "Can only contain letters, spaces, hyphens, and apostrophes"
    case "adult":
        return "Must be at least 18 years old"
    default:
        return "Invalid value"
    }
}

// Usage in handlers
func createUser(c *gin.Context) {
    var req CreateUserRequest
    if !validateRequest(c, &req) {
        return
    }

    // Check if email exists
    existing, _ := userRepository.FindByEmail(req.Email)
    if existing != nil {
        c.JSON(409, ErrorResponse{
            Code:    "EMAIL_EXISTS",
            Message: "User with this email already exists",
            Details: []ValidationError{{
                Field:   "email",
                Message: "Email already in use",
            }},
        })
        return
    }

    // Create user
    user, err := userService.Create(&req)
    if err != nil {
        c.JSON(500, ErrorResponse{
            Code:    "INTERNAL_ERROR",
            Message: "Failed to create user",
        })
        return
    }

    c.JSON(201, user)
}

func listUsers(c *gin.Context) {
    var params UserQueryParams
    if err := c.ShouldBindQuery(&params); err != nil {
        c.JSON(400, ErrorResponse{
            Code:    "VALIDATION_ERROR",
            Message: "Invalid query parameters",
        })
        return
    }

    // Set defaults
    if params.Page == 0 {
        params.Page = 1
    }
    if params.Limit == 0 {
        params.Limit = 20
    }
    if params.Order == "" {
        params.Order = "desc"
    }

    users, err := userService.List(&params)
    if err != nil {
        c.JSON(500, ErrorResponse{
            Code:    "INTERNAL_ERROR",
            Message: "Failed to fetch users",
        })
        return
    }

    c.JSON(200, users)
}
```

## Common Validation Rules

### String Validation
- **Required/Optional**: Field must be present or can be omitted
- **Min/Max length**: Character count constraints
- **Pattern matching**: Regex validation for formats
- **Email format**: RFC 5322 compliant email validation
- **URL format**: Valid HTTP/HTTPS URLs
- **UUID format**: Version 4 UUID validation
- **Enum values**: Must be one of predefined values
- **Trim whitespace**: Remove leading/trailing spaces
- **Lowercase/Uppercase**: Normalize casing

### Number Validation
- **Min/Max values**: Range constraints
- **Integer/Float types**: Numeric type checking
- **Positive/Negative**: Sign constraints
- **Range validation**: Between two values
- **Multiple of**: Divisible by specific number
- **Precision**: Decimal place limits

### Date Validation
- **Date format**: ISO 8601, RFC 3339
- **Past/Future dates**: Relative date constraints
- **Age calculation**: Derive age from birth date
- **Time zones**: UTC normalization
- **Date ranges**: Between two dates
- **Business days**: Exclude weekends

### Array Validation
- **Min/Max items**: Array length constraints
- **Unique items**: No duplicates allowed
- **Item validation**: Validate each element
- **Sorted**: Items in specific order
- **Contains**: Must include specific value

### File Upload Validation
- **File size limits**: Max bytes allowed
- **MIME type checking**: Allowed content types
- **Extension validation**: Allowed file extensions
- **Virus scanning**: Malware detection
- **Image dimensions**: Width/height constraints
- **File content**: Validate actual content matches extension

## Real-World Applications

### Application 1: Complex Nested Validation

```typescript
// Zod schema for complex nested objects
import { z } from 'zod';

const addressSchema = z.object({
  street: z.string().min(1).max(100),
  city: z.string().min(1).max(50),
  state: z.string().length(2).regex(/^[A-Z]{2}$/),
  zipCode: z.string().regex(/^\d{5}(-\d{4})?$/),
  country: z.string().length(2).regex(/^[A-Z]{2}$/)
});

const phoneSchema = z.object({
  type: z.enum(['mobile', 'home', 'work']),
  number: z.string().regex(/^\+[1-9]\d{1,14}$/),
  primary: z.boolean().default(false)
});

const orderItemSchema = z.object({
  productId: z.string().uuid(),
  quantity: z.number().int().positive().max(999),
  price: z.number().positive().multipleOf(0.01),
  discount: z.number().min(0).max(100).optional()
}).refine(
  (data) => {
    if (data.discount && data.discount > 50) {
      return data.quantity >= 10; // Large discount requires min quantity
    }
    return true;
  },
  { message: 'Discount over 50% requires at least 10 items' }
);

const createOrderSchema = z.object({
  customerId: z.string().uuid(),
  shippingAddress: addressSchema,
  billingAddress: addressSchema.optional(),
  phones: z.array(phoneSchema).min(1).max(3),
  items: z.array(orderItemSchema).min(1).max(50),
  paymentMethod: z.enum(['credit_card', 'paypal', 'bank_transfer']),
  notes: z.string().max(500).optional(),
  couponCode: z.string().regex(/^[A-Z0-9]{6,12}$/).optional()
}).refine(
  (data) => {
    // Ensure at least one primary phone
    return data.phones.some(phone => phone.primary);
  },
  { message: 'At least one phone must be marked as primary', path: ['phones'] }
).refine(
  (data) => {
    // Calculate total and validate
    const total = data.items.reduce((sum, item) => {
      const discount = item.discount || 0;
      return sum + (item.price * item.quantity * (1 - discount / 100));
    }, 0);
    return total >= 10; // Minimum order value
  },
  { message: 'Order total must be at least $10', path: ['items'] }
);

// Usage
app.post('/orders', validate(createOrderSchema), async (req, res) => {
  const order = await Order.create(req.body);
  res.status(201).json(order);
});
```

### Application 2: File Upload Validation

```typescript
// Multer with comprehensive file validation
import multer from 'multer';
import sharp from 'sharp';
import { promisify } from 'util';
import { unlink } from 'fs';

const unlinkAsync = promisify(unlink);

// Storage configuration
const storage = multer.diskStorage({
  destination: '/tmp/uploads',
  filename: (req, file, cb) => {
    const uniqueSuffix = `${Date.now()}-${Math.round(Math.random() * 1E9)}`;
    cb(null, `${uniqueSuffix}-${file.originalname}`);
  }
});

// File filter
const fileFilter = (req, file, cb) => {
  const allowedMimes = [
    'image/jpeg',
    'image/png',
    'image/webp',
    'application/pdf'
  ];

  if (allowedMimes.includes(file.mimetype)) {
    cb(null, true);
  } else {
    cb(new Error('Invalid file type. Only JPEG, PNG, WebP, and PDF allowed.'));
  }
};

// Upload configuration
const upload = multer({
  storage,
  fileFilter,
  limits: {
    fileSize: 5 * 1024 * 1024, // 5MB
    files: 5 // Max 5 files
  }
});

// Validation middleware
const validateUpload = async (req, res, next) => {
  if (!req.files || req.files.length === 0) {
    return res.status(400).json({
      error: 'No files uploaded'
    });
  }

  try {
    for (const file of req.files) {
      // Validate image dimensions
      if (file.mimetype.startsWith('image/')) {
        const metadata = await sharp(file.path).metadata();

        if (metadata.width > 4000 || metadata.height > 4000) {
          await unlinkAsync(file.path);
          return res.status(400).json({
            error: `Image ${file.originalname} exceeds maximum dimensions (4000x4000)`
          });
        }

        if (metadata.width < 100 || metadata.height < 100) {
          await unlinkAsync(file.path);
          return res.status(400).json({
            error: `Image ${file.originalname} below minimum dimensions (100x100)`
          });
        }
      }

      // Validate file extension matches MIME type
      const ext = file.originalname.split('.').pop().toLowerCase();
      const mimeToExt = {
        'image/jpeg': ['jpg', 'jpeg'],
        'image/png': ['png'],
        'image/webp': ['webp'],
        'application/pdf': ['pdf']
      };

      if (!mimeToExt[file.mimetype]?.includes(ext)) {
        await unlinkAsync(file.path);
        return res.status(400).json({
          error: `File extension does not match content type for ${file.originalname}`
        });
      }
    }

    next();
  } catch (error) {
    // Clean up uploaded files
    for (const file of req.files) {
      await unlinkAsync(file.path).catch(() => {});
    }
    next(error);
  }
};

// Usage
app.post('/upload', upload.array('files', 5), validateUpload, async (req, res) => {
  const uploadedFiles = req.files.map(file => ({
    filename: file.filename,
    size: file.size,
    mimetype: file.mimetype
  }));

  res.json({
    message: 'Files uploaded successfully',
    files: uploadedFiles
  });
});
```

### Application 3: Custom Business Logic Validation

```python
# FastAPI with complex business rule validation
from pydantic import BaseModel, validator, root_validator
from typing import List, Optional
from datetime import datetime, timedelta
from decimal import Decimal

class BookingCreate(BaseModel):
    room_id: str
    check_in: datetime
    check_out: datetime
    guest_count: int = Field(..., ge=1, le=10)
    special_requests: Optional[str] = Field(None, max_length=500)
    total_price: Decimal = Field(..., gt=0, decimal_places=2)

    @validator('check_in')
    def check_in_must_be_future(cls, v):
        if v < datetime.now():
            raise ValueError('Check-in date must be in the future')
        if v > datetime.now() + timedelta(days=365):
            raise ValueError('Cannot book more than 1 year in advance')
        return v

    @root_validator
    def validate_dates(cls, values):
        check_in = values.get('check_in')
        check_out = values.get('check_out')

        if check_in and check_out:
            if check_out <= check_in:
                raise ValueError('Check-out must be after check-in')

            nights = (check_out - check_in).days
            if nights < 1:
                raise ValueError('Minimum stay is 1 night')
            if nights > 30:
                raise ValueError('Maximum stay is 30 nights')

        return values

    @root_validator
    def validate_price(cls, values):
        room_id = values.get('room_id')
        check_in = values.get('check_in')
        check_out = values.get('check_out')
        total_price = values.get('total_price')
        guest_count = values.get('guest_count')

        if all([room_id, check_in, check_out, total_price]):
            # Calculate expected price
            nights = (check_out - check_in).days
            room_rate = get_room_rate(room_id, check_in, check_out)
            extra_guest_fee = max(0, guest_count - 2) * Decimal('25.00')
            expected_price = (room_rate * nights) + (extra_guest_fee * nights)

            # Allow 1% variance for rounding
            if abs(total_price - expected_price) > (expected_price * Decimal('0.01')):
                raise ValueError(
                    f'Price mismatch. Expected ${expected_price}, got ${total_price}'
                )

        return values

@app.post("/bookings", status_code=201)
async def create_booking(booking_data: BookingCreate, db: Session = Depends(get_db)):
    # Check room availability
    is_available = await check_room_availability(
        booking_data.room_id,
        booking_data.check_in,
        booking_data.check_out,
        db
    )

    if not is_available:
        raise HTTPException(
            status_code=409,
            detail={
                "code": "ROOM_UNAVAILABLE",
                "message": "Room is not available for selected dates"
            }
        )

    # Check room capacity
    room = await db.get(Room, booking_data.room_id)
    if booking_data.guest_count > room.max_occupancy:
        raise HTTPException(
            status_code=400,
            detail={
                "code": "EXCEEDS_CAPACITY",
                "message": f"Room capacity is {room.max_occupancy} guests",
                "field": "guest_count"
            }
        )

    # Create booking
    booking = await Booking.create(db, **booking_data.dict())
    return booking
```

## Sanitization

Automatically adds sanitization:

```javascript
// Auto-sanitization with express-validator
import { body } from 'express-validator';
import sanitizeHtml from 'sanitize-html';

const sanitizationRules = [
  body('input')
    .trim()           // Remove whitespace
    .escape()         // Escape HTML
    .normalizeEmail() // Normalize email
    .toInt()          // Convert to integer
    .toBoolean()      // Convert to boolean
    .toLowerCase()    // Convert to lowercase
    .toUpperCase()    // Convert to uppercase
    .customSanitizer(value => {
      // Custom sanitization
      return sanitizeHtml(value, {
        allowedTags: ['b', 'i', 'em', 'strong', 'a', 'p'],
        allowedAttributes: {
          'a': ['href']
        },
        allowedSchemes: ['http', 'https', 'mailto']
      });
    })
];
```

## SQL Injection Prevention

Ensures parameterized queries:

```python
# Detects and fixes SQL injection vulnerabilities

# ❌ Bad: Vulnerable to SQL injection
query = f"SELECT * FROM users WHERE email = '{email}'"
cursor.execute(query)

# ✅ Good: Parameterized query (safe)
query = "SELECT * FROM users WHERE email = %s"
cursor.execute(query, (email,))

# ✅ Good: ORM usage (safe)
user = await User.filter(email=email).first()

# ❌ Bad: String concatenation
query = "INSERT INTO users (name, email) VALUES ('" + name + "', '" + email + "')"

# ✅ Good: Parameterized insert
query = "INSERT INTO users (name, email) VALUES (%s, %s)"
cursor.execute(query, (name, email))

# ✅ Good: ORM create
user = await User.create(name=name, email=email)
```

## XSS Prevention

Automatically escapes output:

```javascript
// Adds XSS protection
import sanitizeHtml from 'sanitize-html';
import DOMPurify from 'isomorphic-dompurify';

// Server-side sanitization
const clean = sanitizeHtml(dirty, {
  allowedTags: ['b', 'i', 'em', 'strong', 'a', 'p', 'ul', 'ol', 'li'],
  allowedAttributes: {
    'a': ['href', 'title'],
    'img': ['src', 'alt']
  },
  allowedSchemes: ['http', 'https', 'mailto'],
  transformTags: {
    'a': (tagName, attribs) => {
      return {
        tagName: 'a',
        attribs: {
          ...attribs,
          rel: 'noopener noreferrer',
          target: '_blank'
        }
      };
    }
  }
});

// Client-side sanitization (if rendering user content)
const cleanHtml = DOMPurify.sanitize(userInput, {
  ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'a'],
  ALLOWED_ATTR: ['href']
});

// Escape for HTML context
function escapeHtml(text) {
  const map = {
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#039;'
  };
  return text.replace(/[&<>"']/g, m => map[m]);
}
```

## Best Practices Summary

- **Validate on server-side** - Never trust client-side validation alone
- **Whitelist, don't blacklist** - Define allowed values, not blocked ones
- **Sanitize inputs** - Remove/escape dangerous characters
- **Use type-safe schemas** - Leverage TypeScript, Pydantic, or struct tags
- **Provide clear error messages** - Help users fix validation errors
- **Validate early** - Fail fast with clear feedback
- **Use parameterized queries** - Prevent SQL injection
- **Escape output** - Prevent XSS attacks
- **Validate business logic** - Not just data types and formats
- **Log validation failures** - Track potential attacks

## Common Pitfalls

### Pitfall 1: Client-Side Validation Only
```javascript
// ❌ Bad: Relying on client-side validation
// Client code can be bypassed

// ✅ Good: Always validate on server
app.post('/users', validate(schema), handler);
```

### Pitfall 2: Weak Password Validation
```python
# ❌ Bad: Only length check
if len(password) >= 8:
    # Weak passwords like "aaaaaaaa" pass

# ✅ Good: Comprehensive validation
@validator('password')
def validate_password(cls, v):
    if len(v) < 8:
        raise ValueError('Minimum 8 characters')
    if not re.search(r'[A-Z]', v):
        raise ValueError('Need uppercase')
    if not re.search(r'[a-z]', v):
        raise ValueError('Need lowercase')
    if not re.search(r'\d', v):
        raise ValueError('Need digit')
    return v
```

### Pitfall 3: Not Sanitizing HTML Input
```typescript
// ❌ Bad: Storing unsanitized HTML
user.bio = req.body.bio;

// ✅ Good: Sanitize before storing
user.bio = sanitizeHtml(req.body.bio, {
  allowedTags: ['b', 'i', 'em', 'strong'],
  allowedAttributes: {}
});
```

## Related Skills

- **api-best-practices**: Ensures proper HTTP status codes for validation errors
- **error-handling**: Handles validation errors with consistent format
- **auth-patterns**: Validates authentication credentials
- **security-patterns**: Prevents injection and XSS attacks

This skill automatically applies when API endpoints are created or modified.
