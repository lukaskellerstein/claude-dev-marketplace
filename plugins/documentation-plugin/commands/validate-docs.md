---
description: Validate documentation for errors and issues
---

# Validate Documentation

Validate all documentation files for errors and quality issues.

## Task

You are tasked with validating all documentation in the project for correctness, completeness, and quality.

## Validation Scope

Validate all documentation files including:
- README.md
- CHANGELOG.md
- CONTRIBUTING.md
- docs/**/*.md
- All markdown files in the repository

## Validation Checks

### 1. Link Validation

**Internal Links:**
- Verify all internal links point to existing files
- Check anchor links (#section) are valid
- Validate relative paths are correct
- Report broken links with severity: ERROR

**External Links:**
- Check external URLs are accessible (HTTP 200)
- Report dead links with severity: WARNING
- Note: External link checking can be time-consuming

Example validation:

```markdown
✗ ERROR: Broken internal link in README.md:25
  Link: [Architecture](./docs/architecture/README.md)
  File not found: ./docs/architecture/README.md

✗ WARNING: Dead external link in CONTRIBUTING.md:45
  Link: https://example.com/old-page
  Status: 404 Not Found
```

### 2. Image Reference Validation

Check all image references:
- Verify image files exist
- Check image paths are correct
- Validate image formats (PNG, JPG, SVG, GIF)
- Report missing images with severity: ERROR

```markdown
✗ ERROR: Missing image in docs/architecture/README.md:12
  Image: ![System Diagram](./diagrams/system.png)
  File not found: docs/architecture/diagrams/system.png
```

### 3. Markdown Syntax Validation

Check for markdown syntax errors:
- Unclosed code blocks
- Malformed tables
- Broken list indentation
- Invalid heading hierarchy
- Missing language in code blocks
- Inconsistent list markers

Use markdownlint rules:
- MD001: Heading levels increment by one
- MD003: Heading style (ATX vs Setext)
- MD004: Unordered list style
- MD007: Unordered list indentation
- MD009: Trailing spaces
- MD010: Hard tabs
- MD012: Multiple consecutive blank lines
- MD013: Line length
- MD022: Blank lines around headings
- MD025: Multiple top-level headings
- MD040: Fenced code blocks should have a language
- MD047: Files should end with a single newline

```markdown
✗ ERROR: Markdown syntax error in README.md:156
  Rule: MD040 (fenced-code-language)
  Message: Fenced code blocks should have a language specified

  156 | ```
  157 | npm install
  158 | ```

✗ WARNING: Markdown style issue in CHANGELOG.md:23
  Rule: MD012 (no-multiple-blanks)
  Message: Multiple consecutive blank lines
```

### 4. Code Example Validation

Validate code examples where possible:
- Check syntax highlighting language is specified
- Verify code examples are properly formatted
- Test bash commands are valid (basic syntax check)
- Report code blocks without language tags

```markdown
⊙ INFO: Code block without language in docs/api/README.md:89
  Suggestion: Add language identifier (bash, javascript, python, etc.)
```

### 5. Version Number Consistency

Check for version numbers across documentation:
- Package version (package.json, pyproject.toml, etc.)
- README badges
- CHANGELOG latest version
- Installation instructions

Report inconsistencies:

```markdown
✗ WARNING: Version mismatch
  package.json: 2.1.0
  README.md badge: 2.0.0
  CHANGELOG.md latest: 2.1.0

  Suggestion: Update README.md badge to version 2.1.0
```

### 6. Format Consistency

Check for consistent formatting:
- Heading style (ATX # vs Setext)
- List markers (-, *, +)
- Code fence style (``` vs ~~~)
- Emphasis style (** vs __)
- Link style (inline vs reference)

### 7. Missing Sections in README

Verify README contains essential sections:
- Project title and description ✓
- Installation instructions
- Usage examples
- Contributing guidelines link
- License information

```markdown
⊙ INFO: Missing recommended section in README.md
  Section: "Contributing"
  Suggestion: Add link to CONTRIBUTING.md
```

### 8. Table of Contents Accuracy

If README has a table of contents:
- Verify all linked sections exist
- Check anchor links are correct
- Ensure TOC is up-to-date

### 9. Cross-Reference Validation

Check cross-references between documents:
- README links to CONTRIBUTING
- README links to CHANGELOG
- Architecture docs link to each other
- API docs reference architecture

### 10. Spelling and Grammar (Basic)

Basic spell-check for common errors:
- Check for common typos
- Verify technical term consistency
- Report obvious grammar issues (optional)

## Severity Levels

- **ERROR**: Must fix (broken links, missing files, syntax errors)
- **WARNING**: Should fix (dead external links, inconsistencies)
- **INFO**: Nice to fix (style suggestions, missing optional sections)

## Validation Report

Generate a comprehensive validation report:

```markdown
# Documentation Validation Report

Generated: 2024-11-16 18:30:00

## Summary

- Files validated: 23
- Errors: 3 ✗
- Warnings: 7 ⚠
- Info: 5 ⊙
- Passed: 15 ✓

## Errors (Must Fix)

### README.md

✗ Line 25: Broken internal link to './docs/architecture/README.md'
✗ Line 156: Missing language in code block (MD040)

### docs/api/endpoints.md

✗ Line 89: Missing image './images/api-flow.png'

## Warnings (Should Fix)

### CHANGELOG.md

⚠ Version mismatch: Latest entry is 2.0.0, but package.json is 2.1.0
⚠ Line 34: External link returns 404: https://oldsite.com/docs

### CONTRIBUTING.md

⚠ Line 45: Dead external link to https://example.com/old-page
⚠ Line 67: Inconsistent list marker (using * instead of -)

## Info (Nice to Fix)

### README.md

⊙ Missing recommended section: "Security Policy"
⊙ Missing recommended section: "Acknowledgments"

### docs/architecture/components.md

⊙ Line 123: Code block without language identifier

## Passed

✓ All internal links valid in CONTRIBUTING.md
✓ All images found in docs/architecture/README.md
✓ No markdown syntax errors in CHANGELOG.md
✓ Version numbers consistent in docs/api/README.md
...

## Recommendations

1. Fix 3 broken internal links
2. Update version numbers in README badges
3. Add language identifiers to code blocks
4. Consider adding Security Policy section
5. Fix external link in CONTRIBUTING.md

## Next Steps

1. Run: `npm run lint:markdown` for automated fixes
2. Manually fix broken links
3. Update version numbers
4. Re-run validation: `/validate-docs`
```

## Auto-Fix Suggestions

For some issues, suggest auto-fixes:

```markdown
✗ ERROR: Broken link in README.md:25
  Current: [Architecture](./docs/architecture/README.md)
  Did you mean: [Architecture](./docs/arch/README.md)? [Y/n]

✗ ERROR: Code block missing language
  Line 156-158 in README.md
  Add language identifier? [bash/javascript/python/other]
```

## Integration with CI/CD

Suggest integration for automated validation:

```yaml
# .github/workflows/docs-validation.yml
name: Validate Documentation

on: [push, pull_request]

jobs:
  validate-docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Validate Documentation
        run: claude /validate-docs
```

## Output

Generate a detailed validation report with:
- Summary statistics
- Errors by severity
- File-by-file breakdown
- Actionable recommendations
- Auto-fix suggestions where applicable
