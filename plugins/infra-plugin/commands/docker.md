---
description: Generate optimized Dockerfile for specific app type
---

# Generate Dockerfile

## Parse Arguments
```bash
APP_TYPE="${ARGUMENTS[0]}"  # node|python|go|java|dotnet|ruby
OPTIONS="${ARGUMENTS[@]:1}" # --multi-stage, --slim, --alpine, --security-hardened
```

## Validate Input
If APP_TYPE is not provided, ask the user to specify the application type:
- node: Node.js applications
- python: Python applications
- go: Go applications
- java: Java/Spring applications
- dotnet: .NET Core applications
- ruby: Ruby/Rails applications

## Process Options
Parse options for additional configurations:
- `--multi-stage`: Use multi-stage build for smaller images
- `--slim`: Use slim base images
- `--alpine`: Use Alpine Linux base
- `--security-hardened`: Apply maximum security practices

## Invoke Docker Expert
Invoke the `docker-expert` agent with:
- Application type: $APP_TYPE
- Build options: $OPTIONS
- Current directory context

The agent will:
1. Analyze the application structure
2. Identify dependencies and requirements
3. Generate optimized Dockerfile
4. Create .dockerignore file
5. Apply security best practices
6. Optimize for layer caching
7. Minimize final image size

## Output
Display the generated files and provide:
- Build instructions
- Image size estimates
- Security scan results
- Optimization recommendations

## Example Usage
```
/dockerfile node --multi-stage --alpine
/dockerfile python --slim --security-hardened
/dockerfile go --multi-stage
/dockerfile java --slim
```