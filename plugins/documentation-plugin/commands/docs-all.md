---
description: Generate complete documentation suite
---

# Generate Complete Documentation Suite

Generate complete documentation suite: $ARGUMENTS

## Arguments

- **options** (optional): Space-separated flags
  - `--skip-readme` - Skip README generation
  - `--skip-api` - Skip API docs
  - `--skip-arch` - Skip architecture docs
  - `--skip-changelog` - Skip changelog
  - `--skip-contributing` - Skip contributing guide
  - `--force` - Overwrite existing files

## Examples

- `/docs-all` - Generate all documentation
- `/docs-all --skip-readme` - All except README
- `/docs-all --force` - Regenerate everything, overwriting existing files
- `/docs-all --skip-readme --skip-changelog` - Skip multiple docs

## Task

You are tasked with generating a complete documentation suite for the project.

### Argument Parsing

Parse $ARGUMENTS to extract flags:
- Check for `--skip-readme`, `--skip-api`, `--skip-arch`, `--skip-changelog`, `--skip-contributing`
- Check for `--force` to determine if existing files should be overwritten

Default behavior (no flags):
- Generate all documentation
- Skip files that already exist (unless `--force` is specified)

## Documentation Suite

Generate the following documentation in order:

### 1. README.md (unless --skip-readme)

Invoke `/readme` command or readme-generator agent to create:
- Comprehensive README.md
- Project overview and features
- Installation instructions
- Usage examples
- Links to other documentation

### 2. CHANGELOG.md (unless --skip-changelog)

Invoke `/changelog` command to create:
- CHANGELOG.md following Keep a Changelog format
- Version history from git commits
- Categorized changes (Added, Changed, Fixed, etc.)

### 3. CONTRIBUTING.md (unless --skip-contributing)

Invoke `/contributing` command to create:
- Contributing guidelines
- Development setup instructions
- Code standards and conventions
- Pull request process

### 4. Architecture Documentation (unless --skip-arch)

Invoke `/arch-doc` command to create:
- `docs/architecture/README.md` - Overview
- `docs/architecture/components.md` - Component details
- `docs/architecture/data-architecture.md` - Data models
- `docs/architecture/infrastructure.md` - Deployment
- `docs/architecture/security.md` - Security architecture
- `docs/architecture/decisions/` - ADR directory

### 5. API Documentation (unless --skip-api)

Invoke `/api-docs` command to create:
- `docs/api/README.md` - API overview
- `docs/api/endpoints.md` - REST endpoints (if applicable)
- `docs/api/schema.md` - GraphQL schema (if applicable)
- `docs/api/authentication.md` - Auth guide
- `docs/api/errors.md` - Error codes
- `openapi.yaml` - OpenAPI spec (REST)
- `postman_collection.json` - Postman collection

### 6. Documentation Templates

Create templates in `templates/` directory:
- `templates/ADR-template.md` - Architecture Decision Record
- `templates/PR-template.md` - Pull Request template
- `templates/ISSUE-template.md` - Issue template

### 7. Table of Contents

Generate master `docs/README.md` with links to all documentation:

```markdown
# Documentation

## Project Documentation

- [README](../README.md) - Project overview and quick start
- [CHANGELOG](../CHANGELOG.md) - Version history
- [CONTRIBUTING](../CONTRIBUTING.md) - Contribution guidelines

## Architecture

- [Architecture Overview](./architecture/README.md)
- [Components](./architecture/components.md)
- [Data Architecture](./architecture/data-architecture.md)
- [Infrastructure](./architecture/infrastructure.md)
- [Security](./architecture/security.md)
- [Architecture Decisions](./architecture/decisions/)

## API

- [API Overview](./api/README.md)
- [Authentication](./api/authentication.md)
- [Endpoints](./api/endpoints.md)
- [Errors](./api/errors.md)
```

## Workflow

Execute in order:

1. **Pre-check**: Verify which files already exist
2. **README**: Generate if missing or `--force`
3. **CHANGELOG**: Generate if missing or `--force`
4. **CONTRIBUTING**: Generate if missing or `--force`
5. **Architecture**: Generate if missing or `--force`
6. **API**: Generate if missing or `--force` and API detected
7. **Templates**: Create standard templates
8. **TOC**: Generate master documentation index
9. **Cross-link**: Update links between documents

## Cross-Linking

Ensure all documentation is properly linked:
- README links to CONTRIBUTING
- README links to docs/
- Architecture docs link to each other
- API docs reference architecture
- CONTRIBUTING references testing docs

## Progress Reporting

Report progress as files are generated:

```
✓ Generated README.md
✓ Generated CHANGELOG.md
✓ Generated CONTRIBUTING.md
✓ Generated docs/architecture/README.md
✓ Generated docs/architecture/components.md
✓ Generated docs/api/README.md
✓ Generated docs/api/endpoints.md
⊙ Skipped docs/architecture/data-architecture.md (already exists, use --force to overwrite)
✓ Generated docs/README.md (master index)

Documentation suite complete! 8 files generated, 1 skipped.
```

## Validation

After generation:
- Verify all internal links work
- Check for missing sections
- Ensure consistent formatting
- Validate code examples compile/run

## Output

Generate complete documentation suite with:
- All documentation files
- Proper directory structure
- Cross-referenced links
- Table of contents
- Templates for future contributions

Summary of created files at the end.
