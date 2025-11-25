---
description: Generate comprehensive test suites for specified code including unit tests, integration tests, and test fixtures
---

Generate comprehensive test suites for your codebase, including unit tests, integration tests, and necessary test fixtures.

## Process

Follow these steps:

1. **Understand Code Context**: Analyze the code to be tested
   - Identify the testing framework in use (Jest, Vitest, pytest, etc.)
   - Understand code structure and dependencies
   - Review existing test patterns and conventions
   - Identify test file naming conventions
   - Check for existing test utilities and helpers

2. **Analyze Test Requirements**: Determine what needs testing
   - Public API surface (functions, methods, classes)
   - Input/output relationships
   - Edge cases and boundary conditions
   - Error handling paths
   - Integration points with external systems
   - Critical business logic
   - Security-sensitive code paths

3. **Launch Test Generator**: Use the `test-plugin:test-generator` agent to:
   - Generate unit tests for individual functions/methods
   - Create integration tests for component interactions
   - Generate test fixtures and factories for test data
   - Set up mocks and stubs for external dependencies
   - Create E2E tests for critical user flows (if applicable)
   - Ensure tests follow project conventions
   - Add appropriate test coverage

4. **Review Generated Tests**: Verify test quality
   - Tests are readable and maintainable
   - Proper use of arrange-act-assert pattern
   - Appropriate test coverage (happy path, edge cases, errors)
   - Tests are independent and isolated
   - Mocks/stubs used appropriately
   - Test names are descriptive

5. **Run Tests**: Execute the generated tests
   - Verify all tests pass
   - Check for any test failures or errors
   - Ensure tests run quickly (especially unit tests)
   - Fix any issues found

## Output

Present a comprehensive test generation report with:

### Summary
- **Files Analyzed**: Number of source files analyzed
- **Tests Generated**: Total number of test cases created
- **Test Types**: Unit, integration, E2E test counts
- **Coverage Added**: Estimated coverage improvement
- **Framework Used**: Testing framework and version

### Generated Tests

For each source file tested:

**Source File**: `src/services/UserService.js`
**Test File**: `src/services/UserService.test.js`
**Tests Created**: 12 unit tests, 3 integration tests

**Test Categories**:
- ✅ Happy path scenarios (5 tests)
- ✅ Input validation (4 tests)
- ✅ Error handling (3 tests)
- ✅ Edge cases (3 tests)

**Coverage**:
- Line Coverage: 95%
- Branch Coverage: 90%
- Function Coverage: 100%

### Test Files Created

List all test files with descriptions:

```
tests/
├── unit/
│   ├── UserService.test.js         # 12 unit tests for user operations
│   ├── PaymentService.test.js      # 10 unit tests for payment processing
│   └── ValidationUtils.test.js     # 15 unit tests for validators
├── integration/
│   ├── UserAPI.test.js             # 8 integration tests for user API
│   └── PaymentFlow.test.js         # 6 integration tests for checkout
├── e2e/
│   └── UserRegistration.e2e.js     # 3 E2E tests for registration flow
└── fixtures/
    ├── users.js                    # User test data factories
    └── orders.js                   # Order test data fixtures
```

### Key Test Examples

Show examples of important tests generated:

#### Unit Test Example
```javascript
describe('UserService.createUser', () => {
  it('should create user with valid data and hash password', async () => {
    // Arrange
    const userData = {
      email: 'test@example.com',
      name: 'Test User',
      password: 'SecurePass123!'
    };
    const mockDb = {
      findUser: jest.fn().mockResolvedValue(null),
      createUser: jest.fn().mockResolvedValue({ id: 1, ...userData })
    };
    const userService = new UserService(mockDb);

    // Act
    const result = await userService.createUser(userData);

    // Assert
    expect(result.id).toBe(1);
    expect(result.email).toBe(userData.email);
    expect(mockDb.createUser).toHaveBeenCalledWith(
      expect.objectContaining({
        email: userData.email,
        password: expect.not.stringMatching('SecurePass123!') // Password should be hashed
      })
    );
  });
});
```

#### Integration Test Example
```javascript
describe('User API Integration', () => {
  it('should complete full user registration flow', async () => {
    // Arrange
    const testDb = await createTestDatabase();
    const app = createApp(testDb);

    // Act
    const response = await request(app)
      .post('/api/users/register')
      .send({
        email: 'newuser@example.com',
        password: 'TestPass123!',
        name: 'New User'
      });

    // Assert
    expect(response.status).toBe(201);
    expect(response.body).toHaveProperty('id');

    // Verify user in database
    const user = await testDb.findUser({ email: 'newuser@example.com' });
    expect(user).toBeDefined();
    expect(user.email).toBe('newuser@example.com');

    // Cleanup
    await testDb.cleanup();
  });
});
```

### Test Utilities Created

**Fixtures and Factories**:
```javascript
// tests/fixtures/users.js
export const createTestUser = (overrides = {}) => ({
  id: 1,
  email: 'test@example.com',
  name: 'Test User',
  role: 'user',
  createdAt: new Date('2024-01-01'),
  ...overrides
});

export const createAdminUser = () => createTestUser({
  role: 'admin',
  permissions: ['read', 'write', 'delete']
});
```

### Next Steps

**Immediate Actions**:
1. Run test suite to verify all tests pass: `npm test`
2. Check coverage report: `npm run test:coverage`
3. Review and adjust any failing tests
4. Commit test files to version control

**Recommended Improvements**:
1. Add E2E tests for additional user flows
2. Increase coverage for edge cases in PaymentService
3. Add performance tests for critical operations
4. Set up mutation testing for test quality validation

**CI/CD Integration**:
```yaml
# Add to .github/workflows/test.yml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
      - run: npm ci
      - run: npm test
      - run: npm run test:coverage
```

## Examples

### Generate Tests for Specific File

```
/generate-tests

Generate comprehensive unit tests for src/services/UserService.js
including happy path, validation, error handling, and edge cases
```

### Generate Tests for Module

```
/generate-tests

Generate full test suite for the authentication module (src/auth/*)
including unit tests, integration tests, and security test cases
```

### Generate Tests with Coverage Target

```
/generate-tests

Generate tests for src/payment/ directory to achieve 90% coverage.
Focus on critical payment processing paths and error handling
```

### Generate E2E Tests

```
/generate-tests

Generate Playwright E2E tests for the user registration and login
flow, including form validation, success paths, and error scenarios
```

### Generate Tests for New Feature

```
/generate-tests

Generate complete test suite for the newly added shopping cart feature
(src/cart/*) including unit tests, integration tests with payment
service, and E2E checkout flow tests
```

## Best Practices Applied

- **Test Independence**: Each test can run in isolation
- **Clear Naming**: Test names describe behavior and expected outcome
- **AAA Pattern**: Arrange-Act-Assert structure for clarity
- **Proper Mocking**: External dependencies properly mocked
- **Test Coverage**: Happy path, edge cases, and errors all covered
- **Fast Execution**: Unit tests run in milliseconds
- **Maintainability**: Tests are easy to understand and modify
- **Fixtures**: Reusable test data factories for consistency

## Integration with Other Commands

- Generate tests first with `/generate-tests`
- Check coverage with `/analyze-coverage` to find gaps
- Improve test quality with `/assess-test-quality`
- Generate additional tests for uncovered areas

Generate production-ready, maintainable test suites that provide confidence in code correctness and prevent regressions.
