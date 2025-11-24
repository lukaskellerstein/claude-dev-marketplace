---
name: code-documentation
description: Auto-invoked when writing code comments, docstrings, or inline documentation to ensure clarity and completeness
allowed-tools: Read, Grep, Glob
---

# Code Documentation Best Practices

This skill provides guidance on writing clear, useful code documentation including comments, docstrings, and inline documentation.

## When Active

This skill activates when you:
- Write or update function/method documentation
- Add inline code comments
- Document classes and modules
- Create API documentation
- Review code documentation
- Generate documentation from code

## General Principles

### The Documentation Hierarchy

1. **Self-Documenting Code** (Best)
   - Clear variable names
   - Obvious function names
   - Simple, readable logic

2. **Type Annotations** (Better)
   - TypeScript interfaces
   - Python type hints
   - Go struct tags

3. **Docstrings/JSDoc** (Good)
   - Function/method documentation
   - Class documentation
   - Module documentation

4. **Inline Comments** (When Needed)
   - Complex algorithms
   - Non-obvious decisions
   - Workarounds

### When to Document

**Always Document:**
- Public APIs and interfaces
- Complex algorithms
- Non-obvious behavior
- Performance considerations
- Security-related code
- Workarounds for external bugs
- Configuration options

**Rarely Document:**
- Self-explanatory code
- Simple getters/setters
- Obvious logic
- Implementation details that might change

## Language-Specific Standards

### JavaScript/TypeScript (JSDoc)

**Function Documentation**
```javascript
/**
 * Calculate the total price including tax.
 *
 * @param {number} price - The base price
 * @param {number} taxRate - The tax rate (0-1)
 * @returns {number} The total price with tax
 * @throws {RangeError} If taxRate is outside 0-1 range
 *
 * @example
 * calculateTotal(100, 0.2); // returns 120
 *
 * @example
 * // With destructured config
 * calculateTotal(100, { tax: 0.2, discount: 0.1 });
 */
function calculateTotal(price, taxRate) {
  if (taxRate < 0 || taxRate > 1) {
    throw new RangeError('Tax rate must be between 0 and 1');
  }
  return price * (1 + taxRate);
}
```

**Class Documentation**
```typescript
/**
 * User authentication service.
 *
 * Handles user authentication, session management, and token generation.
 *
 * @example
 * const auth = new AuthService(config);
 * const user = await auth.login(email, password);
 */
class AuthService {
  /**
   * Create authentication service.
   *
   * @param {AuthConfig} config - Authentication configuration
   * @param {string} config.secret - JWT secret key
   * @param {number} config.expiresIn - Token expiration in seconds
   */
  constructor(config: AuthConfig) {
    this.config = config;
  }

  /**
   * Authenticate user and generate token.
   *
   * @param {string} email - User email
   * @param {string} password - User password
   * @returns {Promise<AuthResult>} Authentication result with token
   * @throws {AuthError} If credentials are invalid
   */
  async login(email: string, password: string): Promise<AuthResult> {
    // Implementation
  }
}
```

**Interface Documentation**
```typescript
/**
 * User profile data.
 */
interface UserProfile {
  /** Unique user identifier */
  id: string;

  /** User's email address */
  email: string;

  /** Display name (optional) */
  name?: string;

  /**
   * User role for access control.
   * @see RolePermissions for role capabilities
   */
  role: 'admin' | 'user' | 'guest';

  /** Account creation timestamp */
  createdAt: Date;
}
```

### Python (Docstrings)

**Function Documentation (Google Style)**
```python
def calculate_total(price: float, tax_rate: float) -> float:
    """Calculate the total price including tax.

    Args:
        price: The base price in dollars
        tax_rate: The tax rate as a decimal (0-1)

    Returns:
        The total price with tax applied

    Raises:
        ValueError: If tax_rate is outside valid range (0-1)
        TypeError: If inputs are not numeric

    Examples:
        >>> calculate_total(100, 0.2)
        120.0

        >>> calculate_total(50.0, 0.15)
        57.5

    Note:
        Tax rate must be between 0 and 1, representing 0% to 100%.
    """
    if not 0 <= tax_rate <= 1:
        raise ValueError('Tax rate must be between 0 and 1')
    return price * (1 + tax_rate)
```

**Class Documentation**
```python
class AuthService:
    """User authentication service.

    This service handles user authentication, session management,
    and JWT token generation.

    Attributes:
        config: Authentication configuration
        secret: JWT secret key
        expiry: Token expiration time in seconds

    Example:
        >>> auth = AuthService(config)
        >>> user = auth.login('user@example.com', 'password')
        >>> print(user.token)
    """

    def __init__(self, config: AuthConfig):
        """Initialize authentication service.

        Args:
            config: Authentication configuration object

        Raises:
            ConfigError: If configuration is invalid
        """
        self.config = config

    def login(self, email: str, password: str) -> AuthResult:
        """Authenticate user and generate token.

        Args:
            email: User email address
            password: User password

        Returns:
            Authentication result containing user data and JWT token

        Raises:
            AuthError: If credentials are invalid
            DatabaseError: If database connection fails
        """
        pass
```

**Module Documentation**
```python
"""User authentication module.

This module provides user authentication functionality including
login, logout, token generation, and session management.

Classes:
    AuthService: Main authentication service
    TokenManager: JWT token generation and validation
    SessionStore: Session data storage

Functions:
    hash_password: Hash password using bcrypt
    verify_password: Verify password against hash

Constants:
    TOKEN_EXPIRY: Default token expiration (3600 seconds)
    MAX_LOGIN_ATTEMPTS: Maximum failed login attempts (5)

Example:
    >>> from auth import AuthService
    >>> auth = AuthService(config)
    >>> result = auth.login('user@example.com', 'password')
"""
```

### Go

**Function Documentation**
```go
// CalculateTotal calculates the total price including tax.
//
// The tax rate should be provided as a decimal between 0 and 1,
// representing 0% to 100% tax rate.
//
// Example:
//   total := CalculateTotal(100, 0.2) // returns 120
//
// Returns an error if the tax rate is outside the valid range.
func CalculateTotal(price float64, taxRate float64) (float64, error) {
    if taxRate < 0 || taxRate > 1 {
        return 0, fmt.Errorf("tax rate must be between 0 and 1, got %f", taxRate)
    }
    return price * (1 + taxRate), nil
}
```

**Struct Documentation**
```go
// UserProfile represents a user's profile data.
type UserProfile struct {
    // ID is the unique user identifier
    ID string `json:"id"`

    // Email is the user's email address
    Email string `json:"email"`

    // Name is the display name (optional)
    Name string `json:"name,omitempty"`

    // Role defines the user's access level.
    // Valid values: "admin", "user", "guest"
    Role string `json:"role"`

    // CreatedAt is the account creation timestamp
    CreatedAt time.Time `json:"created_at"`
}
```

**Package Documentation**
```go
// Package auth provides user authentication functionality.
//
// This package handles user authentication, session management,
// and JWT token generation. It supports multiple authentication
// strategies including password-based and OAuth2.
//
// Basic usage:
//
//   config := &auth.Config{
//       Secret: "your-secret-key",
//       ExpiresIn: 3600,
//   }
//   service := auth.NewService(config)
//   user, err := service.Login(email, password)
//
// For more examples, see the examples directory.
package auth
```

### Rust

**Function Documentation**
```rust
/// Calculate the total price including tax.
///
/// # Arguments
///
/// * `price` - The base price
/// * `tax_rate` - The tax rate (must be between 0.0 and 1.0)
///
/// # Returns
///
/// The total price with tax applied
///
/// # Errors
///
/// Returns `Err` if the tax rate is outside the valid range
///
/// # Examples
///
/// ```
/// use mylib::calculate_total;
///
/// let total = calculate_total(100.0, 0.2).unwrap();
/// assert_eq!(total, 120.0);
/// ```
pub fn calculate_total(price: f64, tax_rate: f64) -> Result<f64, String> {
    if tax_rate < 0.0 || tax_rate > 1.0 {
        return Err(format!("Tax rate must be between 0 and 1, got {}", tax_rate));
    }
    Ok(price * (1.0 + tax_rate))
}
```

**Struct Documentation**
```rust
/// User profile data.
///
/// Contains basic user information including identification,
/// contact details, and role information.
#[derive(Debug, Clone)]
pub struct UserProfile {
    /// Unique user identifier
    pub id: String,

    /// User's email address
    pub email: String,

    /// Display name (optional)
    pub name: Option<String>,

    /// User role for access control
    pub role: Role,

    /// Account creation timestamp
    pub created_at: DateTime<Utc>,
}
```

## Inline Comments

### When to Use Inline Comments

**Good Use Cases:**

1. **Explain Why, Not What**
```javascript
// Good: Explains reasoning
// Using setTimeout to avoid blocking the main thread during heavy computation
setTimeout(() => processLargeData(data), 0);

// Bad: States the obvious
// Call setTimeout with processLargeData
setTimeout(() => processLargeData(data), 0);
```

2. **Complex Algorithms**
```python
# Binary search implementation
# Time complexity: O(log n)
# Space complexity: O(1)
def binary_search(arr, target):
    left, right = 0, len(arr) - 1

    while left <= right:
        # Calculate mid to avoid integer overflow
        # Using (left + right) // 2 could overflow for large values
        mid = left + (right - left) // 2

        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1
```

3. **Workarounds and Hacks**
```javascript
// Workaround for Safari bug #12345
// Safari doesn't properly handle CSS transforms on fixed elements
// Remove this when Safari 17+ is our minimum supported version
element.style.transform = 'translateZ(0)';
```

4. **Performance Optimizations**
```go
// Preallocate slice to avoid reallocation during loop
// Benchmarks showed 30% performance improvement
results := make([]Result, 0, len(items))
for _, item := range items {
    results = append(results, process(item))
}
```

5. **Non-Obvious Logic**
```typescript
// Normalize phone number by removing all non-digit characters
// except the leading + for international format
const normalized = phone.replace(/(?!^\+)\D/g, '');
```

6. **Security Considerations**
```python
# SECURITY: Never log the actual password
# This could expose passwords in log files
logger.info(f"Login attempt for user: {username}")
```

### Comment Style Guidelines

**Single-Line Comments**
```javascript
// Capitalize first letter and use proper punctuation.
// Add space after comment marker.
```

**Multi-Line Comments**
```javascript
/**
 * Use block comments for longer explanations.
 *
 * Break into paragraphs for readability.
 * Keep lines under 80 characters when possible.
 */
```

**Section Separators**
```javascript
// ============================================================================
// Authentication Utilities
// ============================================================================

// ----------------------------------------------------------------------------
// Private Helper Functions
// ----------------------------------------------------------------------------
```

**TODO Comments**
```javascript
// TODO(username): Add error handling for edge case
// TODO: Optimize this algorithm (Issue #123)
// FIXME: This breaks on invalid input
// HACK: Temporary solution until API v2 is available
// NOTE: This assumes UTC timezone
```

## Documentation Anti-Patterns

### 1. Obvious Comments
```javascript
// Bad: States the obvious
let i = 0; // Set i to 0
i++; // Increment i

// Better: Remove unnecessary comments
let i = 0;
i++;
```

### 2. Outdated Comments
```javascript
// Bad: Comment doesn't match code
// Returns user email
return user.username; // Should return user.email!

// Better: Keep comments in sync with code
// Returns username for display
return user.username;
```

### 3. Commented-Out Code
```javascript
// Bad: Leaving dead code
function login(email, password) {
    // const oldAuth = authenticateOldWay(email);
    // if (oldAuth.valid) {
    //   return oldAuth;
    // }
    return authenticateNewWay(email, password);
}

// Better: Remove and rely on version control
function login(email, password) {
    return authenticateNewWay(email, password);
}
```

### 4. Noise Comments
```javascript
// Bad: Excessive commenting
/**
 * Gets the name.
 * @returns {string} The name
 */
getName() {
    return this.name; // Return the name
}

// Better: Let code speak for itself
getName() {
    return this.name;
}
```

### 5. Vague Comments
```javascript
// Bad: Not helpful
// Handle the data
processData(data);

// Better: Specific and informative
// Validate and sanitize user input before database insertion
processData(data);
```

## Documentation Checklist

When documenting code:

### Function/Method Documentation
- [ ] Purpose clearly stated
- [ ] All parameters documented
- [ ] Return value documented
- [ ] Exceptions/errors documented
- [ ] Examples provided
- [ ] Edge cases mentioned
- [ ] Performance characteristics noted (if relevant)
- [ ] Side effects documented

### Class Documentation
- [ ] Class purpose explained
- [ ] Public properties documented
- [ ] Constructor parameters documented
- [ ] Usage examples provided
- [ ] Inheritance/interface relationships noted
- [ ] Thread safety mentioned (if relevant)

### Module/Package Documentation
- [ ] Module purpose explained
- [ ] Public API documented
- [ ] Usage examples provided
- [ ] Dependencies noted
- [ ] Configuration options documented

### Inline Comments
- [ ] Explain "why" not "what"
- [ ] Necessary and informative
- [ ] Up-to-date with code
- [ ] Proper grammar and spelling
- [ ] Not stating the obvious

## Best Practices Summary

1. **Write Self-Documenting Code First**
   - Clear naming
   - Simple logic
   - Appropriate abstractions

2. **Document the Why, Not the What**
   - Explain reasoning and decisions
   - Document non-obvious behavior
   - Clarify complex algorithms

3. **Keep Documentation Close to Code**
   - Inline docstrings
   - Keep in same file
   - Update with code changes

4. **Provide Examples**
   - Show common use cases
   - Include edge cases
   - Make examples runnable

5. **Be Consistent**
   - Follow language conventions
   - Use consistent format
   - Match team standards

6. **Keep It Current**
   - Update with code changes
   - Remove outdated comments
   - Verify examples still work

7. **Know Your Audience**
   - Public API: Comprehensive docs
   - Internal code: Less detail needed
   - Complex logic: More explanation

Use this guidance to write clear, useful code documentation that helps developers understand and use your code effectively.
