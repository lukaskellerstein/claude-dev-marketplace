---
description: Assess test suite quality, identify test smells, evaluate test maintainability, and provide refactoring recommendations
---

Assess the quality of your test suite, identify test smells and anti-patterns, evaluate test maintainability, and provide specific recommendations for improvement.

## Process

Follow these steps:

1. **Initial Assessment**: Understand test suite structure
   - Identify testing frameworks and tools in use
   - Locate all test files and directories
   - Review test organization and structure
   - Count total tests and test files
   - Check test execution time

2. **Analyze Test Quality**: Evaluate multiple dimensions
   - Test readability and clarity
   - Test maintainability and complexity
   - Test independence and isolation
   - Proper use of mocks and stubs
   - Test naming conventions
   - Test organization (describe/context blocks)

3. **Launch Test Quality Expert**: Use the `test-plugin:test-quality-expert` agent to:
   - Detect test smells and anti-patterns
   - Analyze test structure (AAA pattern adherence)
   - Evaluate test data management
   - Check for proper assertions
   - Identify flaky tests
   - Assess test duplication
   - Verify test independence
   - Analyze test execution performance

4. **Calculate Quality Metrics**: Measure test quality
   - Test complexity (cyclomatic complexity)
   - Test length (lines per test)
   - Setup complexity
   - Test-to-code ratio
   - Assertion density
   - Code duplication in tests
   - Test execution time

5. **Generate Recommendations**: Provide actionable improvements
   - Specific test smells to fix
   - Refactoring opportunities
   - Best practices to adopt
   - Code examples for improvements
   - Priority levels for each issue

## Output

Present a comprehensive test quality assessment report with:

### Executive Summary

```
====================================================================
                    Test Quality Assessment
====================================================================

Overall Quality Grade:   C+  (71/100)
Total Tests:             342
Test Files:              48
Test Smells Found:       27

Quality Dimensions:
  Readability:           B  (78/100)  ✅ Good
  Maintainability:       C  (65/100)  ⚠️  Needs work
  Independence:          B+ (82/100)  ✅ Good
  Performance:           D  (58/100)  🔴 Slow tests
  Best Practices:        C+ (70/100)  ⚠️  Some issues

Status:                  NEEDS IMPROVEMENT
Priority Focus:          Fix test duplication and slow tests
====================================================================
```

### Quality Metrics

**Test Suite Statistics**:
- **Total Tests**: 342
- **Unit Tests**: 268 (78%)
- **Integration Tests**: 62 (18%)
- **E2E Tests**: 12 (4%)
- **Average Test Length**: 28 lines
- **Test-to-Code Ratio**: 1.8:1 (test lines / production lines)
- **Total Test Execution Time**: 2m 47s
- **Average Test Time**: 486ms

**Code Quality Metrics**:
- **Average Cyclomatic Complexity**: 3.2 (Good - target < 5)
- **Code Duplication**: 18% (High - target < 10%)
- **Assertion Density**: 2.1 assertions/test (Good)
- **Setup Complexity**: 8.3 lines average (Acceptable)

---

### Test Smells Detected (27)

#### Critical Test Smells (8)

**1. Mystery Guest - 5 occurrences**
**Severity**: HIGH
**Impact**: Tests depend on external resources without making dependencies explicit

**Location**: `tests/services/ConfigService.test.js:23`
```javascript
// SMELL: Mystery guest
test('should load API configuration', () => {
  const config = loadConfig();  // Reads from filesystem
  expect(config.apiKey).toBeDefined();
});
```

**Refactoring**:
```javascript
// FIXED: Explicit dependency injection
test('should load API configuration', () => {
  const mockFs = {
    readFileSync: jest.fn().mockReturnValue('{"apiKey": "test123"}')
  };
  const config = loadConfig(mockFs);
  expect(config.apiKey).toBe('test123');
});
```

**Also found in**:
- `tests/services/ConfigService.test.js:23, 45, 67`
- `tests/utils/FileReader.test.js:12, 34`

---

**2. Slow Tests - 3 test suites**
**Severity**: HIGH
**Impact**: Slow test execution reduces developer productivity

**Location**: `tests/integration/EmailService.test.js`
**Issue**: Integration tests using real SMTP server (15-20 seconds per test)

```javascript
// SMELL: Slow test using real email service
test('sends welcome email', async () => {
  await sendWelcomeEmail('user@example.com');
  await new Promise(resolve => setTimeout(resolve, 5000)); // Wait for email
  const emails = await checkInbox('user@example.com');
  expect(emails).toHaveLength(1);
}, 20000); // 20 second timeout
```

**Refactoring**:
```javascript
// FIXED: Fast test with mocked email service
test('sends welcome email', async () => {
  const mockMailer = jest.fn().mockResolvedValue({ messageId: '123' });
  await sendWelcomeEmail('user@example.com', mockMailer);

  expect(mockMailer).toHaveBeenCalledWith({
    to: 'user@example.com',
    template: 'welcome',
    data: expect.any(Object)
  });
}); // Runs in ~10ms
```

**Impact**: These 3 slow test suites add 2 minutes to total test time

---

**3. Test Code Duplication - 12 occurrences**
**Severity**: MEDIUM
**Impact**: Difficult to maintain, changes require updates in multiple places

**Location**: `tests/services/UserService.test.js`
```javascript
// SMELL: Repeated setup code
test('admin can create user', () => {
  const admin = { id: 1, role: 'admin', permissions: ['create'] };
  const userData = { email: 'new@example.com', name: 'User' };
  const result = createUser(admin, userData);
  expect(result).toBeDefined();
});

test('admin can delete user', () => {
  const admin = { id: 1, role: 'admin', permissions: ['create'] };
  const user = { id: 2, email: 'delete@example.com' };
  const result = deleteUser(admin, user);
  expect(result.success).toBe(true);
});

// Duplicated 10 more times...
```

**Refactoring**:
```javascript
// FIXED: Extract common test data
const createAdmin = () => ({
  id: 1,
  role: 'admin',
  permissions: ['create']
});

test('admin can create user', () => {
  const userData = { email: 'new@example.com', name: 'User' };
  const result = createUser(createAdmin(), userData);
  expect(result).toBeDefined();
});

test('admin can delete user', () => {
  const user = { id: 2, email: 'delete@example.com' };
  const result = deleteUser(createAdmin(), user);
  expect(result.success).toBe(true);
});
```

**Duplication Summary**:
- User test data: 12 duplications
- Mock database setup: 8 duplications
- API request setup: 6 duplications

---

#### Medium Priority Test Smells (14)

**4. Assertion Roulette - 7 occurrences**
Multiple assertions without clear context

**Location**: `tests/models/User.test.js:45`
```javascript
// SMELL: Multiple assertions without messages
test('creates valid user', () => {
  const user = new User({ email: 'test@example.com', password: 'pass123' });
  expect(user.id).toBeDefined();
  expect(user.email).toBe('test@example.com');
  expect(user.createdAt).toBeDefined();
  expect(user.password).not.toBe('pass123');
  expect(user.password.length).toBeGreaterThan(20);
});
```

**Refactoring**: Split into focused tests or add descriptive messages

---

**5. Eager Test - 4 occurrences**
Tests verify too many things at once

**Location**: `tests/workflows/UserRegistration.test.js:12`
```javascript
// SMELL: Testing entire user lifecycle in one test
test('complete user workflow', async () => {
  const user = await createUser({ email: 'test@example.com' });
  await verifyEmail(user.id, user.verificationToken);
  await updateProfile(user.id, { name: 'Updated' });
  await changePassword(user.id, 'newpass123');
  await deleteUser(user.id);
  // Too many actions in one test!
});
```

**Refactoring**: Split into separate focused tests for each action

---

**6. Conditional Test Logic - 3 occurrences**
Tests contain if/else or loops

**Location**: `tests/validators/InputValidator.test.js:23`
```javascript
// SMELL: Conditional logic in test
test('validates various inputs', () => {
  const inputs = [
    { value: 'test@example.com', valid: true },
    { value: 'invalid', valid: false }
  ];

  inputs.forEach(input => {
    const result = validate(input.value);
    if (input.valid) {
      expect(result.isValid).toBe(true);
    } else {
      expect(result.isValid).toBe(false);
    }
  });
});
```

**Refactoring**: Use parameterized tests or separate test cases

---

#### Low Priority Test Smells (5)

**7. Poor Test Names - 5 occurrences**
Test names are vague or don't describe behavior

Examples:
- `test('test1')` - tests/api/users.test.js:45
- `test('it works')` - tests/utils/helper.test.js:23
- `test('getUserById')` - tests/services/UserService.test.js:67

**Refactoring**: Use descriptive names explaining behavior and expectation

---

### Test Maintainability Issues

**High Complexity Tests (8)**

Tests with cyclomatic complexity > 5:

1. **tests/services/OrderService.test.js:89** - Complexity: 8
   - Multiple nested if statements
   - Complex setup logic
   - Recommendation: Split into smaller tests

2. **tests/integration/CheckoutFlow.test.js:45** - Complexity: 7
   - Testing multiple scenarios in one test
   - Recommendation: Use parameterized tests

**Long Tests (15)**

Tests exceeding 50 lines:

1. **tests/integration/PaymentFlow.test.js:23** - 78 lines
   - Excessive setup (40 lines)
   - Recommendation: Extract setup to helper function

2. **tests/e2e/UserRegistration.test.js:12** - 65 lines
   - Multiple assertions and verifications
   - Recommendation: Split into multiple E2E tests

---

### Test Independence Issues

**Shared State Problems (3)**

Tests that share mutable state:

**Location**: `tests/services/CacheService.test.js`
```javascript
// PROBLEM: Shared cache between tests
let cache = new Cache();

beforeAll(() => {
  cache.set('key1', 'value1');
});

test('retrieves cached value', () => {
  expect(cache.get('key1')).toBe('value1');
});

test('updates cached value', () => {
  cache.set('key1', 'updated'); // Affects other tests!
  expect(cache.get('key1')).toBe('updated');
});
```

**Fix**: Use `beforeEach` instead of `beforeAll` and create fresh instances

---

### Flaky Tests Detected (4)

Tests that fail intermittently:

1. **tests/api/RateLimiter.test.js:45** - Fails ~15% of the time
   - Issue: Timing-dependent, relies on setTimeout
   - Fix: Use fake timers (jest.useFakeTimers())

2. **tests/integration/DatabaseSync.test.js:23** - Fails ~10% of the time
   - Issue: Race condition in async operations
   - Fix: Proper async/await and promise handling

3. **tests/e2e/SearchFlow.test.js:67** - Fails ~8% of the time
   - Issue: Waiting for elements without proper retry
   - Fix: Use Playwright's auto-waiting or explicit wait conditions

---

### Test Performance Analysis

**Slowest Tests (Top 10)**:

1. `tests/integration/DatabaseMigration.test.js` - 45.2s
2. `tests/integration/EmailService.test.js` - 38.7s
3. `tests/e2e/CheckoutFlow.test.js` - 28.4s
4. `tests/integration/FileUpload.test.js` - 22.1s
5. `tests/integration/PaymentGateway.test.js` - 18.9s

**Total slow test time**: 153.3s (92% of total test time)

**Recommendations**:
- Mock external services instead of using real implementations
- Use test containers for database tests
- Parallelize E2E tests
- Consider running slow tests separately in CI

---

### Test Coverage vs Quality

```
File                         Coverage    Quality    Issue
---------------------------------------------------------------------------
src/auth/AuthService.js      95%         B          Good coverage, maintainable tests
src/payment/StripeService.js 58%         C-         Low coverage, test smells present
src/users/UserService.js     88%         D          High coverage, poor test quality
src/orders/OrderService.js   78%         B+         Decent coverage, good tests
```

**Insight**: High coverage doesn't always mean high-quality tests!
`UserService` has 88% coverage but tests are hard to maintain due to duplication and complexity.

---

### Best Practices Compliance

**Checklist Results**:

✅ **Following (70%):**
- Tests use AAA pattern (Arrange-Act-Assert)
- Most tests are independent
- Good use of mocks for external dependencies
- Proper cleanup in afterEach hooks
- Tests fail when they should

⚠️ **Partially Following (20%):**
- Test names mostly descriptive (some exceptions)
- Some code duplication in tests
- Most tests are fast (some slow outliers)

❌ **Not Following (10%):**
- Test fixtures not consistently used
- Some tests have conditional logic
- Flaky tests present
- Excessive test complexity in some cases

---

### Recommendations

#### Immediate Actions (This Week - Priority: HIGH)

1. **Fix Slow Tests** (Highest Priority)
   - Mock EmailService, FileService instead of real services
   - Expected improvement: Reduce test time from 2m 47s to ~45s
   - Estimated effort: 3-4 hours

2. **Remove Test Code Duplication**
   - Extract 12 duplicated test data factories
   - Create reusable test helpers
   - Estimated effort: 4-5 hours

3. **Fix Flaky Tests**
   - Use fake timers for timing-dependent tests
   - Add proper async/await handling
   - Add retry logic for E2E tests
   - Estimated effort: 2-3 hours

**Total effort**: 9-12 hours for immediate improvements

#### Short Term (Next Sprint)

4. Refactor complex tests (split eager tests, remove conditionals)
5. Improve test names for clarity
6. Extract shared setup to fixtures
7. Add missing test documentation

#### Long Term (Next Quarter)

8. Establish test quality gates in CI/CD
9. Add mutation testing for test effectiveness
10. Create test style guide and conventions
11. Regular test code reviews
12. Test refactoring sprints

---

### Test Quality Score Breakdown

```
Overall Quality Score: 71/100 (C+)

Component Scores:
  Test Structure:          78/100  (B)
  ├─ Organization:         85
  ├─ Naming:              75
  └─ AAA Pattern:         90

  Test Maintainability:    65/100  (C)
  ├─ Complexity:          70
  ├─ Duplication:         45  ⚠️
  ├─ Length:              72
  └─ Setup:               73

  Test Independence:       82/100  (B+)
  ├─ Isolation:           88
  ├─ Shared State:        75
  └─ Determinism:         85

  Test Performance:        58/100  (D)
  ├─ Execution Speed:     45  🔴
  ├─ Resource Usage:      68
  └─ Flakiness:          62

  Best Practices:          70/100  (C+)
  ├─ Mocking:            82
  ├─ Assertions:         73
  ├─ Fixtures:           58
  └─ Error Handling:     75
```

---

### Quality Improvement Roadmap

**Phase 1 (Week 1-2): Quick Wins**
- ✅ Fix 4 flaky tests
- ✅ Mock slow external services
- ✅ Remove obvious code duplication
- **Target**: Improve quality score to 78/100 (C+)

**Phase 2 (Week 3-4): Structural Improvements**
- ✅ Refactor complex tests
- ✅ Implement test fixtures
- ✅ Improve test naming
- **Target**: Improve quality score to 82/100 (B-)

**Phase 3 (Month 2): Best Practices**
- ✅ Establish test style guide
- ✅ Implement mutation testing
- ✅ Add quality gates to CI/CD
- **Target**: Improve quality score to 88/100 (B+)

**Phase 4 (Month 3): Excellence**
- ✅ Regular test refactoring
- ✅ Test code reviews
- ✅ Continuous monitoring
- **Target**: Achieve quality score of 90+/100 (A-)

---

## Examples

### Assess Overall Test Quality

```
/assess-test-quality

Analyze the entire test suite to identify test smells, quality
issues, and provide recommendations for improvement
```

### Assess Specific Module Tests

```
/assess-test-quality

Evaluate test quality specifically for the authentication module
tests (tests/auth/*), focusing on security test practices
```

### Focus on Performance

```
/assess-test-quality

Analyze test execution performance, identify slow tests, and
provide recommendations for speeding up the test suite
```

### Check for Test Smells

```
/assess-test-quality

Scan all tests for common test smells and anti-patterns like
mystery guest, assertion roulette, and conditional test logic
```

### Quality Before Refactoring

```
/assess-test-quality

Assess test quality before major refactoring to ensure tests
are maintainable and will support the refactoring safely
```

## Best Practices Applied

- **Comprehensive Analysis**: Multiple quality dimensions evaluated
- **Actionable Recommendations**: Specific improvements with examples
- **Prioritization**: Focus on high-impact issues first
- **Code Examples**: Before/after refactoring examples
- **Metrics-Driven**: Quantitative quality scores
- **Test Smell Detection**: Automated anti-pattern identification

## Integration with Other Commands

- Assess quality first with `/assess-test-quality`
- Fix coverage gaps with `/generate-tests`
- Verify improvements with `/analyze-coverage`
- Re-assess quality after refactoring

Provide comprehensive test quality assessment that enables systematic improvement of test suites toward maintainable, reliable, and fast tests.
