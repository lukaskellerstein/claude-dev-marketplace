---
name: message-patterns
description: Auto-invoked when working with message brokers, events, or async communication to ensure proper messaging patterns
allowed-tools: Read, Grep, Glob
---

# Message Broker and Event-Driven Patterns

This skill provides guidance on message broker patterns and event-driven architecture best practices.

## When Active

This skill activates when you:
- Design message schemas or events
- Implement producers or consumers
- Configure message brokers
- Design event-driven workflows
- Implement saga patterns
- Work with async communication

## Message Design Patterns

### Event Naming
Use past tense for events (something that happened):
- `OrderCreated`, `UserRegistered`, `PaymentProcessed`
- Include version in event type: `OrderCreated.v1`
- Use domain language consistently

```json
// Good event name
{
  "eventType": "OrderCreated.v1",
  "eventId": "evt_123456",
  "timestamp": "2025-01-15T10:30:00Z",
  "data": { ... }
}

// Bad event name (using present/future tense or commands)
{
  "eventType": "CreateOrder",  // This is a command, not an event
  "eventType": "OrderWillBeCreated"  // Future tense
}
```

### Event Structure
Use consistent envelope structure:

```json
{
  "eventId": "evt_123456",
  "eventType": "OrderCreated.v1",
  "eventVersion": "1.0",
  "timestamp": "2025-01-15T10:30:00Z",
  "correlationId": "corr_789",
  "causationId": "evt_000",
  "source": "order-service",
  "subject": "orders/123",
  "data": {
    "orderId": "123",
    "customerId": "456",
    "totalAmount": 99.99,
    "currency": "USD",
    "items": [...]
  },
  "metadata": {
    "userId": "user_789",
    "traceId": "trace_xyz"
  }
}
```

### Event Versioning
Support multiple event versions simultaneously:

```json
// v1
{
  "eventType": "OrderCreated.v1",
  "data": {
    "orderId": "123",
    "amount": 99.99
  }
}

// v2 - added currency field
{
  "eventType": "OrderCreated.v2",
  "data": {
    "orderId": "123",
    "totalAmount": 99.99,
    "currency": "USD"
  }
}
```

Consumers should handle both versions:
```javascript
function handleOrderCreated(event) {
  switch(event.eventType) {
    case 'OrderCreated.v1':
      return processV1(event.data);
    case 'OrderCreated.v2':
      return processV2(event.data);
    default:
      throw new Error(`Unsupported version: ${event.eventType}`);
  }
}
```

## Messaging Patterns

### Publish/Subscribe
One publisher, multiple subscribers receive the same message.

**Use for:**
- Broadcasting events (UserCreated, OrderPlaced)
- Fan-out notifications
- Event sourcing

**NATS Example:**
```javascript
// Publisher
await nc.publish('orders.created', JSON.stringify(event));

// Subscriber 1 (analytics)
nc.subscribe('orders.created', (msg) => {
  updateAnalytics(msg.data);
});

// Subscriber 2 (notifications)
nc.subscribe('orders.created', (msg) => {
  sendNotification(msg.data);
});
```

**RabbitMQ Example:**
```javascript
// Publisher to fanout exchange
channel.publish('order_events', '', Buffer.from(JSON.stringify(event)));

// Subscriber 1
channel.consume('analytics_queue', (msg) => {
  updateAnalytics(JSON.parse(msg.content));
  channel.ack(msg);
});
```

### Point-to-Point Queue
One publisher, one consumer processes each message.

**Use for:**
- Task distribution
- Load balancing
- Background jobs

**NATS Example with Queue Group:**
```javascript
// Publishers
for (let i = 0; i < 100; i++) {
  await nc.publish('jobs.process', JSON.stringify({taskId: i}));
}

// Multiple consumers in queue group
// Only one consumer receives each message
nc.subscribe('jobs.process', {queue: 'workers'}, (msg) => {
  processJob(msg.data);
});
```

**RabbitMQ Example:**
```javascript
// Multiple workers competing for jobs
channel.prefetch(1); // Process one at a time
channel.consume('jobs_queue', (msg) => {
  processJob(JSON.parse(msg.content));
  channel.ack(msg);
}, {noAck: false});
```

### Request/Reply
Synchronous-style communication over async transport.

**Use for:**
- RPC over message broker
- Query patterns in CQRS

**NATS Example:**
```javascript
// Request
const response = await nc.request('user.get',
  JSON.stringify({userId: '123'}),
  {timeout: 5000}
);

// Responder
nc.subscribe('user.get', (msg) => {
  const user = getUser(JSON.parse(msg.data).userId);
  msg.respond(JSON.stringify(user));
});
```

### Fan-out / Fan-in
Distribute work to multiple processors, aggregate results.

**Use for:**
- Parallel processing
- Map-reduce patterns
- Distributed computations

### Dead Letter Queue (DLQ)
Handle messages that fail processing.

**RabbitMQ Example:**
```javascript
// Define DLQ
channel.assertQueue('orders_dlq', {durable: true});

// Main queue with DLX
channel.assertQueue('orders', {
  durable: true,
  arguments: {
    'x-dead-letter-exchange': '',
    'x-dead-letter-routing-key': 'orders_dlq'
  }
});

// Consumer with retries
channel.consume('orders', async (msg) => {
  try {
    await processOrder(JSON.parse(msg.content));
    channel.ack(msg);
  } catch (error) {
    // Will go to DLQ after max retries
    channel.nack(msg, false, false);
  }
});
```

## Advanced Patterns

### Saga Pattern
Coordinate distributed transactions across services.

**Orchestration-based Saga:**
```javascript
// Order saga orchestrator
class OrderSaga {
  async execute(order) {
    const sagaId = generateId();

    try {
      // Step 1: Reserve inventory
      await publish('inventory.reserve', {
        sagaId,
        orderId: order.id,
        items: order.items
      });
      await waitForEvent('inventory.reserved', sagaId);

      // Step 2: Process payment
      await publish('payment.process', {
        sagaId,
        orderId: order.id,
        amount: order.total
      });
      await waitForEvent('payment.processed', sagaId);

      // Step 3: Ship order
      await publish('shipping.create', {
        sagaId,
        orderId: order.id
      });

      return {success: true};
    } catch (error) {
      // Compensate
      await this.compensate(sagaId, error);
      return {success: false, error};
    }
  }

  async compensate(sagaId, error) {
    await publish('inventory.release', {sagaId});
    await publish('payment.refund', {sagaId});
  }
}
```

**Choreography-based Saga:**
```javascript
// Each service handles its own compensation

// Inventory service
subscribe('inventory.reserve', async (msg) => {
  const {sagaId, items} = msg.data;
  try {
    await reserveItems(items);
    await publish('inventory.reserved', {sagaId});
  } catch (error) {
    await publish('inventory.reserve.failed', {sagaId, error});
  }
});

subscribe('order.failed', async (msg) => {
  await releaseReservation(msg.data.sagaId);
});
```

### Outbox Pattern
Ensure message publishing and database update are atomic.

```javascript
// In transaction: save entity and outbox message
async function createOrder(order) {
  return db.transaction(async (tx) => {
    // 1. Insert order
    await tx.orders.create(order);

    // 2. Insert outbox message
    await tx.outbox.create({
      eventType: 'OrderCreated.v1',
      aggregateId: order.id,
      payload: JSON.stringify(order),
      createdAt: new Date()
    });
  });
}

// Background worker publishes outbox messages
setInterval(async () => {
  const messages = await db.outbox.findMany({
    where: {published: false},
    limit: 100
  });

  for (const msg of messages) {
    await messagebroker.publish(msg.eventType, msg.payload);
    await db.outbox.update({
      where: {id: msg.id},
      data: {published: true}
    });
  }
}, 1000);
```

### Inbox Pattern
Ensure idempotent message processing.

```javascript
// Check inbox before processing
async function handleOrderCreated(event) {
  return db.transaction(async (tx) => {
    // 1. Check if already processed
    const existing = await tx.inbox.findUnique({
      where: {eventId: event.eventId}
    });

    if (existing) {
      return; // Already processed
    }

    // 2. Insert inbox record
    await tx.inbox.create({
      eventId: event.eventId,
      eventType: event.eventType,
      processedAt: new Date()
    });

    // 3. Process event
    await processOrder(event.data);
  });
}
```

## Reliability Patterns

### At-Least-Once Delivery
Message may be delivered multiple times.

**Implementation:**
- Producer: Retry on failure
- Consumer: Acknowledge after processing
- Implement idempotency in consumers

### Exactly-Once Delivery
Message processed exactly once.

**Kafka Example:**
```javascript
// Producer with idempotence
const producer = kafka.producer({
  transactionalId: 'order-producer',
  idempotent: true
});

// Consumer with exactly-once
const consumer = kafka.consumer({
  groupId: 'order-processor',
  isolation: 'read_committed'
});

// Transactional processing
const transaction = await producer.transaction();
try {
  await transaction.send({topic: 'orders', messages: [...]});
  await processOrder();
  await transaction.commit();
} catch (e) {
  await transaction.abort();
}
```

### Retry with Exponential Backoff
```javascript
async function consumeWithRetry(message, maxRetries = 5) {
  let retries = 0;
  let delay = 1000; // Start with 1 second

  while (retries < maxRetries) {
    try {
      await processMessage(message);
      return; // Success
    } catch (error) {
      retries++;
      if (retries >= maxRetries) {
        // Send to DLQ
        await sendToDLQ(message, error);
        return;
      }
      // Exponential backoff
      await sleep(delay);
      delay *= 2; // 1s, 2s, 4s, 8s, 16s
    }
  }
}
```

## Broker-Specific Best Practices

### NATS
- Use hierarchical subjects: `orders.created.v1`
- Use wildcards for subscriptions: `orders.*` or `orders.>`
- Use queue groups for load balancing
- Enable JetStream for persistence

### RabbitMQ
- Use topic exchanges for flexible routing
- Set prefetch limit to control concurrency
- Always acknowledge messages
- Use quorum queues for HA

### Kafka
- Choose partition count based on max parallelism
- Use consistent partition keys for ordering
- Monitor consumer lag
- Use schema registry for Avro/Protobuf

### Redis
- Use Redis Streams over pub/sub for persistence
- Implement consumer groups for parallel processing
- Use XACK for message acknowledgment
- Monitor stream length

## Checklist

When working with messages:
- [ ] Is event naming consistent (past tense)?
- [ ] Is event structure versioned and evolvable?
- [ ] Are correlation and causation IDs included?
- [ ] Is message processing idempotent?
- [ ] Are retries implemented with exponential backoff?
- [ ] Is there a dead letter queue for failed messages?
- [ ] Are messages acknowledged after processing?
- [ ] Is ordering guaranteed where needed?
- [ ] Are distributed transactions handled (saga)?
- [ ] Is monitoring configured (lag, errors, throughput)?
- [ ] Are secrets and credentials secured?

Use this guidance to build reliable, scalable message-driven systems.
