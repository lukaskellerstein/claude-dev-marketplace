---
description: Generate Kubernetes resources with best practices
allowed-tools: Write, Read, Grep
---

# Deploy to Kubernetes

## Parse Arguments
```bash
RESOURCE_TYPE="${ARGUMENTS[0]}"  # deployment|service|ingress|statefulset|job|cronjob
RESOURCE_NAME="${ARGUMENTS[1]}"  # Resource name
NAMESPACE="${ARGUMENTS[2]:-default}" # Target namespace (default: default)
```

## Validate Input
Check if RESOURCE_TYPE and RESOURCE_NAME are provided:
- Resource types: deployment, service, ingress, statefulset, job, cronjob
- Name must follow Kubernetes naming conventions (lowercase, alphanumeric, hyphens)
- Namespace defaults to 'default' if not specified

## Invoke K8s Expert
Invoke the `k8s-expert` agent with:
- Resource type: $RESOURCE_TYPE
- Resource name: $RESOURCE_NAME
- Target namespace: $NAMESPACE
- Application context from current directory

The agent will generate:
1. Resource manifest with best practices
2. Resource limits and requests
3. Health checks (liveness, readiness, startup)
4. Security contexts
5. Appropriate labels and annotations
6. Network policies if needed
7. RBAC configurations
8. Autoscaling configurations

## Output
Display the generated manifests and provide:
- Deployment instructions
- kubectl commands
- Resource URLs/endpoints
- Monitoring setup
- Troubleshooting tips

## Example Usage
```
/k8s-deploy deployment api-server production
/k8s-deploy service frontend default
/k8s-deploy ingress app-gateway ingress-nginx
/k8s-deploy statefulset postgres database
/k8s-deploy job data-migration jobs
/k8s-deploy cronjob backup-task system
```