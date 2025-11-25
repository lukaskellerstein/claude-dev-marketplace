---
description: Create or enhance a design system with tokens, components, and documentation
---

Create a comprehensive design system with design tokens, reusable components, and documentation.

## Process

Follow these steps:

1. **Analyze Current State**: Examine existing codebase to:
   - Identify current styling patterns
   - Review existing components
   - Find inconsistencies in spacing, colors, typography
   - Understand project requirements (frameworks, libraries)

2. **Define Design Tokens**: Use the `frontend-plugin:css-tailwind-expert` agent to:
   - Create color system (primary, secondary, semantic colors)
   - Define typography scale (font families, sizes, weights, line heights)
   - Establish spacing scale (4pt or 8pt grid system)
   - Set up border radius, shadows, and effects
   - Configure breakpoints
   - Plan theming strategy (light/dark modes)

3. **Configure Tailwind**: Set up or enhance `tailwind.config.js`:
   - Extend theme with custom design tokens
   - Configure content paths
   - Add necessary plugins
   - Set up dark mode strategy
   - Configure JIT mode

4. **Build Component Library**: Use the `frontend-plugin:react-expert` agent to create:
   - Primitive components (Button, Input, Card, Badge, etc.)
   - Composite components (Form, Modal, Dropdown, etc.)
   - Layout components (Container, Grid, Stack, etc.)
   - Integrate shadcn-ui components where applicable

5. **Ensure Consistency**: Use the `frontend-plugin:responsive-design-expert` agent to:
   - Verify responsive behavior across all components
   - Ensure consistent spacing and sizing
   - Validate accessibility standards
   - Test component combinations

6. **Create Documentation**:
   - Component API documentation
   - Usage examples
   - Design principles
   - Contribution guidelines

## Output

Present a complete design system including:

### 1. Design Tokens Configuration

**Tailwind Config**
```javascript
// tailwind.config.js
module.exports = {
  darkMode: 'class',
  content: ['./src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        // Color system
      },
      fontFamily: {
        // Typography
      },
      spacing: {
        // Custom spacing
      }
    }
  },
  plugins: []
}
```

**CSS Variables** (if using)
```css
/* globals.css */
:root {
  /* Light mode variables */
}

.dark {
  /* Dark mode variables */
}
```

### 2. Component Library Structure

```
src/
├── components/
│   ├── ui/              # Primitive components
│   │   ├── button.tsx
│   │   ├── input.tsx
│   │   ├── card.tsx
│   │   └── ...
│   ├── composed/        # Composite components
│   │   ├── form.tsx
│   │   ├── modal.tsx
│   │   └── ...
│   └── layout/          # Layout components
│       ├── container.tsx
│       ├── grid.tsx
│       └── ...
├── lib/
│   └── utils.ts         # cn() utility, etc.
└── styles/
    └── globals.css
```

### 3. Core Components

Provide implementation for:
- **Button**: All variants, sizes, states
- **Input**: Text, email, password, with validation states
- **Card**: Header, content, footer composition
- **Badge**: Variants and sizes
- **Typography**: Heading, Text, Label components
- **Layout**: Container, Grid, Stack, Spacer

### 4. Component Documentation

For each component:

```markdown
## Button

### Props
| Prop | Type | Default | Description |
|------|------|---------|-------------|
| variant | 'primary' \| 'secondary' \| 'ghost' | 'primary' | Visual style |
| size | 'sm' \| 'md' \| 'lg' | 'md' | Component size |
| disabled | boolean | false | Disabled state |

### Usage
[Code examples]

### Variants
[Visual examples of all variants]

### Accessibility
[ARIA attributes, keyboard support]
```

### 5. Design Principles Document

```markdown
# Design System Principles

## Color System
- Primary: Brand identity
- Secondary: Supporting actions
- Semantic: Success, warning, error, info

## Typography Scale
- Display: Hero sections
- Heading: Section titles
- Body: Main content
- Caption: Supporting text

## Spacing Scale
8pt grid system: 0, 4, 8, 12, 16, 24, 32, 48, 64, 96

## Component Variants
Each component should support:
- Size variants: sm, md, lg
- State variants: default, hover, active, disabled
- Theme variants: light, dark
```

### 6. Utility Functions

```typescript
// lib/utils.ts
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
```

## Design System Checklist

- [ ] Color system with semantic naming
- [ ] Typography scale (5-7 levels)
- [ ] Spacing scale (8pt grid recommended)
- [ ] Consistent border radius values
- [ ] Shadow system for depth
- [ ] Responsive breakpoints
- [ ] Dark mode support
- [ ] Accessibility standards (WCAG 2.1)
- [ ] Icon system integration
- [ ] Animation/transition standards
- [ ] Component library (10+ components)
- [ ] Documentation for each component
- [ ] Usage examples
- [ ] Storybook or component playground (optional)

## Examples

### Basic Design System
```
/create-design-system

Create a basic design system with:
- Color palette (brand colors, semantic colors)
- Typography (2 font families, 5 size levels)
- 10 core components (Button, Input, Card, Badge, Avatar, Dropdown, Modal, Toast, Tabs, Checkbox)
- Tailwind configuration
```

### Enhanced Design System
```
/create-design-system

Enhance existing design system with:
- Dark mode support
- Animation tokens
- Advanced components (DataTable, Calendar, CommandPalette)
- Storybook documentation
- Design tokens exported as JSON
```

### Enterprise Design System
```
/create-design-system

Build enterprise design system with:
- Multi-brand theming support
- Accessibility-first components
- Full shadcn-ui integration
- Component composition patterns
- Testing infrastructure
- Figma design tokens integration
```

Provide complete, production-ready code with all configurations and documentation.
