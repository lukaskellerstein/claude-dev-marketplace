---
name: test-first-development
description: Auto-invoked when writing new code to encourage test-first development and ensure proper test coverage for new features
allowed-tools: Read, Grep, Glob
---

# Test-First Development Best Practices

This skill provides guidance on test-driven development (TDD) and ensures new code is properly tested.

## When Active

This skill activates when you:
- Write new functions, methods, or classes
- Add new features or functionality
- Implement business logic
- Create API endpoints
- Add data validation or processing
- Implement algorithms or calculations
- Make significant code changes

## Core Principles

### 1. Test-Driven Development (TDD) Cycle

The Red-Green-Refactor cycle:

```
1. RED: Write a failing test first
   - Think about the desired behavior
   - Write the test for that behavior
   - Run the test and see it fail (red)

2. GREEN: Write minimal code to pass the test
   - Implement just enough to make the test pass
   - Don't worry about perfection yet
   - Run the test and see it pass (green)

3. REFACTOR: Improve the code
   - Clean up duplication
   - Improve design
   - Optimize if needed
   - Ensure tests still pass
```

### 2. Benefits of Test-First Development

- **Better Design**: Writing tests first forces you to think about API design
- **Confidence**: Tests provide safety net for refactoring
- **Documentation**: Tests serve as executable documentation
- **Fewer Bugs**: Catch issues early in development
- **Faster Development**: Less time debugging, more time building
- **Complete Coverage**: Tests cover all scenarios, not just happy paths

## Test-First Workflow

### Writing a New Function

**Step 1: Write the test first**

```javascript
// tests/services/DiscountService.test.js
import { calculateDiscount } from '../services/DiscountService';

describe('calculateDiscount', () => {
  it('should apply 10% discount for regular customers', () => {
    // Arrange
    const order = { total: 100, customerId: 1 };
    const customer = { id: 1, tier: 'regular' };

    // Act
    const result = calculateDiscount(order, customer);

    // Assert
    expect(result.discountAmount).toBe(10);
    expect(result.finalTotal).toBe(90);
  });

  it('should apply 20% discount for premium customers', () => {
    const order = { total: 100, customerId: 2 };
    const customer = { id: 2, tier: 'premium' };

    const result = calculateDiscount(order, customer);

    expect(result.discountAmount).toBe(20);
    expect(result.finalTotal).toBe(80);
  });

  it('should throw error for invalid order total', () => {
    const order = { total: -10, customerId: 1 };
    const customer = { id: 1, tier: 'regular' };

    expect(() => calculateDiscount(order, customer)).toThrow('Invalid order total');
  });
});
```

**Step 2: Run the test - it should fail**
```bash
npm test
# FAIL: calculateDiscount is not defined
```

**Step 3: Write minimal implementation**

```javascript
// src/services/DiscountService.js
export function calculateDiscount(order, customer) {
  if (order.total < 0) {
    throw new Error('Invalid order total');
  }

  const discountRate = customer.tier === 'premium' ? 0.20 : 0.10;
  const discountAmount = order.total * discountRate;
  const finalTotal = order.total - discountAmount;

  return {
    discountAmount,
    finalTotal
  };
}
```

**Step 4: Run tests - they should pass**
```bash
npm test
# PASS: All tests passing
```

**Step 5: Refactor if needed**

```javascript
// Refactored version with extracted constants
const DISCOUNT_RATES = {
  regular: 0.10,
  premium: 0.20,
  vip: 0.30
};

export function calculateDiscount(order, customer) {
  validateOrder(order);

  const discountRate = DISCOUNT_RATES[customer.tier] || 0;
  const discountAmount = order.total * discountRate;

  return {
    discountAmount,
    finalTotal: order.total - discountAmount
  };
}

function validateOrder(order) {
  if (order.total < 0) {
    throw new Error('Invalid order total');
  }
}
```

### Writing a New Class

**Step 1: Write tests for the class**

```python
# tests/test_shopping_cart.py
import pytest
from shopping_cart import ShoppingCart, CartItem

class TestShoppingCart:
    def test_empty_cart_has_zero_total(self):
        cart = ShoppingCart()
        assert cart.total == 0

    def test_add_item_increases_total(self):
        cart = ShoppingCart()
        cart.add_item(CartItem("Widget", 10.00, 2))

        assert cart.total == 20.00
        assert len(cart.items) == 1

    def test_remove_item_decreases_total(self):
        cart = ShoppingCart()
        item = CartItem("Widget", 10.00, 2)
        cart.add_item(item)
        cart.remove_item(item)

        assert cart.total == 0
        assert len(cart.items) == 0

    def test_clear_cart_removes_all_items(self):
        cart = ShoppingCart()
        cart.add_item(CartItem("Widget", 10.00, 2))
        cart.add_item(CartItem("Gadget", 5.00, 1))
        cart.clear()

        assert cart.total == 0
        assert len(cart.items) == 0

    def test_cannot_add_item_with_negative_price(self):
        cart = ShoppingCart()

        with pytest.raises(ValueError, match="Price must be positive"):
            cart.add_item(CartItem("Widget", -10.00, 1))
```

**Step 2: Implement the class**

```python
# shopping_cart.py
from dataclasses import dataclass
from typing import List

@dataclass
class CartItem:
    name: str
    price: float
    quantity: int

    def __post_init__(self):
        if self.price < 0:
            raise ValueError("Price must be positive")
        if self.quantity < 0:
            raise ValueError("Quantity must be positive")

    @property
    def subtotal(self):
        return self.price * self.quantity

class ShoppingCart:
    def __init__(self):
        self.items: List[CartItem] = []

    def add_item(self, item: CartItem):
        self.items.append(item)

    def remove_item(self, item: CartItem):
        self.items.remove(item)

    def clear(self):
        self.items.clear()

    @property
    def total(self):
        return sum(item.subtotal for item in self.items)
```

## Test Coverage Guidelines

### What to Test

**Always Test:**
- ✅ Public API (functions, methods, classes)
- ✅ Business logic and calculations
- ✅ Input validation and error handling
- ✅ Edge cases and boundary conditions
- ✅ Integration points with external systems
- ✅ Security-sensitive code (auth, validation, encryption)
- ✅ Data transformations

**Consider Testing:**
- Complex algorithms
- State management
- Event handling
- Async operations
- Configuration and initialization

**Usually Don't Test:**
- ❌ Third-party library code
- ❌ Simple getters/setters without logic
- ❌ Private implementation details
- ❌ Framework boilerplate

### Test Scenarios to Cover

For each function/method, test:

1. **Happy Path**: Normal, expected usage
   ```javascript
   it('should create user with valid data', () => {
     const user = createUser({ email: 'test@example.com', name: 'Test' });
     expect(user.id).toBeDefined();
   });
   ```

2. **Edge Cases**: Boundaries and limits
   ```javascript
   it('should handle empty name', () => {
     const user = createUser({ email: 'test@example.com', name: '' });
     expect(user.name).toBe('');
   });

   it('should handle very long name', () => {
     const longName = 'a'.repeat(1000);
     const user = createUser({ email: 'test@example.com', name: longName });
     expect(user.name).toBe(longName);
   });
   ```

3. **Error Cases**: Invalid inputs and failures
   ```javascript
   it('should throw error for invalid email', () => {
     expect(() => createUser({ email: 'invalid', name: 'Test' }))
       .toThrow('Invalid email format');
   });

   it('should throw error for missing required fields', () => {
     expect(() => createUser({}))
       .toThrow('Email is required');
   });
   ```

4. **Null/Undefined**: Handle missing data
   ```javascript
   it('should handle undefined input gracefully', () => {
     expect(() => createUser(undefined))
       .toThrow('User data is required');
   });

   it('should handle null values', () => {
     const user = createUser({ email: 'test@example.com', name: null });
     expect(user.name).toBeNull();
   });
   ```

5. **Special Values**: Empty arrays, zero, etc.
   ```javascript
   it('should handle empty array', () => {
     const result = processItems([]);
     expect(result).toEqual([]);
   });

   it('should handle zero value', () => {
     const result = calculate(0);
     expect(result).toBe(0);
   });
   ```

## BDD (Behavior-Driven Development)

Write tests that describe behavior, not implementation:

### Good: Behavior-Focused
```javascript
describe('User registration', () => {
  it('should send welcome email after successful registration', async () => {
    const mockMailer = jest.fn();
    await registerUser({ email: 'test@example.com' }, mockMailer);

    expect(mockMailer).toHaveBeenCalledWith({
      to: 'test@example.com',
      template: 'welcome'
    });
  });

  it('should not create account if email already exists', async () => {
    const existingEmail = 'existing@example.com';
    await registerUser({ email: existingEmail });

    await expect(registerUser({ email: existingEmail }))
      .rejects.toThrow('Email already registered');
  });
});
```

### Bad: Implementation-Focused
```javascript
describe('registerUser function', () => {
  it('should call database.insert with user data', () => {
    // Too focused on implementation details
  });

  it('should hash password using bcrypt', () => {
    // Testing implementation, not behavior
  });
});
```

## Test Organization

### File Structure
```
src/
├── services/
│   ├── UserService.js
│   └── OrderService.js
tests/
├── unit/
│   ├── services/
│   │   ├── UserService.test.js
│   │   └── OrderService.test.js
├── integration/
│   └── services/
│       └── UserAPI.test.js
└── fixtures/
    └── users.js
```

### Test Grouping
```javascript
describe('UserService', () => {
  // Group related tests
  describe('createUser', () => {
    it('should create user with valid data', () => {});
    it('should validate email format', () => {});
    it('should hash password', () => {});
  });

  describe('updateUser', () => {
    it('should update user name', () => {});
    it('should not allow email change', () => {});
  });

  describe('deleteUser', () => {
    it('should soft delete user', () => {});
    it('should anonymize user data', () => {});
  });
});
```

## Common Test-First Patterns

### Test Data Builders
```javascript
class UserBuilder {
  constructor() {
    this.user = {
      email: 'test@example.com',
      name: 'Test User',
      role: 'user'
    };
  }

  withEmail(email) {
    this.user.email = email;
    return this;
  }

  asAdmin() {
    this.user.role = 'admin';
    return this;
  }

  build() {
    return this.user;
  }
}

// Usage in tests
it('should allow admin to delete users', () => {
  const admin = new UserBuilder().asAdmin().build();
  const result = deleteUser(admin, targetUserId);
  expect(result.success).toBe(true);
});
```

### Test Fixtures
```python
# conftest.py
import pytest

@pytest.fixture
def test_user():
    return User(
        email='test@example.com',
        name='Test User',
        role='user'
    )

@pytest.fixture
def admin_user():
    return User(
        email='admin@example.com',
        name='Admin User',
        role='admin'
    )

# test_permissions.py
def test_admin_can_delete_users(admin_user, test_user):
    result = delete_user(admin_user, test_user.id)
    assert result.success is True

def test_regular_user_cannot_delete_users(test_user):
    other_user_id = 2
    with pytest.raises(PermissionError):
        delete_user(test_user, other_user_id)
```

## Test-First Checklist

Before writing production code, ensure:

- [ ] **Test Written First**: Write failing test before implementation
- [ ] **Test Describes Behavior**: Test name explains what should happen
- [ ] **Test Is Focused**: Tests one behavior or scenario
- [ ] **Test Has Good Coverage**: Happy path, edge cases, errors
- [ ] **Test Uses AAA Pattern**: Arrange, Act, Assert clearly separated
- [ ] **Test Is Independent**: Doesn't depend on other tests
- [ ] **Test Is Fast**: Runs in milliseconds (for unit tests)
- [ ] **Test Uses Mocks**: External dependencies are mocked
- [ ] **Test Fails Correctly**: Test fails when it should
- [ ] **Test Passes After Implementation**: Verifies implementation works

## Anti-Patterns to Avoid

### ❌ Writing Tests After Code
```javascript
// BAD: Code written first, tests added later
function calculateTotal(items) {
  return items.reduce((sum, item) => sum + item.price, 0);
}

// Tests written as afterthought
it('calculates total', () => {
  expect(calculateTotal([{price: 10}, {price: 20}])).toBe(30);
});
```

### ❌ Testing Implementation Details
```javascript
// BAD: Testing private methods or internal state
it('should call _validateEmail internally', () => {
  const spy = jest.spyOn(userService, '_validateEmail');
  userService.createUser({email: 'test@example.com'});
  expect(spy).toHaveBeenCalled();
});
```

### ❌ Over-Mocking
```javascript
// BAD: Mocking everything, including simple logic
const mockAdd = jest.fn((a, b) => a + b);
const mockMultiply = jest.fn((a, b) => a * b);
// Just test the real functions!
```

### ❌ Testing Multiple Things
```javascript
// BAD: One test doing too much
it('user lifecycle', () => {
  const user = createUser({});
  updateUser(user.id, {name: 'New'});
  deleteUser(user.id);
  // Split into separate tests!
});
```

## Quick Reference

### TDD Workflow
1. Write a failing test (RED)
2. Write minimal code to pass (GREEN)
3. Refactor and improve (REFACTOR)
4. Repeat

### Test Structure
```javascript
describe('ComponentName', () => {
  describe('methodName', () => {
    it('should do something when condition', () => {
      // Arrange: Set up test data
      // Act: Execute the code
      // Assert: Verify the result
    });
  });
});
```

### Coverage Goals
- Line coverage: 80%+
- Branch coverage: 80%+
- Critical paths: 95%+
- New code: 100%

Apply test-first development to catch bugs early, improve design, and build confidence in your code.
