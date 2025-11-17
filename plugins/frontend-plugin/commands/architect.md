---
description: Design complete frontend architecture
allowed-tools: Read, Write, Grep, Glob, Task
---

# Frontend Architecture Design

Parse arguments from $ARGUMENTS

## Argument Parsing
```bash
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
```

## Presets

### Enterprise
- Stack: React, TypeScript, Tailwind, shadcn-ui, Zustand, React Router
- Features: Auth, API, State, Routing, i18n, Testing
- Structure: Feature-based architecture

### Minimal
- Stack: React, TypeScript, Tailwind
- Features: Routing
- Structure: Simple component organization

### Custom
Use provided stack and features parameters

## Project Types
- **spa**: Single Page Application
- **dashboard**: Admin/Analytics Dashboard
- **ecommerce**: E-commerce Platform
- **saas**: SaaS Application
- **blog**: Blog/Content Site
- **landing**: Landing Page

## Invoke Agent
Call architecture-planner agent with:
- project_type: Selected project type
- stack: Technology stack (comma-separated)
- features: Required features (comma-separated)
- generate_structure: Create folder structure

## Generated Output

### Architecture Document
- Technology stack overview
- Folder structure design
- Component hierarchy
- State management strategy
- Routing architecture
- API integration patterns
- Testing approach
- Build configuration

### Folder Structure (if --generate)
```
src/
├── features/         # Feature modules
├── components/       # Shared components
├── hooks/           # Custom hooks
├── services/        # API services
├── store/           # State management
├── styles/          # Global styles
├── types/           # TypeScript types
├── utils/           # Utilities
└── config/          # Configuration
```

### Configuration Files
- package.json with dependencies
- tsconfig.json for TypeScript
- tailwind.config.js for Tailwind
- vite.config.js or webpack.config.js
- .eslintrc.js and .prettierrc