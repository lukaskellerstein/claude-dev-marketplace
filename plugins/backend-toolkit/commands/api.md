---
description: Create and manage API endpoints with automatic language detection
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Task
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

!`#!/bin/bash

ACTION=${1:-create}
PROTOCOL=${2:-rest}
RESOURCE=${3:-resource}
OPTIONS=${4:-}

# Detect project language
if [ -f "package.json" ]; then
    LANGUAGE="nodejs"
elif [ -f "go.mod" ]; then
    LANGUAGE="golang"
elif [ -f "pyproject.toml" ] || [ -f "requirements.txt" ]; then
    LANGUAGE="python"
else
    LANGUAGE="unknown"
fi

echo "🔍 Detected language: $LANGUAGE"
echo "📋 Action: $ACTION"
echo "🌐 Protocol: $PROTOCOL"
echo "📦 Resource: $RESOURCE"

case $ACTION in
    create)
        echo "Creating $PROTOCOL API for $RESOURCE in $LANGUAGE..."
        case $LANGUAGE in
            nodejs)
                echo "Invoking Node.js specialist for $PROTOCOL endpoint"
                # Task tool will be invoked by Claude to run the agent
                echo "Please run: Task nodejs-specialist to create the endpoint"
                ;;
            golang)
                echo "Invoking Go specialist for $PROTOCOL endpoint"
                echo "Please run: Task golang-specialist to create the endpoint"
                ;;
            python)
                echo "Invoking Python specialist for $PROTOCOL endpoint"
                echo "Please run: Task python-specialist to create the endpoint"
                ;;
            *)
                echo "Error: Unable to detect project language"
                echo "Please ensure you have one of: package.json, go.mod, or requirements.txt"
                exit 1
                ;;
        esac
        ;;
    list)
        echo "Listing API endpoints..."
        find . -type f \( -name "*.route.*" -o -name "*.controller.*" -o -name "*.handler.*" \) 2>/dev/null | head -20
        ;;
    test)
        echo "Testing $RESOURCE endpoint..."
        echo "Please run: /test-api $RESOURCE"
        ;;
    document)
        echo "Generating API documentation..."
        echo "Looking for OpenAPI/Swagger specs..."
        find . -name "*swagger*" -o -name "*openapi*" 2>/dev/null
        ;;
    *)
        echo "Usage: /api [create|list|test|document] [protocol] [resource]"
        exit 1
        ;;
esac
`