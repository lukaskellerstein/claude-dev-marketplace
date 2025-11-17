---
name: style-assistant
description: Assists with styling decisions and patterns
allowed-tools: Read, Grep
---

# Style Assistant Skill

Automatically provide styling assistance and best practices during development.

## Auto-invocation Triggers

### File Patterns
- `**/*.css` - CSS files
- `**/*.scss` - SCSS files
- `**/*.sass` - Sass files
- `**/*.module.css` - CSS Modules
- `**/*.module.scss` - SCSS Modules
- `**/styles.ts` - CSS-in-JS files

### Tool Usage
- When adding `className` prop
- When adding `style` prop
- When creating style files
- When writing CSS rules

### Keywords
- `className`
- `style`
- `css`
- `tailwind`
- `styled`
- `tw`
- `cn()`

### Context Detection
```tsx
// Triggers on className usage
<div className="...">

// Triggers on style prop
<div style={{...}}>

// Triggers on styled components
const StyledDiv = styled.div`...`;
```

## Tailwind Assistance

### Class Suggestions
```tsx
// User types: "center content"
// Suggest: "flex items-center justify-center"

// User types: "red text"
// Suggest: "text-red-500"

// User types: "spacing"
// Suggest: "p-4" or "m-4" or "space-x-4"
```

### Responsive Patterns
```tsx
// ❌ Desktop-first approach
className="w-1/3 lg:w-full md:w-1/2"

// ✅ Mobile-first approach
className="w-full md:w-1/2 lg:w-1/3"
```

### Common Patterns
```tsx
// Card component
className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow"

// Button variants
className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50"

// Form input
className="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
```

## CSS Best Practices

### Custom Properties
```css
/* ❌ Hardcoded values */
.button {
  background: #3b82f6;
  padding: 16px;
}

/* ✅ Using CSS variables */
.button {
  background: var(--color-primary);
  padding: var(--spacing-md);
}
```

### Specificity Management
```css
/* ❌ High specificity */
#header .nav ul li a.active {
  color: blue;
}

/* ✅ Low specificity with BEM */
.nav__link--active {
  color: var(--color-primary);
}
```

### Modern CSS Features
```css
/* Container Queries */
.card {
  container-type: inline-size;
}

@container (min-width: 400px) {
  .card__content {
    display: grid;
  }
}

/* CSS Grid */
.layout {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: var(--spacing-lg);
}

/* Logical Properties */
.element {
  margin-inline: auto; /* Instead of margin-left/right */
  padding-block: 1rem; /* Instead of padding-top/bottom */
}
```

## SCSS Features

### Nesting Optimization
```scss
// ❌ Over-nesting
.component {
  .header {
    .title {
      .text {
        color: blue;
      }
    }
  }
}

// ✅ Flat structure
.component {
  &__header {
    // Direct children only
  }

  &__title {
    color: blue;
  }
}
```

### Mixins and Functions
```scss
// Useful mixins
@mixin responsive($breakpoint) {
  @media (min-width: $breakpoint) {
    @content;
  }
}

@mixin truncate($lines: 1) {
  overflow: hidden;
  text-overflow: ellipsis;

  @if $lines > 1 {
    display: -webkit-box;
    -webkit-line-clamp: $lines;
    -webkit-box-orient: vertical;
  } @else {
    white-space: nowrap;
  }
}
```

## Performance Optimizations

### Critical CSS
```css
/* Inline critical above-the-fold styles */
<style>
  .hero { /* Critical styles */ }
  .nav { /* Critical styles */ }
</style>

/* Load non-critical CSS asynchronously */
<link rel="preload" href="styles.css" as="style" onload="this.onload=null;this.rel='stylesheet'">
```

### Animation Performance
```css
/* ❌ Animating layout properties */
.element {
  transition: width 0.3s, left 0.3s;
}

/* ✅ Animating compositor properties */
.element {
  transition: transform 0.3s, opacity 0.3s;
  will-change: transform;
}
```

## Responsive Design

### Breakpoint Strategy
```scss
// Mobile-first breakpoints
$breakpoints: (
  'sm': 640px,
  'md': 768px,
  'lg': 1024px,
  'xl': 1280px,
  '2xl': 1536px,
);

// Usage
@media (min-width: map-get($breakpoints, 'md')) {
  // Tablet and up styles
}
```

### Fluid Typography
```css
/* Clamp for responsive font sizes */
.title {
  font-size: clamp(1.5rem, 4vw, 3rem);
}

/* Fluid spacing */
.section {
  padding: clamp(2rem, 5vw, 4rem);
}
```

## Common Issues Detection

### Duplicate Rules
```css
/* Detect and suggest consolidation */
.card {
  padding: 1rem;
}

.card {
  padding: 1rem; /* Duplicate */
}
```

### Unused Styles
- Identify selectors not matching any elements
- Flag CSS rules never applied
- Suggest removal of dead code

### Color Inconsistencies
```css
/* Multiple similar colors */
color: #3b82f6;
color: #3b82f5; /* Almost identical */
color: rgb(59, 130, 246); /* Same as first */

/* Suggest: Use single variable */
color: var(--color-primary);
```

## Suggestions Output

### Format
```markdown
💡 Style Suggestion:

**Issue**: Hardcoded color value
**Location**: Component.tsx:45
**Current**: `style={{ color: '#3b82f6' }}`
**Suggested**: `className="text-blue-600"`
**Reason**: Use Tailwind utilities for consistency
```

### Auto-complete
Provide intelligent auto-completion for:
- Tailwind classes
- CSS properties
- SCSS variables
- Design tokens
- Common patterns

### Documentation Links
- Tailwind docs for utilities
- MDN for CSS properties
- Can I Use for browser support
- CSS Tricks for techniques