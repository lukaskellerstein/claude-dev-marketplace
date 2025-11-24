---
description: Audit frontend codebase for performance, accessibility, and best practices
---

Perform a comprehensive audit of the frontend codebase to identify issues and improvement opportunities.

## Process

Follow these steps:

1. **Codebase Analysis**: Scan the frontend codebase to:
   - Identify all React components
   - Find styling approaches (Tailwind, CSS, SCSS)
   - Detect state management patterns
   - Review component organization
   - Check TypeScript usage and typing quality

2. **Performance Audit**: Use the `react-expert` agent to identify:
   - Unnecessary re-renders
   - Missing memoization opportunities
   - Large bundle sizes
   - Unoptimized images
   - Missing code splitting
   - Inefficient state updates
   - Memory leaks (useEffect cleanup)
   - Expensive computations in render

3. **Accessibility Audit**: Use the `responsive-design-expert` agent to check:
   - ARIA attributes usage
   - Keyboard navigation support
   - Focus management
   - Color contrast issues
   - Alt text for images
   - Form labels and error messages
   - Semantic HTML usage
   - Screen reader compatibility

4. **Styling Audit**: Use the `css-tailwind-expert` agent to review:
   - CSS/Tailwind consistency
   - Design system adherence
   - Redundant or duplicate styles
   - Missing responsive variations
   - Dark mode implementation
   - Animation performance
   - CSS bundle size

5. **Best Practices Review**: Check for:
   - Component organization and naming
   - Props interface design
   - Error boundary implementation
   - Loading and error states
   - TypeScript strict mode compliance
   - Test coverage
   - Documentation quality

6. **Generate Report**: Compile findings into prioritized action items

## Output

Present a comprehensive audit report:

### 1. Executive Summary
- Overall health score (1-10)
- Critical issues count
- High priority improvements
- Estimated effort for fixes

### 2. Performance Issues

**Critical (Fix Immediately)**
```typescript
// ❌ Problem: Component re-renders on every parent update
export function UserList({ users }: { users: User[] }) {
  const [filter, setFilter] = useState('');

  const expensiveComputation = users.map(u => transformUser(u)); // Recalculates every render

  return <div>...</div>;
}

// ✅ Solution: Memoize expensive computation
export const UserList = memo(({ users }: { users: User[] }) => {
  const [filter, setFilter] = useState('');

  const processedUsers = useMemo(
    () => users.map(u => transformUser(u)),
    [users]
  );

  return <div>...</div>;
});
```

**High Priority**
- List of issues with file paths and line numbers
- Code examples
- Recommended fixes

**Medium Priority**
- Optimization opportunities
- Code examples

### 3. Accessibility Issues

**WCAG Violations**
```tsx
// ❌ Problem: Missing alt text
<img src="/profile.jpg" />

// ✅ Solution: Add descriptive alt text
<img src="/profile.jpg" alt="User profile picture" />

// ❌ Problem: No keyboard navigation
<div onClick={handleClick}>Click me</div>

// ✅ Solution: Use button with keyboard support
<button onClick={handleClick}>Click me</button>
```

**Issues by Severity**
- Critical: Blocks accessibility
- High: Major barrier
- Medium: Usability issue
- Low: Enhancement opportunity

### 4. Styling Issues

**Inconsistencies**
- Inconsistent spacing patterns
- Mixed color values (not using design tokens)
- Redundant Tailwind classes
- Missing responsive breakpoints
- Dark mode gaps

```tsx
// ❌ Problem: Hard-coded colors, inconsistent spacing
<div className="bg-[#3b82f6] p-3 mb-5">...</div>
<div className="bg-[#2563eb] p-4 mb-6">...</div>

// ✅ Solution: Use design tokens, consistent spacing
<div className="bg-primary p-4 mb-4">...</div>
<div className="bg-primary-dark p-4 mb-4">...</div>
```

### 5. Code Quality Issues

**TypeScript**
- Any types usage
- Missing type definitions
- Weak typing

**React Patterns**
- Props drilling
- Large components that should be split
- Missing error boundaries
- Inconsistent naming conventions

### 6. Bundle Analysis

```
Bundle Size Report:
- Total: 850 KB (target: < 250 KB)
- JavaScript: 650 KB
  - React: 120 KB
  - node_modules: 400 KB (⚠️ Check for unnecessary deps)
  - App code: 130 KB
- CSS: 200 KB (⚠️ Potential Tailwind purge issue)

Recommendations:
1. Enable Tailwind JIT mode
2. Remove unused dependencies: lodash (40 KB), moment (60 KB)
3. Code split by route
4. Lazy load below-the-fold components
```

### 7. Responsive Design Issues

```tsx
// ❌ Problem: Not mobile-friendly
<div className="flex gap-8 p-8">
  <aside className="w-64">Sidebar</aside>
  <main className="flex-1">Content</main>
</div>

// ✅ Solution: Responsive layout
<div className="flex flex-col md:flex-row gap-4 md:gap-8 p-4 md:p-8">
  <aside className="w-full md:w-64">Sidebar</aside>
  <main className="flex-1">Content</main>
</div>
```

### 8. Action Plan

**Immediate (Next Sprint)**
1. Fix accessibility violations (3 days)
2. Implement code splitting (2 days)
3. Add error boundaries (1 day)

**Short-term (Next Month)**
1. Optimize component re-renders (5 days)
2. Establish design system (10 days)
3. Improve TypeScript coverage (5 days)

**Long-term (Next Quarter)**
1. Comprehensive test coverage
2. Performance monitoring setup
3. Documentation improvements

### 9. Metrics & Benchmarks

**Current**
- Lighthouse Score: 72/100
- First Contentful Paint: 2.5s
- Time to Interactive: 4.2s
- Bundle Size: 850 KB
- Test Coverage: 45%

**Target**
- Lighthouse Score: 90+/100
- First Contentful Paint: < 1.5s
- Time to Interactive: < 3.0s
- Bundle Size: < 250 KB
- Test Coverage: 80%+

### 10. Quick Wins

Easy improvements with high impact:
1. Add missing alt texts (30 minutes)
2. Enable Tailwind JIT (15 minutes)
3. Add React.memo to 5 expensive components (2 hours)
4. Implement lazy loading for images (1 hour)
5. Add focus styles for keyboard navigation (1 hour)

## Examples

### Basic Audit
```
/audit-frontend

Audit the React application in src/components for performance and accessibility issues
```

### Comprehensive Audit
```
/audit-frontend

Perform comprehensive frontend audit:
- Performance bottlenecks
- Accessibility WCAG 2.1 AA compliance
- Bundle size analysis
- TypeScript quality
- Design system consistency
- Responsive design validation
```

### Focused Audit
```
/audit-frontend

Audit specifically for:
- Memory leaks in useEffect hooks
- Missing loading states
- Error handling gaps
- Dark mode inconsistencies
```

Provide detailed findings with file paths, line numbers, code examples, and prioritized recommendations.
