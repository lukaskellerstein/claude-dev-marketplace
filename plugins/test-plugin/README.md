# Test Plugin

Comprehensive testing toolkit for test generation, coverage analysis, test quality assessment, and quality assurance automation. Supports unit testing, integration testing, E2E testing, and test-driven development workflows.

## Features

### Agents

- **test-generator**: Expert in generating comprehensive test suites including unit tests, integration tests, E2E tests, and test fixtures for various frameworks (Jest, Vitest, pytest, JUnit, etc.)
- **coverage-analyzer**: Expert in analyzing test coverage, identifying gaps, generating coverage reports, and improving test suite quality metrics
- **test-quality-expert**: Expert in assessing test quality, identifying test smells, refactoring tests, and establishing testing best practices and standards

### Commands

- `/generate-tests`: Generate comprehensive test suites for specified code including unit tests, integration tests, and test fixtures
- `/analyze-coverage`: Analyze test coverage, identify gaps, generate coverage reports, and provide recommendations for improving coverage
- `/assess-test-quality`: Assess test suite quality, identify test smells, evaluate test maintainability, and provide refactoring recommendations

### Skills

- **test-first-development**: Auto-invoked when writing new code to encourage test-first development and ensure proper test coverage for new features
- **test-maintainability**: Auto-invoked when writing or modifying tests to ensure tests are maintainable, readable, and follow best practices

## Usage

### Generate Comprehensive Test Suite

```
/generate-tests

Generate comprehensive unit tests for src/services/UserService.js
including happy path, validation, error handling, and edge cases
```

**What it does:**
- Analyzes source code structure and dependencies
- Identifies functions, methods, and classes to test
- Generates unit tests with proper mocking
- Creates integration tests for component interactions
- Sets up test fixtures and factories
- Ensures tests follow project conventions
- Provides coverage estimates

**Example Output:**
```
Generated 15 tests for UserService:
✅ 5 unit tests for createUser (happy path, validation, errors)
✅ 4 unit tests for updateUser
✅ 3 unit tests for deleteUser
✅ 3 integration tests for user lifecycle

Coverage Added:
- Line Coverage: 95%
- Branch Coverage: 90%
- Function Coverage: 100%

Test Files Created:
- tests/unit/services/UserService.test.js
- tests/integration/UserAPI.test.js
- tests/fixtures/users.js
```

---

### Analyze Test Coverage

```
/analyze-coverage

Analyze complete test coverage for the project, identify gaps,
and provide prioritized recommendations for improvement
```

**What it does:**
- Runs test suite with coverage collection
- Generates HTML, LCOV, and JSON coverage reports
- Identifies completely uncovered files
- Finds functions with low/no coverage
- Highlights missing branch coverage
- Prioritizes gaps by business impact
- Provides specific test recommendations

**Example Output:**
```
Coverage Analysis Report:

Overall Coverage: 76.5% (Target: 80%)
Critical Gaps: 8
Uncovered Functions: 23
Missing Branches: 45

Critical Gaps:
🔴 src/payment/StripeService.js - 55.8% coverage
   Lines 45-89: Payment processing untested
   Recommendation: Add 12-15 tests for payment flows

🔴 src/auth/AuthService.js - 62.3% coverage
   Lines 67-84: Password reset logic untested
   Recommendation: Add 10-12 tests for auth flows

Immediate Actions:
1. Add payment processing tests (4-6 hours)
2. Cover authentication error paths (3-4 hours)
3. Test validation logic (4-5 hours)
```

---

### Assess Test Quality

```
/assess-test-quality

Analyze the entire test suite to identify test smells, quality
issues, and provide recommendations for improvement
```

**What it does:**
- Scans tests for common test smells
- Evaluates test maintainability
- Identifies flaky tests
- Checks test performance
- Analyzes test complexity
- Detects code duplication in tests
- Provides refactoring recommendations

**Example Output:**
```
Test Quality Assessment:

Overall Grade: C+ (71/100)
Total Tests: 342
Test Smells: 27

Critical Issues:
⚠️  Slow Tests (3 suites) - Add 2 minutes to test time
⚠️  Test Duplication (12 occurrences) - Hard to maintain
⚠️  Mystery Guest (5 tests) - External dependencies unclear

Quality Metrics:
- Readability: B (78/100)
- Maintainability: C (65/100)
- Independence: B+ (82/100)
- Performance: D (58/100)

Recommendations:
1. Mock EmailService to speed up tests (-2 minutes)
2. Extract repeated test data to factories
3. Fix 4 flaky tests
```

---

### Use Agents Directly

Invoke specialized agents for focused work:

- "Use test-generator to create comprehensive unit tests for the authentication module"
- "Use coverage-analyzer to identify critical coverage gaps in payment processing"
- "Use test-quality-expert to refactor tests and remove test smells"

---

## Testing Coverage

### Supported Testing Frameworks

**JavaScript/TypeScript:**
- Jest - Most popular React/Node.js testing framework
- Vitest - Fast Vite-native testing framework
- Mocha + Chai - Flexible test framework and assertion library
- Jasmine - BDD framework for browser and Node.js
- Playwright - Modern E2E testing framework
- Cypress - End-to-end testing framework
- Testing Library - React, Vue, Angular component testing

**Python:**
- pytest - De facto standard Python testing framework
- unittest - Python built-in testing framework
- nose2 - Extends unittest with plugins
- pytest-cov - Coverage plugin for pytest

**Go:**
- testing - Go standard library testing
- testify - Popular assertion and mocking library
- Ginkgo - BDD testing framework
- GoConvey - BDD framework with web UI

**Java:**
- JUnit 5 - Standard Java testing framework
- TestNG - Testing framework with advanced features
- Mockito - Mocking framework
- AssertJ - Fluent assertion library

**Ruby:**
- RSpec - BDD testing framework
- Minitest - Ruby standard library testing

### Test Types Supported

**Unit Tests:**
- Fast, isolated tests for individual functions/methods
- Mocking external dependencies
- Testing business logic
- Input validation testing
- Error handling verification

**Integration Tests:**
- Testing component interactions
- Database integration testing
- API endpoint testing
- Message broker testing
- File system operations
- Third-party service integration

**End-to-End (E2E) Tests:**
- Complete user flow testing
- Browser automation (Playwright, Cypress)
- Multi-step workflows
- Cross-browser testing
- Visual regression testing

**Property-Based Tests:**
- Generative testing with random inputs
- Testing invariants and properties
- Using fast-check, Hypothesis, QuickCheck

**Contract Tests:**
- Consumer-driven contract testing
- API contract validation
- Service integration contracts

---

## Test Generation Examples

### Generate Unit Tests for Service Class

```
/generate-tests

Generate complete unit test suite for src/services/OrderService.js
covering all public methods, edge cases, and error handling
```

**Generated Tests:**
```javascript
// tests/services/OrderService.test.js
describe('OrderService', () => {
  describe('createOrder', () => {
    it('should create order with valid items', async () => {
      // Arrange
      const mockDb = {
        createOrder: jest.fn().mockResolvedValue({ id: 1 })
      };
      const service = new OrderService(mockDb);
      const orderData = {
        userId: 1,
        items: [{ productId: 1, quantity: 2, price: 10 }]
      };

      // Act
      const result = await service.createOrder(orderData);

      // Assert
      expect(result.id).toBe(1);
      expect(mockDb.createOrder).toHaveBeenCalledWith(
        expect.objectContaining({
          userId: 1,
          items: expect.any(Array),
          total: 20
        })
      );
    });

    it('should throw error for empty order', async () => {
      const service = new OrderService();
      await expect(service.createOrder({ items: [] }))
        .rejects.toThrow('Order must contain at least one item');
    });

    it('should calculate total correctly', async () => {
      const service = new OrderService();
      const orderData = {
        items: [
          { productId: 1, quantity: 2, price: 10 },
          { productId: 2, quantity: 1, price: 25 }
        ]
      };
      const result = await service.createOrder(orderData);
      expect(result.total).toBe(45);
    });
  });
});
```

---

### Generate Integration Tests

```
/generate-tests

Generate integration tests for the authentication API endpoints
including registration, login, password reset, and token refresh
```

**Generated Tests:**
```javascript
// tests/integration/AuthAPI.test.js
describe('Authentication API', () => {
  let app;
  let db;

  beforeEach(async () => {
    db = await createTestDatabase();
    app = createApp(db);
  });

  afterEach(async () => {
    await db.cleanup();
  });

  describe('POST /api/auth/register', () => {
    it('should register new user with valid data', async () => {
      const response = await request(app)
        .post('/api/auth/register')
        .send({
          email: 'newuser@example.com',
          password: 'SecurePass123!',
          name: 'New User'
        });

      expect(response.status).toBe(201);
      expect(response.body).toMatchObject({
        user: {
          email: 'newuser@example.com',
          name: 'New User'
        },
        token: expect.any(String)
      });

      // Verify user in database
      const user = await db.findUser({ email: 'newuser@example.com' });
      expect(user).toBeDefined();
      expect(user.password).not.toBe('SecurePass123!'); // Should be hashed
    });

    it('should reject duplicate email', async () => {
      await db.seed({ users: [{ email: 'existing@example.com' }] });

      const response = await request(app)
        .post('/api/auth/register')
        .send({
          email: 'existing@example.com',
          password: 'Pass123!',
          name: 'User'
        });

      expect(response.status).toBe(400);
      expect(response.body.error).toContain('already exists');
    });
  });
});
```

---

### Generate E2E Tests

```
/generate-tests

Generate Playwright E2E tests for the complete user registration
and login flow, including form validation and error scenarios
```

**Generated Tests:**
```javascript
// tests/e2e/UserRegistration.e2e.js
import { test, expect } from '@playwright/test';

test.describe('User Registration Flow', () => {
  test('should complete successful registration', async ({ page }) => {
    // Navigate to registration page
    await page.goto('https://app.example.com/register');

    // Fill registration form
    await page.fill('[name="email"]', 'newuser@example.com');
    await page.fill('[name="password"]', 'SecurePass123!');
    await page.fill('[name="confirmPassword"]', 'SecurePass123!');
    await page.fill('[name="name"]', 'New User');

    // Submit form
    await page.click('button[type="submit"]');

    // Verify redirect to dashboard
    await expect(page).toHaveURL(/.*dashboard/);
    await expect(page.locator('h1')).toContainText('Welcome, New User');
  });

  test('should show validation errors for invalid email', async ({ page }) => {
    await page.goto('https://app.example.com/register');

    await page.fill('[name="email"]', 'invalid-email');
    await page.fill('[name="password"]', 'Pass123!');
    await page.click('button[type="submit"]');

    await expect(page.locator('.error-email')).toContainText('Invalid email format');
  });

  test('should show error when passwords do not match', async ({ page }) => {
    await page.goto('https://app.example.com/register');

    await page.fill('[name="password"]', 'Pass123!');
    await page.fill('[name="confirmPassword"]', 'DifferentPass123!');
    await page.click('button[type="submit"]');

    await expect(page.locator('.error-password')).toContainText('Passwords must match');
  });
});
```

---

## Coverage Analysis Examples

### Analyze Coverage with Prioritization

```
/analyze-coverage

Focus analysis on critical business paths: authentication,
payment processing, and order management. Identify gaps in
these high-risk areas
```

**Output:**
```
Critical Path Coverage Analysis:

Authentication Module (src/auth/):
- Overall: 62.3% ⚠️
- Critical Gaps:
  * Password reset: 0% coverage (HIGH RISK)
  * Token refresh: 45% coverage
  * MFA verification: 30% coverage

Payment Processing (src/payment/):
- Overall: 55.8% 🔴
- Critical Gaps:
  * Card processing: 48% coverage (CRITICAL)
  * Refund logic: 0% coverage (HIGH RISK)
  * Webhook handling: 0% coverage (HIGH RISK)

Order Management (src/orders/):
- Overall: 78.9% ✅
- Minor Gaps:
  * Order cancellation: 65% coverage
  * Inventory updates: 72% coverage

Priority Actions:
1. 🔴 CRITICAL: Test payment card processing (Est: 4-6 hours)
2. 🔴 CRITICAL: Test refund calculations (Est: 3-4 hours)
3. ⚠️  HIGH: Test password reset flow (Est: 2-3 hours)
4. ⚠️  HIGH: Test webhook processing (Est: 2-3 hours)
```

---

### Coverage Trend Analysis

```
/analyze-coverage

Generate coverage report and compare with last week's coverage
to show improvements and regressions
```

**Output:**
```
Coverage Trends (Last 4 Weeks):

Week 1: 72.3%
Week 2: 74.8% (+2.5% ⬆️)
Week 3: 76.1% (+1.3% ⬆️)
Week 4: 76.5% (+0.4% ⬆️)

Trend: Coverage improvements slowing

Module Changes:
✅ UserService: 85% → 92% (+7%)
✅ OrderService: 74% → 81% (+7%)
⚠️  PaymentService: 58% → 56% (-2% ⬇️)
⚠️  AuthService: 64% → 62% (-2% ⬇️)

Recommendations:
- Focus on PaymentService and AuthService (declining coverage)
- Set minimum 80% threshold for new code
- Add pre-commit hook to check coverage
```

---

## Test Quality Assessment Examples

### Identify and Fix Test Smells

```
/assess-test-quality

Scan all tests for common test smells and anti-patterns like
mystery guest, assertion roulette, and conditional test logic
```

**Output:**
```
Test Smells Detected: 27

Critical Smells (8):
1. Mystery Guest - 5 occurrences
   Location: tests/services/ConfigService.test.js:23
   Issue: Test depends on external file without explicit dependency
   Fix: Use dependency injection and mocks

2. Slow Tests - 3 test suites
   Location: tests/integration/EmailService.test.js
   Issue: Tests use real SMTP (15-20 seconds per test)
   Fix: Mock email service, reduce from 2m to ~10s

3. Test Duplication - 12 occurrences
   Location: tests/services/UserService.test.js
   Issue: Repeated user creation code
   Fix: Extract to factory function

Medium Priority (14):
4. Assertion Roulette - 7 occurrences
   Fix: Split into focused tests or add clear messages

5. Eager Test - 4 occurrences
   Fix: Split tests testing multiple behaviors

6. Conditional Logic - 3 occurrences
   Fix: Use parameterized tests or separate cases

Refactoring Examples Provided:
✅ Before/after code for each smell
✅ Estimated effort for each fix
✅ Priority recommendations
```

---

### Performance Analysis

```
/assess-test-quality

Analyze test execution performance, identify slow tests, and
provide recommendations for speeding up the test suite
```

**Output:**
```
Test Performance Analysis:

Total Execution Time: 2m 47s
Unit Tests: 268 tests in 12.4s (46ms average)
Integration Tests: 62 tests in 2m 15s (2.2s average) ⚠️
E2E Tests: 12 tests in 19.2s (1.6s average)

Slowest Tests (Top 10):
1. DatabaseMigration.test.js - 45.2s 🔴
2. EmailService.test.js - 38.7s 🔴
3. CheckoutFlow.e2e.js - 28.4s
4. FileUpload.test.js - 22.1s
5. PaymentGateway.test.js - 18.9s

Recommendations:
1. Mock EmailService → Save 38s
   - Replace real SMTP with mock
   - Estimated effort: 1-2 hours

2. Use Test Containers → Save 45s
   - Replace real migrations with fixtures
   - Estimated effort: 2-3 hours

3. Parallelize E2E Tests → Save 15s
   - Run E2E tests in parallel
   - Estimated effort: 1 hour

Total Time Savings: ~98 seconds (59% faster)
New Total Time: ~69 seconds ✅
```

---

## Test-Driven Development (TDD)

### Red-Green-Refactor Cycle

The plugin encourages test-first development:

**1. RED - Write Failing Test:**
```javascript
test('should calculate discount for premium members', () => {
  const order = { total: 100 };
  const customer = { tier: 'premium' };
  const result = calculateDiscount(order, customer);
  expect(result.finalTotal).toBe(80); // 20% discount
});
// FAIL: calculateDiscount is not defined
```

**2. GREEN - Make It Pass:**
```javascript
function calculateDiscount(order, customer) {
  const discount = customer.tier === 'premium' ? 0.20 : 0.10;
  return {
    finalTotal: order.total * (1 - discount)
  };
}
// PASS: Test now passes
```

**3. REFACTOR - Improve Code:**
```javascript
const DISCOUNTS = {
  premium: 0.20,
  regular: 0.10,
  vip: 0.30
};

function calculateDiscount(order, customer) {
  const discount = DISCOUNTS[customer.tier] || 0;
  return {
    discountAmount: order.total * discount,
    finalTotal: order.total * (1 - discount)
  };
}
// PASS: Tests still pass after refactoring
```

---

## Testing Best Practices

### Unit Test Principles

**Fast, Independent, Repeatable, Self-Validating, Timely (FIRST):**

```javascript
// ✅ GOOD: Fast, focused unit test
test('should validate email format', () => {
  expect(isValidEmail('test@example.com')).toBe(true);
  expect(isValidEmail('invalid')).toBe(false);
}); // Runs in <1ms

// ❌ BAD: Slow test with external dependencies
test('should validate email', async () => {
  const result = await checkEmailWithAPI('test@example.com');
  expect(result.valid).toBe(true);
}); // Runs in 2000ms, depends on external API
```

### Arrange-Act-Assert Pattern

```javascript
test('should create order with items', () => {
  // Arrange: Set up test data
  const items = [
    { productId: 1, quantity: 2, price: 10 },
    { productId: 2, quantity: 1, price: 20 }
  ];

  // Act: Execute the code being tested
  const order = createOrder(items);

  // Assert: Verify expected outcome
  expect(order.total).toBe(40);
  expect(order.items).toHaveLength(2);
});
```

### Test Data Management

```javascript
// Use factories for consistent test data
const UserFactory = {
  create: (overrides = {}) => ({
    id: 1,
    email: 'test@example.com',
    name: 'Test User',
    role: 'user',
    ...overrides
  }),

  createAdmin: () => UserFactory.create({
    role: 'admin',
    permissions: ['read', 'write', 'delete']
  })
};

// Usage in tests
test('admin can delete users', () => {
  const admin = UserFactory.createAdmin();
  const result = deleteUser(admin, targetUserId);
  expect(result.success).toBe(true);
});
```

### Mocking Best Practices

```javascript
// ✅ GOOD: Mock external dependencies
test('should send welcome email', async () => {
  const mockMailer = jest.fn().mockResolvedValue({ messageId: '123' });
  await registerUser({ email: 'test@example.com' }, mockMailer);

  expect(mockMailer).toHaveBeenCalledWith({
    to: 'test@example.com',
    template: 'welcome',
    data: expect.any(Object)
  });
});

// ❌ BAD: Don't mock what you're testing
test('should calculate total', () => {
  const mockCalculate = jest.fn().mockReturnValue(100);
  // This tests the mock, not the actual function!
});
```

---

## Integration with CI/CD

### GitHub Actions Example

```yaml
name: Tests and Coverage

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: Install dependencies
        run: npm ci

      - name: Run tests
        run: npm test

      - name: Run tests with coverage
        run: npm run test:coverage

      - name: Check coverage thresholds
        run: |
          npm run test:coverage -- --coverageThreshold='{"global":{"lines":80,"branches":80,"functions":80,"statements":80}}'

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage/coverage-final.json
          fail_ci_if_error: true

      - name: Comment PR with coverage
        uses: romeovs/lcov-reporter-action@v0.3.1
        with:
          lcov-file: ./coverage/lcov.info
          github-token: ${{ secrets.GITHUB_TOKEN }}
```

### Coverage Badges

Add to your README:
```markdown
![Coverage](https://img.shields.io/codecov/c/github/username/repo)
![Tests](https://github.com/username/repo/workflows/Tests/badge.svg)
```

---

## Example Workflows

### Workflow 1: Test-Driven Development for New Feature

**1. Generate Test Structure**
```
/generate-tests

Create test structure for new shopping cart feature including
unit tests for cart operations and integration tests for checkout
```

**2. Write Tests First (TDD)**
- Write failing tests for each function
- Implement minimal code to pass tests
- Refactor and improve

**3. Verify Coverage**
```
/analyze-coverage

Verify the new shopping cart feature has complete test coverage
```

**4. Assess Quality**
```
/assess-test-quality

Ensure the new tests follow best practices and are maintainable
```

---

### Workflow 2: Legacy Code Testing

**1. Analyze Current Coverage**
```
/analyze-coverage

Analyze coverage for the legacy payment module and identify
the most critical gaps that need tests
```

**2. Generate Missing Tests**
```
/generate-tests

Generate tests for the highest priority uncovered code in the
payment module, focusing on critical business logic
```

**3. Run and Refine**
- Run generated tests
- Fix any failures
- Adjust tests as needed

**4. Verify Improvement**
```
/analyze-coverage

Verify coverage improved for the payment module after adding tests
```

---

### Workflow 3: Test Suite Refactoring

**1. Assess Current Quality**
```
/assess-test-quality

Analyze all tests to identify test smells, slow tests, and
maintainability issues
```

**2. Prioritize Fixes**
- Focus on critical issues first
- Fix slow tests
- Remove test duplication
- Refactor complex tests

**3. Re-assess Quality**
```
/assess-test-quality

Verify test quality improved after refactoring
```

**4. Monitor Ongoing**
- Set up quality gates in CI/CD
- Regular test code reviews
- Continuous refactoring

---

### Workflow 4: Pre-Production Testing

**1. Full Coverage Analysis**
```
/analyze-coverage

Perform final coverage analysis before production deployment
focusing on critical business paths
```

**2. Quality Assessment**
```
/assess-test-quality

Assess test suite quality to ensure tests are reliable and
maintainable for production support
```

**3. Generate Missing Tests**
```
/generate-tests

Generate any critical missing tests identified in the analysis
```

**4. Final Verification**
- Run full test suite
- Verify all tests pass
- Check coverage thresholds met
- Review test quality metrics

---

## Testing Tools Integration

### Coverage Tools
- **Jest**: Built-in coverage with Istanbul
- **Vitest**: Built-in coverage with v8 or Istanbul
- **pytest-cov**: Coverage for Python tests
- **go test -cover**: Built-in Go coverage
- **JaCoCo**: Java code coverage

### Mutation Testing
- **Stryker**: JavaScript/TypeScript mutation testing
- **PITest**: Java mutation testing
- **mutmut**: Python mutation testing
- **go-mutesting**: Go mutation testing

### Test Automation
- **GitHub Actions**: Automated test runs on push/PR
- **GitLab CI**: Continuous testing pipeline
- **Jenkins**: Enterprise CI/CD with testing
- **CircleCI**: Cloud-based testing automation

### Coverage Services
- **Codecov**: Coverage reporting and tracking
- **Coveralls**: Coverage history and badges
- **SonarQube**: Code quality and coverage analysis

---

## Test Quality Metrics

### Coverage Targets
- **Line Coverage**: 80%+ (90%+ for critical code)
- **Branch Coverage**: 80%+ (all paths tested)
- **Function Coverage**: 85%+ (all public functions)
- **Mutation Score**: 70%+ (test effectiveness)

### Quality Targets
- **Test Execution Time**: <2 minutes for unit tests
- **Flakiness Rate**: <1% of tests
- **Test-to-Code Ratio**: 1:1 to 3:1
- **Test Complexity**: <5 cyclomatic complexity
- **Test Length**: <30 lines average

---

## Integration with Other Plugins

- **backend-plugin**: Test API endpoints, services, and middleware
- **frontend-plugin**: Test React components, hooks, and UI logic
- **database-plugin**: Integration tests with database operations
- **cicd-plugin**: Automated testing in CI/CD pipelines
- **security-plugin**: Security testing and vulnerability verification

---

## Resources & References

### Testing Frameworks Documentation
- [Jest](https://jestjs.io/) - JavaScript testing framework
- [Vitest](https://vitest.dev/) - Vite-native testing framework
- [pytest](https://docs.pytest.org/) - Python testing framework
- [Playwright](https://playwright.dev/) - E2E testing framework
- [Cypress](https://www.cypress.io/) - E2E testing framework

### Testing Best Practices
- [Testing Library](https://testing-library.com/) - Testing best practices
- [Test Driven Development by Kent Beck](https://www.amazon.com/Test-Driven-Development-Kent-Beck/dp/0321146530)
- [xUnit Test Patterns](http://xunitpatterns.com/)

### Coverage Tools
- [Istanbul](https://istanbul.js.org/) - JavaScript code coverage
- [Coverage.py](https://coverage.readthedocs.io/) - Python coverage
- [JaCoCo](https://www.jacoco.org/) - Java code coverage

---

## Support & Troubleshooting

### Common Issues

**Tests Running Slowly**
- Mock external services instead of using real ones
- Use test containers for databases
- Run tests in parallel
- Optimize test setup and teardown

**Low Coverage Despite Many Tests**
- Tests may not be testing the right things
- Check for test smells (testing mocks instead of code)
- Use coverage reports to find gaps
- Focus on branch coverage, not just line coverage

**Flaky Tests**
- Remove timing dependencies (use fake timers)
- Ensure proper async/await handling
- Fix race conditions
- Ensure test independence (no shared state)

**Tests Hard to Maintain**
- Extract test data to factories
- Use Page Object Model for E2E tests
- Remove test code duplication
- Follow AAA pattern consistently

### Getting Help

For testing issues:
1. Run `/analyze-coverage` to understand coverage gaps
2. Run `/assess-test-quality` to identify test problems
3. Use `/generate-tests` to create missing tests
4. Review test best practices in skills documentation
5. Consult testing framework documentation

---

**Testing is an investment in code quality and confidence.** Use this plugin to build comprehensive, maintainable test suites that catch bugs early and support rapid, safe development.
