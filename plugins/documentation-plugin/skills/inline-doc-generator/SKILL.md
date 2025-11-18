---
name: inline-doc-generator
description: Master inline documentation (JSDoc, TSDoc, GoDoc, Python docstrings). Use when creating functions/methods, defining classes/types, writing complex logic, creating APIs, defining data models, or writing public interfaces.
---

# Inline Documentation Generator Skill

Master inline documentation standards for all major programming languages, automatically generating high-quality docstrings, JSDoc comments, and API documentation as code is written.

## When to Use This Skill

Use this skill when:

1. Creating new functions or methods
2. Defining new classes or types
3. Writing complex logic or algorithms
4. Creating API endpoints or handlers
5. Defining data models or schemas
6. Writing public interfaces or APIs
7. Implementing business logic functions
8. Creating utility or helper functions
9. Developing library or framework code
10. Writing exported modules or packages
11. Defining GraphQL resolvers or mutations
12. Creating database queries or repositories
13. Implementing authentication or authorization logic
14. Writing webhook handlers or event processors
15. Developing microservice endpoints

## Quick Start

This skill automatically generates documentation as you write code:

```python
# You write:
def process_payment(order_id: str, amount: Decimal) -> PaymentResult:
    pass

# Skill suggests:
def process_payment(order_id: str, amount: Decimal) -> PaymentResult:
    """Process payment for an order.

    Args:
        order_id: Unique identifier of the order.
        amount: Payment amount in the order's currency.

    Returns:
        PaymentResult containing transaction ID and status.

    Raises:
        ValueError: If amount is negative or zero.
        PaymentError: If payment processing fails.
    """
    pass
```

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

### Rust Documentation

```rust
/// Brief one-line description of function.
///
/// More detailed description if needed. Explain the purpose,
/// behavior, and any important details.
///
/// # Arguments
///
/// * `param1` - Description of param1
/// * `param2` - Description of param2
///
/// # Returns
///
/// Description of return value
///
/// # Errors
///
/// Returns an error if:
/// - param1 is empty
/// - param2 is negative
///
/// # Examples
///
/// ```
/// let result = function_name("test", 42)?;
/// println!("{:?}", result);
/// ```
///
/// # Panics
///
/// This function panics if the internal state is invalid.
pub fn function_name(param1: &str, param2: i32) -> Result<Value, Error> {
    // implementation
}
```

### Java (Javadoc)

```java
/**
 * Brief one-line description of method.
 * <p>
 * More detailed description if needed. Explain the purpose,
 * behavior, and any important details.
 *
 * @param param1 description of param1
 * @param param2 description of param2
 * @return description of return value
 * @throws IllegalArgumentException if param1 is null or empty
 * @throws IOException if file operation fails
 * @see RelatedClass for related functionality
 * @since 1.0
 */
public Result methodName(String param1, int param2)
        throws IllegalArgumentException, IOException {
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

## Real-World Applications

### E-commerce Payment Processing

**Scenario:** Documenting a payment processing function

```python
def process_refund(
    transaction_id: str,
    amount: Optional[Decimal] = None,
    reason: str = "customer_request"
) -> RefundResult:
    """Process a refund for a previous transaction.

    Initiates a refund for the specified transaction. If no amount is
    provided, refunds the full transaction amount. Refunds are processed
    asynchronously and may take 5-10 business days to complete.

    Args:
        transaction_id: ID of the original payment transaction.
        amount: Partial refund amount. If None, refunds full amount.
            Must not exceed original transaction amount.
        reason: Reason for refund. One of: customer_request,
            fraudulent, duplicate, product_not_received. Default is
            customer_request.

    Returns:
        RefundResult containing:
            - refund_id: Unique ID for this refund
            - status: PENDING, PROCESSING, COMPLETED, or FAILED
            - amount: Amount being refunded
            - estimated_completion: Expected completion date

    Raises:
        TransactionNotFound: If transaction_id doesn't exist.
        InvalidRefundAmount: If amount > original transaction amount.
        RefundWindowExpired: If refund requested after 90-day window.
        PaymentGatewayError: If payment gateway rejects refund.

    Example:
        >>> # Full refund
        >>> result = process_refund("txn_abc123")
        >>> print(result.status)
        RefundStatus.PENDING

        >>> # Partial refund
        >>> result = process_refund(
        ...     "txn_abc123",
        ...     amount=Decimal("25.00"),
        ...     reason="product_not_received"
        ... )

    Note:
        - Refunds are final and cannot be reversed
        - Refund fees may apply depending on payment method
        - Customer will receive email notification when refund completes
        - Original payment method must still be valid for refund

    See Also:
        - check_refund_eligibility(): Verify if refund is allowed
        - get_refund_status(): Check status of pending refund
    """
    pass
```

### Data Processing Pipeline

**Scenario:** Documenting a data transformation function

```typescript
/**
 * Transform and validate customer data for import.
 *
 * Processes raw customer data from various sources (CSV, JSON, XML)
 * and transforms it into a standardized format. Performs validation,
 * deduplication, and enrichment before importing into the database.
 *
 * @param {RawCustomerData[]} rawData - Array of raw customer records
 * @param {ImportOptions} options - Import configuration options
 * @param {string} [options.source='manual'] - Data source identifier
 * @param {boolean} [options.validateEmails=true] - Validate email addresses
 * @param {boolean} [options.deduplicte=true] - Remove duplicate records
 * @param {boolean} [options.enrichData=false] - Enrich with external data
 * @param {ProgressCallback} [progressCallback] - Optional progress callback
 * @returns {Promise<ImportResult>} Import result with statistics
 *
 * @throws {ValidationError} If data format is invalid
 * @throws {DuplicateError} If critical duplicates found and deduplicate=false
 * @throws {ExternalServiceError} If enrichment service unavailable
 *
 * @example
 * // Basic import
 * const result = await transformCustomerData(rawData, {
 *   source: 'csv_upload',
 *   validateEmails: true
 * });
 * console.log(`Imported ${result.successCount} customers`);
 *
 * @example
 * // Import with progress tracking
 * const result = await transformCustomerData(
 *   rawData,
 *   { enrichData: true },
 *   (progress) => {
 *     console.log(`Progress: ${progress.percent}%`);
 *   }
 * );
 *
 * @performance
 * Processes approximately 1000 records per second.
 * For large datasets (>100k records), consider batch processing.
 *
 * @since 2.0.0
 */
async function transformCustomerData(
  rawData: RawCustomerData[],
  options: ImportOptions = {},
  progressCallback?: ProgressCallback
): Promise<ImportResult> {
  // implementation
}
```

### Machine Learning Model

**Scenario:** Documenting ML prediction function

```python
def predict_churn(
    customer_id: str,
    features: Optional[Dict[str, Any]] = None,
    model_version: str = "latest"
) -> ChurnPrediction:
    """Predict customer churn probability using trained ML model.

    Analyzes customer behavior and engagement metrics to predict
    the likelihood of churn in the next 30 days. Uses ensemble
    model combining XGBoost, Random Forest, and Neural Network.

    Args:
        customer_id: Unique customer identifier.
        features: Optional feature overrides. If None, fetches
            features from database. Useful for what-if analysis.
        model_version: Model version to use. Default is "latest".
            Use specific version (e.g., "v2.1.0") for reproducibility.

    Returns:
        ChurnPrediction containing:
            - probability: Churn probability (0.0 to 1.0)
            - risk_level: LOW, MEDIUM, or HIGH
            - contributing_factors: Top 5 factors influencing prediction
            - recommended_actions: Suggested retention strategies
            - confidence: Model confidence score (0.0 to 1.0)

    Raises:
        CustomerNotFound: If customer_id doesn't exist.
        ModelNotFound: If specified model_version doesn't exist.
        FeatureExtractionError: If required features cannot be computed.

    Example:
        >>> prediction = predict_churn("cust_123")
        >>> if prediction.risk_level == RiskLevel.HIGH:
        ...     print(f"High churn risk: {prediction.probability:.1%}")
        ...     for action in prediction.recommended_actions:
        ...         print(f"  - {action}")

    Example:
        >>> # What-if analysis
        >>> features = get_customer_features("cust_123")
        >>> features["login_frequency"] *= 2  # Simulate more logins
        >>> prediction = predict_churn("cust_123", features=features)
        >>> print(f"Improved probability: {prediction.probability:.1%}")

    Note:
        - Model is retrained weekly with latest data
        - Predictions are cached for 1 hour
        - Feature computation may take 2-3 seconds for new customers
        - Model performs best for customers with 90+ days of history

    Performance:
        - Average latency: 50ms (with cache hit)
        - Average latency: 2.5s (with cache miss)
        - Recommended rate limit: 100 requests/minute

    Model Metrics (v3.2.0):
        - AUC-ROC: 0.89
        - Precision: 0.84
        - Recall: 0.81
        - F1-Score: 0.82

    See Also:
        - get_retention_strategies(): Get detailed retention plans
        - compute_customer_lifetime_value(): Estimate CLV
    """
    pass
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

## Common Pitfalls

### ❌ Documenting Implementation Details

**Problem:**
```python
def calculate_total(items):
    """
    Iterates through items list using a for loop,
    creates a temporary sum variable initialized to 0,
    then adds each item.price to sum...
    """
```

**Solution:** Focus on what, not how
```python
def calculate_total(items):
    """
    Calculate the total price of all items.

    Args:
        items: List of Item objects with price attribute

    Returns:
        Decimal: Total price of all items
    """
```

### ❌ Restating Function Name

**Problem:**
```typescript
/**
 * Gets the user
 */
function getUser(id: string): User
```

**Solution:** Provide meaningful information
```typescript
/**
 * Retrieves user profile from database by ID.
 *
 * @param id - Unique user identifier (UUID)
 * @returns User object with profile data
 * @throws UserNotFoundError if user doesn't exist
 */
function getUser(id: string): User
```

### ❌ Missing Parameter Descriptions

**Problem:**
```python
def send_email(to, subject, body):
    """Sends an email."""
```

**Solution:** Document all parameters
```python
def send_email(to: str, subject: str, body: str) -> bool:
    """
    Send an email message via SMTP.

    Args:
        to: Recipient email address
        subject: Email subject line
        body: Email body content (plain text)

    Returns:
        True if email sent successfully, False otherwise
    """
```

### ❌ Outdated Documentation

**Problem:** Function signature changed but docs didn't update
```typescript
/**
 * @param username - User's login name  ← Old parameter
 */
function login(email: string, password: string)  // ← New signature
```

**Solution:** Keep docs in sync with code
```typescript
/**
 * Authenticate user with email and password.
 *
 * @param email - User's email address
 * @param password - User's password (will be hashed)
 * @returns Authentication token
 */
function login(email: string, password: string)
```

### ❌ Vague Return Descriptions

**Problem:**
```python
def get_users():
    """Returns users."""  # What format? What users?
```

**Solution:** Be specific about return value
```python
def get_users() -> List[User]:
    """
    Retrieve all active users from database.

    Returns:
        List of User objects ordered by creation date (newest first).
        Returns empty list if no users found.
    """
```

### ❌ No Exception Documentation

**Problem:**
```java
/**
 * Processes payment
 */
public void processPayment(Payment payment)  // Can throw multiple exceptions!
```

**Solution:** Document all exceptions
```java
/**
 * Process a payment transaction through payment gateway.
 *
 * @param payment Payment details including amount and method
 * @throws InsufficientFundsException if account balance too low
 * @throws PaymentGatewayException if gateway is unavailable
 * @throws InvalidPaymentException if payment data is invalid
 */
public void processPayment(Payment payment)
```

### ❌ Missing Examples for Complex APIs

**Problem:**
```python
def transform_data(data, schema, options):
    """Transforms data according to schema."""  # How do I use this?
```

**Solution:** Provide usage example
```python
def transform_data(data: dict, schema: Schema, options: TransformOptions) -> dict:
    """
    Transform data structure according to provided schema.

    Args:
        data: Source data dictionary
        schema: Transformation schema defining mappings
        options: Transform options (strict mode, defaults, etc.)

    Returns:
        Transformed data matching target schema

    Example:
        >>> schema = Schema({'name': 'user.fullName', 'age': 'user.years'})
        >>> data = {'user': {'fullName': 'Alice', 'years': 30}}
        >>> transform_data(data, schema, TransformOptions(strict=True))
        {'name': 'Alice', 'age': 30}
    """
```

### ❌ Inconsistent Documentation Style

**Problem:** Mixing JSDoc, docstring, and plain comments in same project

**Solution:** Choose one style and use consistently:
- Python → docstrings (Google/NumPy style)
- TypeScript/JavaScript → JSDoc
- Java → Javadoc
- Go → godoc comments

## Related Skills

- **changelog-tracker**: Documents user-facing changes from code modifications
- **markdown-formatter**: Formats documentation in markdown files
- **api-doc-generator**: Creates comprehensive API documentation
- **test-doc-generator**: Generates documentation from test cases

Follow the standards defined in `DOCUMENTATION_STANDARDS.md`.
