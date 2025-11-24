# Infrastructure Plugin

A comprehensive Claude Code plugin for infrastructure automation, container orchestration, and Infrastructure as Code on Google Cloud Platform.

## Overview

The Infrastructure Plugin provides expert guidance and automation for:
- **Google Cloud Platform**: GCP services, architecture, IAM, networking
- **Kubernetes**: Container orchestration, deployment strategies, monitoring
- **Docker**: Containerization, multi-stage builds, image optimization
- **Terraform**: Infrastructure as Code, state management, module development
- **Helm**: Kubernetes package management (coming soon)

## Features

### Agents

#### 1. Kubernetes Expert (`kubernetes-expert`)
Senior Kubernetes architect specializing in:
- Kubernetes architecture and components
- Workload resources (Deployments, StatefulSets, Jobs)
- Service discovery and networking
- Configuration and secrets management
- Storage and persistence
- Observability and monitoring
- Security best practices
- Deployment strategies (rolling, blue-green, canary)
- Auto-scaling and resource management

**Model**: Sonnet (high complexity)
**Tools**: Glob, Grep, Read, WebFetch, TodoWrite, WebSearch, Bash

#### 2. Terraform Expert (`terraform-expert`)
Infrastructure as Code specialist focusing on:
- Terraform fundamentals and HCL syntax
- Provider configuration (GCP, AWS, Azure)
- Module development and composition
- State management and remote backends
- Google Cloud resource provisioning
- Kubernetes and Helm integration
- Security and compliance
- CI/CD integration
- Advanced patterns and best practices

**Model**: Sonnet (high complexity)
**Tools**: Glob, Grep, Read, WebFetch, TodoWrite, WebSearch, Bash, mcp__terraform__*

#### 3. Docker Expert (`docker-expert`)
Container optimization specialist covering:
- Dockerfile optimization and multi-stage builds
- Docker Compose for multi-container applications
- Image optimization and size reduction
- Container security best practices
- Networking and storage
- Performance optimization
- CI/CD integration
- Debugging and troubleshooting

**Model**: Sonnet (high complexity)
**Tools**: Glob, Grep, Read, WebFetch, TodoWrite, WebSearch, Bash

#### 4. GCloud Expert (`gcloud-expert`)
Google Cloud Platform architect with expertise in:
- Compute services (GCE, GKE, Cloud Run, Cloud Functions)
- Storage and databases (Cloud Storage, Cloud SQL, Firestore)
- Networking (VPC, Load Balancing, Cloud CDN)
- Identity and Access Management
- Security services (Secret Manager, KMS, Binary Authorization)
- Serverless and event-driven architecture
- Data and analytics
- DevOps and CI/CD
- Cost optimization

**Model**: Sonnet (high complexity)
**Tools**: Glob, Grep, Read, WebFetch, TodoWrite, WebSearch, Bash, mcp__gcloud__*

### Commands

#### 1. `/deploy-to-gke`
Deploy applications to Google Kubernetes Engine with:
- Complete Kubernetes manifests (Deployments, Services, Ingress)
- Resource configuration and auto-scaling
- Health checks and monitoring setup
- Security configuration (RBAC, network policies)
- CI/CD pipeline integration
- Production-ready deployment

**Orchestrates**: kubernetes-expert, gcloud-expert, docker-expert

#### 2. `/provision-infrastructure`
Provision complete cloud infrastructure using Terraform:
- Infrastructure as Code with Terraform
- VPC, GKE, Cloud SQL, and supporting services
- Modular, reusable Terraform modules
- Remote state management
- Environment-specific configurations (dev, staging, production)
- Security and compliance
- Cost optimization

**Orchestrates**: terraform-expert, gcloud-expert, kubernetes-expert

#### 3. `/containerize-app`
Containerize applications with Docker:
- Optimized multi-stage Dockerfiles
- Security best practices (non-root, minimal images)
- Docker Compose for local development
- Image optimization and size reduction
- CI/CD integration
- Production-ready containers

**Orchestrates**: docker-expert

### Skills

#### 1. Kubernetes Best Practices (`k8s-best-practices`)
Auto-invoked when working with Kubernetes to ensure:
- Resource requests and limits
- Health checks (liveness and readiness probes)
- Security configuration (non-root, read-only filesystem)
- Network policies
- Pod disruption budgets
- Proper labeling and annotations
- Storage best practices
- Monitoring and logging

**Triggers**: When creating or modifying Kubernetes manifests

#### 2. Terraform Patterns (`terraform-patterns`)
Auto-invoked when writing Terraform to ensure:
- Proper project structure
- Version management
- Variable best practices with validation
- Resource naming and tagging
- State management
- Dynamic blocks and loops
- Lifecycle management
- Module best practices
- Security (never commit secrets)

**Triggers**: When creating or modifying Terraform files

### MCP Servers

#### 1. GCloud MCP Server
- Access to Google Cloud Platform APIs and services
- Project and resource management
- Service configuration and deployment

**Configuration**: Automatically configured via plugin.json

#### 2. Terraform MCP Server
- Terraform operations and state management
- Infrastructure planning and validation
- Resource import and management

**Configuration**: Automatically configured via plugin.json

## Installation

1. Clone or download the plugin to your Claude Code plugins directory:
```bash
cd ~/.claude/plugins
git clone <repo-url> infra-plugin
```

2. The plugin will be automatically loaded by Claude Code

3. MCP servers (gcloud, terraform) will be configured automatically

## Usage Examples

### Deploy to GKE

```
/deploy-to-gke

Deploy our microservices application to GKE production cluster with:
- Frontend and backend services
- PostgreSQL database with Cloud SQL
- Redis for caching
- Ingress with TLS
- Horizontal pod autoscaling
- Comprehensive monitoring
```

### Provision Infrastructure

```
/provision-infrastructure

Create production infrastructure on GCP:
- VPC with public and private subnets
- GKE cluster with multiple node pools
- Cloud SQL PostgreSQL with HA
- Cloud Storage for backups
- IAM and Workload Identity setup
```

### Containerize Application

```
/containerize-app

Create Docker containers for our Node.js application with:
- Multi-stage build for optimal size
- Non-root user for security
- Docker Compose with PostgreSQL and Redis
- Health checks and graceful shutdown
```

### Use Agents Directly

```
@kubernetes-expert Design Kubernetes manifests for a stateful PostgreSQL
deployment with persistent storage, backup CronJob, and monitoring

@terraform-expert Create a Terraform module for GKE cluster with
multiple node pools, Workload Identity, and private cluster setup

@docker-expert Optimize this Dockerfile for a Python FastAPI application
to reduce image size and improve security

@gcloud-expert Design a multi-region architecture on GCP with global
load balancing and Cloud SQL cross-region replication
```

## Best Practices

### Kubernetes
- Always set resource requests and limits
- Configure health checks (liveness and readiness)
- Run as non-root user
- Use multiple replicas for high availability
- Implement network policies for security
- Use HPA for auto-scaling
- Configure proper monitoring and logging

### Terraform
- Use remote state with locking (GCS)
- Pin provider versions
- Validate variables with constraints
- Use modules for reusability
- Never commit secrets to version control
- Tag all resources for organization
- Implement proper state management

### Docker
- Use multi-stage builds
- Choose minimal base images (Alpine, Distroless)
- Run as non-root user
- Scan images for vulnerabilities
- Implement health checks
- Use .dockerignore to reduce context
- Optimize layer caching

### Google Cloud
- Use Workload Identity instead of service account keys
- Enable VPC Service Controls for sensitive data
- Use Private GKE clusters
- Enable Binary Authorization
- Use Secret Manager for secrets
- Implement least privilege IAM
- Enable audit logging

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  Infrastructure Plugin                  │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Commands                    Agents                     │
│  ┌──────────────────┐       ┌──────────────────┐      │
│  │ deploy-to-gke    │──────▶│ kubernetes-expert│      │
│  │                  │       │ terraform-expert │      │
│  │                  │       │ docker-expert    │      │
│  │                  │       │ gcloud-expert    │      │
│  └──────────────────┘       └──────────────────┘      │
│                                                         │
│  ┌──────────────────┐       ┌──────────────────┐      │
│  │ provision-infra  │──────▶│ terraform-expert │      │
│  │                  │       │ gcloud-expert    │      │
│  │                  │       │ kubernetes-expert│      │
│  └──────────────────┘       └──────────────────┘      │
│                                                         │
│  ┌──────────────────┐       ┌──────────────────┐      │
│  │ containerize-app │──────▶│ docker-expert    │      │
│  └──────────────────┘       └──────────────────┘      │
│                                                         │
│  Skills (Auto-invoked)       MCP Servers               │
│  ┌──────────────────┐       ┌──────────────────┐      │
│  │ k8s-best-practices│       │ gcloud-mcp       │      │
│  │ terraform-patterns│       │ terraform-mcp    │      │
│  └──────────────────┘       └──────────────────┘      │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Technologies Covered

- **Google Cloud Platform**: GCE, GKE, Cloud Run, Cloud Functions, Cloud SQL, Cloud Storage, VPC, Load Balancing, IAM
- **Kubernetes**: Deployments, StatefulSets, Services, Ingress, ConfigMaps, Secrets, HPA, Network Policies
- **Docker**: Dockerfiles, Docker Compose, Multi-stage builds, Image optimization
- **Terraform**: HCL, Modules, State management, Provider configuration
- **Helm**: Chart management (coming soon)

## Contributing

Contributions are welcome! Please:
1. Follow the existing patterns for agents, commands, and skills
2. Test thoroughly in development environments
3. Update documentation
4. Follow security best practices

## License

MIT

## Author

Lukas Kellerstein

## Version

1.0.0
