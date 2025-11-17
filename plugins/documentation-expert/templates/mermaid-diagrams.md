# Mermaid Diagram Examples and Templates

This file contains templates and examples for common Mermaid diagram types used in architecture documentation.

## Table of Contents

- [Flowchart](#flowchart)
- [Sequence Diagram](#sequence-diagram)
- [Class Diagram](#class-diagram)
- [State Diagram](#state-diagram)
- [Entity Relationship Diagram](#entity-relationship-diagram)
- [Gantt Chart](#gantt-chart)
- [Git Graph](#git-graph)
- [System Architecture](#system-architecture)

## Flowchart

### Simple Flowchart

```mermaid
graph TD
    A[Start] --> B{Decision}
    B -->|Yes| C[Action 1]
    B -->|No| D[Action 2]
    C --> E[End]
    D --> E
```

### Complex Flowchart with Subgraphs

```mermaid
graph TB
    subgraph "Client Layer"
        A[Web App]
        B[Mobile App]
    end

    subgraph "API Layer"
        C[API Gateway]
        D[Load Balancer]
    end

    subgraph "Service Layer"
        E[Auth Service]
        F[User Service]
        G[Order Service]
    end

    subgraph "Data Layer"
        H[(Database)]
        I[(Cache)]
    end

    A --> C
    B --> C
    C --> D
    D --> E
    D --> F
    D --> G
    E --> H
    F --> H
    G --> H
    F --> I
```

### Process Flow

```mermaid
graph LR
    A[Input] --> B[Validate]
    B -->|Valid| C[Process]
    B -->|Invalid| D[Error]
    C --> E[Transform]
    E --> F[Save]
    F --> G[Output]
    D --> H[Log Error]
```

## Sequence Diagram

### API Request Flow

```mermaid
sequenceDiagram
    participant Client
    participant Gateway
    participant Auth
    participant Service
    participant DB

    Client->>Gateway: POST /api/resource
    Gateway->>Auth: Validate token
    Auth-->>Gateway: Token valid
    Gateway->>Service: Process request
    Service->>DB: Query data
    DB-->>Service: Return data
    Service-->>Gateway: Response
    Gateway-->>Client: 200 OK
```

### Authentication Flow

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant Backend
    participant AuthService
    participant Database

    User->>Frontend: Enter credentials
    Frontend->>Backend: POST /auth/login
    Backend->>AuthService: Validate credentials
    AuthService->>Database: Query user
    Database-->>AuthService: User data
    AuthService->>AuthService: Verify password
    AuthService-->>Backend: JWT token
    Backend-->>Frontend: Token + user info
    Frontend->>Frontend: Store token
    Frontend-->>User: Login successful
```

### Error Handling Flow

```mermaid
sequenceDiagram
    participant Client
    participant API
    participant Service

    Client->>API: Invalid request
    API->>API: Validate
    API-->>Client: 400 Bad Request

    Client->>API: Valid request
    API->>Service: Process
    Service-->>API: Error
    API-->>Client: 500 Internal Error
```

## Class Diagram

### Object-Oriented Design

```mermaid
classDiagram
    class User {
        +String id
        +String email
        +String name
        +Date createdAt
        +login()
        +logout()
        +updateProfile()
    }

    class Order {
        +String id
        +String userId
        +Decimal total
        +String status
        +Date createdAt
        +create()
        +cancel()
        +complete()
    }

    class Product {
        +String id
        +String name
        +Decimal price
        +Int stock
        +updateStock()
        +getPrice()
    }

    User "1" --> "*" Order : places
    Order "*" --> "*" Product : contains
```

### Service Architecture

```mermaid
classDiagram
    class APIGateway {
        +routeRequest()
        +authenticate()
        +rateLimit()
    }

    class UserService {
        +getUser()
        +createUser()
        +updateUser()
        +deleteUser()
    }

    class OrderService {
        +createOrder()
        +getOrder()
        +updateOrder()
        +cancelOrder()
    }

    class Database {
        +query()
        +insert()
        +update()
        +delete()
    }

    APIGateway --> UserService
    APIGateway --> OrderService
    UserService --> Database
    OrderService --> Database
```

## State Diagram

### Order State Machine

```mermaid
stateDiagram-v2
    [*] --> Created
    Created --> Pending : submit
    Pending --> Processing : payment_received
    Pending --> Cancelled : cancel
    Processing --> Shipped : ship
    Processing --> Cancelled : cancel
    Shipped --> Delivered : deliver
    Delivered --> [*]
    Cancelled --> [*]
```

### User Authentication States

```mermaid
stateDiagram-v2
    [*] --> Anonymous
    Anonymous --> Authenticated : login
    Authenticated --> Anonymous : logout
    Authenticated --> Verified : verify_email
    Verified --> Anonymous : logout
```

## Entity Relationship Diagram

### E-Commerce Database

```mermaid
erDiagram
    USER ||--o{ ORDER : places
    USER {
        uuid id PK
        string email UK
        string name
        string password_hash
        timestamp created_at
        timestamp updated_at
    }

    ORDER ||--|{ ORDER_ITEM : contains
    ORDER {
        uuid id PK
        uuid user_id FK
        decimal total
        string status
        timestamp created_at
        timestamp updated_at
    }

    ORDER_ITEM }o--|| PRODUCT : references
    ORDER_ITEM {
        uuid id PK
        uuid order_id FK
        uuid product_id FK
        int quantity
        decimal price_at_time
    }

    PRODUCT ||--o{ REVIEW : has
    PRODUCT {
        uuid id PK
        string name
        string description
        decimal price
        int stock
        timestamp created_at
    }

    REVIEW }o--|| USER : writes
    REVIEW {
        uuid id PK
        uuid product_id FK
        uuid user_id FK
        int rating
        text comment
        timestamp created_at
    }
```

### Simple Relationships

```mermaid
erDiagram
    CUSTOMER ||--o{ ORDER : places
    ORDER ||--|{ LINE_ITEM : contains
    PRODUCT ||--o{ LINE_ITEM : ordered_in
```

## Gantt Chart

### Project Timeline

```mermaid
gantt
    title Project Implementation Timeline
    dateFormat  YYYY-MM-DD
    section Planning
    Requirements Analysis    :a1, 2024-01-01, 7d
    Design                   :a2, after a1, 5d
    section Development
    Backend API              :b1, after a2, 14d
    Frontend UI              :b2, after a2, 14d
    Integration              :b3, after b1, 7d
    section Testing
    Unit Testing             :c1, after b1, 3d
    Integration Testing      :c2, after b3, 5d
    User Acceptance Testing  :c3, after c2, 3d
    section Deployment
    Production Deployment    :d1, after c3, 2d
```

## Git Graph

### Branch Strategy

```mermaid
gitGraph
    commit
    commit
    branch develop
    checkout develop
    commit
    commit
    branch feature/login
    checkout feature/login
    commit
    commit
    checkout develop
    merge feature/login
    checkout main
    merge develop tag: "v1.0"
    checkout develop
    branch feature/api
    checkout feature/api
    commit
    checkout develop
    merge feature/api
    checkout main
    merge develop tag: "v1.1"
```

## System Architecture

### Microservices Architecture

```mermaid
graph TB
    subgraph "Client Layer"
        WebApp[Web Application]
        MobileApp[Mobile App]
    end

    subgraph "Gateway Layer"
        Gateway[API Gateway]
        LB[Load Balancer]
    end

    subgraph "Service Layer"
        Auth[Auth Service]
        Users[User Service]
        Orders[Order Service]
        Products[Product Service]
        Notifications[Notification Service]
    end

    subgraph "Message Layer"
        Queue[Message Queue]
        EventBus[Event Bus]
    end

    subgraph "Data Layer"
        UserDB[(User DB)]
        OrderDB[(Order DB)]
        ProductDB[(Product DB)]
        Cache[(Redis Cache)]
    end

    subgraph "External Services"
        Payment[Payment Gateway]
        Email[Email Service]
    end

    WebApp --> Gateway
    MobileApp --> Gateway
    Gateway --> LB
    LB --> Auth
    LB --> Users
    LB --> Orders
    LB --> Products

    Auth --> UserDB
    Users --> UserDB
    Users --> Cache
    Orders --> OrderDB
    Orders --> Queue
    Products --> ProductDB

    Queue --> Notifications
    Orders --> Payment
    Notifications --> Email
    Notifications --> EventBus
```

### Deployment Architecture

```mermaid
graph TB
    subgraph "Production Environment"
        subgraph "Kubernetes Cluster"
            Ingress[Ingress Controller]

            subgraph "Frontend"
                Web1[Web Pod 1]
                Web2[Web Pod 2]
            end

            subgraph "Backend"
                API1[API Pod 1]
                API2[API Pod 2]
                API3[API Pod 3]
            end

            subgraph "Workers"
                Worker1[Worker Pod 1]
                Worker2[Worker Pod 2]
            end
        end

        LB[Load Balancer]
        DB[(PostgreSQL Primary)]
        DBReplica[(PostgreSQL Replica)]
        Redis[(Redis Cluster)]
        Queue[RabbitMQ]
    end

    Internet[Internet] --> LB
    LB --> Ingress
    Ingress --> Web1
    Ingress --> Web2
    Web1 --> API1
    Web2 --> API2
    API1 --> DB
    API2 --> DB
    API3 --> DB
    DB --> DBReplica
    API1 --> Redis
    API2 --> Redis
    API1 --> Queue
    Worker1 --> Queue
    Worker2 --> Queue
```

## Tips for Creating Diagrams

### Best Practices

1. **Keep it Simple**: Don't overcomplicate diagrams
2. **Use Subgraphs**: Group related components
3. **Consistent Naming**: Use clear, descriptive names
4. **Direction**: Choose appropriate direction (TB, LR, etc.)
5. **Colors**: Use colors sparingly for emphasis
6. **Labels**: Add labels to clarify relationships

### Common Patterns

**For APIs:**
- Use sequence diagrams for request flows
- Use flowcharts for decision logic
- Use class diagrams for data models

**For Architecture:**
- Use component diagrams for system overview
- Use deployment diagrams for infrastructure
- Use sequence diagrams for interactions

**For Data:**
- Use ER diagrams for database schema
- Use state diagrams for entity lifecycles
- Use flowcharts for data transformations

### Resources

- [Mermaid Documentation](https://mermaid.js.org/)
- [Mermaid Live Editor](https://mermaid.live/)
- [Mermaid Chart](https://www.mermaidchart.com/)
