---
description: Add UI library components
---

# Add UI Library Components

Parse arguments from $ARGUMENTS

## Argument Parsing
```bash
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
```

## Interactive Mode
If no components specified:
- Show list of available components for selected library
- Allow multi-select from component list
- Show installation preview

## Library-Specific Installation

### shadcn-ui
```bash
npx shadcn-ui@latest add $components
```
- Automatically configures Tailwind
- Creates components in components/ui
- Handles dependencies

### Radix UI
```bash
npm install @radix-ui/react-$component
```
- Install headless components
- Generate wrapper with basic styling
- Create TypeScript interfaces

### Material-UI (mui)
```bash
npm install @mui/material @emotion/react @emotion/styled
```
- Install MUI components
- Setup theme provider if needed

### Chakra UI
```bash
npm install @chakra-ui/react @emotion/react @emotion/styled
```
- Install Chakra components
- Setup ChakraProvider

### Ant Design
```bash
npm install antd
```
- Install Ant Design
- Configure CSS imports

## Output
- Installed packages
- Generated component files
- Usage examples
- Import statements