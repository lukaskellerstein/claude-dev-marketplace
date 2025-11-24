---
name: k8s-best-practices
description: Auto-invoked when working with Kubernetes manifests to ensure production-ready configurations and best practices
allowed-tools: Read, Grep, Glob
---

# Kubernetes Best Practices

This skill provides guidance on Kubernetes best practices for production deployments.

## When Active

This skill activates when you:
- Create or modify Kubernetes manifests (YAML files)
- Design Kubernetes deployments or configurations
- Review existing Kubernetes resources
- Troubleshoot Kubernetes applications
- Set up monitoring or scaling

## Resource Configuration Best Practices

### 1. Always Set Resource Requests and Limits

**Why**: Ensures proper scheduling and prevents resource starvation

```yaml
resources:
  requests:
    cpu: 100m      # Minimum guaranteed CPU
    memory: 128Mi  # Minimum guaranteed memory
  limits:
    cpu: 500m      # Maximum CPU allowed
    memory: 512Mi  # Maximum memory allowed
```

**Guidelines**:
- Set requests based on average usage
- Set limits based on peak usage with some headroom
- Memory limits should be close to requests (avoid OOM kills)
- CPU limits can be higher than requests (CPU is throttled, not killed)
- Test under load to determine appropriate values

### 2. Configure Health Checks

**Liveness Probe**: Restart container if unhealthy
```yaml
livenessProbe:
  httpGet:
    path: /healthz
    port: 8080
  initialDelaySeconds: 30  # Wait before first check
  periodSeconds: 10        # Check every 10 seconds
  timeoutSeconds: 5        # Request timeout
  failureThreshold: 3      # Restart after 3 failures
```

**Readiness Probe**: Remove from load balancer if not ready
```yaml
readinessProbe:
  httpGet:
    path: /ready
    port: 8080
  initialDelaySeconds: 10  # Start checking sooner
  periodSeconds: 5         # Check more frequently
  timeoutSeconds: 3
  failureThreshold: 3
```

**Guidelines**:
- Always define both liveness and readiness probes
- Readiness should check dependencies (DB, cache)
- Liveness should be lightweight (doesn't check external deps)
- Use different endpoints for liveness vs readiness
- Set appropriate initialDelaySeconds for startup time

### 3. Use Rolling Update Strategy

```yaml
strategy:
  type: RollingUpdate
  rollingUpdate:
    maxSurge: 1        # Create 1 extra pod during update
    maxUnavailable: 0  # Don't terminate any pods until new ones are ready
```

**Guidelines**:
- For zero-downtime: `maxUnavailable: 0` and `maxSurge: 1`
- For faster updates: increase `maxSurge` and `maxUnavailable`
- Set `revisionHistoryLimit: 10` to keep rollback history
- Test rollbacks in staging environment

### 4. Configure Pod Disruption Budgets

```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: web-app-pdb
spec:
  minAvailable: 2  # or maxUnavailable: 1
  selector:
    matchLabels:
      app: web-app
```

**Guidelines**:
- Ensures minimum replicas during voluntary disruptions
- Use `minAvailable` for absolute numbers
- Use `maxUnavailable` for percentage-based
- Essential for cluster upgrades and node maintenance

### 5. Use Labels and Annotations Properly

**Labels** (for selection and grouping):
```yaml
metadata:
  labels:
    app: web-app
    version: v1.0.0
    environment: production
    tier: frontend
    managed-by: helm
```

**Annotations** (for metadata):
```yaml
metadata:
  annotations:
    prometheus.io/scrape: "true"
    prometheus.io/port: "8080"
    prometheus.io/path: "/metrics"
    description: "Frontend web application"
    docs: "https://docs.example.com/web-app"
```

**Guidelines**:
- Use consistent label schema across all resources
- Labels should be short and standardized
- Annotations for longer, descriptive metadata
- Don't put sensitive data in labels or annotations

## Security Best Practices

### 1. Run as Non-Root User

```yaml
securityContext:
  runAsNonRoot: true
  runAsUser: 1000
  runAsGroup: 1000
  fsGroup: 1000
  allowPrivilegeEscalation: false
```

**Guidelines**:
- Always run containers as non-root
- Set specific UID/GID, don't rely on defaults
- Disable privilege escalation
- Set fsGroup for volume permissions

### 2. Use Read-Only Root Filesystem

```yaml
securityContext:
  readOnlyRootFilesystem: true

volumeMounts:
  - name: tmp
    mountPath: /tmp
  - name: cache
    mountPath: /var/cache

volumes:
  - name: tmp
    emptyDir: {}
  - name: cache
    emptyDir: {}
```

**Guidelines**:
- Enhances security by preventing file modifications
- Mount emptyDir volumes for writable directories
- Use tmpfs for temporary data

### 3. Drop Unnecessary Capabilities

```yaml
securityContext:
  capabilities:
    drop:
      - ALL
    add:
      - NET_BIND_SERVICE  # Only if needed
```

**Guidelines**:
- Drop ALL capabilities by default
- Add only required capabilities
- Most apps don't need any special capabilities

### 4. Use Network Policies

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: web-app-netpol
spec:
  podSelector:
    matchLabels:
      app: web-app
  policyTypes:
    - Ingress
    - Egress
  ingress:
    - from:
        - podSelector:
            matchLabels:
              app: nginx-ingress
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

**Guidelines**:
- Implement default deny-all policy
- Allow only necessary traffic
- Use label selectors for flexibility
- Test thoroughly in staging

### 5. Manage Secrets Securely

```yaml
env:
  - name: DATABASE_URL
    valueFrom:
      secretKeyRef:
        name: db-credentials
        key: url
  - name: API_KEY
    valueFrom:
      secretKeyRef:
        name: api-credentials
        key: api-key

# Or use volume mounts
volumeMounts:
  - name: secrets
    mountPath: /etc/secrets
    readOnly: true
volumes:
  - name: secrets
    secret:
      secretName: app-secrets
```

**Guidelines**:
- Never hardcode secrets in manifests
- Use Kubernetes Secrets or external secret managers
- Use GCP Secret Manager with Workload Identity
- Mount secrets as volumes for files, env vars for simple values
- Enable encryption at rest in etcd

## Deployment Best Practices

### 1. Use Multiple Replicas

```yaml
spec:
  replicas: 3  # Minimum for production
```

**Guidelines**:
- Minimum 3 replicas for high availability
- Use HPA for auto-scaling
- Consider pod anti-affinity for zone distribution

### 2. Configure Pod Anti-Affinity

```yaml
affinity:
  podAntiAffinity:
    preferredDuringSchedulingIgnoredDuringExecution:
      - weight: 100
        podAffinityTerm:
          labelSelector:
            matchLabels:
              app: web-app
          topologyKey: kubernetes.io/hostname
```

**Guidelines**:
- Use `preferred` for soft anti-affinity (recommended)
- Use `required` for hard anti-affinity (careful with small clusters)
- Spread across zones for higher availability: `topology.kubernetes.io/zone`

### 3. Set Up Horizontal Pod Autoscaler

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: web-app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: web-app
  minReplicas: 3
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
```

**Guidelines**:
- Set reasonable min/max replica counts
- Target 60-80% CPU utilization
- Consider multiple metrics (CPU + memory)
- Test scaling behavior under load

## Service and Networking

### 1. Use Appropriate Service Types

```yaml
apiVersion: v1
kind: Service
metadata:
  name: web-app
spec:
  type: ClusterIP  # Default, for internal services
  selector:
    app: web-app
  ports:
    - name: http
      port: 80
      targetPort: 8080
      protocol: TCP
  sessionAffinity: ClientIP  # If needed for sticky sessions
```

**Service Types**:
- **ClusterIP**: Internal services (default, most common)
- **NodePort**: Expose on each node's IP (rarely used directly)
- **LoadBalancer**: External load balancer (cloud provider)
- **ExternalName**: DNS CNAME for external service

### 2. Configure Ingress Properly

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: web-app
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/rate-limit: "100"
spec:
  ingressClassName: nginx
  tls:
    - hosts:
        - app.example.com
      secretName: web-app-tls
  rules:
    - host: app.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: web-app
                port:
                  number: 80
```

**Guidelines**:
- Always use TLS in production
- Configure rate limiting
- Use path-based routing when appropriate
- Set appropriate timeouts

## ConfigMap and Environment Variables

### 1. Use ConfigMaps for Configuration

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  LOG_LEVEL: "info"
  MAX_CONNECTIONS: "100"
  config.yaml: |
    database:
      pool_size: 10
      timeout: 30
```

**Usage**:
```yaml
# As environment variables
envFrom:
  - configMapRef:
      name: app-config

# As individual env vars
env:
  - name: LOG_LEVEL
    valueFrom:
      configMapKeyRef:
        name: app-config
        key: LOG_LEVEL

# As mounted file
volumeMounts:
  - name: config
    mountPath: /etc/config
volumes:
  - name: config
    configMap:
      name: app-config
```

## Storage Best Practices

### 1. Use Persistent Volumes Properly

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: data-pvc
spec:
  accessModes:
    - ReadWriteOnce  # Single node read/write
  storageClassName: standard-rwo  # Use appropriate storage class
  resources:
    requests:
      storage: 10Gi
```

**Access Modes**:
- **ReadWriteOnce (RWO)**: Single node, most common
- **ReadOnlyMany (ROX)**: Multiple nodes read-only
- **ReadWriteMany (RWX)**: Multiple nodes read/write (rare, expensive)

**Guidelines**:
- Choose appropriate storage class (SSD vs HDD)
- Set reasonable size with room for growth
- Consider backup strategy
- Use StatefulSets for stateful applications

## Monitoring and Logging

### 1. Add Prometheus Annotations

```yaml
metadata:
  annotations:
    prometheus.io/scrape: "true"
    prometheus.io/port: "8080"
    prometheus.io/path: "/metrics"
```

### 2. Configure Proper Logging

```yaml
# Use structured logging in application
# Log to stdout/stderr (captured by Kubernetes)

# Add log parsing annotations for log aggregation
metadata:
  annotations:
    fluentd.io/parser: "json"
```

## Namespace Organization

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: production
  labels:
    environment: production
    team: platform

---
apiVersion: v1
kind: ResourceQuota
metadata:
  name: compute-quota
  namespace: production
spec:
  hard:
    requests.cpu: "100"
    requests.memory: "200Gi"
    limits.cpu: "200"
    limits.memory: "400Gi"
    persistentvolumeclaims: "50"

---
apiVersion: v1
kind: LimitRange
metadata:
  name: default-limits
  namespace: production
spec:
  limits:
    - type: Container
      default:
        cpu: "500m"
        memory: "512Mi"
      defaultRequest:
        cpu: "100m"
        memory: "128Mi"
```

## Common Issues and Solutions

### Issue: Pods Crashing or CrashLoopBackOff
- Check logs: `kubectl logs pod-name`
- Check events: `kubectl describe pod pod-name`
- Verify health check endpoints are working
- Check resource limits (might be OOM killed)
- Verify image pull policy and image availability

### Issue: Pods Pending
- Check node resources: `kubectl top nodes`
- Check events: `kubectl describe pod pod-name`
- Verify PVC is bound
- Check node selectors and taints/tolerations

### Issue: Service Not Accessible
- Verify Service selector matches Pod labels
- Check if Pods are ready: `kubectl get pods`
- Test from within cluster: `kubectl run -it --rm debug --image=busybox --restart=Never -- wget -O- service-name`
- Check NetworkPolicies

## Checklist

Before deploying to production:
- [ ] Resource requests and limits are set
- [ ] Liveness and readiness probes are configured
- [ ] Running as non-root user
- [ ] Read-only root filesystem where possible
- [ ] Secrets are managed securely (not in Git)
- [ ] Multiple replicas for high availability
- [ ] HPA configured for auto-scaling
- [ ] Pod disruption budget defined
- [ ] Network policies implemented
- [ ] Ingress has TLS configured
- [ ] Monitoring annotations added
- [ ] Logging is properly configured
- [ ] Resource quotas set for namespace
- [ ] Labels follow consistent schema
- [ ] Documentation includes deployment instructions

Use this guidance to ensure Kubernetes deployments are production-ready, secure, and follow best practices.
