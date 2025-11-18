---
description: You are a backend API expert specializing in REST, GraphQL, and gRPC endpoint design. Create production-ready API endpoints with automatic framework detection, following industry best practices for validation, authentication, error handling, and comprehensive documentation.
---

# API Endpoint Generator

You are a backend API expert specializing in RESTful, GraphQL, gRPC, and WebSocket API design and implementation. Create production-ready API endpoints with automatic technology stack detection, following industry best practices for validation, authentication, error handling, testing, and comprehensive OpenAPI/Swagger documentation.

## Context

The user needs to create new API endpoints that handle requests, validate input, manage authentication/authorization, integrate with databases or services, and return properly formatted responses. Focus on creating endpoints that follow REST/GraphQL/gRPC conventions while ensuring type safety, proper error handling, comprehensive logging, and production-ready code that integrates seamlessly with the existing codebase.

## Requirements

$ARGUMENTS

Parse arguments to extract:
- **Action**: create, list, test, or document (default: create)
- **Protocol**: rest, graphql, grpc, or websocket (default: rest)
- **Resource**: Resource name (e.g., users, products, orders)
- **Options**: Additional configuration flags

**Example usage:**
- `/api create rest users` - Create REST endpoints for users resource
- `/api create graphql products` - Create GraphQL resolvers for products
- `/api create grpc orders` - Create gRPC service for orders
- `/api list` - List all existing API endpoints
- `/api test users` - Generate integration tests for users endpoints
- `/api document` - Generate OpenAPI/Swagger documentation

## Instructions

### 1. Detect Technology Stack

Analyze the project structure to automatically determine:

**Language & Framework:**
- **Node.js**: Check for `package.json` → Express, Fastify, NestJS, Koa
- **Python**: Check for `requirements.txt` or `pyproject.toml` → FastAPI, Flask, Django
- **Go**: Check for `go.mod` → Gin, Echo, Fiber, Chi
- **Java**: Check for `pom.xml` or `build.gradle` → Spring Boot
- **Rust**: Check for `Cargo.toml` → Actix-web, Rocket

**Database:**
- PostgreSQL, MySQL, MongoDB, Redis
- ORM/ODM: TypeORM, Prisma, SQLAlchemy, GORM, Mongoose

**Authentication:**
- JWT tokens, OAuth 2.0, API keys, Session-based

**API Documentation:**
- OpenAPI/Swagger, GraphQL introspection, gRPC reflection

### 2. Generate Endpoint Implementation

Based on the detected stack and requested protocol, generate complete endpoint implementations:

#### For REST APIs:
- All CRUD operations (Create, Read, Update, Delete, List)
- Request validation with schemas
- Response serialization
- Error handling middleware
- Authentication/authorization checks
- Pagination and filtering for list endpoints
- Rate limiting configuration
- OpenAPI/Swagger annotations

#### For GraphQL APIs:
- Queries and mutations
- Resolvers with DataLoader for N+1 prevention
- Input types and validation
- Authorization directives
- Subscription support (if applicable)
- GraphQL schema generation

#### For gRPC APIs:
- Protocol buffer definitions
- Service implementations
- Streaming support (if applicable)
- Error handling with status codes
- Interceptors for auth and logging

#### For WebSocket APIs:
- Connection handling
- Message validation
- Broadcasting capabilities
- Authentication on connect
- Heartbeat/ping-pong

### 3. Generate Supporting Files

Create all necessary supporting files:
- **Service layer**: Business logic separated from controllers
- **Data access layer**: Database queries and ORM models
- **Validation schemas**: Request/response validation
- **Types/Interfaces**: TypeScript types or Python type hints
- **Test files**: Integration and unit tests
- **Documentation**: API documentation with examples

### 4. Integrate with Existing Codebase

Ensure seamless integration:
- Follow existing project conventions (naming, folder structure)
- Use established patterns (error handling, logging)
- Integrate with existing middleware (auth, cors, rate limiting)
- Add routes to main router/app configuration
- Update imports and exports

## Reference Examples

### Example 1: Express + TypeScript REST API

**Complete REST endpoint with validation, auth, and error handling**

```typescript
// src/routes/users.routes.ts
import { Router } from 'express';
import { UserController } from '../controllers/user.controller';
import { authenticate } from '../middleware/auth';
import { validateRequest } from '../middleware/validation';
import { createUserSchema, updateUserSchema, getUsersQuerySchema } from '../schemas/user.schema';
import { asyncHandler } from '../utils/async-handler';

const router = Router();
const userController = new UserController();

/**
 * @openapi
 * /users:
 *   post:
 *     tags:
 *       - Users
 *     summary: Create a new user
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             $ref: '#/components/schemas/CreateUserRequest'
 *     responses:
 *       201:
 *         description: User created successfully
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/UserResponse'
 *       400:
 *         description: Invalid input
 *       401:
 *         description: Unauthorized
 */
router.post(
  '/users',
  authenticate,
  validateRequest(createUserSchema),
  asyncHandler(userController.create)
);

/**
 * @openapi
 * /users:
 *   get:
 *     tags:
 *       - Users
 *     summary: Get all users with pagination
 *     parameters:
 *       - in: query
 *         name: page
 *         schema:
 *           type: integer
 *           default: 1
 *       - in: query
 *         name: limit
 *         schema:
 *           type: integer
 *           default: 20
 *       - in: query
 *         name: search
 *         schema:
 *           type: string
 *     responses:
 *       200:
 *         description: List of users
 */
router.get(
  '/users',
  authenticate,
  validateRequest(getUsersQuerySchema, 'query'),
  asyncHandler(userController.list)
);

/**
 * @openapi
 * /users/{id}:
 *   get:
 *     tags:
 *       - Users
 *     summary: Get user by ID
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: string
 *     responses:
 *       200:
 *         description: User details
 *       404:
 *         description: User not found
 */
router.get(
  '/users/:id',
  authenticate,
  asyncHandler(userController.getById)
);

router.put(
  '/users/:id',
  authenticate,
  validateRequest(updateUserSchema),
  asyncHandler(userController.update)
);

router.delete(
  '/users/:id',
  authenticate,
  asyncHandler(userController.delete)
);

export default router;
```

```typescript
// src/controllers/user.controller.ts
import { Request, Response } from 'express';
import { UserService } from '../services/user.service';
import { CreateUserDto, UpdateUserDto, GetUsersQueryDto } from '../dtos/user.dto';
import { ApiError } from '../utils/api-error';

export class UserController {
  private userService: UserService;

  constructor() {
    this.userService = new UserService();
  }

  create = async (req: Request, res: Response): Promise<void> => {
    const createUserDto: CreateUserDto = req.body;

    // Check if user already exists
    const existingUser = await this.userService.findByEmail(createUserDto.email);
    if (existingUser) {
      throw new ApiError(400, 'User with this email already exists');
    }

    const user = await this.userService.create(createUserDto);

    res.status(201).json({
      success: true,
      data: user,
      message: 'User created successfully',
    });
  };

  list = async (req: Request, res: Response): Promise<void> => {
    const query: GetUsersQueryDto = req.query;

    const { users, total, page, limit } = await this.userService.findAll(query);

    res.status(200).json({
      success: true,
      data: users,
      pagination: {
        page,
        limit,
        total,
        pages: Math.ceil(total / limit),
      },
    });
  };

  getById = async (req: Request, res: Response): Promise<void> => {
    const { id } = req.params;

    const user = await this.userService.findById(id);

    if (!user) {
      throw new ApiError(404, 'User not found');
    }

    res.status(200).json({
      success: true,
      data: user,
    });
  };

  update = async (req: Request, res: Response): Promise<void> => {
    const { id } = req.params;
    const updateUserDto: UpdateUserDto = req.body;

    const user = await this.userService.update(id, updateUserDto);

    if (!user) {
      throw new ApiError(404, 'User not found');
    }

    res.status(200).json({
      success: true,
      data: user,
      message: 'User updated successfully',
    });
  };

  delete = async (req: Request, res: Response): Promise<void> => {
    const { id } = req.params;

    await this.userService.delete(id);

    res.status(200).json({
      success: true,
      message: 'User deleted successfully',
    });
  };
}
```

```typescript
// src/services/user.service.ts
import { Repository } from 'typeorm';
import { AppDataSource } from '../config/database';
import { User } from '../entities/user.entity';
import { CreateUserDto, UpdateUserDto, GetUsersQueryDto } from '../dtos/user.dto';
import { hashPassword } from '../utils/crypto';

export class UserService {
  private userRepository: Repository<User>;

  constructor() {
    this.userRepository = AppDataSource.getRepository(User);
  }

  async create(createUserDto: CreateUserDto): Promise<User> {
    const hashedPassword = await hashPassword(createUserDto.password);

    const user = this.userRepository.create({
      ...createUserDto,
      password: hashedPassword,
    });

    return await this.userRepository.save(user);
  }

  async findAll(query: GetUsersQueryDto) {
    const { page = 1, limit = 20, search } = query;
    const skip = (page - 1) * limit;

    const queryBuilder = this.userRepository.createQueryBuilder('user');

    if (search) {
      queryBuilder.where(
        'user.email ILIKE :search OR user.name ILIKE :search',
        { search: `%${search}%` }
      );
    }

    const [users, total] = await queryBuilder
      .skip(skip)
      .take(limit)
      .orderBy('user.createdAt', 'DESC')
      .getManyAndCount();

    return { users, total, page, limit };
  }

  async findById(id: string): Promise<User | null> {
    return await this.userRepository.findOne({ where: { id } });
  }

  async findByEmail(email: string): Promise<User | null> {
    return await this.userRepository.findOne({ where: { email } });
  }

  async update(id: string, updateUserDto: UpdateUserDto): Promise<User | null> {
    const user = await this.findById(id);

    if (!user) {
      return null;
    }

    if (updateUserDto.password) {
      updateUserDto.password = await hashPassword(updateUserDto.password);
    }

    Object.assign(user, updateUserDto);

    return await this.userRepository.save(user);
  }

  async delete(id: string): Promise<void> {
    await this.userRepository.delete(id);
  }
}
```

```typescript
// src/schemas/user.schema.ts
import { z } from 'zod';

export const createUserSchema = z.object({
  body: z.object({
    email: z.string().email('Invalid email format'),
    name: z.string().min(2, 'Name must be at least 2 characters'),
    password: z.string().min(8, 'Password must be at least 8 characters'),
    role: z.enum(['user', 'admin']).optional().default('user'),
  }),
});

export const updateUserSchema = z.object({
  body: z.object({
    email: z.string().email().optional(),
    name: z.string().min(2).optional(),
    password: z.string().min(8).optional(),
    role: z.enum(['user', 'admin']).optional(),
  }),
});

export const getUsersQuerySchema = z.object({
  query: z.object({
    page: z.string().transform(Number).pipe(z.number().int().positive()).optional(),
    limit: z.string().transform(Number).pipe(z.number().int().positive().max(100)).optional(),
    search: z.string().optional(),
  }),
});

export type CreateUserDto = z.infer<typeof createUserSchema>['body'];
export type UpdateUserDto = z.infer<typeof updateUserSchema>['body'];
export type GetUsersQueryDto = z.infer<typeof getUsersQuerySchema>['query'];
```

### Example 2: FastAPI + Python REST API

**Complete REST endpoint with Pydantic validation and async operations**

```python
# app/routers/users.py
from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserResponse, UserListResponse
from app.services.user_service import UserService
from app.middleware.auth import get_current_user

router = APIRouter(prefix="/users", tags=["users"])

@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
    description="Create a new user with email, name, and password"
)
async def create_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new user.

    - **email**: Valid email address
    - **name**: User's full name
    - **password**: Minimum 8 characters
    - **role**: user or admin (default: user)
    """
    user_service = UserService(db)

    # Check if user already exists
    existing_user = await user_service.get_by_email(user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )

    user = await user_service.create(user_data)
    return user

@router.get(
    "",
    response_model=UserListResponse,
    summary="Get all users",
    description="Get all users with pagination and optional search"
)
async def get_users(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    search: Optional[str] = Query(None, description="Search by email or name"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get all users with pagination.

    Returns a paginated list of users with total count.
    """
    user_service = UserService(db)

    users, total = await user_service.get_all(
        skip=(page - 1) * limit,
        limit=limit,
        search=search
    )

    return {
        "users": users,
        "total": total,
        "page": page,
        "limit": limit,
        "pages": (total + limit - 1) // limit
    }

@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Get user by ID"
)
async def get_user(
    user_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific user by ID"""
    user_service = UserService(db)
    user = await user_service.get_by_id(user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user

@router.put(
    "/{user_id}",
    response_model=UserResponse,
    summary="Update user"
)
async def update_user(
    user_id: str,
    user_data: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a user's information"""
    user_service = UserService(db)
    user = await user_service.update(user_id, user_data)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user

@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete user"
)
async def delete_user(
    user_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a user"""
    user_service = UserService(db)
    deleted = await user_service.delete(user_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
```

```python
# app/schemas/user.py
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional, List
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"

class UserBase(BaseModel):
    email: EmailStr
    name: str = Field(..., min_length=2, max_length=100)

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)
    role: UserRole = UserRole.USER

    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    password: Optional[str] = Field(None, min_length=8)
    role: Optional[UserRole] = None

class UserResponse(UserBase):
    id: str
    role: UserRole
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class UserListResponse(BaseModel):
    users: List[UserResponse]
    total: int
    page: int
    limit: int
    pages: int
```

```python
# app/services/user_service.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, func
from typing import Optional, Tuple, List

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.utils.security import hash_password

class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, user_data: UserCreate) -> User:
        """Create a new user"""
        hashed_password = hash_password(user_data.password)

        user = User(
            email=user_data.email,
            name=user_data.name,
            password=hashed_password,
            role=user_data.role
        )

        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)

        return user

    async def get_all(
        self,
        skip: int = 0,
        limit: int = 20,
        search: Optional[str] = None
    ) -> Tuple[List[User], int]:
        """Get all users with pagination and optional search"""
        query = select(User)

        if search:
            search_filter = or_(
                User.email.ilike(f"%{search}%"),
                User.name.ilike(f"%{search}%")
            )
            query = query.where(search_filter)

        # Get total count
        count_query = select(func.count()).select_from(query.subquery())
        total = await self.db.scalar(count_query)

        # Get paginated results
        query = query.offset(skip).limit(limit).order_by(User.created_at.desc())
        result = await self.db.execute(query)
        users = result.scalars().all()

        return users, total

    async def get_by_id(self, user_id: str) -> Optional[User]:
        """Get user by ID"""
        query = select(User).where(User.id == user_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        query = select(User).where(User.email == email)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def update(self, user_id: str, user_data: UserUpdate) -> Optional[User]:
        """Update user"""
        user = await self.get_by_id(user_id)

        if not user:
            return None

        update_data = user_data.model_dump(exclude_unset=True)

        if 'password' in update_data:
            update_data['password'] = hash_password(update_data['password'])

        for field, value in update_data.items():
            setattr(user, field, value)

        await self.db.commit()
        await self.db.refresh(user)

        return user

    async def delete(self, user_id: str) -> bool:
        """Delete user"""
        user = await self.get_by_id(user_id)

        if not user:
            return False

        await self.db.delete(user)
        await self.db.commit()

        return True
```

### Example 3: GraphQL Resolver with Apollo Server

**Complete GraphQL API with resolvers, DataLoader, and subscriptions**

```typescript
// src/graphql/resolvers/user.resolver.ts
import { UserService } from '../../services/user.service';
import { CreateUserInput, UpdateUserInput, UsersQueryInput } from '../inputs/user.input';
import { AuthenticationError, UserInputError } from 'apollo-server-express';
import { Context } from '../context';
import DataLoader from 'dataloader';

export const userResolvers = {
  Query: {
    users: async (
      _parent: any,
      { input }: { input: UsersQueryInput },
      { userService, user }: Context
    ) => {
      if (!user) {
        throw new AuthenticationError('Not authenticated');
      }

      const { page = 1, limit = 20, search } = input;
      return await userService.findAll({ page, limit, search });
    },

    user: async (
      _parent: any,
      { id }: { id: string },
      { userService, user, loaders }: Context
    ) => {
      if (!user) {
        throw new AuthenticationError('Not authenticated');
      }

      // Use DataLoader to batch and cache user fetches
      return await loaders.userLoader.load(id);
    },

    me: async (_parent: any, _args: any, { user }: Context) => {
      if (!user) {
        throw new AuthenticationError('Not authenticated');
      }

      return user;
    },
  },

  Mutation: {
    createUser: async (
      _parent: any,
      { input }: { input: CreateUserInput },
      { userService, user }: Context
    ) => {
      if (!user) {
        throw new AuthenticationError('Not authenticated');
      }

      const existingUser = await userService.findByEmail(input.email);
      if (existingUser) {
        throw new UserInputError('User with this email already exists');
      }

      const newUser = await userService.create(input);
      return newUser;
    },

    updateUser: async (
      _parent: any,
      { id, input }: { id: string; input: UpdateUserInput },
      { userService, user, loaders }: Context
    ) => {
      if (!user) {
        throw new AuthenticationError('Not authenticated');
      }

      const updatedUser = await userService.update(id, input);

      if (!updatedUser) {
        throw new UserInputError('User not found');
      }

      // Clear DataLoader cache for this user
      loaders.userLoader.clear(id);

      return updatedUser;
    },

    deleteUser: async (
      _parent: any,
      { id }: { id: string },
      { userService, user, loaders }: Context
    ) => {
      if (!user) {
        throw new AuthenticationError('Not authenticated');
      }

      await userService.delete(id);

      // Clear DataLoader cache
      loaders.userLoader.clear(id);

      return { success: true, message: 'User deleted successfully' };
    },
  },

  User: {
    // Field resolver for computed fields
    fullName: (parent: any) => {
      return `${parent.firstName} ${parent.lastName}`;
    },

    // Field resolver with DataLoader for related data
    posts: async (parent: any, _args: any, { loaders }: Context) => {
      return await loaders.postsByUserLoader.load(parent.id);
    },
  },
};

// DataLoader for batching user fetches
export const createUserLoader = (userService: UserService) => {
  return new DataLoader<string, any>(async (ids: readonly string[]) => {
    const users = await userService.findByIds([...ids]);

    // Return users in the same order as requested IDs
    const userMap = new Map(users.map(user => [user.id, user]));
    return ids.map(id => userMap.get(id) || null);
  });
};
```

```typescript
// src/graphql/schema.ts
import { gql } from 'apollo-server-express';

export const typeDefs = gql`
  type User {
    id: ID!
    email: String!
    name: String!
    fullName: String!
    role: UserRole!
    posts: [Post!]!
    createdAt: DateTime!
    updatedAt: DateTime!
  }

  enum UserRole {
    USER
    ADMIN
  }

  type UsersResponse {
    users: [User!]!
    total: Int!
    page: Int!
    limit: Int!
    pages: Int!
  }

  type DeleteResponse {
    success: Boolean!
    message: String!
  }

  input CreateUserInput {
    email: String!
    name: String!
    password: String!
    role: UserRole
  }

  input UpdateUserInput {
    email: String
    name: String
    password: String
    role: UserRole
  }

  input UsersQueryInput {
    page: Int
    limit: Int
    search: String
  }

  type Query {
    users(input: UsersQueryInput!): UsersResponse!
    user(id: ID!): User
    me: User
  }

  type Mutation {
    createUser(input: CreateUserInput!): User!
    updateUser(id: ID!, input: UpdateUserInput!): User!
    deleteUser(id: ID!): DeleteResponse!
  }

  scalar DateTime
`;
```

### Example 4: Go Gin REST API

**Complete REST API with Go and Gin framework**

```go
// internal/handlers/user_handler.go
package handlers

import (
	"net/http"
	"strconv"

	"github.com/gin-gonic/gin"
	"github.com/your-app/internal/dto"
	"github.com/your-app/internal/middleware"
	"github.com/your-app/internal/services"
)

type UserHandler struct {
	userService *services.UserService
}

func NewUserHandler(userService *services.UserService) *UserHandler {
	return &UserHandler{
		userService: userService,
	}
}

// RegisterRoutes registers all user routes
func (h *UserHandler) RegisterRoutes(r *gin.RouterGroup) {
	users := r.Group("/users")
	users.Use(middleware.AuthMiddleware())
	{
		users.POST("", h.CreateUser)
		users.GET("", h.GetUsers)
		users.GET("/:id", h.GetUser)
		users.PUT("/:id", h.UpdateUser)
		users.DELETE("/:id", h.DeleteUser)
	}
}

// CreateUser godoc
// @Summary Create a new user
// @Description Create a new user with email, name, and password
// @Tags users
// @Accept json
// @Produce json
// @Param user body dto.CreateUserRequest true "User data"
// @Success 201 {object} dto.UserResponse
// @Failure 400 {object} dto.ErrorResponse
// @Failure 401 {object} dto.ErrorResponse
// @Security BearerAuth
// @Router /users [post]
func (h *UserHandler) CreateUser(c *gin.Context) {
	var req dto.CreateUserRequest

	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, dto.ErrorResponse{
			Success: false,
			Error:   "Invalid request body",
			Details: err.Error(),
		})
		return
	}

	// Check if user already exists
	existing, err := h.userService.GetByEmail(c.Request.Context(), req.Email)
	if err == nil && existing != nil {
		c.JSON(http.StatusBadRequest, dto.ErrorResponse{
			Success: false,
			Error:   "User with this email already exists",
		})
		return
	}

	user, err := h.userService.Create(c.Request.Context(), &req)
	if err != nil {
		c.JSON(http.StatusInternalServerError, dto.ErrorResponse{
			Success: false,
			Error:   "Failed to create user",
			Details: err.Error(),
		})
		return
	}

	c.JSON(http.StatusCreated, dto.SuccessResponse{
		Success: true,
		Data:    user,
		Message: "User created successfully",
	})
}

// GetUsers godoc
// @Summary Get all users
// @Description Get all users with pagination and optional search
// @Tags users
// @Accept json
// @Produce json
// @Param page query int false "Page number" default(1)
// @Param limit query int false "Items per page" default(20)
// @Param search query string false "Search by email or name"
// @Success 200 {object} dto.UsersListResponse
// @Failure 401 {object} dto.ErrorResponse
// @Security BearerAuth
// @Router /users [get]
func (h *UserHandler) GetUsers(c *gin.Context) {
	page, _ := strconv.Atoi(c.DefaultQuery("page", "1"))
	limit, _ := strconv.Atoi(c.DefaultQuery("limit", "20"))
	search := c.Query("search")

	if page < 1 {
		page = 1
	}
	if limit < 1 || limit > 100 {
		limit = 20
	}

	users, total, err := h.userService.GetAll(c.Request.Context(), page, limit, search)
	if err != nil {
		c.JSON(http.StatusInternalServerError, dto.ErrorResponse{
			Success: false,
			Error:   "Failed to fetch users",
			Details: err.Error(),
		})
		return
	}

	pages := (total + int64(limit) - 1) / int64(limit)

	c.JSON(http.StatusOK, dto.UsersListResponse{
		Success: true,
		Data:    users,
		Pagination: dto.PaginationMeta{
			Page:  page,
			Limit: limit,
			Total: int(total),
			Pages: int(pages),
		},
	})
}

// GetUser godoc
// @Summary Get user by ID
// @Description Get a specific user by their ID
// @Tags users
// @Accept json
// @Produce json
// @Param id path string true "User ID"
// @Success 200 {object} dto.UserResponse
// @Failure 404 {object} dto.ErrorResponse
// @Security BearerAuth
// @Router /users/{id} [get]
func (h *UserHandler) GetUser(c *gin.Context) {
	id := c.Param("id")

	user, err := h.userService.GetByID(c.Request.Context(), id)
	if err != nil {
		c.JSON(http.StatusNotFound, dto.ErrorResponse{
			Success: false,
			Error:   "User not found",
		})
		return
	}

	c.JSON(http.StatusOK, dto.SuccessResponse{
		Success: true,
		Data:    user,
	})
}

// UpdateUser godoc
// @Summary Update user
// @Description Update a user's information
// @Tags users
// @Accept json
// @Produce json
// @Param id path string true "User ID"
// @Param user body dto.UpdateUserRequest true "Update data"
// @Success 200 {object} dto.UserResponse
// @Failure 404 {object} dto.ErrorResponse
// @Security BearerAuth
// @Router /users/{id} [put]
func (h *UserHandler) UpdateUser(c *gin.Context) {
	id := c.Param("id")
	var req dto.UpdateUserRequest

	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, dto.ErrorResponse{
			Success: false,
			Error:   "Invalid request body",
			Details: err.Error(),
		})
		return
	}

	user, err := h.userService.Update(c.Request.Context(), id, &req)
	if err != nil {
		c.JSON(http.StatusNotFound, dto.ErrorResponse{
			Success: false,
			Error:   "User not found",
		})
		return
	}

	c.JSON(http.StatusOK, dto.SuccessResponse{
		Success: true,
		Data:    user,
		Message: "User updated successfully",
	})
}

// DeleteUser godoc
// @Summary Delete user
// @Description Delete a user by ID
// @Tags users
// @Accept json
// @Produce json
// @Param id path string true "User ID"
// @Success 200 {object} dto.MessageResponse
// @Failure 404 {object} dto.ErrorResponse
// @Security BearerAuth
// @Router /users/{id} [delete]
func (h *UserHandler) DeleteUser(c *gin.Context) {
	id := c.Param("id")

	err := h.userService.Delete(c.Request.Context(), id)
	if err != nil {
		c.JSON(http.StatusNotFound, dto.ErrorResponse{
			Success: false,
			Error:   "User not found",
		})
		return
	}

	c.JSON(http.StatusOK, dto.MessageResponse{
		Success: true,
		Message: "User deleted successfully",
	})
}
```

### Example 5: WebSocket Handler with Authentication

**Complete WebSocket server with connection management and broadcasting**

```typescript
// src/websocket/chat.handler.ts
import { WebSocket, WebSocketServer } from 'ws';
import { IncomingMessage } from 'http';
import { v4 as uuidv4 } from 'uuid';
import { verifyToken } from '../utils/jwt';
import { ChatMessage, ConnectionInfo } from '../types/chat.types';

export class ChatWebSocketHandler {
  private wss: WebSocketServer;
  private connections: Map<string, ConnectionInfo> = new Map();
  private pingInterval: NodeJS.Timeout;

  constructor(wss: WebSocketServer) {
    this.wss = wss;
    this.setupConnectionHandler();
    this.startHeartbeat();
  }

  private setupConnectionHandler() {
    this.wss.on('connection', async (ws: WebSocket, req: IncomingMessage) => {
      try {
        // Authenticate connection
        const token = this.extractToken(req);
        if (!token) {
          ws.close(401, 'Unauthorized: No token provided');
          return;
        }

        const user = await verifyToken(token);
        if (!user) {
          ws.close(401, 'Unauthorized: Invalid token');
          return;
        }

        // Create connection info
        const connectionId = uuidv4();
        const connectionInfo: ConnectionInfo = {
          id: connectionId,
          userId: user.id,
          username: user.username,
          ws,
          isAlive: true,
          connectedAt: new Date(),
        };

        this.connections.set(connectionId, connectionInfo);
        console.log(`User ${user.username} connected (${connectionId})`);

        // Send welcome message
        this.sendToConnection(connectionId, {
          type: 'connection',
          data: {
            connectionId,
            message: 'Connected successfully',
            onlineUsers: this.getOnlineUsers(),
          },
        });

        // Broadcast user joined
        this.broadcast({
          type: 'user_joined',
          data: {
            userId: user.id,
            username: user.username,
          },
        }, connectionId);

        // Setup message handler
        ws.on('message', (rawData: Buffer) => {
          this.handleMessage(connectionId, rawData);
        });

        // Setup pong handler for heartbeat
        ws.on('pong', () => {
          const conn = this.connections.get(connectionId);
          if (conn) {
            conn.isAlive = true;
          }
        });

        // Setup close handler
        ws.on('close', () => {
          this.handleDisconnection(connectionId);
        });

        // Setup error handler
        ws.on('error', (error) => {
          console.error(`WebSocket error for ${connectionId}:`, error);
          this.handleDisconnection(connectionId);
        });
      } catch (error) {
        console.error('Connection setup error:', error);
        ws.close(500, 'Internal server error');
      }
    });
  }

  private extractToken(req: IncomingMessage): string | null {
    const url = new URL(req.url || '', `http://${req.headers.host}`);
    return url.searchParams.get('token');
  }

  private handleMessage(connectionId: string, rawData: Buffer) {
    try {
      const conn = this.connections.get(connectionId);
      if (!conn) return;

      const message: ChatMessage = JSON.parse(rawData.toString());

      // Validate message
      if (!message.type || !message.data) {
        this.sendError(connectionId, 'Invalid message format');
        return;
      }

      switch (message.type) {
        case 'chat_message':
          this.handleChatMessage(connectionId, message.data);
          break;
        case 'typing':
          this.handleTyping(connectionId, message.data);
          break;
        case 'private_message':
          this.handlePrivateMessage(connectionId, message.data);
          break;
        default:
          this.sendError(connectionId, `Unknown message type: ${message.type}`);
      }
    } catch (error) {
      console.error(`Message handling error for ${connectionId}:`, error);
      this.sendError(connectionId, 'Failed to process message');
    }
  }

  private handleChatMessage(connectionId: string, data: any) {
    const conn = this.connections.get(connectionId);
    if (!conn) return;

    const chatMessage = {
      type: 'chat_message',
      data: {
        id: uuidv4(),
        userId: conn.userId,
        username: conn.username,
        content: data.content,
        timestamp: new Date().toISOString(),
      },
    };

    // Broadcast to all connected clients
    this.broadcast(chatMessage);
  }

  private handleTyping(connectionId: string, data: any) {
    const conn = this.connections.get(connectionId);
    if (!conn) return;

    this.broadcast({
      type: 'typing',
      data: {
        userId: conn.userId,
        username: conn.username,
        isTyping: data.isTyping,
      },
    }, connectionId);
  }

  private handlePrivateMessage(connectionId: string, data: any) {
    const sender = this.connections.get(connectionId);
    if (!sender) return;

    // Find recipient connection
    const recipientConn = Array.from(this.connections.values()).find(
      conn => conn.userId === data.recipientId
    );

    if (!recipientConn) {
      this.sendError(connectionId, 'Recipient not found or offline');
      return;
    }

    const privateMessage = {
      type: 'private_message',
      data: {
        id: uuidv4(),
        senderId: sender.userId,
        senderUsername: sender.username,
        content: data.content,
        timestamp: new Date().toISOString(),
      },
    };

    // Send to recipient
    this.sendToConnection(recipientConn.id, privateMessage);

    // Send confirmation to sender
    this.sendToConnection(connectionId, {
      type: 'message_sent',
      data: privateMessage.data,
    });
  }

  private handleDisconnection(connectionId: string) {
    const conn = this.connections.get(connectionId);
    if (!conn) return;

    console.log(`User ${conn.username} disconnected (${connectionId})`);

    // Broadcast user left
    this.broadcast({
      type: 'user_left',
      data: {
        userId: conn.userId,
        username: conn.username,
      },
    });

    // Remove connection
    this.connections.delete(connectionId);
  }

  private broadcast(message: any, excludeConnectionId?: string) {
    const data = JSON.stringify(message);

    this.connections.forEach((conn, id) => {
      if (id !== excludeConnectionId && conn.ws.readyState === WebSocket.OPEN) {
        conn.ws.send(data);
      }
    });
  }

  private sendToConnection(connectionId: string, message: any) {
    const conn = this.connections.get(connectionId);
    if (conn && conn.ws.readyState === WebSocket.OPEN) {
      conn.ws.send(JSON.stringify(message));
    }
  }

  private sendError(connectionId: string, error: string) {
    this.sendToConnection(connectionId, {
      type: 'error',
      data: { error },
    });
  }

  private getOnlineUsers() {
    return Array.from(this.connections.values()).map(conn => ({
      userId: conn.userId,
      username: conn.username,
    }));
  }

  private startHeartbeat() {
    this.pingInterval = setInterval(() => {
      this.connections.forEach((conn, id) => {
        if (!conn.isAlive) {
          console.log(`Terminating inactive connection: ${id}`);
          conn.ws.terminate();
          this.connections.delete(id);
          return;
        }

        conn.isAlive = false;
        conn.ws.ping();
      });
    }, 30000); // Check every 30 seconds
  }

  public shutdown() {
    clearInterval(this.pingInterval);
    this.connections.forEach(conn => {
      conn.ws.close(1000, 'Server shutting down');
    });
    this.connections.clear();
  }
}
```

## Quality Standards

Ensure all generated API code:

- **Type Safety**: Full TypeScript types or Python type hints
- **Validation**: Request/response validation with clear error messages
- **Authentication**: Proper auth checks on protected endpoints
- **Authorization**: Role-based access control where applicable
- **Error Handling**: Consistent error responses with appropriate status codes
- **Logging**: Structured logging for debugging and monitoring
- **Documentation**: OpenAPI/Swagger annotations or GraphQL descriptions
- **Testing**: Integration tests for all endpoints
- **Security**: Protection against common vulnerabilities (SQL injection, XSS, CSRF)
- **Performance**: Efficient database queries, caching where appropriate
- **Pagination**: For list endpoints that could return many results
- **Rate Limiting**: Protection against abuse
- **CORS**: Proper CORS configuration for browser clients
- **Versioning**: API versioning strategy (URL, header, or parameter)

## Output Format

Provide the following deliverables:

1. **Route/Handler Files**
   - Main endpoint definitions with HTTP methods
   - Request validation middleware
   - Authentication/authorization checks
   - Location: `src/routes/{resource}.routes.ts` or similar

2. **Controller/Handler Layer**
   - Business logic coordination
   - Request parsing and response formatting
   - Error handling
   - Location: `src/controllers/{resource}.controller.ts` or similar

3. **Service Layer**
   - Core business logic
   - Database interactions
   - External API calls
   - Location: `src/services/{resource}.service.ts` or similar

4. **Data Access Layer (if using ORM)**
   - Repository patterns
   - Query builders
   - Location: `src/repositories/{resource}.repository.ts` or similar

5. **Validation Schemas**
   - Request validation (Zod, Joi, Pydantic, etc.)
   - Response serialization
   - Location: `src/schemas/{resource}.schema.ts` or similar

6. **Types/Interfaces/DTOs**
   - TypeScript interfaces
   - Data transfer objects
   - Location: `src/types/{resource}.types.ts` or `src/dtos/{resource}.dto.ts`

7. **Integration Tests**
   - Test all endpoints
   - Test error cases
   - Test authentication/authorization
   - Location: `tests/integration/{resource}.test.ts` or similar

8. **API Documentation**
   - OpenAPI/Swagger spec (for REST)
   - GraphQL schema (for GraphQL)
   - Usage examples with curl/Postman
   - Location: `docs/api/{resource}.md` or auto-generated

9. **Summary**
   - List of created endpoints with methods and paths
   - Authentication requirements
   - Example API calls with curl
   - Next steps (connecting to database, adding more features, deployment)
   - How to run tests
   - How to view API documentation

**Example Summary:**

```markdown
## Created API Endpoints

### Users Resource

**Endpoints:**
- POST /users - Create new user (requires authentication)
- GET /users - List all users with pagination (requires authentication)
- GET /users/:id - Get user by ID (requires authentication)
- PUT /users/:id - Update user (requires authentication)
- DELETE /users/:id - Delete user (requires authentication)

**Authentication:**
All endpoints require a valid JWT token in the Authorization header:
```bash
Authorization: Bearer <your-jwt-token>
```

**Example Usage:**

Create user:
```bash
curl -X POST http://localhost:3000/api/users \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "email": "user@example.com",
    "name": "John Doe",
    "password": "SecurePass123"
  }'
```

Get users:
```bash
curl -X GET "http://localhost:3000/api/users?page=1&limit=20&search=john" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Next Steps:**
1. Run tests: `npm test` or `pytest`
2. View API docs: http://localhost:3000/api-docs (Swagger UI)
3. Update environment variables for database connection
4. Add additional business logic to service layer
5. Configure CORS for your frontend domain
6. Set up rate limiting in production
7. Deploy to production environment

**Files Created:**
- src/routes/users.routes.ts (API routes)
- src/controllers/user.controller.ts (Request handling)
- src/services/user.service.ts (Business logic)
- src/schemas/user.schema.ts (Validation)
- src/types/user.types.ts (TypeScript types)
- tests/integration/users.test.ts (Integration tests)
- docs/api/users.md (API documentation)
```
