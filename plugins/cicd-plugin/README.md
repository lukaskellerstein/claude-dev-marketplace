# CI/CD Plugin

Comprehensive toolkit for CI/CD automation covering GitHub Actions, deployment strategies, and release management.

## Features

### Agents

- **github-actions-expert**: Expert in designing and optimizing GitHub Actions workflows with best practices for CI/CD, testing, building, and deployment automation
- **deployment-architect**: Expert in designing automated deployment strategies for Kubernetes, cloud platforms, and infrastructure with zero-downtime and rollback capabilities
- **release-manager**: Expert in release management, versioning strategies, changelog generation, and automated release workflows

### Commands

- `/setup-github-actions`: Create GitHub Actions workflows for CI/CD with testing, building, and deployment automation
- `/design-deployment`: Design automated deployment strategy with zero-downtime, rollback capabilities, and infrastructure as code
- `/setup-release-workflow`: Create automated release workflow with semantic versioning, changelog generation, and artifact publishing

### Skills

- **cicd-best-practices**: Auto-invoked when working with CI/CD pipelines, GitHub Actions, or deployment configurations to ensure best practices
- **deployment-patterns**: Auto-invoked when designing or implementing deployments to ensure proper deployment patterns and strategies

## Usage

### Setup GitHub Actions

```
/setup-github-actions

Create GitHub Actions workflows for Node.js application with Jest tests,
Docker build, and deployment to GCP Cloud Run
```

```
/setup-github-actions

Setup CI/CD for Python FastAPI service with pytest, container scanning,
and Kubernetes deployment to GKE
```

```
/setup-github-actions

Create workflows for monorepo with multiple packages, matrix testing,
and independent deployment pipelines
```

### Design Deployments

```
/design-deployment

Design Kubernetes deployment with Helm charts, rolling updates,
and autoscaling for microservices architecture
```

```
/design-deployment

Create blue-green deployment strategy for critical payment service
with instant rollback capability
```

```
/design-deployment

Setup canary deployment with progressive rollout and automated
rollback based on error rate metrics
```

```
/design-deployment

Design serverless deployment to AWS Lambda with API Gateway
and DynamoDB integration
```

### Setup Release Management

```
/setup-release-workflow

Create automated release workflow for npm package with semantic
versioning and publishing to npm registry
```

```
/setup-release-workflow

Setup release automation for Docker application with multi-platform
builds and publishing to Google Container Registry
```

```
/setup-release-workflow

Design release workflow for monorepo with independent versioning
and changelog generation per package
```

### Use Agents Directly

Invoke specialized agents for focused work:

- "Use github-actions-expert to optimize existing workflow performance"
- "Use deployment-architect to design zero-downtime database migration"
- "Use release-manager to implement semantic release with conventional commits"

## Technologies Covered

### CI/CD Platforms
- **GitHub Actions**: Native GitHub CI/CD with workflows, actions, and runners
- **GitLab CI**: Pipeline configuration and automation
- **Jenkins**: Classic CI/CD with pipelines
- **CircleCI**: Cloud-based CI/CD

### Deployment Targets
- **Kubernetes**: Deployments, StatefulSets, DaemonSets, Jobs
- **Cloud Run**: Serverless containers on GCP
- **AWS ECS/EKS**: Container orchestration on AWS
- **Azure AKS**: Managed Kubernetes on Azure
- **Cloud Functions/Lambda**: Serverless functions
- **App Engine**: Platform as a Service

### Infrastructure as Code
- **Terraform**: Infrastructure provisioning and management
- **Helm**: Kubernetes package manager
- **Kustomize**: Kubernetes manifest customization
- **Ansible**: Configuration management
- **ArgoCD/Flux**: GitOps continuous delivery

### Deployment Strategies
- **Rolling Update**: Gradual pod replacement (default)
- **Blue-Green**: Two identical environments with instant switch
- **Canary**: Progressive rollout with traffic splitting
- **A/B Testing**: Multiple versions with intelligent routing
- **Feature Flags**: Decouple deployment from release

### Release Management
- **Semantic Versioning**: MAJOR.MINOR.PATCH versioning
- **Conventional Commits**: Standardized commit messages
- **Semantic Release**: Automated version bumping and publishing
- **Changelog Generation**: Automated release notes
- **Git Tagging**: Release version management

## Patterns & Best Practices

### GitHub Actions
- Workflow organization and naming conventions
- Caching strategies (dependencies, Docker layers)
- Matrix builds for multi-platform testing
- Secrets management and OIDC authentication
- Parallel job execution with dependencies
- Conditional execution based on context
- Reusable workflows and composite actions
- Self-hosted runners for performance

### Pipeline Optimization
- Fast feedback with fail-fast strategy
- Test pyramid (unit → integration → E2E)
- Parallel execution where possible
- Incremental builds and testing
- Artifact caching and reuse
- Build time monitoring and optimization

### Deployment Best Practices
- Zero-downtime deployments with rolling updates
- Health checks (readiness, liveness, startup probes)
- Graceful shutdown with SIGTERM handling
- Connection draining periods
- Automated rollback on failures
- Resource requests and limits
- Horizontal Pod Autoscaling (HPA)
- Multi-environment strategy (dev, staging, prod)

### Database Migrations
- Zero-downtime migration techniques
- Backward compatible schema changes
- Additive migrations (add before remove)
- Backfill strategies for data migrations
- Migration rollback procedures
- Version control for migrations

### Release Automation
- Semantic versioning based on commits
- Conventional Commits enforcement
- Automated changelog generation
- Multi-artifact publishing (npm, Docker, binaries)
- Git tag management
- Release notes generation
- Hotfix procedures

### Security
- Secrets management (GitHub Secrets, HashiCorp Vault)
- Dependency scanning (Dependabot, Snyk)
- Container image scanning (Trivy, Clair)
- SAST/DAST security testing
- Least privilege permissions
- OIDC for cloud authentication
- Code signing and verification

### Monitoring & Observability
- Deployment metrics tracking
- Error rate monitoring
- Latency percentiles (p50, p95, p99)
- Resource utilization tracking
- Distributed tracing
- Centralized logging
- Alert configuration
- Deployment dashboards

## Example Workflows

### Building a Node.js Application CI/CD

1. **Setup CI Pipeline**
   ```
   /setup-github-actions
   Create CI workflow for Node.js app with Jest tests, ESLint,
   and Docker image building
   ```

2. **Design Deployment**
   ```
   /design-deployment
   Design Kubernetes deployment to GKE with rolling updates
   and autoscaling
   ```

3. **Setup Release Automation**
   ```
   /setup-release-workflow
   Setup semantic release with npm publishing and Docker
   image tagging
   ```

### Building a Python Microservice

1. **Setup CI/CD**
   ```
   /setup-github-actions
   Create workflows for Python FastAPI with pytest, coverage,
   and deployment to Cloud Run
   ```

2. **Design Database Migrations**
   ```
   /design-deployment
   Design zero-downtime deployment with Alembic migrations
   and health checks
   ```

3. **Setup Release Management**
   ```
   /setup-release-workflow
   Setup automated versioning with changelog generation
   and PyPI publishing
   ```

### Building a Monorepo Application

1. **Setup Selective CI**
   ```
   /setup-github-actions
   Create workflows with path-based triggering and matrix
   builds for multiple packages
   ```

2. **Design Multi-Service Deployment**
   ```
   /design-deployment
   Design independent deployment pipelines for frontend,
   backend, and worker services
   ```

3. **Setup Independent Releases**
   ```
   /setup-release-workflow
   Setup independent versioning and changelog per package
   with workspace support
   ```

## Integration with Other Plugins

- **backend-plugin**: Design APIs first, then create CI/CD pipelines for testing and deployment
- **frontend-plugin**: Build React applications, then setup automated deployment to CDN
- **database-plugin**: Design database schema, then create migration workflows
- **infra-plugin**: Provision infrastructure with Terraform, then deploy applications
- **test-plugin**: Design comprehensive test strategy, then integrate into CI pipeline

## Best Practices

### CI/CD Pipeline Design
- Start with comprehensive CI before adding CD
- Keep pipelines fast with aggressive caching
- Implement security scanning at multiple stages
- Use matrix builds for multi-platform support
- Configure appropriate timeouts
- Pin action versions for reproducibility

### Deployment Strategy Selection
- Rolling update for most applications (default)
- Blue-green for critical services needing instant rollback
- Canary for high-risk changes requiring validation
- Feature flags for decoupling deployment from release

### Release Management
- Use Semantic Versioning (SemVer)
- Enforce Conventional Commits
- Automate version bumping and changelog
- Test releases in staging before production
- Document breaking changes clearly
- Maintain version compatibility matrix

### Zero-Downtime Deployments
- Always configure readiness probes
- Implement graceful shutdown (SIGTERM)
- Set appropriate connection draining periods
- Use rolling updates with maxUnavailable: 0
- Test rollback procedures regularly

### Security & Compliance
- Never commit secrets to repositories
- Use OIDC instead of long-lived credentials
- Scan dependencies and containers regularly
- Implement least privilege permissions
- Enable audit logging
- Regular security updates

### Monitoring & Feedback
- Track deployment frequency and duration
- Monitor error rates during rollouts
- Set up alerts for failed deployments
- Create deployment dashboards
- Conduct post-mortems for failed deployments
- Continuously optimize pipeline performance

## Advanced Topics

### Progressive Delivery
- Feature flags and toggles
- Canary analysis with automated rollback
- Traffic shaping and routing
- User segmentation for rollouts
- Experimentation platforms

### GitOps
- Infrastructure and application code in Git
- Automated synchronization with ArgoCD/Flux
- Declarative infrastructure management
- Audit trail through Git history
- Self-healing applications

### Multi-Region Deployments
- Traffic distribution strategies
- Data replication and consistency
- Disaster recovery procedures
- Latency-based routing
- Regional failover

### Cost Optimization
- Self-hosted runners for frequent builds
- Aggressive caching strategies
- Spot instances for CI workloads
- Build parallelization
- Resource right-sizing

### Compliance & Governance
- Deployment approval gates
- Change management integration
- Audit logging and reporting
- Policy enforcement (OPA)
- Compliance scanning

Start building robust, automated CI/CD pipelines with comprehensive testing, zero-downtime deployments, and intelligent release management!
