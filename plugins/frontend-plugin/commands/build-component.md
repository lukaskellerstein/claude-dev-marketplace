---
description: Build a production-ready React component with TypeScript, styling, and tests
---

Build a comprehensive, production-ready React component based on the specified requirements.

## Process

Follow these steps:

1. **Analyze Requirements**: Understand the component purpose, props interface, styling needs, and interaction patterns from the user's request

2. **Design Component Architecture**: Use the `react-expert` agent to:
   - Define component props interface with TypeScript
   - Plan state management approach
   - Design component composition and structure
   - Identify reusable custom hooks
   - Plan accessibility features (ARIA attributes, keyboard navigation)

3. **Implement Styling**: Use the `css-tailwind-expert` agent to:
   - Create responsive styles with Tailwind CSS
   - Integrate shadcn-ui or Radix UI components if applicable
   - Implement component variants
   - Add animations and transitions
   - Ensure dark mode support

4. **Ensure Responsiveness**: Use the `responsive-design-expert` agent to:
   - Verify mobile-first responsive behavior
   - Test across breakpoints
   - Ensure touch-friendly interactions
   - Optimize performance for mobile devices

5. **Generate Tests** (optional): Create test cases for:
   - Component rendering
   - User interactions
   - Props variations
   - Accessibility features

## Output

Present a complete component implementation including:

### 1. Component File
```typescript
// components/YourComponent.tsx
```
Complete TypeScript React component with:
- Proper TypeScript interfaces
- JSDoc comments
- Accessibility attributes
- Error handling

### 2. Styles
- Tailwind CSS classes integrated in component
- Custom CSS/SCSS if needed
- Responsive variations
- Dark mode support

### 3. Usage Example
```typescript
// Example usage in parent component
```

### 4. Props Documentation
Table or list of all props:
- Name, type, default value, description
- Required vs optional props
- Variant options

### 5. Accessibility Features
- ARIA attributes used
- Keyboard navigation support
- Screen reader compatibility
- Focus management

### 6. Test File (if requested)
```typescript
// __tests__/YourComponent.test.tsx
```

## Best Practices

Ensure the component follows:
- Single Responsibility Principle
- Composition over inheritance
- Proper TypeScript typing
- Accessibility standards (WCAG 2.1)
- Performance optimization (memoization where needed)
- Responsive design (mobile-first)
- Clean code principles

## Examples

### Simple Component
```
/build-component

Create a Button component with variants (primary, secondary, danger), sizes (sm, md, lg), and loading state
```

### Complex Component
```
/build-component

Build a DataTable component with:
- Sortable columns
- Pagination
- Row selection
- Responsive mobile view (cards)
- Loading and empty states
```

### Form Component
```
/build-component

Create a SearchInput component with:
- Debounced input
- Clear button
- Loading indicator
- Keyboard shortcuts (Cmd+K to focus)
- Autocomplete dropdown
```

Make all recommendations specific and actionable with complete, production-ready code.
