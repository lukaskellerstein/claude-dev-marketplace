---
name: react-guardian
description: Master React best practices for robust, maintainable applications. Use when writing components, implementing hooks, ensuring type safety, fixing violations, or enforcing React patterns and conventions.
allowed-tools: Read, Grep, Glob
---

# React Guardian Skill

Automatically monitor and enforce React best practices during development.

## When to Use This Skill

This skill automatically activates and provides assistance in these specific scenarios:

1. **Component Creation** - When creating new React functional components
2. **Hook Implementation** - When using useState, useEffect, or custom hooks
3. **Props Type Checking** - When defining component props without TypeScript types
4. **List Rendering** - When mapping arrays to JSX elements
5. **Event Handlers** - When adding onClick, onChange, or other event handlers
6. **Effect Dependencies** - When writing useEffect with dependency arrays
7. **Accessibility Issues** - Missing ARIA attributes or semantic HTML
8. **State Mutations** - Detecting direct state modifications
9. **Ref Usage** - When using useRef or forwardRef
10. **Context Implementation** - When creating or consuming React Context
11. **Performance Patterns** - Missing memo, useMemo, or useCallback
12. **TypeScript Integration** - Ensuring proper type definitions
13. **Component Structure** - Organizing component code logically
14. **Class to Functional Migration** - Converting legacy class components
15. **React 18+ Features** - Implementing Suspense, transitions, or concurrent features

## Quick Start

### Step 1: Automatic Monitoring
The skill monitors your code in real-time as you write React components. No setup required.

### Step 2: Instant Feedback
When best practice violations are detected, you receive:
- Clear error/warning with line numbers
- Explanation of why it's problematic
- Code example showing the fix
- Links to official React documentation

### Step 3: Apply Fixes
Follow the suggested patterns to write better React code. The skill categorizes issues by severity:
- **Error**: Critical violations (hooks rules, missing keys)
- **Warning**: Important patterns (missing memo, large components)
- **Info**: Style improvements (naming, structure)

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

// ❌ Violation: Hook in loop
for (let i = 0; i < count; i++) {
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
  const [count, setCount] = useState(0);

  useEffect(() => {
    // Effect logic
  }, []);

  // Rest of component
}
```

### Custom Hooks Rules
```typescript
// ❌ Custom hook not starting with 'use'
function fetchData() {
  const [data, setData] = useState(null); // Violates rules
  return data;
}

// ✅ Proper custom hook naming
function useFetchData(url: string) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    setLoading(true);
    fetch(url)
      .then(res => res.json())
      .then(data => {
        setData(data);
        setLoading(false);
      });
  }, [url]);

  return { data, loading };
}
```

### Key Props
```typescript
// ❌ Missing key in list
items.map(item => <Item {...item} />)

// ❌ Using index as key (anti-pattern if items can reorder)
items.map((item, index) => <Item key={index} {...item} />)

// ✅ Correct: Unique stable key provided
items.map(item => <Item key={item.id} {...item} />)

// ✅ Using composite key when needed
users.map(user =>
  user.posts.map(post => (
    <Post key={`${user.id}-${post.id}`} post={post} />
  ))
)
```

### Performance Patterns
```typescript
// Suggest memo for expensive components
// If component has >100 lines or complex props
export const Component = memo(({ data, onUpdate }) => {
  // Component logic
});

// Suggest useCallback for event handlers
const handleClick = useCallback(() => {
  // Handler logic
}, [dependency]);

// Suggest useMemo for expensive computations
const sortedData = useMemo(
  () => data.sort(complexComparison),
  [data]
);
```

## Best Practices Enforcement

### Component Structure
```typescript
// ✅ Recommended structure
interface ComponentProps {
  title: string;
  items: Item[];
  onItemClick: (id: string) => void;
}

export const Component: FC<ComponentProps> = ({
  title,
  items,
  onItemClick,
}) => {
  // 1. Hooks first
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [filter, setFilter] = useState('');

  // 2. Derived state
  const filteredItems = useMemo(
    () => items.filter(item => item.name.includes(filter)),
    [items, filter]
  );

  // 3. Effects
  useEffect(() => {
    // Effect logic
  }, [selectedId]);

  // 4. Event handlers
  const handleClick = useCallback((id: string) => {
    setSelectedId(id);
    onItemClick(id);
  }, [onItemClick]);

  // 5. Early returns
  if (items.length === 0) {
    return <EmptyState />;
  }

  // 6. Main render
  return (
    <div>
      <h2>{title}</h2>
      {filteredItems.map(item => (
        <Item key={item.id} item={item} onClick={handleClick} />
      ))}
    </div>
  );
};

Component.displayName = 'Component';
```

### TypeScript Types
```typescript
// ❌ Avoid 'any' type
const data: any = fetchData();
const onClick: any = () => {};

// ✅ Use proper types
interface Data {
  id: string;
  name: string;
  metadata: Record<string, unknown>;
}

const data: Data = fetchData();
const onClick: (id: string) => void = (id) => console.log(id);

// ✅ Use React types
import { FC, ReactNode, MouseEvent, ChangeEvent } from 'react';

interface Props {
  children: ReactNode;
  onSubmit: (e: FormEvent<HTMLFormElement>) => void;
}

const Component: FC<Props> = ({ children, onSubmit }) => {
  const handleClick = (e: MouseEvent<HTMLButtonElement>) => {
    e.preventDefault();
  };

  return <form onSubmit={onSubmit}>{children}</form>;
};
```

### Accessibility Props
```typescript
// ❌ Image without alt
<img src="photo.jpg" />

// ✅ Proper alt text
<img src="photo.jpg" alt="Description of photo" />

// ❌ Decorative image with alt text
<img src="divider.png" alt="divider" />

// ✅ Decorative image
<img src="divider.png" alt="" role="presentation" />

// ❌ Click handler on div
<div onClick={handler}>Click me</div>

// ✅ Use semantic button
<button onClick={handler}>Click me</button>

// ❌ Missing ARIA for custom controls
<div onClick={toggle}>Menu</div>

// ✅ Proper ARIA attributes
<button
  onClick={toggle}
  aria-expanded={isOpen}
  aria-controls="menu-panel"
  aria-label="Toggle menu"
>
  Menu
</button>
```

## Anti-patterns Detection

### Direct State Mutation
```typescript
// ❌ Mutating state directly
const [items, setItems] = useState<Item[]>([]);

// Wrong!
items.push(newItem);
setItems(items);

// Wrong!
state.user.name = 'New Name';
setState(state);

// ✅ Creating new state
setItems([...items, newItem]);

// ✅ Using immutable update
setState(prevState => ({
  ...prevState,
  user: {
    ...prevState.user,
    name: 'New Name'
  }
}));

// ✅ Using immer for complex updates
import { produce } from 'immer';

setState(produce(draft => {
  draft.user.name = 'New Name';
  draft.items.push(newItem);
}));
```

### Missing Dependencies
```typescript
// ❌ Missing dependency
useEffect(() => {
  console.log(value);
}, []); // 'value' missing

// ❌ Disabling exhaustive-deps
useEffect(() => {
  doSomething(value);
  // eslint-disable-next-line react-hooks/exhaustive-deps
}, []);

// ✅ Complete dependencies
useEffect(() => {
  console.log(value);
}, [value]);

// ✅ Using callback to avoid dependency
useEffect(() => {
  setState(prev => prev + 1); // No dependency needed
}, []);
```

### Inline Functions
```typescript
// ❌ Inline function causing re-renders
<Child onClick={() => doSomething()} />

// ❌ Inline function with parameters
{items.map(item => (
  <Item key={item.id} onClick={() => handleClick(item.id)} />
))}

// ✅ Memoized callback
const handleClick = useCallback(() => doSomething(), []);
<Child onClick={handleClick} />

// ✅ Separate component with callback
const ItemRow = memo(({ item, onItemClick }) => {
  const handleClick = useCallback(
    () => onItemClick(item.id),
    [onItemClick, item.id]
  );

  return <Item onClick={handleClick} />;
});
```

### Stale Closures
```typescript
// ❌ Stale closure in interval
useEffect(() => {
  const id = setInterval(() => {
    setCount(count + 1); // 'count' is stale
  }, 1000);
  return () => clearInterval(id);
}, []); // Empty deps causes stale closure

// ✅ Use functional update
useEffect(() => {
  const id = setInterval(() => {
    setCount(c => c + 1);
  }, 1000);
  return () => clearInterval(id);
}, []);

// ✅ Include dependency
useEffect(() => {
  const id = setInterval(() => {
    setCount(count + 1);
  }, 1000);
  return () => clearInterval(id);
}, [count]); // Recreates interval when count changes
```

## Real-World Applications

### Example 1: Form Component with Validation
```typescript
interface FormProps {
  onSubmit: (data: FormData) => void;
}

interface FormData {
  email: string;
  password: string;
}

interface FormErrors {
  email?: string;
  password?: string;
}

export const LoginForm: FC<FormProps> = ({ onSubmit }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [errors, setErrors] = useState<FormErrors>({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Validate on blur
  const validateEmail = useCallback((value: string) => {
    if (!value) return 'Email is required';
    if (!/\S+@\S+\.\S+/.test(value)) return 'Email is invalid';
    return undefined;
  }, []);

  const handleEmailBlur = useCallback(() => {
    const error = validateEmail(email);
    setErrors(prev => ({ ...prev, email: error }));
  }, [email, validateEmail]);

  const handleSubmit = useCallback(async (e: FormEvent) => {
    e.preventDefault();

    const emailError = validateEmail(email);
    const passwordError = password ? undefined : 'Password is required';

    if (emailError || passwordError) {
      setErrors({ email: emailError, password: passwordError });
      return;
    }

    setIsSubmitting(true);
    try {
      await onSubmit({ email, password });
    } finally {
      setIsSubmitting(false);
    }
  }, [email, password, validateEmail, onSubmit]);

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label htmlFor="email">Email</label>
        <input
          id="email"
          type="email"
          value={email}
          onChange={e => setEmail(e.target.value)}
          onBlur={handleEmailBlur}
          aria-invalid={!!errors.email}
          aria-describedby={errors.email ? 'email-error' : undefined}
        />
        {errors.email && (
          <span id="email-error" role="alert">
            {errors.email}
          </span>
        )}
      </div>

      <div>
        <label htmlFor="password">Password</label>
        <input
          id="password"
          type="password"
          value={password}
          onChange={e => setPassword(e.target.value)}
          aria-invalid={!!errors.password}
          aria-describedby={errors.password ? 'password-error' : undefined}
        />
        {errors.password && (
          <span id="password-error" role="alert">
            {errors.password}
          </span>
        )}
      </div>

      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? 'Signing in...' : 'Sign in'}
      </button>
    </form>
  );
};
```

### Example 2: Data Fetching with Custom Hook
```typescript
interface UseDataOptions<T> {
  initialData?: T;
  onSuccess?: (data: T) => void;
  onError?: (error: Error) => void;
}

interface UseDataResult<T> {
  data: T | null;
  loading: boolean;
  error: Error | null;
  refetch: () => void;
}

function useData<T>(
  url: string,
  options: UseDataOptions<T> = {}
): UseDataResult<T> {
  const { initialData = null, onSuccess, onError } = options;

  const [data, setData] = useState<T | null>(initialData);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const fetchData = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const json = await response.json();
      setData(json);
      onSuccess?.(json);
    } catch (e) {
      const error = e instanceof Error ? e : new Error('Unknown error');
      setError(error);
      onError?.(error);
    } finally {
      setLoading(false);
    }
  }, [url, onSuccess, onError]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  return { data, loading, error, refetch: fetchData };
}

// Usage
function UserProfile({ userId }: { userId: string }) {
  const { data, loading, error, refetch } = useData<User>(
    `/api/users/${userId}`,
    {
      onSuccess: (user) => console.log('Loaded user:', user.name),
      onError: (err) => console.error('Failed to load user:', err),
    }
  );

  if (loading) return <Spinner />;
  if (error) return <ErrorMessage error={error} onRetry={refetch} />;
  if (!data) return <EmptyState />;

  return <UserCard user={data} />;
}
```

## Best Practices

### 1. Component Organization
- Keep components focused and single-purpose
- Extract reusable logic into custom hooks
- Use composition over prop drilling
- Implement proper error boundaries

### 2. State Management
- Lift state only when necessary
- Use reducers for complex state logic
- Consider context for deeply nested props
- Avoid global state when local state suffices

### 3. TypeScript Integration
- Define explicit prop types
- Use generics for reusable components
- Leverage type inference where appropriate
- Avoid 'any' type unless absolutely necessary

### 4. Performance
- Memoize expensive computations
- Use React.memo for pure components
- Implement proper key props
- Avoid inline functions in JSX

### 5. Accessibility
- Use semantic HTML elements
- Provide meaningful alt text
- Implement keyboard navigation
- Include ARIA attributes when needed

## Common Pitfalls

### 1. Unnecessary useEffect
```typescript
// ❌ useEffect for derived state
const [items, setItems] = useState([]);
const [filteredItems, setFilteredItems] = useState([]);

useEffect(() => {
  setFilteredItems(items.filter(item => item.active));
}, [items]);

// ✅ Calculate during render
const [items, setItems] = useState([]);
const filteredItems = items.filter(item => item.active);
```

### 2. Creating Objects in Render
```typescript
// ❌ New object every render
<Component style={{ margin: 10 }} />

// ✅ Stable reference
const style = { margin: 10 };
<Component style={style} />

// Or use useMemo for dynamic values
const style = useMemo(() => ({ margin: spacing }), [spacing]);
```

### 3. Too Many Props
```typescript
// ❌ Too many props (prop drilling)
function Parent() {
  return (
    <Child
      prop1={a}
      prop2={b}
      prop3={c}
      prop4={d}
      prop5={e}
      prop6={f}
    />
  );
}

// ✅ Use composition or context
function Parent() {
  const config = { prop1: a, prop2: b, prop3: c };
  return (
    <ConfigContext.Provider value={config}>
      <Child />
    </ConfigContext.Provider>
  );
}
```

### 4. Ignoring Cleanup
```typescript
// ❌ Missing cleanup
useEffect(() => {
  const subscription = api.subscribe(userId, handleUpdate);
  // Memory leak!
}, [userId]);

// ✅ Proper cleanup
useEffect(() => {
  const subscription = api.subscribe(userId, handleUpdate);
  return () => subscription.unsubscribe();
}, [userId, handleUpdate]);
```

### 5. Forgetting Display Names
```typescript
// ❌ Anonymous components
export default memo(() => <div>Content</div>);

// ✅ Named components
const Component = memo(() => <div>Content</div>);
Component.displayName = 'Component';
export default Component;
```

## React 18+ Features

### Concurrent Features
```typescript
// useTransition for non-urgent updates
const [isPending, startTransition] = useTransition();

function handleTabChange(tab: string) {
  startTransition(() => {
    setActiveTab(tab); // Non-urgent update
  });
}

// useDeferredValue for deferred rendering
const deferredQuery = useDeferredValue(searchQuery);

return <SearchResults query={deferredQuery} />;
```

### Suspense Boundaries
```typescript
// Wrap async components
<Suspense fallback={<Loading />}>
  <UserProfile userId={userId} />
</Suspense>

// Multiple suspense boundaries
<Suspense fallback={<HeaderSkeleton />}>
  <Header />
  <Suspense fallback={<ContentSkeleton />}>
    <Content />
  </Suspense>
</Suspense>
```

### Error Boundaries
```typescript
class ErrorBoundary extends React.Component<
  { children: ReactNode },
  { hasError: boolean }
> {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error: Error) {
    return { hasError: true };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('Error caught:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return <ErrorFallback />;
    }

    return this.props.children;
  }
}
```

## Integration Output

When triggered, provide:
1. Issue identification with line numbers
2. Explanation of why it's an issue
3. Suggested fix with code example
4. Links to React documentation
5. Performance impact if applicable

## Related Skills

- **performance-monitor**: Optimizes React component performance
- **style-assistant**: Ensures consistent styling patterns
- **test-writer**: Creates tests for React components
