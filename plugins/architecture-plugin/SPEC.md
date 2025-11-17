# Architecture Plugin Specification

## Plugin Overview

**Name**: `architecture-plugin`  
**Version**: `1.0.0`  
**Description**: Comprehensive architecture design toolkit for microservices, cloud patterns, monolithic systems, event-driven architectures, and system design best practices.

## Core Capabilities

### Architecture Patterns

- **Microservices**: Domain-driven design, service boundaries, communication patterns
- **Monolithic**: Modular monoliths, clean architecture, layered architecture
- **3-Layer Architecture**: Presentation → Business Logic → Data Access
- **Event-Driven**: Event sourcing, CQRS, saga patterns
- **Cloud Native**: 12-factor apps, serverless, container orchestration

### Communication Patterns

- **Synchronous**: REST, GraphQL, gRPC
- **Asynchronous**: Message queues, event streams, pub/sub
- **Service Mesh**: Circuit breakers, retries, load balancing
- **API Gateway**: Rate limiting, authentication, routing

### Design Patterns

- **Creational**: Factory, Builder, Singleton
- **Structural**: Adapter, Facade, Proxy
- **Behavioral**: Strategy, Observer, Command
- **Integration**: Gateway, Translator, Canonical Data Model

## Plugin Structure

```
architecture-plugin/
├── manifest.json
├── commands/
│   ├── architect.md          # Main architecture command
│   ├── analyze.md            # Analyze existing architecture
│   ├── migrate.md            # Migration strategies
│   ├── visualize.md          # Architecture diagrams
│   └── pattern.md            # Apply design patterns
├── agents/
│   ├── microservices-architect.md
│   ├── cloud-architect.md
│   ├── monolith-specialist.md
│   ├── event-architect.md
│   ├── ddd-expert.md
│   └── patterns-expert.md
├── skills/
│   ├── service-boundaries.md
│   ├── anti-patterns.md
│   ├── scalability-check.md
│   └── coupling-analysis.md
├── mcp-servers/
│   └── config.json
└── output-styles/
    ├── architecture-doc.md
    ├── adr-template.md
    └── c4-diagram.md
```

## Manifest Configuration

```json
{
  "name": "architecture-plugin",
  "version": "1.0.0",
  "description": "Architecture design toolkit for microservices, cloud patterns, and system design",
  "author": {
    "name": "Claude Code Team",
    "email": "team@claude.code",
    "url": "https://github.com/claude-code/architecture-plugin"
  },
  "keywords": [
    "architecture",
    "microservices",
    "ddd",
    "event-sourcing",
    "cqrs",
    "monolith",
    "cloud",
    "patterns",
    "system-design",
    "saga"
  ],
  "commands": [
    "./commands/architect.md",
    "./commands/analyze.md",
    "./commands/migrate.md",
    "./commands/visualize.md",
    "./commands/pattern.md"
  ],
  "agents": "./agents/",
  "skills": "./skills/",
  "hooks": "./hooks/hooks.json",
  "mcpServers": "./mcp-servers/config.json",
  "outputStyles": "./output-styles/"
}
```

## Commands

### `/architect` Command

```markdown
---
description: Design and implement architecture patterns
allowed-tools: Bash, Read, Write, Execute
---

# Architect Command

Design system architecture with best practices and patterns.

## Usage

`/architect [pattern] [scope] [options]`

## Patterns

- `microservices` - Microservices architecture
- `monolith` - Monolithic architecture
- `event-driven` - Event-driven architecture
- `3-layer` - Three-layer architecture
- `serverless` - Serverless architecture
- `hybrid` - Hybrid approach

## Scope

- `new` - Design from scratch
- `refactor` - Refactor existing system
- `extend` - Extend current architecture

## Implementation

!`
#!/bin/bash

PATTERN=$1
SCOPE=$2
OPTIONS=$3

# Analyze current project structure

analyze_project() {
echo "Analyzing project structure..."

    # Check for existing services
    if [ -d "services" ] || [ -d "microservices" ]; then
        echo "Detected microservices structure"
        return 1
    fi

    # Check for monolithic indicators
    if [ -f "app.js" ] || [ -f "main.go" ] || [ -f "app.py" ]; then
        echo "Detected monolithic structure"
        return 2
    fi

    echo "New project detected"
    return 0

}

PROJECT_TYPE=$(analyze_project)

case $PATTERN in
microservices)
echo "Designing microservices architecture..."
echo "Scope: $SCOPE" # Invoke microservices-architect agent
;;
monolith)
echo "Designing monolithic architecture..."
echo "Scope: $SCOPE" # Invoke monolith-specialist agent
;;
event-driven)
echo "Designing event-driven architecture..." # Invoke event-architect agent
;;
3-layer)
echo "Designing 3-layer architecture..." # Creates UI, API, and DB layers
;;
serverless)
echo "Designing serverless architecture..." # Invoke cloud-architect agent with serverless context
;;
hybrid)
echo "Designing hybrid architecture..." # Combines patterns based on requirements
;;
\*)
echo "Usage: /architect [microservices|monolith|event-driven|3-layer|serverless|hybrid] [new|refactor|extend]"
exit 1
;;
esac
`
```

### `/analyze` Command

```markdown
---
description: Analyze existing architecture for issues and improvements
allowed-tools: Bash, Read, Analyze
---

# Analyze Command

Analyze current architecture for patterns, anti-patterns, and improvements.

## Usage

`/analyze [aspect]`

## Aspects

- `dependencies` - Analyze service dependencies
- `coupling` - Check coupling between components
- `complexity` - Measure system complexity
- `patterns` - Identify design patterns
- `anti-patterns` - Detect anti-patterns
- `all` - Complete analysis

!`
#!/bin/bash

ASPECT=${1:-all}

echo "Architecture Analysis: $ASPECT"

case $ASPECT in
dependencies)
echo "Analyzing dependencies..." # Find all package files
find . -name "package.json" -o -name "go.mod" -o -name "requirements.txt" | while read file; do
echo "Found: $file"
done # Invoke patterns-expert to analyze
;;
coupling)
echo "Analyzing coupling..." # Check import statements and module boundaries
;;
complexity)
echo "Measuring complexity..." # Count services, endpoints, dependencies
;;
patterns)
echo "Identifying patterns..." # Detect common design patterns
;;
anti-patterns)
echo "Detecting anti-patterns..." # Check for god objects, circular dependencies, etc.
;;
all)
echo "Running complete analysis..."
;;
esac
`
```

### `/migrate` Command

```markdown
---
description: Create migration strategy from one architecture to another
allowed-tools: Read, Write, Plan
---

# Migrate Command

Plan and execute architecture migrations.

## Usage

`/migrate [from] [to] [strategy]`

## Migration Paths

- `monolith-to-microservices` - Strangler fig pattern
- `microservices-to-monolith` - Service consolidation
- `on-premise-to-cloud` - Cloud migration
- `sync-to-event` - Event-driven transformation

## Strategies

- `big-bang` - Complete rewrite
- `strangler` - Gradual replacement
- `parallel` - Run both systems
- `phased` - Phase by phase

!`
#!/bin/bash

FROM=$1
TO=$2
STRATEGY=${3:-strangler}

echo "Migration Plan: $FROM → $TO"
echo "Strategy: $STRATEGY"

# Generate migration plan based on pattern

case "${FROM}-to-${TO}" in
monolith-to-microservices)
echo "Generating Strangler Fig migration plan..." # Invoke microservices-architect with migration context
;;
microservices-to-monolith)
echo "Generating consolidation plan..." # Invoke monolith-specialist with consolidation context
;;
\*)
echo "Analyzing custom migration path..."
;;
esac
`
```

### `/visualize` Command

```markdown
---
description: Generate architecture diagrams and visualizations
allowed-tools: Write, Execute
---

# Visualize Command

Create architecture diagrams using PlantUML, Mermaid, or C4.

## Usage

`/visualize [type] [level]`

## Types

- `c4` - C4 model diagrams
- `flow` - Data flow diagrams
- `sequence` - Sequence diagrams
- `component` - Component diagrams
- `deployment` - Deployment diagrams

## Levels (for C4)

- `context` - System context
- `container` - Container diagram
- `component` - Component diagram
- `code` - Code diagram

!`
#!/bin/bash

TYPE=$1
LEVEL=${2:-context}

case $TYPE in
c4)
echo "Generating C4 $LEVEL diagram..." # Generate PlantUML C4 diagram
;;
flow)
echo "Generating data flow diagram..." # Generate Mermaid flowchart
;;
sequence)
echo "Generating sequence diagram..." # Generate sequence diagram
;;
component)
echo "Generating component diagram..."
;;
deployment)
echo "Generating deployment diagram..."
;;
esac
`
```

### `/pattern` Command

```markdown
---
description: Apply design patterns to solve specific problems
allowed-tools: Read, Write, Refactor
---

# Pattern Command

Apply design patterns to solve architectural problems.

## Usage

`/pattern [pattern] [context]`

## Patterns

- `repository` - Repository pattern for data access
- `factory` - Factory pattern for object creation
- `strategy` - Strategy pattern for algorithms
- `observer` - Observer pattern for events
- `saga` - Saga pattern for transactions
- `cqrs` - Command Query Responsibility Segregation
- `event-sourcing` - Event sourcing for state

!`
#!/bin/bash

PATTERN=$1
CONTEXT=$2

echo "Applying $PATTERN pattern"

case $PATTERN in
repository)
echo "Implementing Repository pattern..." # Generate repository interfaces and implementations
;;
saga)
echo "Implementing Saga pattern..." # Generate saga orchestrator or choreography
;;
cqrs)
echo "Implementing CQRS pattern..." # Separate command and query models
;;
event-sourcing)
echo "Implementing Event Sourcing..." # Create event store and projections
;;
\*)
echo "Implementing $PATTERN pattern..." # Invoke patterns-expert agent
;;
esac
`
```

## Agents

### microservices-architect.md

````markdown
---
name: microservices-architect
description: Expert in microservices design, DDD, and distributed systems
tools: Read, Write, Design, Analyze
model: opus
---

# Microservices Architect

Expert in designing scalable microservices architectures with proper boundaries and communication patterns.

## Domain-Driven Design (DDD)

### Identifying Bounded Contexts

```yaml
# Example: E-commerce System
bounded_contexts:
  catalog:
    aggregates:
      - Product
      - Category
    services:
      - ProductService
      - SearchService

  ordering:
    aggregates:
      - Order
      - Cart
    services:
      - OrderService
      - CartService

  payment:
    aggregates:
      - Payment
      - Invoice
    services:
      - PaymentService
      - BillingService

  shipping:
    aggregates:
      - Shipment
      - Tracking
    services:
      - ShippingService
      - TrackingService
```
````

### Service Communication Patterns

#### Synchronous Communication

```typescript
// API Gateway Pattern
class APIGateway {
  async getOrderDetails(orderId: string) {
    // Aggregate data from multiple services
    const [order, payment, shipping] = await Promise.all([
      this.orderService.getOrder(orderId),
      this.paymentService.getPayment(orderId),
      this.shippingService.getShipment(orderId),
    ]);

    return {
      order,
      payment,
      shipping,
    };
  }
}
```

#### Asynchronous Communication

```typescript
// Event-Driven Communication
interface OrderEvent {
  eventId: string;
  aggregateId: string;
  eventType: "OrderCreated" | "OrderShipped" | "OrderCancelled";
  payload: any;
  timestamp: Date;
}

class OrderService {
  async createOrder(orderData: CreateOrderDto) {
    // Create order
    const order = await this.orderRepo.save(orderData);

    // Publish event
    await this.eventBus.publish("order.created", {
      eventId: uuid(),
      aggregateId: order.id,
      eventType: "OrderCreated",
      payload: order,
      timestamp: new Date(),
    });

    return order;
  }
}
```

### Service Mesh Implementation

```yaml
# Istio Service Mesh Configuration
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: order-service
spec:
  hosts:
    - order-service
  http:
    - match:
        - headers:
            x-version:
              exact: v2
      route:
        - destination:
            host: order-service
            subset: v2
    - route:
        - destination:
            host: order-service
            subset: v1
          weight: 90
        - destination:
            host: order-service
            subset: v2
          weight: 10
```

### Data Management Patterns

#### Database per Service

```yaml
services:
  order-service:
    database: postgres
    schema: orders

  product-service:
    database: mongodb
    collection: products

  search-service:
    database: elasticsearch
    index: products
```

#### Saga Pattern for Distributed Transactions

```typescript
class OrderSaga {
  private steps = [
    { service: "order", action: "create", compensate: "cancel" },
    { service: "payment", action: "charge", compensate: "refund" },
    { service: "inventory", action: "reserve", compensate: "release" },
    { service: "shipping", action: "schedule", compensate: "cancel" },
  ];

  async execute(orderData: any) {
    const completed = [];

    try {
      for (const step of this.steps) {
        await this.executeStep(step, orderData);
        completed.push(step);
      }
    } catch (error) {
      // Compensate in reverse order
      for (const step of completed.reverse()) {
        await this.compensateStep(step, orderData);
      }
      throw error;
    }
  }
}
```

## Service Discovery and Load Balancing

```yaml
# Consul Service Discovery
service:
  name: order-service
  port: 8080
  tags:
    - version:1.0.0
    - environment:production
  check:
    http: http://localhost:8080/health
    interval: 10s
  connect:
    sidecar_service:
      proxy:
        upstreams:
          - destination_name: payment-service
            local_bind_port: 9001
          - destination_name: inventory-service
            local_bind_port: 9002
```

## Best Practices

1. **Service Boundaries**: Align with business domains
2. **Data Consistency**: Use eventual consistency
3. **Service Discovery**: Implement dynamic discovery
4. **Circuit Breakers**: Prevent cascade failures
5. **Observability**: Distributed tracing, metrics, logs
6. **API Versioning**: Support multiple versions
7. **Security**: Service-to-service authentication

````

### cloud-architect.md

```markdown
---
name: cloud-architect
description: Cloud-native architecture expert for AWS, GCP, Azure
tools: Read, Write, Design, Deploy
model: opus
---

# Cloud Architect

Expert in cloud-native architectures, serverless patterns, and cloud migrations.

## Cloud-Native Patterns

### 12-Factor App Principles
```yaml
principles:
  1_codebase: One codebase in version control
  2_dependencies: Explicitly declare dependencies
  3_config: Store config in environment
  4_backing_services: Treat as attached resources
  5_build_release_run: Separate build and run stages
  6_processes: Execute as stateless processes
  7_port_binding: Export services via port binding
  8_concurrency: Scale out via process model
  9_disposability: Fast startup and graceful shutdown
  10_dev_prod_parity: Keep environments similar
  11_logs: Treat logs as event streams
  12_admin_processes: Run admin tasks as one-off processes
````

### Serverless Architecture

```typescript
// AWS Lambda Function Structure
export const handler = async (
  event: APIGatewayEvent
): Promise<APIGatewayProxyResult> => {
  // Parse request
  const body = JSON.parse(event.body || "{}");

  try {
    // Business logic
    const result = await processRequest(body);

    // Return success
    return {
      statusCode: 200,
      headers: {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
      },
      body: JSON.stringify(result),
    };
  } catch (error) {
    // Error handling
    return {
      statusCode: 500,
      body: JSON.stringify({ error: error.message }),
    };
  }
};

// Infrastructure as Code (CDK)
class ServerlessStack extends Stack {
  constructor(scope: App, id: string) {
    super(scope, id);

    // DynamoDB Table
    const table = new Table(this, "OrderTable", {
      partitionKey: { name: "id", type: AttributeType.STRING },
      billingMode: BillingMode.PAY_PER_REQUEST,
    });

    // Lambda Function
    const orderFunction = new Function(this, "OrderFunction", {
      runtime: Runtime.NODEJS_18_X,
      handler: "index.handler",
      code: Code.fromAsset("lambda"),
      environment: {
        TABLE_NAME: table.tableName,
      },
    });

    // API Gateway
    const api = new RestApi(this, "OrderAPI");
    api.root
      .addResource("orders")
      .addMethod("POST", new LambdaIntegration(orderFunction));

    // Grant permissions
    table.grantReadWriteData(orderFunction);
  }
}
```

### Container Orchestration (Kubernetes)

```yaml
# Deployment Configuration
apiVersion: apps/v1
kind: Deployment
metadata:
  name: order-service
spec:
  replicas: 3
  selector:
    matchLabels:
      app: order-service
  template:
    metadata:
      labels:
        app: order-service
    spec:
      containers:
        - name: order-service
          image: gcr.io/project/order-service:1.0.0
          ports:
            - containerPort: 8080
          env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: database-secret
                  key: url
          resources:
            requests:
              memory: "256Mi"
              cpu: "250m"
            limits:
              memory: "512Mi"
              cpu: "500m"
          livenessProbe:
            httpGet:
              path: /health
              port: 8080
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /ready
              port: 8080
            initialDelaySeconds: 5
            periodSeconds: 5
---
# Horizontal Pod Autoscaler
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: order-service-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: order-service
  minReplicas: 3
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
```

### Multi-Cloud Strategy

```typescript
// Cloud Provider Abstraction
interface CloudStorage {
  upload(key: string, data: Buffer): Promise<void>;
  download(key: string): Promise<Buffer>;
  delete(key: string): Promise<void>;
}

class AWSStorage implements CloudStorage {
  async upload(key: string, data: Buffer) {
    await s3
      .putObject({
        Bucket: this.bucket,
        Key: key,
        Body: data,
      })
      .promise();
  }
}

class GCPStorage implements CloudStorage {
  async upload(key: string, data: Buffer) {
    await storage.bucket(this.bucket).file(key).save(data);
  }
}

class StorageFactory {
  static create(provider: "aws" | "gcp" | "azure"): CloudStorage {
    switch (provider) {
      case "aws":
        return new AWSStorage();
      case "gcp":
        return new GCPStorage();
      case "azure":
        return new AzureStorage();
    }
  }
}
```

## Cloud Migration Patterns

### Lift and Shift

- Minimal changes
- Quick migration
- Higher cloud costs

### Replatform

- Some optimization
- Use managed services
- Better cost-efficiency

### Refactor/Re-architect

- Cloud-native redesign
- Maximum benefits
- Highest effort

````

### monolith-specialist.md

```markdown
---
name: monolith-specialist
description: Expert in monolithic architecture, modular design, and clean architecture
tools: Read, Write, Refactor, Analyze
model: sonnet
---

# Monolith Specialist

Expert in designing maintainable monolithic architectures with clean boundaries and modular structure.

## Clean Architecture

### Layer Structure
````

├── presentation/ # UI/Controllers
│ ├── controllers/
│ ├── views/
│ └── validators/
├── application/ # Use Cases
│ ├── use-cases/
│ ├── dto/
│ └── mappers/
├── domain/ # Business Logic
│ ├── entities/
│ ├── value-objects/
│ └── domain-services/
├── infrastructure/ # External Services
│ ├── persistence/
│ ├── messaging/
│ └── external-apis/

````

### Three-Layer Architecture Implementation
```typescript
// Presentation Layer (Controller)
@Controller('/api/orders')
export class OrderController {
  constructor(
    private orderService: OrderService
  ) {}

  @Post()
  async createOrder(@Body() dto: CreateOrderDto) {
    // Validation handled by decorator
    const order = await this.orderService.createOrder(dto);
    return OrderResponseDto.fromEntity(order);
  }

  @Get('/:id')
  async getOrder(@Param('id') id: string) {
    const order = await this.orderService.getOrder(id);
    if (!order) {
      throw new NotFoundException('Order not found');
    }
    return OrderResponseDto.fromEntity(order);
  }
}

// Business Logic Layer (Service)
@Injectable()
export class OrderService {
  constructor(
    private orderRepository: OrderRepository,
    private inventoryService: InventoryService,
    private paymentService: PaymentService,
    private eventEmitter: EventEmitter
  ) {}

  async createOrder(dto: CreateOrderDto): Promise<Order> {
    // Begin transaction
    const transaction = await this.orderRepository.beginTransaction();

    try {
      // Business logic
      const order = Order.create(dto);

      // Check inventory
      await this.inventoryService.reserveItems(order.items);

      // Process payment
      await this.paymentService.processPayment(order.total);

      // Save order
      const savedOrder = await this.orderRepository.save(order, transaction);

      // Commit transaction
      await transaction.commit();

      // Emit event
      this.eventEmitter.emit('order.created', savedOrder);

      return savedOrder;
    } catch (error) {
      await transaction.rollback();
      throw error;
    }
  }
}

// Data Access Layer (Repository)
@Injectable()
export class OrderRepository {
  constructor(
    private db: Database
  ) {}

  async save(order: Order, transaction?: Transaction): Promise<Order> {
    const query = `
      INSERT INTO orders (id, customer_id, items, total, status, created_at)
      VALUES ($1, $2, $3, $4, $5, $6)
      RETURNING *
    `;

    const result = await this.db.query(query, [
      order.id,
      order.customerId,
      JSON.stringify(order.items),
      order.total,
      order.status,
      order.createdAt
    ], transaction);

    return Order.fromDatabase(result.rows[0]);
  }

  async findById(id: string): Promise<Order | null> {
    const query = 'SELECT * FROM orders WHERE id = $1';
    const result = await this.db.query(query, [id]);

    if (result.rows.length === 0) {
      return null;
    }

    return Order.fromDatabase(result.rows[0]);
  }
}
````

### Modular Monolith Pattern

```typescript
// Module Structure
modules/
├── catalog/
│   ├── application/
│   ├── domain/
│   ├── infrastructure/
│   └── catalog.module.ts
├── ordering/
│   ├── application/
│   ├── domain/
│   ├── infrastructure/
│   └── ordering.module.ts
├── payment/
│   ├── application/
│   ├── domain/
│   ├── infrastructure/
│   └── payment.module.ts
└── shared/
    ├── kernel/
    └── infrastructure/

// Module Boundary with Internal Events
@Module({
  imports: [SharedModule],
  controllers: [OrderController],
  providers: [OrderService, OrderRepository],
  exports: [OrderService]
})
export class OrderingModule {
  constructor(
    private eventBus: InternalEventBus
  ) {
    // Subscribe to events from other modules
    this.eventBus.subscribe('payment.completed',
      this.handlePaymentCompleted.bind(this)
    );
  }

  private async handlePaymentCompleted(event: PaymentCompletedEvent) {
    // Update order status
    await this.orderService.updateStatus(
      event.orderId,
      OrderStatus.PAID
    );
  }
}

// Internal Communication via Interfaces
interface CatalogService {
  getProduct(id: string): Promise<Product>;
  checkInventory(productId: string, quantity: number): Promise<boolean>;
  reserveInventory(items: OrderItem[]): Promise<void>;
}

// Dependency Injection
@Injectable()
export class OrderService {
  constructor(
    @Inject('CatalogService')
    private catalogService: CatalogService
  ) {}

  async validateOrder(items: OrderItem[]) {
    for (const item of items) {
      const available = await this.catalogService.checkInventory(
        item.productId,
        item.quantity
      );
      if (!available) {
        throw new Error(`Product ${item.productId} not available`);
      }
    }
  }
}
```

### Refactoring Strategies

#### Strangler Fig Pattern for Gradual Migration

```typescript
// Legacy Code Wrapper
class LegacyOrderService {
  createOrder(data: any): any {
    // Complex legacy logic
  }
}

// New Service with Adapter
@Injectable()
export class ModernOrderService {
  constructor(
    private legacyService: LegacyOrderService,
    private featureFlag: FeatureFlagService
  ) {}

  async createOrder(dto: CreateOrderDto): Promise<Order> {
    if (this.featureFlag.isEnabled("use-modern-order-flow")) {
      // New implementation
      return this.createModernOrder(dto);
    } else {
      // Delegate to legacy
      const legacyResult = this.legacyService.createOrder(dto);
      return this.adaptLegacyOrder(legacyResult);
    }
  }

  private createModernOrder(dto: CreateOrderDto): Promise<Order> {
    // Clean, modern implementation
  }

  private adaptLegacyOrder(legacyData: any): Order {
    // Convert legacy format to modern
  }
}
```

## Best Practices

1. **Module Boundaries**: Clear separation between modules
2. **Dependency Rule**: Dependencies point inward
3. **Database Transactions**: ACID compliance
4. **Feature Flags**: Gradual rollout of changes
5. **Vertical Slicing**: Organize by feature, not layer
6. **Testing Strategy**: Unit, integration, and E2E tests

````

### event-architect.md

```markdown
---
name: event-architect
description: Event-driven architecture expert specializing in event sourcing, CQRS, and messaging
tools: Read, Write, Design
model: opus
---

# Event-Driven Architecture Expert

Specialist in event sourcing, CQRS, event streaming, and asynchronous patterns.

## Event Sourcing Implementation

### Event Store Design
```typescript
// Event Definition
interface Event {
  aggregateId: string;
  aggregateType: string;
  eventType: string;
  eventVersion: number;
  payload: any;
  metadata: EventMetadata;
  timestamp: Date;
}

interface EventMetadata {
  userId: string;
  correlationId: string;
  causationId: string;
}

// Event Store Implementation
class EventStore {
  async append(events: Event[]): Promise<void> {
    const query = `
      INSERT INTO events
      (aggregate_id, aggregate_type, event_type, event_version,
       payload, metadata, timestamp)
      VALUES ($1, $2, $3, $4, $5, $6, $7)
    `;

    for (const event of events) {
      await this.db.query(query, [
        event.aggregateId,
        event.aggregateType,
        event.eventType,
        event.eventVersion,
        JSON.stringify(event.payload),
        JSON.stringify(event.metadata),
        event.timestamp
      ]);
    }

    // Publish to event bus
    await this.eventBus.publishBatch(events);
  }

  async getEvents(aggregateId: string, fromVersion?: number): Promise<Event[]> {
    const query = `
      SELECT * FROM events
      WHERE aggregate_id = $1
      ${fromVersion ? 'AND event_version > $2' : ''}
      ORDER BY event_version ASC
    `;

    const result = await this.db.query(
      query,
      fromVersion ? [aggregateId, fromVersion] : [aggregateId]
    );

    return result.rows.map(row => this.deserializeEvent(row));
  }
}

// Aggregate with Event Sourcing
class Order extends AggregateRoot {
  private status: OrderStatus;
  private items: OrderItem[];
  private customerId: string;

  // Replay events to rebuild state
  static async fromEvents(events: Event[]): Promise<Order> {
    const order = new Order();

    for (const event of events) {
      order.apply(event, false); // Don't record during replay
    }

    return order;
  }

  // Command handlers
  create(customerId: string, items: OrderItem[]): void {
    if (this.id) {
      throw new Error('Order already created');
    }

    this.apply(new OrderCreatedEvent({
      orderId: generateId(),
      customerId,
      items
    }));
  }

  ship(trackingNumber: string): void {
    if (this.status !== OrderStatus.PAID) {
      throw new Error('Order must be paid before shipping');
    }

    this.apply(new OrderShippedEvent({
      orderId: this.id,
      trackingNumber
    }));
  }

  // Event handlers
  protected onOrderCreated(event: OrderCreatedEvent): void {
    this.id = event.payload.orderId;
    this.customerId = event.payload.customerId;
    this.items = event.payload.items;
    this.status = OrderStatus.PENDING;
  }

  protected onOrderShipped(event: OrderShippedEvent): void {
    this.status = OrderStatus.SHIPPED;
    this.trackingNumber = event.payload.trackingNumber;
  }
}
````

### CQRS Pattern

```typescript
// Command Side
interface Command {
  aggregateId: string;
  payload: any;
}

class CommandBus {
  private handlers = new Map<string, CommandHandler>();

  register(commandType: string, handler: CommandHandler): void {
    this.handlers.set(commandType, handler);
  }

  async execute(command: Command): Promise<void> {
    const handler = this.handlers.get(command.constructor.name);
    if (!handler) {
      throw new Error(`No handler for ${command.constructor.name}`);
    }

    await handler.handle(command);
  }
}

@CommandHandler(CreateOrderCommand)
class CreateOrderHandler {
  constructor(private eventStore: EventStore) {}

  async handle(command: CreateOrderCommand): Promise<void> {
    const order = new Order();
    order.create(command.customerId, command.items);

    await this.eventStore.append(order.getUncommittedEvents());
  }
}

// Query Side (Read Model)
interface QueryModel {
  rebuild(): Promise<void>;
  handleEvent(event: Event): Promise<void>;
}

class OrderReadModel implements QueryModel {
  async rebuild(): Promise<void> {
    // Clear existing read model
    await this.db.query("TRUNCATE TABLE order_read_model");

    // Replay all events
    const events = await this.eventStore.getAllEvents("Order");

    for (const event of events) {
      await this.handleEvent(event);
    }
  }

  async handleEvent(event: Event): Promise<void> {
    switch (event.eventType) {
      case "OrderCreated":
        await this.db.query(
          `
          INSERT INTO order_read_model 
          (id, customer_id, items, status, created_at)
          VALUES ($1, $2, $3, $4, $5)
        `,
          [
            event.payload.orderId,
            event.payload.customerId,
            JSON.stringify(event.payload.items),
            "PENDING",
            event.timestamp,
          ]
        );
        break;

      case "OrderShipped":
        await this.db.query(
          `
          UPDATE order_read_model 
          SET status = 'SHIPPED', 
              tracking_number = $1,
              shipped_at = $2
          WHERE id = $3
        `,
          [event.payload.trackingNumber, event.timestamp, event.payload.orderId]
        );
        break;
    }
  }
}

// Query Service
class OrderQueryService {
  constructor(private readModel: OrderReadModel) {}

  async getOrder(id: string): Promise<OrderView> {
    const result = await this.db.query(
      "SELECT * FROM order_read_model WHERE id = $1",
      [id]
    );

    return OrderView.fromDatabase(result.rows[0]);
  }

  async getOrdersByCustomer(customerId: string): Promise<OrderView[]> {
    const result = await this.db.query(
      "SELECT * FROM order_read_model WHERE customer_id = $1",
      [customerId]
    );

    return result.rows.map((row) => OrderView.fromDatabase(row));
  }
}
```

### Event Streaming with Kafka

```typescript
// Producer Configuration
class EventProducer {
  private producer: Kafka.Producer;

  constructor() {
    this.producer = new Kafka.Producer({
      "metadata.broker.list": "localhost:9092",
      dr_cb: true,
    });
  }

  async publish(topic: string, event: Event): Promise<void> {
    const message = {
      key: event.aggregateId,
      value: JSON.stringify(event),
      headers: {
        "event-type": event.eventType,
        "aggregate-type": event.aggregateType,
      },
    };

    await this.producer.produce(
      topic,
      null,
      Buffer.from(message.value),
      message.key,
      Date.now(),
      message.headers
    );
  }
}

// Consumer Configuration
class EventConsumer {
  async consume(topics: string[], handler: EventHandler): Promise<void> {
    const consumer = new Kafka.KafkaConsumer({
      "group.id": "order-service",
      "metadata.broker.list": "localhost:9092",
      "enable.auto.commit": false,
    });

    consumer.subscribe(topics);

    consumer.on("data", async (message) => {
      const event = JSON.parse(message.value.toString());

      try {
        await handler.handle(event);
        consumer.commit(message);
      } catch (error) {
        // Handle error - dead letter queue
        await this.sendToDeadLetter(event, error);
      }
    });
  }
}
```

## Event-Driven Patterns

### Choreography vs Orchestration

```yaml
# Choreography - Events trigger reactions
OrderCreated → PaymentService subscribes → PaymentProcessed
PaymentProcessed → InventoryService subscribes → InventoryReserved
InventoryReserved → ShippingService subscribes → ShipmentScheduled

# Orchestration - Central coordinator
OrderSaga:
  1. Send CreateOrder command
  2. Wait for OrderCreated event
  3. Send ProcessPayment command
  4. Wait for PaymentProcessed event
  5. Send ReserveInventory command
  6. Wait for InventoryReserved event
  7. Send ScheduleShipment command
```

## Best Practices

1. **Event Schema Evolution**: Version events properly
2. **Idempotency**: Handle duplicate events
3. **Event Ordering**: Maintain order within aggregates
4. **Snapshots**: Periodic state snapshots for performance
5. **Projections**: Multiple read models for different use cases

````

### ddd-expert.md

```markdown
---
name: ddd-expert
description: Domain-Driven Design expert for complex business domains
tools: Read, Write, Analyze, Model
model: opus
---

# Domain-Driven Design Expert

Specialist in tactical and strategic DDD patterns for complex business domains.

## Strategic Design

### Bounded Context Mapping
```typescript
// Context Mapping Patterns
enum ContextRelationship {
  SHARED_KERNEL,      // Shared model between teams
  CUSTOMER_SUPPLIER,  // Upstream/downstream relationship
  CONFORMIST,         // Downstream conforms to upstream
  ANTICORRUPTION,     // Translation layer
  OPEN_HOST,          // Published language
  PUBLISHED_LANGUAGE, // Well-documented integration
  SEPARATE_WAYS       // No integration
}

// Example: E-Commerce Context Map
interface ContextMap {
  contexts: {
    catalog: {
      team: 'Product Team',
      relationships: {
        ordering: ContextRelationship.CUSTOMER_SUPPLIER,
        search: ContextRelationship.SHARED_KERNEL
      }
    },
    ordering: {
      team: 'Order Team',
      relationships: {
        catalog: ContextRelationship.ANTICORRUPTION,
        payment: ContextRelationship.CUSTOMER_SUPPLIER,
        shipping: ContextRelationship.OPEN_HOST
      }
    },
    payment: {
      team: 'Finance Team',
      relationships: {
        ordering: ContextRelationship.CONFORMIST,
        accounting: ContextRelationship.PUBLISHED_LANGUAGE
      }
    }
  }
}
````

### Ubiquitous Language

```typescript
// Domain Glossary
interface DomainTerms {
  // Order Context
  Order: "Customer purchase request with items and payment";
  OrderLine: "Single product with quantity in an order";
  OrderStatus: "Current state of order processing";

  // Product Context
  Product: "Sellable item with price and inventory";
  SKU: "Stock Keeping Unit - unique product identifier";
  Variant: "Product variation (size, color)";

  // Pricing Context
  Price: "Monetary value with currency";
  Discount: "Price reduction based on rules";
  PriceRule: "Logic for calculating final price";
}
```

## Tactical Patterns

### Aggregate Design

```typescript
// Aggregate Root
class Order implements AggregateRoot {
  private readonly id: OrderId;
  private customerId: CustomerId;
  private items: OrderItem[];
  private status: OrderStatus;
  private total: Money;

  // Invariants enforced at aggregate boundary
  addItem(product: ProductId, quantity: number, price: Money): void {
    // Business rule: Max 10 different products per order
    if (this.items.length >= 10) {
      throw new DomainException(
        "Order cannot have more than 10 different products"
      );
    }

    // Business rule: Order must be in DRAFT status
    if (this.status !== OrderStatus.DRAFT) {
      throw new DomainException("Cannot add items to confirmed order");
    }

    const item = new OrderItem(product, quantity, price);
    this.items.push(item);
    this.recalculateTotal();

    // Raise domain event
    this.addEvent(new OrderItemAddedEvent(this.id, item));
  }

  confirm(): void {
    // Business rule: Order must have items
    if (this.items.length === 0) {
      throw new DomainException("Cannot confirm empty order");
    }

    // Business rule: Total must be positive
    if (this.total.isNegativeOrZero()) {
      throw new DomainException("Order total must be positive");
    }

    this.status = OrderStatus.CONFIRMED;
    this.addEvent(new OrderConfirmedEvent(this.id, this.total));
  }

  private recalculateTotal(): void {
    this.total = this.items.reduce(
      (sum, item) => sum.add(item.getSubtotal()),
      Money.zero(this.total.currency)
    );
  }
}

// Value Objects
class Money implements ValueObject {
  constructor(
    private readonly amount: number,
    private readonly currency: Currency
  ) {
    if (amount < 0) {
      throw new Error("Money amount cannot be negative");
    }
  }

  add(other: Money): Money {
    if (!this.currency.equals(other.currency)) {
      throw new Error("Cannot add money with different currencies");
    }
    return new Money(this.amount + other.amount, this.currency);
  }

  equals(other: Money): boolean {
    return this.amount === other.amount && this.currency.equals(other.currency);
  }
}

// Entity within Aggregate
class OrderItem implements Entity {
  private readonly id: OrderItemId;
  private productId: ProductId;
  private quantity: Quantity;
  private unitPrice: Money;

  constructor(productId: ProductId, quantity: number, price: Money) {
    this.id = OrderItemId.generate();
    this.productId = productId;
    this.quantity = new Quantity(quantity);
    this.unitPrice = price;
  }

  getSubtotal(): Money {
    return this.unitPrice.multiply(this.quantity.value);
  }

  changeQuantity(newQuantity: number): void {
    this.quantity = new Quantity(newQuantity);
  }
}
```

### Domain Services

```typescript
// Domain Service for complex business logic
@DomainService()
class PricingService {
  calculateOrderTotal(
    items: OrderItem[],
    customer: Customer,
    promotions: Promotion[]
  ): Money {
    let subtotal = this.calculateSubtotal(items);

    // Apply customer-specific discounts
    const customerDiscount = this.getCustomerDiscount(customer);
    subtotal = subtotal.applyDiscount(customerDiscount);

    // Apply promotions
    for (const promotion of promotions) {
      if (promotion.isApplicable(items, customer)) {
        subtotal = promotion.apply(subtotal);
      }
    }

    return subtotal;
  }

  private calculateSubtotal(items: OrderItem[]): Money {
    return items.reduce(
      (sum, item) => sum.add(item.getSubtotal()),
      Money.zero("USD")
    );
  }
}
```

### Repository Pattern

```typescript
// Repository Interface (Domain Layer)
interface OrderRepository {
  save(order: Order): Promise<void>;
  findById(id: OrderId): Promise<Order | null>;
  findByCustomer(customerId: CustomerId): Promise<Order[]>;
  nextIdentity(): OrderId;
}

// Implementation (Infrastructure Layer)
class SqlOrderRepository implements OrderRepository {
  async save(order: Order): Promise<void> {
    const events = order.getUncommittedEvents();

    await this.db.transaction(async (trx) => {
      // Save aggregate state
      await trx.query(
        `
        INSERT INTO orders (id, customer_id, status, total, data)
        VALUES ($1, $2, $3, $4, $5)
        ON CONFLICT (id) DO UPDATE SET
          status = $3,
          total = $4,
          data = $5
      `,
        [
          order.id.value,
          order.customerId.value,
          order.status,
          order.total.amount,
          JSON.stringify(order),
        ]
      );

      // Save events
      for (const event of events) {
        await this.eventStore.append(event, trx);
      }
    });

    // Publish events after successful transaction
    for (const event of events) {
      await this.eventBus.publish(event);
    }
  }

  async findById(id: OrderId): Promise<Order | null> {
    const result = await this.db.query(
      "SELECT data FROM orders WHERE id = $1",
      [id.value]
    );

    if (result.rows.length === 0) return null;

    return Order.fromSnapshot(result.rows[0].data);
  }
}
```

### Specification Pattern

```typescript
// Specification for complex queries
abstract class Specification<T> {
  abstract isSatisfiedBy(candidate: T): boolean;

  and(other: Specification<T>): Specification<T> {
    return new AndSpecification(this, other);
  }

  or(other: Specification<T>): Specification<T> {
    return new OrSpecification(this, other);
  }

  not(): Specification<T> {
    return new NotSpecification(this);
  }
}

class HighValueOrderSpecification extends Specification<Order> {
  constructor(private threshold: Money) {
    super();
  }

  isSatisfiedBy(order: Order): boolean {
    return order.total.isGreaterThan(this.threshold);
  }
}

class PremiumCustomerOrderSpecification extends Specification<Order> {
  isSatisfiedBy(order: Order): boolean {
    return order.customer.isPremium();
  }
}

// Usage
const spec = new HighValueOrderSpecification(new Money(1000, "USD")).and(
  new PremiumCustomerOrderSpecification()
);

const orders = await repository.findAll();
const eligibleOrders = orders.filter((order) => spec.isSatisfiedBy(order));
```

## Best Practices

1. **Start with the Domain**: Model business concepts first
2. **Bounded Contexts**: Keep contexts small and focused
3. **Aggregate Boundaries**: Small aggregates for consistency
4. **Event Storming**: Collaborative domain exploration
5. **Ubiquitous Language**: Use domain terms in code

````

### patterns-expert.md

```markdown
---
name: patterns-expert
description: Design patterns expert for solving architectural problems
tools: Read, Write, Refactor
model: sonnet
---

# Design Patterns Expert

Expert in applying design patterns to solve architectural and code design problems.

## Creational Patterns

### Factory Method Pattern
```typescript
// Abstract Creator
abstract class PaymentProcessorFactory {
  abstract createProcessor(): PaymentProcessor;

  processPayment(amount: Money): PaymentResult {
    const processor = this.createProcessor();
    return processor.process(amount);
  }
}

// Concrete Creators
class StripePaymentFactory extends PaymentProcessorFactory {
  createProcessor(): PaymentProcessor {
    return new StripeProcessor(this.apiKey);
  }
}

class PayPalPaymentFactory extends PaymentProcessorFactory {
  createProcessor(): PaymentProcessor {
    return new PayPalProcessor(this.clientId, this.secret);
  }
}

// Usage with Configuration
class PaymentFactoryProvider {
  static getFactory(type: PaymentType): PaymentProcessorFactory {
    switch(type) {
      case PaymentType.STRIPE:
        return new StripePaymentFactory();
      case PaymentType.PAYPAL:
        return new PayPalPaymentFactory();
      default:
        throw new Error(`Unknown payment type: ${type}`);
    }
  }
}
````

### Builder Pattern

```typescript
// Complex object construction
class QueryBuilder {
  private selectClause: string[] = [];
  private fromClause: string;
  private whereClause: string[] = [];
  private orderByClause: string[] = [];
  private limitValue: number;

  select(...fields: string[]): this {
    this.selectClause.push(...fields);
    return this;
  }

  from(table: string): this {
    this.fromClause = table;
    return this;
  }

  where(condition: string): this {
    this.whereClause.push(condition);
    return this;
  }

  orderBy(field: string, direction: "ASC" | "DESC" = "ASC"): this {
    this.orderByClause.push(`${field} ${direction}`);
    return this;
  }

  limit(value: number): this {
    this.limitValue = value;
    return this;
  }

  build(): string {
    const query = [
      `SELECT ${this.selectClause.join(", ") || "*"}`,
      `FROM ${this.fromClause}`,
      this.whereClause.length ? `WHERE ${this.whereClause.join(" AND ")}` : "",
      this.orderByClause.length
        ? `ORDER BY ${this.orderByClause.join(", ")}`
        : "",
      this.limitValue ? `LIMIT ${this.limitValue}` : "",
    ]
      .filter(Boolean)
      .join(" ");

    return query;
  }
}

// Usage
const query = new QueryBuilder()
  .select("id", "name", "email")
  .from("users")
  .where('status = "active"')
  .where('created_at > "2024-01-01"')
  .orderBy("created_at", "DESC")
  .limit(10)
  .build();
```

## Structural Patterns

### Adapter Pattern

```typescript
// Legacy interface
interface LegacyPaymentGateway {
  makePayment(amount: number, currency: string): string;
}

// Modern interface
interface PaymentGateway {
  processPayment(payment: Payment): Promise<PaymentResult>;
}

// Adapter
class LegacyPaymentAdapter implements PaymentGateway {
  constructor(private legacyGateway: LegacyPaymentGateway) {}

  async processPayment(payment: Payment): Promise<PaymentResult> {
    try {
      const transactionId = this.legacyGateway.makePayment(
        payment.amount.value,
        payment.amount.currency
      );

      return {
        success: true,
        transactionId,
        amount: payment.amount,
      };
    } catch (error) {
      return {
        success: false,
        error: error.message,
      };
    }
  }
}
```

### Facade Pattern

```typescript
// Complex subsystem
class OrderSubsystem {
  createOrder(items: Item[]): Order {
    /* ... */
  }
  calculateTotal(order: Order): Money {
    /* ... */
  }
}

class PaymentSubsystem {
  processPayment(amount: Money): PaymentResult {
    /* ... */
  }
  refund(transactionId: string): RefundResult {
    /* ... */
  }
}

class ShippingSubsystem {
  calculateShipping(order: Order): Money {
    /* ... */
  }
  scheduleDelivery(order: Order): Delivery {
    /* ... */
  }
}

// Facade
class EcommerceFacade {
  constructor(
    private orderSystem: OrderSubsystem,
    private paymentSystem: PaymentSubsystem,
    private shippingSystem: ShippingSubsystem
  ) {}

  async placeOrder(
    items: Item[],
    paymentMethod: PaymentMethod
  ): Promise<OrderResult> {
    // Simplified interface for complex operations
    const order = this.orderSystem.createOrder(items);
    const subtotal = this.orderSystem.calculateTotal(order);
    const shipping = this.shippingSystem.calculateShipping(order);
    const total = subtotal.add(shipping);

    const payment = await this.paymentSystem.processPayment(total);
    if (!payment.success) {
      throw new Error("Payment failed");
    }

    const delivery = await this.shippingSystem.scheduleDelivery(order);

    return {
      order,
      payment,
      delivery,
      total,
    };
  }
}
```

## Behavioral Patterns

### Strategy Pattern

```typescript
// Strategy Interface
interface PricingStrategy {
  calculatePrice(basePrice: Money, quantity: number): Money;
}

// Concrete Strategies
class RegularPricing implements PricingStrategy {
  calculatePrice(basePrice: Money, quantity: number): Money {
    return basePrice.multiply(quantity);
  }
}

class BulkPricing implements PricingStrategy {
  constructor(private bulkQuantity: number, private discountPercent: number) {}

  calculatePrice(basePrice: Money, quantity: number): Money {
    const total = basePrice.multiply(quantity);

    if (quantity >= this.bulkQuantity) {
      return total.applyDiscount(this.discountPercent);
    }

    return total;
  }
}

class TieredPricing implements PricingStrategy {
  constructor(private tiers: Array<{ quantity: number; price: Money }>) {}

  calculatePrice(basePrice: Money, quantity: number): Money {
    const tier = this.tiers
      .sort((a, b) => b.quantity - a.quantity)
      .find((t) => quantity >= t.quantity);

    return tier ? tier.price.multiply(quantity) : basePrice.multiply(quantity);
  }
}

// Context
class Product {
  constructor(
    private name: string,
    private basePrice: Money,
    private pricingStrategy: PricingStrategy
  ) {}

  calculatePrice(quantity: number): Money {
    return this.pricingStrategy.calculatePrice(this.basePrice, quantity);
  }

  setPricingStrategy(strategy: PricingStrategy): void {
    this.pricingStrategy = strategy;
  }
}
```

### Observer Pattern

```typescript
// Subject
interface EventEmitter {
  on(event: string, handler: Function): void;
  off(event: string, handler: Function): void;
  emit(event: string, data: any): void;
}

class DomainEventEmitter implements EventEmitter {
  private handlers = new Map<string, Set<Function>>();

  on(event: string, handler: Function): void {
    if (!this.handlers.has(event)) {
      this.handlers.set(event, new Set());
    }
    this.handlers.get(event)!.add(handler);
  }

  off(event: string, handler: Function): void {
    this.handlers.get(event)?.delete(handler);
  }

  emit(event: string, data: any): void {
    const eventHandlers = this.handlers.get(event);
    if (eventHandlers) {
      eventHandlers.forEach((handler) => handler(data));
    }
  }
}

// Observer Usage
class InventoryService {
  constructor(private eventEmitter: EventEmitter) {
    this.eventEmitter.on("order.created", this.reserveInventory.bind(this));
    this.eventEmitter.on("order.cancelled", this.releaseInventory.bind(this));
  }

  private async reserveInventory(order: Order): Promise<void> {
    for (const item of order.items) {
      await this.decrementStock(item.productId, item.quantity);
    }
  }

  private async releaseInventory(order: Order): Promise<void> {
    for (const item of order.items) {
      await this.incrementStock(item.productId, item.quantity);
    }
  }
}
```

### Chain of Responsibility

```typescript
// Handler Interface
abstract class ValidationHandler {
  protected nextHandler: ValidationHandler | null = null;

  setNext(handler: ValidationHandler): ValidationHandler {
    this.nextHandler = handler;
    return handler;
  }

  async handle(request: Order): Promise<ValidationResult> {
    const result = await this.validate(request);

    if (!result.isValid || !this.nextHandler) {
      return result;
    }

    return this.nextHandler.handle(request);
  }

  protected abstract validate(request: Order): Promise<ValidationResult>;
}

// Concrete Handlers
class InventoryValidator extends ValidationHandler {
  protected async validate(order: Order): Promise<ValidationResult> {
    for (const item of order.items) {
      const available = await this.checkInventory(
        item.productId,
        item.quantity
      );
      if (!available) {
        return {
          isValid: false,
          error: `Insufficient inventory for product ${item.productId}`,
        };
      }
    }
    return { isValid: true };
  }
}

class PaymentValidator extends ValidationHandler {
  protected async validate(order: Order): Promise<ValidationResult> {
    const valid = await this.validatePaymentMethod(order.paymentMethod);
    if (!valid) {
      return {
        isValid: false,
        error: "Invalid payment method",
      };
    }
    return { isValid: true };
  }
}

class FraudValidator extends ValidationHandler {
  protected async validate(order: Order): Promise<ValidationResult> {
    const fraudScore = await this.calculateFraudScore(order);
    if (fraudScore > 0.7) {
      return {
        isValid: false,
        error: "Order flagged for fraud review",
      };
    }
    return { isValid: true };
  }
}

// Usage
const validationChain = new InventoryValidator();
validationChain.setNext(new PaymentValidator()).setNext(new FraudValidator());

const result = await validationChain.handle(order);
```

## Best Practices

1. **Don't Overuse**: Patterns add complexity
2. **Know When to Apply**: Each pattern solves specific problems
3. **Combine Patterns**: Many patterns work well together
4. **Refactor to Patterns**: Start simple, refactor when needed
5. **Document Pattern Usage**: Make intent clear

````

## Skills

### service-boundaries.md

```markdown
---
name: service-boundaries
description: Automatically detects and suggests service boundary improvements
allowed-tools: Read, Analyze
---

# Service Boundaries Skill

Automatically analyzes code to identify service boundaries and coupling issues.

## Detection Patterns

### High Cohesion Indicators
- Classes that frequently change together
- Methods that access the same data
- Related business concepts

### Low Coupling Indicators
- Minimal cross-service calls
- Well-defined interfaces
- Asynchronous communication

### Boundary Violations
- Direct database access across services
- Shared domain models
- Circular dependencies
- Chatty interfaces

## Analysis Triggers
- Creating new services
- Adding service dependencies
- Modifying service interfaces
- Database schema changes

## Suggestions
- Merge overly granular services
- Split services with multiple responsibilities
- Introduce anti-corruption layers
- Convert sync to async communication
````

### anti-patterns.md

````markdown
---
name: anti-patterns
description: Detects architectural anti-patterns and suggests fixes
allowed-tools: Read, Analyze, Suggest
---

# Anti-Patterns Detection Skill

## Common Anti-Patterns

### Distributed Monolith

**Detection**: Services that must deploy together
**Fix**: Decouple services, version APIs

### Chatty Services

**Detection**: >10 calls between services per request
**Fix**: Aggregate calls, introduce facade

### Shared Database

**Detection**: Multiple services accessing same tables
**Fix**: Database per service, event streaming

### God Service

**Detection**: Service with >20 endpoints
**Fix**: Split by domain boundaries

### Anemic Services

**Detection**: Services with only CRUD operations
**Fix**: Move business logic from orchestrator

### Big Ball of Mud

**Detection**: No clear architecture patterns
**Fix**: Introduce boundaries gradually

## Auto-Detection Rules

```yaml
rules:
  - name: circular_dependency
    condition: service A → B → C → A
    severity: critical

  - name: excessive_coupling
    condition: service depends on >5 other services
    severity: high

  - name: missing_abstraction
    condition: direct infrastructure access in domain
    severity: medium
```
````

````

### scalability-check.md

```markdown
---
name: scalability-check
description: Analyzes architecture for scalability issues
allowed-tools: Analyze, Report
---

# Scalability Analysis Skill

## Scalability Dimensions

### Horizontal Scaling
- Stateless services ✓
- Session management strategy
- Database connection pooling
- Cache distribution

### Vertical Scaling
- Resource utilization
- Memory leaks detection
- CPU bottlenecks
- I/O optimization

### Data Scaling
- Database sharding strategy
- Read replicas
- Caching layers
- CDN usage

## Performance Patterns
- Circuit breakers for fault tolerance
- Bulkheads for isolation
- Rate limiting for protection
- Backpressure for flow control

## Bottleneck Detection
1. Database N+1 queries
2. Synchronous cascade calls
3. Missing indexes
4. Inefficient algorithms
5. Memory leaks

## Recommendations
- Add caching where beneficial
- Implement async processing
- Use message queues for decoupling
- Apply database optimization
````

### coupling-analysis.md

````markdown
---
name: coupling-analysis
description: Measures and reports coupling between components
allowed-tools: Read, Analyze, Visualize
---

# Coupling Analysis Skill

## Coupling Types

### Afferent Coupling (Ca)

Components that depend on this component

### Efferent Coupling (Ce)

Components this component depends on

### Instability Metric

I = Ce / (Ca + Ce)

- I = 0: Maximally stable
- I = 1: Maximally unstable

## Coupling Levels

### Content Coupling (Worst)

Direct access to internal data

### Common Coupling

Shared global data

### Control Coupling

Passing control flags

### Data Coupling (Best)

Passing data only

## Analysis Output

```json
{
  "service": "order-service",
  "metrics": {
    "afferent": 3,
    "efferent": 5,
    "instability": 0.625
  },
  "dependencies": [
    {
      "service": "payment-service",
      "type": "data",
      "strength": "low"
    }
  ],
  "recommendations": [
    "Consider event-driven communication",
    "Introduce API gateway"
  ]
}
```
````

````

## MCP Server Configuration

```json
{
  "servers": [
    {
      "name": "architecture-analyzer",
      "description": "Analyzes codebase architecture",
      "command": "python",
      "args": ["./mcp-servers/arch_analyzer.py"],
      "env": {
        "ANALYSIS_DEPTH": "3"
      }
    },
    {
      "name": "diagram-generator",
      "description": "Generates architecture diagrams",
      "command": "node",
      "args": ["./mcp-servers/diagram-gen.js"]
    },
    {
      "name": "pattern-detector",
      "description": "Detects design patterns in code",
      "command": "go",
      "args": ["run", "./mcp-servers/pattern-detector.go"]
    }
  ]
}
````

## Hooks Configuration

```json
{
  "hooks": {
    "pre-service-create": {
      "enabled": true,
      "actions": [
        {
          "type": "skill",
          "name": "service-boundaries"
        }
      ]
    },
    "post-refactor": {
      "enabled": true,
      "actions": [
        {
          "type": "skill",
          "name": "anti-patterns"
        },
        {
          "type": "skill",
          "name": "coupling-analysis"
        }
      ]
    },
    "architecture-review": {
      "enabled": true,
      "schedule": "weekly",
      "actions": [
        {
          "type": "command",
          "name": "analyze",
          "args": ["all"]
        },
        {
          "type": "command",
          "name": "visualize",
          "args": ["c4", "context"]
        }
      ]
    }
  }
}
```

## Output Styles

### architecture-doc.md

```markdown
---
name: architecture-documentation
description: Comprehensive architecture documentation template
---

# System Architecture Document

## Executive Summary

{{SUMMARY}}

## Architecture Overview

{{ARCHITECTURE_TYPE}} architecture with {{PATTERN_LIST}}

## System Context

{{C4_CONTEXT_DIAGRAM}}

## Components

{{COMPONENT_LIST}}

## Data Flow

{{DATA_FLOW_DIAGRAM}}

## Technology Stack

{{TECH_STACK}}

## Deployment Architecture

{{DEPLOYMENT_DIAGRAM}}

## Security Architecture

{{SECURITY_MEASURES}}

## Performance Considerations

{{PERFORMANCE_METRICS}}

## Scalability Strategy

{{SCALABILITY_PLAN}}

## Decision Records

{{ADR_LINKS}}
```

### adr-template.md

```markdown
---
name: architecture-decision-record
description: ADR template for documenting architectural decisions
---

# ADR-{{NUMBER}}: {{TITLE}}

## Status

{{STATUS}} <!-- Proposed, Accepted, Deprecated, Superseded -->

## Context

{{PROBLEM_DESCRIPTION}}

## Decision

{{DECISION_MADE}}

## Consequences

### Positive

{{POSITIVE_OUTCOMES}}

### Negative

{{NEGATIVE_OUTCOMES}}

### Neutral

{{NEUTRAL_IMPACTS}}

## Alternatives Considered

{{ALTERNATIVES}}

## References

{{REFERENCE_LINKS}}
```

## Usage Examples

### Creating Microservices Architecture

```bash
# User command
/architect microservices new

# Plugin flow:
1. Analyze current codebase structure
2. Invoke microservices-architect agent
3. Agent identifies bounded contexts
4. Creates service structure:
   - API gateway
   - Service templates
   - Message broker setup
   - Service discovery
5. service-boundaries skill validates design
6. Generates architecture documentation
```

### Migrating Monolith to Microservices

```bash
# User command
/migrate monolith-to-microservices strangler

# Plugin flow:
1. Analyze monolithic application
2. Identify service boundaries
3. Create migration plan:
   - Phase 1: Extract authentication
   - Phase 2: Extract payment processing
   - Phase 3: Extract order management
4. Generate strangler fig proxy
5. Create gradual migration scripts
```

### Analyzing Architecture

```bash
# User command
/analyze all

# Plugin flow:
1. Scan codebase for patterns
2. Detect anti-patterns
3. Measure coupling metrics
4. Identify scalability issues
5. Generate comprehensive report
6. Create architecture diagrams
7. Provide improvement recommendations
```

## Success Metrics

- **Design Quality**: Coupling < 0.5, Cohesion > 0.7
- **Pattern Detection**: 95% accuracy in pattern identification
- **Migration Success**: Zero-downtime migrations
- **Documentation**: Auto-generated C4 diagrams
- **Anti-pattern Detection**: Catch 90% of common issues

## Future Enhancements

1. **AI-Powered Design**: ML-based architecture recommendations
2. **Cost Optimization**: Cloud cost analysis and optimization
3. **Compliance Checking**: GDPR, HIPAA, SOC2 validation
4. **Performance Prediction**: Load testing and capacity planning
5. **Automated Refactoring**: Safe architectural refactoring tools
