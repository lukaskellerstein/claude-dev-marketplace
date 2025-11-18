---
name: docker-security
description: Master Docker security (CIS Docker Benchmark). Use when creating/editing Dockerfiles, modifying docker-compose.yml, working with container configs, building images, or ensuring container security.
allowed-tools: Read, Grep
---

# Docker Security Skill

Master Docker security best practices and CIS Docker Benchmark standards to automatically scan, validate, and fix security vulnerabilities in container configurations.

## When to Use This Skill

Use this skill when:

1. Creating or editing Dockerfiles
2. Modifying docker-compose.yml files
3. Working with container configurations
4. Building container images
5. Deploying containerized applications
6. Reviewing container security posture
7. Implementing multi-stage builds
8. Configuring container runtimes
9. Setting up container registries
10. Implementing image scanning in CI/CD
11. Hardening production containers
12. Migrating to containerized workloads
13. Auditing existing container images
14. Implementing least privilege containers
15. Troubleshooting security violations

## Quick Start

This skill automatically scans and fixes Dockerfiles as you write them:

```dockerfile
# You write:
FROM node:latest
COPY . /app
RUN npm install
CMD ["node", "app.js"]

# Skill alerts:
❌ CIS 4.1: Using 'latest' tag (not reproducible)
❌ CIS 4.2: Running as root user
❌ Security: No vulnerability scanning
⚠️  Missing: Health check instruction

# Auto-suggested secure version:
FROM node:18.19.0-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

FROM node:18.19.0-alpine
RUN addgroup -g 1001 -S nodejs && adduser -S nodejs -u 1001
WORKDIR /app
COPY --from=builder --chown=nodejs:nodejs /app/node_modules ./node_modules
COPY --chown=nodejs:nodejs . .
USER nodejs
HEALTHCHECK --interval=30s CMD node healthcheck.js
CMD ["node", "app.js"]

✅ Security improvements applied
```

## Purpose
This skill automatically activates when working with Docker configurations to ensure security best practices are followed and vulnerabilities are avoided.

## Auto-Invocation Context

This skill triggers when:
- Creating or editing Dockerfiles
- Modifying docker-compose.yml files
- Working with container configurations
- Building container images

## Security Checks Performed

### 1. Base Image Security
- **Check for vulnerable base images**: Warn about known CVEs
- **Avoid using `latest` tag**: Pin specific versions for reproducibility
- **Prefer minimal base images**: Alpine, distroless, or scratch
- **Check for deprecated images**: Warn about EOL base images

### 2. User Security
```dockerfile
# BAD - Running as root
FROM node:18

# GOOD - Running as non-root user
FROM node:18
USER node

# BETTER - Creating custom user
FROM node:18-alpine
RUN addgroup -g 1001 -S nodejs && adduser -S nodejs -u 1001
USER nodejs
```

### 3. Secret Management
Detect and prevent:
- Hardcoded passwords
- API keys in environment variables
- Private keys in images
- AWS credentials
- Database connection strings

### 4. Build Security
```dockerfile
# BAD - Using ADD for remote content (can extract archives)
ADD https://example.com/big.tar.gz /app/

# GOOD - Using COPY for local files
COPY ./app /app/

# BAD - Running everything in one layer with sudo
RUN apt-get update && apt-get install -y sudo curl wget

# GOOD - Removing package manager cache
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*
```

### 5. Runtime Security
```dockerfile
# Security contexts
SECURITY_OPTIONS:
  - no-new-privileges:true
  - seccomp:unconfined

# Read-only root filesystem
READ_ONLY: true

# Drop capabilities
CAP_DROP:
  - ALL
CAP_ADD:
  - NET_BIND_SERVICE
```

### 6. Network Exposure
```dockerfile
# BAD - Exposing unnecessary ports
EXPOSE 22 3306 5432 6379 8080 9090

# GOOD - Only expose required application port
EXPOSE 8080

# BETTER - Document port purpose
EXPOSE 8080/tcp # HTTP API endpoint
```

## Automatic Fixes Applied

### Fix 1: Add Non-Root User
When detecting root user:
```dockerfile
# Automatically add before CMD/ENTRYPOINT
USER 1000:1000
```

### Fix 2: Pin Base Image Versions
```dockerfile
# Change from:
FROM node:latest

# To:
FROM node:18.19.0-alpine
```

### Fix 3: Add Security Labels
```dockerfile
# Add security metadata
LABEL security.scan-date="2024-01-15" \
      security.scan-tool="docker-security" \
      security.compliance="CIS-Docker-1.2"
```

### Fix 4: Optimize Package Installation
```dockerfile
# For Alpine
RUN apk add --no-cache package-name

# For Debian/Ubuntu
RUN apt-get update \
    && apt-get install -y --no-install-recommends package-name \
    && rm -rf /var/lib/apt/lists/*

# For CentOS/RHEL
RUN yum install -y package-name \
    && yum clean all
```

### Fix 5: Set Proper File Permissions
```dockerfile
# Ensure proper ownership
COPY --chown=1000:1000 . /app

# Set executable permissions appropriately
RUN chmod +x /app/entrypoint.sh
```

## Docker Compose Security

### Service Configuration
```yaml
services:
  app:
    image: myapp:1.0.0
    # Security additions
    security_opt:
      - no-new-privileges:true
    read_only: true
    user: "1000:1000"
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE
```

### Network Isolation
```yaml
networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true  # No external access
```

### Volume Security
```yaml
volumes:
  data:
    driver: local
    driver_opts:
      o: "uid=1000,gid=1000"
```

## Security Scanning Commands

Suggest running:
```bash
# Scan with Trivy
trivy image myapp:latest

# Scan with Snyk
snyk container test myapp:latest

# Scan with Docker Scout
docker scout cves myapp:latest

# Check for secrets
docker run --rm -v "$PWD:/path" trufflesecurity/trufflehog:latest filesystem /path
```

## Compliance Checks

### CIS Docker Benchmark
- 4.1 - Create a user for the container
- 4.2 - Use trusted base images
- 4.5 - Enable Content trust for Docker
- 4.6 - Add HEALTHCHECK instruction
- 4.7 - Do not use update instructions alone

### Security Best Practices Applied
1. **Least Privilege**: Minimal permissions
2. **Defense in Depth**: Multiple security layers
3. **Immutability**: Read-only filesystems
4. **Minimal Attack Surface**: Small base images
5. **Supply Chain Security**: Verified base images

## Real-World Applications

### Production-Ready Python Application

**Scenario:** Secure Python web application for production

```dockerfile
# Multi-stage build for security and size
FROM python:3.11-slim AS builder

WORKDIR /app

# Install dependencies in separate layer
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Final production image
FROM python:3.11-slim

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

# Copy only necessary files
COPY --from=builder --chown=appuser:appuser /root/.local /home/appuser/.local
COPY --chown=appuser:appuser . .

# Set PATH for user-installed packages
ENV PATH=/home/appuser/.local/bin:$PATH

# Security: Run as non-root
USER appuser

# Security: Read-only root filesystem (requires tmp volume)
VOLUME /tmp

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Expose only required port
EXPOSE 8000

# Use exec form for proper signal handling
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
```

### Node.js Microservice with Security Hardening

**Scenario:** Secure Node.js microservice following CIS benchmarks

```dockerfile
# Use specific version (CIS 4.1)
FROM node:18.19.0-alpine AS builder

# Add security labels
LABEL security.scan-date="2024-01-15" \
      security.scan-tool="trivy" \
      maintainer="security@company.com"

WORKDIR /app

# Copy package files first (better caching)
COPY package*.json ./

# Install production dependencies only
RUN npm ci --only=production && \
    npm cache clean --force

# Production image
FROM node:18.19.0-alpine

# Install dumb-init for proper signal handling
RUN apk add --no-cache dumb-init

# Create non-root user (CIS 4.2)
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001

WORKDIR /app

# Copy with correct ownership
COPY --from=builder --chown=nodejs:nodejs /app/node_modules ./node_modules
COPY --chown=nodejs:nodejs . .

# Switch to non-root user
USER nodejs

# Health check (CIS 4.6)
HEALTHCHECK --interval=30s --timeout=3s \
  CMD node healthcheck.js || exit 1

# Expose only required port
EXPOSE 3000

# Use dumb-init for proper signal handling
ENTRYPOINT ["dumb-init", "--"]
CMD ["node", "server.js"]
```

### Secure Go Application with Distroless

**Scenario:** Minimal attack surface Go application

```dockerfile
# Build stage
FROM golang:1.21-alpine AS builder

WORKDIR /app

# Copy dependency files
COPY go.mod go.sum ./
RUN go mod download

# Copy source code
COPY . .

# Build statically linked binary
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o main .

# Production stage using distroless
FROM gcr.io/distroless/static-debian11

# Copy binary from builder
COPY --from=builder /app/main /

# Distroless images run as non-root by default
# No shell, no package manager = minimal attack surface

EXPOSE 8080

# Health check (requires external monitoring since no shell)
# Use Kubernetes liveness probe instead

USER nonroot:nonroot

ENTRYPOINT ["/main"]
```

### Database Container with Security

**Scenario:** PostgreSQL with security hardening

```dockerfile
FROM postgres:15-alpine

# Security: Run as postgres user (already default)
# Security: Use secrets for passwords (via environment or files)

# Add custom healthcheck
HEALTHCHECK --interval=10s --timeout=5s --retries=5 \
  CMD pg_isready -U postgres || exit 1

# Security: Limit capabilities
# Set via docker-compose or Kubernetes securityContext:
# cap_drop:
#   - ALL
# cap_add:
#   - CHOWN
#   - DAC_OVERRIDE
#   - SETGID
#   - SETUID

# Use initialization scripts for schema
COPY --chown=postgres:postgres ./init-scripts/ /docker-entrypoint-initdb.d/

# Expose only PostgreSQL port
EXPOSE 5432

# Default CMD from base image is secure
```

### Docker Compose with Security

**Scenario:** Multi-container application with security

```yaml
version: '3.8'

services:
  web:
    image: myapp:1.0.0
    # Security: Run as non-root
    user: "1000:1000"
    # Security: Read-only root filesystem
    read_only: true
    # Security: Drop all capabilities
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE
    # Security: No new privileges
    security_opt:
      - no-new-privileges:true
    # Temporary filesystem for writes
    tmpfs:
      - /tmp
    # Resource limits
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M
    # Health check
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    # Network isolation
    networks:
      - frontend

  db:
    image: postgres:15-alpine
    user: postgres
    read_only: true
    security_opt:
      - no-new-privileges:true
    # Persistent volume
    volumes:
      - db-data:/var/lib/postgresql/data
      - /tmp
    environment:
      # Use secrets instead of environment variables
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
    secrets:
      - db_password
    networks:
      - backend

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true  # No external access

volumes:
  db-data:
    driver: local

secrets:
  db_password:
    external: true
```

## Best Practices

### Image Security
- Use official base images from trusted registries
- Pin specific image versions (avoid :latest)
- Scan images for vulnerabilities before deployment
- Minimize image layers and size
- Remove build tools and unnecessary packages

### Runtime Security
- Run containers as non-root user
- Use read-only root filesystems
- Drop all capabilities, add only required ones
- Apply seccomp and AppArmor profiles
- Limit resource usage (CPU, memory, PIDs)

### Secrets Management
- Never hardcode secrets in images or env vars
- Use Docker secrets or external secret managers
- Rotate secrets regularly
- Scan for leaked credentials in images

### Network Security
- Expose only necessary ports
- Use private networks for inter-container communication
- Implement TLS for external communication
- Use network policies to restrict traffic

### Compliance and Auditing
- Sign images with Docker Content Trust
- Enable audit logging
- Regularly update base images
- Maintain image provenance

## Common Pitfalls

### ❌ Running as Root

**Problem:**
```dockerfile
FROM node:18
COPY . /app
WORKDIR /app
RUN npm install
CMD ["node", "server.js"]
# Runs as root - major security risk!
```

**Solution:** Create and use non-root user
```dockerfile
FROM node:18
RUN groupadd -r appuser && useradd -r -g appuser appuser
COPY --chown=appuser:appuser . /app
WORKDIR /app
RUN npm install
USER appuser
CMD ["node", "server.js"]
```

### ❌ Secrets in Environment Variables

**Problem:**
```yaml
# docker-compose.yml
services:
  app:
    environment:
      DATABASE_PASSWORD: "secretpassword123"  # Visible in logs!
```

**Solution:** Use Docker secrets
```yaml
services:
  app:
    secrets:
      - db_password
    environment:
      DATABASE_PASSWORD_FILE: /run/secrets/db_password

secrets:
  db_password:
    external: true
```

### ❌ Using :latest Tag

**Problem:**
```dockerfile
FROM python:latest  # Unpredictable, can break builds!
```

**Solution:** Pin specific versions
```dockerfile
FROM python:3.11.6-slim  # Reproducible builds
```

### ❌ Installing Unnecessary Packages

**Problem:**
```dockerfile
FROM ubuntu:22.04
RUN apt-get update && apt-get install -y \
    curl vim git build-essential \
    # Many unnecessary tools increasing attack surface
```

**Solution:** Use minimal base images
```dockerfile
FROM python:3.11-alpine  # Minimal base
RUN apk add --no-cache \
    ca-certificates \
    # Only essential packages
```

### ❌ Not Scanning for Vulnerabilities

**Problem:** Deploying images without security scanning

**Solution:** Scan before deployment
```bash
# Scan with Trivy
trivy image myapp:1.0.0

# Fail build if HIGH/CRITICAL vulnerabilities
trivy image --severity HIGH,CRITICAL --exit-code 1 myapp:1.0.0

# Scan with Docker Scout
docker scout cves myapp:1.0.0
```

### ❌ Exposing Unnecessary Ports

**Problem:**
```dockerfile
EXPOSE 22 3000 8080 9090  # Too many ports exposed!
```

**Solution:** Expose only required ports
```dockerfile
EXPOSE 8080  # Only the application port
```

### ❌ Building with Secrets

**Problem:**
```dockerfile
RUN git clone https://user:password@github.com/private/repo.git
# Password leaked in image layer!
```

**Solution:** Use build secrets (BuildKit)
```dockerfile
# syntax=docker/dockerfile:1.4
RUN --mount=type=secret,id=github_token \
    git clone https://$(cat /run/secrets/github_token)@github.com/private/repo.git

# Build with:
# docker build --secret id=github_token,src=token.txt .
```

### ❌ Large Image Sizes

**Problem:**
```dockerfile
FROM node:18  # 1.1GB base image
COPY . /app
RUN npm install  # Includes devDependencies
# Final image: 1.5GB
```

**Solution:** Use multi-stage builds
```dockerfile
# Build stage
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

# Runtime stage
FROM node:18-alpine  # 170MB
WORKDIR /app
COPY --from=builder /app/node_modules ./node_modules
COPY . .
# Final image: 250MB
```

### ❌ Not Using Health Checks

**Problem:**
```dockerfile
# No HEALTHCHECK - Docker doesn't know if container is healthy
```

**Solution:** Add health checks
```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8080/health || exit 1
```

## Related Skills

- **k8s-optimizer**: Ensures Kubernetes deployments use secure container configurations
- **helm-validator**: Validates Helm charts reference secure container images
- **iac-compliance**: Ensures container configurations meet compliance standards
- **gcp-cost-guard**: Optimizes container resource usage

This skill ensures that every Docker configuration follows security best practices, reducing vulnerabilities and improving the overall security posture of containerized applications.