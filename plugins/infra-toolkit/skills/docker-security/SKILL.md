---
name: docker-security
description: Automatically scan Dockerfiles for security issues
allowed-tools: Read, Grep
---

# Docker Security Skill

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

This skill ensures that every Docker configuration follows security best practices, reducing vulnerabilities and improving the overall security posture of containerized applications.