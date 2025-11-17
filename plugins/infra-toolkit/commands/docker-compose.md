---
description: Generate docker-compose.yml for local development
allowed-tools: Write, Read, Edit
---

# Generate Docker Compose Configuration

## Parse Arguments
```bash
SERVICES="${ARGUMENTS[0]}"  # Comma-separated list of services
```

## Validate Input
Parse comma-separated services:
- redis: Redis cache
- postgres: PostgreSQL database
- mysql: MySQL database
- mongodb: MongoDB database
- rabbitmq: RabbitMQ message broker
- kafka: Apache Kafka
- elasticsearch: Elasticsearch
- nginx: Nginx reverse proxy
- app: Application service (from current directory)

## Invoke Docker Expert
Invoke the `docker-expert` agent to generate docker-compose.yml with:
- Requested services: $SERVICES
- Proper networking setup
- Volume configurations
- Environment variables
- Health checks
- Restart policies

## Service Configurations
The agent will configure each service with:
1. Appropriate image versions
2. Port mappings
3. Volume mounts for persistence
4. Environment variables
5. Health checks
6. Resource limits
7. Network settings
8. Dependencies

## Output
Generate docker-compose.yml with:
- Service definitions
- Network configuration
- Volume declarations
- Environment file template
- Override file for production

Provide:
- Usage instructions
- Service URLs
- Default credentials
- Data persistence information
- Troubleshooting guide

## Example Usage
```
/docker-compose redis,postgres,rabbitmq
/docker-compose nginx,app,mongodb
/docker-compose elasticsearch,kafka
/docker-compose mysql,redis
```