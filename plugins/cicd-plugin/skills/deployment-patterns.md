---
name: deployment-patterns
description: Auto-invoked when designing or implementing deployments to ensure proper deployment patterns and strategies
allowed-tools: Read, Grep, Glob
---

# Deployment Patterns

This skill provides guidance on deployment patterns and strategies for achieving zero-downtime deployments with proper rollback capabilities.

## When Active

This skill activates when you:
- Design deployment strategies
- Create Kubernetes deployment manifests
- Configure cloud service deployments
- Implement infrastructure as code
- Work with database migrations
- Set up health checks and monitoring

## Deployment Strategies

### Rolling Update (Default)
Best for: Most applications requiring zero downtime

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1        # Can have 4 pods during rollout
      maxUnavailable: 0  # Always maintain 3 pods minimum
  template:
    spec:
      containers:
      - name: app
        image: myapp:v2.0.0
        readinessProbe:
          httpGet:
            path: /health/ready
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 5
          failureThreshold: 3
```

**Characteristics:**
- Updates pods gradually (one at a time by default)
- Zero downtime with proper configuration
- Low resource overhead
- Easy rollback with `kubectl rollout undo`
- Both old and new versions run simultaneously during rollout

**When to use:**
- Standard web applications
- Stateless services
- Backward compatible changes
- Most production deployments

### Blue-Green Deployment
Best for: Critical services requiring instant rollback

```yaml
# Blue deployment (current)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-blue
  labels:
    version: blue
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
      version: blue
  template:
    metadata:
      labels:
        app: myapp
        version: blue
    spec:
      containers:
      - name: app
        image: myapp:v1.0.0

---
# Green deployment (new)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-green
  labels:
    version: green
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
      version: green
  template:
    metadata:
      labels:
        app: myapp
        version: green
    spec:
      containers:
      - name: app
        image: myapp:v2.0.0

---
# Service switches between blue and green
apiVersion: v1
kind: Service
metadata:
  name: myapp
spec:
  selector:
    app: myapp
    version: blue  # Change to 'green' to switch
  ports:
  - port: 80
    targetPort: 8080
```

**Characteristics:**
- Two identical environments (blue and green)
- Instant traffic switch
- Easy instant rollback
- Requires double resources temporarily
- Full testing before cutover

**When to use:**
- Critical production services
- Major version upgrades
- When instant rollback is required
- When you can afford temporary double resources

### Canary Deployment
Best for: High-risk changes requiring progressive validation

```yaml
# Stable deployment (90% traffic)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-stable
spec:
  replicas: 9
  selector:
    matchLabels:
      app: myapp
      track: stable
  template:
    metadata:
      labels:
        app: myapp
        track: stable
    spec:
      containers:
      - name: app
        image: myapp:v1.0.0

---
# Canary deployment (10% traffic)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-canary
spec:
  replicas: 1
  selector:
    matchLabels:
      app: myapp
      track: canary
  template:
    metadata:
      labels:
        app: myapp
        track: canary
    spec:
      containers:
      - name: app
        image: myapp:v2.0.0

---
# Service includes both stable and canary
apiVersion: v1
kind: Service
metadata:
  name: myapp
spec:
  selector:
    app: myapp  # Matches both stable and canary
  ports:
  - port: 80
    targetPort: 8080
```

**Progressive Rollout:**
```
1. Deploy canary: 5% traffic
2. Monitor metrics for 1 hour
3. If healthy, increase to 25%
4. Monitor for 30 minutes
5. If healthy, increase to 50%
6. Monitor for 30 minutes
7. If healthy, increase to 100%
8. If issues detected at any point, rollback
```

**Characteristics:**
- Progressive traffic increase
- Minimizes blast radius
- Requires traffic splitting (Istio, Linkerd)
- Gradual validation with real users
- Easy rollback at any stage

**When to use:**
- High-risk changes (algorithm changes, new features)
- When you want to validate with real traffic
- When you have service mesh capability
- For gradual confidence building

### A/B Testing Deployment
Best for: Testing multiple versions simultaneously

```yaml
# Version A
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-a
spec:
  replicas: 3
  template:
    metadata:
      labels:
        app: myapp
        variant: a
    spec:
      containers:
      - name: app
        image: myapp:v1-with-feature-x

---
# Version B
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-b
spec:
  replicas: 3
  template:
    metadata:
      labels:
        app: myapp
        variant: b
    spec:
      containers:
      - name: app
        image: myapp:v1-with-feature-y

---
# Istio VirtualService for intelligent routing
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: myapp
spec:
  hosts:
  - myapp
  http:
  - match:
    - headers:
        user-type:
          exact: "premium"
    route:
    - destination:
        host: myapp
        subset: a
  - route:
    - destination:
        host: myapp
        subset: b
```

**Characteristics:**
- Multiple versions run simultaneously
- Traffic routing based on criteria (user segment, geography)
- Requires service mesh or intelligent routing
- Measure business metrics between variants

**When to use:**
- Testing different features or UX
- When you need to measure business impact
- For product experimentation
- When you have sophisticated routing capability

## Health Checks

### Readiness Probe
Determines if pod is ready to receive traffic

```yaml
readinessProbe:
  httpGet:
    path: /health/ready
    port: 8080
    httpHeaders:
    - name: Custom-Header
      value: Awesome
  initialDelaySeconds: 10  # Wait before first check
  periodSeconds: 5         # Check every 5 seconds
  timeoutSeconds: 3        # Timeout for each check
  successThreshold: 1      # Must succeed once
  failureThreshold: 3      # Fail after 3 failures
```

**Readiness endpoint should check:**
- Database connectivity
- Required dependencies availability
- Configuration loaded
- Caches warmed up
- Application fully initialized

**Implementation example:**
```javascript
app.get('/health/ready', async (req, res) => {
  try {
    // Check database
    await db.ping();

    // Check Redis
    await redis.ping();

    // Check required services
    await axios.get('http://auth-service/health');

    res.status(200).json({ status: 'ready' });
  } catch (error) {
    res.status(503).json({
      status: 'not ready',
      error: error.message
    });
  }
});
```

### Liveness Probe
Determines if pod is alive and should be restarted

```yaml
livenessProbe:
  httpGet:
    path: /health/live
    port: 8080
  initialDelaySeconds: 30  # Wait longer before first check
  periodSeconds: 10        # Check every 10 seconds
  timeoutSeconds: 5
  failureThreshold: 3      # Restart after 3 failures
```

**Liveness endpoint should check:**
- Application is running (not deadlocked)
- Critical threads are alive
- Memory is not exhausted
- No unrecoverable errors

**Implementation example:**
```javascript
app.get('/health/live', (req, res) => {
  // Simple check - is process responsive?
  // Don't check external dependencies here!
  res.status(200).json({ status: 'alive' });
});
```

### Startup Probe
Handles slow-starting containers

```yaml
startupProbe:
  httpGet:
    path: /health/startup
    port: 8080
  initialDelaySeconds: 0
  periodSeconds: 10
  failureThreshold: 30  # Allow 300s (5min) for startup
```

**Best Practices:**
- Readiness: Check dependencies, fail temporarily
- Liveness: Simple check, avoid checking dependencies
- Startup: Allow sufficient time for slow initialization
- All probes: Include timeout and failure thresholds
- Monitoring: Track probe failures in metrics

## Graceful Shutdown

### Kubernetes Configuration
```yaml
spec:
  terminationGracePeriodSeconds: 30  # Allow 30s for shutdown
  containers:
  - name: app
    lifecycle:
      preStop:
        exec:
          command: ["/bin/sh", "-c", "sleep 15"]  # Connection draining
```

### Application Implementation
```javascript
// Node.js example
let isShuttingDown = false;

// Handle SIGTERM
process.on('SIGTERM', async () => {
  console.log('SIGTERM received, starting graceful shutdown');
  isShuttingDown = true;

  // Stop accepting new connections
  server.close(async () => {
    console.log('HTTP server closed');

    // Close database connections
    await db.close();

    // Close Redis connections
    await redis.quit();

    // Exit cleanly
    process.exit(0);
  });

  // Force exit after timeout
  setTimeout(() => {
    console.error('Forced shutdown after timeout');
    process.exit(1);
  }, 25000);  // 25s (before k8s kills at 30s)
});

// Update readiness probe during shutdown
app.get('/health/ready', (req, res) => {
  if (isShuttingDown) {
    return res.status(503).json({ status: 'shutting down' });
  }
  res.status(200).json({ status: 'ready' });
});
```

## Database Migrations

### Zero-Downtime Migration Strategy

**Phase 1: Add new column (optional)**
```sql
-- Migration 1: Add column
ALTER TABLE users ADD COLUMN email_verified BOOLEAN DEFAULT false;
CREATE INDEX idx_users_email_verified ON users(email_verified);
```
Deploy application that writes to both old and new columns.

**Phase 2: Backfill data**
```sql
-- Migration 2: Backfill
UPDATE users
SET email_verified = true
WHERE confirmation_token IS NULL;
```

**Phase 3: Make required and remove old**
```sql
-- Migration 3: Make NOT NULL
ALTER TABLE users ALTER COLUMN email_verified SET NOT NULL;
ALTER TABLE users DROP COLUMN confirmation_token;
```
Deploy application that only uses new column.

### Migration Best Practices
- Never break backward compatibility in single deployment
- Add before removing (additive changes)
- Use feature flags for schema-dependent features
- Test rollback scenarios
- Keep migrations small and focused
- Use transactions where possible
- Have rollback scripts ready

### Flyway Example
```yaml
# V1__create_users.sql
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL UNIQUE
);

# V2__add_email_verification.sql
ALTER TABLE users ADD COLUMN email_verified BOOLEAN DEFAULT false;
CREATE INDEX idx_users_email_verified ON users(email_verified);

# V3__backfill_email_verification.sql
UPDATE users SET email_verified = true WHERE id > 0;
```

## Rollback Procedures

### Kubernetes Rollback
```bash
# View rollout history
kubectl rollout history deployment/myapp

# Rollback to previous version
kubectl rollout undo deployment/myapp

# Rollback to specific revision
kubectl rollout undo deployment/myapp --to-revision=3

# Check rollout status
kubectl rollout status deployment/myapp
```

### Automated Rollback
```yaml
- name: Deploy
  run: kubectl apply -f k8s/

- name: Wait for rollout
  run: kubectl rollout status deployment/myapp --timeout=5m

- name: Health check
  id: health
  run: |
    for i in {1..30}; do
      if curl -f https://example.com/health; then
        echo "Health check passed"
        exit 0
      fi
      sleep 10
    done
    exit 1

- name: Check error rate
  id: errors
  run: |
    # Query Prometheus for error rate
    ERROR_RATE=$(curl -s 'http://prometheus:9090/api/v1/query?query=rate(http_errors[5m])' | jq '.data.result[0].value[1]')
    if (( $(echo "$ERROR_RATE > 0.05" | bc -l) )); then
      echo "Error rate too high: $ERROR_RATE"
      exit 1
    fi

- name: Rollback on failure
  if: failure()
  run: |
    echo "Deployment failed, rolling back"
    kubectl rollout undo deployment/myapp
    kubectl rollout status deployment/myapp
```

## Resource Management

### Resource Requests and Limits
```yaml
resources:
  requests:
    cpu: 250m      # Guaranteed CPU
    memory: 256Mi  # Guaranteed memory
  limits:
    cpu: 500m      # Maximum CPU
    memory: 512Mi  # Maximum memory (pod killed if exceeded)
```

**Best Practices:**
- Always set requests (for scheduling)
- Set limits to prevent resource exhaustion
- Requests = typical usage, Limits = peak usage
- Monitor actual usage and adjust
- Use Vertical Pod Autoscaler for recommendations

### Horizontal Pod Autoscaling
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: myapp
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: myapp
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
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300  # Wait 5min before scale down
      policies:
      - type: Percent
        value: 50
        periodSeconds: 60  # Max 50% reduction per minute
```

## Checklist

When designing deployments:
- [ ] Is the deployment strategy appropriate for the risk level?
- [ ] Are readiness probes configured correctly?
- [ ] Are liveness probes simple and not checking dependencies?
- [ ] Is graceful shutdown implemented with SIGTERM handling?
- [ ] Are resource requests and limits defined?
- [ ] Is autoscaling configured if needed?
- [ ] Are database migrations backward compatible?
- [ ] Is rollback procedure documented and tested?
- [ ] Are health check endpoints monitoring critical dependencies?
- [ ] Is monitoring configured for deployment metrics?
- [ ] Is connection draining implemented?
- [ ] Are deployment timeouts set appropriately?

Use this guidance to ensure deployments are zero-downtime, reliable, and easily recoverable.
