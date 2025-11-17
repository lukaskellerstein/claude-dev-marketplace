---
name: performance-monitor
description: Monitors performance patterns and suggests optimizations
allowed-tools: Read, Grep
---

# Performance Monitor Skill

Automatically detect performance issues and suggest optimizations during development.

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

// ✅ Lazy loading
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
```

## Image Optimization

### Lazy Loading
```tsx
// ❌ Loading all images immediately
<img src={imageUrl} alt="Product" />

// ✅ Lazy loading
<img
  src={imageUrl}
  alt="Product"
  loading="lazy"
  decoding="async"
/>

// ✅ With placeholder
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

## Optimization Suggestions

### Immediate Actions
```markdown
🚀 Performance Optimization Detected

**Issue**: Component re-renders 8 times on data update
**Location**: Dashboard.tsx
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

## Monitoring Integration

### React DevTools Profiler
- Identify components causing re-renders
- Measure render duration
- Find performance bottlenecks

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