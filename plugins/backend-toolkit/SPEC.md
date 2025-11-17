# Backend Plugin Specification

## Plugin Overview

**Name**: `backend-plugin`  
**Version**: `1.0.0`  
**Description**: Comprehensive backend development toolkit supporting REST, GraphQL, gRPC, WebSocket, and message brokers across Node.js, Go, and Python.

## Core Capabilities

### Supported Languages

- **Node.js/TypeScript**: Express, Fastify, NestJS
- **Go**: Gin, Fiber, Echo, native net/http
- **Python**: FastAPI, Django, Flask

### Supported Protocols

- **REST API**: OpenAPI/Swagger spec generation
- **GraphQL**: Schema-first development, resolvers
- **gRPC**: Protocol buffer definitions, service generation
- **WebSocket**: Real-time bidirectional communication
- **Message Brokers**: NATS, RabbitMQ, Redis Pub/Sub, Kafka

## Plugin Structure

```
backend-plugin/
├── manifest.json
├── commands/
│   ├── api.md              # Main API creation command
│   ├── server.md           # Server management
│   ├── broker.md           # Message broker setup
│   └── test-api.md         # API testing command
├── agents/
│   ├── nodejs-specialist.md
│   ├── golang-specialist.md
│   ├── python-specialist.md
│   ├── api-architect.md
│   ├── grpc-expert.md
│   ├── graphql-expert.md
│   └── broker-specialist.md
├── skills/
│   ├── api-best-practices.md
│   ├── error-handling.md
│   ├── auth-patterns.md
│   └── validation-rules.md
├── mcp-servers/
│   └── config.json
└── output-styles/
    ├── api-documentation.md
    └── openapi-spec.md
```

## Manifest Configuration

```json
{
  "name": "backend-plugin",
  "version": "1.0.0",
  "description": "Comprehensive backend development toolkit for REST, GraphQL, gRPC, WebSocket, and message brokers",
  "author": {
    "name": "Claude Code Team",
    "email": "team@claude.code",
    "url": "https://github.com/claude-code/backend-plugin"
  },
  "keywords": [
    "backend",
    "api",
    "rest",
    "graphql",
    "grpc",
    "websocket",
    "nodejs",
    "golang",
    "python",
    "fastapi",
    "express",
    "gin",
    "nats",
    "rabbitmq",
    "redis",
    "kafka"
  ],
  "commands": [
    "./commands/api.md",
    "./commands/server.md",
    "./commands/broker.md",
    "./commands/test-api.md"
  ],
  "agents": "./agents/",
  "skills": "./skills/",
  "hooks": "./hooks/hooks.json",
  "mcpServers": "./mcp-servers/config.json",
  "outputStyles": "./output-styles/"
}
```

## Commands

### `/api` Command

```markdown
---
description: Create and manage API endpoints
allowed-tools: Bash, Read, Write, Execute
---

# API Command

Create API endpoints with automatic language detection and best practices.

## Usage

`/api [action] [protocol] [resource] [options]`

## Actions

- `create` - Create new endpoint
- `list` - List existing endpoints
- `test` - Test endpoint
- `document` - Generate documentation

## Protocols

- `rest` - RESTful API
- `graphql` - GraphQL resolver
- `grpc` - gRPC service
- `websocket` - WebSocket handler

## Implementation

!`
#!/bin/bash

ACTION=$1
PROTOCOL=$2
RESOURCE=$3
OPTIONS=$4

# Detect project language

detect_language() {
if [ -f "package.json" ]; then
echo "nodejs"
elif [ -f "go.mod" ]; then
echo "golang"
elif [ -f "pyproject.toml" ] || [ -f "requirements.txt" ]; then
echo "python"
else
echo "unknown"
fi
}

LANGUAGE=$(detect_language)

case $ACTION in
create)
echo "Creating $PROTOCOL API for $RESOURCE in $LANGUAGE" # Invoke appropriate specialist agent
case $LANGUAGE in
nodejs)
echo "Invoking Node.js specialist for $PROTOCOL endpoint"
;;
golang)
echo "Invoking Go specialist for $PROTOCOL endpoint"
;;
python)
echo "Invoking Python specialist for $PROTOCOL endpoint"
;;
esac
;;
list)
echo "Listing API endpoints..."
find . -type f -name "_.route._" -o -name "_.controller._" -o -name "_.handler._" | head -20
;;
test)
echo "Testing $RESOURCE endpoint..."
;;
document)
echo "Generating API documentation..."
;;
\*)
echo "Usage: /api [create|list|test|document] [protocol] [resource]"
exit 1
;;
esac
`
```

### `/server` Command

```markdown
---
description: Manage backend servers
allowed-tools: Bash, Read, Write
---

# Server Command

Start, stop, and manage backend servers.

## Usage

`/server [action] [port]`

## Actions

- `start` - Start development server
- `stop` - Stop server
- `restart` - Restart server
- `status` - Check server status

!`
#!/bin/bash

ACTION=$1
PORT=${2:-3000}

case $ACTION in
start)
if [ -f "package.json" ]; then
npm run dev || npm start
elif [ -f "go.mod" ]; then
go run . &
elif [ -f "manage.py" ]; then
python manage.py runserver $PORT
elif [ -f "main.py" ]; then
uvicorn main:app --reload --port $PORT
fi
;;
stop)
pkill -f "node|go run|python|uvicorn"
;;
status)
ps aux | grep -E "node|go run|python|uvicorn" | grep -v grep
;;
esac
`
```

### `/broker` Command

```markdown
---
description: Setup and configure message brokers
allowed-tools: Bash, Write, Read
---

# Message Broker Command

Configure NATS, RabbitMQ, Redis Pub/Sub, or Kafka.

## Usage

`/broker [type] [action]`

## Supported Brokers

- `nats` - NATS messaging
- `rabbitmq` - RabbitMQ
- `redis` - Redis Pub/Sub
- `kafka` - Apache Kafka

!`
#!/bin/bash

BROKER=$1
ACTION=$2

case $BROKER in
nats)
echo "Setting up NATS connection..." # Invoke broker-specialist agent with NATS context
;;
rabbitmq)
echo "Configuring RabbitMQ..." # Invoke broker-specialist agent with RabbitMQ context
;;
redis)
echo "Setting up Redis Pub/Sub..." # Invoke broker-specialist agent with Redis context
;;
kafka)
echo "Configuring Kafka..." # Invoke broker-specialist agent with Kafka context
;;
esac
`
```

## Agents

### nodejs-specialist.md

````markdown
---
name: nodejs-specialist
description: Node.js and TypeScript backend development expert
tools: Read, Write, Execute, Npm
model: sonnet
---

# Node.js Backend Specialist

Expert in Node.js backend development with TypeScript, focusing on Express.

## Core Expertise

### REST API with Express/TypeScript

```typescript
import express, { Request, Response, NextFunction } from "express";
import { body, validationResult } from "express-validator";

interface User {
  id: string;
  name: string;
  email: string;
}

class UserController {
  async create(req: Request, res: Response, next: NextFunction) {
    try {
      const errors = validationResult(req);
      if (!errors.isEmpty()) {
        return res.status(400).json({ errors: errors.array() });
      }

      const user = await userService.create(req.body);
      res.status(201).json(user);
    } catch (error) {
      next(error);
    }
  }
}

// Route setup
const router = express.Router();
router.post(
  "/users",
  body("email").isEmail(),
  body("name").notEmpty(),
  userController.create
);
```
````

### GraphQL with Apollo Server

```typescript
import { ApolloServer, gql } from "apollo-server-express";

const typeDefs = gql`
  type User {
    id: ID!
    name: String!
    email: String!
  }

  type Query {
    users: [User!]!
    user(id: ID!): User
  }

  type Mutation {
    createUser(input: CreateUserInput!): User!
  }

  input CreateUserInput {
    name: String!
    email: String!
  }
`;

const resolvers = {
  Query: {
    users: () => userService.findAll(),
    user: (_, { id }) => userService.findById(id),
  },
  Mutation: {
    createUser: (_, { input }) => userService.create(input),
  },
};
```

### WebSocket with ws

```typescript
import WebSocket from "ws";

const ws = new WebSocket("ws://www.host.com/path");

ws.on("error", console.error);

ws.on("open", function open() {
  ws.send("something");
});

ws.on("message", function message(data) {
  console.log("received: %s", data);
});
```

### Message Broker Integration

```typescript
// NATS
import { connect, StringCodec } from "nats";

const nc = await connect({ servers: "localhost:4222" });
const sc = StringCodec();

// Publisher
nc.publish("user.created", sc.encode(JSON.stringify(user)));

// Subscriber
const sub = nc.subscribe("user.created");
for await (const msg of sub) {
  const user = JSON.parse(sc.decode(msg.data));
  console.log("User created:", user);
}
```

## Best Practices

1. Always use TypeScript with strict mode
2. Implement proper error handling middleware
3. Use validation libraries (Joi, express-validator)
4. Implement rate limiting and security headers
5. Use environment variables for configuration
6. Structure code with clean architecture (controllers, services, repositories)

````

### golang-specialist.md

```markdown
---
name: golang-specialist
description: Go backend development expert specializing in high-performance APIs
tools: Read, Write, Execute, Go
model: sonnet
---

# Go Backend Specialist

Expert in Go backend development, specializing in Gin, Fiber, Echo, and native net/http.

## Core Expertise

### REST API with Gin
```go
package main

import (
    "net/http"
    "github.com/gin-gonic/gin"
    "github.com/go-playground/validator/v10"
)

type User struct {
    ID    string `json:"id"`
    Name  string `json:"name" binding:"required"`
    Email string `json:"email" binding:"required,email"`
}

type UserHandler struct {
    service *UserService
}

func (h *UserHandler) Create(c *gin.Context) {
    var user User
    if err := c.ShouldBindJSON(&user); err != nil {
        c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
        return
    }

    created, err := h.service.Create(&user)
    if err != nil {
        c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
        return
    }

    c.JSON(http.StatusCreated, created)
}

func setupRouter() *gin.Engine {
    r := gin.Default()

    // Middleware
    r.Use(gin.Logger())
    r.Use(gin.Recovery())
    r.Use(corsMiddleware())

    // Routes
    api := r.Group("/api/v1")
    {
        api.POST("/users", userHandler.Create)
        api.GET("/users/:id", userHandler.Get)
        api.PUT("/users/:id", userHandler.Update)
        api.DELETE("/users/:id", userHandler.Delete)
    }

    return r
}
````

### gRPC Service

```go
package main

import (
    "context"
    "google.golang.org/grpc"
    pb "myapp/proto"
)

type userServer struct {
    pb.UnimplementedUserServiceServer
    service *UserService
}

func (s *userServer) CreateUser(ctx context.Context, req *pb.CreateUserRequest) (*pb.User, error) {
    user := &User{
        Name:  req.Name,
        Email: req.Email,
    }

    created, err := s.service.Create(user)
    if err != nil {
        return nil, status.Error(codes.Internal, err.Error())
    }

    return &pb.User{
        Id:    created.ID,
        Name:  created.Name,
        Email: created.Email,
    }, nil
}

// Proto file
syntax = "proto3";
package user;

service UserService {
    rpc CreateUser(CreateUserRequest) returns (User);
    rpc GetUser(GetUserRequest) returns (User);
}

message User {
    string id = 1;
    string name = 2;
    string email = 3;
}
```

### WebSocket with Gorilla

```go
import (
    "github.com/gorilla/websocket"
)

var upgrader = websocket.Upgrader{
    CheckOrigin: func(r *http.Request) bool { return true },
}

type Hub struct {
    clients    map[*Client]bool
    broadcast  chan []byte
    register   chan *Client
    unregister chan *Client
}

func handleWebSocket(hub *Hub, w http.ResponseWriter, r *http.Request) {
    conn, err := upgrader.Upgrade(w, r, nil)
    if err != nil {
        return
    }

    client := &Client{hub: hub, conn: conn, send: make(chan []byte, 256)}
    client.hub.register <- client

    go client.writePump()
    go client.readPump()
}
```

### Message Broker Integration

```go
// NATS
import "github.com/nats-io/nats.go"

nc, _ := nats.Connect(nats.DefaultURL)
defer nc.Close()

// Publish
nc.Publish("user.created", userData)

// Subscribe
nc.Subscribe("user.created", func(m *nats.Msg) {
    log.Printf("Received: %s", string(m.Data))
})

// RabbitMQ
import "github.com/streadway/amqp"

conn, _ := amqp.Dial("amqp://guest:guest@localhost:5672/")
ch, _ := conn.Channel()

q, _ := ch.QueueDeclare("tasks", false, false, false, false, nil)
ch.Publish("", q.Name, false, false, amqp.Publishing{
    ContentType: "application/json",
    Body:        []byte(message),
})
```

## Best Practices

1. Use proper error handling (don't ignore errors)
2. Implement context for cancellation and timeouts
3. Use interfaces for dependency injection
4. Proper goroutine management
5. Use structured logging (zerolog, zap)
6. Implement graceful shutdown

````

### python-specialist.md

```markdown
---
name: python-specialist
description: Python backend development expert with FastAPI, Django, and async programming
tools: Read, Write, Execute, Pip
model: sonnet
---

# Python Backend Specialist

Expert in Python backend development with FastAPI, Django, Flask, and async programming.

## Core Expertise

### FastAPI REST API
```python
from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel, EmailStr, validator
from typing import List, Optional
import asyncio
from datetime import datetime

app = FastAPI(title="User API", version="1.0.0")

# Models
class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        return v

class User(UserBase):
    id: str
    created_at: datetime

    class Config:
        orm_mode = True

# Dependency injection
async def get_db():
    async with AsyncSession() as session:
        yield session

# Routes
@app.post("/users", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(
    user: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    db_user = await user_service.create(db, user)
    return db_user

@app.get("/users/{user_id}", response_model=User)
async def get_user(
    user_id: str,
    db: AsyncSession = Depends(get_db)
):
    user = await user_service.get(db, user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    return user

# Middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
````

### GraphQL with Strawberry

```python
import strawberry
from typing import List, Optional

@strawberry.type
class User:
    id: strawberry.ID
    name: str
    email: str
    posts: List["Post"]

@strawberry.type
class Post:
    id: strawberry.ID
    title: str
    content: str
    author: User

@strawberry.type
class Query:
    @strawberry.field
    async def users(self) -> List[User]:
        return await user_service.get_all()

    @strawberry.field
    async def user(self, id: strawberry.ID) -> Optional[User]:
        return await user_service.get_by_id(id)

@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_user(
        self,
        name: str,
        email: str
    ) -> User:
        return await user_service.create(name=name, email=email)

schema = strawberry.Schema(query=Query, mutation=Mutation)
```

### WebSocket with FastAPI

```python
from fastapi import WebSocket, WebSocketDisconnect
from typing import List

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    client_id: str
):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Client {client_id}: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client {client_id} left")
```

### Message Broker Integration

```python
# NATS
import nats
from nats.aio.client import Client as NATS

nc = await nats.connect("localhost:4222")

# Publish
await nc.publish("user.created", json.dumps(user_data).encode())

# Subscribe
async def message_handler(msg):
    subject = msg.subject
    data = json.loads(msg.data.decode())
    print(f"Received on {subject}: {data}")

await nc.subscribe("user.*", cb=message_handler)

# Redis Pub/Sub
import aioredis

redis = await aioredis.create_redis_pool('redis://localhost')

# Publish
await redis.publish('channel:user', json.dumps(user_data))

# Subscribe
channel = (await redis.subscribe('channel:user'))[0]
while await channel.wait_message():
    msg = await channel.get_json()
    print(f"Received: {msg}")

# Kafka with aiokafka
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer

producer = AIOKafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode()
)
await producer.start()
await producer.send('user-events', {'event': 'created', 'user': user_data})
```

## Best Practices

1. Use type hints everywhere
2. Implement async/await for I/O operations
3. Use Pydantic for data validation
4. Implement proper error handling
5. Use environment variables with python-dotenv
6. Structure with clean architecture
7. Use SQLAlchemy with async support

````

### api-architect.md

```markdown
---
name: api-architect
description: API design expert for REST, GraphQL, and gRPC architecture
tools: Read, Write, Analyze
model: opus
---

# API Architect

Expert in API design patterns, versioning, documentation, and best practices across all protocols.

## API Design Principles

### RESTful API Design
```yaml
# OpenAPI 3.0 Specification
openapi: 3.0.0
info:
  title: User Management API
  version: 1.0.0

paths:
  /api/v1/users:
    get:
      summary: List users
      parameters:
        - in: query
          name: page
          schema:
            type: integer
            default: 1
        - in: query
          name: limit
          schema:
            type: integer
            default: 20
      responses:
        200:
          description: Success
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    type: array
                    items:
                      $ref: '#/components/schemas/User'
                  pagination:
                    $ref: '#/components/schemas/Pagination'
````

### API Versioning Strategies

1. **URI Versioning**: `/api/v1/resource`
2. **Header Versioning**: `Accept: application/vnd.api+json;version=1`
3. **Query Parameter**: `/api/resource?version=1`

### Error Handling Standards

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Validation failed",
    "details": [
      {
        "field": "email",
        "message": "Invalid email format"
      }
    ],
    "timestamp": "2024-01-01T00:00:00Z",
    "path": "/api/v1/users",
    "request_id": "550e8400-e29b-41d4-a716-446655440000"
  }
}
```

### Authentication Patterns

- **JWT**: Stateless authentication
- **OAuth 2.0**: Third-party integration
- **API Keys**: Service-to-service
- **mTLS**: High-security environments

### Rate Limiting

```http
HTTP/1.1 429 Too Many Requests
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1640995200
Retry-After: 3600
```

## Protocol Selection Guide

- **REST**: CRUD operations, public APIs
- **GraphQL**: Complex queries, mobile apps
- **gRPC**: Microservices, high performance
- **WebSocket**: Real-time updates, chat

````

### broker-specialist.md

```markdown
---
name: broker-specialist
description: Message broker integration expert for NATS, RabbitMQ, Redis, and Kafka
tools: Read, Write, Configure
model: sonnet
---

# Message Broker Specialist

Expert in event-driven architecture and message broker integration.

## Broker Comparison

| Feature | NATS | RabbitMQ | Redis Pub/Sub | Kafka |
|---------|------|----------|---------------|-------|
| Throughput | Very High | High | High | Very High |
| Persistence | Optional | Yes | Limited | Yes |
| Ordering | Yes | Yes | No | Yes |
| Replay | JetStream | No | No | Yes |
| Complexity | Low | Medium | Low | High |

## Integration Patterns

### Pub/Sub Pattern
````

Publisher -> Topic/Channel -> Subscribers

```

### Request/Reply Pattern
```

Client -> Request Queue -> Server
<- Reply Queue <-

```

### Work Queue Pattern
```

Producer -> Queue -> Worker 1
-> Worker 2
-> Worker 3

````

## Implementation Examples

### NATS Setup
```yaml
# Basic pub/sub
nats:
  url: nats://localhost:4222
  subjects:
    - user.created
    - order.placed
    - payment.processed

# JetStream for persistence
jetstream:
  streams:
    - name: EVENTS
      subjects: ["events.>"]
      retention: limits
      max_age: 7d
````

### RabbitMQ Configuration

```yaml
rabbitmq:
  exchanges:
    - name: user-events
      type: topic
      durable: true
  queues:
    - name: email-notifications
      durable: true
      bindings:
        - exchange: user-events
          routing_key: user.created
```

### Kafka Topics

```yaml
kafka:
  brokers: ["localhost:9092"]
  topics:
    - name: user-events
      partitions: 3
      replication: 2
      retention: 168h
```

## Best Practices

1. Implement idempotent consumers
2. Use dead letter queues
3. Monitor queue depths
4. Implement circuit breakers
5. Use schemas for messages

````

## Skills

### api-best-practices.md

```markdown
---
name: api-best-practices
description: Automatically enforces API design best practices
allowed-tools: Read, Analyze
---

# API Best Practices Skill

This skill automatically activates when working on API endpoints.

## Automatic Checks

### REST API
✅ Proper HTTP methods (GET, POST, PUT, DELETE, PATCH)
✅ Consistent naming (plural nouns for collections)
✅ Status codes (200, 201, 204, 400, 401, 404, 500)
✅ Pagination for lists
✅ Filtering and sorting support
✅ HATEOAS links where appropriate

### Security
✅ Authentication implemented
✅ Authorization checks
✅ Input validation
✅ SQL injection prevention
✅ Rate limiting
✅ CORS configuration

### Performance
✅ Database query optimization (N+1 prevention)
✅ Caching headers
✅ Response compression
✅ Connection pooling
✅ Async operations

### Documentation
✅ OpenAPI/Swagger spec
✅ Request/response examples
✅ Error code documentation
✅ Authentication documentation
````

### error-handling.md

```markdown
---
name: error-handling
description: Ensures consistent error handling across all endpoints
allowed-tools: Read, Analyze, Suggest
---

# Error Handling Skill

Automatically reviews and improves error handling.

## Pattern Detection

### Global Error Handler

Ensures centralized error handling middleware exists.

### Error Categories

- **Validation Errors** (400)
- **Authentication Errors** (401)
- **Authorization Errors** (403)
- **Not Found Errors** (404)
- **Conflict Errors** (409)
- **Server Errors** (500)

## Suggestions

- Add try/catch blocks
- Implement error logging
- Sanitize error messages
- Add correlation IDs
- Implement retry logic
```

### auth-patterns.md

```markdown
---
name: auth-patterns
description: Implements authentication and authorization patterns
allowed-tools: Read, Write, Suggest
---

# Authentication Patterns Skill

## JWT Implementation

- Token generation
- Token validation
- Refresh token rotation
- Token blacklisting

## Session Management

- Session storage
- Session expiry
- Concurrent session limits

## OAuth 2.0

- Authorization code flow
- Client credentials flow
- PKCE implementation

## Security Headers

- CORS configuration
- CSP headers
- Rate limiting headers
```

## MCP Server Configuration

```json
{
  "servers": [
    {
      "name": "api-testing",
      "description": "API testing and mocking server",
      "command": "node",
      "args": ["./mcp-servers/api-testing.js"],
      "env": {
        "PORT": "4000"
      }
    },
    {
      "name": "broker-monitor",
      "description": "Message broker monitoring",
      "command": "node",
      "args": ["./mcp-servers/broker-monitor.js"]
    },
    {
      "name": "openapi-generator",
      "description": "OpenAPI spec generation",
      "command": "python",
      "args": ["./mcp-servers/openapi_generator.py"]
    }
  ]
}
```

## Hooks Configuration

```json
{
  "hooks": {
    "pre-api-create": {
      "enabled": true,
      "actions": [
        {
          "type": "skill",
          "name": "api-best-practices"
        }
      ]
    },
    "post-api-create": {
      "enabled": true,
      "actions": [
        {
          "type": "command",
          "name": "test-api",
          "args": ["--endpoint", "$ENDPOINT"]
        }
      ]
    },
    "file-save": {
      "enabled": true,
      "patterns": ["*.controller.*", "*.handler.*", "*.route.*"],
      "actions": [
        {
          "type": "skill",
          "name": "error-handling"
        },
        {
          "type": "skill",
          "name": "auth-patterns"
        }
      ]
    }
  }
}
```

## Output Styles

### api-documentation.md

````markdown
---
name: api-documentation
description: API documentation format
---

# API Documentation Template

## Endpoint: {{METHOD}} {{PATH}}

### Description

{{DESCRIPTION}}

### Authentication

{{AUTH_TYPE}}

### Request

```{{LANGUAGE}}
{{REQUEST_EXAMPLE}}
```
````

### Response

```json
{{RESPONSE_EXAMPLE}}
```

### Error Codes

| Code | Description |
| ---- | ----------- |

{{ERROR_CODES}}

### Rate Limiting

{{RATE_LIMIT_INFO}}

````

## Usage Examples

### Creating a REST API Endpoint

```bash
# User command
/api create rest users

# Plugin flow:
1. Command detects Node.js project
2. Invokes nodejs-specialist agent
3. Agent creates Express router with:
   - CRUD endpoints
   - Validation middleware
   - Error handling
   - TypeScript types
4. api-best-practices skill reviews
5. Generates OpenAPI documentation
````

### Setting up Message Broker

```bash
# User command
/broker nats setup

# Plugin flow:
1. Command invokes broker-specialist
2. Agent creates NATS connection module
3. Sets up publish/subscribe helpers
4. Creates example consumers
5. Configures reconnection logic
```

### GraphQL Schema Creation

```bash
# User command
/api create graphql schema

# Plugin flow:
1. Command detects Python project
2. Invokes python-specialist agent
3. Agent creates Strawberry schema
4. Sets up resolvers
5. Configures GraphQL playground
```

## Testing Strategy

The plugin includes comprehensive testing support:

1. **Unit Tests**: For individual endpoints
2. **Integration Tests**: For API workflows
3. **Contract Tests**: For API contracts
4. **Load Tests**: For performance validation

## Performance Considerations

1. **Language Detection Caching**: Cache project language detection
2. **Template Reuse**: Reuse code templates for common patterns
3. **Lazy Agent Loading**: Load agents only when needed
4. **MCP Server Pooling**: Maintain connection pools for MCP servers

## Success Metrics

- **Time to Endpoint**: < 30 seconds to create working endpoint
- **Code Quality**: Generated code passes linting
- **Test Coverage**: Generated tests cover happy path and errors
- **Documentation**: Auto-generated docs for every endpoint

## Dependencies

### External Tools Required

- Language runtimes (Node.js, Go, Python)
- Package managers (npm, go mod, pip)
- Optional: Docker for message brokers

### Recommended VS Code Extensions

- REST Client
- GraphQL
- Protocol Buffer Editor

## Future Enhancements

1. **Database Integration**: Auto-generate ORM models
2. **API Gateway Support**: Kong, Traefik integration
3. **Service Mesh**: Istio, Linkerd configuration
4. **API Versioning**: Automated version management
5. **Contract Testing**: Pact integration
