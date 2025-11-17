---
description: Test API endpoints with automatic request generation
allowed-tools: Bash, Read, Write
---

# Test API Command

Test API endpoints with automatically generated requests and validation.

## Usage

`/test-api [endpoint] [method] [data]`

## Parameters

- `endpoint` - The API endpoint to test (e.g., /api/users)
- `method` - HTTP method (GET, POST, PUT, DELETE, PATCH)
- `data` - Request body data (JSON format)

## Implementation

!`#!/bin/bash

ENDPOINT=${1:-/api/health}
METHOD=${2:-GET}
DATA=${3:-}
BASE_URL=${BASE_URL:-http://localhost:3000}

# Function to test endpoint
test_endpoint() {
  local url="$BASE_URL$ENDPOINT"
  echo "Testing: $METHOD $url"

  case $METHOD in
    GET)
      curl -X GET "$url" \
        -H "Accept: application/json" \
        -w "\n\nStatus: %{http_code}\nTime: %{time_total}s\n" \
        -s
      ;;
    POST|PUT|PATCH)
      if [ -z "$DATA" ]; then
        echo "Error: Request body required for $METHOD"
        exit 1
      fi
      curl -X $METHOD "$url" \
        -H "Content-Type: application/json" \
        -H "Accept: application/json" \
        -d "$DATA" \
        -w "\n\nStatus: %{http_code}\nTime: %{time_total}s\n" \
        -s
      ;;
    DELETE)
      curl -X DELETE "$url" \
        -H "Accept: application/json" \
        -w "\n\nStatus: %{http_code}\nTime: %{time_total}s\n" \
        -s
      ;;
    *)
      echo "Unsupported method: $METHOD"
      exit 1
      ;;
  esac
}

# Check if server is running
if ! curl -s -o /dev/null -w "%{http_code}" "$BASE_URL" | grep -q "200\|404"; then
  echo "Warning: Server may not be running at $BASE_URL"
  echo "Start the server with: /server start"
fi

# Run the test
test_endpoint

# Generate sample requests for common endpoints
if [ "$ENDPOINT" == "/api/health" ] && [ "$METHOD" == "GET" ]; then
  echo ""
  echo "Sample API test commands:"
  echo "  /test-api /api/users GET"
  echo "  /test-api /api/users POST '{\"name\":\"John\",\"email\":\"john@example.com\"}'"
  echo "  /test-api /api/users/123 PUT '{\"name\":\"Jane\"}'"
  echo "  /test-api /api/users/123 DELETE"
fi
`