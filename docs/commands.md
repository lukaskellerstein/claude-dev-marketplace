# Claude Code Custom Commands Guide

## Overview

Custom slash commands in Claude Code are Markdown files that define reusable prompts and workflows. They allow you to automate repetitive tasks and standardize team workflows.

## Basic Structure

### Simple Command (No Frontmatter)

**File:** `./commands/optimize.md`

```markdown
Analyze this code for performance issues and suggest optimizations:
```

Usage: `/optimize`

### Command with Frontmatter (Recommended)

**File:** `./commands/security-review.md`

```markdown
---
description: Review this code for security vulnerabilities
disable-model-invocation: false
---

# Security Review

Review the provided code for:

- SQL injection vulnerabilities
- XSS risks
- Authentication issues
- Data exposure problems
- Insecure dependencies

Provide actionable recommendations for each issue found.
```

Usage: `/security-review`

## Namespaced Commands

Organize commands in subdirectories for better structure:

**File:** `./commands/dev/code-review.md`

```markdown
---
description: Perform comprehensive code review
---

# Code Review

You are the Code Review Coordinator directing four review specialists:

1. **Quality Auditor** – examines code quality, readability, and maintainability
2. **Security Analyst** – identifies vulnerabilities and security best practices
3. **Performance Reviewer** – evaluates efficiency and optimization opportunities
4. **Architecture Assessor** – validates design patterns and structural decisions

## Process

1. **Code Examination**: Systematically analyze target code sections and dependencies
2. **Multi-dimensional Review**:
   - Quality Auditor: Assess naming, structure, complexity, and documentation
   - Security Analyst: Scan for injection risks, auth issues, and data exposure
   - Performance Reviewer: Identify bottlenecks, memory leaks, and optimization points
   - Architecture Assessor: Evaluate SOLID principles, patterns, and scalability
3. **Synthesis**: Compile findings with prioritized recommendations
4. **Actionable Output**: Provide specific code improvements

## Output Format

- Critical Issues (must fix)
- Recommendations (should fix)
- Suggestions (nice to have)
- Positive Observations
```

Usage: `/dev:code-review`

## Commands with Arguments

Commands support `$ARGUMENTS` placeholder for dynamic input:

**File:** `./commands/fix-issue.md`

```markdown
---
description: Fix GitHub issue by number
---

# Fix GitHub Issue

Please analyze and fix GitHub issue: $ARGUMENTS

## Steps

1. Use `gh issue view $ARGUMENTS` to get issue details
2. Analyze the problem and root cause
3. Implement necessary changes
4. Create tests to verify the fix
5. Commit changes with conventional commit message
6. Create PR linking to the issue
```

Usage: `/fix-issue 123`

## Advanced Example: Git Commit Workflow

**File:** `./commands/commit.md`

```markdown
---
description: Create conventional commit and push changes
---

# Commit and Push Changes

Create a conventional commit with all current changes and push to the remote repository.

## Steps

1. Run `git status` to see all changes
2. Run `git diff` to review the changes
3. Analyze the changes and determine the appropriate conventional commit type:
   - `feat:` for new features
   - `fix:` for bug fixes
   - `docs:` for documentation changes
   - `style:` for formatting changes
   - `refactor:` for code refactoring
   - `test:` for test additions/changes
   - `chore:` for maintenance tasks
4. Stage all changes with `git add -A`
5. Create a conventional commit with a descriptive message
6. Push to the current branch with `git push`

## Rules

- Follow Conventional Commits specification
- Do NOT add co-authors to the commit message
- Ensure commit message is clear and descriptive
```

Usage: `/commit`

## Complex Multi-Step Command

**File:** `./commands/project/create-feature.md`

```markdown
---
description: Create complete feature implementation
---

# Create Feature

Create a complete feature implementation: $ARGUMENTS

## Your Role

You are the Feature Implementation Coordinator orchestrating four specialists:

1. **Architect Agent** – designs API contracts, data models, and component structure
2. **Implementation Engineer** – writes core functionality with proper error handling
3. **Integration Specialist** – ensures compatibility with existing systems
4. **Code Reviewer** – validates code quality, security, and performance

## Implementation Strategy

1. **Requirements Analysis**

   - Parse feature requirements from $ARGUMENTS
   - Identify dependencies and constraints
   - Define acceptance criteria

2. **Architecture Design**

   - Design API contracts and interfaces
   - Plan data models and schemas
   - Define component structure and relationships

3. **Progressive Development**

   - Build incrementally with validation at each step
   - Write comprehensive tests
   - Document as you build

4. **Quality Validation**
   - Run tests and verify functionality
   - Review code for maintainability
   - Check performance and security

## Output Format

1. **Implementation Plan** – technical approach with component breakdown
2. **Code Implementation** – complete, working code with comments
3. **Tests** – unit and integration tests
4. **Integration Guide** – steps to integrate with existing codebase
5. **Documentation** – API docs and usage examples
6. **Next Actions** – deployment steps and future enhancements
```

Usage: `/project:create-feature user-authentication`

## Testing Command Example

**File:** `./commands/test/generate-tests.md`

````markdown
---
description: Generate comprehensive test suite
---

# Generate Test Suite

Generate comprehensive tests for: $ARGUMENTS

## Test Coverage

Create tests covering:

1. **Unit Tests**

   - Test individual functions and methods
   - Mock external dependencies
   - Cover edge cases and error conditions

2. **Integration Tests**

   - Test component interactions
   - Verify data flow
   - Test API endpoints

3. **Edge Cases**
   - Null/undefined inputs
   - Empty strings and arrays
   - Boundary values
   - Invalid data types

## Test Structure

```javascript
describe("Feature Name", () => {
  describe("Unit Tests", () => {
    // Individual function tests
  });

  describe("Integration Tests", () => {
    // Component interaction tests
  });

  describe("Edge Cases", () => {
    // Boundary and error tests
  });
});
```
````

## Requirements

- Use the project's testing framework
- Follow existing test patterns
- Aim for >80% code coverage
- Include descriptive test names

````

Usage: `/test:generate-tests UserService`

## Frontmatter Options

```markdown
---
description: Brief description shown in /help (required for SlashCommand tool)
disable-model-invocation: true  # Prevents Claude from auto-invoking this command
---
````

### Key Frontmatter Fields:

- **`description`**: Required for the SlashCommand tool to work. Shows up in `/help` output
- **`disable-model-invocation`**: Set to `true` to prevent Claude from automatically invoking this command via the SlashCommand tool

## Integration with CLAUDE.md

Reference commands in your CLAUDE.md for natural language triggers:

```markdown
### Work Keywords

- **"commit my changes"**: Execute `/commit` command
- **"review this code"**: Execute `/dev:code-review` command
- **"run tests"**: Execute `/test:generate-tests` command
```

This allows users to say "commit my changes" and Claude will automatically execute `/commit`.

## Best Practices

1. **Use Descriptive Names**: Command names should clearly indicate their purpose
2. **Add Frontmatter**: Always include `description` field for better discoverability
3. **Namespace Commands**: Use subdirectories for organization (`dev/`, `test/`, `deploy/`)
4. **Document Arguments**: Clearly explain how to use `$ARGUMENTS` in your commands
5. **Structure Output**: Define clear output formats for consistency
6. **Chain Commands**: Design commands that work well together
7. **Keep It Simple**: Start with simple commands and add complexity as needed

## Example Command Library Structure

```
.claude/
└── commands/
    ├── README.md                    # Documentation for your commands
    ├── optimize.md                  # Quick performance check
    ├── commit.md                    # Git commit workflow
    ├── dev/
    │   ├── code-review.md          # Comprehensive review
    │   ├── refactor.md             # Refactoring suggestions
    │   └── debug.md                # Debugging assistance
    ├── test/
    │   ├── generate-tests.md       # Test generation
    │   ├── coverage.md             # Coverage analysis
    │   └── e2e.md                  # E2E test creation
    ├── project/
    │   ├── create-feature.md       # Feature implementation
    │   ├── architecture.md         # Architecture review
    │   └── api-design.md           # API design
    └── deploy/
        ├── prepare-release.md      # Release preparation
        ├── changelog.md            # Changelog generation
        └── rollback.md             # Rollback procedure
```
