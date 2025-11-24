---
name: documentation-standards
description: Auto-invoked when writing or reviewing documentation to ensure best practices and consistency
allowed-tools: Read, Grep, Glob
---

# Documentation Standards and Best Practices

This skill provides guidance on documentation standards across all types of documentation to ensure consistency, clarity, and quality.

## When Active

This skill activates when you:
- Write or generate documentation
- Review or update documentation
- Create README, CHANGELOG, or other .md files
- Write code comments or docstrings
- Create API documentation
- Generate architecture documentation

## Markdown Best Practices

### Headings

Use ATX-style headings (# syntax):
```markdown
# H1 - Document title (one per document)
## H2 - Main sections
### H3 - Subsections
#### H4 - Sub-subsections
```

Rules:
- One H1 per document (document title)
- Don't skip heading levels (no H1 → H4)
- Use sentence case for headings
- No period at end of headings
- Add blank line before and after headings

### Lists

**Unordered lists:**
```markdown
- Use hyphens for bullets
- Be consistent with bullet character
- Add space after bullet
- Use parallel structure
```

**Ordered lists:**
```markdown
1. Use numbers followed by period
2. Start with 1 for each list
3. Let markdown auto-number if desired
```

**Nested lists:**
```markdown
- Parent item
  - Child item (2 spaces indent)
  - Another child
    - Grandchild (4 spaces indent)
```

### Links

**Inline links (preferred for readability):**
```markdown
See the [documentation](https://example.com/docs) for details.
```

**Reference links (for repeated URLs):**
```markdown
Check out [Project A][a] and [Project B][a].

[a]: https://example.com
```

**Anchor links (internal navigation):**
```markdown
Jump to [Installation](#installation) section.
```

Rules:
- Use descriptive link text (not "click here")
- Verify links work
- Use HTTPS when available
- Consider using reference links for long URLs

### Code Blocks

**Inline code:**
```markdown
Use `code` for commands, variables, and short snippets.
```

**Fenced code blocks:**
````markdown
```javascript
function example() {
  return "Always specify language for syntax highlighting";
}
```
````

Language identifiers:
- `javascript`, `typescript`, `python`, `go`, `rust`
- `bash`, `shell`, `sh`, `zsh`
- `json`, `yaml`, `toml`, `xml`
- `sql`, `graphql`, `proto`
- `markdown`, `html`, `css`

### Tables

```markdown
| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Value 1  | Value 2  | Value 3  |
| Value 4  | Value 5  | Value 6  |
```

Alignment:
```markdown
| Left    | Center  | Right   |
|:--------|:-------:|--------:|
| Left    | Center  | Right   |
```

Rules:
- Include header row
- Use alignment for numbers (right) and text (left)
- Keep tables simple (complex data → link to external file)

### Emphasis

```markdown
*italic* or _italic_
**bold** or __bold__
***bold italic*** or ___bold italic___
```

Rules:
- Use italics for emphasis
- Use bold for strong emphasis
- Don't overuse emphasis
- Be consistent with style choice

### Images

```markdown
![Alt text describing image](path/to/image.png)
![Logo](logo.png "Optional title")
```

Rules:
- Always provide descriptive alt text
- Use relative paths when possible
- Keep images in docs/images/ or similar
- Optimize image sizes

### Blockquotes

```markdown
> Use blockquotes for quotes, notes, or callouts.
> Multiple lines are supported.

> **Note**: Important information
```

### Horizontal Rules

```markdown
Use three or more hyphens, asterisks, or underscores:

---
```

## Writing Style

### Voice and Tone

**Active Voice (Preferred)**
```markdown
Good: "The system validates the input"
Bad:  "The input is validated by the system"

Good: "You can configure the timeout"
Bad:  "The timeout can be configured"
```

**Imperative Mood for Instructions**
```markdown
Good: "Install the package"
Bad:  "You should install the package"

Good: "Run the tests"
Bad:  "The tests should be run"
```

**Present Tense**
```markdown
Good: "The function returns a promise"
Bad:  "The function will return a promise"
```

### Clarity

**Be Concise**
```markdown
Good: "This function validates email addresses"
Bad:  "This function is responsible for performing validation of email addresses"
```

**Be Specific**
```markdown
Good: "Timeout occurs after 30 seconds"
Bad:  "Timeout occurs after a while"
```

**Define Terms**
```markdown
First use: "JSON Web Token (JWT)"
Subsequent: "JWT"
```

### Consistency

**Terminology**
- Choose one term and stick with it
- "username" not "user name" or "user-name"
- "email" not "e-mail" or "Email"

**Capitalization**
- Product names: as specified (GitHub, npm, PostgreSQL)
- Generic terms: lowercase (database, server, api)
- Acronyms: uppercase (API, REST, JSON, SQL)

**Numbers**
```markdown
Good: 1, 2, 10, 100 (use numerals for numbers)
Bad:  one, two, ten, one hundred

Exception: Start of sentence or "zero"
```

## README Standards

### Required Sections

1. **Title and Description**
   - Clear project name
   - One-line description
   - Badges (build, version, license)

2. **Table of Contents** (if README > 200 lines)

3. **Installation**
   - Prerequisites
   - Step-by-step instructions
   - Platform-specific notes

4. **Usage**
   - Quick start example
   - Common use cases
   - Configuration options

5. **Documentation**
   - Link to detailed docs
   - API reference
   - Examples

6. **Contributing**
   - How to contribute
   - Code of conduct
   - Development setup

7. **License**
   - License type
   - Link to LICENSE file

### Optional but Recommended

- **Features**: Highlight key features
- **Screenshots**: Visual examples
- **FAQ**: Common questions
- **Troubleshooting**: Common issues
- **Roadmap**: Future plans
- **Acknowledgments**: Credits

## CHANGELOG Standards

Follow [Keep a Changelog](https://keepachangelog.com):

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2025-01-15

### Added
- New features

### Changed
- Changes to existing functionality

### Deprecated
- Soon-to-be removed features

### Removed
- Removed features

### Fixed
- Bug fixes

### Security
- Security fixes
```

## API Documentation Standards

### Endpoint Documentation

```markdown
### GET /api/users/:id

Get user by ID.

**Parameters**

| Name | Type | Location | Required | Description |
|------|------|----------|----------|-------------|
| id   | string | path   | Yes      | User ID     |
| include | string | query | No    | Related resources |

**Request Example**

```http
GET /api/users/123?include=profile
Authorization: Bearer <token>
```

**Response Example**

```json
{
  "id": "123",
  "name": "John Doe",
  "email": "john@example.com"
}
```

**Status Codes**

- `200 OK`: Success
- `404 Not Found`: User not found
- `401 Unauthorized`: Missing or invalid token
```

### Function Documentation

**JavaScript/TypeScript (JSDoc)**
```javascript
/**
 * Calculate the sum of two numbers.
 *
 * @param {number} a - The first number
 * @param {number} b - The second number
 * @returns {number} The sum of a and b
 * @throws {TypeError} If parameters are not numbers
 *
 * @example
 * add(2, 3); // returns 5
 */
function add(a, b) {
  return a + b;
}
```

**Python (docstring)**
```python
def add(a: int, b: int) -> int:
    """
    Calculate the sum of two numbers.

    Args:
        a: The first number
        b: The second number

    Returns:
        The sum of a and b

    Raises:
        TypeError: If parameters are not integers

    Example:
        >>> add(2, 3)
        5
    """
    return a + b
```

## Architecture Documentation Standards

### ADR Format

Use consistent ADR numbering and format:
- `001-decision-title.md` (zero-padded numbers)
- Follow standard ADR template
- Include status, context, decision, consequences
- Link related ADRs

### Diagram Standards

**Mermaid Diagrams**
- Add titles to diagrams
- Use consistent node naming
- Add comments for complex diagrams
- Label all connections
- Use appropriate diagram type

**Diagram Types by Use Case**
- System overview: `graph TB` or `graph LR`
- Components: `C4Component`
- Sequences: `sequenceDiagram`
- Data model: `erDiagram`
- States: `stateDiagram-v2`

## Code Comment Standards

### Inline Comments

```javascript
// Good: Explain why, not what
// Using cache to avoid repeated API calls
const cached = cache.get(key);

// Bad: Stating the obvious
// Get value from cache
const cached = cache.get(key);
```

### When to Comment

**Do comment:**
- Complex algorithms
- Non-obvious decisions
- Workarounds for bugs
- Performance optimizations
- Public APIs

**Don't comment:**
- Obvious code
- To fix bad code (refactor instead)
- Outdated information
- Commented-out code (use version control)

## Accessibility Standards

### Inclusive Language

**Use:**
- "allowlist" not "whitelist"
- "blocklist" not "blacklist"
- "primary/replica" not "master/slave"
- "placeholder" not "dummy"

### Screen Reader Friendly

- Use descriptive headings
- Provide alt text for images
- Use semantic markup
- Ensure logical reading order
- Test with screen reader if possible

## Quality Checklist

When creating or reviewing documentation:

- [ ] Clear, concise language
- [ ] Active voice used
- [ ] Present tense
- [ ] Proper markdown formatting
- [ ] Code blocks have language tags
- [ ] Links work and use HTTPS
- [ ] Images have alt text
- [ ] Headings are hierarchical
- [ ] Terminology is consistent
- [ ] Examples are tested and working
- [ ] Technical terms are defined
- [ ] Inclusive language used
- [ ] Spelling and grammar checked
- [ ] Table of contents (if needed)
- [ ] Version/date information

## Common Mistakes to Avoid

1. **Missing language tags on code blocks**
2. **Using relative links incorrectly**
3. **Inconsistent heading levels**
4. **Unclear link text** ("click here")
5. **Missing alt text on images**
6. **Passive voice overuse**
7. **Undefined acronyms**
8. **Outdated examples**
9. **Broken links**
10. **Inconsistent terminology**

Use this guidance to ensure all documentation is clear, consistent, and high-quality.
