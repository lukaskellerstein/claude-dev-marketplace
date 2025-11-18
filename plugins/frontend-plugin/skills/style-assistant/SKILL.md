---
name: style-assistant
description: Master modern CSS and styling for beautiful, accessible interfaces. Use when implementing Tailwind utilities, writing CSS, integrating design systems (shadcn/ui, Radix UI), optimizing styles, or ensuring responsive design.
allowed-tools: Read, Grep
---

# Style Assistant Skill

Automatically provide styling assistance and best practices during development.

## When to Use This Skill

This skill automatically activates and provides assistance in these specific scenarios:

1. **Tailwind Class Selection** - Choosing optimal utility classes for layouts
2. **Responsive Design** - Implementing mobile-first responsive patterns
3. **CSS Variables** - Creating and using custom properties
4. **Design System Integration** - Working with shadcn/ui or Radix UI components
5. **Color Management** - Ensuring consistent color usage
6. **Typography** - Implementing fluid typography and text styles
7. **Spacing Systems** - Applying consistent spacing scales
8. **Animation Performance** - Creating smooth, performant animations
9. **Dark Mode** - Implementing theme switching
10. **CSS Architecture** - Organizing CSS with BEM, CSS Modules, or CSS-in-JS
11. **Accessibility Styles** - Focus states, color contrast, responsive text
12. **Performance Optimization** - Critical CSS, reducing specificity
13. **Modern CSS Features** - Container queries, grid, logical properties
14. **Style Debugging** - Fixing specificity conflicts or layout issues
15. **Component Styling** - Styling React components with Tailwind or CSS Modules

## Quick Start

### Step 1: Automatic Detection
The skill monitors your styling patterns as you write code. It activates when:
- You add `className` attributes
- You create or edit CSS files
- You use CSS-in-JS solutions
- You work with Tailwind utilities

### Step 2: Get Suggestions
Receive instant recommendations for:
- Better Tailwind class combinations
- Responsive design patterns
- Accessibility improvements
- Performance optimizations

### Step 3: Apply Best Practices
Follow the provided patterns to create consistent, maintainable styles across your application.

## Auto-invocation Triggers

### File Patterns
- `**/*.css` - CSS files
- `**/*.scss` - SCSS files
- `**/*.sass` - Sass files
- `**/*.module.css` - CSS Modules
- `**/*.module.scss` - SCSS Modules
- `**/styles.ts` - CSS-in-JS files
- `**/tailwind.config.*` - Tailwind configuration

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
- `clsx`

### Context Detection
```tsx
// Triggers on className usage
<div className="...">

// Triggers on style prop
<div style={{...}}>

// Triggers on styled components
const StyledDiv = styled.div`...`;

// Triggers on Tailwind merge
import { cn } from '@/lib/utils';
className={cn('base-class', conditionalClass)}
```

## Tailwind Assistance

### Class Suggestions
```tsx
// User intent: "center content"
// Suggest: "flex items-center justify-center"
<div className="flex items-center justify-center">

// User intent: "red text"
// Suggest: "text-red-500" or "text-red-600" for better contrast
<p className="text-red-600">

// User intent: "spacing"
// Context-aware suggestions:
<div className="p-4">      // padding all sides
<div className="m-4">      // margin all sides
<div className="space-y-4"> // vertical spacing between children
<div className="gap-4">    // gap in flex/grid
```

### Responsive Patterns
```tsx
// ❌ Desktop-first approach (harder to maintain)
className="w-1/3 lg:w-full md:w-1/2"

// ✅ Mobile-first approach (Tailwind default)
className="w-full md:w-1/2 lg:w-1/3"

// ✅ Comprehensive responsive layout
className="
  grid
  grid-cols-1
  sm:grid-cols-2
  md:grid-cols-3
  lg:grid-cols-4
  gap-4
  p-4
  md:p-6
  lg:p-8
"
```

### Common Tailwind Patterns
```tsx
// Card component
className="
  bg-white dark:bg-gray-800
  rounded-lg
  shadow-md hover:shadow-lg
  transition-shadow duration-200
  p-6
  border border-gray-200 dark:border-gray-700
"

// Primary button
className="
  px-4 py-2
  bg-blue-600 hover:bg-blue-700
  text-white font-medium
  rounded-md
  transition-colors duration-150
  focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2
  disabled:opacity-50 disabled:cursor-not-allowed
  active:bg-blue-800
"

// Form input
className="
  w-full
  px-3 py-2
  border border-gray-300 dark:border-gray-600
  rounded-md
  bg-white dark:bg-gray-800
  text-gray-900 dark:text-gray-100
  placeholder-gray-400
  focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent
  disabled:bg-gray-100 disabled:cursor-not-allowed
"

// Container with max-width
className="
  w-full
  max-w-7xl
  mx-auto
  px-4
  sm:px-6
  lg:px-8
"
```

### Tailwind with cn() Utility
```tsx
import { cn } from '@/lib/utils';

// Conditional classes
<button
  className={cn(
    'px-4 py-2 rounded-md font-medium transition-colors',
    variant === 'primary' && 'bg-blue-600 text-white hover:bg-blue-700',
    variant === 'secondary' && 'bg-gray-200 text-gray-900 hover:bg-gray-300',
    variant === 'danger' && 'bg-red-600 text-white hover:bg-red-700',
    disabled && 'opacity-50 cursor-not-allowed'
  )}
>
  {children}
</button>

// Merging with prop classes
<div className={cn('flex items-center gap-2', className)}>
```

## CSS Best Practices

### Custom Properties
```css
/* ❌ Hardcoded values */
.button {
  background: #3b82f6;
  padding: 16px;
  border-radius: 8px;
  font-size: 14px;
}

/* ✅ Using CSS variables with fallbacks */
:root {
  --color-primary: #3b82f6;
  --color-primary-hover: #2563eb;
  --spacing-sm: 0.5rem;
  --spacing-md: 1rem;
  --spacing-lg: 1.5rem;
  --radius-md: 0.5rem;
  --font-size-sm: 0.875rem;
}

.button {
  background: var(--color-primary);
  padding: var(--spacing-md);
  border-radius: var(--radius-md);
  font-size: var(--font-size-sm);
}

.button:hover {
  background: var(--color-primary-hover);
}

/* ✅ Dark mode with CSS variables */
:root {
  --bg-primary: #ffffff;
  --text-primary: #1f2937;
}

[data-theme="dark"] {
  --bg-primary: #1f2937;
  --text-primary: #f9fafb;
}

.container {
  background: var(--bg-primary);
  color: var(--text-primary);
}
```

### Specificity Management
```css
/* ❌ High specificity (hard to override) */
#header .nav ul li a.active {
  color: blue;
}

/* ❌ Over-qualified selectors */
div.container div.card div.header h2.title {
  font-size: 24px;
}

/* ✅ Low specificity with BEM */
.nav__link {
  color: var(--color-text-secondary);
}

.nav__link--active {
  color: var(--color-primary);
  font-weight: 600;
}

/* ✅ CSS Modules (scoped by default) */
.link {
  color: var(--color-text-secondary);
}

.linkActive {
  color: var(--color-primary);
  font-weight: 600;
}
```

### Modern CSS Features

#### Container Queries
```css
/* Container queries for component-level responsive design */
.card {
  container-type: inline-size;
  container-name: card;
}

@container card (min-width: 400px) {
  .card__content {
    display: grid;
    grid-template-columns: 1fr 2fr;
    gap: 1rem;
  }
}

@container card (min-width: 600px) {
  .card__image {
    aspect-ratio: 16 / 9;
  }
}
```

#### CSS Grid
```css
/* Modern grid layouts */
.layout {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: var(--spacing-lg);
}

/* Named grid areas */
.page {
  display: grid;
  grid-template-areas:
    "header header header"
    "sidebar main main"
    "footer footer footer";
  grid-template-columns: 200px 1fr 1fr;
  grid-template-rows: auto 1fr auto;
  gap: 1rem;
  min-height: 100vh;
}

.header { grid-area: header; }
.sidebar { grid-area: sidebar; }
.main { grid-area: main; }
.footer { grid-area: footer; }
```

#### Logical Properties
```css
/* ❌ Physical properties (not RTL-friendly) */
.element {
  margin-left: auto;
  margin-right: auto;
  padding-top: 1rem;
  padding-bottom: 1rem;
  border-left: 2px solid blue;
}

/* ✅ Logical properties (works with RTL) */
.element {
  margin-inline: auto;
  padding-block: 1rem;
  border-inline-start: 2px solid blue;
}
```

#### Color Functions
```css
/* Modern color manipulation */
.button {
  background: oklch(60% 0.15 270);
}

.button:hover {
  background: oklch(55% 0.15 270); /* Darker */
}

/* Using color-mix */
.alert {
  background: color-mix(in oklch, var(--color-primary) 20%, transparent);
}

/* Relative colors */
.card {
  background: rgb(from var(--color-primary) r g b / 0.1);
}
```

## SCSS Features

### Nesting Optimization
```scss
// ❌ Over-nesting (creates high specificity)
.component {
  .header {
    .title {
      .text {
        color: blue;
      }
    }
  }
}

// ✅ Flat BEM structure
.component {
  &__header {
    padding: 1rem;
  }

  &__title {
    font-size: 1.5rem;
    font-weight: 600;
  }

  &__text {
    color: var(--color-primary);
  }

  // Modifiers
  &--large {
    .component__title {
      font-size: 2rem;
    }
  }
}
```

### Mixins and Functions
```scss
// Responsive mixin
@mixin responsive($breakpoint) {
  @media (min-width: $breakpoint) {
    @content;
  }
}

// Usage
.element {
  padding: 1rem;

  @include responsive(768px) {
    padding: 2rem;
  }
}

// Text truncation mixin
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

// Usage
.title {
  @include truncate(2); // Truncate to 2 lines
}

// Spacing function
@function spacing($multiplier) {
  @return calc($multiplier * var(--spacing-base));
}

.card {
  padding: spacing(2); // 2 * base spacing
  margin-bottom: spacing(4); // 4 * base spacing
}
```

## Design System Integration

### shadcn/ui Patterns
```tsx
// Using shadcn/ui components with custom styles
import { Button } from '@/components/ui/button';
import { cn } from '@/lib/utils';

<Button
  variant="default"
  size="lg"
  className={cn(
    'w-full',
    'sm:w-auto',
    'bg-gradient-to-r from-blue-600 to-purple-600',
    'hover:from-blue-700 hover:to-purple-700'
  )}
>
  Get Started
</Button>

// Custom variant with CVA (class-variance-authority)
import { cva, type VariantProps } from 'class-variance-authority';

const buttonVariants = cva(
  'inline-flex items-center justify-center rounded-md font-medium transition-colors',
  {
    variants: {
      variant: {
        default: 'bg-primary text-primary-foreground hover:bg-primary/90',
        destructive: 'bg-destructive text-destructive-foreground hover:bg-destructive/90',
        outline: 'border border-input hover:bg-accent hover:text-accent-foreground',
        ghost: 'hover:bg-accent hover:text-accent-foreground',
      },
      size: {
        default: 'h-10 px-4 py-2',
        sm: 'h-9 px-3 text-sm',
        lg: 'h-11 px-8',
        icon: 'h-10 w-10',
      },
    },
    defaultVariants: {
      variant: 'default',
      size: 'default',
    },
  }
);
```

### Radix UI Styling
```tsx
// Styling Radix primitives with Tailwind
import * as DropdownMenu from '@radix-ui/react-dropdown-menu';

<DropdownMenu.Content
  className={cn(
    'min-w-[220px]',
    'bg-white dark:bg-gray-800',
    'rounded-md',
    'shadow-md',
    'border border-gray-200 dark:border-gray-700',
    'p-1',
    'animate-in fade-in-80 zoom-in-95',
    'data-[side=bottom]:slide-in-from-top-2',
    'data-[side=top]:slide-in-from-bottom-2'
  )}
>
  <DropdownMenu.Item
    className={cn(
      'relative flex cursor-pointer select-none items-center',
      'rounded-sm px-2 py-1.5 text-sm',
      'outline-none transition-colors',
      'focus:bg-gray-100 dark:focus:bg-gray-700',
      'data-[disabled]:pointer-events-none data-[disabled]:opacity-50'
    )}
  >
    Item
  </DropdownMenu.Item>
</DropdownMenu.Content>
```

## Performance Optimizations

### Critical CSS
```html
<!-- Inline critical above-the-fold styles -->
<head>
  <style>
    /* Critical styles for initial render */
    .hero {
      display: flex;
      align-items: center;
      min-height: 100vh;
      background: linear-gradient(to right, #3b82f6, #8b5cf6);
    }
    .nav {
      display: flex;
      justify-content: space-between;
      padding: 1rem;
    }
  </style>

  <!-- Load non-critical CSS asynchronously -->
  <link
    rel="preload"
    href="/styles/main.css"
    as="style"
    onload="this.onload=null;this.rel='stylesheet'"
  >
  <noscript>
    <link rel="stylesheet" href="/styles/main.css">
  </noscript>
</head>
```

### Animation Performance
```css
/* ❌ Animating layout properties (causes reflow) */
.element {
  transition: width 0.3s, left 0.3s, margin 0.3s;
}

.element:hover {
  width: 200px;
  left: 100px;
}

/* ✅ Animating compositor properties (GPU accelerated) */
.element {
  transition: transform 0.3s, opacity 0.3s;
  will-change: transform;
}

.element:hover {
  transform: translateX(100px) scale(1.1);
  opacity: 0.9;
}

/* ✅ Modern animations with @keyframes */
@keyframes slide-in {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.card {
  animation: slide-in 0.3s ease-out;
}

/* ✅ Respect user preferences */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

## Responsive Design

### Breakpoint Strategy
```scss
// Mobile-first breakpoints
$breakpoints: (
  'xs': 475px,
  'sm': 640px,
  'md': 768px,
  'lg': 1024px,
  'xl': 1280px,
  '2xl': 1536px,
);

// Mixin for consistent breakpoints
@mixin breakpoint($size) {
  @media (min-width: map-get($breakpoints, $size)) {
    @content;
  }
}

// Usage
.container {
  padding: 1rem;

  @include breakpoint('md') {
    padding: 2rem;
  }

  @include breakpoint('lg') {
    padding: 3rem;
  }
}
```

### Fluid Typography
```css
/* ❌ Fixed font sizes */
h1 { font-size: 48px; }
h2 { font-size: 36px; }

/* ✅ Fluid typography with clamp */
:root {
  --font-size-base: clamp(1rem, 0.9rem + 0.5vw, 1.125rem);
  --font-size-lg: clamp(1.125rem, 1rem + 0.625vw, 1.25rem);
  --font-size-xl: clamp(1.25rem, 1.1rem + 0.75vw, 1.5rem);
  --font-size-2xl: clamp(1.5rem, 1.3rem + 1vw, 2rem);
  --font-size-3xl: clamp(2rem, 1.6rem + 2vw, 3rem);
}

h1 {
  font-size: var(--font-size-3xl);
  line-height: 1.2;
}

h2 {
  font-size: var(--font-size-2xl);
  line-height: 1.3;
}

/* ✅ Fluid spacing */
.section {
  padding-block: clamp(2rem, 5vw, 6rem);
}
```

## Real-World Applications

### Example 1: Responsive Navigation
```tsx
import { cn } from '@/lib/utils';
import { useState } from 'react';

export function Navigation() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <nav className="bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          {/* Logo */}
          <div className="flex items-center">
            <img
              src="/logo.svg"
              alt="Logo"
              className="h-8 w-auto"
            />
          </div>

          {/* Desktop navigation */}
          <div className="hidden md:flex md:items-center md:space-x-8">
            <a
              href="/features"
              className={cn(
                'text-sm font-medium',
                'text-gray-700 dark:text-gray-300',
                'hover:text-gray-900 dark:hover:text-white',
                'transition-colors duration-150'
              )}
            >
              Features
            </a>
            <a
              href="/pricing"
              className="text-sm font-medium text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white transition-colors duration-150"
            >
              Pricing
            </a>
          </div>

          {/* Mobile menu button */}
          <div className="flex items-center md:hidden">
            <button
              onClick={() => setIsOpen(!isOpen)}
              className={cn(
                'p-2 rounded-md',
                'text-gray-700 dark:text-gray-300',
                'hover:bg-gray-100 dark:hover:bg-gray-800',
                'focus:outline-none focus:ring-2 focus:ring-blue-500'
              )}
              aria-expanded={isOpen}
              aria-label="Toggle menu"
            >
              <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                {isOpen ? (
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                ) : (
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                )}
              </svg>
            </button>
          </div>
        </div>
      </div>

      {/* Mobile menu */}
      <div
        className={cn(
          'md:hidden overflow-hidden transition-all duration-300 ease-in-out',
          isOpen ? 'max-h-screen opacity-100' : 'max-h-0 opacity-0'
        )}
      >
        <div className="px-2 pt-2 pb-3 space-y-1">
          <a
            href="/features"
            className="block px-3 py-2 rounded-md text-base font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800"
          >
            Features
          </a>
          <a
            href="/pricing"
            className="block px-3 py-2 rounded-md text-base font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800"
          >
            Pricing
          </a>
        </div>
      </div>
    </nav>
  );
}
```

### Example 2: Dark Mode Implementation
```tsx
// context/ThemeContext.tsx
import { createContext, useContext, useEffect, useState } from 'react';

type Theme = 'light' | 'dark' | 'system';

const ThemeContext = createContext<{
  theme: Theme;
  setTheme: (theme: Theme) => void;
}>({
  theme: 'system',
  setTheme: () => null,
});

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [theme, setTheme] = useState<Theme>('system');

  useEffect(() => {
    const root = window.document.documentElement;
    root.classList.remove('light', 'dark');

    if (theme === 'system') {
      const systemTheme = window.matchMedia('(prefers-color-scheme: dark)').matches
        ? 'dark'
        : 'light';
      root.classList.add(systemTheme);
    } else {
      root.classList.add(theme);
    }
  }, [theme]);

  return (
    <ThemeContext.Provider value={{ theme, setTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

export const useTheme = () => useContext(ThemeContext);
```

```css
/* globals.css - Dark mode styles */
:root {
  --background: 0 0% 100%;
  --foreground: 222.2 84% 4.9%;
  --primary: 222.2 47.4% 11.2%;
  --primary-foreground: 210 40% 98%;
}

.dark {
  --background: 222.2 84% 4.9%;
  --foreground: 210 40% 98%;
  --primary: 210 40% 98%;
  --primary-foreground: 222.2 47.4% 11.2%;
}

* {
  border-color: hsl(var(--border));
}

body {
  background-color: hsl(var(--background));
  color: hsl(var(--foreground));
}
```

## Common Issues Detection

### Duplicate Rules
```css
/* ❌ Detect and suggest consolidation */
.card {
  padding: 1rem;
  border-radius: 0.5rem;
}

.card {
  padding: 1rem; /* Duplicate */
  margin-bottom: 1rem;
}

/* ✅ Consolidated */
.card {
  padding: 1rem;
  border-radius: 0.5rem;
  margin-bottom: 1rem;
}
```

### Unused Styles
- Identify selectors not matching any elements
- Flag CSS rules never applied
- Suggest removal of dead code
- Use tools like PurgeCSS in production

### Color Inconsistencies
```css
/* ❌ Multiple similar colors */
.button-1 { color: #3b82f6; }
.button-2 { color: #3b82f5; } /* Almost identical */
.button-3 { color: rgb(59, 130, 246); } /* Same as first */

/* ✅ Suggest: Use design system variables */
:root {
  --color-primary: #3b82f6;
}

.button-1,
.button-2,
.button-3 {
  color: var(--color-primary);
}
```

## Best Practices

### 1. Use Design Tokens
- Define all colors, spacing, and typography in variables
- Create semantic naming (--color-primary, not --blue-500)
- Implement consistent spacing scale
- Use CSS custom properties for theming

### 2. Mobile-First Approach
- Start with mobile styles
- Add complexity at larger breakpoints
- Test on real devices
- Use responsive images and fonts

### 3. Accessibility
- Ensure sufficient color contrast (WCAG AA: 4.5:1 for text)
- Provide focus indicators
- Use relative units (rem, em) for font sizes
- Respect prefers-reduced-motion

### 4. Performance
- Minimize specificity
- Use CSS containment
- Avoid expensive properties (box-shadow on large lists)
- Implement critical CSS strategy

### 5. Maintainability
- Follow consistent naming conventions (BEM, OOCSS)
- Use CSS Modules or scoped styles
- Document complex calculations
- Keep selectors shallow

## Common Pitfalls

### 1. !important Overuse
```css
/* ❌ Using !important to fix specificity */
.button {
  color: blue !important;
}

/* ✅ Fix specificity properly */
.nav .button {
  color: blue;
}
```

### 2. Magic Numbers
```css
/* ❌ Random values without context */
.element {
  margin-top: 23px;
  padding-left: 17px;
}

/* ✅ Use spacing scale */
.element {
  margin-top: var(--spacing-3); /* 24px */
  padding-left: var(--spacing-2); /* 16px */
}
```

### 3. Absolute Units
```css
/* ❌ Fixed pixel sizes */
body {
  font-size: 16px;
}

h1 {
  font-size: 32px;
}

/* ✅ Relative units */
body {
  font-size: 1rem; /* Respects user preferences */
}

h1 {
  font-size: 2rem; /* Scales with root */
}
```

### 4. Color Contrast
```css
/* ❌ Poor contrast (fails WCAG) */
.text {
  color: #999; /* 2.8:1 on white */
  background: #fff;
}

/* ✅ Sufficient contrast */
.text {
  color: #666; /* 5.7:1 on white */
  background: #fff;
}
```

### 5. Layout Thrashing
```tsx
// ❌ Reading layout, then writing (causes reflow)
const height = element.offsetHeight;
element.style.height = height + 10 + 'px';

// ✅ Use CSS when possible
.element {
  height: calc(100% + 10px);
}
```

## Suggestions Output

### Format
```markdown
💡 Style Suggestion:

**Issue**: Hardcoded color value
**Location**: Component.tsx:45
**Current**: `style={{ color: '#3b82f6' }}`
**Suggested**: `className="text-blue-600"`
**Reason**: Use Tailwind utilities for consistency and dark mode support
**Impact**: Better maintainability, automatic dark mode
```

### Auto-complete
Provide intelligent auto-completion for:
- Tailwind classes with descriptions
- CSS properties with browser support
- SCSS variables from your theme
- Design tokens from your system
- Common responsive patterns

## Related Skills

- **react-guardian**: Ensures React component best practices
- **performance-monitor**: Optimizes CSS and animation performance
- **a11y-checker**: Validates accessibility of styles (contrast, focus states)
