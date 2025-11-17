---
name: helm-validator
description: Validate and improve Helm charts
allowed-tools: Read, Edit
---

# Helm Validator Skill

## Purpose
This skill automatically validates and improves Helm charts when they are created or edited, ensuring they follow best practices and are production-ready.

## Auto-Invocation Context

This skill triggers when:
- Creating new Helm charts
- Editing Chart.yaml files
- Modifying values.yaml
- Working with Helm templates
- Updating chart dependencies

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
    # kubernetes.io/ingress.class: nginx
    # kubernetes.io/tls-acme: "true"
  hosts:
    - host: chart-example.local
      paths:
        - path: /
          pathType: ImplementationSpecific
  tls: []
  #  - secretName: chart-example-tls
  #    hosts:
  #      - chart-example.local

# Resources
resources: {}
  # We usually recommend not to specify default resources
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
  # targetMemoryUtilizationPercentage: 80

# Node selection
nodeSelector: {}

tolerations: []

affinity: {}
```

### 4. Dependency Version Management

```yaml
# Check dependency versions
dependencies:
  - name: postgresql
    version: "12.1.9"  # ✗ Exact version (fragile)
    version: "~12.1.9"  # ✓ Patch updates allowed
    version: "^12.1.9"  # ✓ Minor updates allowed
    version: ">=12.1.9 <13.0.0"  # ✓ Range specified

# Validate repository URLs
repository: "https://charts.bitnami.com/bitnami"  # ✓ Valid
repository: "bitnami"  # ✗ Missing URL
```

### 5. Security Best Practices

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
    password: ""  # ✗ Empty default
    password: "changeme"  # ✗ Weak default
    existingSecret: ""  # ✓ Use existing secret
```

### 6. Label Standards

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

### 7. Helper Template Validation

```yaml
# _helpers.tpl best practices
{{- define "chart.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{- define "chart.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{- define "chart.labels" -}}
helm.sh/chart: {{ include "chart.chart" . }}
{{ include "chart.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}
```

### 8. NOTES.txt Template

```
CHART NAME: {{ .Chart.Name }}
CHART VERSION: {{ .Chart.Version }}
APP VERSION: {{ .Chart.AppVersion }}

** Please be patient while the chart is being deployed **

{{- if .Values.ingress.enabled }}

1. Get the application URL by running:

{{- range $host := .Values.ingress.hosts }}
  {{- range .paths }}
  http{{ if $.Values.ingress.tls }}s{{ end }}://{{ $host.host }}{{ .path }}
  {{- end }}
{{- end }}

{{- else if contains "NodePort" .Values.service.type }}

1. Get the application URL by running:
  export NODE_PORT=$(kubectl get --namespace {{ .Release.Namespace }} -o jsonpath="{.spec.ports[0].nodePort}" services {{ include "chart.fullname" . }})
  export NODE_IP=$(kubectl get nodes --namespace {{ .Release.Namespace }} -o jsonpath="{.items[0].status.addresses[0].address}")
  echo http://$NODE_IP:$NODE_PORT

{{- else if contains "LoadBalancer" .Values.service.type }}

1. Get the application URL by running:
     NOTE: It may take a few minutes for the LoadBalancer IP to be available.
  export SERVICE_IP=$(kubectl get svc --namespace {{ .Release.Namespace }} {{ include "chart.fullname" . }} --template "{{ "{{ range (index .status.loadBalancer.ingress 0) }}{{.}}{{ end }}" }}")
  echo http://$SERVICE_IP:{{ .Values.service.port }}

{{- else }}

1. Get the application URL by running:
  kubectl --namespace {{ .Release.Namespace }} port-forward service/{{ include "chart.fullname" . }} 8080:{{ .Values.service.port }}
  echo "Visit http://127.0.0.1:8080 to use your application"

{{- end }}

2. Monitor the deployment:
  kubectl --namespace {{ .Release.Namespace }} get pods -l "app.kubernetes.io/name={{ include "chart.name" . }},app.kubernetes.io/instance={{ .Release.Name }}"
```

### 9. Schema Validation

Create values.schema.json:
```json
{
  "$schema": "https://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["image", "service"],
  "properties": {
    "replicaCount": {
      "type": "integer",
      "minimum": 1
    },
    "image": {
      "type": "object",
      "required": ["repository"],
      "properties": {
        "repository": {
          "type": "string",
          "pattern": "^[a-z0-9-_/]+$"
        },
        "tag": {
          "type": "string"
        },
        "pullPolicy": {
          "type": "string",
          "enum": ["Always", "IfNotPresent", "Never"]
        }
      }
    },
    "service": {
      "type": "object",
      "properties": {
        "type": {
          "type": "string",
          "enum": ["ClusterIP", "NodePort", "LoadBalancer", "ExternalName"]
        },
        "port": {
          "type": "integer",
          "minimum": 1,
          "maximum": 65535
        }
      }
    }
  }
}
```

### 10. Test Templates

```yaml
# templates/tests/test-connection.yaml
apiVersion: v1
kind: Pod
metadata:
  name: "{{ include "chart.fullname" . }}-test-connection"
  labels:
    {{- include "chart.labels" . | nindent 4 }}
  annotations:
    "helm.sh/hook": test
spec:
  containers:
    - name: wget
      image: busybox
      command: ['wget']
      args: ['{{ include "chart.fullname" . }}:{{ .Values.service.port }}']
  restartPolicy: Never
```

## Validation Report

Generate validation summary:
```
Helm Chart Validation Report
============================
Chart: my-app
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

This skill ensures every Helm chart is properly structured, follows best practices, and is ready for production deployment.