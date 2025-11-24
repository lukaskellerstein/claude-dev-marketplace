---
description: Design automated deployment strategy with zero-downtime, rollback capabilities, and infrastructure as code
---

Design a comprehensive automated deployment strategy for your application with infrastructure as code and deployment automation.

## Process

Follow these steps:

1. **Analyze Requirements**: Understand deployment needs, constraints, and target platforms
   - Review application architecture and dependencies
   - Identify target deployment platforms (Kubernetes, Cloud Run, ECS, etc.)
   - Understand scalability and availability requirements
   - Check for stateful components (databases, storage)
   - Review security and compliance requirements

2. **Launch Deployment Architect**: Use the `deployment-architect` agent to:
   - Choose appropriate deployment strategy (rolling, blue-green, canary)
   - Design infrastructure as code (Terraform, Helm, Kustomize)
   - Create Kubernetes manifests or cloud service configurations
   - Design database migration strategy
   - Configure health checks and monitoring
   - Design rollback procedures
   - Plan for disaster recovery

3. **CI/CD Integration**: Use the `github-actions-expert` agent to:
   - Create deployment workflow in GitHub Actions
   - Configure deployment triggers
   - Set up environment promotion (dev -> staging -> prod)
   - Implement approval gates for production
   - Add deployment notifications

4. **Release Strategy** (if applicable): Use the `release-manager` agent to:
   - Design version tagging strategy
   - Configure artifact versioning
   - Set up release notes generation
   - Plan hotfix procedures

## Output

Present comprehensive deployment architecture including:

### Deployment Strategy Document
- Selected deployment approach (rolling, blue-green, canary)
- Rationale for chosen strategy
- Traffic splitting configuration
- Rollout timeline and phases

### Infrastructure as Code
**Kubernetes (Helm)**
- `Chart.yaml` with chart metadata
- `values.yaml` with configuration
- `templates/deployment.yaml` with deployment spec
- `templates/service.yaml` with service definition
- `templates/ingress.yaml` with ingress rules
- `templates/configmap.yaml` for configuration
- `templates/secret.yaml` for sensitive data

**Terraform**
- `main.tf` with resource definitions
- `variables.tf` with input variables
- `outputs.tf` with output values
- `terraform.tfvars` with environment config
- Provider configurations for cloud platforms

**Kubernetes Raw Manifests**
- Deployment YAML with strategy configuration
- Service YAML for load balancing
- Ingress YAML for external access
- ConfigMap and Secret YAMLs
- HPA YAML for autoscaling

### Deployment Pipeline
- GitHub Actions workflow for deployment
- Environment-specific configurations
- Deployment validation steps
- Health check integration
- Rollback automation

### Database Migration Strategy
- Migration tool setup (Flyway, Liquibase, Alembic)
- Migration workflow in CI/CD
- Rollback procedures for failed migrations
- Zero-downtime migration techniques

### Monitoring & Observability
- Health check endpoints
- Readiness and liveness probes
- Metrics collection (Prometheus)
- Log aggregation configuration
- Alert rules for deployment issues
- Dashboard for deployment tracking

### Runbook Documentation
- Deployment procedures
- Pre-deployment checklist
- Post-deployment validation
- Rollback procedures
- Incident response guide
- Troubleshooting common issues

### Architecture Diagrams
- Deployment flow diagram
- Infrastructure topology
- Traffic routing configuration
- Multi-region setup (if applicable)

## Examples

### Deploy to Kubernetes with Helm
```
/design-deployment

Design Kubernetes deployment for microservices with Helm charts,
rolling updates, and autoscaling for GKE cluster
```

### Deploy to Cloud Run
```
/design-deployment

Create deployment for Node.js API to GCP Cloud Run with
canary deployment and Cloud SQL database
```

### Deploy Multi-Service Application
```
/design-deployment

Design deployment for e-commerce platform with frontend,
backend, and worker services to Kubernetes with Istio
```

### Deploy Serverless Application
```
/design-deployment

Setup deployment for serverless functions to AWS Lambda
with API Gateway and DynamoDB
```

## Deployment Strategies

### Rolling Update (Default)
- Best for: Most applications
- Downtime: None
- Resource overhead: Low
- Rollback: Gradual
- Complexity: Low

### Blue-Green Deployment
- Best for: Critical services requiring instant rollback
- Downtime: None
- Resource overhead: High (2x)
- Rollback: Instant
- Complexity: Medium

### Canary Deployment
- Best for: High-risk changes requiring validation
- Downtime: None
- Resource overhead: Medium
- Rollback: Progressive
- Complexity: High

### Feature Flag Deployment
- Best for: Decoupling deployment from release
- Downtime: None
- Resource overhead: Low
- Rollback: Instant (no redeployment)
- Complexity: Medium

## Best Practices Applied

### Zero-Downtime Deployment
- Graceful shutdown with SIGTERM handling
- Connection draining period
- Readiness probes prevent premature traffic
- Rolling update with maxSurge and maxUnavailable
- Pre-stop hooks for cleanup

### Security
- Container image scanning before deployment
- Secrets management (not in code)
- Least privilege IAM roles
- Network policies for pod communication
- TLS/SSL for all external traffic

### Reliability
- Health checks at multiple levels
- Automatic rollback on failed health checks
- Circuit breakers for external dependencies
- Retry logic with exponential backoff
- Resource limits and requests

### Scalability
- Horizontal Pod Autoscaling (HPA)
- Cluster autoscaling
- Connection pooling for databases
- CDN for static assets
- Caching strategies

### Monitoring
- Deployment metrics tracking
- Error rate monitoring during rollout
- Latency percentiles (p50, p95, p99)
- Resource utilization tracking
- Log aggregation and analysis

Create production-ready deployment configurations that can be immediately implemented with confidence.
