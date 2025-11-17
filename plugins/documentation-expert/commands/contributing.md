---
description: Generate CONTRIBUTING.md file
---

# Generate CONTRIBUTING.md

Generate comprehensive CONTRIBUTING.md file for the current project.

## Task

You are tasked with generating a CONTRIBUTING.md file that provides clear guidelines for contributors.

## Analysis

1. **Analyze Project Structure and Tech Stack**:
   - Examine build tools and package managers
   - Identify testing frameworks
   - Detect linting and formatting tools
   - Check for CI/CD pipelines
   - Review existing contribution patterns

2. **Detect Project Practices**:
   - Commit message conventions (Conventional Commits, etc.)
   - Branch naming patterns
   - PR/MR workflow
   - Code review process

## Content to Generate

### 1. Welcome and Code of Conduct

```markdown
# Contributing to [Project Name]

First off, thank you for considering contributing to [Project Name]! It's people like you that make [Project Name] such a great tool.

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to [email].
```

### 2. How Can I Contribute?

Document different ways to contribute:
- Reporting bugs
- Suggesting enhancements
- Code contributions
- Documentation improvements
- Translations

### 3. Development Setup

Provide step-by-step setup instructions:

```markdown
## Development Setup

### Prerequisites

- Node.js >= 18.0.0
- npm >= 9.0.0
- Git

### Setup Steps

1. Fork the repository
2. Clone your fork:
   \`\`\`bash
   git clone https://github.com/YOUR_USERNAME/project-name.git
   cd project-name
   \`\`\`
3. Install dependencies:
   \`\`\`bash
   npm install
   \`\`\`
4. Create a branch:
   \`\`\`bash
   git checkout -b feature/your-feature-name
   \`\`\`
```

### 4. Development Workflow

```markdown
## Development Workflow

1. Make your changes
2. Write or update tests
3. Run tests: \`npm test\`
4. Run linter: \`npm run lint\`
5. Build project: \`npm run build\`
6. Commit your changes
7. Push to your fork
8. Create a pull request
```

### 5. Coding Standards

Define code style and conventions:
- Code formatting (Prettier, Black, etc.)
- Naming conventions
- File organization
- Comment style
- Testing requirements

### 6. Commit Message Conventions

```markdown
## Commit Messages

We follow [Conventional Commits](https://www.conventionalcommits.org/):

- \`feat:\` - New feature
- \`fix:\` - Bug fix
- \`docs:\` - Documentation changes
- \`style:\` - Code style changes (formatting)
- \`refactor:\` - Code refactoring
- \`test:\` - Test additions/changes
- \`chore:\` - Build process or auxiliary tool changes

Example:
\`\`\`
feat: add user authentication
fix: resolve memory leak in cache
docs: update API documentation
\`\`\`
```

### 7. Pull Request Process

```markdown
## Pull Request Process

1. Update the README.md with details of changes if applicable
2. Update the CHANGELOG.md following [Keep a Changelog](https://keepachangelog.com/)
3. Ensure all tests pass
4. Update documentation
5. Request review from maintainers
6. Address review feedback
7. PR will be merged once approved
```

### 8. Testing Requirements

Document testing expectations:
- Unit tests required for new features
- Integration tests for API changes
- E2E tests for critical workflows
- Minimum coverage requirements (e.g., 80%)

### 9. Documentation Requirements

```markdown
## Documentation

- Add JSDoc/docstring comments for public APIs
- Update README.md for user-facing changes
- Update API documentation for endpoint changes
- Add examples for new features
```

### 10. Issue Templates

Link to issue templates if they exist:
- Bug report template
- Feature request template
- Question template

### 11. Getting Help

```markdown
## Getting Help

- Check existing issues and pull requests
- Read the documentation
- Ask questions in Discussions
- Join our Discord/Slack community
- Email maintainers at [email]
```

## Best Practices

Follow standards from `DOCUMENTATION_STANDARDS.md`:

- Use clear, welcoming language
- Provide complete setup instructions
- Include examples
- Be specific about requirements
- Make it beginner-friendly
- Include troubleshooting tips

## Template

Use the template from `templates/CONTRIBUTING-template.md` as a base and customize for the specific project.

## Output

Generate CONTRIBUTING.md and save it to the project root.
