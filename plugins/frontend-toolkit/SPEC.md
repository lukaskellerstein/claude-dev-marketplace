# Frontend Toolkit Plugin - Specification v2.0

## Overview

Comprehensive frontend development plugin for React, TypeScript, CSS/SCSS, Tailwind CSS, shadcn-ui, and Radix UI with streamlined commands, consolidated agents, and intelligent skills.

**Architecture:** Commands parse arguments → Agents perform heavy work → Skills provide auto-assistance

**Key Improvements:**
- ✅ Proper argument parsing with defaults
- ✅ Consolidated agents (4 instead of 9)
- ✅ Clear skill trigger definitions
- ✅ Simplified command structure

---

## Table of Contents

1. [Commands](#commands) - 7 streamlined commands
2. [Agents](#agents) - 4 powerful consolidated agents
3. [Skills](#skills) - Auto-invoked with clear triggers
4. [MCP Servers](#mcp-servers) - Documentation access
5. [Files Structure](#files-structure)
6. [Usage Examples](#usage-examples)

---

## Commands

### `/component` - Generate React Components

**Purpose:** Generate React components with TypeScript and chosen styling
**Allowed Tools:** Read, Write, Grep, Glob, Task

```markdown
---
description: Generate React component with best practices
allowed-tools: Read, Write, Grep, Glob, Task
---

# Parse arguments with smart defaults
name="${1:-}"
shift || true
args="$*"

# Extract flags with defaults
type="basic"
ui_lib="shadcn"
styles="tailwind"
with_state=false
with_memo=false
with_test=false

for arg in $args; do
  case $arg in
    --type=*) type="${arg#*=}" ;;
    --ui=*) ui_lib="${arg#*=}" ;;
    --styles=*) styles="${arg#*=}" ;;
    --with-state) with_state=true ;;
    --memo) with_memo=true ;;
    --test) with_test=true ;;
  esac
done

# Interactive mode if no name
if [ -z "$name" ]; then
  Ask user for component name and preferences
fi

# Detect project conventions
Use Grep to detect:
- Existing UI library patterns
- Current styling approach
- TypeScript/JavaScript usage

# Invoke agent
Invoke react-generator agent with:
- name: $name
- type: $type (basic|form|page|layout|card)
- ui_lib: $ui_lib (shadcn|radix|headless|none)
- styles: $styles (tailwind|css-modules|scss|styled-components)
- with_state: $with_state
- with_memo: $with_memo
- with_test: $with_test
```

**Examples:**
```bash
/component UserCard
/component UserCard --type=card --ui=shadcn --styles=tailwind
/component LoginForm --type=form --ui=radix --with-state --test
/component Dashboard --type=page --memo
```

---

### `/hook` - Generate Custom Hooks

**Purpose:** Generate custom React hooks
**Allowed Tools:** Read, Write, Grep, Task

```markdown
---
description: Generate custom React hook
allowed-tools: Read, Write, Grep, Task
---

# Parse arguments
name="${1:-}"
shift || true
args="$*"

# Validate hook name
if [[ ! "$name" =~ ^use ]]; then
  if [ -n "$name" ]; then
    name="use${name^}"  # Capitalize and prepend 'use'
  fi
fi

# Extract purpose and options
purpose="custom"
with_cleanup=false
with_test=false

for arg in $args; do
  case $arg in
    --purpose=*) purpose="${arg#*=}" ;;
    --with-cleanup) with_cleanup=true ;;
    --test) with_test=true ;;
  esac
done

# Interactive mode if no name
if [ -z "$name" ]; then
  Ask user for hook name and purpose
fi

# Invoke agent
Invoke react-generator agent with:
- name: $name
- purpose: $purpose (state|fetch|storage|media-query|animation|form|custom)
- with_cleanup: $with_cleanup
- with_test: $with_test
```

**Examples:**
```bash
/hook useLocalStorage --purpose=storage
/hook useMediaQuery --purpose=media-query
/hook useFadeIn --purpose=animation --with-cleanup
/hook useDebounce --test
```

---

### `/style` - Style Management

**Purpose:** Add, convert, or optimize styles
**Allowed Tools:** Read, Write, Grep, Glob, Task

```markdown
---
description: Manage component styles
allowed-tools: Read, Write, Grep, Glob, Task
---

# Parse arguments
target="${1:-.}"  # Default to current directory
shift || true
args="$*"

# Extract options
method="tailwind"  # Default
action="add"  # add|convert|optimize
convert_from=""
convert_to=""
responsive=false

for arg in $args; do
  case $arg in
    --method=*) method="${arg#*=}" ;;
    --convert=*)
      action="convert"
      IFS='→' read -r convert_from convert_to <<< "${arg#*=}"
      ;;
    --optimize) action="optimize" ;;
    --responsive) responsive=true ;;
  esac
done

# Invoke appropriate agent based on action
case $action in
  add)
    Invoke style-master agent to add $method styles to $target
    ;;
  convert)
    Invoke style-master agent to convert from $convert_from to $convert_to
    ;;
  optimize)
    Invoke style-master agent to optimize styles in $target
    ;;
esac
```

**Examples:**
```bash
/style . --method=tailwind
/style UserCard.tsx --method=scss --responsive
/style . --convert=css-modules→tailwind
/style src/components --optimize
```

---

### `/add-ui` - Add UI Components

**Purpose:** Add UI library components (replaces /shadcn-add and /radix-add)
**Allowed Tools:** Bash, Read, Write, Task

```markdown
---
description: Add UI library components
allowed-tools: Bash, Read, Write, Task
---

# Parse arguments
library="${1:-shadcn}"  # Default to shadcn
shift || true
components="$*"

# Handle special flags
if [[ "$components" == *"--list"* ]]; then
  Show available components for $library
  exit 0
fi

# Validate library
case $library in
  shadcn|radix|mui|chakra|ant)
    ;;
  *)
    echo "Unknown library: $library"
    echo "Available: shadcn, radix, mui, chakra, ant"
    exit 1
    ;;
esac

# Interactive mode if no components
if [ -z "$components" ]; then
  Ask user to select components from list
fi

# Install based on library
case $library in
  shadcn)
    npx shadcn-ui@latest add $components
    ;;
  radix)
    npm install @radix-ui/react-$components
    Generate wrapper components with basic styling
    ;;
  *)
    Install and configure $library components
    ;;
esac
```

**Examples:**
```bash
/add-ui shadcn button card dialog
/add-ui radix dropdown-menu tooltip
/add-ui shadcn --list
/add-ui mui data-grid
```

---

### `/architect` - Project Architecture

**Purpose:** Design complete frontend architecture
**Allowed Tools:** Read, Write, Grep, Glob, Task

```markdown
---
description: Design frontend architecture
allowed-tools: Read, Write, Grep, Glob, Task
---

# Parse arguments
project_type="${1:-spa}"
shift || true
args="$*"

# Extract options with smart defaults
preset=""
stack=""
features=""
generate_structure=false

for arg in $args; do
  case $arg in
    --preset=*) preset="${arg#*=}" ;;
    --stack=*) stack="${arg#*=}" ;;
    --features=*) features="${arg#*=}" ;;
    --generate) generate_structure=true ;;
  esac
done

# Apply preset if specified
case $preset in
  enterprise)
    stack="react,typescript,tailwind,shadcn,zustand,react-router"
    features="auth,api,state,routing,i18n,testing"
    ;;
  minimal)
    stack="react,typescript,tailwind"
    features="routing"
    ;;
  *)
    # Use provided stack and features or defaults
    ;;
esac

# Invoke architect agent
Invoke architecture-planner agent with:
- project_type: $project_type (spa|dashboard|ecommerce|saas|blog|landing)
- stack: $stack
- features: $features
- generate_structure: $generate_structure
```

**Examples:**
```bash
/architect dashboard --preset=enterprise --generate
/architect spa --stack=react,tailwind,zustand
/architect ecommerce --features=cart,checkout,auth
```

---

### `/audit` - Performance & Quality Audit

**Purpose:** Comprehensive audit (replaces /optimize)
**Allowed Tools:** Read, Grep, Glob, Task

```markdown
---
description: Audit performance and quality
allowed-tools: Read, Grep, Glob, Task
---

# Parse arguments
scope="${1:-.}"  # Default to current directory
shift || true
args="$*"

# Extract focus areas
focus="all"  # all|react|styles|bundle|a11y
fix=false
report_only=false

for arg in $args; do
  case $arg in
    --focus=*) focus="${arg#*=}" ;;
    --fix) fix=true ;;
    --report) report_only=true ;;
  esac
done

# Run comprehensive audit
Invoke performance-auditor agent with:
- scope: $scope
- focus: $focus
- fix: $fix
- report_only: $report_only

# Agent will analyze:
- React performance (memo, hooks, re-renders)
- Style optimization (unused CSS, duplicates)
- Bundle size and code splitting
- Accessibility compliance
- SEO and meta tags
```

**Examples:**
```bash
/audit
/audit src/components --focus=react
/audit . --focus=styles --fix
/audit . --focus=a11y --report
```

---

### `/test` - Testing Utilities

**Purpose:** Generate and run tests
**Allowed Tools:** Read, Write, Bash, Task

```markdown
---
description: Testing utilities for components
allowed-tools: Read, Write, Bash, Task
---

# Parse arguments
target="${1:-}"
shift || true
args="$*"

# Extract options
type="unit"  # unit|integration|e2e|visual
generate=false
run=false
coverage=false

for arg in $args; do
  case $arg in
    --type=*) type="${arg#*=}" ;;
    --generate) generate=true ;;
    --run) run=true ;;
    --coverage) coverage=true ;;
  esac
done

# Handle test generation
if [ "$generate" = true ]; then
  Generate tests for $target of type $type
fi

# Handle test execution
if [ "$run" = true ]; then
  Run tests with optional coverage report
fi
```

**Examples:**
```bash
/test UserCard --generate --type=unit
/test . --run --coverage
/test src/components --type=visual --generate
```

---

## Agents (Consolidated)

### 1. `react-generator` - All React Generation

**Purpose:** Generate all React code (components, hooks, tests)
**Tools:** Read, Write, Grep, Glob
**Model:** sonnet

**Capabilities:**
- Generate components with any UI library
- Create custom hooks with proper TypeScript
- Apply chosen styling method
- Include state management
- Generate tests alongside code
- Follow project conventions

**Handles:**
- Component generation (all types)
- Hook generation (all purposes)
- Test generation
- TypeScript interfaces

---

### 2. `style-master` - All Styling Operations

**Purpose:** Handle all style-related operations
**Tools:** Read, Write, Grep, Glob
**Model:** sonnet

**Capabilities:**
- Add styles (Tailwind, CSS, SCSS, CSS-in-JS)
- Convert between styling methods
- Optimize existing styles
- Implement responsive design
- Configure Tailwind
- Manage design tokens

**Handles:**
- Style addition
- Style conversion
- Style optimization
- Responsive patterns
- Theme management

---

### 3. `architecture-planner` - Architecture & Design Systems

**Purpose:** Plan architecture and design systems
**Tools:** Read, Write, Grep, Glob
**Model:** sonnet

**Capabilities:**
- Design project architecture
- Create folder structures
- Setup design systems
- Configure build tools
- Plan state management
- Design routing structure

**Handles:**
- Project scaffolding
- Design system setup
- Architecture documentation
- Tech stack selection

---

### 4. `performance-auditor` - All Optimization & Analysis

**Purpose:** Analyze and optimize performance
**Tools:** Read, Grep, Glob
**Model:** sonnet

**Capabilities:**
- React performance analysis
- Style optimization
- Bundle size analysis
- Accessibility audit
- SEO analysis
- Code quality checks

**Handles:**
- Performance metrics
- Optimization suggestions
- Accessibility compliance
- Bundle analysis
- Code quality reports

---

## Skills (With Clear Triggers)

### `react-guardian` - React Best Practices

```markdown
---
name: react-guardian
description: Enforces React best practices automatically
allowed-tools: Read, Grep, Glob
---

## Auto-invocation Triggers
- **File Patterns:** **/*.tsx, **/*.jsx, **/*.ts (hooks)
- **Tool Usage:** When Write or Edit targets React files
- **Keywords:** component, useState, useEffect, props, render
- **Imports:** Detects React, { useState, useEffect } imports

## Actions
- Validate hooks rules
- Check for missing keys in lists
- Suggest memo optimization
- Flag anti-patterns
- Ensure proper TypeScript types
- Check accessibility props

## Examples
# Triggers on:
- Creating new .tsx file
- Writing "import React from"
- Using useState in code
- Editing component files
```

---

### `style-assistant` - Styling Best Practices

```markdown
---
name: style-assistant
description: Assists with styling decisions and patterns
allowed-tools: Read, Grep
---

## Auto-invocation Triggers
- **File Patterns:** **/*.css, **/*.scss, **/*.module.css
- **Tool Usage:** When adding className or style props
- **Keywords:** className, style, css, tailwind, styled
- **Context:** Style-related commands

## Actions
- Suggest Tailwind utilities
- Recommend CSS custom properties
- Flag hardcoded values
- Suggest responsive patterns
- Optimize specificity

## Examples
# Triggers on:
- Writing className="..."
- Creating .css files
- Using style={{...}}
- Adding Tailwind classes
```

---

### `a11y-watcher` - Accessibility Monitor

```markdown
---
name: a11y-watcher
description: Monitors accessibility compliance
allowed-tools: Read, Grep
---

## Auto-invocation Triggers
- **Elements:** button, input, img, form, nav, main
- **Props:** onClick, onKeyDown, role, aria-*
- **Missing:** alt text, labels, ARIA attributes
- **Context:** Interactive elements

## Actions
- Ensure semantic HTML
- Check ARIA attributes
- Validate keyboard navigation
- Check color contrast
- Suggest focus indicators
- Flag missing alt text

## Examples
# Triggers on:
- <img> without alt
- <button> with div
- onClick without keyboard handler
- Missing form labels
```

---

### `performance-monitor` - Performance Tracking

```markdown
---
name: performance-monitor
description: Monitors performance patterns
allowed-tools: Read, Grep
---

## Auto-invocation Triggers
- **Patterns:** Large components (>200 lines)
- **Imports:** Heavy libraries detected
- **Hooks:** Multiple useState, useEffect in component
- **Arrays:** .map() without key prop
- **Context:** Bundle size concerns

## Actions
- Suggest code splitting
- Recommend lazy loading
- Flag unnecessary re-renders
- Suggest memo usage
- Identify heavy operations
- Recommend virtualization

## Examples
# Triggers on:
- Component >200 lines
- Multiple useEffects
- Large dependency arrays
- Missing React.memo
- Inline function props
```

---

## MCP Servers

**File:** `.mcp.json`

```json
{
  "mcpServers": {
    "shadcn": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-shadcn"],
      "description": "shadcn-ui component integration"
    },
    "javascript-docs": {
      "command": "uvx",
      "args": ["mcp-server-fetch"],
      "env": {
        "ALLOWED_DOMAINS": "developer.mozilla.org,javascript.info"
      },
      "description": "JavaScript documentation"
    },
    "typescript-docs": {
      "command": "uvx",
      "args": ["mcp-server-fetch"],
      "env": {
        "ALLOWED_DOMAINS": "typescriptlang.org,www.typescriptlang.org"
      },
      "description": "TypeScript documentation"
    },
    "react-docs": {
      "command": "uvx",
      "args": ["mcp-server-fetch"],
      "env": {
        "ALLOWED_DOMAINS": "react.dev"
      },
      "description": "React documentation"
    },
    "tailwind-docs": {
      "command": "uvx",
      "args": ["mcp-server-fetch"],
      "env": {
        "ALLOWED_DOMAINS": "tailwindcss.com"
      },
      "description": "Tailwind CSS documentation"
    },
    "css-docs": {
      "command": "uvx",
      "args": ["mcp-server-fetch"],
      "env": {
        "ALLOWED_DOMAINS": "developer.mozilla.org,css-tricks.com,sass-lang.com"
      },
      "description": "CSS/SCSS documentation"
    }
  }
}
```

---

## Files Structure (Simplified)

```
frontend-toolkit/
├── plugin.json                    # Plugin manifest
├── .mcp.json                      # MCP servers
├── hooks.json                     # Git hooks
│
├── commands/                      # 7 streamlined commands
│   ├── component.md
│   ├── hook.md
│   ├── style.md
│   ├── add-ui.md
│   ├── architect.md
│   ├── audit.md
│   └── test.md
│
├── agents/                        # 4 powerful agents
│   ├── react-generator.md
│   ├── style-master.md
│   ├── architecture-planner.md
│   └── performance-auditor.md
│
├── skills/                        # Auto-invoked skills
│   ├── react-guardian.md
│   ├── style-assistant.md
│   ├── a11y-watcher.md
│   └── performance-monitor.md
│
└── templates/                     # Code templates
    ├── components/
    ├── hooks/
    ├── styles/
    └── tests/
```

---

## Usage Examples

### Basic Usage
```bash
# Simple component creation
/component UserCard

# Hook with purpose
/hook useLocalStorage --purpose=storage

# Add UI components
/add-ui shadcn button card

# Run audit
/audit
```

### Intermediate Usage
```bash
# Component with options
/component UserProfile --type=page --ui=shadcn --with-state

# Style conversion
/style . --convert=css-modules→tailwind

# Architecture with preset
/architect dashboard --preset=enterprise
```

### Advanced Usage
```bash
# Full component with tests
/component features/auth/LoginForm --type=form --ui=radix --styles=scss --with-state --memo --test

# Comprehensive audit with fix
/audit src/components --focus=react --fix

# Complete project setup
/architect saas --stack=react,typescript,tailwind,shadcn,zustand --features=auth,api,i18n --generate

# Style optimization pipeline
/style . --convert=css→tailwind && /audit . --focus=styles --fix
```

---

## Key Improvements Summary

### Commands (7 instead of 10)
- ✅ Proper argument parsing with `--flag=value` syntax
- ✅ Smart defaults based on project detection
- ✅ Interactive mode fallbacks
- ✅ Unified `/add-ui` for all UI libraries
- ✅ Single `/audit` replacing multiple optimize commands

### Agents (4 instead of 9)
- ✅ `react-generator` - All React code generation
- ✅ `style-master` - All styling operations
- ✅ `architecture-planner` - Architecture & design systems
- ✅ `performance-auditor` - All optimization & analysis

### Skills (Clear Triggers)
- ✅ File pattern matching
- ✅ Tool usage detection
- ✅ Keyword triggers
- ✅ Import detection
- ✅ Context awareness

### Benefits
- **Simpler UX** - Fewer, more intuitive commands
- **Better DX** - Proper argument parsing with defaults
- **Less Overlap** - Consolidated agents with clear responsibilities
- **Smart Assistance** - Skills with precise trigger conditions
- **Project Awareness** - Auto-detection of conventions

---

## Migration from v1.0

### Command Mapping
```bash
# Old → New
/component [name] [type] → /component name --type=type
/shadcn-add → /add-ui shadcn
/radix-add → /add-ui radix
/optimize → /audit
/frontend-architect → /architect
```

### Agent Consolidation
```
component-generator + hook-generator → react-generator
style-converter + style-optimizer + tailwind-expert → style-master
component-optimizer + style-optimizer → performance-auditor
frontend-architect + design-system-manager → architecture-planner
```

---

## Version

**Version:** 2.0.0
**Status:** Improved Architecture
**License:** MIT