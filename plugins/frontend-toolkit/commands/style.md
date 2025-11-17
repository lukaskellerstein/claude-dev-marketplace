---
description: Manage component styles - add, convert, or optimize
allowed-tools: Read, Write, Grep, Glob, Task
---

# Style Management

Parse arguments from $ARGUMENTS

## Argument Parsing
```bash
target="${1:-.}"  # Default to current directory
shift || true
args="$*"

# Extract options
method="tailwind"  # Default styling method
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
```

## Actions

### Add Styles
Invoke style-master agent to add styles:
- Target: File or directory to style
- Method: tailwind, css-modules, scss, styled-components
- Responsive: Add responsive breakpoints

### Convert Styles
Invoke style-master agent to convert between methods:
- From: Source styling method
- To: Target styling method
- Preserve: Custom properties, theme tokens
- Examples:
  - css-modules→tailwind
  - scss→css-modules
  - inline→tailwind

### Optimize Styles
Invoke style-master agent to optimize:
- Remove unused CSS
- Consolidate duplicates
- Optimize specificity
- Convert to utility classes
- Minimize bundle size

## Output
- Updated style files
- Migration report for conversions
- Optimization report with metrics
- Updated component imports