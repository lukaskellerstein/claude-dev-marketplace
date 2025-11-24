---
name: performance-optimizer
description: Auto-invoked when working with React components to identify and prevent performance issues
allowed-tools: Read, Grep, Glob
---

# Performance Optimizer

This skill provides real-time guidance on React performance optimization, helping prevent common performance pitfalls and unnecessary re-renders.

## When Active

This skill activates when you:
- Create or modify React components
- Implement state management
- Work with lists or large datasets
- Add effects or side effects
- Integrate third-party libraries
- Build forms or complex interactions

## React Performance Principles

### 1. Prevent Unnecessary Re-renders

#### React.memo for Component Memoization
```tsx
import { memo } from 'react';

// ❌ Re-renders whenever parent re-renders
export function ExpensiveComponent({ data }) {
  return <div>{/* Complex rendering logic */}</div>;
}

// ✅ Only re-renders when props change
export const ExpensiveComponent = memo(({ data }) => {
  return <div>{/* Complex rendering logic */}</div>;
});

// ✅ With custom comparison
export const ExpensiveComponent = memo(
  ({ data }) => {
    return <div>{/* Complex rendering logic */}</div>;
  },
  (prevProps, nextProps) => {
    // Return true if props are equal (skip re-render)
    return prevProps.data.id === nextProps.data.id;
  }
);
```

#### useMemo for Expensive Computations
```tsx
import { useMemo } from 'react';

function DataTable({ data, filters }) {
  // ❌ Recalculates on every render
  const filteredData = data.filter(item =>
    item.name.includes(filters.search)
  ).sort((a, b) => a.name.localeCompare(b.name));

  // ✅ Only recalculates when dependencies change
  const filteredData = useMemo(() => {
    return data
      .filter(item => item.name.includes(filters.search))
      .sort((a, b) => a.name.localeCompare(b.name));
  }, [data, filters.search]);

  return <div>{/* Render filtered data */}</div>;
}
```

#### useCallback for Function Stability
```tsx
import { useCallback } from 'react';

function ParentComponent() {
  // ❌ Creates new function on every render
  const handleClick = (id: string) => {
    console.log('Clicked', id);
  };

  // ✅ Stable function reference
  const handleClick = useCallback((id: string) => {
    console.log('Clicked', id);
  }, []);

  return <ChildComponent onClick={handleClick} />;
}

// ChildComponent is memoized, so stable onClick prevents re-renders
const ChildComponent = memo(({ onClick }) => {
  return <button onClick={() => onClick('123')}>Click</button>;
});
```

### 2. Optimize State Management

#### Minimize State Updates
```tsx
// ❌ Multiple state updates cause multiple re-renders
function Form() {
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [email, setEmail] = useState('');

  // Each keystroke triggers 3 re-renders
}

// ✅ Single state object, single update
function Form() {
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    email: '',
  });

  const updateField = (field: string, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };
}
```

#### Lazy State Initialization
```tsx
// ❌ Runs expensive computation on every render
function Component() {
  const [data, setData] = useState(expensiveComputation());
}

// ✅ Only runs once on initial render
function Component() {
  const [data, setData] = useState(() => expensiveComputation());
}
```

#### Functional Updates
```tsx
// ❌ May use stale state
function Counter() {
  const [count, setCount] = useState(0);

  const increment = () => {
    setCount(count + 1);
    setCount(count + 1); // Still uses original count value
  };
}

// ✅ Always uses latest state
function Counter() {
  const [count, setCount] = useState(0);

  const increment = () => {
    setCount(prev => prev + 1);
    setCount(prev => prev + 1); // Correctly increments twice
  };
}
```

### 3. Code Splitting and Lazy Loading

#### Route-based Code Splitting
```tsx
import { lazy, Suspense } from 'react';
import { Routes, Route } from 'react-router-dom';

// ❌ Loads all routes upfront
import Home from './pages/Home';
import Dashboard from './pages/Dashboard';
import Settings from './pages/Settings';

// ✅ Loads routes on demand
const Home = lazy(() => import('./pages/Home'));
const Dashboard = lazy(() => import('./pages/Dashboard'));
const Settings = lazy(() => import('./pages/Settings'));

function App() {
  return (
    <Suspense fallback={<LoadingSpinner />}>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/settings" element={<Settings />} />
      </Routes>
    </Suspense>
  );
}
```

#### Component-based Lazy Loading
```tsx
import { lazy, Suspense } from 'react';

// ✅ Lazy load below-the-fold content
const HeavyChart = lazy(() => import('./HeavyChart'));
const Comments = lazy(() => import('./Comments'));

function ArticlePage() {
  return (
    <article>
      <h1>Article Title</h1>
      <p>Article content...</p>

      <Suspense fallback={<div>Loading chart...</div>}>
        <HeavyChart />
      </Suspense>

      <Suspense fallback={<div>Loading comments...</div>}>
        <Comments />
      </Suspense>
    </article>
  );
}
```

### 4. Virtual Scrolling for Large Lists

```tsx
import { useVirtualizer } from '@tanstack/react-virtual';
import { useRef } from 'react';

// ❌ Renders all 10,000 items (slow!)
function LargeList({ items }) {
  return (
    <div>
      {items.map(item => (
        <div key={item.id}>{item.name}</div>
      ))}
    </div>
  );
}

// ✅ Only renders visible items
function VirtualizedList({ items }) {
  const parentRef = useRef<HTMLDivElement>(null);

  const virtualizer = useVirtualizer({
    count: items.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 50, // Estimated row height
    overscan: 5, // Render extra items for smooth scrolling
  });

  return (
    <div ref={parentRef} className="h-[600px] overflow-auto">
      <div
        style={{
          height: `${virtualizer.getTotalSize()}px`,
          position: 'relative',
        }}
      >
        {virtualizer.getVirtualItems().map(virtualRow => (
          <div
            key={virtualRow.index}
            style={{
              position: 'absolute',
              top: 0,
              left: 0,
              width: '100%',
              transform: `translateY(${virtualRow.start}px)`,
            }}
          >
            {items[virtualRow.index].name}
          </div>
        ))}
      </div>
    </div>
  );
}
```

### 5. Optimize useEffect

#### Cleanup Functions
```tsx
// ✅ Always cleanup to prevent memory leaks
function Component() {
  useEffect(() => {
    const subscription = api.subscribe(data => {
      // Handle data
    });

    // Cleanup on unmount
    return () => {
      subscription.unsubscribe();
    };
  }, []);
}

// ✅ Cancel pending requests
function DataFetcher({ userId }) {
  useEffect(() => {
    let cancelled = false;

    async function fetchData() {
      const data = await api.fetchUser(userId);
      if (!cancelled) {
        setUser(data);
      }
    }

    fetchData();

    return () => {
      cancelled = true;
    };
  }, [userId]);
}
```

#### Minimal Dependencies
```tsx
// ❌ Unnecessary dependencies
function Component({ onUpdate, config }) {
  useEffect(() => {
    if (config.enabled) {
      onUpdate();
    }
  }, [onUpdate, config]); // Re-runs when entire config changes
}

// ✅ Specific dependencies
function Component({ onUpdate, config }) {
  const enabled = config.enabled;

  useEffect(() => {
    if (enabled) {
      onUpdate();
    }
  }, [onUpdate, enabled]); // Only re-runs when enabled changes
}
```

### 6. Debouncing and Throttling

```tsx
import { useState, useCallback } from 'react';
import { debounce } from 'lodash';

// ✅ Debounce search input
function SearchInput() {
  const [query, setQuery] = useState('');

  const debouncedSearch = useCallback(
    debounce((searchTerm: string) => {
      // API call
      api.search(searchTerm);
    }, 300),
    []
  );

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setQuery(value);
    debouncedSearch(value);
  };

  return <input value={query} onChange={handleChange} />;
}

// ✅ Throttle scroll handler
import { throttle } from 'lodash';

function ScrollTracker() {
  const handleScroll = useCallback(
    throttle(() => {
      const scrollPosition = window.scrollY;
      // Update scroll position
    }, 100),
    []
  );

  useEffect(() => {
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, [handleScroll]);
}
```

### 7. Image Optimization

```tsx
// ✅ Next.js Image component (automatic optimization)
import Image from 'next/image';

<Image
  src="/hero.jpg"
  alt="Hero image"
  width={1200}
  height={600}
  loading="lazy" // or "eager" for above-the-fold
  placeholder="blur"
  blurDataURL="data:image/..." // Low-quality placeholder
  sizes="(max-width: 768px) 100vw, 50vw"
/>

// ✅ Standard lazy loading
<img
  src="/image.jpg"
  alt="Description"
  loading="lazy"
  decoding="async"
/>

// ✅ Responsive images with srcset
<img
  srcset="
    image-400.jpg 400w,
    image-800.jpg 800w,
    image-1200.jpg 1200w
  "
  sizes="(max-width: 768px) 100vw, 50vw"
  src="image-800.jpg"
  alt="Description"
  loading="lazy"
/>
```

### 8. Bundle Size Optimization

```tsx
// ❌ Import entire library
import _ from 'lodash';
const result = _.debounce(fn, 300);

// ✅ Import only what you need
import debounce from 'lodash/debounce';
const result = debounce(fn, 300);

// ❌ Import entire icon library
import { IconName } from 'react-icons/fa';

// ✅ Import specific icon
import { FaBeer } from 'react-icons/fa';

// ✅ Use tree-shakeable libraries
import { format } from 'date-fns'; // Instead of moment.js
```

### 9. React DevTools Profiler

```tsx
import { Profiler } from 'react';

function onRenderCallback(
  id: string,
  phase: 'mount' | 'update',
  actualDuration: number,
  baseDuration: number,
  startTime: number,
  commitTime: number
) {
  console.log(`${id}'s ${phase} phase:`);
  console.log(`Actual time: ${actualDuration}ms`);
  console.log(`Base time: ${baseDuration}ms`);
}

function App() {
  return (
    <Profiler id="App" onRender={onRenderCallback}>
      <YourComponents />
    </Profiler>
  );
}
```

## Performance Metrics

### Core Web Vitals
- **LCP (Largest Contentful Paint)**: < 2.5s (good)
- **FID (First Input Delay)**: < 100ms (good)
- **CLS (Cumulative Layout Shift)**: < 0.1 (good)

### React-Specific Metrics
- **Initial Render Time**: Time to first meaningful paint
- **Re-render Count**: Number of unnecessary re-renders
- **Bundle Size**: Total JavaScript size
- **Time to Interactive**: When page becomes fully interactive

## Performance Checklist

When writing React components:
- [ ] Use React.memo for expensive components
- [ ] Memoize expensive computations with useMemo
- [ ] Stabilize callbacks with useCallback
- [ ] Implement code splitting for routes
- [ ] Lazy load below-the-fold content
- [ ] Use virtual scrolling for long lists (100+ items)
- [ ] Clean up effects to prevent memory leaks
- [ ] Debounce/throttle frequent event handlers
- [ ] Optimize images (lazy loading, srcset, WebP)
- [ ] Minimize bundle size (tree-shaking, code splitting)
- [ ] Use production build for deployment
- [ ] Profile with React DevTools
- [ ] Monitor with Lighthouse or Web Vitals

## Common Performance Anti-Patterns

### 1. Creating Objects/Arrays in Render
```tsx
// ❌ Creates new array on every render
function Component() {
  return <ChildComponent items={[1, 2, 3]} />;
}

// ✅ Stable reference
const ITEMS = [1, 2, 3];
function Component() {
  return <ChildComponent items={ITEMS} />;
}
```

### 2. Inline Function Props
```tsx
// ❌ New function on every render
function Parent() {
  return <Child onClick={() => console.log('clicked')} />;
}

// ✅ Stable callback
function Parent() {
  const handleClick = useCallback(() => {
    console.log('clicked');
  }, []);

  return <Child onClick={handleClick} />;
}
```

### 3. Not Splitting Context
```tsx
// ❌ All consumers re-render on any state change
const AppContext = createContext({
  user: null,
  theme: 'light',
  notifications: [],
});

// ✅ Split into specific contexts
const UserContext = createContext(null);
const ThemeContext = createContext('light');
const NotificationsContext = createContext([]);
```

## Tools and Resources

- **React DevTools Profiler**: Identify performance bottlenecks
- **Lighthouse**: Audit performance, accessibility, SEO
- **Web Vitals**: Measure Core Web Vitals
- **Bundle Analyzer**: webpack-bundle-analyzer, @next/bundle-analyzer
- **why-did-you-render**: Debug unnecessary re-renders
- **Chrome Performance Tab**: Detailed performance profiling

Use this guidance to build fast, responsive React applications that provide excellent user experience across all devices.
