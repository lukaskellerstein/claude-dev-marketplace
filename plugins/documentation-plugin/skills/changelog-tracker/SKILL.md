---
name: changelog-tracker
description: Master Keep a Changelog format. Use when making code changes, adding features, fixing bugs, updating dependencies, making breaking changes, creating commits, or preparing releases.
---

# Changelog Tracker Skill

Master the Keep a Changelog format and Semantic Versioning principles to automatically track changes and suggest appropriate changelog entries for all code modifications.

## When to Use This Skill

Use this skill when:

1. Adding new features or capabilities to the codebase
2. Fixing bugs or resolving issues
3. Making breaking changes to APIs or interfaces
4. Updating dependencies or third-party libraries
5. Deprecating existing functionality
6. Removing features or capabilities
7. Addressing security vulnerabilities
8. Before committing changes to version control
9. Creating or reviewing pull requests
10. Preparing for a new release
11. Refactoring code with user-facing impacts
12. Improving performance significantly
13. Updating configuration file formats
14. Changing default behavior
15. Documenting changes for team communication

## Quick Start

This skill automatically activates when code changes are detected. It analyzes your changes and suggests appropriate changelog entries:

```bash
# After making changes, the skill suggests:
📝 Suggested Changelog Entry:

### Added
- GraphQL API support with queries, mutations, and subscriptions
- Export functionality for CSV and JSON formats

📊 Version Impact: MINOR (1.2.0 → 1.3.0)

Add to CHANGELOG.md under [Unreleased] section.
```

## Auto-Invocation Contexts

This skill is automatically invoked when:
- Making significant code changes
- Adding new features
- Fixing bugs
- Updating dependencies
- Making breaking changes
- Before committing changes
- Creating pull requests

## Purpose

Automatically track changes and suggest appropriate changelog entries following Keep a Changelog format and Semantic Versioning principles.

## Actions

When auto-invoked, this skill:

1. **Analyzes Changes**:
   - Identify type of change (feature, fix, breaking change, etc.)
   - Determine user-facing impact
   - Assess version impact (major, minor, patch)
   - Detect breaking changes

2. **Suggests Changelog Entry**:
   - Generate appropriate changelog entry
   - Categorize change correctly
   - Write clear, user-focused description
   - Recommend version bump

3. **Tracks Breaking Changes**:
   - Identify API changes
   - Detect removed features
   - Flag incompatible changes
   - Suggest migration notes

4. **Maintains Format**:
   - Follow Keep a Changelog format
   - Maintain consistent structure
   - Use proper markdown
   - Keep entries concise

## Change Categories

### Added
New features or capabilities added to the project.

**Trigger patterns:**
- New functions, classes, or modules
- New API endpoints
- New configuration options
- New CLI commands
- New exports from libraries

**Example entries:**
```markdown
### Added
- New `/api/users` endpoint for user management
- Support for environment-based configuration via `.env` files
- `--verbose` flag for detailed logging output
- GraphQL API support alongside REST API
```

### Changed
Changes to existing functionality that don't break backward compatibility.

**Trigger patterns:**
- Performance improvements
- Refactoring (if user-facing behavior changes)
- UI/UX improvements
- Enhanced error messages
- Updated documentation

**Example entries:**
```markdown
### Changed
- Improved error messages for validation failures
- Updated default timeout from 30s to 60s
- Enhanced performance of search functionality (30% faster)
- Simplified configuration file format (old format still supported)
```

### Deprecated
Features that will be removed in future versions.

**Trigger patterns:**
- `@deprecated` annotations
- Comments mentioning deprecation
- Adding replacement for existing feature

**Example entries:**
```markdown
### Deprecated
- `getUserById()` function (use `getUser()` instead)
- `/api/v1/users` endpoint (migrate to `/api/v2/users`)
- `--old-format` flag will be removed in v3.0.0
```

### Removed
Features removed from the project (breaking change).

**Trigger patterns:**
- Deleted functions, classes, modules
- Removed API endpoints
- Removed configuration options
- Removed CLI commands

**Example entries:**
```markdown
### Removed
- Support for Node.js 14 (now requires Node.js 18+)
- Deprecated `/api/v1/users` endpoint (use `/api/v2/users`)
- `--legacy-mode` flag (no longer needed)
```

### Fixed
Bug fixes that resolve incorrect behavior.

**Trigger patterns:**
- Commits mentioning "fix", "bug", "issue"
- Closed issue references
- Error handling improvements

**Example entries:**
```markdown
### Fixed
- Fixed memory leak in connection pool (#123)
- Corrected timezone handling in date parsing
- Fixed race condition in cache invalidation
- Resolved issue where CSV export failed for large datasets
```

### Security
Security vulnerability fixes (critical).

**Trigger patterns:**
- Security-related commits
- Dependency updates addressing CVEs
- Authentication/authorization fixes

**Example entries:**
```markdown
### Security
- Fixed SQL injection vulnerability in search endpoint (CVE-2024-1234)
- Updated `lodash` to address prototype pollution vulnerability
- Improved input validation to prevent XSS attacks
```

## Semantic Versioning Recommendations

### MAJOR (X.0.0) - Breaking Changes

**Triggers:**
- Removed features or functions
- Changed function signatures
- Renamed exports
- Changed configuration format (without backward compatibility)
- Removed API endpoints
- Changed default behavior that breaks existing usage
- Dropped support for platform/language version

**Recommendation format:**
```
Breaking changes detected:
- Removed getUserById() function
- Changed User model schema

Recommended version bump: MAJOR (2.0.0 → 3.0.0)
```

### MINOR (0.X.0) - New Features

**Triggers:**
- New features added
- New API endpoints
- New functions/classes
- New CLI commands
- Deprecated features (not removed)
- Performance improvements (significant)

**Recommendation format:**
```
New features detected:
- Added GraphQL API support
- New --export flag for CLI

Recommended version bump: MINOR (2.3.0 → 2.4.0)
```

### PATCH (0.0.X) - Bug Fixes

**Triggers:**
- Bug fixes
- Documentation updates
- Performance improvements (minor)
- Dependency updates (no new features)
- Refactoring (no behavior change)

**Recommendation format:**
```
Bug fixes detected:
- Fixed memory leak in connection pool
- Corrected date parsing issue

Recommended version bump: PATCH (2.3.1 → 2.3.2)
```

## Changelog Entry Generation

### Format Template

```markdown
## [Unreleased]

### Added
- Description of new feature [#PR_NUMBER]
- Another new feature

### Changed
- Description of change
- Another change

### Fixed
- Bug fix description [#ISSUE_NUMBER]
- Another bug fix
```

### Entry Guidelines

**Good entries:**
```markdown
### Added
- New `/api/v2/export` endpoint for bulk data export
- Support for MySQL database alongside PostgreSQL
- `--quiet` flag to suppress all non-error output
```

**Bad entries:**
```markdown
### Added
- Add new endpoint
- Support stuff
- Flag
```

**Rules for good entries:**
- Start with action verb
- Be specific and descriptive
- Include context (what, where, why if not obvious)
- Reference issues/PRs when relevant
- Focus on user impact, not implementation details
- Keep entries concise (one line preferred)

## Detecting Breaking Changes

### Automatic Detection

Look for:
```python
# Function signature changes
- def get_user(id: str) → Optional[User]:
+ def get_user(user_id: str, include_details: bool = False) → User:
```

```typescript
// Removed exports
- export function oldFunction(): void;
```

```yaml
# Changed configuration structure
- database_url: string
+ database:
+   host: string
+   port: number
```

### Warning Messages

```
⚠️ BREAKING CHANGE DETECTED:
- Function signature changed: get_user()
  • Parameter 'id' renamed to 'user_id'
  • New required parameter 'include_details' added

This is a MAJOR version change.
Consider:
1. Maintain backward compatibility with overloading
2. Add migration guide to CHANGELOG
3. Update version to 3.0.0
```

## Integration with Commits

### Conventional Commits

Parse commit messages following Conventional Commits:

```
feat: add user export functionality
^     ^
|     |
|     +-> Subject
+-> Type (maps to category)
```

**Type mapping:**
- `feat:` → Added
- `fix:` → Fixed
- `docs:` → (mention in Added/Changed if significant)
- `style:` → (usually omit from changelog)
- `refactor:` → Changed (if user-facing)
- `perf:` → Changed or Added
- `test:` → (usually omit from changelog)
- `chore:` → (usually omit from changelog)
- `BREAKING CHANGE:` → Removed or Changed (note in header)

### Auto-Generate from Commits

```bash
# Generate changelog entries from commits
$ git log v1.2.0..HEAD --oneline

abc123 feat: add GraphQL support
def456 fix: correct date parsing
ghi789 feat: add export command
```

**Generated entry:**
```markdown
## [Unreleased]

### Added
- GraphQL support (abc123)
- Export command for data extraction (ghi789)

### Fixed
- Corrected date parsing in timezone conversion (def456)
```

## Workflow Integration

### Pre-Commit Hook

Before committing, suggest changelog entry:

```
Changes detected:
- New file: src/api/graphql.ts
- Modified: package.json (new dependency: apollo-server)

Suggested changelog entry:
### Added
- GraphQL API support alongside REST API

Add this to CHANGELOG.md? [Y/n]
```

### Pull Request Template

Auto-populate PR description with changelog entry:

```markdown
## Changes

### Added
- GraphQL API support

## Changelog Entry

\`\`\`markdown
### Added
- GraphQL API support with queries and mutations
\`\`\`

## Version Impact
- [ ] MAJOR (breaking change)
- [x] MINOR (new feature)
- [ ] PATCH (bug fix)
```

## Real-World Applications

### Microservice Release

**Scenario:** Releasing a new version of a payment processing microservice

```markdown
## [2.0.0] - 2024-01-15

### Added
- Support for Apple Pay and Google Pay payment methods
- Webhook retry mechanism with exponential backoff
- Real-time payment status notifications

### Changed
- Improved error handling with more specific error codes
- Enhanced logging for payment transaction tracking

### Fixed
- Race condition in concurrent payment processing
- Incorrect tax calculation for international transactions

### Security
- Updated payment gateway SDK to address CVE-2024-1234
- Implemented rate limiting for payment API endpoints
```

### Library Update

**Scenario:** Publishing a new version of a JavaScript utility library

```markdown
## [1.5.0] - 2024-01-15

### Added
- `deepMerge()` utility for nested object merging
- TypeScript type definitions for all functions
- Tree-shaking support for smaller bundle sizes

### Changed
- Improved performance of `debounce()` by 40%
- Updated error messages to be more descriptive

### Deprecated
- `merge()` function (use `deepMerge()` instead, will be removed in v2.0.0)
```

### API Version Update

**Scenario:** Releasing a new API version with breaking changes

```markdown
## [3.0.0] - 2024-01-15

### Added
- GraphQL API support alongside REST
- Pagination support for all list endpoints
- Filtering and sorting capabilities

### Changed
- All timestamps now use ISO 8601 format instead of Unix timestamps
- Error responses now include correlation IDs for debugging

### Removed
- `/api/v1/*` endpoints (use `/api/v3/*` instead)
- Support for API keys (use OAuth 2.0 tokens instead)
- XML response format (JSON only)

### Migration Guide
See MIGRATION.md for detailed upgrade instructions from v2.x to v3.x
```

## Best Practices

### Entry Quality

**Good:**
- "Added support for MySQL databases"
- "Fixed memory leak in WebSocket connection handler"
- "Improved search performance by 40%"
- "Deprecated `oldApi()` in favor of `newApi()`"

**Bad:**
- "Added stuff"
- "Fixed bug"
- "Updated code"
- "Changes"

### User Focus

Write from user perspective:
- ✅ "Added dark mode support"
- ❌ "Implemented ThemeProvider component"

- ✅ "Fixed login failure with special characters in password"
- ❌ "Fixed regex pattern in auth validation"

### Conciseness

One line per entry when possible:
```markdown
### Added
- User profile customization
- Export to CSV/JSON formats
- Real-time notifications

### Fixed
- Duplicate entries in search results
- Incorrect pagination on mobile
```

## Quality Checks

Before suggesting entry:
- [ ] Change is user-facing (not internal refactoring)
- [ ] Description is clear and specific
- [ ] Correct category (Added/Changed/Fixed/etc.)
- [ ] Version impact is assessed
- [ ] Breaking changes are flagged
- [ ] Entry follows markdown formatting
- [ ] Grammar and spelling are correct

## Output

Suggest changelog entries in this format:

```markdown
📝 Suggested Changelog Entry:

### Added
- GraphQL API support with queries, mutations, and subscriptions
- Export functionality for CSV and JSON formats

📊 Version Impact: MINOR (1.2.0 → 1.3.0)

Add to CHANGELOG.md under [Unreleased] section.
```

## Common Pitfalls

### ❌ Documenting Internal Changes

**Problem:**
```markdown
### Changed
- Refactored UserService class hierarchy
- Moved utility functions to separate module
- Updated import statements
```

**Solution:** Only document user-facing changes
```markdown
### Changed
- Improved user profile loading speed by 40%
```

### ❌ Vague Descriptions

**Problem:**
```markdown
### Fixed
- Fixed bug
- Updated stuff
- Improved things
```

**Solution:** Be specific
```markdown
### Fixed
- Corrected timezone handling in date picker
- Resolved memory leak in WebSocket connections
- Fixed validation error with international phone numbers
```

### ❌ Wrong Categories

**Problem:**
```markdown
### Changed
- Added GraphQL support  ← Should be "Added"
```

**Solution:** Use correct category
```markdown
### Added
- GraphQL API support alongside REST
```

### ❌ Missing Breaking Change Warnings

**Problem:**
```markdown
### Changed
- Updated authentication to use OAuth 2.0 only
```

**Solution:** Flag breaking changes prominently
```markdown
### Removed
- **BREAKING:** API key authentication (use OAuth 2.0 instead)
```

### ❌ Including Every Commit

**Problem:** Creating changelog entry for every minor commit or internal change

**Solution:** Group related changes and focus on user impact:
```markdown
### Added
- Comprehensive user export functionality (CSV, JSON, Excel formats)
  (Instead of listing 10 commits for each format and fix)
```

### ❌ Incorrect Version Impact

**Problem:** Marking new feature as PATCH or bug fix as MAJOR

**Solution:** Follow semantic versioning strictly:
- **MAJOR**: Breaking changes, removed features
- **MINOR**: New features, new deprecations
- **PATCH**: Bug fixes, security patches

### ❌ Poor Timing

**Problem:** Adding changelog entries after release or forgetting entirely

**Solution:** Make it part of development workflow:
- Add entry with each PR
- Review during code review
- Verify before release

## Related Skills

- **markdown-formatter**: Ensures changelog entries follow proper markdown formatting
- **inline-doc-generator**: Documents code changes that trigger changelog entries
- **git-commit-helper**: Coordinates with conventional commit messages
- **release-notes-generator**: Expands changelog entries into detailed release notes

Follow the Keep a Changelog format defined in `DOCUMENTATION_STANDARDS.md`.
