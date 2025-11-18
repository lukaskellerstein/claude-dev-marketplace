# Source Control

## Github

MCP: https://github.com/github/github-mcp-server

# Graphs

## Mermaid

MCP: https://docs.mermaidchart.com/ai/mcp-server

**Configuration (`.mcp.json`):**

```json
{
  "servers": {
    "mermaid-mcp": {
      "url": "https://mcp.mermaidchart.com/mcp",
      "type": "http"
    }
  }
}
```

# Documents

## Markitdown

MCP: https://github.com/microsoft/markitdown/tree/main/packages/markitdown-mcp

MarkItDown currently supports the conversion from:

PDF
PowerPoint
Word
Excel
Images (EXIF metadata and OCR)
Audio (EXIF metadata and speech transcription)
HTML
Text-based formats (CSV, JSON, XML)
ZIP files (iterates over contents)
Youtube URLs
EPubs
... and more!

**Configuration Option 1 - Basic (`.mcp.json`):**

```json
{
  "mcpServers": {
    "markitdown": {
      "command": "docker",
      "args": ["run", "--rm", "-i", "markitdown-mcp:latest"]
    }
  }
}
```

**Configuration Option 2 - With Volume Mount (`.mcp.json`):**

```json
{
  "mcpServers": {
    "markitdown": {
      "command": "docker",
      "args": [
        "run",
        "--rm",
        "-i",
        "-v",
        "/home/user/data:/workdir",
        "markitdown-mcp:latest"
      ]
    }
  }
}
```

# Google cloud

Documentation: `https://github.com/googleapis/gcloud-mcp`

GCloud:

```json
{
  "mcpServers": {
    "gcloud": {
      "command": "npx",
      "args": ["-y", "@google-cloud/gcloud-mcp"]
    }
  }
}
```

Google Cloud storage:

```json
{
  "mcpServers": {
    "gcloudstorage": {
      "command": "npx",
      "args": ["-y", "@google-cloud/storage-mcp"]
    }
  }
}
```

# Terraform

Documentation: `https://github.com/hashicorp/terraform-mcp-server`

```json
{
  "mcpServers": {
    "terraform": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "hashicorp/terraform-mcp-server:0.2.3"]
    }
  }
}
```

# Helm

Official one is not available.

# Kubernetes

Official one is not available.

# Shadcn UI

Documentation: https://ui.shadcn.com/docs/mcp

```json
{
  "mcpServers": {
    "shadcn": {
      "command": "npx",
      "args": ["shadcn@latest", "mcp"]
    }
  }
}
```

# Documentations

```json
{
  "mcpServers": {
    "docs-index": {
      "command": "python",
      "args": ["../../mcp-servers/docs-index/server.py"],
      "description": "Curated documentation index for backend development"
    }
  }
}
```
