---
name: performance-monitor
description: Master React performance optimization for faster, more efficient applications. Use when detecting performance bottlenecks, optimizing re-renders, reducing bundle size, or improving Core Web Vitals in React applications.
allowed-tools: Read, Grep
---

# Performance Monitor Skill

Automatically detect performance issues and suggest optimizations during development.

## When to Use This Skill

This skill automatically activates and provides assistance in these specific scenarios:

1. **Large Component Detection** - When components exceed 200 lines of code
2. **Multiple State Variables** - When components have more than 5 useState calls
3. **Effect Overload** - When components have more than 3 useEffect hooks
4. **Large Dependency Arrays** - When useEffect has more than 5 dependencies
5. **Inline Functions in JSX** - Detecting performance-killing inline handlers
6. **Missing Memoization** - Complex components without React.memo
7. **Heavy Library Imports** - Detecting large libraries like lodash, moment, or icon packs
8. **Large List Rendering** - Arrays with 100+ items without virtualization
9. **Missing Keys in Lists** - List items without proper key props
10. **Unoptimized Images** - Images without lazy loading or responsive formats
11. **State Management Issues** - Unnecessary state lifting or monolithic state objects
12. **Bundle Size Concerns** - When imports exceed recommended size budgets
13. **Memory Leaks** - Detecting unmounted component state updates
14. **Animation Performance** - Non-compositor animations causing jank
15. **Web Vitals Violations** - When Core Web Vitals metrics are degraded

## Quick Start

### Step 1: Automatic Detection
The skill automatically monitors your code as you write. No manual activation needed.

### Step 2: Review Suggestions
When performance issues are detected, you'll receive:
- Clear issue identification with line numbers
- Performance impact assessment
- Specific code examples for fixes
- Expected improvement metrics

### Step 3: Apply Optimizations
Follow the provided code examples to implement optimizations. The skill tracks:
- Re-render counts
- Bundle size impacts
- Web Vitals improvements

## Auto-invocation Triggers

### Pattern Detection
- Large components (>200 lines)
- Multiple useState calls (>5 in one component)
- Multiple useEffect calls (>3 in one component)
- Large dependency arrays (>5 dependencies)
- Inline function definitions in JSX
- Missing React.memo on complex components

### Import Analysis
```typescript
// Heavy library detection
import _ from 'lodash'; // 70KB
import moment from 'moment'; // 67KB
import * as Icons from '@mui/icons-material'; // 2MB+

// Triggers optimization suggestions
```

### Array Operations
```tsx
// Missing key prop
items.map(item => <Item />)

// Large list without virtualization
data.slice(0, 10000).map(item => <Row key={item.id} />)
```

## React Performance Issues

### Unnecessary Re-renders
```tsx
// ❌ Component re-renders on every parent update
function ExpensiveList({ items, onItemClick }) {
  const processedItems = items.map(complexProcessing);
  return (
    <ul>
      {processedItems.map(item => (
        <li key={item.id} onClick={() => onItemClick(item.id)}>
          {item.name}
        </li>
      ))}
    </ul>
  );
}

// ✅ Optimized with memo and useCallback
const ExpensiveList = memo(({ items, onItemClick }) => {
  const processedItems = useMemo(
    () => items.map(complexProcessing),
    [items]
  );

  return (
    <ul>
      {processedItems.map(item => (
        <ListItem
          key={item.id}
          item={item}
          onClick={onItemClick}
        />
      ))}
    </ul>
  );
});

const ListItem = memo(({ item, onClick }) => {
  const handleClick = useCallback(
    () => onClick(item.id),
    [onClick, item.id]
  );

  return <li onClick={handleClick}>{item.name}</li>;
});
```

### Hook Optimization
```tsx
// ❌ Expensive computation on every render
function Component({ data }) {
  const result = expensiveCalculation(data);
  // ...
}

// ✅ Memoized computation
function Component({ data }) {
  const result = useMemo(
    () => expensiveCalculation(data),
    [data]
  );
  // ...
}
```

### Effect Dependencies
```tsx
// ❌ Effect runs on every render
useEffect(() => {
  fetchData(id);
}); // Missing dependencies

// ❌ Recreated function causes effect to run
useEffect(() => {
  fetchData(id);
}, [fetchData, id]); // fetchData changes every render

// ✅ Stable dependencies
const fetchData = useCallback((id) => {
  // fetch logic
}, []);

useEffect(() => {
  fetchData(id);
}, [fetchData, id]);
```

## Bundle Size Optimization

### Code Splitting
```tsx
// ❌ Loading everything upfront
import Dashboard from './Dashboard';
import Analytics from './Analytics';
import Reports from './Reports';

// ✅ Lazy loading with React 18 Suspense
const Dashboard = lazy(() => import('./Dashboard'));
const Analytics = lazy(() => import('./Analytics'));
const Reports = lazy(() => import('./Reports'));

// Usage with Suspense
<Suspense fallback={<Loading />}>
  <Routes>
    <Route path="/dashboard" element={<Dashboard />} />
    <Route path="/analytics" element={<Analytics />} />
    <Route path="/reports" element={<Reports />} />
  </Routes>
</Suspense>
```

### Tree Shaking
```tsx
// ❌ Importing entire library
import _ from 'lodash';
const debounced = _.debounce(fn, 300);

// ✅ Import specific functions
import debounce from 'lodash/debounce';
const debounced = debounce(fn, 300);

// ❌ Importing all icons
import * as Icons from '@mui/icons-material';
<Icons.Add />

// ✅ Import specific icons
import AddIcon from '@mui/icons-material/Add';
<AddIcon />
```

### Dynamic Imports
```tsx
// Conditional feature loading
async function loadAdvancedFeatures() {
  if (user.hasProPlan) {
    const { AdvancedCharts } = await import('./AdvancedCharts');
    return AdvancedCharts;
  }
  return null;
}

// Route-based code splitting
const routes = [
  {
    path: '/admin',
    component: lazy(() => import('./pages/Admin')),
  },
  {
    path: '/dashboard',
    component: lazy(() => import('./pages/Dashboard')),
  },
];
```

## List Virtualization

### Large List Detection
```tsx
// ❌ Rendering 1000+ items
<ul>
  {largeArray.map(item => (
    <li key={item.id}>{item.name}</li>
  ))}
</ul>

// ✅ Virtual scrolling with react-window
import { FixedSizeList } from 'react-window';

<FixedSizeList
  height={600}
  itemCount={largeArray.length}
  itemSize={50}
  width="100%"
>
  {({ index, style }) => (
    <div style={style}>
      {largeArray[index].name}
    </div>
  )}
</FixedSizeList>

// ✅ Variable size list
import { VariableSizeList } from 'react-window';

<VariableSizeList
  height={600}
  itemCount={items.length}
  itemSize={(index) => items[index].height}
  width="100%"
>
  {({ index, style }) => (
    <div style={style}>{items[index].content}</div>
  )}
</VariableSizeList>
```

## Image Optimization

### Lazy Loading
```tsx
// ❌ Loading all images immediately
<img src={imageUrl} alt="Product" />

// ✅ Native lazy loading
<img
  src={imageUrl}
  alt="Product"
  loading="lazy"
  decoding="async"
/>

// ✅ Progressive image loading with placeholder
const [imageSrc, setImageSrc] = useState(placeholder);

useEffect(() => {
  const img = new Image();
  img.src = highResUrl;
  img.onload = () => setImageSrc(highResUrl);
}, [highResUrl]);

<img src={imageSrc} alt="Product" />
```

### Responsive Images
```tsx
<picture>
  <source
    media="(max-width: 768px)"
    srcSet="image-mobile.webp"
    type="image/webp"
  />
  <source
    media="(max-width: 768px)"
    srcSet="image-mobile.jpg"
  />
  <source
    srcSet="image-desktop.webp"
    type="image/webp"
  />
  <img
    src="image-desktop.jpg"
    alt="Description"
    loading="lazy"
  />
</picture>
```

## State Management

### State Colocation
```tsx
// ❌ Lifting state unnecessarily
function App() {
  const [searchTerm, setSearchTerm] = useState('');
  return <SearchBar value={searchTerm} onChange={setSearchTerm} />;
}

// ✅ Keep state local when possible
function SearchBar() {
  const [searchTerm, setSearchTerm] = useState('');
  // Use searchTerm locally
}
```

### State Splitting
```tsx
// ❌ Single state object causing full re-renders
const [state, setState] = useState({
  user: {},
  posts: [],
  comments: [],
  ui: {}
});

// ✅ Split independent state
const [user, setUser] = useState({});
const [posts, setPosts] = useState([]);
const [comments, setComments] = useState([]);
const [ui, setUI] = useState({});
```

## Performance Metrics

### Component Metrics
```typescript
// Detect and report:
interface ComponentMetrics {
  lineCount: number;        // >200 lines = warning
  stateCount: number;       // >5 states = warning
  effectCount: number;      // >3 effects = warning
  propCount: number;        // >10 props = warning
  depthLevel: number;       // >5 nesting = warning
  rerenderCount: number;    // Track re-renders
}
```

### Bundle Analysis
```typescript
// Analyze imports
interface ImportMetrics {
  totalSize: number;        // Total import size
  largestImport: string;    // Biggest dependency
  unusedImports: string[];  // Detected unused
  duplicates: string[];     // Duplicate packages
}
```

## Real-World Applications

### Example 1: Dashboard Performance Optimization
```tsx
// Before: Slow dashboard with 30+ widgets
function Dashboard() {
  const [data, setData] = useState({});
  const widgets = generateWidgets(data); // Heavy computation

  return (
    <div>
      {widgets.map(w => <Widget key={w.id} {...w} />)}
    </div>
  );
}

// After: Optimized with React 18 concurrent features
function Dashboard() {
  const [data, setData] = useState({});

  // Split data fetching
  const { widgets } = useDeferredValue(data);

  // Memoize expensive computation
  const processedWidgets = useMemo(
    () => generateWidgets(widgets),
    [widgets]
  );

  return (
    <Suspense fallback={<DashboardSkeleton />}>
      <div>
        {processedWidgets.map(w => (
          <Widget key={w.id} {...w} />
        ))}
      </div>
    </Suspense>
  );
}

const Widget = memo(({ id, data, onUpdate }) => {
  const handleUpdate = useCallback(
    (newData) => onUpdate(id, newData),
    [id, onUpdate]
  );

  return <div onClick={handleUpdate}>{data.title}</div>;
});
```

### Example 2: E-commerce Product List
```tsx
// Before: Rendering 1000+ products
function ProductList({ products }) {
  return (
    <div className="grid">
      {products.map(p => (
        <ProductCard key={p.id} product={p} />
      ))}
    </div>
  );
}

// After: Virtualized with intersection observer
import { FixedSizeGrid } from 'react-window';

function ProductList({ products }) {
  const columnCount = useBreakpointValue({ base: 1, md: 2, lg: 3 });
  const rowCount = Math.ceil(products.length / columnCount);

  return (
    <FixedSizeGrid
      columnCount={columnCount}
      columnWidth={300}
      height={800}
      rowCount={rowCount}
      rowHeight={400}
      width={1200}
    >
      {({ columnIndex, rowIndex, style }) => {
        const index = rowIndex * columnCount + columnIndex;
        const product = products[index];

        if (!product) return null;

        return (
          <div style={style}>
            <ProductCard product={product} />
          </div>
        );
      }}
    </FixedSizeGrid>
  );
}
```

## Optimization Suggestions

### Immediate Actions
```markdown
🚀 Performance Optimization Detected

**Issue**: Component re-renders 8 times on data update
**Location**: Dashboard.tsx:45
**Impact**: High - Causes layout thrashing

**Solution**:
1. Add React.memo to component
2. Use useMemo for expensive calculations
3. Extract child components

**Code**:
```tsx
export const Dashboard = memo(() => {
  // Component code
});
```

**Expected Improvement**: 70% reduction in re-renders
```

### Performance Budget
```javascript
// performance.config.js
module.exports = {
  bundles: {
    main: { maxSize: '200kb' },
    vendor: { maxSize: '150kb' },
  },
  metrics: {
    fcp: { max: 1500 },  // First Contentful Paint
    lcp: { max: 2500 },  // Largest Contentful Paint
    fid: { max: 100 },   // First Input Delay
    cls: { max: 0.1 },   // Cumulative Layout Shift
  },
  components: {
    maxLines: 200,
    maxProps: 10,
    maxStateVars: 5,
  }
};
```

## Best Practices

### 1. Memoization Strategy
- Use `React.memo` for components that render often with same props
- Use `useMemo` for expensive calculations
- Use `useCallback` for functions passed to child components
- Don't over-optimize - profile first!

### 2. Code Splitting
- Split routes with `React.lazy`
- Use dynamic imports for heavy features
- Implement proper loading states with `Suspense`
- Prefetch critical routes on idle

### 3. Bundle Optimization
- Analyze bundle with webpack-bundle-analyzer
- Tree-shake unused code
- Use modern formats (ES modules)
- Implement proper caching strategies

### 4. Image Strategy
- Use modern formats (WebP, AVIF)
- Implement responsive images
- Lazy load below-the-fold images
- Use CDN for image optimization

### 5. State Management
- Keep state as local as possible
- Split unrelated state
- Use reducers for complex state
- Consider Zustand or Jotai for global state

## Common Pitfalls

### 1. Premature Optimization
```tsx
// ❌ Memoizing everything unnecessarily
const name = useMemo(() => props.firstName + ' ' + props.lastName, [props.firstName, props.lastName]);

// ✅ Simple operations don't need memoization
const name = props.firstName + ' ' + props.lastName;
```

### 2. Broken Dependencies
```tsx
// ❌ Missing dependency causing stale closure
useEffect(() => {
  const timer = setInterval(() => {
    setCount(count + 1); // count is stale
  }, 1000);
  return () => clearInterval(timer);
}, []); // count missing from deps

// ✅ Use functional update
useEffect(() => {
  const timer = setInterval(() => {
    setCount(c => c + 1); // Always fresh
  }, 1000);
  return () => clearInterval(timer);
}, []);
```

### 3. Inline Object/Array Props
```tsx
// ❌ New object on every render
<Component config={{ theme: 'dark' }} />

// ✅ Stable reference
const config = useMemo(() => ({ theme: 'dark' }), []);
<Component config={config} />
```

### 4. Over-nesting Components
```tsx
// ❌ Deep component tree
<A><B><C><D><E><Component /></E></D></C></B></A>

// ✅ Flatten when possible
<Component />
```

### 5. Ignoring Web Vitals
- Monitor LCP, FID, CLS regularly
- Test on real devices, not just localhost
- Use Chrome DevTools Performance tab
- Implement RUM (Real User Monitoring)

## Monitoring Integration

### React DevTools Profiler
- Identify components causing re-renders
- Measure render duration
- Find performance bottlenecks
- Track component lifecycle

### Web Vitals
```typescript
import { getCLS, getFID, getFCP, getLCP, getTTFB } from 'web-vitals';

getCLS(console.log);
getFID(console.log);
getFCP(console.log);
getLCP(console.log);
getTTFB(console.log);
```

### Custom Performance Marks
```typescript
// Mark component lifecycle
useEffect(() => {
  performance.mark('Component-Mount-Start');

  return () => {
    performance.mark('Component-Mount-End');
    performance.measure(
      'Component-Mount',
      'Component-Mount-Start',
      'Component-Mount-End'
    );
  };
}, []);
```

### React 18 Concurrent Features
```tsx
// useTransition for non-urgent updates
const [isPending, startTransition] = useTransition();

function handleClick() {
  startTransition(() => {
    setTab('posts'); // Non-urgent update
  });
}

// useDeferredValue for deferred rendering
const deferredQuery = useDeferredValue(searchQuery);
```

## Related Skills

- **react-guardian**: Ensures React best practices and patterns
- **style-assistant**: Optimizes CSS and styling performance
- **test-writer**: Writes performance tests to catch regressions
