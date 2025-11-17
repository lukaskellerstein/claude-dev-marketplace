# Agent Improvement Guide

## Why Your Agents Aren't Being Used

After analyzing the popular claude-code-marketplaces repository (20k stars), I've identified critical differences that prevent your agents from being invoked.

---

## 🔴 Critical Issues

### 1. **Missing Activation Triggers**

**Popular Marketplace Pattern:**
```yaml
description: Expert backend architect specializing in scalable API design, microservices
  architecture, and distributed systems. Masters REST/GraphQL/gRPC APIs,
  event-driven architectures, service mesh patterns...
  Use PROACTIVELY when creating new backend services or APIs.
```

**Your Current Pattern:**
```yaml
description: API design expert for REST, GraphQL, and gRPC architecture
```

**Problem:** Claude doesn't know WHEN to use your agent!

**Fix:** Every agent description MUST include:
- Clear expertise statement
- Specific technologies/domains mastered
- **"Use PROACTIVELY when..."** or **"Use IMMEDIATELY for..."** trigger clause

---

### 2. **Agent Content Too Shallow**

**Metrics Comparison:**

| Metric | Popular Marketplace | Your Repository | Required |
|--------|---------------------|-----------------|----------|
| **Agent Length** | 280-500+ lines | 50-150 lines | 250+ lines |
| **Capability Sections** | 15-25 sections | 2-5 sections | 15+ sections |
| **Technologies Listed** | 100+ specific tools | 20-30 tools | 80+ tools |
| **Behavioral Traits** | 8-12 traits | 0-2 traits | 8+ traits |
| **Example Interactions** | 5-15 examples | 0-3 examples | 8+ examples |
| **Response Methodology** | 7-12 steps | None | 7+ steps |

---

## 📋 Agent Structure Template

Based on successful agents from the popular marketplace, here's the required structure:

### **Frontmatter (YAML)**

```yaml
---
name: agent-name
description: |
  [Role statement] specializing in [domains]. Masters [technologies/patterns].
  [Additional expertise].
  Use PROACTIVELY when [specific trigger condition].
model: sonnet  # or haiku for fast execution tasks
---
```

### **Content Sections (Markdown)**

```markdown
You are [role with expertise level].

## Purpose
[2-3 sentences explaining core purpose and specialization domains]

## Core Philosophy
[3-5 sentences describing design principles and approach]

## Capabilities

### [Domain 1]
- **Specific Technology 1**: Description, use cases, patterns
- **Specific Technology 2**: Additional details
- **Pattern/Concept 3**: Implementation approaches
[... 8-15 items per section]

### [Domain 2]
[... repeat for 15-25 capability sections]

## Behavioral Traits
- Trait describing work style or quality standard
- Trait about prioritization or methodology
[... 8-12 total traits]

## Response Approach
1. **Step 1**: What to do first, expected outputs
2. **Step 2**: Next action, deliverables
[... 7-12 systematic steps]

## Example Interactions
- "Example prompt showing when to use this agent"
- "Another realistic use case"
[... 5-15 diverse examples]

## Key Distinctions
- vs [related-agent]: [boundary clarification]
- vs [another-agent]: [scope difference]
```

---

## 🔧 Specific Agent Fixes Needed

### **api-architect.md** → Needs Major Enhancement

**Current Issues:**
1. ❌ Description lacks "Use PROACTIVELY when..." trigger
2. ❌ Only 5 capability sections (need 15+)
3. ❌ No behavioral traits section
4. ❌ No response approach methodology
5. ❌ Only 3 example interactions (need 8+)
6. ❌ Missing key distinctions from other agents

**Required Changes:**

#### Update Description:
```yaml
---
name: api-architect
description: |
  Expert API architect specializing in REST, GraphQL, and gRPC design patterns.
  Masters OpenAPI/Swagger specifications, API versioning strategies, authentication
  patterns (OAuth, JWT, mTLS), and comprehensive API documentation. Handles API
  gateway configuration, rate limiting, caching strategies, and multi-protocol
  service design.
  Use PROACTIVELY when designing new APIs or refactoring existing API architecture.
model: sonnet
---
```

#### Add Missing Capability Sections:
- API Gateway & Load Balancing (Kong, AWS API Gateway, Azure APIM)
- Caching Strategies (Redis, Memcached, HTTP caching, ETags)
- Real-time Communication (WebSocket, Server-Sent Events, long polling)
- API Composition & Aggregation (BFF pattern, GraphQL stitching)
- Performance Optimization (pagination, batch endpoints, compression)
- Observability (API metrics, distributed tracing, logging)
- Contract Testing (Pact, consumer-driven contracts)
- SDK Generation (OpenAPI Generator, GraphQL Code Generator)
- API Lifecycle Management (deprecation, sunset headers, migration)
- Multi-tenancy Patterns (tenant isolation, per-tenant configs)

#### Add Behavioral Traits Section:
```markdown
## Behavioral Traits
- Follows OpenAPI 3.0+ specifications for REST API documentation
- Prioritizes backward compatibility in versioning strategies
- Implements comprehensive error handling with RFC 7807 Problem Details
- Uses semantic HTTP status codes consistently
- Designs for idempotency in POST/PUT/PATCH operations
- Enforces consistent naming conventions (kebab-case for endpoints)
- Implements proper CORS and security headers
- Focuses on developer experience with clear documentation
- Validates API contracts with schema-based testing
- Monitors API performance with SLIs/SLOs
```

#### Add Response Approach Section:
```markdown
## Response Approach
1. **Understand requirements**: Business domain, client types (web/mobile/3rd-party),
   expected scale, latency requirements, data consistency needs
2. **Select API protocol**: REST for CRUD, GraphQL for flexible queries, gRPC for
   high-performance microservices, WebSocket for real-time
3. **Design resource model**: Domain entities, relationships, aggregates, URI structure
4. **Define API contract**: OpenAPI/GraphQL schema, request/response models,
   error formats
5. **Plan versioning strategy**: URL versioning, header versioning, sunset policies
6. **Design authentication**: OAuth flows, JWT structure, refresh token rotation,
   API key management
7. **Implement resilience patterns**: Rate limiting, retry logic, circuit breakers,
   timeout configuration
8. **Add observability**: Request logging, metrics (latency, error rate), distributed
   tracing
9. **Document thoroughly**: Interactive documentation (Swagger UI), code examples,
   authentication guides
10. **Plan testing strategy**: Contract tests, integration tests, load tests,
    security tests
```

#### Add Example Interactions Section:
```markdown
## Example Interactions
- "Design a RESTful API for an e-commerce order management system"
- "Create an OpenAPI 3.0 specification for a multi-tenant SaaS platform"
- "Design a GraphQL API with subscriptions for real-time chat"
- "Plan API versioning strategy for backward-incompatible changes"
- "Implement OAuth 2.0 with PKCE for a mobile application"
- "Design API gateway configuration with rate limiting and caching"
- "Create gRPC service definitions for microservices communication"
- "Implement webhook delivery system with retry logic"
- "Design API contract testing strategy with Pact"
- "Plan API deprecation and migration strategy"
```

#### Add Key Distinctions Section:
```markdown
## Key Distinctions
- vs backend-architect: Focuses on API design and contracts; defers overall
  service architecture to backend-architect
- vs security-auditor: Designs API security patterns; defers security audits
  to security-auditor
- vs database-architect: Designs API data models; defers database schema
  to database-architect
```

---

## 🎯 Agent Activation Formula

For Claude to use your agents, they need:

### **1. Clear Triggers (Required)**
```yaml
# Good examples from popular marketplace:
"Use PROACTIVELY when creating new backend services or APIs"
"Use IMMEDIATELY for production incidents or outages"
"Use when building async APIs or concurrent systems"
"Use for greenfield database design or major schema changes"
"Use when deploying infrastructure or managing cloud resources"
```

### **2. Comprehensive Capabilities (Required)**
- **15-25 capability subsections** (not 2-5)
- **Each subsection: 8-15 specific technologies/patterns**
- **Total: 100+ specific tools/frameworks mentioned**

### **3. Behavioral Identity (Required)**
- **8-12 behavioral traits** defining work style
- Mix of technical standards and soft priorities
- Shows personality and quality expectations

### **4. Systematic Methodology (Required)**
- **7-12 numbered steps** showing approach
- Each step has clear inputs/outputs
- Progressive problem-solving workflow

### **5. Realistic Examples (Required)**
- **8-15 example prompts** showing usage
- Diverse use cases demonstrating range
- Real-world scenarios users recognize

---

## 📊 Model Selection Strategy

**Use `model: sonnet` when:**
- Designing architecture (backend-architect, database-architect, api-architect)
- Making technology selection decisions
- Performing security reviews or audits
- Handling complex language-specific expertise (python-specialist, golang-specialist)
- Orchestrating multi-step workflows
- Making business-critical decisions

**Use `model: haiku` when:**
- Generating code from well-defined specifications
- Creating tests following established patterns
- Writing documentation with clear templates
- Executing infrastructure operations
- Performing deterministic tasks
- Need fast execution for simple tasks

**Your Current Issues:**
- api-architect uses `model: opus` → Should be `sonnet`
- Most agents use default → Should explicitly specify `sonnet` or `haiku`

---

## ✅ Quick Wins (Do These First)

### **Priority 1: Fix All Agent Descriptions**

Update every agent's frontmatter description to include:
1. Clear role statement with expertise level
2. Specific technologies/domains mastered
3. **"Use PROACTIVELY when [trigger]"** clause
4. Explicit model assignment (`sonnet` or `haiku`)

### **Priority 2: Expand Capability Sections**

For each agent, expand from 2-5 sections to 15-25 sections:
- Research similar agents in popular marketplace
- List 8-15 specific technologies per section
- Include frameworks, tools, patterns, methodologies
- Be concrete (name specific tools, not generic concepts)

### **Priority 3: Add Missing Sections**

Add to every agent:
- **Behavioral Traits** (8-12 items)
- **Response Approach** (7-12 steps)
- **Example Interactions** (8-15 prompts)

### **Priority 4: Optimize Model Assignment**

Review every agent and assign appropriate model:
- Complex reasoning/architecture → `sonnet`
- Fast execution/code generation → `haiku`
- Default → `sonnet` (when unsure)

---

## 📈 Success Metrics

**After implementing these changes, you should see:**

| Metric | Before | After | Target |
|--------|--------|-------|--------|
| Agent invocations per session | 0-1 | 3-8 | 5+ |
| User satisfaction | Low | High | High |
| Agent description length | 20-50 chars | 200-400 chars | 300+ chars |
| Capability sections | 2-5 | 15-25 | 15+ |
| Example interactions | 0-3 | 8-15 | 10+ |
| Total agent content | 50-150 lines | 250-500 lines | 300+ lines |

---

## 🔗 Reference: Complete Agent Example

See `/home/lukas/Projects/Temp/claude-code-marketplaces/agents/plugins/backend-development/agents/backend-architect.md` for a complete example of a well-structured agent.

**Key characteristics of this agent:**
- ✅ 355 lines of content
- ✅ "Use PROACTIVELY when..." trigger in description
- ✅ 20 capability subsections
- ✅ 100+ specific technologies mentioned
- ✅ 10 behavioral traits
- ✅ 10-step response approach
- ✅ Clear key distinctions from related agents
- ✅ Explicit `model: sonnet` assignment

**This is the quality bar your agents need to meet.**

---

## 🚀 Next Steps

1. **Apply fixes to api-architect.md first** (use as template for others)
2. **Test with Claude Code** - create a new API and see if api-architect is invoked
3. **Iterate on remaining agents** using the same pattern
4. **Monitor agent usage** and refine triggers based on actual usage
5. **Expand capability sections** based on user feedback

---

## ❓ Common Questions

**Q: Why do descriptions need to be so long?**
A: Claude needs context to understand WHEN to invoke your agent. Generic descriptions like "API design expert" could apply to many situations, so Claude ignores them. Specific triggers like "Use PROACTIVELY when creating new backend services or APIs" give clear activation criteria.

**Q: Do I really need 15+ capability sections?**
A: Yes. This shows Claude the breadth and depth of the agent's expertise. Without comprehensive capabilities, Claude assumes the agent has limited knowledge and won't use it for complex tasks.

**Q: What if my agent is intentionally narrow in scope?**
A: Even narrow agents need detailed capabilities. Example: A "dockerfile-expert" might be narrow, but should still have 10+ sections covering: multi-stage builds, layer optimization, security scanning, base image selection, build arguments, health checks, entrypoint patterns, volume management, network configuration, compose integration, etc.

**Q: Can I use tools other than Read, Write, Edit, Grep, Glob?**
A: Yes! Look at popular marketplace agents - they use Bash, Task, WebFetch, and other tools. The `tools` field can list any available tools, or omit it to inherit all tools.

---

**Remember:** Claude is VERY selective about which agents to invoke. Only agents with:
- Clear activation triggers
- Comprehensive capabilities
- Professional structure
- Realistic examples

...will be used regularly. Your agents need to compete for Claude's attention!
