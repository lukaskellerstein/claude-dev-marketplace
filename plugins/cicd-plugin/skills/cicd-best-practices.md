---
name: cicd-best-practices
description: Auto-invoked when working with CI/CD pipelines, GitHub Actions, or deployment configurations to ensure best practices
allowed-tools: Read, Grep, Glob
---

# CI/CD Best Practices

This skill provides guidance on CI/CD best practices across GitHub Actions, deployment automation, and release management.

## When Active

This skill activates when you:
- Create or modify GitHub Actions workflows
- Design CI/CD pipelines
- Configure deployment automation
- Set up testing in CI
- Work with release processes
- Configure build optimization

## GitHub Actions Best Practices

### Workflow Organization
```yaml
# Use clear, descriptive workflow names
name: CI

# Specific triggers, not catch-all
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

# Explicit permissions (least privilege)
permissions:
  contents: read
  pull-requests: write
```

### Job Structure
```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    timeout-minutes: 15  # Always set timeouts

    steps:
      # Pin action versions with SHA for security
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Or specific depth if needed

      # Clear step names
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'  # Enable caching

      # Install dependencies
      - name: Install dependencies
        run: npm ci  # Use 'ci' not 'install' in CI

      # Run tests with coverage
      - name: Run tests
        run: npm test -- --coverage

      # Upload artifacts for later use
      - name: Upload coverage
        uses: actions/upload-artifact@v4
        if: always()  # Upload even if tests fail
        with:
          name: coverage-report
          path: coverage/
```

### Caching Strategies
```yaml
# NPM/Node.js
- uses: actions/setup-node@v4
  with:
    cache: 'npm'

# Python/pip
- uses: actions/setup-python@v5
  with:
    cache: 'pip'

# Custom cache
- uses: actions/cache@v4
  with:
    path: |
      ~/.cache
      node_modules
    key: ${{ runner.os }}-deps-${{ hashFiles('**/package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-deps-
```

### Matrix Builds
```yaml
strategy:
  matrix:
    os: [ubuntu-latest, macos-latest, windows-latest]
    node-version: [18, 20, 22]
  fail-fast: false  # Don't cancel other jobs on first failure

runs-on: ${{ matrix.os }}

steps:
  - uses: actions/setup-node@v4
    with:
      node-version: ${{ matrix.node-version }}
```

### Conditional Execution
```yaml
# Only deploy on main branch
- name: Deploy to production
  if: github.ref == 'refs/heads/main' && github.event_name == 'push'
  run: npm run deploy

# Skip on specific commit messages
- name: Run expensive tests
  if: "!contains(github.event.head_commit.message, '[skip-tests]')"
  run: npm run test:e2e

# Run on specific file changes
- name: Build documentation
  if: contains(github.event.head_commit.modified, 'docs/')
  run: npm run docs:build
```

### Secrets Management
```yaml
# Use GitHub Secrets, never hardcode
- name: Deploy
  env:
    API_KEY: ${{ secrets.API_KEY }}
    DATABASE_URL: ${{ secrets.DATABASE_URL }}
  run: npm run deploy

# Use OIDC instead of long-lived credentials
- name: Configure AWS credentials
  uses: aws-actions/configure-aws-credentials@v4
  with:
    role-to-assume: arn:aws:iam::123456789012:role/GitHubActions
    aws-region: us-east-1
```

### Parallel Jobs with Dependencies
```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - run: npm run build
      - uses: actions/upload-artifact@v4
        with:
          name: dist
          path: dist/

  test:
    runs-on: ubuntu-latest
    steps:
      - run: npm test

  deploy:
    needs: [build, test]  # Wait for both
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/download-artifact@v4
        with:
          name: dist
      - run: npm run deploy
```

## Pipeline Best Practices

### Stages
Organize pipelines into clear stages:
1. **Validate**: Lint, format check
2. **Build**: Compile, package
3. **Test**: Unit, integration, E2E
4. **Security**: Scan dependencies, containers
5. **Deploy**: Deploy to environments
6. **Verify**: Smoke tests, health checks

### Fast Feedback
- Run fast tests first (unit tests)
- Fail fast on critical issues
- Parallel execution where possible
- Cache dependencies aggressively
- Incremental builds when possible

### Testing Strategy
```yaml
test:
  name: Test Suite
  runs-on: ubuntu-latest
  steps:
    # Unit tests (fast)
    - name: Unit tests
      run: npm run test:unit

    # Integration tests
    - name: Integration tests
      run: npm run test:integration

    # E2E tests (slower, run after others pass)
    - name: E2E tests
      if: success()
      run: npm run test:e2e

    # Upload test results
    - name: Upload test results
      if: always()
      uses: actions/upload-artifact@v4
      with:
        name: test-results
        path: test-results/
```

## Deployment Best Practices

### Environment Strategy
```yaml
deploy-staging:
  name: Deploy to Staging
  environment:
    name: staging
    url: https://staging.example.com
  runs-on: ubuntu-latest
  steps:
    - name: Deploy
      run: ./deploy.sh staging

deploy-production:
  name: Deploy to Production
  needs: [deploy-staging]
  environment:
    name: production
    url: https://example.com
  runs-on: ubuntu-latest
  steps:
    - name: Deploy
      run: ./deploy.sh production
```

### Health Checks
```yaml
- name: Deploy application
  run: kubectl apply -f k8s/

- name: Wait for rollout
  run: kubectl rollout status deployment/myapp

- name: Health check
  run: |
    for i in {1..30}; do
      if curl -f https://example.com/health; then
        echo "Health check passed"
        exit 0
      fi
      sleep 10
    done
    echo "Health check failed"
    exit 1

- name: Rollback on failure
  if: failure()
  run: kubectl rollout undo deployment/myapp
```

### Zero-Downtime Deployment
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
      maxSurge: 1        # Add 1 extra pod during rollout
      maxUnavailable: 0  # Never have pods unavailable
  template:
    spec:
      containers:
      - name: app
        image: myapp:v1.2.3
        # Readiness probe prevents traffic to non-ready pods
        readinessProbe:
          httpGet:
            path: /health/ready
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 5
        # Liveness probe restarts unhealthy pods
        livenessProbe:
          httpGet:
            path: /health/live
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        # Graceful shutdown
        lifecycle:
          preStop:
            exec:
              command: ["/bin/sh", "-c", "sleep 15"]
```

## Build Optimization

### Docker Optimization
```dockerfile
# Multi-stage build
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

# Small production image
FROM node:20-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
USER node
EXPOSE 3000
CMD ["node", "dist/index.js"]
```

### Build Caching
```yaml
- name: Set up Docker Buildx
  uses: docker/setup-buildx-action@v3

- name: Build and push
  uses: docker/build-push-action@v5
  with:
    context: .
    push: true
    tags: myapp:latest
    cache-from: type=gha  # GitHub Actions cache
    cache-to: type=gha,mode=max
```

## Security Best Practices

### Scan Dependencies
```yaml
- name: Run security audit
  run: npm audit --audit-level=moderate

- name: Scan with Snyk
  uses: snyk/actions/node@master
  env:
    SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
```

### Scan Container Images
```yaml
- name: Scan Docker image
  uses: aquasecurity/trivy-action@master
  with:
    image-ref: myapp:latest
    severity: 'CRITICAL,HIGH'
    exit-code: 1  # Fail on vulnerabilities
```

### Least Privilege
```yaml
# Minimal permissions
permissions:
  contents: read

# Request additional permissions only when needed
deploy:
  permissions:
    contents: read
    id-token: write  # For OIDC
```

## Monitoring & Observability

### Workflow Notifications
```yaml
- name: Notify on failure
  if: failure()
  uses: slackapi/slack-github-action@v1
  with:
    webhook: ${{ secrets.SLACK_WEBHOOK }}
    payload: |
      {
        "text": "Deployment failed: ${{ github.workflow }}"
      }
```

### Deployment Tracking
```yaml
- name: Record deployment
  run: |
    curl -X POST https://api.example.com/deployments \
      -H "Content-Type: application/json" \
      -d '{
        "version": "${{ github.sha }}",
        "environment": "production",
        "status": "success"
      }'
```

## Checklist

When creating/modifying CI/CD pipelines:
- [ ] Are workflow names clear and descriptive?
- [ ] Are action versions pinned for security?
- [ ] Are timeouts set for all jobs?
- [ ] Is caching configured for dependencies?
- [ ] Are secrets managed securely (not hardcoded)?
- [ ] Are permissions set to least privilege?
- [ ] Are tests run in appropriate order (fast first)?
- [ ] Are test results uploaded for analysis?
- [ ] Are deployments validated with health checks?
- [ ] Is rollback automated on failures?
- [ ] Are notifications configured for failures?
- [ ] Is the pipeline optimized for speed?
- [ ] Are security scans included?
- [ ] Is the pipeline well-documented?

## Common Anti-Patterns to Avoid

### Don't
```yaml
# ❌ Hardcoded secrets
env:
  API_KEY: "sk_live_123abc"

# ❌ No timeout (can run forever)
jobs:
  build:
    runs-on: ubuntu-latest

# ❌ Using 'latest' tag (not reproducible)
- uses: actions/checkout@latest

# ❌ No caching (slow builds)
- run: npm install

# ❌ Ignoring test failures
- run: npm test || true
```

### Do
```yaml
# ✅ Use secrets
env:
  API_KEY: ${{ secrets.API_KEY }}

# ✅ Set timeouts
jobs:
  build:
    runs-on: ubuntu-latest
    timeout-minutes: 15

# ✅ Pin versions
- uses: actions/checkout@v4

# ✅ Enable caching
- uses: actions/setup-node@v4
  with:
    cache: 'npm'

# ✅ Fail on test errors
- run: npm test
```

Use this guidance to ensure CI/CD pipelines are fast, secure, reliable, and maintainable.
