---
description: Create GitHub Actions workflows for CI/CD with testing, building, and deployment automation
---

Create comprehensive GitHub Actions workflows for continuous integration and deployment.

## Process

Follow these steps:

1. **Analyze Project**: Understand the technology stack, testing requirements, and deployment targets
   - Detect language/framework (Node.js, Python, Go, Java, etc.)
   - Identify test frameworks and tools
   - Review existing deployment infrastructure
   - Check for monorepo or multi-package setup
   - Identify dependencies and build requirements

2. **Launch GitHub Actions Expert**: Use the `cicd-plugin:github-actions-expert` agent to:
   - Design workflow structure (CI, CD, release workflows)
   - Configure appropriate triggers (push, PR, schedule)
   - Set up test execution with proper reporting
   - Configure build optimization with caching
   - Design deployment strategy
   - Implement security scanning
   - Add monitoring and notifications

3. **Validate with Deployment Architect**: Use the `cicd-plugin:deployment-architect` agent to:
   - Review deployment strategy
   - Validate infrastructure requirements
   - Check health check configuration
   - Verify rollback procedures
   - Ensure monitoring setup

4. **Release Workflow** (if applicable): Use the `release-manager` agent to:
   - Set up automated versioning
   - Configure changelog generation
   - Design release workflow
   - Set up artifact publishing

## Output

Present comprehensive GitHub Actions workflows including:

### CI Workflow (`.github/workflows/ci.yml`)
- Run on pull requests and main branch
- Test execution with coverage reporting
- Linting and code quality checks
- Build verification
- Security scanning
- Artifact generation

### CD Workflow (`.github/workflows/cd.yml`)
- Deploy to staging/production
- Environment-based configuration
- Health checks and validation
- Rollback capabilities
- Deployment notifications

### Release Workflow (`.github/workflows/release.yml`)
- Automated version bumping
- Changelog generation
- Git tag creation
- Package/container publishing
- Release notes generation

### Additional Workflows
- Dependency updates (Dependabot)
- Security scanning
- Performance testing
- Documentation deployment

### Configuration Files
- `.github/dependabot.yml` for dependency updates
- `.github/CODEOWNERS` for code review
- Branch protection rules documentation

### Documentation
- README section on CI/CD workflows
- Development workflow guide
- Deployment procedures
- Troubleshooting guide

## Examples

### Setup for Node.js Application
```
/setup-github-actions

Create GitHub Actions for Node.js app with Jest tests,
Docker build, and deployment to GCP Cloud Run
```

### Setup for Python Service
```
/setup-github-actions

Setup CI/CD for Python FastAPI service with pytest,
Docker image publishing, and Kubernetes deployment
```

### Setup for Monorepo
```
/setup-github-actions

Create GitHub Actions for monorepo with multiple packages,
selective testing, and independent versioning
```

### Setup for Library/Package
```
/setup-github-actions

Setup automated release workflow for npm package with
semantic versioning and automated publishing
```

## Best Practices Applied

### Performance
- Aggressive dependency caching
- Matrix builds for parallel execution
- Docker layer caching
- Conditional job execution
- Artifact sharing between jobs

### Security
- Secrets management with GitHub Secrets
- OIDC authentication for cloud providers
- Dependency scanning with Dependabot
- Container image scanning
- Code security scanning (SAST)

### Reliability
- Retry logic for flaky operations
- Timeout settings for all jobs
- Comprehensive error handling
- Health checks before/after deployment
- Automated rollback on failures

### Maintainability
- Clear workflow and job names
- Modular design with reusable workflows
- Comprehensive comments
- Version pinning for actions
- Regular dependency updates

### Observability
- Detailed logging at each step
- Test result reporting
- Code coverage reporting
- Deployment status tracking
- Slack/email notifications

Create production-ready workflows that can be immediately used and easily maintained.
