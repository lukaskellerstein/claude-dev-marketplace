---
description: Generate or update CHANGELOG.md
---

# Generate or Update CHANGELOG.md

Generate changelog: $ARGUMENTS

## Arguments

- **version** (optional): Version number (e.g., `1.2.0`) or `auto` (default)
- **range** (optional): Git range (e.g., `v1.0.0..HEAD`, `last-release..HEAD`) or `auto` (default)

## Examples

- `/changelog` - Since last release with auto-versioning
- `/changelog 2.0.0` - For version 2.0.0
- `/changelog auto v1.0.0..HEAD` - Specific range with auto-versioning
- `/changelog 1.5.0 last-release..HEAD` - Version 1.5.0 since last release

## Task

You are tasked with generating or updating the CHANGELOG.md file for the current project.

### Argument Parsing

Parse $ARGUMENTS to extract:
1. **Version** (first argument) - defaults to `auto` if not provided
2. **Git range** (second argument) - defaults to `auto` (last release to HEAD) if not provided

### Version Handling

- **auto**: Analyze commits and suggest version bump based on Semantic Versioning
- **Specific version** (e.g., `2.0.0`): Use provided version number

### Range Handling

- **auto**: Automatically detect last release tag and use `last-tag..HEAD`
- **Specific range** (e.g., `v1.0.0..HEAD`): Use provided git range
- **last-release..HEAD**: From most recent release to current HEAD

## Analysis Steps

1. **Check for Existing Changelog**:
   - Look for CHANGELOG.md or CHANGELOG in project root
   - Determine the last documented version
   - Identify the format used (if any)

2. **Analyze Git History**:
   - Get commits in specified range
   - If no releases exist, analyze all commits
   - Group commits by type (feat, fix, docs, etc.)
   - Identify breaking changes

3. **Determine Version Impact**:
   - Identify if changes are breaking (MAJOR)
   - Identify new features (MINOR)
   - Identify bug fixes (PATCH)
   - Suggest next version number using Semantic Versioning

## Changelog Format

Follow [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) format as defined in `DOCUMENTATION_STANDARDS.md`:

### Structure

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- New features

### Changed
- Changes in existing functionality

### Deprecated
- Soon-to-be removed features

### Removed
- Removed features

### Fixed
- Bug fixes

### Security
- Security vulnerability fixes

## [1.0.0] - YYYY-MM-DD

...
```

## Change Categories

Categorize changes into:

1. **Added**: New features, new capabilities
2. **Changed**: Changes to existing functionality
3. **Deprecated**: Soon-to-be removed features (with timeline)
4. **Removed**: Removed features (breaking)
5. **Fixed**: Bug fixes
6. **Security**: Security vulnerability fixes (critical)

## Commit Analysis

Parse commit messages following Conventional Commits format:

- `feat:` → Added
- `fix:` → Fixed
- `docs:` → (mention in Added/Changed if significant)
- `style:` → (usually omit from changelog)
- `refactor:` → Changed (if user-facing)
- `perf:` → Changed or Added (performance improvements)
- `test:` → (usually omit from changelog)
- `chore:` → (usually omit from changelog)
- `BREAKING CHANGE:` → Note in header, likely Removed or Changed

## Version Recommendation

Based on changes since last release, recommend version bump:

- **MAJOR** (X.0.0): Breaking changes, removed features
- **MINOR** (0.X.0): New features, new APIs (backward compatible)
- **PATCH** (0.0.X): Bug fixes, documentation (backward compatible)

## Release Notes Generation

For the current release, also generate release notes that include:

1. Version number and date
2. Summary of major changes
3. Breaking changes (if any)
4. Migration guide (if breaking changes)
5. Full changelog
6. Contributors (if available)

## Best Practices

- Keep entries concise but descriptive
- Link to issues/PRs when available
- Mention breaking changes prominently
- Group related changes together
- Use consistent language and terminology
- Date format: YYYY-MM-DD
- List most recent changes first

## Output

Generate or update CHANGELOG.md with:

1. Header with format reference
2. [Unreleased] section (always present)
3. Version sections in reverse chronological order
4. Proper categorization of changes
5. Links to compare versions (if git repository)

## Example

```markdown
## [Unreleased]

### Added
- New `/api/users` endpoint for user management
- Support for environment-based configuration

### Fixed
- Fixed memory leak in connection pool (#123)
- Corrected timezone handling in date parsing

## [1.2.0] - 2024-01-15

### Added
- GraphQL API support
- Real-time notifications via WebSocket

### Changed
- Improved error messages for validation failures
- Updated dependencies to latest versions

### Fixed
- Fixed race condition in cache invalidation

## [1.1.0] - 2024-01-01

...
```

Generate or update CHANGELOG.md in the project root.
