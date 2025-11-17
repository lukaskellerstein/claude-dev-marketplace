---
name: inline-doc-generator
description: Auto-generate inline documentation (docstrings, JSDoc) when writing code
---

# Inline Documentation Generator Skill

## Auto-Invocation Contexts

This skill is automatically invoked when:
- Creating new functions or methods
- Defining new classes or types
- Writing complex logic or algorithms
- Creating API endpoints or handlers
- Defining data models or schemas
- Writing public interfaces or APIs

## Purpose

Automatically generate high-quality inline documentation (docstrings, JSDoc comments) for code as it's being written.

## Actions

When auto-invoked, this skill:

1. **Analyzes the code context**:
   - Function/method signature
   - Parameter types and names
   - Return type
   - Exceptions/errors that may be raised
   - Complexity of the implementation

2. **Generates appropriate documentation**:
   - Brief description of purpose
   - Parameter descriptions with types
   - Return value description
   - Exceptions/errors that may be raised
   - Usage examples for public APIs
   - Notes about side effects or important behavior

3. **Follows language conventions**:
   - **Python**: Google-style docstrings
   - **JavaScript/TypeScript**: JSDoc comments
   - **Go**: Go doc comments
   - **Java**: Javadoc
   - **Other languages**: Appropriate documentation style

## Documentation Templates

### Python (Google-style Docstrings)

```python
def function_name(param1: str, param2: int, optional_param: bool = False) -> Dict[str, Any]:
    """Brief one-line description of function.

    More detailed description if needed. Explain the purpose, behavior,
    and any important details.

    Args:
        param1: Description of param1. Explain what it's used for.
        param2: Description of param2. Include valid ranges if applicable.
        optional_param: Description of optional parameter. Include default
            behavior if omitted.

    Returns:
        Description of return value. Explain the structure if complex.
        For dict/list returns, describe the contents.

    Raises:
        ValueError: When param1 is empty or invalid.
        TypeError: When param2 is not an integer.
        KeyError: When required key is missing in data.

    Example:
        >>> result = function_name("test", 42)
        >>> print(result)
        {'status': 'success', 'value': 42}

    Note:
        Any important notes about usage, performance, or side effects.
    """
    pass
```

### TypeScript/JavaScript (JSDoc)

```typescript
/**
 * Brief one-line description of function.
 *
 * More detailed description if needed. Explain the purpose, behavior,
 * and any important details.
 *
 * @param {string} param1 - Description of param1
 * @param {number} param2 - Description of param2
 * @param {boolean} [optionalParam=false] - Description of optional parameter
 * @returns {Promise<Object>} Description of return value
 * @throws {Error} When param1 is empty or invalid
 * @throws {TypeError} When param2 is not a number
 *
 * @example
 * const result = await functionName("test", 42);
 * console.log(result); // { status: 'success', value: 42 }
 *
 * @see {@link RelatedFunction} for related functionality
 */
async function functionName(
  param1: string,
  param2: number,
  optionalParam: boolean = false
): Promise<object> {
  // implementation
}
```

### Go Doc Comments

```go
// FunctionName performs a specific operation on the given parameters.
//
// This function processes param1 and param2 to produce a result.
// It returns an error if the parameters are invalid.
//
// Parameters:
//   - param1: description of param1
//   - param2: description of param2
//
// Returns:
//   - A pointer to the result object
//   - An error if the operation fails
//
// Example:
//
//	result, err := FunctionName("test", 42)
//	if err != nil {
//	    log.Fatal(err)
//	}
//	fmt.Println(result)
func FunctionName(param1 string, param2 int) (*Result, error) {
    // implementation
}
```

## Guidelines

### For Simple Functions

Minimal documentation for obvious functions:

```python
def get_user_by_id(user_id: str) -> Optional[User]:
    """Retrieve a user by their ID.

    Args:
        user_id: The unique identifier of the user.

    Returns:
        User object if found, None otherwise.
    """
    pass
```

### For Complex Functions

Comprehensive documentation for complex logic:

```python
def process_payment_with_retry(
    order_id: str,
    amount: Decimal,
    payment_method: PaymentMethod,
    max_retries: int = 3
) -> PaymentResult:
    """Process payment with automatic retry on transient failures.

    Attempts to process the payment using the specified payment method.
    If the payment fails due to transient errors (network issues, timeout),
    it will retry up to max_retries times with exponential backoff.

    Args:
        order_id: Unique identifier of the order being paid.
        amount: Payment amount in the order's currency. Must be positive.
        payment_method: Payment method to use (card, bank_transfer, etc.).
        max_retries: Maximum number of retry attempts. Default is 3.

    Returns:
        PaymentResult containing transaction_id, status, and timestamp.

    Raises:
        ValueError: If amount is negative or zero.
        PaymentError: If payment fails after all retries.
        InvalidPaymentMethod: If payment method is not supported.

    Example:
        >>> result = process_payment_with_retry(
        ...     order_id="ORD-123",
        ...     amount=Decimal("99.99"),
        ...     payment_method=PaymentMethod.CREDIT_CARD
        ... )
        >>> print(result.status)
        PaymentStatus.SUCCESS

    Note:
        This function may take several seconds to complete if retries
        are needed. Consider using async version for high-volume scenarios.
    """
    pass
```

### For Classes

```python
class UserRepository:
    """Repository for managing user data persistence.

    This class provides an abstraction layer for user data operations,
    handling database interactions and caching. It implements the
    repository pattern to separate data access logic from business logic.

    Attributes:
        db_connection: Database connection instance.
        cache: Redis cache instance for user data.
        _cache_ttl: Cache TTL in seconds (default: 300).

    Example:
        >>> repo = UserRepository(db, cache)
        >>> user = repo.get_by_id("user-123")
        >>> user.name = "New Name"
        >>> repo.update(user)
    """

    def __init__(self, db_connection: Connection, cache: RedisCache):
        """Initialize the repository with database and cache connections.

        Args:
            db_connection: Active database connection.
            cache: Redis cache instance.
        """
        pass
```

### For API Endpoints

```typescript
/**
 * Create a new user account.
 *
 * POST /api/v1/users
 *
 * Creates a new user account with the provided information.
 * Validates email uniqueness and password strength.
 * Sends verification email upon successful creation.
 *
 * @param {Request} req - Express request object
 * @param {Object} req.body - Request body
 * @param {string} req.body.email - User's email address (must be unique)
 * @param {string} req.body.password - User's password (min 8 chars)
 * @param {string} req.body.name - User's full name
 * @param {Response} res - Express response object
 * @returns {Promise<void>}
 *
 * @throws {ValidationError} If email is invalid or already exists
 * @throws {ValidationError} If password doesn't meet requirements
 *
 * @example
 * // Request
 * POST /api/v1/users
 * {
 *   "email": "user@example.com",
 *   "password": "SecurePass123",
 *   "name": "John Doe"
 * }
 *
 * // Response (201 Created)
 * {
 *   "id": "usr_abc123",
 *   "email": "user@example.com",
 *   "name": "John Doe",
 *   "created_at": "2024-01-01T00:00:00Z"
 * }
 */
async function createUser(req: Request, res: Response): Promise<void> {
  // implementation
}
```

## Best Practices

1. **Be Concise**: First line should be brief and descriptive
2. **Be Complete**: Document all parameters, returns, and exceptions
3. **Be Accurate**: Documentation must match actual behavior
4. **Include Examples**: Add usage examples for non-trivial functions
5. **Type Information**: Include type information even if language has type hints
6. **Edge Cases**: Document edge cases and special behavior
7. **Side Effects**: Mention any side effects (database writes, API calls, etc.)
8. **Performance**: Note performance characteristics if relevant

## When NOT to Auto-Generate

Skip auto-generation for:
- Trivial getters/setters (unless required by team standards)
- Private helper functions with obvious purpose
- Test functions (use descriptive names instead)
- One-line utility functions

## Integration with Code

- Generate documentation BEFORE function implementation
- Update documentation when function signature changes
- Suggest documentation improvements during code review
- Flag undocumented public APIs

## Follow Project Standards

Check for project-specific documentation standards:
- Team documentation guidelines
- Language-specific conventions
- Framework requirements (e.g., FastAPI requires docstrings for OpenAPI)
- Auto-generated API documentation tools

## Quality Checks

Verify generated documentation:
- [ ] First line is concise and descriptive
- [ ] All parameters documented
- [ ] Return value documented
- [ ] Exceptions/errors documented
- [ ] Examples provided for complex functions
- [ ] Type information included
- [ ] Grammar and spelling correct
- [ ] Matches actual implementation

Follow the standards defined in `DOCUMENTATION_STANDARDS.md`.
