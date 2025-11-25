---
description: Update CHANGELOG.md with recent changes, following Keep a Changelog format and Semantic Versioning
---

Update or create CHANGELOG.md with recent changes, properly categorized and formatted.

## Process

Follow these steps:

1. **Analyze Changes**: Review recent modifications
   - Get git commits since last release (if git available)
   - Review merged pull requests
   - Check for breaking changes
   - Identify new features
   - List bug fixes
   - Note security updates

2. **Launch Changelog Maintainer**: Use the `documentation-plugin:changelog-maintainer` agent to:
   - Parse and categorize changes
   - Determine appropriate version bump (major/minor/patch)
   - Format changes according to Keep a Changelog
   - Write clear, user-focused descriptions
   - Add dates and version numbers
   - Include links to commits/PRs
   - Generate version comparison links

3. **Version Determination**: Calculate next version using Semantic Versioning:
   - **MAJOR**: Breaking changes, removed features
   - **MINOR**: New features (backward compatible)
   - **PATCH**: Bug fixes, security patches
   - Consider pre-release tags (alpha, beta, rc) if needed

4. **Review**: Ensure changelog entry is:
   - Accurate and complete
   - User-focused (not technical details)
   - Properly categorized
   - Well-formatted
   - Includes migration notes for breaking changes

## Output

Present an updated CHANGELOG.md including:

### For New Release
```markdown
## [X.Y.Z] - YYYY-MM-DD

### Added
- New feature descriptions with context
- Links to relevant PRs/issues

### Changed
- Changes to existing functionality
- Performance improvements
- Updated dependencies

### Deprecated
- Features marked for removal
- Migration paths provided

### Removed
- Removed features
- Breaking changes clearly marked

### Fixed
- Bug fixes with context
- Links to issues

### Security
- Security fixes (without exposing vulnerabilities)
- CVE numbers if applicable
```

### For Unreleased Changes
```markdown
## [Unreleased]

### Added
- Changes staged for next release

### Changed
- Modifications not yet released

### Fixed
- Bug fixes pending release
```

## Usage Scenarios

### Update with Recent Changes
```
/update-changelog

Add entries for the last 2 weeks of changes, determining
appropriate version bump based on change types
```

### Create Release Entry
```
/update-changelog

Move unreleased changes to a new version 2.1.0 entry
dated today, and create fresh Unreleased section
```

### Add Specific Change
```
/update-changelog

Add a security fix to the unreleased section:
Fixed SQL injection vulnerability in search endpoint
```

### Create Initial Changelog
```
/update-changelog

Create new CHANGELOG.md file with current version
and set up structure for future updates
```

## Change Categories

### Added
New features and capabilities:
- New API endpoints or functions
- New configuration options
- New integrations
- New documentation
- New platform support

### Changed
Modifications to existing functionality:
- Behavior changes
- Performance improvements
- Refactored APIs (backward compatible)
- Updated dependencies
- UI/UX improvements

### Deprecated
Features scheduled for removal:
- Mark deprecated APIs
- Provide migration paths
- Set sunset timeline
- Recommend alternatives

### Removed
Removed features (breaking changes):
- Deleted endpoints
- Removed configuration options
- Discontinued features
- Dropped platform support

### Fixed
Bug fixes and corrections:
- Fixed crashes or errors
- Corrected calculations
- Resolved race conditions
- Fixed memory leaks
- Documentation corrections

### Security
Security-related changes:
- Vulnerability fixes
- Authentication improvements
- Encryption updates
- Dependency security patches
- Security best practices

## Version Bump Guidelines

### Major Version (X.0.0)
When you have:
- Breaking API changes
- Removed features
- Incompatible changes
- Major architectural changes

### Minor Version (0.X.0)
When you have:
- New features (backward compatible)
- Deprecations
- Substantial improvements
- New APIs

### Patch Version (0.0.X)
When you have:
- Bug fixes only
- Security patches
- Documentation fixes
- Minor improvements

### Pre-release (0.0.0-alpha/beta/rc)
For testing releases:
- Alpha: Early development
- Beta: Feature complete, testing
- RC: Release candidate

## Best Practices Applied

- **Keep a Changelog Format**: Follow keepachangelog.com standard
- **Semantic Versioning**: Follow semver.org rules
- **User-Focused**: Write for users, not developers
- **Specificity**: Be specific about what changed
- **Context**: Include why changes were made
- **Links**: Reference issues and PRs
- **Breaking Changes**: Clearly mark with BREAKING
- **Migration Guides**: Provide for breaking changes
- **Date Format**: Use ISO 8601 (YYYY-MM-DD)
- **Consistency**: Maintain format across entries

## Breaking Change Handling

When adding breaking changes:

1. **Mark Clearly**: Use **BREAKING** prefix
2. **Explain Impact**: What will break?
3. **Provide Migration**: How to update?
4. **Timeline**: When will it take effect?
5. **Examples**: Show before/after code

Example:
```markdown
### Changed
- **BREAKING**: Authentication now requires OAuth2 instead of API keys
  - Existing API keys will stop working after 2025-03-01
  - Migration guide: docs/migration/oauth2.md
  - See examples/auth-migration for code samples
```

## Git Integration

When git is available:

1. **Collect Commits**: Since last tag/release
2. **Parse Conventional Commits**: If using conventional commit format
3. **Group Changes**: By category
4. **Generate Entries**: From commit messages
5. **Enhance**: Add context and links

Conventional commit mapping:
- `feat:` → Added
- `fix:` → Fixed
- `perf:` → Changed
- `security:` → Security
- `BREAKING CHANGE:` → Removed/Changed (major)

## Quality Checklist

Before finalizing:
- [ ] All user-facing changes are documented
- [ ] Changes are properly categorized
- [ ] Version number follows semantic versioning
- [ ] Breaking changes are clearly marked
- [ ] Migration guides provided for breaking changes
- [ ] Dates are in ISO 8601 format (YYYY-MM-DD)
- [ ] Links to commits/PRs are included
- [ ] Format follows Keep a Changelog standard
- [ ] Language is user-focused and clear
- [ ] Security fixes don't expose vulnerabilities

Provide a complete, properly formatted CHANGELOG.md entry ready to commit.
