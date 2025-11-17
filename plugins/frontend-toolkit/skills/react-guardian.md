---
name: react-guardian
description: Enforces React best practices automatically
allowed-tools: Read, Grep, Glob
---

# React Guardian Skill

Automatically monitor and enforce React best practices during development.

## Auto-invocation Triggers

### File Patterns
- `**/*.tsx` - TypeScript React components
- `**/*.jsx` - JavaScript React components
- `**/*.ts` - Potential hooks files
- `**/use*.ts` - Custom hooks

### Tool Usage
- When `Write` tool creates React files
- When `Edit` tool modifies React components
- When generating components or hooks

### Keywords
- `component`
- `useState`
- `useEffect`
- `props`
- `render`
- `React.FC`
- `React.memo`

### Import Detection
```typescript
// Triggers on these imports
import React from 'react';
import { useState, useEffect } from 'react';
import { FC, ReactNode } from 'react';
```

## Validation Rules

### Hooks Rules
```typescript
// ❌ Violation: Conditional hook
if (condition) {
  const [state, setState] = useState();
}

// ❌ Violation: Hook in nested function
function Component() {
  function nested() {
    const [state, setState] = useState(); // Error!
  }
}

// ✅ Correct: Hooks at top level
function Component() {
  const [state, setState] = useState();
  // ...
}
```

### Key Props
```typescript
// ❌ Missing key in list
items.map(item => <Item {...item} />)

// ✅ Correct: Unique key provided
items.map(item => <Item key={item.id} {...item} />)
```

### Performance Patterns
```typescript
// Suggest memo for expensive components
// If component has >100 lines or complex props
export const Component = memo(() => {
  // Component logic
});

// Suggest useCallback for handlers
const handleClick = useCallback(() => {
  // Handler logic
}, [dependency]);
```

## Best Practices Enforcement

### Component Structure
```typescript
// ✅ Recommended structure
interface ComponentProps {
  // Props definition
}

export const Component: FC<ComponentProps> = ({
  prop1,
  prop2,
}) => {
  // Hooks first
  const [state, setState] = useState();

  // Effects next
  useEffect(() => {
    // Effect logic
  }, []);

  // Handlers
  const handleEvent = () => {};

  // Render
  return <div>Content</div>;
};
```

### TypeScript Types
```typescript
// ❌ Avoid 'any' type
const data: any = fetchData();

// ✅ Use proper types
interface Data {
  id: string;
  name: string;
}
const data: Data = fetchData();
```

### Accessibility Props
```typescript
// Check for missing accessibility
// ❌ Image without alt
<img src="photo.jpg" />

// ✅ Proper alt text
<img src="photo.jpg" alt="Description" />

// ❌ Click handler on div
<div onClick={handler}>Click me</div>

// ✅ Use semantic button
<button onClick={handler}>Click me</button>
```

## Anti-patterns Detection

### Direct State Mutation
```typescript
// ❌ Mutating state
state.items.push(newItem);
setState(state);

// ✅ Creating new state
setState({
  ...state,
  items: [...state.items, newItem]
});
```

### Missing Dependencies
```typescript
// ❌ Missing dependency
useEffect(() => {
  console.log(value);
}, []); // 'value' missing

// ✅ Complete dependencies
useEffect(() => {
  console.log(value);
}, [value]);
```

### Inline Functions
```typescript
// ❌ Inline function causing re-renders
<Child onClick={() => doSomething()} />

// ✅ Memoized callback
const handleClick = useCallback(() => doSomething(), []);
<Child onClick={handleClick} />
```

## Suggestions

### When to Apply
- During component creation
- When editing existing components
- Before commits (if integrated with hooks)
- During code reviews

### Severity Levels
- **Error**: Hooks violations, missing keys
- **Warning**: Missing memo, large components
- **Info**: Style suggestions, naming conventions

### Auto-fix Capabilities
- Add missing keys (using index as fallback)
- Add missing TypeScript types
- Convert class components to functional
- Add display names to components

## Integration Output
When triggered, provide:
1. Issue identification with line numbers
2. Explanation of why it's an issue
3. Suggested fix with code example
4. Links to React documentation
5. Performance impact if applicable