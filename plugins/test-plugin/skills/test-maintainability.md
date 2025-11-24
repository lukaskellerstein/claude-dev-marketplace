---
name: test-maintainability
description: Auto-invoked when writing or modifying tests to ensure tests are maintainable, readable, and follow best practices
allowed-tools: Read, Grep, Glob
---

# Test Maintainability Best Practices

This skill ensures tests remain maintainable, readable, and easy to modify as the codebase evolves.

## When Active

This skill activates when you:
- Write new tests
- Modify existing tests
- Refactor test code
- Notice test code duplication
- See complex test setup
- Find tests hard to understand
- Update tests after code changes

## Core Principles

### 1. Tests Are Code Too

Tests should be held to the same quality standards as production code:

- **Readable**: Easy to understand what is being tested
- **Maintainable**: Easy to modify when requirements change
- **DRY (Don't Repeat Yourself)**: Extract common patterns
- **SOLID Principles**: Apply good design principles
- **Simple**: Keep tests simple and focused

### 2. Test Maintainability Metrics

**Good Test Characteristics:**
- Complexity: Low (< 5 cyclomatic complexity)
- Length: Short (< 30 lines typically)
- Setup: Minimal (< 10 lines)
- Assertions: Focused (1-3 assertions)
- Dependencies: Few (isolated from other tests)
- Execution: Fast (milliseconds for unit tests)

## Maintainable Test Patterns

### Pattern 1: Extract Test Data Factories

**Problem**: Duplicated test data creation

```javascript
// ❌ BAD: Repeated test data
test('admin can approve post', () => {
  const admin = {
    id: 1,
    role: 'admin',
    permissions: ['read', 'write', 'approve']
  };
  const post = { id: 1, status: 'pending', title: 'Test Post' };
  // ... test logic
});

test('admin can reject post', () => {
  const admin = {
    id: 1,
    role: 'admin',
    permissions: ['read', 'write', 'approve']
  };
  const post = { id: 2, status: 'pending', title: 'Test Post' };
  // ... test logic
});
```

**Solution**: Extract to factory functions

```javascript
// ✅ GOOD: Reusable factories
// tests/fixtures/users.js
export const createUser = (overrides = {}) => ({
  id: 1,
  email: 'test@example.com',
  name: 'Test User',
  role: 'user',
  ...overrides
});

export const createAdmin = () => createUser({
  role: 'admin',
  permissions: ['read', 'write', 'approve']
});

// tests/fixtures/posts.js
export const createPost = (overrides = {}) => ({
  id: 1,
  title: 'Test Post',
  status: 'pending',
  content: 'Test content',
  ...overrides
});

// Usage in tests
import { createAdmin } from './fixtures/users';
import { createPost } from './fixtures/posts';

test('admin can approve post', () => {
  const admin = createAdmin();
  const post = createPost();
  const result = approvePost(admin, post);
  expect(result.status).toBe('approved');
});

test('admin can reject post', () => {
  const admin = createAdmin();
  const post = createPost();
  const result = rejectPost(admin, post);
  expect(result.status).toBe('rejected');
});
```

### Pattern 2: Builder Pattern for Complex Objects

**Problem**: Complex object creation clutters tests

```javascript
// ❌ BAD: Complex inline object creation
test('creates order with shipping', () => {
  const order = {
    id: 1,
    userId: 123,
    items: [
      { productId: 1, quantity: 2, price: 10.00 },
      { productId: 2, quantity: 1, price: 25.00 }
    ],
    total: 45.00,
    status: 'pending',
    shippingAddress: {
      street: '123 Main St',
      city: 'New York',
      state: 'NY',
      zipCode: '10001'
    },
    billingAddress: {
      street: '123 Main St',
      city: 'New York',
      state: 'NY',
      zipCode: '10001'
    },
    createdAt: new Date('2024-01-01')
  };
  // Test logic...
});
```

**Solution**: Use builder pattern

```javascript
// ✅ GOOD: Builder pattern
class OrderBuilder {
  constructor() {
    this.order = {
      id: 1,
      userId: 123,
      items: [],
      total: 0,
      status: 'pending',
      createdAt: new Date()
    };
  }

  withItem(productId, quantity, price) {
    this.order.items.push({ productId, quantity, price });
    this.order.total += quantity * price;
    return this;
  }

  withShipping(address) {
    this.order.shippingAddress = address;
    return this;
  }

  withBilling(address) {
    this.order.billingAddress = address;
    return this;
  }

  asPending() {
    this.order.status = 'pending';
    return this;
  }

  asCompleted() {
    this.order.status = 'completed';
    return this;
  }

  build() {
    return this.order;
  }
}

// Usage in tests
test('creates order with shipping', () => {
  const order = new OrderBuilder()
    .withItem(1, 2, 10.00)
    .withItem(2, 1, 25.00)
    .withShipping({ street: '123 Main St', city: 'New York' })
    .build();

  const result = processOrder(order);
  expect(result.status).toBe('confirmed');
});
```

### Pattern 3: Extract Setup to Helper Functions

**Problem**: Repeated setup code

```javascript
// ❌ BAD: Repeated database setup
test('creates user', async () => {
  const db = new Database();
  await db.connect();
  await db.clear();
  await db.seed({ users: [] });

  const result = await createUser({ email: 'test@example.com' });
  expect(result.id).toBeDefined();

  await db.close();
});

test('updates user', async () => {
  const db = new Database();
  await db.connect();
  await db.clear();
  await db.seed({ users: [{ id: 1, email: 'test@example.com' }] });

  const result = await updateUser(1, { name: 'Updated' });
  expect(result.name).toBe('Updated');

  await db.close();
});
```

**Solution**: Extract to setup helpers

```javascript
// ✅ GOOD: Reusable setup helpers
// tests/helpers/database.js
export async function setupTestDatabase(seedData = {}) {
  const db = new Database();
  await db.connect();
  await db.clear();
  await db.seed(seedData);
  return db;
}

export async function teardownTestDatabase(db) {
  await db.close();
}

// Usage in tests
import { setupTestDatabase, teardownTestDatabase } from './helpers/database';

describe('User operations', () => {
  let db;

  beforeEach(async () => {
    db = await setupTestDatabase();
  });

  afterEach(async () => {
    await teardownTestDatabase(db);
  });

  test('creates user', async () => {
    const result = await createUser({ email: 'test@example.com' });
    expect(result.id).toBeDefined();
  });

  test('updates user', async () => {
    await db.seed({ users: [{ id: 1, email: 'test@example.com' }] });
    const result = await updateUser(1, { name: 'Updated' });
    expect(result.name).toBe('Updated');
  });
});
```

### Pattern 4: Custom Matchers for Domain Logic

**Problem**: Complex assertions that are hard to read

```javascript
// ❌ BAD: Complex assertion logic
test('validates user data', () => {
  const user = createUser({ email: 'test@example.com' });

  expect(user.id).toBeDefined();
  expect(user.email).toBe('test@example.com');
  expect(user.createdAt).toBeInstanceOf(Date);
  expect(user.createdAt.getTime()).toBeLessThanOrEqual(Date.now());
  expect(user.password).not.toBe('plaintext');
  expect(user.password.length).toBeGreaterThan(20);
  expect(user.password).toMatch(/^\$2[aby]\$/);
});
```

**Solution**: Create custom matchers

```javascript
// ✅ GOOD: Custom matcher
// tests/matchers/userMatchers.js
export const userMatchers = {
  toBeValidUser(received) {
    const pass =
      received.id !== undefined &&
      received.email &&
      received.createdAt instanceof Date &&
      received.createdAt.getTime() <= Date.now();

    return {
      pass,
      message: () => pass
        ? `Expected user not to be valid`
        : `Expected user to be valid, but missing: ${this.utils.printReceived(received)}`
    };
  },

  toHaveHashedPassword(received) {
    const pass =
      received.password &&
      received.password.length > 20 &&
      /^\$2[aby]\$/.test(received.password);

    return {
      pass,
      message: () => pass
        ? `Expected password not to be hashed`
        : `Expected password to be hashed with bcrypt`
    };
  }
};

// Setup in test file
expect.extend(userMatchers);

// Usage in tests
test('validates user data', () => {
  const user = createUser({ email: 'test@example.com' });
  expect(user).toBeValidUser();
  expect(user).toHaveHashedPassword();
});
```

### Pattern 5: Page Object Model for E2E Tests

**Problem**: Duplicated UI interaction code

```javascript
// ❌ BAD: Repeated UI interactions
test('user can login', async ({ page }) => {
  await page.goto('https://app.example.com/login');
  await page.fill('[name="email"]', 'user@example.com');
  await page.fill('[name="password"]', 'password123');
  await page.click('button[type="submit"]');
  await page.waitForURL('**/dashboard');
  expect(page.url()).toContain('dashboard');
});

test('user can logout', async ({ page }) => {
  await page.goto('https://app.example.com/login');
  await page.fill('[name="email"]', 'user@example.com');
  await page.fill('[name="password"]', 'password123');
  await page.click('button[type="submit"]');
  await page.waitForURL('**/dashboard');
  await page.click('[data-testid="user-menu"]');
  await page.click('text=Logout');
  expect(page.url()).toContain('login');
});
```

**Solution**: Page Object Model

```javascript
// ✅ GOOD: Page Object Model
// tests/pages/LoginPage.js
export class LoginPage {
  constructor(page) {
    this.page = page;
    this.emailInput = page.locator('[name="email"]');
    this.passwordInput = page.locator('[name="password"]');
    this.submitButton = page.locator('button[type="submit"]');
  }

  async goto() {
    await this.page.goto('https://app.example.com/login');
  }

  async login(email, password) {
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
    await this.submitButton.click();
    await this.page.waitForURL('**/dashboard');
  }
}

// tests/pages/DashboardPage.js
export class DashboardPage {
  constructor(page) {
    this.page = page;
    this.userMenu = page.locator('[data-testid="user-menu"]');
    this.logoutLink = page.locator('text=Logout');
  }

  async logout() {
    await this.userMenu.click();
    await this.logoutLink.click();
  }
}

// Usage in tests
import { LoginPage } from './pages/LoginPage';
import { DashboardPage } from './pages/DashboardPage';

test('user can login', async ({ page }) => {
  const loginPage = new LoginPage(page);
  await loginPage.goto();
  await loginPage.login('user@example.com', 'password123');
  expect(page.url()).toContain('dashboard');
});

test('user can logout', async ({ page }) => {
  const loginPage = new LoginPage(page);
  await loginPage.goto();
  await loginPage.login('user@example.com', 'password123');

  const dashboardPage = new DashboardPage(page);
  await dashboardPage.logout();
  expect(page.url()).toContain('login');
});
```

## Test Organization

### File Structure
```
tests/
├── unit/                    # Fast, isolated unit tests
│   ├── services/
│   ├── utils/
│   └── models/
├── integration/             # Tests with dependencies
│   ├── api/
│   └── database/
├── e2e/                     # End-to-end tests
│   └── flows/
├── fixtures/                # Test data factories
│   ├── users.js
│   ├── orders.js
│   └── products.js
├── helpers/                 # Test utilities
│   ├── database.js
│   ├── mocks.js
│   └── assertions.js
├── pages/                   # Page objects for E2E
│   ├── LoginPage.js
│   └── DashboardPage.js
└── setup.js                 # Global test setup
```

### Naming Conventions

**Test Files:**
```
ProductService.js       → ProductService.test.js
userUtils.js           → userUtils.spec.js
ShoppingCart.ts        → ShoppingCart.test.ts
```

**Test Descriptions:**
```javascript
// ✅ GOOD: Descriptive, behavior-focused
describe('UserService.createUser', () => {
  it('should create user with valid email and password', () => {});
  it('should throw ValidationError when email format is invalid', () => {});
  it('should hash password before storing in database', () => {});
});

// ❌ BAD: Vague, implementation-focused
describe('createUser', () => {
  it('works', () => {});
  it('test1', () => {});
  it('calls bcrypt', () => {});
});
```

## Maintainability Checklist

When writing or reviewing tests:

### Readability
- [ ] **Clear Test Name**: Describes behavior and expected outcome
- [ ] **Obvious Intent**: Easy to understand what is being tested
- [ ] **Minimal Complexity**: No complex logic or conditionals
- [ ] **Good Comments**: Complex setup explained with comments

### Structure
- [ ] **AAA Pattern**: Arrange, Act, Assert clearly separated
- [ ] **Single Responsibility**: Tests one behavior
- [ ] **Focused Assertions**: 1-3 related assertions per test
- [ ] **Logical Grouping**: Related tests in describe blocks

### Reusability
- [ ] **No Duplication**: Common code extracted to helpers
- [ ] **Fixtures Used**: Test data from factories
- [ ] **Shared Setup**: BeforeEach/beforeAll for common setup
- [ ] **Custom Matchers**: Domain-specific assertions

### Independence
- [ ] **No Test Order Dependency**: Tests can run in any order
- [ ] **Proper Cleanup**: AfterEach/afterAll cleanup
- [ ] **Fresh Data**: Each test gets fresh test data
- [ ] **No Shared State**: No global variables modified

### Performance
- [ ] **Fast Execution**: Unit tests < 100ms
- [ ] **Minimal Setup**: Only necessary setup
- [ ] **Mocked Dependencies**: External services mocked
- [ ] **Parallel Safe**: Tests can run in parallel

## Common Maintainability Issues

### Issue 1: God Tests
Tests that do too much

```javascript
// ❌ BAD: Testing entire flow in one test
test('complete user lifecycle', async () => {
  const user = await createUser({ email: 'test@example.com' });
  await verifyEmail(user.id);
  const updated = await updateUser(user.id, { name: 'Updated' });
  await changePassword(user.id, 'newpass');
  await deleteUser(user.id);
  // Too much in one test!
});
```

**Fix**: Split into focused tests
```javascript
// ✅ GOOD: Separate focused tests
describe('User lifecycle', () => {
  test('should create user', async () => {
    const user = await createUser({ email: 'test@example.com' });
    expect(user.id).toBeDefined();
  });

  test('should verify email', async () => {
    const user = await createUser({ email: 'test@example.com' });
    await verifyEmail(user.id);
    const verified = await getUser(user.id);
    expect(verified.emailVerified).toBe(true);
  });

  // More focused tests...
});
```

### Issue 2: Brittle Tests
Tests break when unrelated things change

```javascript
// ❌ BAD: Testing internal implementation
test('should use bcrypt with 12 rounds', async () => {
  const spy = jest.spyOn(bcrypt, 'hash');
  await createUser({ password: 'test123' });
  expect(spy).toHaveBeenCalledWith('test123', 12);
});
```

**Fix**: Test behavior, not implementation
```javascript
// ✅ GOOD: Testing behavior
test('should hash password before saving', async () => {
  const user = await createUser({ password: 'plaintext' });
  expect(user.password).not.toBe('plaintext');
  expect(user.password.length).toBeGreaterThan(20);
  // Verify password can be validated
  const isValid = await verifyPassword('plaintext', user.password);
  expect(isValid).toBe(true);
});
```

### Issue 3: Complex Setup
Too much setup obscures the test

```javascript
// ❌ BAD: Complex inline setup
test('processes order', async () => {
  const db = new Database();
  await db.connect();
  await db.clear();
  const user = await db.insert('users', { email: 'test@example.com' });
  const product1 = await db.insert('products', { name: 'Widget', price: 10 });
  const product2 = await db.insert('products', { name: 'Gadget', price: 20 });
  const cart = await db.insert('carts', { userId: user.id });
  await db.insert('cart_items', { cartId: cart.id, productId: product1.id, qty: 2 });
  await db.insert('cart_items', { cartId: cart.id, productId: product2.id, qty: 1 });

  const order = await processOrder(cart.id);
  expect(order.total).toBe(40);
});
```

**Fix**: Extract setup to helper
```javascript
// ✅ GOOD: Clean setup with helpers
async function setupOrderTest() {
  const user = await createTestUser();
  const products = await createTestProducts([
    { name: 'Widget', price: 10 },
    { name: 'Gadget', price: 20 }
  ]);
  const cart = await createTestCart(user, [
    { product: products[0], quantity: 2 },
    { product: products[1], quantity: 1 }
  ]);
  return { user, products, cart };
}

test('processes order', async () => {
  const { cart } = await setupOrderTest();
  const order = await processOrder(cart.id);
  expect(order.total).toBe(40);
});
```

## Quick Reference

### Maintainable Test Principles
1. **DRY**: Don't Repeat Yourself - extract common code
2. **KISS**: Keep It Simple, Stupid - avoid complexity
3. **Clear Intent**: Test name + code clearly shows purpose
4. **Independent**: Each test stands alone
5. **Fast**: Quick execution enables frequent running
6. **Focused**: One behavior per test

### Extract When You See
- Same setup in multiple tests → Extract to beforeEach or helper
- Repeated test data → Create factory or fixture
- Complex assertions → Create custom matcher
- Duplicated interactions → Create helper function or page object
- Multiple steps repeated → Extract to test utility

### Good Test Structure
```javascript
describe('ComponentName', () => {
  // Shared setup
  let dependency;

  beforeEach(() => {
    dependency = createMockDependency();
  });

  describe('methodName', () => {
    it('should do X when Y', () => {
      // Arrange: Minimal, focused setup
      const input = createTestInput();

      // Act: One clear action
      const result = method(input);

      // Assert: Clear expectation
      expect(result).toMatchExpectedOutcome();
    });
  });
});
```

Apply these maintainability practices to keep tests clean, understandable, and easy to modify as the codebase evolves.
