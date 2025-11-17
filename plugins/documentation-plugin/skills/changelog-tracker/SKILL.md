---
name: changelog-tracker
description: Track changes and suggest changelog entries following Keep a Changelog format
---

# Changelog Tracker Skill

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

Follow the Keep a Changelog format defined in `DOCUMENTATION_STANDARDS.md`.
