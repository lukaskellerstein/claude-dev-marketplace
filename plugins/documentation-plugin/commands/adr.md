---
description: Create Architecture Decision Record
---

# Create Architecture Decision Record

Create new Architecture Decision Record: $ARGUMENTS

## Arguments

- **decision-title** (required): Title of the architectural decision

## Examples

- `/adr Use PostgreSQL for primary database`
- `/adr Adopt microservices architecture`
- `/adr Implement event sourcing for order system`
- `/adr Switch to React for frontend framework`

## Task

You are tasked with creating a new Architecture Decision Record (ADR) following best practices.

### Argument Parsing

Parse $ARGUMENTS to extract:
1. **Decision title** (required) - the full title of the decision

Validate that the title:
- Is not empty
- Is descriptive enough (minimum 3 words recommended)
- Doesn't duplicate an existing ADR title

## ADR Creation Process

### 1. Setup ADR Directory

Ensure the ADR directory structure exists:

```
docs/
└── architecture/
    └── decisions/
        ├── README.md (index of all ADRs)
        ├── ADR-001-initial-architecture.md
        ├── ADR-002-database-choice.md
        └── ...
```

Create directories if they don't exist.

### 2. Auto-Number the ADR

Scan existing ADRs to determine the next number:
- Find all ADR files matching pattern `ADR-\d+-.*.md`
- Extract the highest number
- Increment by 1 for the new ADR
- Format as zero-padded 3 digits (e.g., ADR-001, ADR-012, ADR-123)

### 3. Generate Filename

Create filename from title:
- Convert to lowercase
- Replace spaces with hyphens
- Remove special characters
- Keep alphanumeric and hyphens only

Example:
- Title: "Use PostgreSQL for primary database"
- Number: 5
- Filename: `ADR-005-use-postgresql-for-primary-database.md`

### 4. Load ADR Template

Use the template from `templates/ADR-template.md` as the base structure.

Standard ADR template:

```markdown
# ADR-XXX: [Decision Title]

## Status

[Proposed | Accepted | Deprecated | Superseded]

## Context

What is the issue that we're seeing that is motivating this decision or change?

## Decision

What is the change that we're proposing and/or doing?

## Consequences

### Positive

- Consequence 1
- Consequence 2

### Negative

- Consequence 1
- Consequence 2

## Alternatives Considered

### Alternative 1

**Pros:**
- Pro 1
- Pro 2

**Cons:**
- Con 1
- Con 2

**Decision:** [Why this was rejected]

### Alternative 2

...

## References

- [Link 1](url)
- [Link 2](url)
```

### 5. Populate Initial Content

Fill in known information:
- ADR number
- Decision title
- Status: "Proposed" (default for new ADRs)
- Current date

Leave placeholders for:
- Context (with guidance)
- Decision details
- Consequences
- Alternatives

### 6. Add Contextual Prompts

Include helpful prompts in the ADR:

```markdown
## Context

<!-- Describe the context and problem:
- What is the current situation?
- What problem are we trying to solve?
- What are the constraints?
- What are the requirements?
-->

## Decision

<!-- Describe the decision:
- What are we going to do?
- How will it work?
- What are the key aspects of this decision?
-->
```

### 7. Link to Related ADRs

Scan existing ADRs for potential relationships:
- Check for similar topics or technologies
- Identify superseded ADRs
- Find dependent or related decisions

Add references section if related ADRs found:

```markdown
## Related ADRs

- [ADR-003: Database Selection](./ADR-003-database-selection.md) - Related decision
- Supersedes [ADR-001: Initial Data Storage](./ADR-001-initial-data-storage.md)
```

### 8. Update ADR Index

Update `docs/architecture/decisions/README.md` to include the new ADR:

```markdown
# Architecture Decision Records

## Index

- [ADR-001: Initial Architecture](./ADR-001-initial-architecture.md) - Accepted
- [ADR-002: API Design](./ADR-002-api-design.md) - Accepted
- [ADR-005: Use PostgreSQL](./ADR-005-use-postgresql-for-primary-database.md) - Proposed ← NEW
```

## Interactive Prompts

After creating the ADR file, prompt the user to fill in key sections:

```
ADR created: docs/architecture/decisions/ADR-005-use-postgresql-for-primary-database.md

Let's fill in the key details:

1. Context - What problem does this solve?
   [User input or "Skip to edit manually"]

2. What alternatives did you consider?
   [User input: comma-separated list or "Skip"]

3. Why was this chosen over alternatives?
   [User input or "Skip"]

Would you like me to:
1. Open the file for manual editing
2. Fill in more details interactively
3. Complete as-is (you can edit later)
```

## Best Practices

Follow ADR best practices:

- **Be specific**: Avoid vague language
- **Explain the "why"**: Context is more important than the "what"
- **Document alternatives**: Show what was considered
- **Capture consequences**: Both positive and negative
- **Link to related ADRs**: Build a knowledge graph
- **Update status**: As the decision evolves
- **Keep it concise**: One ADR per decision

## Status Lifecycle

```
Proposed → Accepted → [Deprecated | Superseded]
         ↓
      Rejected
```

- **Proposed**: Initial state, under consideration
- **Accepted**: Decision approved and being implemented
- **Deprecated**: No longer recommended, but not superseded
- **Superseded**: Replaced by a newer ADR (link to it)
- **Rejected**: Proposed but not accepted

## Output

Generate:
1. New ADR file with template and initial content
2. Updated ADR index
3. Open file for editing (optional)
4. Summary of created ADR

Example output:

```
✓ Created ADR-005: Use PostgreSQL for primary database

File: docs/architecture/decisions/ADR-005-use-postgresql-for-primary-database.md
Status: Proposed
Related ADRs: ADR-003 (Database Selection)

Next steps:
1. Fill in the Context section
2. Add alternatives considered
3. Document consequences
4. Get team review
5. Update status to "Accepted" when approved
```
