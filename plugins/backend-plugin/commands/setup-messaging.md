---
description: Design and implement message broker integration with NATS, RabbitMQ, Kafka, or Redis
---

Design and implement a complete messaging solution for event-driven architecture and asynchronous communication.

## Process

Follow these steps:

1. **Analyze Requirements**: Understand messaging needs and constraints
   - Identify communication patterns (pub/sub, queue, streaming)
   - Determine delivery guarantees needed
   - Assess throughput and latency requirements
   - Review existing infrastructure and codebase

2. **Launch Message Broker Expert**: Use the `backend-plugin:message-broker-expert` agent to:
   - Select appropriate message broker (NATS, RabbitMQ, Kafka, Redis)
   - Design topic/queue structure and naming
   - Define message schemas and events
   - Design producer and consumer configurations
   - Plan error handling and retry strategies
   - Design monitoring and observability

3. **Real-time Integration** (if applicable): If WebSocket integration needed, use the `backend-plugin:realtime-communication-expert` agent to:
   - Design WebSocket protocol for client communication
   - Integrate message broker with WebSocket gateway
   - Design message routing between broker and WebSocket

4. **Implementation Guide**: Provide:
   - Message broker deployment configuration
   - Producer implementation with error handling
   - Consumer implementation with retry logic
   - Message schema definitions
   - Monitoring and alerting setup

## Output

Present a comprehensive messaging architecture including:

### Broker Selection
- Chosen broker with detailed rationale
- Comparison with alternatives
- Trade-offs and limitations
- Infrastructure requirements

### Topic/Queue Design
- Naming conventions and structure
- Partitioning strategy (if applicable)
- Retention policies
- Replication configuration
- Access control and security

### Message Schemas
- Event definitions with versioning
- Message envelope structure
- Correlation IDs and metadata
- Schema evolution strategy
- Example messages

### Producer Design
- Producer configuration for reliability
- Retry and timeout settings
- Batching and compression
- Connection pooling
- Error handling and circuit breakers
- Code examples

### Consumer Design
- Consumer group configuration
- Processing patterns (at-least-once, exactly-once)
- Concurrent processing strategy
- Error handling and dead letter queues
- Idempotency patterns
- Backpressure handling
- Code examples

### Deployment Configuration
- Broker deployment manifests (Docker, Kubernetes)
- Connection settings and credentials
- Resource limits and scaling rules
- High availability setup
- Monitoring configuration

### Monitoring & Observability
- Key metrics to track
- Alerting rules
- Distributed tracing integration
- Dashboard templates
- Log aggregation

### Migration Strategy
- If migrating from existing system
- Phased rollout plan
- Dual-write strategy
- Rollback procedures

## Examples

### Setup Kafka for Event Streaming
```
/setup-messaging

Implement Kafka for order events with exactly-once delivery,
10 partitions for high throughput, and stream processing for analytics
```

### Setup RabbitMQ for Task Queue
```
/setup-messaging

Setup RabbitMQ for background job processing with retry logic,
dead letter queue, and priority queue support
```

### Setup NATS for Microservices
```
/setup-messaging

Implement NATS JetStream for microservices communication with
request/reply pattern and guaranteed delivery
```

### Setup Redis Pub/Sub for Notifications
```
/setup-messaging

Setup Redis pub/sub for real-time notifications with WebSocket
integration and channel-based subscriptions
```

## Message Broker Patterns Applied

### NATS Patterns
- Subject-based routing with wildcards
- Queue groups for load balancing
- JetStream for persistence and guaranteed delivery
- Key-value store for configuration

### RabbitMQ Patterns
- Topic exchanges for flexible routing
- Quorum queues for high availability
- Dead letter exchanges for failed messages
- Consumer prefetch and acknowledgments

### Kafka Patterns
- Partitioned topics for parallelism
- Consumer groups for scalability
- Compacted topics for state
- Exactly-once semantics with transactions

### Redis Patterns
- Pub/sub for ephemeral messages
- Streams for persistent messaging
- Consumer groups for competing consumers
- Sorted sets for priority queues

## Best Practices Applied

- **Reliability**: Acknowledgments, retries, dead letter queues
- **Performance**: Batching, compression, partitioning
- **Scalability**: Consumer groups, horizontal scaling
- **Monitoring**: Metrics, tracing, alerting
- **Security**: Authentication, authorization, encryption
- **Operations**: Deployment automation, disaster recovery

Provide production-ready messaging implementations with complete configuration and code examples.
