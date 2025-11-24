# Backend Plugin

Comprehensive toolkit for backend development covering REST, GraphQL, gRPC, WebSocket, and message broker integrations.

## Features

### Agents

- **api-designer**: Expert in designing REST, GraphQL, and gRPC APIs with best practices for versioning, documentation, authentication, and performance
- **message-broker-expert**: Expert in designing event-driven architectures with NATS, RabbitMQ, Kafka, and Redis pub/sub
- **realtime-communication-expert**: Expert in WebSocket, Server-Sent Events, and real-time communication patterns

### Commands

- `/design-api`: Design comprehensive REST, GraphQL, or gRPC API for a domain
- `/setup-messaging`: Design and implement message broker integration
- `/implement-realtime`: Implement WebSocket or SSE for real-time communication

### Skills

- **api-best-practices**: Auto-invoked when designing APIs to ensure REST, GraphQL, and gRPC best practices
- **message-patterns**: Auto-invoked when working with message brokers to ensure proper messaging patterns

## Usage

### Design a New API

```
/design-api

Design a REST API for user management with CRUD operations,
authentication, and profile picture upload
```

```
/design-api

Design a GraphQL API for an e-commerce catalog with products,
categories, and real-time inventory updates
```

```
/design-api

Design a gRPC API for a payment service with transaction
processing and webhook notifications
```

### Setup Message Broker

```
/setup-messaging

Implement Kafka for order events with exactly-once delivery
and stream processing for analytics
```

```
/setup-messaging

Setup RabbitMQ for background job processing with retry logic
and dead letter queue
```

```
/setup-messaging

Implement NATS JetStream for microservices communication with
request/reply pattern
```

### Implement Real-time Features

```
/implement-realtime

Build a real-time chat system with private messages, group channels,
and user presence
```

```
/implement-realtime

Create WebSocket connection for live dashboard with real-time metrics
and 1000+ concurrent users
```

```
/implement-realtime

Setup real-time push notifications with multiple channels and
delivery tracking
```

### Use Agents Directly

Invoke specialized agents for focused work:

- "Use api-designer to design REST endpoints for order management"
- "Use message-broker-expert to design Kafka topic structure for events"
- "Use realtime-communication-expert to implement WebSocket chat protocol"

## Technologies Covered

### API Protocols
- **REST**: Resource-oriented HTTP APIs with OpenAPI/Swagger
- **GraphQL**: Schema-based APIs with queries, mutations, subscriptions
- **gRPC**: Protocol Buffers with streaming support

### Message Brokers
- **NATS**: Lightweight pub/sub with JetStream persistence
- **RabbitMQ**: AMQP broker with complex routing and exchanges
- **Kafka**: Distributed event streaming with high throughput
- **Redis**: In-memory pub/sub and streams

### Real-time Communication
- **WebSocket**: Full-duplex bidirectional communication
- **Server-Sent Events**: Unidirectional server-to-client streaming
- **Socket.IO**: Enhanced WebSocket with rooms and namespaces

## Patterns & Best Practices

### API Design
- Resource-oriented REST with proper HTTP methods
- GraphQL schema-first design with DataLoader
- gRPC streaming patterns for efficient data transfer
- API versioning and deprecation strategies
- Authentication (JWT, OAuth2) and authorization (RBAC)
- Rate limiting and throttling
- Comprehensive error handling
- OpenAPI/GraphQL schema documentation

### Message Broker Patterns
- Publish/Subscribe for event broadcasting
- Point-to-Point queues for task distribution
- Request/Reply for synchronous-style communication
- Saga pattern for distributed transactions
- Outbox pattern for atomic messaging
- Inbox pattern for idempotent processing
- Dead letter queues for error handling
- Event versioning and schema evolution

### Real-time Patterns
- Connection lifecycle management
- Authentication and authorization
- Heartbeat and reconnection logic
- Message routing and broadcasting
- Room/channel-based messaging
- Scaling with sticky sessions and message brokers
- Rate limiting per connection

## Example Workflows

### Building an E-commerce Backend

1. **Design REST API** for product catalog
   ```
   /design-api
   Design REST API for products with search, filtering, and pagination
   ```

2. **Setup Message Broker** for order events
   ```
   /setup-messaging
   Setup Kafka for order events with order-placed, order-shipped topics
   ```

3. **Add Real-time Updates** for inventory
   ```
   /implement-realtime
   Add WebSocket for real-time inventory updates to connected clients
   ```

### Building a Chat Application

1. **Design GraphQL API** for chat history
   ```
   /design-api
   Design GraphQL API for chat messages, channels, and user profiles
   ```

2. **Implement WebSocket** for real-time messaging
   ```
   /implement-realtime
   Implement WebSocket chat with private and group channels
   ```

3. **Setup Message Broker** for notifications
   ```
   /setup-messaging
   Setup Redis pub/sub for cross-instance message broadcasting
   ```

### Building Microservices Communication

1. **Design gRPC APIs** for service contracts
   ```
   /design-api
   Design gRPC APIs for user service, order service, and payment service
   ```

2. **Setup Event Bus** with NATS
   ```
   /setup-messaging
   Setup NATS for inter-service events with guaranteed delivery
   ```

## Integration with Other Plugins

- **architecture-plugin**: Design microservices architecture first, then use backend-plugin for API and messaging implementation
- **database-plugin**: Design database schema, then create APIs to access the data
- **infra-plugin**: Deploy message brokers and API gateways to Kubernetes

## Best Practices

- Start with API contract design before implementation
- Choose the right tool for the job (REST vs GraphQL vs gRPC)
- Select message broker based on requirements (throughput, ordering, persistence)
- Implement comprehensive error handling and retries
- Design for idempotency in message consumers
- Use authentication and authorization for all endpoints
- Document APIs thoroughly with OpenAPI/GraphQL schema
- Monitor API performance and message broker metrics
- Implement rate limiting and circuit breakers
- Version APIs and events for backward compatibility

## Advanced Topics

### API Gateway Patterns
- Backend for Frontend (BFF)
- API composition and aggregation
- Request/response transformation
- Authentication and rate limiting

### Saga Orchestration
- Orchestration-based sagas with central coordinator
- Choreography-based sagas with event reactions
- Compensation logic for failures

### Event Sourcing
- Event store design
- Event replay and projections
- CQRS with separate read/write models

### Real-time Scaling
- Horizontal scaling with sticky sessions
- Cross-instance communication with Redis/NATS
- Connection distribution and load balancing
- Graceful shutdown and deployment strategies

Start building robust, scalable backend systems with comprehensive API and messaging support!
