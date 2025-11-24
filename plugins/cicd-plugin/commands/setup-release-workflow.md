---
description: Create automated release workflow with semantic versioning, changelog generation, and artifact publishing
---

Create a comprehensive automated release workflow with version management, changelog generation, and artifact publishing.

## Process

Follow these steps:

1. **Analyze Release Requirements**: Understand versioning needs, release cadence, and artifact types
   - Review project type (library, application, monorepo)
   - Identify release artifacts (npm package, Docker image, binaries)
   - Understand versioning preferences (SemVer, CalVer)
   - Check existing git workflow and branching strategy
   - Review changelog and documentation requirements

2. **Launch Release Manager**: Use the `release-manager` agent to:
   - Design versioning strategy (SemVer recommended)
   - Configure Conventional Commits rules
   - Set up automated changelog generation
   - Design release workflow stages
   - Configure artifact publishing
   - Set up release notes generation
   - Design hotfix procedures

3. **CI/CD Integration**: Use the `github-actions-expert` agent to:
   - Create GitHub Actions release workflow
   - Configure release triggers
   - Set up version bumping automation
   - Implement changelog updates
   - Add artifact publishing steps
   - Configure GitHub Releases

4. **Deployment Integration** (if applicable): Use the `deployment-architect` agent to:
   - Integrate release with deployment
   - Configure environment promotion
   - Add release validation steps

## Output

Present comprehensive release automation including:

### Release Configuration

**Semantic Release Config** (`.releaserc.json`)
```json
{
  "branches": ["main"],
  "plugins": [
    "@semantic-release/commit-analyzer",
    "@semantic-release/release-notes-generator",
    "@semantic-release/changelog",
    "@semantic-release/npm",
    "@semantic-release/github",
    "@semantic-release/git"
  ]
}
```

**Conventional Commits Convention**
- Commit message format specification
- Types that trigger releases (feat, fix, etc.)
- Breaking change detection rules
- Commit validation rules

### Release Workflow

**GitHub Actions** (`.github/workflows/release.yml`)
- Automated version bumping
- Changelog generation from commits
- Git tag creation
- Artifact building and publishing
- GitHub Release creation
- Release notes generation
- Deployment trigger (optional)

### Versioning Strategy
- Semantic Versioning scheme (MAJOR.MINOR.PATCH)
- Pre-release versions (alpha, beta, rc)
- Version bumping rules based on commits
- Git tag naming convention
- Branch-based versioning (if needed)

### Changelog Management
- Automated CHANGELOG.md generation
- Conventional Commits parsing
- Categorized changes (Features, Bug Fixes, Breaking Changes)
- Contributor attribution
- Issue/PR linking

### Artifact Publishing
**For npm packages:**
- Package.json version updates
- npm publish automation
- Dist tag management
- Registry authentication

**For Docker images:**
- Image building and tagging
- Multi-platform builds
- Registry publishing (Docker Hub, GCR, ECR)
- Image scanning before publish

**For GitHub Releases:**
- Binary attachments
- Source code archives
- Release assets
- Release notes

### Branching Strategy
- Main branch for releases
- Develop branch for next release (optional)
- Feature branches with conventional commits
- Release branches for major versions (optional)
- Hotfix branch workflow

### Documentation
- CONTRIBUTING.md with commit conventions
- Release process documentation
- Version compatibility matrix
- Migration guides for breaking changes
- Upgrade instructions

### Quality Gates
- All tests must pass
- Code coverage thresholds
- Security scans clean
- Build successful
- Documentation updated

## Examples

### Setup for npm Package
```
/setup-release-workflow

Create automated release workflow for npm package with
semantic versioning and automated publishing to npm registry
```

### Setup for Docker Application
```
/setup-release-workflow

Setup release workflow for Docker application with
automated image building, tagging, and publishing to GCR
```

### Setup for Monorepo
```
/setup-release-workflow

Create release workflow for monorepo with independent
versioning for multiple packages
```

### Setup for Go Application
```
/setup-release-workflow

Setup release workflow for Go CLI tool with automated
binary building for multiple platforms and GitHub Releases
```

## Release Strategies

### Automated Releases (Recommended)
- Every merge to main triggers release analysis
- Version determined by commit messages
- Fully automated with no manual intervention
- Consistent and predictable
- Fast feedback loop

### Manual Release Approval
- Automated release preparation
- Manual approval gate before publishing
- Control over release timing
- Suitable for regulated environments
- Requires process discipline

### Scheduled Releases
- Releases on fixed schedule (weekly, monthly)
- Accumulate changes between releases
- Predictable for users
- May delay important fixes
- Suitable for stable projects

### Continuous Deployment
- Every change deployed immediately
- Feature flags for incomplete features
- Maximum agility
- Requires robust testing
- Suitable for SaaS applications

## Versioning Rules

### Semantic Versioning
```
MAJOR.MINOR.PATCH

MAJOR (1.0.0 -> 2.0.0)
- Triggered by: commits with BREAKING CHANGE
- Breaking API changes
- Incompatible updates
- Removed features

MINOR (1.0.0 -> 1.1.0)
- Triggered by: feat() commits
- New features
- Backward compatible additions
- Deprecations

PATCH (1.0.0 -> 1.0.1)
- Triggered by: fix() commits
- Bug fixes
- Performance improvements
- Security patches

Pre-release (1.0.0-alpha.1)
- Used for testing before stable release
- alpha -> beta -> rc -> stable
```

### Commit Message Format
```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]

Types:
- feat: New feature (MINOR)
- fix: Bug fix (PATCH)
- docs: Documentation only
- style: Code style (no logic change)
- refactor: Code refactoring
- perf: Performance improvement (PATCH)
- test: Test changes
- build: Build system changes
- ci: CI/CD changes
- chore: Maintenance

Breaking changes:
- Add "BREAKING CHANGE:" in footer (MAJOR)
- Or add "!" after type: "feat!:" (MAJOR)

Examples:
feat(auth): add OAuth2 login
fix(api): resolve rate limiting issue
feat!: remove deprecated v1 endpoints
```

## Best Practices Applied

### Automation
- Fully automated version bumping
- Automated changelog generation
- Automated artifact publishing
- Automated release notes
- No manual version editing

### Quality
- Enforce Conventional Commits
- Run full test suite before release
- Security scanning before publish
- Code coverage requirements
- Documentation updates

### Communication
- Clear changelog with categorization
- Breaking changes highlighted
- Migration guides for major versions
- Release announcements
- Version compatibility documentation

### Rollback
- Keep previous versions available
- Document rollback procedures
- Easy version pinning
- Quick hotfix workflow

### Consistency
- Standardized commit messages
- Predictable versioning
- Consistent release process
- Clear version history

Create production-ready release automation that ensures consistent, reliable, and well-documented releases.
