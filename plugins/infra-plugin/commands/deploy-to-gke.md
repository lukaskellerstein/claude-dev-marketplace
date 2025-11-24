---
description: Deploy application to Google Kubernetes Engine with complete setup including manifests, CI/CD, and monitoring
---

Deploy a production-ready application to GKE with comprehensive Kubernetes manifests, ingress, monitoring, and CI/CD pipeline.

## Process

Follow these steps:

1. **Analyze Application**: Understand the application architecture and requirements
   - Identify application components (frontend, backend, databases)
   - Review existing Docker images or Dockerfiles
   - Determine resource requirements (CPU, memory)
   - Check for dependencies (databases, caches, message queues)
   - Review existing infrastructure (GCP project, VPC, GKE cluster)

2. **Launch Kubernetes Expert**: Use the `kubernetes-expert` agent to:
   - Design Kubernetes manifests (Deployments, Services, Ingress)
   - Configure resource limits and requests
   - Set up health checks and probes
   - Design ConfigMaps and Secrets management
   - Configure HPA for auto-scaling
   - Design network policies if needed
   - Set up RBAC and service accounts

3. **Launch GCloud Expert**: Use the `gcloud-expert` agent to:
   - Verify GCP project and GKE cluster setup
   - Configure Cloud SQL or Cloud Storage if needed
   - Set up IAM and Workload Identity
   - Configure Cloud Load Balancer and Cloud CDN
   - Set up Secret Manager for sensitive data
   - Configure Cloud Monitoring and Logging

4. **Launch Docker Expert** (if needed): Use the `docker-expert` agent to:
   - Optimize Dockerfiles for production
   - Set up multi-stage builds
   - Implement security best practices
   - Configure image scanning in CI/CD

5. **Create Deployment Pipeline**: Set up CI/CD automation
   - Configure Cloud Build or GitHub Actions
   - Implement automated testing
   - Set up image building and pushing to GCR/Artifact Registry
   - Configure automated deployment to GKE
   - Implement rollback strategy

6. **Set Up Monitoring**: Configure observability
   - Deploy Prometheus and Grafana (or use Cloud Monitoring)
   - Set up log aggregation (Cloud Logging or EFK stack)
   - Configure alerts for critical metrics
   - Set up dashboards for key metrics

## Output

Present a comprehensive GKE deployment including:

### Kubernetes Manifests
- Namespace configuration
- Deployment manifests with resource limits
- Service definitions (ClusterIP, LoadBalancer)
- Ingress configuration with TLS
- ConfigMap and Secret templates
- HPA configuration for auto-scaling
- PersistentVolumeClaim if needed
- NetworkPolicy for security
- ServiceAccount and RBAC

### GCP Infrastructure
- GKE cluster configuration (if creating new)
- VPC network and subnet setup
- Cloud SQL instance (if needed)
- Cloud Storage buckets (if needed)
- IAM service accounts and roles
- Workload Identity binding
- Secret Manager secrets

### CI/CD Pipeline
- Cloud Build configuration or GitHub Actions workflow
- Build triggers and automation
- Image tagging strategy
- Deployment automation
- Rollback procedures
- Testing in pipeline

### Monitoring & Observability
- Prometheus ServiceMonitor (if using Prometheus)
- Grafana dashboard JSON
- Cloud Monitoring alert policies
- Log-based metrics
- SLI/SLO definitions

### Documentation
- Deployment instructions
- kubectl commands for management
- Troubleshooting guide
- Scaling guidelines
- Backup and disaster recovery plan

### Security Configuration
- Pod security standards
- Network policies
- Secret encryption
- Image scanning results
- Security best practices checklist

## Examples

### Deploy Microservices Application
```
/deploy-to-gke

Deploy our e-commerce microservices (frontend, API gateway, order service,
payment service) to GKE production cluster with Istio service mesh,
Cloud SQL for databases, and comprehensive monitoring
```

### Deploy Stateful Application
```
/deploy-to-gke

Deploy PostgreSQL database with StatefulSet, persistent storage,
automated backups to Cloud Storage, and monitoring
```

### Deploy Serverless Workload
```
/deploy-to-gke

Deploy batch processing job that runs daily using CronJob,
processes files from Cloud Storage, and stores results in BigQuery
```

## Best Practices Applied

- **High Availability**: Multi-replica deployments with pod anti-affinity
- **Auto-scaling**: HPA based on CPU/memory metrics
- **Security**: Non-root containers, network policies, secret management
- **Observability**: Comprehensive logging, metrics, and tracing
- **Resource Optimization**: Appropriate resource limits and requests
- **Zero-downtime**: Rolling updates with readiness probes
- **Disaster Recovery**: Backup strategies and rollback procedures
- **Cost Optimization**: Right-sized resources and auto-scaling

Provide actionable, production-ready deployment configurations that can be applied immediately to GKE.
