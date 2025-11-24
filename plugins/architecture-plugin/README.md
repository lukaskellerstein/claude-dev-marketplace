# Architecture Plugin

Comprehensive toolkit for designing and reviewing software architectures, with focus on microservices, cloud patterns, and event-driven systems.

## Features

### Agents

- **microservices-architect**: Expert in designing microservices with DDD, service boundaries, and data management
- **cloud-patterns-expert**: Specializes in cloud-native patterns, scalability, and reliability for AWS/GCP/Azure
- **event-sourcing-expert**: Expert in event sourcing, CQRS, and message broker patterns

### Commands

- `/design-microservices`: Design comprehensive microservices architecture
- `/review-architecture`: Review existing architecture with improvement recommendations

### Skills

- **ddd-patterns**: Auto-invoked when working with domain models to ensure proper DDD patterns

## Usage

### Design New Microservices Architecture

```
/design-microservices

Design microservices for an e-commerce system with order management, inventory, and payments
```

### Review Existing Architecture

```
/review-architecture

Review the current architecture and identify scalability bottlenecks
```

### Use Agents Directly

Invoke specialized agents for focused architectural work:

- "Use microservices-architect to define service boundaries for user management"
- "Use cloud-patterns-expert to design multi-region deployment"
- "Use event-sourcing-expert to implement order saga pattern"

## Best Practices

- Start with domain analysis before diving into technical decisions
- Consider both functional and non-functional requirements
- Document architectural decisions with ADRs
- Use diagrams to communicate architecture
- Validate designs against scalability and reliability requirements

## Architecture Patterns Covered

- Microservices & Service Mesh
- Domain-Driven Design (DDD)
- Event Sourcing & CQRS
- Saga Pattern
- API Gateway & BFF
- Circuit Breaker & Bulkhead
- 12-Factor Apps
- Cloud-Native Patterns
- Multi-Region Deployments
