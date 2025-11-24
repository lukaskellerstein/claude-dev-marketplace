---
name: accessibility-checker
description: Auto-invoked when creating or modifying UI components to ensure WCAG 2.1 accessibility standards
allowed-tools: Read, Grep, Glob
---

# Accessibility Checker

This skill provides real-time guidance on implementing accessible UI components that comply with WCAG 2.1 Level AA standards.

## When Active

This skill activates when you:
- Create new React components with UI elements
- Modify existing components with interactive elements
- Add forms, buttons, inputs, or navigation
- Implement modals, dropdowns, or dynamic content
- Work with images, videos, or media
- Design responsive layouts

## WCAG 2.1 Principles (POUR)

### Perceivable
Information must be presentable to users in ways they can perceive.

### Operable
User interface components must be operable.

### Understandable
Information and operation must be understandable.

### Robust
Content must be robust enough for assistive technologies.

## Accessibility Checklist

### Semantic HTML
Use semantic HTML elements for their intended purpose:

```tsx
// ❌ Bad: Non-semantic markup
<div onClick={handleClick}>Submit</div>

// ✅ Good: Semantic button
<button onClick={handleClick}>Submit</button>

// ❌ Bad: Generic containers
<div>
  <div>Main Article</div>
  <div>Sidebar</div>
</div>

// ✅ Good: Semantic structure
<main>
  <article>Main Article</article>
  <aside>Sidebar</aside>
</main>
```

### Keyboard Navigation
All interactive elements must be keyboard accessible:

```tsx
// ✅ Interactive elements
<button
  onClick={handleClick}
  onKeyDown={(e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      handleClick();
    }
  }}
  tabIndex={0}
>
  Click me
</button>

// ✅ Custom interactive element
<div
  role="button"
  tabIndex={0}
  onClick={handleClick}
  onKeyDown={(e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      handleClick();
    }
  }}
>
  Custom button
</div>

// ✅ Skip to main content
<a href="#main-content" className="sr-only focus:not-sr-only">
  Skip to main content
</a>
```

### ARIA Attributes
Use ARIA to enhance accessibility when HTML semantics aren't enough:

```tsx
// Labels
<button aria-label="Close modal">
  <X className="h-4 w-4" />
</button>

// Described by
<input
  type="email"
  aria-describedby="email-hint"
  aria-invalid={hasError}
/>
<p id="email-hint">We'll never share your email</p>

// Live regions for dynamic updates
<div
  role="status"
  aria-live="polite"
  aria-atomic="true"
>
  {successMessage}
</div>

// Modal dialog
<div
  role="dialog"
  aria-modal="true"
  aria-labelledby="modal-title"
  aria-describedby="modal-description"
>
  <h2 id="modal-title">Confirm Action</h2>
  <p id="modal-description">Are you sure you want to continue?</p>
</div>

// Loading state
<button
  disabled={isLoading}
  aria-busy={isLoading}
>
  {isLoading ? 'Loading...' : 'Submit'}
</button>

// Expanded/collapsed state
<button
  aria-expanded={isOpen}
  aria-controls="dropdown-menu"
  onClick={() => setIsOpen(!isOpen)}
>
  Menu
</button>
<div id="dropdown-menu" hidden={!isOpen}>
  Menu items
</div>
```

### Focus Management

```tsx
import { useRef, useEffect } from 'react';

// Focus trap in modal
function Modal({ isOpen, onClose }) {
  const modalRef = useRef<HTMLDivElement>(null);
  const previousFocusRef = useRef<HTMLElement | null>(null);

  useEffect(() => {
    if (isOpen) {
      // Save current focus
      previousFocusRef.current = document.activeElement as HTMLElement;

      // Focus first focusable element in modal
      const firstFocusable = modalRef.current?.querySelector(
        'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
      ) as HTMLElement;
      firstFocusable?.focus();

      // Handle Escape key
      const handleEscape = (e: KeyboardEvent) => {
        if (e.key === 'Escape') {
          onClose();
        }
      };
      document.addEventListener('keydown', handleEscape);

      return () => {
        document.removeEventListener('keydown', handleEscape);
        // Restore focus
        previousFocusRef.current?.focus();
      };
    }
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return (
    <div
      ref={modalRef}
      role="dialog"
      aria-modal="true"
      className="fixed inset-0 z-50 flex items-center justify-center"
      onClick={(e) => {
        if (e.target === e.currentTarget) onClose();
      }}
    >
      <div className="bg-white rounded-lg p-6">
        <h2 id="modal-title">Modal Title</h2>
        <button onClick={onClose}>Close</button>
      </div>
    </div>
  );
}
```

### Form Accessibility

```tsx
// ✅ Accessible form
<form onSubmit={handleSubmit}>
  <div>
    <label htmlFor="email" className="block text-sm font-medium">
      Email Address
      <span className="text-red-500" aria-label="required">*</span>
    </label>
    <input
      id="email"
      type="email"
      name="email"
      required
      aria-required="true"
      aria-invalid={errors.email ? 'true' : 'false'}
      aria-describedby={errors.email ? 'email-error' : 'email-hint'}
      className="mt-1 block w-full"
    />
    <p id="email-hint" className="text-sm text-gray-500">
      We'll never share your email
    </p>
    {errors.email && (
      <p id="email-error" className="text-sm text-red-600" role="alert">
        {errors.email}
      </p>
    )}
  </div>

  <fieldset>
    <legend className="text-sm font-medium">Notification Preferences</legend>
    <div className="space-y-2">
      <label className="flex items-center">
        <input type="checkbox" name="email_notifications" />
        <span className="ml-2">Email notifications</span>
      </label>
      <label className="flex items-center">
        <input type="checkbox" name="sms_notifications" />
        <span className="ml-2">SMS notifications</span>
      </label>
    </div>
  </fieldset>

  <button
    type="submit"
    disabled={isSubmitting}
    aria-busy={isSubmitting}
  >
    {isSubmitting ? 'Submitting...' : 'Submit'}
  </button>
</form>
```

### Images and Media

```tsx
// Decorative images
<img src="/decoration.svg" alt="" role="presentation" />

// Informative images
<img
  src="/chart.png"
  alt="Sales growth chart showing 25% increase from Q1 to Q2"
/>

// Complex images with longdesc
<img
  src="/complex-diagram.png"
  alt="System architecture diagram"
  aria-describedby="diagram-description"
/>
<div id="diagram-description" className="sr-only">
  Detailed description of the architecture showing three layers...
</div>

// Video with captions
<video controls>
  <source src="/video.mp4" type="video/mp4" />
  <track
    kind="captions"
    src="/captions.vtt"
    srcLang="en"
    label="English captions"
    default
  />
</video>
```

### Color Contrast

Ensure WCAG AA compliance:
- Normal text: 4.5:1 contrast ratio
- Large text (18pt+): 3:1 contrast ratio
- UI components: 3:1 contrast ratio

```tsx
// ❌ Bad: Insufficient contrast
<p className="text-gray-400 bg-white">Low contrast text</p>

// ✅ Good: Sufficient contrast
<p className="text-gray-700 bg-white">Good contrast text</p>

// Use tools to check:
// - Chrome DevTools Accessibility panel
// - WebAIM Contrast Checker
// - axe DevTools extension
```

### Screen Reader Support

```tsx
// Screen reader only text
<span className="sr-only">
  Opens in new window
</span>

// Hide decorative elements
<div aria-hidden="true">
  <DecorativeIcon />
</div>

// Announce dynamic changes
function Toast({ message }: { message: string }) {
  return (
    <div
      role="alert"
      aria-live="assertive"
      aria-atomic="true"
      className="fixed bottom-4 right-4 bg-green-600 text-white p-4 rounded"
    >
      {message}
    </div>
  );
}
```

### Touch Targets

Minimum 44x44px for touch targets:

```tsx
// ✅ Touch-friendly button
<button className="min-h-[44px] min-w-[44px] p-3">
  <Icon className="h-5 w-5" />
</button>

// ✅ Touch-friendly list items
<nav className="space-y-2">
  {items.map(item => (
    <a
      key={item.id}
      href={item.url}
      className="block py-3 px-4 hover:bg-gray-100"
    >
      {item.label}
    </a>
  ))}
</nav>
```

## Common ARIA Roles

- `role="banner"` - Site header
- `role="navigation"` - Navigation section
- `role="main"` - Main content
- `role="complementary"` - Sidebar/aside
- `role="contentinfo"` - Footer
- `role="search"` - Search form
- `role="button"` - Custom button
- `role="dialog"` - Modal dialog
- `role="alert"` - Important message
- `role="status"` - Status update
- `role="progressbar"` - Progress indicator
- `role="tab"`, `role="tabpanel"` - Tabs
- `role="menu"`, `role="menuitem"` - Menu

## Testing Checklist

When implementing components, verify:
- [ ] Can navigate entire UI with keyboard only
- [ ] Tab order is logical
- [ ] Focus is visible
- [ ] Screen reader announces all content correctly
- [ ] Color is not the only way to convey information
- [ ] Text meets contrast requirements (4.5:1)
- [ ] Form inputs have labels
- [ ] Error messages are associated with inputs
- [ ] Images have alt text
- [ ] Buttons have accessible names
- [ ] Interactive elements have appropriate ARIA
- [ ] Loading states are announced
- [ ] Modal focus is trapped
- [ ] Headings are hierarchical (h1, h2, h3)

## Testing Tools

- **Chrome DevTools**: Accessibility panel, Lighthouse audit
- **axe DevTools**: Browser extension for accessibility testing
- **WAVE**: Web accessibility evaluation tool
- **NVDA/JAWS**: Screen reader testing (Windows)
- **VoiceOver**: Screen reader testing (Mac/iOS)
- **jest-axe**: Automated accessibility testing in Jest

## Resources

- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [MDN Accessibility](https://developer.mozilla.org/en-US/docs/Web/Accessibility)
- [React Accessibility](https://react.dev/learn/accessibility)
- [A11y Project Checklist](https://www.a11yproject.com/checklist/)
- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)

Use this guidance to ensure all UI components are accessible to all users, regardless of ability or assistive technology.
