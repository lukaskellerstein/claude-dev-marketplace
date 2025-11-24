---
description: Analyze test coverage, identify gaps, generate coverage reports, and provide recommendations for improving coverage
---

Analyze test coverage to identify gaps, generate detailed coverage reports, and provide actionable recommendations for improving test coverage.

## Process

Follow these steps:

1. **Initial Assessment**: Understand the project's testing setup
   - Identify testing framework and coverage tool
   - Locate existing coverage configuration
   - Check for coverage reports in CI/CD
   - Review coverage thresholds and targets
   - Identify critical code paths requiring coverage

2. **Generate Coverage Report**: Run coverage analysis
   - Execute test suite with coverage collection
   - Generate coverage reports in multiple formats
   - Collect line, branch, function, and statement coverage
   - Create visual coverage reports (HTML)
   - Export coverage data for analysis

3. **Launch Coverage Analyzer**: Use the `coverage-analyzer` agent to:
   - Parse coverage data and identify patterns
   - Find completely uncovered files
   - Identify functions with low/no coverage
   - Detect missing branch coverage (if/else not tested)
   - Highlight untested error handling paths
   - Find critical code paths without tests
   - Analyze coverage trends over time
   - Compare coverage against thresholds

4. **Prioritize Coverage Gaps**: Focus on high-impact areas
   - Critical business logic
   - Security-sensitive code (authentication, authorization, validation)
   - Payment and financial operations
   - Data persistence and retrieval
   - Error handling and recovery
   - API endpoints and public interfaces
   - Complex algorithms and calculations

5. **Generate Recommendations**: Provide actionable steps
   - Specific files and functions needing tests
   - Test types needed (unit, integration, E2E)
   - Priority levels (critical, high, medium, low)
   - Estimated effort and test count
   - Code examples for uncovered scenarios

## Output

Present a comprehensive coverage analysis report with:

### Executive Summary

```
====================================================================
                    Coverage Analysis Report
====================================================================

Overall Coverage:        76.5%  ⚠️  Below 80% threshold
Target Coverage:         80%
Gap:                     -3.5%

Files Analyzed:          87
Critical Gaps:           8
Uncovered Functions:     23
Missing Branches:        45

Status:                  NEEDS IMPROVEMENT
Priority Actions:        Fix 8 critical gaps in authentication and payment modules
====================================================================
```

### Coverage Metrics

**Overall Coverage**:
- **Line Coverage**: 78.3% (3,456 / 4,412 lines)
- **Branch Coverage**: 71.2% (234 / 329 branches)
- **Function Coverage**: 85.7% (156 / 182 functions)
- **Statement Coverage**: 78.1% (3,401 / 4,356 statements)

**Coverage by Directory**:
```
src/auth/           62.3%  ⚠️  CRITICAL - Below threshold
src/payment/        55.8%  🔴 CRITICAL - Very low coverage
src/users/          89.4%  ✅ Good coverage
src/orders/         78.9%  ⚠️  Slightly below threshold
src/api/            92.1%  ✅ Excellent coverage
src/utils/          95.6%  ✅ Excellent coverage
src/validation/     88.2%  ✅ Good coverage
```

### Critical Coverage Gaps

#### 1. Payment Processing - Very Low Coverage (55.8%)
**File**: `src/payment/StripeService.js`
**Priority**: 🔴 CRITICAL
**Risk Level**: HIGH

**Uncovered Code**:
- **Lines 45-89**: Payment intent creation and card processing
  - No tests for successful payment processing
  - Error handling for declined cards not tested
  - Network timeout scenarios not covered

- **Lines 120-156**: Refund processing logic
  - Complete refund path untested
  - Partial refund calculations not verified
  - Refund failure handling missing

- **Lines 178-205**: Webhook signature verification
  - Webhook processing not tested
  - Invalid signature handling missing

**Impact**:
- Financial transactions not adequately validated
- Card decline scenarios may not work correctly
- Refund bugs could lead to financial losses
- Webhook vulnerabilities could be exploited

**Recommended Tests** (Priority: Immediate):
```javascript
describe('StripeService.createPaymentIntent', () => {
  it('should process successful card payment', async () => {
    // Test successful payment flow
  });

  it('should handle declined card gracefully', async () => {
    // Test card decline error handling
  });

  it('should retry on network timeout', async () => {
    // Test network error recovery
  });

  it('should validate payment amount', async () => {
    // Test amount validation (negative, zero, too large)
  });
});

describe('StripeService.processRefund', () => {
  it('should process full refund correctly', async () => {
    // Test full refund
  });

  it('should calculate partial refund amount', async () => {
    // Test partial refund calculations
  });

  it('should handle refund failures', async () => {
    // Test refund error scenarios
  });
});
```

**Estimated Effort**: 4-6 hours, 12-15 tests

---

#### 2. Authentication Module - Low Coverage (62.3%)
**File**: `src/auth/AuthService.js`
**Priority**: 🔴 CRITICAL
**Risk Level**: HIGH

**Uncovered Code**:
- **Lines 67-84**: Password reset token generation and validation
- **Lines 102-118**: JWT token refresh logic
- **Lines 145-167**: Multi-factor authentication verification

**Impact**:
- Security vulnerabilities in authentication flow
- Password reset may not work correctly
- Token refresh bugs could lock users out
- MFA bypass potential

**Recommended Tests** (Priority: Immediate):
```javascript
describe('AuthService.resetPassword', () => {
  it('should generate valid reset token', async () => {});
  it('should expire reset token after 1 hour', async () => {});
  it('should reject expired token', async () => {});
  it('should invalidate token after use', async () => {});
});

describe('AuthService.refreshToken', () => {
  it('should issue new token with valid refresh token', async () => {});
  it('should reject expired refresh token', async () => {});
  it('should maintain user session data', async () => {});
});
```

**Estimated Effort**: 3-4 hours, 10-12 tests

---

### Completely Uncovered Files (8)

Files with 0% coverage requiring immediate attention:

1. **src/payment/RefundCalculator.js** (0% coverage)
   - Refund amount calculations completely untested
   - Critical business logic with financial impact
   - Need: 8-10 unit tests

2. **src/auth/PasswordValidator.js** (0% coverage)
   - Password strength validation not tested
   - Security risk for weak passwords
   - Need: 6-8 unit tests

3. **src/api/webhooks/StripeWebhook.js** (0% coverage)
   - Webhook processing untested
   - Integration point with payment provider
   - Need: 5-7 integration tests

4. **src/utils/EmailValidator.js** (0% coverage)
   - Email validation logic not tested
   - Could allow invalid emails
   - Need: 4-6 unit tests

---

### Missing Branch Coverage (45 branches)

**High Priority Branches** (15):

1. **src/auth/login.js:45** - Failed login attempt handling
   ```javascript
   // Line 45: Branch not tested
   if (loginAttempts > MAX_ATTEMPTS) {
     lockAccount(user.id);  // Not covered
   }
   ```
   **Test needed**: Verify account lockout after failed attempts

2. **src/payment/checkout.js:89** - Insufficient funds error
   ```javascript
   // Line 89: Error branch not tested
   if (balance < amount) {
     throw new InsufficientFundsError();  // Not covered
   }
   ```
   **Test needed**: Test insufficient balance scenario

3. **src/users/validation.js:34** - Invalid email format
   ```javascript
   // Line 34: Validation branch not tested
   if (!isValidEmail(email)) {
     return { valid: false, error: 'Invalid email' };  // Not covered
   }
   ```
   **Test needed**: Test email validation with invalid formats

---

### Uncovered Functions (23)

**Critical Functions** (8):

1. **validatePaymentMethod** (`src/payment/validation.js:45`)
   - Validates credit card details
   - Used in checkout flow
   - Need: 5 unit tests (valid card, expired card, invalid CVV, etc.)

2. **hashPassword** (`src/auth/crypto.js:23`)
   - Hashes user passwords
   - Security critical function
   - Need: 4 unit tests (bcrypt, salt rounds, comparison)

3. **calculateShippingCost** (`src/orders/shipping.js:67`)
   - Calculates shipping fees
   - Business logic with financial impact
   - Need: 6 unit tests (domestic, international, weight-based, etc.)

---

### Coverage Trends

```
Coverage History (Last 4 Weeks):
Week 1:  72.3%
Week 2:  74.8%  (+2.5%)
Week 3:  76.1%  (+1.3%)
Week 4:  76.5%  (+0.4%)

Trend: Coverage improvements slowing
Recommendation: Focus on critical gaps rather than incremental gains
```

---

### Recommendations

#### Immediate Actions (This Sprint - Priority: CRITICAL)

1. **Add Payment Processing Tests** (Highest Priority)
   - File: `src/payment/StripeService.js`
   - Tests needed: 12-15 tests
   - Estimated time: 4-6 hours
   - Impact: Prevents financial bugs

2. **Cover Authentication Error Paths**
   - File: `src/auth/AuthService.js`
   - Tests needed: 10-12 tests
   - Estimated time: 3-4 hours
   - Impact: Improves security

3. **Test Uncovered Validation Logic**
   - Files: `src/*/validation.js`
   - Tests needed: 15-20 tests
   - Estimated time: 4-5 hours
   - Impact: Prevents invalid data

**Total Effort**: 11-15 hours to address critical gaps

#### Short Term (Next Sprint)

4. Cover all 8 files with 0% coverage
5. Improve branch coverage to 80%
6. Add integration tests for payment + order flow
7. Add E2E tests for checkout process

#### Long Term (Next Quarter)

8. Establish 90% coverage target for new code
9. Implement mutation testing for critical modules
10. Set up coverage monitoring and alerts
11. Add visual regression tests for UI components

---

### Coverage Configuration

**Recommended Coverage Thresholds**:
```javascript
// jest.config.js or vitest.config.js
{
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 85,
      lines: 80,
      statements: 80
    },
    // Stricter thresholds for critical code
    './src/auth/': {
      branches: 90,
      functions: 95,
      lines: 90,
      statements: 90
    },
    './src/payment/': {
      branches: 95,
      functions: 95,
      lines: 95,
      statements: 95
    }
  }
}
```

**CI/CD Integration**:
```yaml
# .github/workflows/coverage.yml
name: Coverage Check
on: [push, pull_request]
jobs:
  coverage:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: npm ci
      - run: npm run test:coverage
      - name: Upload to Codecov
        uses: codecov/codecov-action@v3
      - name: Check thresholds
        run: |
          npm run test:coverage -- --coverageThreshold='{"global":{"lines":80}}'
```

---

### Coverage Report Files Generated

- **HTML Report**: `coverage/index.html` (Interactive line-by-line coverage)
- **LCOV Report**: `coverage/lcov.info` (For CI/CD tools)
- **JSON Report**: `coverage/coverage-final.json` (For programmatic analysis)
- **Text Summary**: Displayed in terminal

**View HTML Report**: `open coverage/index.html`

---

## Examples

### Analyze Overall Coverage

```
/analyze-coverage

Analyze complete test coverage for the project, identify gaps,
and provide prioritized recommendations for improvement
```

### Coverage for Specific Module

```
/analyze-coverage

Analyze test coverage specifically for the authentication module
(src/auth/*) and identify security-critical gaps
```

### Coverage with Threshold Check

```
/analyze-coverage

Analyze coverage and verify it meets 80% threshold across all
metrics. Highlight any modules below threshold
```

### Compare Coverage Over Time

```
/analyze-coverage

Generate coverage report and compare with last week's coverage
to show improvements and regressions
```

### Critical Path Coverage

```
/analyze-coverage

Focus analysis on critical business paths: authentication,
payment processing, and order management. Identify gaps in
these high-risk areas
```

## Best Practices Applied

- **Risk-Based Prioritization**: Focus on critical code first
- **Actionable Recommendations**: Specific tests to write, not just numbers
- **Coverage Thresholds**: Enforce minimum coverage standards
- **Trend Analysis**: Track coverage over time
- **Multiple Metrics**: Line, branch, function, statement coverage
- **Visual Reports**: Easy-to-understand HTML reports
- **CI/CD Integration**: Automated coverage checks

## Integration with Other Commands

- Analyze coverage first with `/analyze-coverage`
- Generate missing tests with `/generate-tests` for identified gaps
- Assess test quality with `/assess-test-quality`
- Re-run coverage analysis to verify improvements

Provide data-driven, actionable coverage analysis that guides testing efforts toward high-impact improvements.
