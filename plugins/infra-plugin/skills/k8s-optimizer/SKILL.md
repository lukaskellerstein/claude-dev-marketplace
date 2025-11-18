---
name: k8s-optimizer
description: Master Kubernetes optimization and best practices. Use when creating YAML files, editing Deployments/StatefulSets, defining Services/Ingresses, working with resource definitions, ensuring production readiness, or when discussing Kubernetes resource optimization, pod resource limits, autoscaling strategies, high availability, pod disruption budgets, node affinity, taints and tolerations, or performance tuning.
allowed-tools: Read, Edit
---

# Kubernetes Optimizer Skill

Master Kubernetes resource optimization to ensure optimal utilization, high availability, and production-ready configurations for all Kubernetes workloads.

## When to Use This Skill

Use this skill when:

1. Creating Kubernetes YAML manifest files
2. Editing Deployments, StatefulSets, or DaemonSets
3. Defining Services or Ingresses
4. Working with any Kubernetes resource definitions
5. Implementing autoscaling configurations
6. Setting up pod disruption budgets
7. Configuring health probes and readiness checks
8. Defining resource limits and requests
9. Implementing pod anti-affinity rules
10. Creating network policies
11. Deploying stateful applications
12. Optimizing CI/CD deployment pipelines
13. Troubleshooting resource contention issues
14. Migrating applications to Kubernetes
15. Reviewing Kubernetes manifests for production readiness

## Quick Start

This skill automatically optimizes manifests as you create them:

```yaml
# You write:
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  containers:
  - name: app
    image: myapp:1.0

# Skill auto-enhances:
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 2  # Added for HA
  containers:
  - name: app
    image: myapp:1.0
    # Auto-added resource limits
    resources:
      requests:
        cpu: 250m
        memory: 256Mi
      limits:
        cpu: 500m
        memory: 512Mi
    # Auto-added health probes
    livenessProbe:
      httpGet:
        path: /health
        port: 8080
    readinessProbe:
      httpGet:
        path: /ready
        port: 8080
    # Auto-added security context
    securityContext:
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true

✅ Optimizations applied: Resource limits, health probes, security context
```

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

## Real-World Applications

### High-Traffic Web Application

**Scenario:** E-commerce platform handling millions of requests

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-frontend
spec:
  replicas: 10  # High availability
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 3
      maxUnavailable: 0  # Zero downtime deployments

  template:
    spec:
      # Spread across zones for disaster recovery
      topologySpreadConstraints:
      - maxSkew: 1
        topologyKey: topology.kubernetes.io/zone
        whenUnsatisfiable: DoNotSchedule
        labelSelector:
          matchLabels:
            app: web-frontend

      containers:
      - name: web
        image: company/web:v2.5.0
        # Right-sized resources based on metrics
        resources:
          requests:
            cpu: 500m
            memory: 1Gi
          limits:
            cpu: 1000m
            memory: 2Gi

        # Comprehensive health checks
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
          failureThreshold: 3

        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5

        # Graceful shutdown
        lifecycle:
          preStop:
            exec:
              command: ["/bin/sh", "-c", "sleep 15"]

---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: web-frontend-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: web-frontend
  minReplicas: 10
  maxReplicas: 100
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
        value: 10  # Scale down slowly
        periodSeconds: 60
```

### Stateful Database Workload

**Scenario:** PostgreSQL database cluster with high availability

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres
spec:
  serviceName: postgres
  replicas: 3  # Primary + 2 replicas

  template:
    spec:
      # Anti-affinity to spread across nodes
      affinity:
        podAntiAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
          - labelSelector:
              matchExpressions:
              - key: app
                operator: In
                values:
                - postgres
            topologyKey: kubernetes.io/hostname

      containers:
      - name: postgres
        image: postgres:15
        # Database-optimized resources
        resources:
          requests:
            cpu: 2000m
            memory: 4Gi
          limits:
            cpu: 4000m
            memory: 8Gi

        # Persistent storage
        volumeMounts:
        - name: data
          mountPath: /var/lib/postgresql/data

        # Database health checks
        livenessProbe:
          exec:
            command:
            - pg_isready
            - -U
            - postgres
          initialDelaySeconds: 30
          periodSeconds: 10

        readinessProbe:
          exec:
            command:
            - pg_isready
            - -U
            - postgres
          initialDelaySeconds: 5
          periodSeconds: 5

  volumeClaimTemplates:
  - metadata:
      name: data
    spec:
      accessModes: ["ReadWriteOnce"]
      storageClassName: fast-ssd
      resources:
        requests:
          storage: 100Gi

---
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: postgres-pdb
spec:
  minAvailable: 2  # Always keep 2 replicas running
  selector:
    matchLabels:
      app: postgres
```

### Microservices with Service Mesh

**Scenario:** Complex microservices architecture

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: payment-service
spec:
  replicas: 5

  template:
    metadata:
      annotations:
        # Istio sidecar injection
        sidecar.istio.io/inject: "true"
        # Prometheus scraping
        prometheus.io/scrape: "true"
        prometheus.io/port: "9090"

    spec:
      serviceAccountName: payment-service

      containers:
      - name: payment
        image: company/payment-service:v3.2.1
        # Optimized for fast transactions
        resources:
          requests:
            cpu: 1000m
            memory: 2Gi
          limits:
            cpu: 2000m
            memory: 4Gi

        # Transaction health checks
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 45
          timeoutSeconds: 5

        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 3

        # Sensitive env vars from secrets
        envFrom:
        - secretRef:
            name: payment-secrets

        # Security hardening
        securityContext:
          runAsNonRoot: true
          runAsUser: 1000
          allowPrivilegeEscalation: false
          capabilities:
            drop:
            - ALL
          readOnlyRootFilesystem: true

---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: payment-service-netpol
spec:
  podSelector:
    matchLabels:
      app: payment-service
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: api-gateway
    ports:
    - protocol: TCP
      port: 8080
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: postgres
    ports:
    - protocol: TCP
      port: 5432
```

## Best Practices

### Resource Management
- Always define resource requests and limits
- Set requests based on actual usage (p50-p90)
- Set limits at p99 + 20% headroom
- Use Vertical Pod Autoscaler for initial sizing

### High Availability
- Run at least 3 replicas for critical services
- Use Pod Disruption Budgets to prevent outages
- Implement liveness and readiness probes
- Spread replicas across availability zones

### Security
- Never run containers as root
- Use read-only root filesystems
- Drop all capabilities, add only required ones
- Scan images for vulnerabilities regularly

### Observability
- Add meaningful labels for filtering/grouping
- Implement structured logging to stdout
- Export Prometheus metrics
- Use distributed tracing for microservices

### Configuration
- Store secrets in Kubernetes Secrets, not ConfigMaps
- Use external secret management (Vault, GCP Secret Manager)
- Version all manifests in Git
- Use Kustomize or Helm for environment differences

## Common Pitfalls

### ❌ No Resource Limits

**Problem:**
```yaml
containers:
- name: app
  image: myapp:latest
  # No resources - can OOM the node!
```

**Solution:** Always set resource limits
```yaml
containers:
- name: app
  image: myapp:latest
  resources:
    requests:
      memory: "128Mi"
      cpu: "100m"
    limits:
      memory: "256Mi"
      cpu: "500m"
```

### ❌ Running as Root

**Problem:**
```yaml
containers:
- name: app
  image: myapp:latest
  # Runs as root by default - security risk!
```

**Solution:** Run as non-root user
```yaml
containers:
- name: app
  image: myapp:latest
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    capabilities:
      drop:
        - ALL
```

### ❌ Missing Health Probes

**Problem:**
```yaml
containers:
- name: app
  image: myapp:latest
  # No probes - K8s doesn't know if app is healthy!
```

**Solution:** Add liveness and readiness probes
```yaml
containers:
- name: app
  image: myapp:latest
  livenessProbe:
    httpGet:
      path: /healthz
      port: 8080
    initialDelaySeconds: 30
    periodSeconds: 10
  readinessProbe:
    httpGet:
      path: /ready
      port: 8080
    initialDelaySeconds: 5
    periodSeconds: 5
```

### ❌ Single Replica for Critical Services

**Problem:**
```yaml
spec:
  replicas: 1  # Single point of failure!
```

**Solution:** Run multiple replicas with PDB
```yaml
spec:
  replicas: 3  # High availability
---
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: myapp-pdb
spec:
  minAvailable: 2
  selector:
    matchLabels:
      app: myapp
```

### ❌ Latest Image Tag

**Problem:**
```yaml
containers:
- name: app
  image: myapp:latest  # Unpredictable, can break deployments!
```

**Solution:** Use specific version tags
```yaml
containers:
- name: app
  image: myapp:v1.2.3  # Reproducible deployments
  imagePullPolicy: IfNotPresent
```

### ❌ No Pod Disruption Budget

**Problem:** Cluster autoscaler or manual drains evict all pods at once

**Solution:** Define PDB to maintain availability
```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: critical-app-pdb
spec:
  maxUnavailable: 1  # Only one pod can be down
  selector:
    matchLabels:
      app: critical-app
```

### ❌ Storing Secrets in ConfigMaps

**Problem:**
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  database_password: "secret123"  # Plain text!
```

**Solution:** Use Secrets with encryption at rest
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
type: Opaque
data:
  database_password: c2VjcmV0MTIz  # Base64 encoded
```

### ❌ Not Setting Priority Class

**Problem:** All pods have same priority during resource pressure

**Solution:** Set priority for critical workloads
```yaml
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: high-priority
value: 1000
---
spec:
  priorityClassName: high-priority  # Won't be evicted first
  containers:
  - name: critical-app
```

## Related Skills

- **helm-validator**: Optimizes Helm charts containing Kubernetes manifests
- **gcp-cost-guard**: Ensures resource limits are cost-effective
- **iac-compliance**: Validates Kubernetes configs meet security standards
- **docker-security**: Ensures container images are secure

This skill ensures that every Kubernetes resource is optimized for production use, improving reliability, security, and cost-effectiveness.