---
description: Review existing architecture for improvements and best practices
---

Conduct a comprehensive review of the existing architecture and provide recommendations for improvements.

## Process

1. **Codebase Analysis**: Analyze the current architecture by examining:
   - Service boundaries and responsibilities
   - Communication patterns
   - Data architecture
   - Deployment configuration
   - Documentation (README, CLAUDE.md, architecture docs)

2. **Launch Architecture Review**: Use multiple specialized agents in parallel:
   - `microservices-architect`: Review service boundaries, coupling, and DDD patterns
   - `cloud-patterns-expert`: Assess scalability, reliability, and cloud best practices
   - `event-sourcing-expert` (if applicable): Review event-driven patterns and messaging

3. **Identify Issues**: For each area, identify:
   - Anti-patterns and code smells
   - Scalability bottlenecks
   - Single points of failure
   - Security vulnerabilities
   - Cost optimization opportunities
   - Technical debt

4. **Prioritize Recommendations**: Rank findings by:
   - Impact (high, medium, low)
   - Effort (high, medium, low)
   - Risk if not addressed

## Output

Deliver a comprehensive architecture review report:

### Current State
- Architecture overview with diagrams
- Technology stack
- Identified patterns and conventions

### Findings
For each issue found:
- **Description**: What is the problem?
- **Impact**: How does it affect the system?
- **Evidence**: Specific file:line references
- **Severity**: Critical/High/Medium/Low

### Recommendations
For each recommendation:
- **Improvement**: What should be changed?
- **Rationale**: Why is this better?
- **Implementation**: Step-by-step approach
- **Trade-offs**: What are the costs/risks?
- **Priority**: Impact/Effort matrix

### Roadmap
- Quick wins (low effort, high impact)
- Strategic improvements (high effort, high impact)
- Long-term optimizations

Use diagrams to illustrate current vs proposed architecture. Cite specific files and line numbers for all findings.
