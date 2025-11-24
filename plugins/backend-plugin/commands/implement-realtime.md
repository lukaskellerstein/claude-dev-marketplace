---
description: Implement WebSocket, Server-Sent Events, or real-time communication for live updates
---

Design and implement real-time bidirectional communication for interactive features like chat, notifications, live dashboards, or collaborative tools.

## Process

Follow these steps:

1. **Analyze Requirements**: Understand real-time needs
   - Identify use case (chat, notifications, live updates, collaboration)
   - Determine latency and performance requirements
   - Assess scale (concurrent connections, messages per second)
   - Review existing infrastructure and client applications

2. **Launch Real-time Communication Expert**: Use the `realtime-communication-expert` agent to:
   - Choose technology (WebSocket, SSE, Long Polling)
   - Design protocol and message types
   - Plan authentication and authorization
   - Design connection management and lifecycle
   - Plan scaling strategy for multiple instances
   - Design monitoring and debugging approach

3. **Message Broker Integration** (if needed): If integrating with message broker, use the `message-broker-expert` agent to:
   - Design message flow between broker and WebSocket
   - Setup pub/sub for cross-instance communication
   - Design message routing and filtering

4. **Implementation Guide**: Provide:
   - Server-side WebSocket handler implementation
   - Client-side connection management
   - Reconnection and error handling logic
   - Scaling configuration

## Output

Present a comprehensive real-time communication solution including:

### Technology Selection
- Chosen technology (WebSocket, SSE, etc.)
- Detailed rationale and trade-offs
- Browser compatibility considerations
- Fallback strategy

### Protocol Design
- Message types and event schemas
- Binary vs text protocol
- Compression strategy
- Message envelope structure
- Example messages for all scenarios

### Authentication & Authorization
- Connection authentication flow
- Token-based or session-based auth
- Per-message authorization (if needed)
- Origin validation
- CORS configuration

### Connection Management
- Lifecycle (connect, message, disconnect)
- Heartbeat/ping-pong mechanism
- Timeout configuration
- Graceful shutdown
- Connection limits per user

### Server Implementation
- WebSocket handler/controller code
- Connection registry and state management
- Broadcasting to multiple clients
- Room/channel management
- Message routing logic
- Error handling
- Code examples in project's framework

### Client Implementation
- Connection establishment
- Event listeners and handlers
- Reconnection logic with exponential backoff
- Message queueing during disconnection
- Error handling and user feedback
- Code examples in JavaScript/TypeScript

### Scaling Strategy
- Load balancer configuration (sticky sessions)
- Message broker integration (Redis, NATS)
- Cross-instance message distribution
- Presence tracking across instances
- Horizontal scaling approach

### Security Measures
- Input validation
- Rate limiting per connection
- XSS prevention
- DDoS protection
- Monitoring for abuse

### Performance Optimization
- Message batching
- Binary protocol (MessagePack, Protobuf)
- Compression (permessage-deflate)
- Connection pooling
- Memory management

### Monitoring & Debugging
- Active connections metric
- Messages per second
- Latency measurements
- Error rate tracking
- Connection lifecycle logging
- Debug tools and dashboards

### Deployment Configuration
- Server deployment settings
- Load balancer configuration
- Resource limits
- Auto-scaling rules
- Health checks

## Examples

### Implement Chat System
```
/implement-realtime

Build a real-time chat system with private messages, group channels,
typing indicators, read receipts, and user presence
```

### Implement Live Dashboard
```
/implement-realtime

Create WebSocket connection for live dashboard with real-time metrics,
automatic reconnection, and 1000+ concurrent users
```

### Implement Notifications
```
/implement-realtime

Setup real-time push notifications with multiple channels,
badge counts, and delivery tracking
```

### Implement Collaborative Editing
```
/implement-realtime

Implement real-time collaborative editing with operational transformation,
cursor tracking, and presence indicators
```

## Patterns Applied

### Connection Patterns
- Heartbeat for connection health
- Exponential backoff for reconnection
- Graceful degradation to polling
- Connection pooling and reuse

### Message Patterns
- Request/response over WebSocket
- Broadcast to all clients
- Targeted messaging to specific users
- Room/channel-based messaging
- Message acknowledgments

### Scaling Patterns
- Sticky sessions with load balancer
- Redis pub/sub for cross-instance
- Shared state in distributed cache
- Connection distribution monitoring

### Security Patterns
- Token in handshake, not messages
- Rate limiting per connection
- Input validation on all messages
- Origin whitelist

## Best Practices Applied

- **Reliability**: Reconnection, message queuing, acknowledgments
- **Performance**: Binary protocols, compression, batching
- **Security**: Authentication, validation, rate limiting
- **Scalability**: Horizontal scaling, message brokers
- **Monitoring**: Connection tracking, error rates, latency
- **UX**: Offline indicators, reconnection feedback, loading states

Provide production-ready real-time implementations with working code, configuration, and deployment guides.
