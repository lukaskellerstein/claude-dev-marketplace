---
name: optimize-react-rendering
description: Auto-invoked when writing React components to prevent unnecessary re-renders and optimize performance
allowed-tools: Read, Grep, Glob
---

# Optimize React Rendering

This skill provides guidance on optimizing React component rendering to prevent unnecessary re-renders and improve application performance.

## When Active

This skill activates when you:
- Write React components
- Use useState, useEffect, useCallback, useMemo hooks
- Pass props to child components
- Work with Context API
- Implement event handlers
- Create lists or tables
- Work with forms and inputs
- Implement real-time features

## Common Performance Issues

### 1. Missing Memoization

#### Problem: Component Re-renders Unnecessarily
```javascript
// ❌ BAD: Component re-renders even when props haven't changed
function UserCard({ user, onClick }) {
  console.log('UserCard rendered');

  return (
    <div onClick={() => onClick(user.id)}>
      <h3>{user.name}</h3>
      <p>{user.email}</p>
    </div>
  );
}

// Parent component
function UserList({ users }) {
  const [count, setCount] = useState(0);

  const handleClick = (userId) => {
    console.log('Clicked:', userId);
  };

  return (
    <>
      <button onClick={() => setCount(count + 1)}>Count: {count}</button>
      {users.map(user => (
        <UserCard key={user.id} user={user} onClick={handleClick} />
      ))}
    </>
  );
}
// Issue: All UserCards re-render when count changes
```

#### Solution: Use React.memo and useCallback
```javascript
// ✅ GOOD: Component only re-renders when props change
const UserCard = React.memo(({ user, onClick }) => {
  console.log('UserCard rendered');

  return (
    <div onClick={() => onClick(user.id)}>
      <h3>{user.name}</h3>
      <p>{user.email}</p>
    </div>
  );
});

// Parent component
function UserList({ users }) {
  const [count, setCount] = useState(0);

  // Memoize callback to prevent new function on every render
  const handleClick = useCallback((userId) => {
    console.log('Clicked:', userId);
  }, []);

  return (
    <>
      <button onClick={() => setCount(count + 1)}>Count: {count}</button>
      {users.map(user => (
        <UserCard key={user.id} user={user} onClick={handleClick} />
      ))}
    </>
  );
}
// Now: UserCards only re-render when user data changes
```

### 2. Expensive Calculations Without Memoization

#### Problem: Recalculating on Every Render
```javascript
// ❌ BAD: Filters and sorts on every render
function ProductList({ products, category }) {
  // This runs on EVERY render, even unrelated state changes
  const filteredProducts = products
    .filter(p => p.category === category)
    .sort((a, b) => b.rating - a.rating);

  return (
    <div>
      {filteredProducts.map(product => (
        <ProductCard key={product.id} product={product} />
      ))}
    </div>
  );
}
```

#### Solution: Use useMemo
```javascript
// ✅ GOOD: Only recalculates when dependencies change
function ProductList({ products, category }) {
  const filteredProducts = useMemo(() => {
    console.log('Filtering and sorting...');
    return products
      .filter(p => p.category === category)
      .sort((a, b) => b.rating - a.rating);
  }, [products, category]);

  return (
    <div>
      {filteredProducts.map(product => (
        <ProductCard key={product.id} product={product} />
      ))}
    </div>
  );
}
```

### 3. Context Causing Unnecessary Re-renders

#### Problem: All Consumers Re-render on Any Context Change
```javascript
// ❌ BAD: Single context with multiple values
const AppContext = createContext();

function AppProvider({ children }) {
  const [user, setUser] = useState(null);
  const [theme, setTheme] = useState('light');
  const [notifications, setNotifications] = useState([]);

  const value = {
    user,
    setUser,
    theme,
    setTheme,
    notifications,
    setNotifications,
  };

  return <AppContext.Provider value={value}>{children}</AppContext.Provider>;
}

// Component that only needs theme
function ThemeToggle() {
  const { theme, setTheme } = useContext(AppContext);
  // Issue: Re-renders when user or notifications change
  return <button onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}>Toggle</button>;
}
```

#### Solution: Split Context or Use Selectors
```javascript
// ✅ GOOD: Separate contexts for different concerns
const UserContext = createContext();
const ThemeContext = createContext();
const NotificationContext = createContext();

function AppProvider({ children }) {
  const [user, setUser] = useState(null);
  const [theme, setTheme] = useState('light');
  const [notifications, setNotifications] = useState([]);

  const userValue = useMemo(() => ({ user, setUser }), [user]);
  const themeValue = useMemo(() => ({ theme, setTheme }), [theme]);
  const notificationValue = useMemo(() => ({ notifications, setNotifications }), [notifications]);

  return (
    <UserContext.Provider value={userValue}>
      <ThemeContext.Provider value={themeValue}>
        <NotificationContext.Provider value={notificationValue}>
          {children}
        </NotificationContext.Provider>
      </ThemeContext.Provider>
    </UserContext.Provider>
  );
}

// Component only subscribes to theme changes
function ThemeToggle() {
  const { theme, setTheme } = useContext(ThemeContext);
  // Now: Only re-renders when theme changes
  return <button onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}>Toggle</button>;
}
```

### 4. Creating New Objects/Arrays in Render

#### Problem: New Reference on Every Render
```javascript
// ❌ BAD: New style object on every render
function Button({ label }) {
  return (
    <button style={{ padding: 10, margin: 5 }}>
      {label}
    </button>
  );
}

// ❌ BAD: New array on every render
function UserProfile({ userId }) {
  return (
    <UserCard userId={userId} fields={['name', 'email', 'avatar']} />
  );
}
```

#### Solution: Move Constants Outside or Memoize
```javascript
// ✅ GOOD: Constant outside component
const BUTTON_STYLE = { padding: 10, margin: 5 };
const USER_FIELDS = ['name', 'email', 'avatar'];

function Button({ label }) {
  return <button style={BUTTON_STYLE}>{label}</button>;
}

function UserProfile({ userId }) {
  return <UserCard userId={userId} fields={USER_FIELDS} />;
}

// ✅ ALTERNATIVE: Memoize if dynamic
function Button({ label, isPrimary }) {
  const style = useMemo(() => ({
    padding: 10,
    margin: 5,
    backgroundColor: isPrimary ? 'blue' : 'gray',
  }), [isPrimary]);

  return <button style={style}>{label}</button>;
}
```

### 5. Large Lists Without Virtualization

#### Problem: Rendering Thousands of Items
```javascript
// ❌ BAD: Rendering 10,000 items at once
function LargeList({ items }) {
  return (
    <div>
      {items.map(item => (
        <ListItem key={item.id} item={item} />
      ))}
    </div>
  );
}
// Issue: Slow initial render, high memory usage
```

#### Solution: Use Virtual Scrolling
```javascript
// ✅ GOOD: Only render visible items
import { FixedSizeList } from 'react-window';

function LargeList({ items }) {
  const Row = ({ index, style }) => (
    <div style={style}>
      <ListItem item={items[index]} />
    </div>
  );

  return (
    <FixedSizeList
      height={600}
      itemCount={items.length}
      itemSize={50}
      width="100%"
    >
      {Row}
    </FixedSizeList>
  );
}
// Now: Only renders visible items (60-100x faster for large lists)
```

### 6. Inline Function Definitions

#### Problem: New Function on Every Render
```javascript
// ❌ BAD: New function on every render
function TodoList({ todos }) {
  return (
    <>
      {todos.map(todo => (
        <TodoItem
          key={todo.id}
          todo={todo}
          onToggle={() => handleToggle(todo.id)}
          onDelete={() => handleDelete(todo.id)}
        />
      ))}
    </>
  );
}
```

#### Solution: Use useCallback or Optimize Handler
```javascript
// ✅ GOOD: Memoized callbacks
function TodoList({ todos }) {
  const handleToggle = useCallback((id) => {
    // Toggle logic
  }, []);

  const handleDelete = useCallback((id) => {
    // Delete logic
  }, []);

  return (
    <>
      {todos.map(todo => (
        <TodoItem
          key={todo.id}
          todo={todo}
          onToggle={handleToggle}
          onDelete={handleDelete}
        />
      ))}
    </>
  );
}

// TodoItem handles ID internally
const TodoItem = React.memo(({ todo, onToggle, onDelete }) => {
  return (
    <div>
      <input
        type="checkbox"
        checked={todo.completed}
        onChange={() => onToggle(todo.id)}
      />
      <span>{todo.text}</span>
      <button onClick={() => onDelete(todo.id)}>Delete</button>
    </div>
  );
});
```

### 7. State Updates Triggering Full Tree Re-renders

#### Problem: Top-Level State Change
```javascript
// ❌ BAD: Search input at top causes everything to re-render
function App() {
  const [searchTerm, setSearchTerm] = useState('');
  const [products, setProducts] = useState([]);

  return (
    <div>
      <input
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
      />
      <ExpensiveChart data={products} />
      <ExpensiveTable data={products} />
      <ExpensiveVisualization data={products} />
    </div>
  );
}
// Issue: Every keystroke re-renders all expensive components
```

#### Solution: Use useTransition or Split Components
```javascript
// ✅ GOOD: Use useTransition for non-urgent updates
import { useState, useTransition } from 'react';

function App() {
  const [searchTerm, setSearchTerm] = useState('');
  const [displayTerm, setDisplayTerm] = useState('');
  const [isPending, startTransition] = useTransition();
  const [products, setProducts] = useState([]);

  const handleSearch = (value) => {
    setSearchTerm(value); // Urgent: Update input immediately

    startTransition(() => {
      setDisplayTerm(value); // Non-urgent: Update results
    });
  };

  const filteredProducts = useMemo(() => {
    return products.filter(p =>
      p.name.toLowerCase().includes(displayTerm.toLowerCase())
    );
  }, [products, displayTerm]);

  return (
    <div>
      <input value={searchTerm} onChange={(e) => handleSearch(e.target.value)} />
      {isPending && <Spinner />}
      <ExpensiveChart data={filteredProducts} />
      <ExpensiveTable data={filteredProducts} />
    </div>
  );
}

// ✅ ALTERNATIVE: Split components
function App() {
  const [products, setProducts] = useState([]);

  return (
    <div>
      <SearchInput /> {/* Isolated state */}
      <ExpensiveChart data={products} />
      <ExpensiveTable data={products} />
    </div>
  );
}
```

## Performance Optimization Patterns

### Pattern 1: Component Memoization Strategy
```javascript
// Memoize leaf components that receive complex props
const UserAvatar = React.memo(({ user }) => (
  <img src={user.avatar} alt={user.name} />
));

// Memoize with custom comparison
const UserCard = React.memo(
  ({ user, onSelect }) => (
    <div onClick={() => onSelect(user.id)}>
      <UserAvatar user={user} />
      <h3>{user.name}</h3>
    </div>
  ),
  (prevProps, nextProps) => {
    // Only re-render if user ID changed
    return prevProps.user.id === nextProps.user.id;
  }
);
```

### Pattern 2: Derived State Optimization
```javascript
// ❌ BAD: Storing derived state
function ProductList({ products }) {
  const [sortedProducts, setSortedProducts] = useState([]);

  useEffect(() => {
    setSortedProducts([...products].sort((a, b) => a.price - b.price));
  }, [products]);

  return <div>{sortedProducts.map(...)}</div>;
}

// ✅ GOOD: Compute derived state
function ProductList({ products }) {
  const sortedProducts = useMemo(() => {
    return [...products].sort((a, b) => a.price - b.price);
  }, [products]);

  return <div>{sortedProducts.map(...)}</div>;
}
```

### Pattern 3: Event Handler Optimization
```javascript
// ✅ GOOD: Stable event handlers
function Form() {
  const [formData, setFormData] = useState({});

  // Single handler for all fields
  const handleChange = useCallback((e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  }, []);

  return (
    <form>
      <input name="email" onChange={handleChange} />
      <input name="password" onChange={handleChange} />
      <input name="name" onChange={handleChange} />
    </form>
  );
}
```

### Pattern 4: Lazy Initialization
```javascript
// ❌ BAD: Expensive initialization on every render
function Component() {
  const [data] = useState(expensiveComputation());
}

// ✅ GOOD: Lazy initialization (only runs once)
function Component() {
  const [data] = useState(() => expensiveComputation());
}
```

### Pattern 5: Debouncing Expensive Operations
```javascript
import { useState, useMemo } from 'react';
import debounce from 'lodash.debounce';

function SearchComponent() {
  const [searchTerm, setSearchTerm] = useState('');

  // Debounce search API call
  const debouncedSearch = useMemo(
    () => debounce((term) => {
      // API call
      fetch(`/api/search?q=${term}`);
    }, 300),
    []
  );

  const handleChange = (e) => {
    const value = e.target.value;
    setSearchTerm(value);
    debouncedSearch(value);
  };

  return <input value={searchTerm} onChange={handleChange} />;
}
```

## Performance Profiling

### Using React DevTools Profiler
```javascript
import { Profiler } from 'react';

function onRenderCallback(
  id, // Component ID
  phase, // "mount" or "update"
  actualDuration, // Time spent rendering
  baseDuration, // Estimated time without memoization
  startTime, // When render started
  commitTime // When committed
) {
  console.log(`${id} (${phase}) took ${actualDuration}ms`);
}

function App() {
  return (
    <Profiler id="App" onRender={onRenderCallback}>
      <Dashboard />
    </Profiler>
  );
}
```

### Performance Markers
```javascript
import { useEffect } from 'react';

function Component() {
  useEffect(() => {
    performance.mark('component-mount-start');

    return () => {
      performance.mark('component-mount-end');
      performance.measure(
        'component-mount',
        'component-mount-start',
        'component-mount-end'
      );

      const measure = performance.getEntriesByName('component-mount')[0];
      console.log(`Component took ${measure.duration}ms to mount`);
    };
  }, []);

  return <div>Content</div>;
}
```

## Checklist for React Performance

When writing React components:

- [ ] Use React.memo for components with complex props
- [ ] Use useCallback for event handlers passed as props
- [ ] Use useMemo for expensive calculations
- [ ] Avoid creating new objects/arrays in render
- [ ] Split context into smaller, focused contexts
- [ ] Use virtual scrolling for large lists (>100 items)
- [ ] Lazy load routes and heavy components
- [ ] Use useTransition for non-urgent updates
- [ ] Avoid inline function definitions in JSX
- [ ] Profile with React DevTools to identify bottlenecks

## When NOT to Optimize

Don't optimize prematurely:
- Small lists (<50 items): No need for virtualization
- Simple calculations: useMemo overhead may be worse
- Leaf components without children: React.memo overhead not worth it
- Static props: No need for memoization

**Always measure first**: Use React DevTools Profiler to identify actual bottlenecks before optimizing.

## Red Flags

1. **Many re-renders**: Component re-renders more than expected
2. **Slow interactions**: Clicks/inputs feel sluggish
3. **High render time**: React DevTools shows long render times
4. **Memory leaks**: Component state growing over time
5. **Scrolling jank**: Scroll performance degraded
6. **High CPU usage**: Browser consuming excessive CPU

## Testing Performance

```javascript
describe('ProductList performance', () => {
  it('should not re-render unnecessarily', () => {
    const { rerender } = render(<ProductList products={products} />);

    const renderCount = getRenderCount('ProductList');

    // Change unrelated prop
    rerender(<ProductList products={products} otherProp="changed" />);

    // Should not have re-rendered
    expect(getRenderCount('ProductList')).toBe(renderCount);
  });
});
```

By following these optimization patterns, you can ensure your React components render efficiently and provide a smooth user experience.
