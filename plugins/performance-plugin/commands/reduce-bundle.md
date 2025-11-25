---
description: Analyze and reduce frontend bundle size through tree shaking, code splitting, and dependency optimization
---

Analyze JavaScript bundle size and implement optimizations to reduce initial load time, improve Core Web Vitals, and enhance user experience.

## Process

Follow these steps:

1. **Bundle Analysis**: Analyze current bundle composition
   - Identify bundle size and breakdown
   - Detect large dependencies
   - Find duplicate dependencies
   - Analyze chunk distribution
   - Check for unused code
   - Review source maps

2. **Launch Frontend Optimizer**: Use `performance-plugin:frontend-optimizer` agent to:
   - Analyze webpack/vite bundle
   - Identify large dependencies (> 50KB)
   - Find tree-shaking opportunities
   - Recommend dependency replacements
   - Suggest code splitting strategies
   - Optimize chunk configuration
   - Review dynamic imports

3. **Dependency Audit**: Review package dependencies
   - Check package sizes (bundlephobia)
   - Find smaller alternatives
   - Identify unused dependencies
   - Check for tree-shakeable versions
   - Analyze transitive dependencies
   - Review peer dependencies

4. **Code Splitting Strategy**: Implement optimal splitting
   - Route-based code splitting
   - Component-based lazy loading
   - Vendor chunk optimization
   - Common chunk extraction
   - Dynamic imports for heavy components
   - Preloading critical chunks

5. **Tree Shaking Optimization**: Enable dead code elimination
   - Configure proper sideEffects
   - Use ES6 module imports
   - Enable production mode optimizations
   - Remove unused exports
   - Optimize package.json

6. **Bundle Budget**: Set performance budgets
   - Define size limits per chunk
   - Configure webpack performance hints
   - Setup CI/CD bundle size checks
   - Monitor bundle size over time

## Output

Present a detailed bundle optimization report:

### Bundle Analysis Summary
```
Bundle Size Analysis
====================

Total Bundle Size: 2.5MB (uncompressed)
                   850KB (gzip)

Breakdown:
- Vendor chunks: 1.8MB (72%)
- Application code: 700KB (28%)

Large Dependencies (>50KB):
1. moment.js: 288KB (11.5%)
2. lodash: 531KB (21.2%)
3. chart.js: 245KB (9.8%)
4. react + react-dom: 350KB (14%)
5. material-ui: 420KB (16.8%)

Optimization Potential: 60% size reduction (2.5MB → 1MB)
Expected LCP Improvement: 3.2s → 1.8s
```

### Critical Issues

#### 1. Entire Lodash Library Imported

**Current Usage**:
```javascript
import _ from 'lodash'; // Imports entire 531KB library

const debounced = _.debounce(handler, 300);
const sorted = _.sortBy(items, 'name');
```

**Issue**: Using only 2 functions but importing entire library

**Impact**:
- Bundle size: +531KB
- Parse time: +180ms
- Unnecessary code: 99% of lodash unused

**Solution 1**: Use lodash-es with tree shaking
```javascript
// Install tree-shakeable version
npm uninstall lodash
npm install lodash-es

// Import only what you need
import { debounce, sortBy } from 'lodash-es';

const debounced = debounce(handler, 300);
const sorted = sortBy(items, 'name');
```

**Solution 2**: Use individual packages
```javascript
npm install lodash.debounce lodash.sortby

import debounce from 'lodash.debounce';
import sortBy from 'lodash.sortby';
```

**Results**:
- Bundle size: 531KB → 15KB (97% reduction)
- Parse time: 180ms → 5ms

---

#### 2. Moment.js for Simple Date Formatting

**Current Usage**:
```javascript
import moment from 'moment'; // 288KB

const formatted = moment(date).format('YYYY-MM-DD');
const relative = moment(date).fromNow();
```

**Issue**: Using heavy library for simple formatting

**Impact**:
- Bundle size: +288KB
- Parse time: +95ms
- Includes all locales (unnecessary)

**Solution 1**: Replace with date-fns (modern, tree-shakeable)
```javascript
npm uninstall moment
npm install date-fns

import { format, formatDistanceToNow } from 'date-fns';

const formatted = format(date, 'yyyy-MM-dd');
const relative = formatDistanceToNow(date, { addSuffix: true });
```

**Solution 2**: Replace with dayjs (2KB, moment-like API)
```javascript
npm install dayjs

import dayjs from 'dayjs';
import relativeTime from 'dayjs/plugin/relativeTime';

dayjs.extend(relativeTime);

const formatted = dayjs(date).format('YYYY-MM-DD');
const relative = dayjs(date).fromNow();
```

**Solution 3**: Use native Intl API (no dependencies)
```javascript
// Date formatting
const formatted = new Intl.DateTimeFormat('en-US', {
  year: 'numeric',
  month: '2-digit',
  day: '2-digit',
}).format(date);

// Relative time (requires polyfill for older browsers)
const relative = new Intl.RelativeTimeFormat('en', {
  style: 'long',
}).format(-5, 'day'); // "5 days ago"
```

**Results**:
| Solution | Bundle Size | Savings |
|----------|-------------|---------|
| date-fns | 14KB | 274KB (95%) |
| dayjs | 2KB | 286KB (99%) |
| Native Intl | 0KB | 288KB (100%) |

---

#### 3. No Code Splitting

**Current Build**:
```
main.js: 2.5MB (entire app in one file)
```

**Issues**:
- Large initial download
- Slow parse time
- No lazy loading
- Poor caching (entire bundle invalidated on any change)

**Solution**: Implement route-based code splitting
```javascript
// Before: Import all routes
import Dashboard from './pages/Dashboard';
import Profile from './pages/Profile';
import Settings from './pages/Settings';
import Analytics from './pages/Analytics';

// After: Lazy load routes
import { lazy, Suspense } from 'react';

const Dashboard = lazy(() => import('./pages/Dashboard'));
const Profile = lazy(() => import('./pages/Profile'));
const Settings = lazy(() => import('./pages/Settings'));
const Analytics = lazy(() => import('./pages/Analytics'));

function App() {
  return (
    <Suspense fallback={<LoadingSpinner />}>
      <Routes>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/profile" element={<Profile />} />
        <Route path="/settings" element={<Settings />} />
        <Route path="/analytics" element={<Analytics />} />
      </Routes>
    </Suspense>
  );
}
```

**Webpack Configuration**:
```javascript
// webpack.config.js
module.exports = {
  optimization: {
    splitChunks: {
      chunks: 'all',
      cacheGroups: {
        // Vendor chunk
        vendor: {
          test: /[\\/]node_modules[\\/]/,
          name: 'vendors',
          priority: 10,
        },
        // Common code used by multiple routes
        common: {
          minChunks: 2,
          priority: 5,
          reuseExistingChunk: true,
        },
        // React and React-DOM in separate chunk
        react: {
          test: /[\\/]node_modules[\\/](react|react-dom)[\\/]/,
          name: 'react',
          priority: 20,
        },
      },
    },
    runtimeChunk: 'single',
  },
};
```

**Results**:
```
Before:
  main.js: 2.5MB

After:
  main.js: 150KB (app shell)
  vendors.js: 800KB (shared dependencies)
  react.js: 350KB (React framework)
  dashboard.js: 180KB (loaded on demand)
  profile.js: 120KB (loaded on demand)
  settings.js: 95KB (loaded on demand)
  analytics.js: 340KB (loaded on demand)
```

**Benefits**:
- Initial bundle: 2.5MB → 1.3MB (48% reduction)
- Subsequent routes load on demand
- Better caching (vendor chunk rarely changes)
- Faster initial page load

---

#### 4. Unused Dependencies

**Detection**:
```bash
npm install -g depcheck
depcheck
```

**Found Unused**:
```
Unused dependencies:
- axios-retry (45KB) - installed but never imported
- lodash.merge (12KB) - replaced but not removed
- classnames (2KB) - alternative solution used
- prop-types (8KB) - TypeScript used instead

Total: 67KB of unused dependencies
```

**Solution**:
```bash
npm uninstall axios-retry lodash.merge classnames prop-types
```

**Results**: 67KB removed from bundle

---

#### 5. Material-UI Full Import

**Current Usage**:
```javascript
// Imports entire Material-UI library
import { Button, TextField, Dialog } from '@material-ui/core';
```

**Issue**: Imports all components even when only using a few

**Impact**:
- Bundle size: +420KB
- Tree shaking not working properly

**Solution**: Use path imports
```javascript
// Import only specific components
import Button from '@material-ui/core/Button';
import TextField from '@material-ui/core/TextField';
import Dialog from '@material-ui/core/Dialog';
```

**Better Solution**: Configure babel plugin
```bash
npm install babel-plugin-import --save-dev
```

```javascript
// .babelrc
{
  "plugins": [
    [
      "import",
      {
        "libraryName": "@material-ui/core",
        "libraryDirectory": "",
        "camel2DashComponentName": false
      }
    ]
  ]
}

// Now this works with tree shaking
import { Button, TextField, Dialog } from '@material-ui/core';
```

**Results**:
- Bundle size: 420KB → 85KB (80% reduction)
- Only includes used components

---

### Tree Shaking Configuration

#### Enable Proper Tree Shaking

**package.json**:
```json
{
  "sideEffects": false
}
```

Or specify files with side effects:
```json
{
  "sideEffects": [
    "*.css",
    "*.scss",
    "src/polyfills.js"
  ]
}
```

**Webpack Production Mode**:
```javascript
// webpack.config.js
module.exports = {
  mode: 'production', // Enables tree shaking and minification

  optimization: {
    usedExports: true, // Mark unused exports
    minimize: true,
    minimizer: [
      new TerserPlugin({
        terserOptions: {
          compress: {
            drop_console: true, // Remove console.logs
            dead_code: true,
            unused: true,
          },
        },
      }),
    ],
  },
};
```

---

### Dependency Replacements

| Current | Size | Alternative | Size | Savings |
|---------|------|-------------|------|---------|
| moment | 288KB | date-fns | 14KB | 274KB (95%) |
| lodash | 531KB | lodash-es | ~15KB | 516KB (97%) |
| axios | 35KB | fetch API | 0KB | 35KB (100%) |
| uuid | 15KB | crypto.randomUUID() | 0KB | 15KB (100%) |
| classnames | 2KB | clsx | 0.5KB | 1.5KB (75%) |

**Total Savings**: 841.5KB (33% of total bundle)

---

### Image and Asset Optimization

**Current Assets**:
```
images/hero.png: 2.1MB
images/logo.png: 450KB
images/product-*.jpg: 500KB - 1.5MB each
```

**Solution 1**: Convert to Modern Formats
```bash
# Install sharp for image optimization
npm install sharp

# Convert to WebP
sharp input.png -o output.webp
```

```javascript
// Use picture element for format selection
<picture>
  <source srcSet="hero.avif" type="image/avif" />
  <source srcSet="hero.webp" type="image/webp" />
  <img src="hero.jpg" alt="Hero" />
</picture>
```

**Solution 2**: Lazy Load Images
```javascript
// Native lazy loading
<img src="product.jpg" loading="lazy" alt="Product" />

// Or with Intersection Observer for better control
import { useEffect, useRef, useState } from 'react';

function LazyImage({ src, alt }) {
  const [isLoaded, setIsLoaded] = useState(false);
  const imgRef = useRef();

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsLoaded(true);
          observer.disconnect();
        }
      },
      { rootMargin: '50px' }
    );

    if (imgRef.current) {
      observer.observe(imgRef.current);
    }

    return () => observer.disconnect();
  }, []);

  return (
    <img
      ref={imgRef}
      src={isLoaded ? src : 'placeholder.jpg'}
      alt={alt}
    />
  );
}
```

**Results**:
- Image sizes: 70-90% reduction with WebP/AVIF
- Initial page load: Only loads visible images
- Bandwidth: Significantly reduced

---

### Bundle Budget Configuration

**webpack.config.js**:
```javascript
module.exports = {
  performance: {
    hints: 'error',
    maxEntrypointSize: 512000, // 500 KB
    maxAssetSize: 512000,
  },
};
```

**CI/CD Integration**:
```javascript
// scripts/check-bundle-size.js
const fs = require('fs');
const path = require('path');

const BUDGET = {
  'main.js': 200 * 1024, // 200 KB
  'vendors.js': 500 * 1024, // 500 KB
  'react.js': 150 * 1024, // 150 KB
};

const distPath = path.join(__dirname, '../dist');
const files = fs.readdirSync(distPath);

let failed = false;

files.forEach(file => {
  if (file.endsWith('.js')) {
    const filePath = path.join(distPath, file);
    const size = fs.statSync(filePath).size;
    const budgetKey = file.split('.')[0] + '.js';
    const budget = BUDGET[budgetKey];

    if (budget && size > budget) {
      console.error(`❌ ${file}: ${(size / 1024).toFixed(2)}KB exceeds budget ${(budget / 1024).toFixed(2)}KB`);
      failed = true;
    } else {
      console.log(`✅ ${file}: ${(size / 1024).toFixed(2)}KB`);
    }
  }
});

if (failed) {
  process.exit(1);
}
```

**package.json**:
```json
{
  "scripts": {
    "build": "webpack --mode production",
    "check-size": "node scripts/check-bundle-size.js",
    "build:check": "npm run build && npm run check-size"
  }
}
```

---

### Implementation Plan

#### Week 1: Quick Wins
- [ ] Replace moment.js with date-fns (274KB saved)
- [ ] Switch lodash to lodash-es with tree shaking (516KB saved)
- [ ] Remove unused dependencies (67KB saved)
- [ ] Enable production mode optimizations
- [ ] Configure proper sideEffects

**Total Savings**: 857KB (34% reduction)

#### Week 2: Code Splitting
- [ ] Implement route-based lazy loading
- [ ] Setup vendor chunk optimization
- [ ] Configure chunk splitting strategy
- [ ] Add loading states for lazy components
- [ ] Preload critical chunks

**Additional Savings**: Initial bundle reduced by 50%

#### Week 3: Advanced Optimizations
- [ ] Optimize Material-UI imports (335KB saved)
- [ ] Convert images to WebP/AVIF
- [ ] Implement image lazy loading
- [ ] Setup bundle size monitoring
- [ ] Configure performance budgets in CI/CD

**Additional Savings**: 500KB+ (images)

---

### Results Summary

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Total Bundle | 2.5MB | 1.0MB | 60% reduction |
| Initial Load | 2.5MB | 1.3MB | 48% reduction |
| Gzip Size | 850KB | 340KB | 60% reduction |
| Parse Time | 850ms | 280ms | 67% faster |
| LCP | 3.2s | 1.8s | 44% faster |
| FCP | 2.1s | 1.2s | 43% faster |
| Lighthouse Score | 65 | 92 | +27 points |

---

## Best Practices Applied

- **Tree Shaking**: Use ES6 imports and configure sideEffects
- **Code Splitting**: Lazy load routes and heavy components
- **Dependency Audit**: Replace large dependencies with smaller alternatives
- **Bundle Analysis**: Regular analysis with webpack-bundle-analyzer
- **Performance Budgets**: Enforce size limits in CI/CD
- **Modern Formats**: Use WebP/AVIF for images
- **Lazy Loading**: Load images and components on demand

## Examples

### Full Bundle Optimization
```
/reduce-bundle

Analyze entire bundle, identify large dependencies,
implement code splitting, and set up performance budgets.
```

### Dependency Optimization Only
```
/reduce-bundle

Focus on replacing large dependencies with smaller
alternatives (moment → date-fns, lodash → lodash-es).
```

### Code Splitting Strategy
```
/reduce-bundle

Implement route-based and component-based code splitting
with optimal chunk configuration.
```

### Bundle Size Regression Prevention
```
/reduce-bundle

Setup bundle size monitoring and CI/CD checks to
prevent future regressions.
```

## Integration with Other Commands

- Use as follow-up to `/performance-audit`
- Complements frontend performance optimization
- Precedes load testing to verify improvements
- Part of continuous performance monitoring

Provide specific, actionable bundle optimizations with before/after comparisons, bundle analysis visualizations, and measurable performance improvements.
