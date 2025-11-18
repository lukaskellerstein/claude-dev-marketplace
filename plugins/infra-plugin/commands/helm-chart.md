---
description: Create Helm chart with production-ready structure
---

# Create Helm Chart

## Parse Arguments
```bash
CHART_NAME="${ARGUMENTS[0]}"           # Chart name
CHART_TYPE="${ARGUMENTS[1]:-application}" # application|library|operator (default: application)
```

## Validate Input
Check if CHART_NAME is provided:
- Name must follow Helm naming conventions
- Type defaults to 'application' if not specified
- Valid types: application, library, operator

## Invoke Helm Expert
Invoke the `helm-expert` agent with:
- Chart name: $CHART_NAME
- Chart type: $CHART_TYPE
- Application context

The agent will generate:
1. Chart directory structure
2. Chart.yaml with metadata
3. values.yaml with sensible defaults
4. Templates for Kubernetes resources:
   - Deployment/StatefulSet
   - Service
   - Ingress
   - ConfigMap
   - Secret
   - HorizontalPodAutoscaler
5. _helpers.tpl with template functions
6. NOTES.txt for post-installation instructions
7. Tests for chart validation

## Chart Types
### Application
- Standard application deployment
- Includes all common Kubernetes resources
- Ready for production use

### Library
- Reusable chart components
- No default templates
- Meant to be included as dependency

### Operator
- Operator pattern implementation
- CRD definitions
- RBAC configurations
- Webhook configurations

## Output
Display the generated chart structure and provide:
- Installation instructions
- Helm commands (install, upgrade, rollback)
- Values customization guide
- Dependency management
- Chart repository setup

## Example Usage
```
/helm-chart my-app application
/helm-chart shared-lib library
/helm-chart redis-operator operator
/helm-chart frontend application
```