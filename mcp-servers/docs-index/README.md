# Documentation Index MCP Server

A shared, curated index of development documentation links for all Claude Code marketplace plugins.

## What This Provides

This MCP server exposes a comprehensive, curated list of development documentation as **resources**. Claude can:

- **List all available docs**: See what documentation is available across frontend, backend, and infrastructure
- **Read specific docs**: Get the URL and description for a specific topic
- **Discover related topics**: Find related documentation through the relationship graph

## Why This Approach?

Instead of using `mcp-server-fetch` with `ALLOWED_DOMAINS` (which **doesn't actually work**), this provides:

✅ **Curated links** - Only the most relevant documentation pages
✅ **Fast discovery** - No searching needed
✅ **Categorized** - Organized by domain (frontend, backend, infrastructure)
✅ **Related topics** - Discover connected documentation
✅ **Efficient** - Direct links, no wasted searches
✅ **Shared** - One server used by multiple plugins

## Documentation Coverage

### Frontend
- JavaScript (MDN, javascript.info)
- TypeScript
- React
- UI Libraries (shadcn/ui, Radix UI)
- CSS (Tailwind, MDN, Sass)

### Backend
- APIs (GraphQL, REST, gRPC)
- Messaging (WebSocket, Socket.IO, NATS, RabbitMQ, Kafka)
- Databases (PostgreSQL, MongoDB, Redis, Elasticsearch)

### Infrastructure
- Kubernetes
- Terraform
- Docker
- GCP
- Helm
- Traefik

## How Claude Uses This

1. **List resources**: Claude sees all available documentation
2. **Find relevant docs**: Based on the task, Claude identifies needed docs
3. **Get the URL**: Read the resource to get the documentation URL
4. **Fetch content**: Use WebFetch or fetch MCP to get the actual documentation content

## Installation

```bash
cd mcp-servers/docs-index
pip install -r requirements.txt
```

## Configuration in Plugins

Each plugin should add this to their `.mcp.json`:

```json
{
  "mcpServers": {
    "docs-index": {
      "command": "python",
      "args": ["../../mcp-servers/docs-index/server.py"],
      "description": "Curated documentation index for all development topics"
    },
    "fetch": {
      "command": "uvx",
      "args": ["mcp-server-fetch"],
      "description": "Web fetching for documentation URLs"
    }
  }
}
```

**Note the relative path**: `../../mcp-servers/docs-index/server.py` (from plugin directory to root)

## Adding Documentation

Edit `docs-index.json` to add new documentation:

```json
{
  "category": {
    "subcategory": [
      {
        "id": "your-topic",
        "name": "Your Topic Name",
        "description": "What this documentation covers",
        "url": "https://example.com/docs/...",
        "tags": ["tag1", "tag2"],
        "related": ["other-topic-id"]
      }
    ]
  }
}
```

## Example Usage

**Claude listing resources:**
```
I can see the following frontend documentation:
- JavaScript - MDN (docs://frontend/javascript/mdn-js)
- React Quick Start (docs://frontend/react/react-start)
- Tailwind CSS (docs://frontend/css/tailwind)
...
```

**Claude reading a resource:**
```
Reading docs://infrastructure/kubernetes/deployments...

# Kubernetes Deployments
Official guide for creating and managing Kubernetes deployments

Documentation URL: https://kubernetes.io/docs/concepts/workloads/controllers/deployment/

Tags: workloads, controllers
Related Topics: services, statefulsets
```

**Claude using the URL:**
```
Now fetching the deployment documentation from:
https://kubernetes.io/docs/concepts/workloads/controllers/deployment/
```

## Benefits

- **DRY Principle**: One documentation index for all plugins
- **Consistency**: Same documentation sources across all plugins
- **Maintainability**: Update docs in one place
- **Performance**: Direct access without search overhead
- **Discovery**: Browse available documentation by category
