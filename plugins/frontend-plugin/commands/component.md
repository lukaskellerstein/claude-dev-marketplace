---
description: Generate React component with best practices
allowed-tools: Read, Write, Grep, Glob, Task
---

# Generate React Component

Parse arguments from $ARGUMENTS

## Argument Parsing
```bash
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
```

## Interactive Mode
If no component name provided, ask user for:
- Component name (required)
- Component type: basic, form, page, layout, card
- UI library: shadcn, radix, headless, none
- Styling method: tailwind, css-modules, scss, styled-components
- Additional options: state, memo, tests

## Project Convention Detection
Use Grep to detect existing patterns:
- Check for TypeScript (.tsx) or JavaScript (.jsx) usage
- Detect current UI library (shadcn, radix, etc.)
- Identify styling approach in use
- Find component directory structure

## Generate Component
Invoke react-generator agent with collected parameters:
- name: Component name
- type: Component type (basic|form|page|layout|card)
- ui_lib: UI library preference
- styles: Styling method
- with_state: Include useState hook
- with_memo: Wrap with React.memo
- with_test: Generate test file

## Output
- Component file at appropriate location
- Style file if needed (CSS/SCSS modules)
- Test file if requested
- Export in index.ts if present