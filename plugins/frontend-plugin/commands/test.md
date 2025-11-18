---
description: Testing utilities for components
---

# Testing Utilities

Parse arguments from $ARGUMENTS

## Argument Parsing
```bash
target="${1:-}"
shift || true
args="$*"

# Extract options
type="unit"  # unit|integration|e2e|visual
generate=false
run=false
coverage=false

for arg in $args; do
  case $arg in
    --type=*) type="${arg#*=}" ;;
    --generate) generate=true ;;
    --run) run=true ;;
    --coverage) coverage=true ;;
  esac
done
```

## Test Types

### Unit Tests
- Component render tests
- Hook behavior tests
- Utility function tests
- Props validation
- State changes
- Event handlers

### Integration Tests
- Component interaction
- API integration
- State management flow
- Routing behavior
- Form submissions

### E2E Tests
- User workflows
- Critical paths
- Cross-browser testing
- Mobile responsiveness
- Performance metrics

### Visual Tests
- Screenshot comparisons
- Component variations
- Theme testing
- Responsive layouts
- Style regression

## Generate Tests
If --generate flag is set:
1. Analyze target component/hook
2. Identify testable behaviors
3. Generate appropriate test file
4. Include:
   - Setup and teardown
   - Mock dependencies
   - Test cases
   - Assertions
   - Coverage targets

## Run Tests
If --run flag is set:
```bash
# Detect test runner
if [ -f "jest.config.js" ]; then
  npm test $target
elif [ -f "vitest.config.js" ]; then
  npm run test $target
elif [ -f "cypress.config.js" ] && [ "$type" = "e2e" ]; then
  npm run cypress:run
fi

# With coverage if requested
if [ "$coverage" = true ]; then
  npm test -- --coverage $target
fi
```

## Test File Templates

### Component Test
```typescript
import { render, screen, fireEvent } from '@testing-library/react';
import { ComponentName } from './ComponentName';

describe('ComponentName', () => {
  it('renders correctly', () => {
    render(<ComponentName />);
    expect(screen.getByRole('...')).toBeInTheDocument();
  });

  it('handles user interaction', () => {
    // Test implementation
  });
});
```

### Hook Test
```typescript
import { renderHook, act } from '@testing-library/react';
import { useHookName } from './useHookName';

describe('useHookName', () => {
  it('returns expected values', () => {
    const { result } = renderHook(() => useHookName());
    expect(result.current).toBeDefined();
  });
});
```

## Output
- Generated test files
- Test execution results
- Coverage report
- Failed test details
- Improvement suggestions