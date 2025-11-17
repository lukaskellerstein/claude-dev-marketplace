# Contributing to Project Name

Thank you for considering contributing to Project Name! We welcome contributions from the community.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Commit Message Guidelines](#commit-message-guidelines)
- [Pull Request Process](#pull-request-process)
- [Testing Guidelines](#testing-guidelines)
- [Documentation Guidelines](#documentation-guidelines)

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

### Our Standards

- Be respectful and inclusive
- Accept constructive criticism gracefully
- Focus on what is best for the community
- Show empathy towards other community members

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates.

**When creating a bug report, include:**

- **Clear title and description**
- **Steps to reproduce** the issue
- **Expected behavior** vs **actual behavior**
- **Screenshots** if applicable
- **Environment details** (OS, version, browser, etc.)
- **Error messages** or logs

**Bug report template:**

```markdown
**Describe the bug**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '...'
3. See error

**Expected behavior**
What you expected to happen.

**Screenshots**
If applicable, add screenshots.

**Environment:**
 - OS: [e.g., Ubuntu 22.04]
 - Version: [e.g., 1.2.3]
 - Browser: [e.g., Chrome 120]

**Additional context**
Any other relevant information.
```

### Suggesting Features

Feature suggestions are welcome! Please provide:

- **Clear use case**: Why is this feature needed?
- **Proposed solution**: How should it work?
- **Alternatives considered**: What other approaches did you think of?
- **Additional context**: Any examples or mockups

### Submitting Pull Requests

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write or update tests
5. Update documentation
6. Submit a pull request

## Development Setup

### Prerequisites

- Node.js >= 18.0.0
- npm >= 9.0.0
- Git

### Setup Steps

```bash
# Fork and clone the repository
git clone https://github.com/YOUR-USERNAME/project-name.git
cd project-name

# Add upstream remote
git remote add upstream https://github.com/original/project-name.git

# Install dependencies
npm install

# Create a branch for your feature
git checkout -b feature/your-feature-name

# Run development server
npm run dev
```

### Keeping Your Fork Updated

```bash
git fetch upstream
git checkout main
git merge upstream/main
git push origin main
```

## Coding Standards

### Code Style

We use ESLint and Prettier for code formatting.

```bash
# Run linter
npm run lint

# Fix linting issues
npm run lint:fix

# Format code
npm run format
```

### Best Practices

- **SOLID Principles**: Follow SOLID design patterns
- **DRY**: Don't Repeat Yourself
- **KISS**: Keep It Simple, Stupid
- **Clean Code**: Write self-documenting code
- **Type Safety**: Use TypeScript types properly

### Code Review Checklist

- [ ] Code follows project style guidelines
- [ ] No commented-out code
- [ ] No console.log statements (use proper logging)
- [ ] Functions are small and focused
- [ ] No code duplication
- [ ] Proper error handling
- [ ] Type safety maintained
- [ ] Tests written and passing

## Commit Message Guidelines

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification.

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting, semicolons, etc.)
- **refactor**: Code refactoring
- **perf**: Performance improvements
- **test**: Adding or updating tests
- **chore**: Maintenance tasks

### Examples

```bash
feat(api): add user authentication endpoint

Implement JWT-based authentication for the API.

Closes #123
```

```bash
fix(parser): correct date parsing in timezone conversion

Fixed issue where dates were incorrectly parsed when timezone
offset was negative.

Fixes #456
```

### Breaking Changes

For breaking changes, add `BREAKING CHANGE:` in the footer:

```bash
feat(api): change user endpoint response format

BREAKING CHANGE: User endpoint now returns nested object structure
instead of flat structure. Update client code accordingly.
```

## Pull Request Process

### Before Submitting

1. **Update documentation**: README, API docs, etc.
2. **Add tests**: Ensure tests cover your changes
3. **Run tests**: All tests must pass
4. **Update CHANGELOG**: Add entry to [Unreleased] section
5. **Check code style**: Run linter and formatter
6. **Rebase if needed**: Ensure clean commit history

### PR Template

```markdown
## Description

Brief description of changes and why they're needed.

## Type of Change

- [ ] Bug fix (non-breaking change fixing an issue)
- [ ] New feature (non-breaking change adding functionality)
- [ ] Breaking change (fix or feature causing existing functionality to change)
- [ ] Documentation update

## Testing

- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] All tests passing

## Checklist

- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] No new warnings generated
- [ ] Tests added and passing
- [ ] CHANGELOG updated

## Related Issues

Closes #(issue number)

## Screenshots (if applicable)

Add screenshots showing the changes.
```

### Review Process

1. **Automated checks**: CI/CD must pass
2. **Code review**: At least one approval required
3. **Testing**: Manual testing if applicable
4. **Approval**: Maintainer approval needed
5. **Merge**: Squash and merge into main

## Testing Guidelines

### Writing Tests

```javascript
describe('FeatureName', () => {
  test('should do something correctly', () => {
    // Arrange
    const input = 'test';

    // Act
    const result = functionUnderTest(input);

    // Assert
    expect(result).toBe(expected);
  });
});
```

### Test Coverage

- Maintain >= 80% code coverage
- Test edge cases and error conditions
- Write unit tests for utilities
- Write integration tests for APIs
- Write E2E tests for critical flows

### Running Tests

```bash
# Run all tests
npm test

# Run with coverage
npm run test:coverage

# Run specific test
npm test path/to/test.spec.js

# Run in watch mode
npm run test:watch
```

## Documentation Guidelines

### Code Documentation

- Add JSDoc comments for public functions
- Include examples in documentation
- Document parameters and return values
- Explain complex algorithms

### Markdown Documentation

- Follow markdown best practices
- Use proper heading hierarchy
- Include code examples
- Keep documentation up-to-date

### API Documentation

- Document all endpoints
- Include request/response examples
- Document error responses
- Keep OpenAPI spec updated

## Release Process

Maintainers only:

1. Update version in `package.json`
2. Update `CHANGELOG.md`
3. Create release tag
4. Publish to npm/PyPI
5. Create GitHub release

## Questions?

- 💬 Discord: [Join our server](https://discord.gg/example)
- 📧 Email: dev@example.com
- 🐛 Issues: [GitHub Issues](https://github.com/username/project/issues)

## Recognition

Contributors will be recognized in:
- README.md
- Release notes
- Contributors page

Thank you for contributing! 🎉
