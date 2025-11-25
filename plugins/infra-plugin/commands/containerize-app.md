---
description: Containerize application with optimized Docker configuration, multi-stage builds, and Docker Compose for local development
---

Create production-ready Docker containers with optimized Dockerfiles, security best practices, and Docker Compose for multi-service orchestration.

## Process

Follow these steps:

1. **Analyze Application**: Understand the application stack and requirements
   - Identify programming language and runtime (Node.js, Python, Go, Java, etc.)
   - Review application dependencies and build process
   - Determine runtime requirements and environment variables
   - Check for multi-service architecture (web, API, workers, databases)
   - Identify data persistence needs
   - Review existing Docker configuration if any

2. **Launch Docker Expert**: Use the `infra-plugin:docker-expert` agent to:
   - Design optimized multi-stage Dockerfiles
   - Select appropriate base images (Alpine, Distroless)
   - Implement security best practices
   - Configure build caching strategies
   - Create .dockerignore files
   - Set up health checks
   - Configure resource limits
   - Implement non-root user execution

3. **Create Docker Compose** (if multi-service): Design orchestration
   - Define all services and their relationships
   - Configure networking between services
   - Set up volumes for data persistence
   - Define environment variables and secrets
   - Configure health checks and dependencies
   - Set up profiles for different environments
   - Create override files for development vs production

4. **Security Hardening**: Implement security measures
   - Scan images for vulnerabilities (Trivy, Snyk)
   - Use minimal base images
   - Run as non-root user
   - Implement read-only root filesystem where possible
   - Drop unnecessary capabilities
   - Use secret management (Docker secrets, env files)
   - Keep base images updated

5. **Optimization**: Optimize for size and performance
   - Minimize image layers
   - Use multi-stage builds
   - Optimize layer caching
   - Remove unnecessary files
   - Use build cache mounts
   - Implement parallel builds where possible

6. **CI/CD Integration**: Set up automated builds
   - Configure automated image builds
   - Implement image tagging strategy
   - Set up vulnerability scanning
   - Configure registry pushing (GCR, Docker Hub)
   - Create build scripts and Makefiles

## Output

Present a comprehensive containerization solution including:

### Dockerfiles
- **Production Dockerfile**: Optimized multi-stage build
- **Development Dockerfile** (optional): With dev dependencies and hot reload
- Base image selection and justification
- Build arguments for flexibility
- Security hardening steps
- Health check configuration
- Proper labeling (version, commit, build date)

### Docker Compose Configuration
```yaml
version: '3.9'

services:
  web:
    build: .
    ports: ["3000:3000"]
    environment: []
    depends_on: []
    healthcheck: {}

  database:
    image: postgres:16-alpine
    volumes: []
    environment: []
    healthcheck: {}
```

Complete service definitions with:
- Service dependencies
- Network configuration
- Volume mounts
- Environment variables
- Resource limits
- Health checks
- Restart policies

### .dockerignore
- Files and directories to exclude from build context
- Development files
- Documentation
- Tests
- CI/CD files

### Build Scripts
```bash
#!/bin/bash
# Build script with proper tagging
docker build -t myapp:latest \
  --build-arg VERSION=1.0.0 \
  --build-arg BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ') \
  .
```

### Documentation
- **README.md**: Build and run instructions
- Environment variable documentation
- Volume mount explanations
- Port mappings
- Development setup guide
- Production deployment guide
- Troubleshooting common issues

### Security Configuration
- Vulnerability scan results
- Security best practices checklist
- User configuration (non-root)
- Capability restrictions
- Secret management strategy
- Image signing (optional)

### CI/CD Pipeline Configuration
- Automated build configuration (Cloud Build, GitHub Actions)
- Image tagging strategy (semantic versioning, git commit)
- Registry authentication
- Vulnerability scanning in pipeline
- Multi-architecture builds (if needed)

## Examples

### Containerize Node.js Application
```
/containerize-app

Containerize our Express.js API with:
- Multi-stage build to minimize image size
- Node 20 Alpine base image
- Development and production configurations
- Docker Compose with PostgreSQL and Redis
- Health checks and graceful shutdown
```

### Containerize Python Application
```
/containerize-app

Create Docker container for FastAPI application with:
- Multi-stage build with virtual environment
- Python 3.11 slim base image
- Gunicorn for production serving
- Docker Compose with PostgreSQL, Redis, and Celery worker
- Proper logging configuration
```

### Containerize Go Application
```
/containerize-app

Containerize Go microservice with:
- Multi-stage build with scratch final image
- Statically compiled binary
- Minimal attack surface with distroless base
- Docker Compose for local development with dependencies
```

### Containerize Monorepo Application
```
/containerize-app

Create containers for monorepo with:
- Multiple services (frontend, backend, workers)
- Shared base image for consistency
- Docker Compose for complete local environment
- Build optimization with BuildKit cache mounts
```

## Docker Commands Reference

```bash
# Build image
docker build -t myapp:v1.0.0 .

# Build with BuildKit (faster)
DOCKER_BUILDKIT=1 docker build -t myapp:v1.0.0 .

# Build multi-architecture
docker buildx build --platform linux/amd64,linux/arm64 -t myapp:v1.0.0 .

# Run container
docker run -d -p 8080:8080 --name myapp myapp:v1.0.0

# Run with environment variables
docker run -d -p 8080:8080 -e NODE_ENV=production myapp:v1.0.0

# Docker Compose
docker compose up -d
docker compose down
docker compose logs -f
docker compose ps

# Scan for vulnerabilities
docker scan myapp:v1.0.0
trivy image myapp:v1.0.0

# Inspect image
docker inspect myapp:v1.0.0
docker history myapp:v1.0.0
```

## Best Practices Applied

- **Multi-stage Builds**: Separate build and runtime stages
- **Minimal Base Images**: Alpine, Distroless, or scratch for security
- **Layer Optimization**: Minimize layers and maximize cache reuse
- **Security**: Non-root user, vulnerability scanning, minimal attack surface
- **Health Checks**: Proper liveness and readiness checks
- **Resource Limits**: CPU and memory constraints
- **Logging**: Proper log configuration for container environments
- **Documentation**: Clear build and run instructions
- **CI/CD Ready**: Automated builds and testing
- **Version Control**: Semantic versioning and proper tagging

Provide production-ready Docker containers that follow best practices and can be deployed immediately to any container platform (GKE, Cloud Run, Docker Swarm, etc.).
