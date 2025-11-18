---
name: markdown-formatter
description: Master markdownlint standards. Use when creating/editing .md files, writing documentation, creating README/CHANGELOG/CONTRIBUTING files, or working with markdown in docs/ directories.
---

# Markdown Formatter Skill

Master markdownlint standards and markdown best practices to ensure consistent, properly formatted documentation across all markdown files.

## When to Use This Skill

Use this skill when:

1. Creating new markdown (.md) files
2. Editing existing documentation
3. Writing README files for projects
4. Creating CHANGELOG.md entries
5. Drafting CONTRIBUTING.md guidelines
6. Writing documentation in docs/ directories
7. Creating wiki pages or documentation sites
8. Formatting comments in markdown syntax
9. Creating GitHub issue/PR templates
10. Writing blog posts in markdown
11. Creating technical specifications
12. Formatting API documentation
13. Creating user guides or tutorials
14. Writing release notes
15. Creating markdown tables or diagrams

## Quick Start

This skill automatically formats markdown as you write:

```markdown
# Before (inconsistent formatting)
##Header with no space
- item 1
* item 2
+  item 3

```python
code without language
```

# After (auto-formatted)
## Header with Space

- item 1
- item 2
- item 3

\`\`\`python
code with language specified
\`\`\`
```

## Auto-Invocation Contexts

This skill is automatically invoked when:
- Creating or editing `.md` files
- Writing documentation in markdown
- Creating README, CHANGELOG, CONTRIBUTING files
- Writing comments in markdown format
- Creating documentation in docs/ directories

## Purpose

Automatically apply consistent markdown formatting following best practices and the project's documentation standards.

## Actions

When auto-invoked, this skill:

1. **Applies Formatting Rules**:
   - Use ATX-style headers (`#` prefix)
   - Consistent list formatting
   - Proper code block formatting with language specifiers
   - Correct table formatting
   - Appropriate link formatting

2. **Ensures Consistency**:
   - Consistent heading hierarchy
   - Uniform list markers
   - Standard spacing
   - Proper emphasis (bold/italic)
   - Link style consistency

3. **Improves Readability**:
   - Add blank lines appropriately
   - Organize content logically
   - Use tables for structured data
   - Break long lines when appropriate

4. **Validates Structure**:
   - Check heading hierarchy (no skipped levels)
   - Validate link syntax
   - Ensure code blocks are closed
   - Check list indentation

## Formatting Rules

### Headers

**✅ Correct (ATX-style):**
```markdown
# H1 Header

## H2 Header

### H3 Header
```

**❌ Avoid (Setext-style):**
```markdown
H1 Header
=========

H2 Header
---------
```

**Rules:**
- Use ATX-style headers (`#`) exclusively
- Add blank line before and after headers
- Don't skip heading levels (h1 → h2 → h3, not h1 → h3)
- Only one h1 per document (the title)
- Space after `#`: `## Header` not `##Header`

### Lists

**Unordered Lists:**
```markdown
- Item 1
- Item 2
  - Nested item 2.1
  - Nested item 2.2
- Item 3
```

**Rules:**
- Use `-` for unordered lists (not `*` or `+`)
- Indent nested lists with 2 spaces
- Add blank line before/after list (unless in nested context)
- Add blank line between items if any item has multiple paragraphs

**Ordered Lists:**
```markdown
1. First item
2. Second item
   1. Nested item
   2. Nested item
3. Third item
```

**Rules:**
- Use `1.` for all items (auto-numbering)
- Indent nested lists with 3 spaces
- Consistent indentation

**Lists with Multiple Paragraphs:**
```markdown
1. First item

   Additional paragraph for first item.

2. Second item

   Additional paragraph for second item.
```

### Code Blocks

**Inline Code:**
```markdown
Use `code` for inline code.
```

**Fenced Code Blocks:**
```markdown
\`\`\`python
def hello():
    print("Hello, World!")
\`\`\`

\`\`\`javascript
function hello() {
  console.log("Hello, World!");
}
\`\`\`
```

**Rules:**
- Always use fenced code blocks (\`\`\`) not indented code blocks
- Always specify language for syntax highlighting
- Use lowercase language identifiers: `python` not `Python`
- Common identifiers: `python`, `javascript`, `typescript`, `bash`, `json`, `yaml`, `sql`, `go`, `rust`, `java`, `csharp`

### Tables

**Well-Formatted:**
```markdown
| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Data 1   | Data 2   | Data 3   |
| Data 4   | Data 5   | Data 6   |
```

**Alignment:**
```markdown
| Left Aligned | Center Aligned | Right Aligned |
|:-------------|:--------------:|--------------:|
| Left         | Center         | Right         |
```

**Rules:**
- Include header row with separator
- Align columns for readability in source
- Add blank line before/after table
- Use `:` in separator for alignment
- Keep tables simple (use nested lists for complex data)

### Links

**Inline Links:**
```markdown
Visit [OpenAI](https://openai.com) for more information.
```

**Reference Links (for repeated URLs):**
```markdown
Check out [Claude Code][cc] and [Claude API][api].

[cc]: https://claude.code
[api]: https://anthropic.com/claude
```

**Auto-Links:**
```markdown
<https://example.com>
```

**Rules:**
- Use descriptive link text (not "click here")
- Use reference links for repeated URLs
- Verify links work before committing
- Use relative paths for internal docs
- Prefer HTTPS over HTTP

### Images

```markdown
![Alt text describing the image](path/to/image.png)

![Logo](./images/logo.png "Optional title")
```

**Rules:**
- Always include alt text
- Use relative paths for local images
- Add descriptive alt text for accessibility
- Include title attribute for tooltips (optional)

### Emphasis

**Bold:**
```markdown
**bold text** or __bold text__
```

**Italic:**
```markdown
*italic text* or _italic text_
```

**Bold and Italic:**
```markdown
***bold and italic*** or ___bold and italic___
```

**Rules:**
- Use `**` for bold (not `__`)
- Use `*` for italic (not `_`)
- Don't use emphasis for formatting (use headers, lists, etc.)

### Horizontal Rules

```markdown
---
```

**Rules:**
- Use `---` for horizontal rules
- Add blank line before and after
- Use sparingly (prefer sections with headers)

### Blockquotes

```markdown
> This is a blockquote.
>
> Multiple paragraphs in quote.

> **Note:** Important information in blockquote.
```

**Rules:**
- Add `>` for each line in quote
- Add blank line between paragraphs in quote
- Useful for notes, warnings, tips

### Spacing

**Blank Lines:**
- Before and after headers
- Before and after lists
- Before and after code blocks
- Before and after tables
- Between sections
- Between paragraphs

**No Extra Spaces:**
- No trailing spaces at end of lines
- No multiple consecutive blank lines
- No spaces in empty lines

### Line Length

- Aim for 80-120 characters per line for readability
- Break long lines in paragraphs naturally
- Don't break URLs or code blocks
- Don't break table formatting

## Common Patterns

### README Structure

```markdown
# Project Name

Brief description.

[![Build](badge)](link) [![Coverage](badge)](link)

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)

## Features

- Feature 1
- Feature 2

## Installation

\`\`\`bash
npm install package-name
\`\`\`

## Usage

\`\`\`javascript
const pkg = require('package-name');
pkg.doSomething();
\`\`\`
```

### API Documentation

```markdown
## `functionName(param1, param2)`

Description of function.

**Parameters:**

| Parameter | Type   | Required | Description        |
|-----------|--------|----------|--------------------|
| param1    | string | Yes      | Description        |
| param2    | number | No       | Description        |

**Returns:** `object` - Description

**Example:**

\`\`\`javascript
const result = functionName('test', 42);
console.log(result);
\`\`\`
```

### Changelog Entry

```markdown
## [1.2.0] - 2024-01-01

### Added
- New feature 1
- New feature 2

### Fixed
- Bug fix 1
- Bug fix 2
```

## Linting Rules

Apply these rules automatically:

1. **MD001** - Heading levels increment by one
2. **MD003** - Use ATX-style headers
3. **MD004** - Use consistent list style (-)
4. **MD005** - No inconsistent indentation in lists
5. **MD007** - Use 2 spaces for unordered list indentation
6. **MD009** - No trailing spaces
7. **MD010** - No hard tabs
8. **MD012** - No multiple consecutive blank lines
9. **MD013** - Line length (soft limit 120 chars)
10. **MD018** - Space after hash in headers
11. **MD022** - Blank lines around headers
12. **MD023** - Headers start at beginning of line
13. **MD025** - Only one top-level header
14. **MD030** - Spaces after list markers
15. **MD031** - Blank lines around fenced code blocks
16. **MD032** - Blank lines around lists
17. **MD040** - Language specified in fenced code blocks
18. **MD047** - File ends with newline

## Auto-Fixes

Automatically fix common issues:

- Convert Setext headers to ATX
- Fix inconsistent list markers
- Add missing language to code blocks
- Remove trailing spaces
- Fix heading hierarchy
- Add missing blank lines
- Align table columns
- Fix link syntax errors

## Real-World Applications

### Technical Documentation Site

**Scenario:** Creating documentation for a software library

```markdown
# Getting Started with MyLibrary

MyLibrary is a powerful tool for data processing.

## Installation

Install via npm:

\`\`\`bash
npm install mylibrary
\`\`\`

## Quick Example

\`\`\`javascript
const MyLibrary = require('mylibrary');

const processor = new MyLibrary({
  mode: 'fast',
  cache: true
});

const result = processor.process(data);
console.log(result);
\`\`\`

## API Reference

### `process(data, options)`

Processes the input data according to specified options.

**Parameters:**

| Name    | Type   | Required | Description                |
|---------|--------|----------|----------------------------|
| data    | object | Yes      | Input data to process      |
| options | object | No       | Processing options         |

**Returns:** Processed data object

## Advanced Usage

For advanced scenarios, see our [guides](./guides/README.md).
```

### Contributing Guide

**Scenario:** Creating CONTRIBUTING.md for open source project

```markdown
# Contributing to Project

Thank you for your interest in contributing!

## Getting Started

1. Fork the repository
2. Clone your fork
3. Create a feature branch
4. Make your changes
5. Submit a pull request

## Development Setup

\`\`\`bash
git clone https://github.com/user/repo.git
cd repo
npm install
npm test
\`\`\`

## Code Style

- Follow ESLint configuration
- Write tests for new features
- Update documentation

## Pull Request Process

1. Update the README.md with details of changes
2. Update the CHANGELOG.md
3. Ensure all tests pass
4. Request review from maintainers

## Code of Conduct

Be respectful and inclusive. See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
```

### Project README

**Scenario:** Comprehensive project README

```markdown
# Awesome Project

A modern web application for task management.

[![Build Status](https://img.shields.io/travis/user/repo)](https://travis-ci.org/user/repo)
[![Coverage](https://img.shields.io/codecov/c/github/user/repo)](https://codecov.io/gh/user/repo)
[![License](https://img.shields.io/github/license/user/repo)](LICENSE)

## Features

- Real-time collaboration
- Cloud synchronization
- Mobile-friendly interface
- Offline support

## Installation

\`\`\`bash
npm install awesome-project
\`\`\`

## Usage

\`\`\`javascript
import { TaskManager } from 'awesome-project';

const manager = new TaskManager();
manager.createTask('Buy groceries');
\`\`\`

## Documentation

See [full documentation](https://docs.example.com).

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT License - see [LICENSE](LICENSE) file.
```

## Quality Checks

Before finalizing markdown:
- [ ] All headers use ATX-style
- [ ] Heading hierarchy is correct (no skipped levels)
- [ ] Lists use consistent markers (-)
- [ ] Code blocks have language specifiers
- [ ] Tables are properly formatted
- [ ] Links are valid
- [ ] Images have alt text
- [ ] No trailing spaces
- [ ] File ends with newline
- [ ] Consistent spacing throughout

## Integration

- Apply formatting as markdown is written
- Suggest fixes for formatting issues
- Auto-format on save (if configured)
- Integrate with markdown linters (markdownlint, remark)

## Best Practices

### Header Structure

**Good:**
```markdown
# Main Title (only one H1)

## Section

### Subsection

#### Detail
```

**Bad:**
```markdown
### Skipped H2

# Multiple H1s in Same File
```

### List Consistency

**Good:** Use consistent markers throughout file
```markdown
- Item 1
- Item 2
  - Sub-item 2.1
  - Sub-item 2.2
- Item 3
```

**Bad:** Mixed markers
```markdown
- Item 1
* Item 2
+ Item 3
```

### Code Block Language

**Good:** Always specify language
```markdown
\`\`\`typescript
const greeting: string = "Hello";
\`\`\`

\`\`\`bash
npm install
\`\`\`
```

**Bad:** No language specified
```markdown
\`\`\`
some code here
\`\`\`
```

### Link Formatting

**Good:**
```markdown
[Descriptive link text](https://example.com)

[Reference-style link][ref-id]

[ref-id]: https://example.com "Optional title"
```

**Bad:**
```markdown
[Click here](https://example.com)
[link](url)  ← No actual URL
```

### Table Alignment

**Good:** Properly aligned
```markdown
| Name    | Status | Count |
|---------|--------|------:|
| Alice   | Active |   150 |
| Bob     | Idle   |    42 |
```

**Bad:** Misaligned or missing separators

## Common Pitfalls

### ❌ Skipping Header Levels

**Problem:**
```markdown
# Title

### Subsection  ← Skipped H2
```

**Solution:** Follow proper hierarchy
```markdown
# Title

## Section

### Subsection
```

### ❌ Inconsistent List Markers

**Problem:** Mixing `-`, `*`, `+` in same document

**Solution:** Choose one marker (prefer `-`) and stick with it:
```markdown
- Item 1
- Item 2
- Item 3
```

### ❌ Missing Code Block Languages

**Problem:**
```markdown
\`\`\`
function example() {}
\`\`\`
```

**Solution:** Always specify language
```markdown
\`\`\`javascript
function example() {}
\`\`\`
```

### ❌ Trailing Whitespace

**Problem:** Invisible spaces at end of lines causing linting errors

**Solution:** Configure editor to remove trailing whitespace automatically or run:
```bash
sed -i 's/[[:space:]]*$//' file.md
```

### ❌ Missing Blank Lines

**Problem:**
```markdown
## Header
Content starts immediately
```

**Solution:** Add blank line after headers
```markdown
## Header

Content starts after blank line
```

### ❌ Invalid Table Formatting

**Problem:**
```markdown
| Name | Status
| Alice | Active
```

**Solution:** Include proper separators
```markdown
| Name  | Status |
|-------|--------|
| Alice | Active |
```

### ❌ Unescaped Special Characters

**Problem:** Using `*`, `_`, `#` without escaping when meant literally

**Solution:** Escape with backslash
```markdown
This is a literal \* asterisk, not emphasis
```

### ❌ Missing Alt Text for Images

**Problem:**
```markdown
![](image.png)
```

**Solution:** Always provide descriptive alt text
```markdown
![Screenshot of the dashboard showing user analytics](image.png)
```

## Related Skills

- **changelog-tracker**: Works with CHANGELOG.md formatting
- **inline-doc-generator**: Generates markdown documentation from code
- **readme-generator**: Creates formatted README files
- **mermaid-diagram-helper**: Adds diagrams to markdown documentation

Follow the standards defined in `DOCUMENTATION_STANDARDS.md`.
