---
name: helm-validator
description: Master Helm chart best practices and validation. Use when creating Helm charts, editing Chart.yaml/values.yaml, modifying templates, working with dependencies, ensuring production readiness, or when discussing Helm chart structure, template best practices, values schema, chart dependencies, helm hooks, chart testing, release management, or package versioning.
allowed-tools: Read, Edit
---

# Helm Validator Skill

Master Helm chart best practices and production readiness standards to ensure all Helm charts follow conventions, security requirements, and deployment best practices.

## When to Use This Skill

Use this skill when:

1. Creating new Helm charts from scratch
2. Editing Chart.yaml metadata files
3. Modifying values.yaml configuration
4. Working with Helm template files
5. Updating chart dependencies
6. Defining chart hooks or tests
7. Creating reusable chart libraries
8. Publishing charts to repositories
9. Migrating applications to Helm
10. Reviewing chart pull requests
11. Troubleshooting chart deployment issues
12. Upgrading Helm chart versions
13. Creating subchart configurations
14. Implementing chart CI/CD pipelines
15. Auditing charts for security compliance

## Quick Start

This skill automatically validates Helm charts as you create them:

```bash
# Creating a new chart triggers validation
$ helm create my-app

✅ Chart structure validation: PASSED
⚠️  Missing: templates/NOTES.txt
⚠️  Security: No default securityContext
✓  Suggestion: Add resource limits

Automatically applying fixes...
✅ All improvements applied
```

## Auto-Invocation Context

This skill triggers when:
- Creating new Helm charts
- Editing Chart.yaml files
- Modifying values.yaml
- Working with Helm templates
- Updating chart dependencies

## Purpose
This skill automatically validates and improves Helm charts when they are created or edited, ensuring they follow best practices and are production-ready.

## Validations Performed

### 1. Chart Structure Compliance

#### Required Files Check
```
✓ Chart.yaml present and valid
✓ values.yaml with defaults
✓ templates/ directory exists
✓ templates/NOTES.txt for user guidance
✓ README.md documentation
✓ LICENSE file (if distributing)
```

#### Chart.yaml Validation
```yaml
# Ensure required fields
apiVersion: v2  # Must be v2 for Helm 3
name: my-chart  # Required, lowercase with hyphens
version: 1.0.0  # Required, semantic versioning
appVersion: "2.0.0"  # Application version
description: A Helm chart for...  # Required description
type: application  # application or library

# Recommended fields
keywords:
  - web
  - application
home: https://example.com
sources:
  - https://github.com/example/chart
maintainers:
  - name: Team Name
    email: team@example.com
    url: https://example.com
icon: https://example.com/icon.png

# Validate dependencies
dependencies:
  - name: redis
    version: "~17.0.0"  # Use version constraints
    repository: "https://charts.bitnami.com/bitnami"
    condition: redis.enabled
    tags:
      - cache
    import-values:
      - child: auth.password
        parent: redisPassword
```

### 2. Template Syntax Validation

#### Proper Template Functions
```yaml
# BAD: Incorrect function usage
name: {{ .Values.name | default .Chart.Name }}

# GOOD: Proper default function
name: {{ default .Chart.Name .Values.name }}

# BAD: Missing nil checks
port: {{ .Values.service.port }}

# GOOD: Safe navigation
port: {{ default 8080 .Values.service.port }}

# BAD: Incorrect quote usage
value: "{{ .Values.config.value }}"

# GOOD: Use quote function
value: {{ .Values.config.value | quote }}
```

#### Template Best Practices
```yaml
# Use include for reusable templates
metadata:
  labels:
    {{- include "chart.labels" . | nindent 4 }}

# Proper indentation with nindent
annotations:
  {{- with .Values.podAnnotations }}
  {{- toYaml . | nindent 8 }}
  {{- end }}

# Conditional sections
{{- if .Values.ingress.enabled }}
---
apiVersion: networking.k8s.io/v1
kind: Ingress
# ...
{{- end }}

# Range with proper spacing
{{- range .Values.ingress.hosts }}
  - host: {{ .host | quote }}
    http:
      paths:
      {{- range .paths }}
      - path: {{ .path }}
        pathType: {{ .pathType }}
      {{- end }}
{{- end }}
```

### 3. Values Organization

#### Structured values.yaml
```yaml
# Global values
global:
  imageRegistry: ""
  imagePullSecrets: []
  storageClass: ""

# Image configuration
image:
  repository: myapp
  pullPolicy: IfNotPresent
  tag: ""  # Defaults to Chart.appVersion

# Deployment settings
replicaCount: 2

# Service configuration
service:
  type: ClusterIP
  port: 80
  targetPort: http
  annotations: {}

# Ingress configuration
ingress:
  enabled: false
  className: ""
  annotations: {}
  hosts:
    - host: chart-example.local
      paths:
        - path: /
          pathType: ImplementationSpecific
  tls: []

# Resources
resources: {}
  # limits:
  #   cpu: 100m
  #   memory: 128Mi
  # requests:
  #   cpu: 100m
  #   memory: 128Mi

# Autoscaling
autoscaling:
  enabled: false
  minReplicas: 1
  maxReplicas: 100
  targetCPUUtilizationPercentage: 80

# Node selection
nodeSelector: {}
tolerations: []
affinity: {}
```

### 4. Security Best Practices

#### Default Security Settings
```yaml
# values.yaml should default to secure
podSecurityContext:
  runAsNonRoot: true
  runAsUser: 1000
  fsGroup: 2000

securityContext:
  allowPrivilegeEscalation: false
  capabilities:
    drop:
    - ALL
  readOnlyRootFilesystem: true

# No default passwords
postgresql:
  auth:
    existingSecret: ""  # ✓ Use existing secret
```

### 5. Label Standards

```yaml
# Required labels
metadata:
  labels:
    app.kubernetes.io/name: {{ include "chart.name" . }}
    app.kubernetes.io/instance: {{ .Release.Name }}
    app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
    app.kubernetes.io/component: {{ .Values.component }}
    app.kubernetes.io/part-of: {{ .Values.partOf }}
    app.kubernetes.io/managed-by: {{ .Release.Service }}
    helm.sh/chart: {{ include "chart.chart" . }}
```

## Real-World Applications

### Microservice Helm Chart

**Scenario:** Creating production-ready chart for microservice

```yaml
# Chart.yaml
apiVersion: v2
name: payment-service
version: 1.0.0
appVersion: "2.3.1"
description: Payment processing microservice
type: application
keywords:
  - payment
  - microservice
  - fintech
maintainers:
  - name: Platform Team
    email: platform@company.com

# values.yaml
replicaCount: 3

image:
  repository: company/payment-service
  tag: "2.3.1"
  pullPolicy: IfNotPresent

service:
  type: ClusterIP
  port: 8080

ingress:
  enabled: true
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/rate-limit: "100"

resources:
  requests:
    cpu: 500m
    memory: 512Mi
  limits:
    cpu: 1000m
    memory: 1Gi

autoscaling:
  enabled: true
  minReplicas: 3
  maxReplicas: 10
  targetCPUUtilizationPercentage: 70
```

### Multi-Tenant Application

**Scenario:** Helm chart for multi-tenant SaaS application

```yaml
# values.yaml - Production configuration
global:
  environment: production
  region: us-east-1

tenants:
  - name: acme-corp
    database:
      host: postgres-acme.internal
      existingSecret: acme-db-credentials
    resources:
      requests:
        cpu: 1000m
        memory: 2Gi
  - name: globex
    database:
      host: postgres-globex.internal
      existingSecret: globex-db-credentials
    resources:
      requests:
        cpu: 500m
        memory: 1Gi
```

## Validation Report

Generate validation summary:
```
Helm Chart Validation Report
============================
Chart: payment-service
Version: 1.0.0

✅ Structure Validation: PASSED
✅ Template Syntax: PASSED
✅ Values Organization: PASSED
✅ Dependencies: PASSED
✅ Security Defaults: PASSED
✅ Label Compliance: PASSED
✅ Helper Templates: PASSED
✅ Documentation: PASSED

Improvements Applied:
- Added missing labels
- Fixed template indentation
- Added security defaults
- Organized values.yaml
- Created values.schema.json
- Updated NOTES.txt

Warnings:
- Consider adding resource limits
- Add PodDisruptionBudget template
- Include backup/restore hooks

Score: A (95/100)
Status: Production Ready
```

## Best Practices

### Chart Structure
- Keep `values.yaml` organized with clear sections
- Document all values with comments
- Use consistent naming conventions
- Separate development and production configurations

### Template Design
- Use `_helpers.tpl` for reusable template snippets
- Implement proper label selectors
- Add resource limits to all containers
- Include health probes (liveness, readiness)

### Version Management
- Follow semantic versioning for chart versions
- Pin application versions in Chart.yaml
- Document breaking changes in NOTES.txt
- Maintain CHANGELOG.md for chart releases

### Security
- Never commit secrets to version control
- Use Kubernetes Secrets for sensitive data
- Implement RBAC with minimal permissions
- Scan images for vulnerabilities

### Testing
- Test with `helm lint` before every commit
- Validate with `helm template` to check output
- Use `helm test` for integration testing
- Test upgrades from previous versions

## Common Pitfalls

### ❌ Hardcoded Values in Templates

**Problem:**
```yaml
# templates/deployment.yaml
spec:
  replicas: 3  # Hardcoded!
  template:
    spec:
      containers:
      - image: myapp:1.0.0  # Hardcoded version!
```

**Solution:** Use values.yaml
```yaml
# values.yaml
replicaCount: 3
image:
  repository: myapp
  tag: 1.0.0

# templates/deployment.yaml
spec:
  replicas: {{ .Values.replicaCount }}
  template:
    spec:
      containers:
      - image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
```

### ❌ Missing Resource Limits

**Problem:**
```yaml
containers:
- name: app
  image: {{ .Values.image.repository }}
  # No resources defined - can consume unlimited CPU/memory!
```

**Solution:** Always define resource limits
```yaml
containers:
- name: app
  image: {{ .Values.image.repository }}
  resources:
    requests:
      memory: "128Mi"
      cpu: "100m"
    limits:
      memory: "256Mi"
      cpu: "200m"
```

### ❌ Incorrect Label Selectors

**Problem:**
```yaml
# Service can't find pods because labels don't match
apiVersion: v1
kind: Service
metadata:
  name: {{ .Release.Name }}
spec:
  selector:
    app: myapp  # Hardcoded
---
apiVersion: apps/v1
kind: Deployment
spec:
  selector:
    matchLabels:
      app: {{ include "myapp.name" . }}  # Dynamic - doesn't match!
```

**Solution:** Use helpers for consistency
```yaml
{{/* _helpers.tpl */}}
{{- define "myapp.labels" -}}
app: {{ include "myapp.name" . }}
release: {{ .Release.Name }}
{{- end }}

# Both Service and Deployment use same labels
selector:
  {{- include "myapp.labels" . | nindent 4 }}
```

### ❌ Not Testing Chart Installation

**Problem:** Chart fails on first install in production

**Solution:** Test locally before deploying
```bash
# Lint the chart
helm lint ./mychart

# Dry-run install to check output
helm install --dry-run --debug myrelease ./mychart

# Template and pipe to kubectl for validation
helm template myrelease ./mychart | kubectl apply --dry-run=client -f -
```

### ❌ Breaking Changes Without Version Bump

**Problem:** Changed required values without MAJOR version bump

**Solution:** Follow semantic versioning
- MAJOR: Breaking changes (removed/renamed values)
- MINOR: New features (new optional values)
- PATCH: Bug fixes (template corrections)

### ❌ Missing Dependencies

**Problem:**
```yaml
# Chart.yaml
dependencies:
- name: postgresql
  version: "12.0.0"
  repository: "https://charts.bitnami.com/bitnami"
# But forgot to run 'helm dependency update'!
```

**Solution:** Always update dependencies
```bash
helm dependency update ./mychart
# This creates charts/ directory with dependency .tgz files
```

## Related Skills

- **k8s-optimizer**: Optimizes Kubernetes manifests within Helm templates
- **iac-compliance**: Ensures Helm charts meet compliance requirements
- **docker-security**: Validates container images referenced in charts
- **yaml-validator**: Validates YAML syntax in all chart files

This skill ensures every Helm chart is properly structured, follows best practices, and is ready for production deployment.
