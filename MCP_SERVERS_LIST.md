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

# Documentations

```json
{
  "mcpServers": {
    "javascript-docs": {
      "command": "uvx",
      "args": ["mcp-server-fetch"],
      "env": {
        "ALLOWED_DOMAINS": "developer.mozilla.org,javascript.info"
      },
      "description": "JavaScript documentation (MDN & javascript.info)"
    },

    "typescript-docs": {
      "command": "uvx",
      "args": ["mcp-server-fetch"],
      "env": {
        "ALLOWED_DOMAINS": "typescriptlang.org,www.typescriptlang.org"
      },
      "description": "TypeScript official documentation"
    },

    "react-docs": {
      "command": "uvx",
      "args": ["mcp-server-fetch"],
      "env": {
        "ALLOWED_DOMAINS": "react.dev"
      },
      "description": "React official documentation"
    },

    "shadcn-docs": {
      "command": "uvx",
      "args": ["mcp-server-fetch"],
      "env": {
        "ALLOWED_DOMAINS": "ui.shadcn.com"
      },
      "description": "shadcn/ui component library documentation"
    },

    "radix-docs": {
      "command": "uvx",
      "args": ["mcp-server-fetch"],
      "env": {
        "ALLOWED_DOMAINS": "radix-ui.com,www.radix-ui.com"
      },
      "description": "Radix UI primitives documentation"
    },

    "tailwind-docs": {
      "command": "uvx",
      "args": ["mcp-server-fetch"],
      "env": {
        "ALLOWED_DOMAINS": "tailwindcss.com"
      },
      "description": "Tailwind CSS documentation"
    },

    "css-docs": {
      "command": "uvx",
      "args": ["mcp-server-fetch"],
      "env": {
        "ALLOWED_DOMAINS": "developer.mozilla.org,css-tricks.com,sass-lang.com"
      },
      "description": "CSS/SCSS documentation (MDN, CSS-Tricks, Sass)"
    },

    "rest-graphql-docs": {
      "command": "uvx",
      "args": ["mcp-server-fetch"],
      "env": {
        "ALLOWED_DOMAINS": "graphql.org,www.graphql.org"
      },
      "description": "REST API and GraphQL documentation"
    },

    "grpc-docs": {
      "command": "uvx",
      "args": ["mcp-server-fetch"],
      "env": {
        "ALLOWED_DOMAINS": "grpc.io"
      },
      "description": "gRPC official documentation"
    },

    "websocket-docs": {
      "command": "uvx",
      "args": ["mcp-server-fetch"],
      "env": {
        "ALLOWED_DOMAINS": "developer.mozilla.org,socket.io,websocket.org"
      },
      "description": "WebSocket documentation"
    },

    "nats-docs": {
      "command": "uvx",
      "args": ["mcp-server-fetch"],
      "env": {
        "ALLOWED_DOMAINS": "docs.nats.io,nats.io"
      },
      "description": "NATS messaging system documentation"
    },

    "rabbitmq-docs": {
      "command": "uvx",
      "args": ["mcp-server-fetch"],
      "env": {
        "ALLOWED_DOMAINS": "rabbitmq.com,www.rabbitmq.com"
      },
      "description": "RabbitMQ message broker documentation"
    },

    "kafka-docs": {
      "command": "uvx",
      "args": ["mcp-server-fetch"],
      "env": {
        "ALLOWED_DOMAINS": "kafka.apache.org"
      },
      "description": "Apache Kafka documentation"
    },

    "postgresql-docs": {
      "command": "uvx",
      "args": ["mcp-server-fetch"],
      "env": {
        "ALLOWED_DOMAINS": "postgresql.org,www.postgresql.org"
      },
      "description": "PostgreSQL official documentation"
    },

    "supabase-docs": {
      "command": "uvx",
      "args": ["mcp-server-fetch"],
      "env": {
        "ALLOWED_DOMAINS": "supabase.com,supabase.io"
      },
      "description": "Supabase documentation"
    },

    "qdrant-docs": {
      "command": "uvx",
      "args": ["mcp-server-fetch"],
      "env": {
        "ALLOWED_DOMAINS": "qdrant.tech"
      },
      "description": "Qdrant vector database documentation"
    },

    "elasticsearch-docs": {
      "command": "uvx",
      "args": ["mcp-server-fetch"],
      "env": {
        "ALLOWED_DOMAINS": "elastic.co,www.elastic.co"
      },
      "description": "Elasticsearch documentation"
    },

    "mongodb-docs": {
      "command": "uvx",
      "args": ["mcp-server-fetch"],
      "env": {
        "ALLOWED_DOMAINS": "mongodb.com,www.mongodb.com,docs.mongodb.com"
      },
      "description": "MongoDB documentation"
    },

    "redis-docs": {
      "command": "uvx",
      "args": ["mcp-server-fetch"],
      "env": {
        "ALLOWED_DOMAINS": "redis.io,redis.com"
      },
      "description": "Redis documentation (including pub/sub)"
    },

    "minio-docs": {
      "command": "uvx",
      "args": ["mcp-server-fetch"],
      "env": {
        "ALLOWED_DOMAINS": "min.io,docs.min.io"
      },
      "description": "MinIO S3-compatible storage documentation"
    },

    "github-actions-docs": {
      "command": "uvx",
      "args": ["mcp-server-fetch"],
      "env": {
        "ALLOWED_DOMAINS": "docs.github.com"
      },
      "description": "GitHub Actions documentation"
    },

    "gcp-docs": {
      "command": "uvx",
      "args": ["mcp-server-fetch"],
      "env": {
        "ALLOWED_DOMAINS": "docs.cloud.google.com,cloud.google.com"
      },
      "description": "Google Cloud Platform documentation"
    },

    "kubernetes-docs": {
      "command": "uvx",
      "args": ["mcp-server-fetch"],
      "env": {
        "ALLOWED_DOMAINS": "kubernetes.io"
      },
      "description": "Kubernetes official documentation"
    },

    "docker-docs": {
      "command": "uvx",
      "args": ["mcp-server-fetch"],
      "env": {
        "ALLOWED_DOMAINS": "docs.docker.com"
      },
      "description": "Docker documentation"
    },

    "terraform-docs": {
      "command": "uvx",
      "args": ["mcp-server-fetch"],
      "env": {
        "ALLOWED_DOMAINS": "terraform.io,www.terraform.io,registry.terraform.io"
      },
      "description": "Terraform and provider registry documentation"
    },

    "helm-docs": {
      "command": "uvx",
      "args": ["mcp-server-fetch"],
      "env": {
        "ALLOWED_DOMAINS": "helm.sh"
      },
      "description": "Helm package manager documentation"
    },

    "pytorch-docs": {
      "command": "uvx",
      "args": ["mcp-server-fetch"],
      "env": {
        "ALLOWED_DOMAINS": "pytorch.org"
      },
      "description": "PyTorch deep learning framework documentation"
    },

    "huggingface-docs": {
      "command": "uvx",
      "args": ["mcp-server-fetch"],
      "env": {
        "ALLOWED_DOMAINS": "huggingface.co"
      },
      "description": "HuggingFace (datasets, transformers, trl, peft) documentation"
    },

    "unsloth-docs": {
      "command": "uvx",
      "args": ["mcp-server-fetch"],
      "env": {
        "ALLOWED_DOMAINS": "unsloth.ai,github.com/unslothai"
      },
      "description": "Unsloth fine-tuning documentation"
    },

    "vllm-docs": {
      "command": "uvx",
      "args": ["mcp-server-fetch"],
      "env": {
        "ALLOWED_DOMAINS": "docs.vllm.ai"
      },
      "description": "vLLM inference engine documentation"
    },

    "ollama-docs": {
      "command": "uvx",
      "args": ["mcp-server-fetch"],
      "env": {
        "ALLOWED_DOMAINS": "ollama.com,github.com/ollama"
      },
      "description": "Ollama local LLM documentation"
    },

    "openai-docs": {
      "command": "uvx",
      "args": ["mcp-server-fetch"],
      "env": {
        "ALLOWED_DOMAINS": "platform.openai.com/docs"
      },
      "description": "OpenAI GPT models documentation"
    },

    "meta-llama-docs": {
      "command": "uvx",
      "args": ["mcp-server-fetch"],
      "env": {
        "ALLOWED_DOMAINS": "llama.meta.com,ai.meta.com,github.com/meta-llama"
      },
      "description": "Meta Llama models documentation"
    },

    "anthropic-docs": {
      "command": "uvx",
      "args": ["mcp-server-fetch"],
      "env": {
        "ALLOWED_DOMAINS": "docs.anthropic.com,anthropic.com"
      },
      "description": "Claude Agent SDK and Anthropic API documentation"
    },

    "openai-codex-docs": {
      "command": "uvx",
      "args": ["mcp-server-fetch"],
      "env": {
        "ALLOWED_DOMAINS": "developers.openai.com/codex/cli"
      },
      "description": "OpenAI Codex documentation"
    },

    "langchain-docs": {
      "command": "uvx",
      "args": ["mcp-server-fetch"],
      "env": {
        "ALLOWED_DOMAINS": "python.langchain.com,js.langchain.com,langchain.com"
      },
      "description": "LangChain and LangGraph documentation"
    },

    "microsoft-agent-docs": {
      "command": "uvx",
      "args": ["mcp-server-fetch"],
      "env": {
        "ALLOWED_DOMAINS": "learn.microsoft.com,github.com/microsoft/agent-framework"
      },
      "description": "Microsoft AutoGen agent framework documentation"
    },

    "temporal-docs": {
      "command": "uvx",
      "args": ["mcp-server-fetch"],
      "env": {
        "ALLOWED_DOMAINS": "docs.temporal.io,temporal.io"
      },
      "description": "Temporal.io workflow engine documentation"
    }
  }
}
```
