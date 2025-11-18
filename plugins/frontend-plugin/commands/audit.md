---
description: Comprehensive performance and quality audit
---

# Performance & Quality Audit

Parse arguments from $ARGUMENTS

## Argument Parsing
```bash
scope="${1:-.}"  # Default to current directory
shift || true
args="$*"

# Extract focus areas
focus="all"  # all|react|styles|bundle|a11y
fix=false
report_only=false

for arg in $args; do
  case $arg in
    --focus=*) focus="${arg#*=}" ;;
    --fix) fix=true ;;
    --report) report_only=true ;;
  esac
done
```

## Focus Areas

### React Performance
- Component re-renders analysis
- Missing React.memo opportunities
- UseCallback/useMemo usage
- Large component detection
- Hook dependencies analysis
- State management patterns

### Style Optimization
- Unused CSS detection
- Duplicate rules identification
- Specificity issues
- Bundle size impact
- Tailwind class optimization
- CSS-in-JS performance

### Bundle Analysis
- Code splitting opportunities
- Lazy loading candidates
- Tree shaking effectiveness
- Dependency size analysis
- Dynamic imports usage
- Chunk optimization

### Accessibility (a11y)
- Missing ARIA attributes
- Semantic HTML validation
- Keyboard navigation
- Color contrast issues
- Alt text presence
- Focus management

### All
Comprehensive audit covering all areas

## Invoke Agent
Call performance-auditor agent with:
- scope: Directory or file to audit
- focus: Specific area or 'all'
- fix: Auto-fix issues where possible
- report_only: Generate report without fixes

## Output

### Audit Report
```markdown
# Frontend Audit Report

## Summary
- Total issues found: X
- Critical: X
- Warning: X
- Info: X

## React Performance
- [ ] Component X has 5 unnecessary re-renders
- [ ] Add React.memo to UserList component
- [ ] Optimize useEffect in Dashboard

## Style Optimization
- [ ] Remove 245 lines of unused CSS
- [ ] Consolidate 15 duplicate rules
- [ ] Convert inline styles to Tailwind

## Bundle Size
- [ ] Enable code splitting for routes
- [ ] Lazy load heavy components
- [ ] Tree-shake lodash imports

## Accessibility
- [ ] Add alt text to 3 images
- [ ] Fix keyboard navigation in modal
- [ ] Improve color contrast on buttons
```

### Auto-fixes (if --fix)
- Apply React.memo where beneficial
- Remove unused styles
- Add missing accessibility attributes
- Optimize imports