---
name: markdown-formatter
description: Apply consistent markdown formatting following best practices
---

# Markdown Formatter Skill

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

Follow the standards defined in `DOCUMENTATION_STANDARDS.md`.
