# Frontend Plugin

Comprehensive toolkit for modern frontend development with React, TypeScript, Tailwind CSS, shadcn-ui, and responsive design best practices.

## Features

### Agents

- **react-expert**: Senior React engineer specializing in hooks, TypeScript, component architecture, state management, and performance optimization
- **css-tailwind-expert**: Styling expert for CSS, SCSS, Tailwind CSS, shadcn-ui, Radix UI, and design systems
- **responsive-design-expert**: Specialist in responsive web design, mobile-first development, and cross-device compatibility

### Commands

- `/build-component`: Build production-ready React components with TypeScript, styling, and tests
- `/create-design-system`: Create or enhance design systems with tokens, components, and documentation
- `/audit-frontend`: Comprehensive audit for performance, accessibility, and best practices

### Skills

- **accessibility-checker**: Auto-invoked to ensure WCAG 2.1 accessibility standards in UI components
- **performance-optimizer**: Auto-invoked to identify and prevent React performance issues

### MCP Integration

- **shadcn-ui MCP**: Direct integration with shadcn-ui component library for seamless component installation and customization

## Usage

### Build React Components

```
/build-component

Create a Button component with variants (primary, secondary, ghost), sizes (sm, md, lg), and loading state
```

The command will:
1. Design the component architecture with TypeScript interfaces
2. Implement responsive styles with Tailwind CSS
3. Add accessibility features (ARIA, keyboard navigation)
4. Include usage examples and documentation

**More Examples:**

```
/build-component

Build a DataTable component with:
- Sortable columns
- Pagination
- Row selection
- Responsive mobile view
- Loading and empty states
```

```
/build-component

Create a SearchInput with debounced input, clear button, and autocomplete dropdown
```

### Create Design System

```
/create-design-system

Create a design system with:
- Color palette (brand + semantic colors)
- Typography (2 font families, 5 size levels)
- 10 core components (Button, Input, Card, Badge, etc.)
- Dark mode support
```

The command will:
1. Analyze existing codebase
2. Define design tokens (colors, typography, spacing)
3. Configure Tailwind with custom theme
4. Build component library with shadcn-ui integration
5. Create comprehensive documentation

**More Examples:**

```
/create-design-system

Enhance existing design system with:
- Advanced components (DataTable, Calendar, CommandPalette)
- Animation tokens
- Multi-theme support
```

### Audit Frontend Codebase

```
/audit-frontend

Audit the React application for performance and accessibility issues
```

The command will:
1. Scan codebase for issues
2. Identify performance bottlenecks
3. Check WCAG 2.1 accessibility compliance
4. Review bundle size
5. Generate prioritized action plan

**More Examples:**

```
/audit-frontend

Perform comprehensive audit:
- Memory leaks in useEffect
- Missing loading states
- Dark mode inconsistencies
- Bundle size optimization
```

### Use Agents Directly

Invoke specialized agents for focused work:

**React Development:**
```
Use react-expert to refactor this component with proper TypeScript types and custom hooks
```

**Styling Work:**
```
Use css-tailwind-expert to create a responsive navigation bar with Tailwind and shadcn-ui
```

**Responsive Design:**
```
Use responsive-design-expert to make this dashboard mobile-friendly with proper breakpoints
```

## Technology Stack

### Core Technologies
- **React 18+**: Server Components, Suspense, Concurrent Features
- **TypeScript**: Strong typing, interfaces, generics
- **Tailwind CSS**: Utility-first styling with JIT mode
- **shadcn-ui**: High-quality, accessible component primitives
- **Radix UI**: Unstyled, accessible UI components

### State Management
- **Context API**: Built-in React state management
- **Zustand**: Lightweight state management
- **TanStack Query**: Server state management
- **React Hook Form**: Form state and validation

### Build Tools
- **Vite**: Fast build tool and dev server
- **Next.js**: React framework with SSR/SSG
- **Remix**: Full-stack React framework

### Testing
- **React Testing Library**: Component testing
- **Jest**: Unit testing framework
- **Playwright**: E2E testing

### Performance
- **React DevTools Profiler**: Performance analysis
- **Lighthouse**: Performance auditing
- **Bundle Analyzer**: Bundle size optimization

## Best Practices Covered

### React Patterns
- Functional components with hooks
- Custom hooks for reusable logic
- Component composition
- Props interface design
- Error boundaries
- Suspense and lazy loading
- Server Components (React 18+)

### TypeScript
- Strongly typed components
- Generic components
- Type-safe event handlers
- Utility types
- Discriminated unions

### Styling
- Tailwind utility-first approach
- Design system with tokens
- Responsive design (mobile-first)
- Dark mode support
- CSS Grid and Flexbox
- Animations and transitions

### Performance
- React.memo for expensive components
- useMemo for computations
- useCallback for function stability
- Code splitting and lazy loading
- Virtual scrolling for long lists
- Image optimization
- Bundle size optimization

### Accessibility
- WCAG 2.1 Level AA compliance
- Semantic HTML
- ARIA attributes
- Keyboard navigation
- Screen reader support
- Color contrast
- Focus management

### Responsive Design
- Mobile-first approach
- Breakpoint strategy
- Responsive typography
- Touch-friendly interfaces
- Container queries
- Responsive images

## Integration with shadcn-ui

This plugin includes the shadcn-ui MCP server for seamless component integration:

```bash
# Add components directly
npx shadcn@latest add button
npx shadcn@latest add card
npx shadcn@latest add form

# Or let agents recommend and integrate components
```

The agents will automatically suggest shadcn-ui components when appropriate and customize them for your needs.

## Example Workflows

### 1. Building a Dashboard

```
1. Use create-design-system to establish design tokens
2. Use build-component to create layout components (Sidebar, Header)
3. Use build-component to create data visualization components
4. Use responsive-design-expert to optimize for mobile
5. Use audit-frontend to verify performance and accessibility
```

### 2. Creating a Landing Page

```
1. Use css-tailwind-expert to design hero section with animations
2. Use build-component to create feature cards
3. Use build-component to create contact form with validation
4. Use responsive-design-expert to ensure mobile responsiveness
5. Use accessibility-checker skill (auto-invoked) to verify WCAG compliance
```

### 3. Refactoring Legacy Code

```
1. Use audit-frontend to identify issues
2. Use react-expert to refactor components with modern patterns
3. Use css-tailwind-expert to migrate to Tailwind CSS
4. Use performance-optimizer skill (auto-invoked) to prevent performance issues
5. Use build-component to create missing test coverage
```

## Output Quality

All agents and commands provide:
- **Production-ready code**: Complete, tested, and documented
- **TypeScript types**: Proper interfaces and type safety
- **Accessibility**: WCAG 2.1 compliance
- **Responsiveness**: Mobile-first, cross-device support
- **Performance**: Optimized for speed and efficiency
- **Best practices**: Industry-standard patterns and conventions
- **Documentation**: Clear usage examples and API docs

## Skills Auto-Invocation

The plugin includes intelligent skills that automatically activate:

### Accessibility Checker
Activates when you:
- Create UI components
- Add forms or inputs
- Implement navigation
- Work with images or media

Ensures:
- Semantic HTML
- ARIA attributes
- Keyboard navigation
- Screen reader support
- Color contrast

### Performance Optimizer
Activates when you:
- Create React components
- Implement state management
- Work with lists
- Add effects

Ensures:
- Proper memoization
- Efficient state updates
- No memory leaks
- Optimized re-renders

## Getting Started

1. **Install the plugin** in your Claude Code marketplace
2. **Start with audit**: `/audit-frontend` to understand current state
3. **Build components**: Use `/build-component` for new features
4. **Create design system**: Use `/create-design-system` to establish consistency
5. **Iterate**: Use agents directly for focused improvements

## Support and Resources

- [React Documentation](https://react.dev)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [Tailwind CSS Docs](https://tailwindcss.com/docs)
- [shadcn-ui Components](https://ui.shadcn.com)
- [Radix UI Primitives](https://www.radix-ui.com)
- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [React Performance](https://react.dev/learn/render-and-commit)

## Contributing

This plugin follows best practices for:
- Component architecture
- TypeScript usage
- Accessibility standards
- Performance optimization
- Responsive design
- Code quality

All recommendations are based on industry standards and official documentation.
