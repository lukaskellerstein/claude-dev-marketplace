---
description: Generate custom React hook
allowed-tools: Read, Write, Grep, Task
---

# Generate Custom React Hook

Parse arguments from $ARGUMENTS

## Argument Parsing
```bash
name="${1:-}"
shift || true
args="$*"

# Validate and format hook name
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
```

## Interactive Mode
If no hook name provided, ask user for:
- Hook name (must start with 'use')
- Purpose: state, fetch, storage, media-query, animation, form, custom
- Cleanup needed? (for useEffect)
- Generate tests?

## Generate Hook
Invoke react-generator agent with:
- name: Hook name (validated to start with 'use')
- purpose: Hook purpose type
- with_cleanup: Include cleanup in useEffect
- with_test: Generate test file

## Hook Types
- **state**: State management hook
- **fetch**: Data fetching with loading/error states
- **storage**: LocalStorage/SessionStorage hook
- **media-query**: Responsive breakpoint detection
- **animation**: Animation state management
- **form**: Form handling with validation
- **custom**: Custom logic hook

## Output
- Hook file in hooks directory
- TypeScript definitions
- Test file if requested
- Usage documentation comment