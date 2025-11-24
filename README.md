# Claude Code Marketplace

A comprehensive marketplace of production-ready Claude Code plugins for modern software development. This marketplace provides 12 specialized plugins covering architecture, frontend, backend, databases, infrastructure, AI/ML, security, performance, testing, and more.

## 🎯 Overview

This marketplace contains **12 plugins** with **125+ files** and **1.7MB** of expert knowledge, covering the entire software development lifecycle.

## 📦 Plugins

### Architecture & Design

#### 🏛️ Architecture Plugin
**Path:** `./plugins/architecture-plugin`

Design and review software architectures with microservices, cloud patterns, and event-driven systems.

**Agents:**
- `microservices-architect` - DDD, service boundaries, data management
- `cloud-patterns-expert` - Cloud-native patterns, scalability, reliability
- `event-sourcing-expert` - Event sourcing, CQRS, message brokers

**Commands:**
- `/design-microservices` - Design comprehensive microservices architecture
- `/review-architecture` - Review existing architecture with improvements

**Skills:**
- `ddd-patterns` - Auto-invokes for proper DDD patterns

**Coverage:** Microservices, DDD, Event Sourcing, CQRS, Saga Pattern, Cloud Patterns

---

### Frontend Development

#### ⚛️ Frontend Plugin
**Path:** `./plugins/frontend-plugin`

Build modern React applications with TypeScript, Tailwind CSS, shadcn-ui, and Radix UI.

**Agents:**
- `react-expert` - React 18+, TypeScript, hooks, state management
- `css-tailwind-expert` - CSS, SCSS, Tailwind, shadcn-ui, Radix UI
- `responsive-design-expert` - Mobile-first, responsive, cross-device

**Commands:**
- `/build-component` - Build production-ready React components
- `/create-design-system` - Create/enhance design systems
- `/audit-frontend` - Comprehensive frontend audits

**Skills:**
- `accessibility-checker` - WCAG 2.1 compliance
- `performance-optimizer` - React performance optimization

**MCP Integration:** shadcn-ui MCP server

**Coverage:** React, TypeScript, Tailwind CSS, shadcn-ui, Radix UI, Responsive Design

---

### Backend Development

#### 🔧 Backend Plugin
**Path:** `./plugins/backend-plugin`

Build robust APIs and real-time systems with REST, GraphQL, gRPC, WebSocket, and message brokers.

**Agents:**
- `api-designer` - REST, GraphQL, gRPC expert
- `message-broker-expert` - NATS, RabbitMQ, Kafka, Redis
- `realtime-communication-expert` - WebSocket, SSE, Socket.IO

**Commands:**
- `/design-api` - Design comprehensive APIs
- `/setup-messaging` - Setup message broker integrations
- `/implement-realtime` - Implement real-time communication

**Skills:**
- `api-best-practices` - API design best practices
- `message-patterns` - Messaging patterns (pub/sub, saga)

**Coverage:** REST, GraphQL, gRPC, WebSocket, NATS, RabbitMQ, Kafka, Redis

---

### Database Management

#### 🗄️ Database Plugin
**Path:** `./plugins/database-plugin`

Design and optimize databases across SQL, NoSQL, vector, and object storage.

**Agents:**
- `sql-database-expert` - PostgreSQL, Supabase
- `nosql-database-expert` - MongoDB, Redis, Elasticsearch, Qdrant, MinIO
- `data-modeling-expert` - Data modeling and architecture

**Commands:**
- `/design-database` - Design complete database schemas
- `/optimize-queries` - Analyze and optimize queries
- `/migrate-database` - Plan and execute migrations

**Skills:**
- `sql-best-practices` - SQL security and performance
- `database-indexing` - Indexing strategies

**Coverage:** PostgreSQL, Supabase, MongoDB, Redis, Elasticsearch, Qdrant, MinIO (S3)

---

### DevOps & Infrastructure

#### 🚀 CI/CD Plugin
**Path:** `./plugins/cicd-plugin`

Automate CI/CD pipelines, deployments, and release management.

**Agents:**
- `github-actions-expert` - GitHub Actions workflows
- `deployment-architect` - Deployment strategies, IaC
- `release-manager` - Versioning, changelog, releases

**Commands:**
- `/setup-github-actions` - Create CI/CD workflows
- `/design-deployment` - Design deployment strategy
- `/setup-release-workflow` - Automated release management

**Skills:**
- `cicd-best-practices` - GitHub Actions best practices
- `deployment-patterns` - Deployment strategies

**MCP Integration:** GitHub MCP server

**Coverage:** GitHub Actions, Deployment Strategies, Release Management, IaC

---

#### ☁️ Infrastructure Plugin
**Path:** `./plugins/infra-plugin`

Provision and manage cloud infrastructure with Google Cloud, Kubernetes, Docker, Terraform, and Helm.

**Agents:**
- `kubernetes-expert` - K8s orchestration and best practices
- `terraform-expert` - Infrastructure as Code
- `docker-expert` - Container optimization
- `gcloud-expert` - Google Cloud Platform

**Commands:**
- `/deploy-to-gke` - Deploy applications to GKE
- `/provision-infrastructure` - Provision infrastructure with Terraform
- `/containerize-app` - Containerize applications

**Skills:**
- `k8s-best-practices` - Kubernetes manifest best practices
- `terraform-patterns` - Terraform code patterns

**MCP Integration:** gcloud-mcp, terraform-mcp

**Coverage:** GCP, Kubernetes, Docker, Terraform, Helm

---

### AI & Machine Learning

#### 🤖 AI Agent Plugin
**Path:** `./plugins/aiagent-plugin`

Build AI agent systems with Claude SDK, LangChain, LangGraph, Microsoft Agent Framework, and Temporal.io.

**Agents:**
- `agent-orchestration-expert` - Multi-agent systems
- `workflow-automation-expert` - Temporal.io workflows
- `langchain-expert` - LangChain and LangGraph
- `claude-agent-expert` - Claude Agent SDK

**Commands:**
- `/design-agent-system` - Design multi-agent systems
- `/implement-workflow` - Create durable workflows
- `/build-rag-system` - Build RAG systems

**Skills:**
- `agent-reliability` - Error handling and retries
- `agent-memory-patterns` - Memory management

**Coverage:** Claude Agent SDK, LangChain, LangGraph, Microsoft Agent Framework, Temporal.io

---

#### 🧠 LLM Plugin
**Path:** `./plugins/llm-plugin`

Train, fine-tune, and deploy large language models with PyTorch, HuggingFace, and modern tooling.

**Agents:**
- `llm-training-expert` - Train LLMs from scratch
- `llm-finetuning-expert` - PEFT, LoRA, QLoRA, Unsloth
- `llm-deployment-expert` - vLLM, Ollama, TGI
- `model-optimization-expert` - Quantization, pruning

**Commands:**
- `/train-model` - Complete training pipeline
- `/fine-tune-model` - Efficient fine-tuning
- `/deploy-model` - Production deployment

**Skills:**
- `training-best-practices` - Training stability
- `model-optimization` - Performance optimization

**Coverage:** PyTorch, HuggingFace, Unsloth, vLLM, Ollama, Llama, Mistral, GPT

---

### Quality & Documentation

#### 📚 Documentation Plugin
**Path:** `./plugins/documentation-plugin`

Generate, review, and score documentation including README, CHANGELOG, API docs, and architecture docs.

**Agents:**
- `technical-writer` - Technical writing expert
- `documentation-reviewer` - Quality assessment and scoring
- `changelog-maintainer` - CHANGELOG management
- `architecture-documenter` - Architecture docs and diagrams

**Commands:**
- `/generate-readme` - Generate comprehensive README
- `/update-changelog` - Update CHANGELOG.md
- `/document-architecture` - Create architecture docs
- `/review-docs` - Review documentation quality

**Skills:**
- `documentation-standards` - Markdown best practices
- `code-documentation` - Code comments and docstrings

**MCP Integration:** Mermaid MCP, Markitdown MCP

**Coverage:** README, CHANGELOG, API Docs, Architecture Docs, ADRs, Diagrams

---

#### 🔒 Security Plugin
**Path:** `./plugins/security-plugin`

Audit security, scan vulnerabilities, and implement fixes following OWASP Top 10.

**Agents:**
- `security-auditor` - OWASP Top 10 audits
- `vulnerability-scanner` - Automated vulnerability scanning
- `secure-code-expert` - Secure coding implementations

**Commands:**
- `/security-audit` - Comprehensive security audit
- `/scan-vulnerabilities` - Automated vulnerability scanning
- `/fix-vulnerability` - Implement security fixes

**Skills:**
- `input-validation` - Injection prevention
- `secure-authentication` - Authentication best practices

**Coverage:** OWASP Top 10, Vulnerability Scanning, Secrets Detection, Secure Coding

---

#### ⚡ Performance Plugin
**Path:** `./plugins/performance-plugin`

Monitor, profile, and optimize application performance across frontend and backend.

**Agents:**
- `frontend-optimizer` - React, bundle size, Core Web Vitals
- `backend-profiler` - API, database, caching
- `memory-cpu-analyst` - Memory leaks, CPU profiling
- `load-testing-specialist` - k6, Artillery, capacity planning

**Commands:**
- `/performance-audit` - Comprehensive performance audit
- `/optimize-queries` - Database query optimization
- `/reduce-bundle` - Bundle size reduction

**Skills:**
- `prevent-n-plus-one` - N+1 query prevention
- `optimize-react-rendering` - React performance
- `efficient-caching` - Caching strategies

**Coverage:** Frontend Performance, Backend Performance, Memory/CPU Profiling, Load Testing

---

#### 🧪 Test Plugin
**Path:** `./plugins/test-plugin`

Generate tests, analyze coverage, and ensure testing quality across multiple frameworks.

**Agents:**
- `test-generator` - Generate unit, integration, E2E tests
- `coverage-analyzer` - Coverage analysis and reporting
- `test-quality-expert` - Test quality assessment

**Commands:**
- `/generate-tests` - Generate comprehensive test suites
- `/analyze-coverage` - Analyze test coverage
- `/assess-test-quality` - Assess test quality

**Skills:**
- `test-first-development` - TDD practices
- `test-maintainability` - Maintainable tests

**Coverage:** Jest, Vitest, pytest, JUnit, Coverage Analysis, Test Quality

---

## 🚀 Installation

### Install the Marketplace

```bash
# Clone the marketplace
git clone https://github.com/lukaskellerstein/claude-dev-marketplace.git

# Add marketplace to Claude Code
claude marketplace add ./claude-dev-marketplace
```

### Install Individual Plugins

```bash
# Install specific plugin
claude plugin install architecture-plugin
claude plugin install frontend-plugin
claude plugin install backend-plugin
# ... etc
```

## 📖 Usage

### Using Commands

```bash
# Architecture design
/design-microservices

# Frontend development
/build-component Button with loading state and variants

# Security audit
/security-audit

# Performance optimization
/performance-audit
```

### Invoking Agents Directly

```
Use microservices-architect to design service boundaries for user management

Use react-expert to optimize this component for performance

Use security-auditor to review authentication implementation
```

### Auto-Invoked Skills

Skills automatically activate when working in their domain:
- Writing domain models → `ddd-patterns` activates
- Creating React components → `accessibility-checker` activates
- Writing database queries → `sql-best-practices` activates
- Implementing authentication → `secure-authentication` activates

## 🎯 Coverage Matrix

| Domain | Plugin | Agents | Commands | Skills | MCP Servers |
|--------|--------|--------|----------|--------|-------------|
| Architecture | architecture-plugin | 3 | 2 | 1 | - |
| Frontend | frontend-plugin | 3 | 3 | 2 | shadcn |
| Backend | backend-plugin | 3 | 3 | 2 | - |
| Database | database-plugin | 3 | 3 | 2 | - |
| CI/CD | cicd-plugin | 3 | 3 | 2 | github |
| Infrastructure | infra-plugin | 4 | 3 | 2 | gcloud, terraform |
| AI Agents | aiagent-plugin | 4 | 3 | 2 | - |
| LLM | llm-plugin | 4 | 3 | 2 | - |
| Documentation | documentation-plugin | 4 | 4 | 2 | mermaid, markitdown |
| Security | security-plugin | 3 | 3 | 2 | - |
| Performance | performance-plugin | 4 | 3 | 3 | - |
| Testing | test-plugin | 3 | 3 | 2 | - |

**Total:** 41 Agents, 36 Commands, 24 Skills, 5 MCP Integrations

## 🏗️ Architecture

Each plugin follows a consistent structure:

```
plugin-name/
├── .claude-plugin/
│   └── plugin.json          # Plugin manifest
├── agents/                  # Specialized domain experts
│   ├── expert-1.md
│   ├── expert-2.md
│   └── expert-3.md
├── commands/                # User-facing commands
│   ├── command-1.md
│   └── command-2.md
├── skills/                  # Auto-invoked assistants
│   ├── skill-1.md
│   └── skill-2.md
└── README.md               # Plugin documentation
```

## 🤝 Contributing

Contributions are welcome! To add or improve plugins:

1. Follow the established plugin structure
2. Use Sonnet model for complex agents
3. Provide comprehensive documentation
4. Include real-world examples
5. Test commands and agents thoroughly

## 📄 License

MIT License - see LICENSE file for details

## 👤 Author

**Lukas Kellerstein**
- GitHub: [@lukaskellerstein](https://github.com/lukaskellerstein)

## 🙏 Acknowledgments

Built following official Claude Code plugin patterns and best practices from Anthropic.

## 📊 Stats

- **12 Plugins** covering the full development lifecycle
- **125+ Files** of expert knowledge
- **1.7MB** of production-ready content
- **41 Specialized Agents** with deep domain expertise
- **36 User Commands** for complex workflows
- **24 Auto-Invoked Skills** maintaining best practices
- **5 MCP Server Integrations** for extended capabilities

---

**Ready to supercharge your Claude Code experience!** 🚀
