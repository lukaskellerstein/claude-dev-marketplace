---
name: k8s-optimizer
description: Optimize Kubernetes resource definitions automatically
allowed-tools: Read, Edit
---

# Kubernetes Optimizer Skill

## Purpose
This skill automatically activates when creating or editing Kubernetes manifests to ensure optimal resource utilization, high availability, and production readiness.

## Auto-Invocation Context

This skill triggers when:
- Creating Kubernetes YAML files
- Editing Deployments, StatefulSets, or DaemonSets
- Defining Services or Ingresses
- Working with any Kubernetes resource definitions

## Optimizations Applied

### 1. Resource Limits and Requests
Automatically add resource management:
```yaml
# Before
spec:
  containers:
  - name: app
    image: myapp:1.0.0

# After optimization
spec:
  containers:
  - name: app
    image: myapp:1.0.0
    resources:
      requests:
        memory: "256Mi"
        cpu: "250m"
      limits:
        memory: "512Mi"
        cpu: "500m"
```

### 2. Health Probes
Add comprehensive health checks:
```yaml
# Added automatically
livenessProbe:
  httpGet:
    path: /health
    port: 8080
  initialDelaySeconds: 30
  periodSeconds: 10
  timeoutSeconds: 5
  successThreshold: 1
  failureThreshold: 3

readinessProbe:
  httpGet:
    path: /ready
    port: 8080
  initialDelaySeconds: 5
  periodSeconds: 5
  timeoutSeconds: 3
  successThreshold: 1
  failureThreshold: 3

startupProbe:
  httpGet:
    path: /startup
    port: 8080
  initialDelaySeconds: 0
  periodSeconds: 10
  timeoutSeconds: 3
  successThreshold: 1
  failureThreshold: 30
```

### 3. Security Context
Enforce security best practices:
```yaml
# Pod level security
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    fsGroup: 2000
    seccompProfile:
      type: RuntimeDefault

  # Container level security
  containers:
  - name: app
    securityContext:
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
      capabilities:
        drop:
        - ALL
        add:
        - NET_BIND_SERVICE
```

### 4. Autoscaling Configuration
Add HorizontalPodAutoscaler:
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: app
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 50
        periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
      - type: Percent
        value: 100
        periodSeconds: 60
```

### 5. Pod Disruption Budget
Ensure availability during updates:
```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: app-pdb
spec:
  minAvailable: 1
  # OR
  maxUnavailable: 1
  selector:
    matchLabels:
      app: myapp
```

### 6. Anti-Affinity Rules
Distribute pods across nodes:
```yaml
spec:
  affinity:
    podAntiAffinity:
      preferredDuringSchedulingIgnoredDuringExecution:
      - weight: 100
        podAffinityTerm:
          labelSelector:
            matchExpressions:
            - key: app
              operator: In
              values:
              - myapp
          topologyKey: kubernetes.io/hostname
```

### 7. Topology Spread Constraints
Better distribution across zones:
```yaml
spec:
  topologySpreadConstraints:
  - maxSkew: 1
    topologyKey: topology.kubernetes.io/zone
    whenUnsatisfiable: DoNotSchedule
    labelSelector:
      matchLabels:
        app: myapp
  - maxSkew: 1
    topologyKey: kubernetes.io/hostname
    whenUnsatisfiable: ScheduleAnyway
    labelSelector:
      matchLabels:
        app: myapp
```

### 8. Service Configuration
Optimize service definitions:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: app-service
  annotations:
    # Cloud provider specific optimizations
    service.beta.kubernetes.io/aws-load-balancer-type: "nlb"
    service.beta.kubernetes.io/aws-load-balancer-cross-zone-load-balancing-enabled: "true"
spec:
  type: LoadBalancer
  sessionAffinity: ClientIP
  sessionAffinityConfig:
    clientIP:
      timeoutSeconds: 10800
  ports:
  - port: 80
    targetPort: 8080
    protocol: TCP
    name: http
```

### 9. ConfigMap and Secret Management
Optimize configuration:
```yaml
# Add checksums to trigger pod restarts on config changes
spec:
  template:
    metadata:
      annotations:
        checksum/config: {{ include (print $.Template.BasePath "/configmap.yaml") . | sha256sum }}
        checksum/secret: {{ include (print $.Template.BasePath "/secret.yaml") . | sha256sum }}
```

### 10. Network Policies
Add network segmentation:
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: app-netpol
spec:
  podSelector:
    matchLabels:
      app: myapp
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          role: frontend
    ports:
    - protocol: TCP
      port: 8080
  egress:
  - to:
    - podSelector:
        matchLabels:
          role: database
    ports:
    - protocol: TCP
      port: 5432
```

## Deployment Strategy Optimization

### Rolling Update Configuration
```yaml
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  minReadySeconds: 30
  progressDeadlineSeconds: 600
  revisionHistoryLimit: 10
```

## Quality of Service (QoS) Classes

Ensure appropriate QoS:
- **Guaranteed**: Requests = Limits for all resources
- **Burstable**: Requests < Limits
- **BestEffort**: No requests or limits (avoid in production)

## Labels and Annotations

Add standard labels:
```yaml
metadata:
  labels:
    app: myapp
    version: v1.0.0
    component: backend
    part-of: myapp-system
    managed-by: helm
    environment: production
  annotations:
    prometheus.io/scrape: "true"
    prometheus.io/port: "9090"
    prometheus.io/path: "/metrics"
```

## Priority Classes

Add pod priority:
```yaml
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: high-priority
value: 1000
globalDefault: false
description: "High priority class for critical services"

---
spec:
  priorityClassName: high-priority
```

## Optimization Report

Generate optimization summary:
```
Kubernetes Manifest Optimization Report
========================================
✅ Resource limits/requests added
✅ Health probes configured
✅ Security context applied
✅ Autoscaling enabled
✅ Pod disruption budget created
✅ Anti-affinity rules added
✅ Network policies defined

Estimated improvements:
- Resource utilization: +40% efficiency
- Availability: 99.9% uptime
- Security score: A+ rating
- Cost optimization: -30% resource waste
```

This skill ensures that every Kubernetes resource is optimized for production use, improving reliability, security, and cost-effectiveness.