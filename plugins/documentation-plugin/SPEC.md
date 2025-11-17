# Documentation Generator Plugin - Component Specification

## Overview

Documentation plugin for generating README files, API docs, architecture diagrams, changelogs, and comprehensive project documentation with intelligent argument support and health scoring.

## Components

### Commands

#### 1. `/readme [project-type] [audience]`

**Purpose:** Generate comprehensive README.md
**Arguments:**

- `project-type` (optional): `library`, `cli-tool`, `web-app`, `api`, `mobile-app`, or `auto` (default)
- `audience` (optional): `developers`, `users`, or `both` (default)

**Examples:**

- `/readme` - Auto-detect project type
- `/readme library` - Generate library-focused README
- `/readme api developers` - API README for developers

**Behavior:**

- Analyze project structure
- Generate sections: Overview, Features, Installation, Usage, etc.
- Include badges (build status, coverage, etc.)
- Add code examples relevant to project type
- Include contributing guidelines link
- Tailor content to target audience

#### 2. `/changelog [version] [range]`

**Purpose:** Generate or update CHANGELOG.md
**Arguments:**

- `version` (optional): Version number (e.g., `1.2.0`) or `auto` (default)
- `range` (optional): Git range (e.g., `v1.0.0..HEAD`, `last-release..HEAD`) or `auto` (default)

**Examples:**

- `/changelog` - Since last release
- `/changelog 2.0.0` - For version 2.0.0
- `/changelog auto v1.0.0..HEAD` - Specific range

**Behavior:**

- Analyze git commits in specified range
- Group by type (feat, fix, docs, etc.)
- Follow Keep a Changelog format
- Suggest version bump (semver) if `auto`
- Generate release notes
- Detect breaking changes

#### 3. `/arch-doc [focus] [style]`

**Purpose:** Generate architecture documentation
**Arguments:**

- `focus` (optional): `overview`, `components`, `data`, `security`, `infrastructure`, or `all` (default)
- `style` (optional): `c4`, `uml`, or `simple` (default)

**Examples:**

- `/arch-doc` - Complete architecture docs
- `/arch-doc security` - Security architecture only
- `/arch-doc components c4` - Components using C4 model

**Behavior:**

- Analyze codebase structure
- Document system components
- Create architecture decision records (ADRs)
- Generate component diagrams (Mermaid)
- Document data flows
- Apply specified architectural style

#### 4. `/api-docs [api-type] [framework]`

**Purpose:** Generate API documentation
**Arguments:**

- `api-type` (optional): `rest`, `graphql`, `grpc`, or `all` (default: auto-detect)
- `framework` (optional): `express`, `fastapi`, `gin`, etc., or `auto` (default)

**Examples:**

- `/api-docs` - Auto-detect API type
- `/api-docs rest` - REST API only
- `/api-docs graphql fastapi` - GraphQL with FastAPI

**Behavior:**

- Extract API endpoints for specified type
- Generate request/response examples
- Document authentication
- Create Postman collection (REST)
- Generate OpenAPI spec (REST)
- Document GraphQL schema (GraphQL)
- Document Protocol Buffers (gRPC)

#### 5. `/contributing`

**Purpose:** Generate CONTRIBUTING.md file
**Behavior:**

- Analyze project structure and tech stack
- Generate code of conduct
- Document development setup
- Explain pull request process
- Define coding standards
- Specify testing requirements
- Include commit message conventions
- Link to issue templates

#### 6. `/docs-all [options]`

**Purpose:** Generate complete documentation suite
**Arguments:**

- `options` (optional): Space-separated flags
  - `--skip-readme` - Skip README generation
  - `--skip-api` - Skip API docs
  - `--skip-arch` - Skip architecture docs
  - `--skip-changelog` - Skip changelog
  - `--skip-contributing` - Skip contributing guide
  - `--force` - Overwrite existing files

**Examples:**

- `/docs-all` - Generate all docs
- `/docs-all --skip-readme` - All except README
- `/docs-all --force` - Regenerate everything

**Behavior:**

- Generate README.md
- Generate CHANGELOG.md
- Generate CONTRIBUTING.md
- Generate architecture docs
- Generate API docs
- Create documentation templates
- Generate table of contents
- Cross-link all documentation

#### 7. `/convert-doc <file-path>`

**Purpose:** Convert external documents to markdown
**Arguments:**

- `file-path` (required): Path to document file

**Supported formats:**

- Word (.docx)
- PDF (.pdf)
- PowerPoint (.pptx)
- Excel (.xlsx)
- HTML (.html)
- Images (with OCR)

**Examples:**

- `/convert-doc ./legacy/design-doc.docx`
- `/convert-doc ./specs/api.pdf`

**Behavior:**

- Uses MarkItDown MCP to convert file
- Preserves formatting when possible
- Converts images to markdown image references
- Converts tables to markdown tables
- Outputs converted content
- Optionally saves to file

#### 8. `/adr <decision-title>`

**Purpose:** Create Architecture Decision Record
**Arguments:**

- `decision-title` (required): Title of the architectural decision

**Examples:**

- `/adr Use PostgreSQL for primary database`
- `/adr Adopt microservices architecture`

**Behavior:**

- Create new ADR file in `docs/architecture/decisions/`
- Use ADR template from `templates/ADR-template.md`
- Auto-number ADR (ADR-001, ADR-002, etc.)
- Include decision context placeholder
- Prompt for alternatives considered
- Capture consequences (positive/negative)
- Link to related ADRs

#### 9. `/validate-docs`

**Purpose:** Validate documentation for errors and issues
**Behavior:**

- Check for broken links (internal & external)
- Verify images exist and are accessible
- Validate markdown syntax
- Test code examples (if possible)
- Check for outdated version numbers
- Verify consistent formatting
- Detect missing sections in README
- Check table of contents accuracy
- Verify cross-references
- Report issues with severity levels

#### 10. `/doc-health`

**Purpose:** Analyze documentation health and provide score
**Behavior:**

- Calculate documentation coverage score (0-100)
- Check README completeness
- Verify API documentation exists
- Check for architecture docs
- Verify changelog is up-to-date
- Check code documentation coverage
- Analyze markdown quality
- Check for broken links
- Verify examples are working
- Provide actionable recommendations
- Generate health report with metrics

### Agents

#### 1. `readme-generator`

**Purpose:** Create comprehensive README files tailored to project type and audience
**Capabilities:**

- Project analysis and type detection
- Feature extraction from code
- Installation instructions generation (multi-platform)
- Usage examples creation
- Badge suggestions (build, coverage, version, etc.)
- Table of contents generation
- Project type specialization (library, CLI, web app, API, mobile)
- Audience-targeted content (developers vs. users)
  **Invoked by:** `/readme` command
  **Usage:** When creating new project or updating README
  **Output:** Complete README.md file optimized for project type

#### 2. `api-documenter`

**Purpose:** Generate comprehensive API documentation for REST, GraphQL, and gRPC APIs
**Capabilities:**

- Endpoint documentation (all API types)
- Request/response schemas extraction
- Authentication documentation
- Error code documentation
- Rate limiting documentation
- Example generation (curl, Postman, code samples)
- OpenAPI spec generation (REST)
- GraphQL schema documentation
- Protocol Buffer documentation (gRPC)
- Postman collection generation
  **Invoked by:** `/api-docs` command
  **Usage:** When API is ready for documentation
  **Output:** Complete API documentation with specs

#### 3. `architecture-documenter`

**Purpose:** Document system architecture with diagrams and ADRs
**Capabilities:**

- System component identification
- Architecture diagram generation (Mermaid via MCP)
- ADR creation and management
- Design pattern documentation
- Dependency documentation
- Data flow documentation
- Security architecture documentation
- Infrastructure documentation
- Multiple architectural styles (C4, UML, simple)
  **Invoked by:** `/arch-doc` command
  **Usage:** For comprehensive architecture documentation
  **Output:** Architecture documentation with diagrams and ADRs

#### 4. `contributing-generator`

**Purpose:** Generate comprehensive CONTRIBUTING.md with guidelines and workflows
**Capabilities:**

- Code of conduct generation
- Development environment setup docs
- Pull request process documentation
- Coding standards definition
- Testing requirements specification
- Commit message convention docs
- Issue template integration
- Project-specific contribution guidelines
  **Invoked by:** `/contributing` command
  **Usage:** When establishing contribution guidelines
  **Output:** Complete CONTRIBUTING.md file

#### 5. `adr-generator`

**Purpose:** Create Architecture Decision Records following ADR template
**Capabilities:**

- ADR file creation with auto-numbering
- Template-based structure
- Context and rationale documentation
- Alternatives analysis
- Consequences tracking (positive/negative)
- Related ADR linking
- Status tracking (proposed, accepted, deprecated, superseded)
  **Invoked by:** `/adr` command
  **Usage:** When documenting architectural decisions
  **Output:** New ADR file in `docs/architecture/decisions/`

#### 6. `doc-validator`

**Purpose:** Validate documentation quality and correctness
**Capabilities:**

- Link validation (internal and external)
- Image reference validation
- Markdown syntax checking
- Code example validation
- Version number consistency checking
- Formatting consistency analysis
- Cross-reference verification
- Table of contents validation
- Issue reporting with severity levels
  **Invoked by:** `/validate-docs` command
  **Usage:** Before releases or as part of CI/CD
  **Output:** Validation report with issues and warnings

#### 7. `doc-health-analyzer`

**Purpose:** Analyze and score documentation completeness and quality
**Capabilities:**

- Documentation coverage calculation (0-100 score)
- README completeness analysis
- API documentation verification
- Architecture documentation checking
- Changelog currency verification
- Code documentation coverage analysis
- Markdown quality assessment
- Link health checking
- Example validation
- Actionable recommendations generation
- Health metrics reporting
  **Invoked by:** `/doc-health` command
  **Usage:** Regular documentation quality checks
  **Output:** Health score and detailed recommendations

### Skills

#### 1. `inline-doc-generator`

**Purpose:** Auto-generate inline documentation when writing code
**Supported Languages:**

- **Python**: Google-style docstrings
- **JavaScript/TypeScript**: JSDoc comments with type annotations
- **Go**: Go doc comments
- **Java**: Javadoc
- **Rust**: Rustdoc comments
- **C#**: XML documentation comments
- **Ruby**: RDoc/YARD
- **PHP**: PHPDoc

**Auto-invocation context:**

- Creating new functions or methods
- Defining new classes or types
- Writing complex logic or algorithms
- Creating API endpoints or handlers
- Defining data models or schemas
- Writing public interfaces or APIs

**Actions:**

- Generate language-appropriate doc comments
- Add parameter descriptions with types
- Document return values
- Include usage examples for complex functions
- Add type information (even if language has type hints)
- Document exceptions/errors that may be raised
- Add notes about side effects
- Include performance characteristics if relevant

**Integration:**

- Auto-invokes BEFORE writing function implementation
- Updates documentation when signature changes
- Suggests improvements during code review
- Flags undocumented public APIs

#### 2. `markdown-formatter`

**Purpose:** Auto-apply consistent markdown formatting
**Auto-invocation context:**

- Creating or editing `.md` files
- Writing README, CHANGELOG, CONTRIBUTING files
- Creating documentation in docs/ directories
- Writing markdown comments or descriptions
- Editing existing markdown documentation

**Actions:**

- Apply ATX-style headers (`#` prefix)
- Enforce consistent list formatting (use `-` for unordered)
- Add language specifiers to code blocks
- Format tables with proper alignment
- Fix link syntax and validate references
- Ensure proper heading hierarchy (no skipped levels)
- Remove trailing spaces
- Add blank lines appropriately
- Fix inconsistent emphasis (bold/italic)
- Validate and close code blocks

**Formatting Rules Applied:**

- MD001: Heading levels increment by one
- MD003: Use ATX-style headers
- MD004: Consistent list style
- MD007: 2 spaces for list indentation
- MD009: No trailing spaces
- MD012: No multiple blank lines
- MD022: Blank lines around headers
- MD040: Language in fenced code blocks
- MD047: File ends with newline

**Auto-Fixes:**

- Convert Setext headers to ATX
- Fix inconsistent list markers
- Add missing language to code blocks
- Remove trailing spaces
- Fix heading hierarchy
- Align table columns

#### 3. `changelog-tracker`

**Purpose:** Track changes and suggest changelog entries
**Auto-invocation context:**

- Making significant code changes
- Adding new features
- Fixing bugs
- Updating dependencies
- Making breaking changes
- Before git commits (if git hook configured)
- When creating pull requests
- On feature completion

**Actions:**

- Analyze change type (feat, fix, breaking, etc.)
- Suggest appropriate changelog entry
- Categorize into Keep a Changelog sections:
  - **Added**: New features
  - **Changed**: Changes to existing functionality
  - **Deprecated**: Soon-to-be removed features
  - **Removed**: Removed features (breaking)
  - **Fixed**: Bug fixes
  - **Security**: Security vulnerability fixes
- Recommend semantic version impact:
  - **MAJOR**: Breaking changes
  - **MINOR**: New features (backward compatible)
  - **PATCH**: Bug fixes
- Track and flag breaking changes prominently
- Parse Conventional Commit messages
- Generate user-focused descriptions (not implementation details)

**Commit Message Mapping:**

- `feat:` → Added
- `fix:` → Fixed
- `docs:` → Changed (if significant)
- `refactor:` → Changed (if user-facing)
- `perf:` → Changed/Added
- `BREAKING CHANGE:` → Removed or Changed with note

**Integration:**

- Pre-commit hook integration
- Pull request description auto-population
- Release notes generation
- Version bump recommendations

### MCP Servers

#### 1. MarkItDown MCP

**Purpose:** Convert various file formats to markdown
**Repository:** https://github.com/microsoft/markitdown/tree/main/packages/markitdown-mcp
**Use Cases:**

- Import existing documentation (Word, PDF, PowerPoint, Excel)
- Convert spreadsheets to markdown tables for documentation
- Extract content from legacy docs for README generation
- Process images with descriptions for documentation

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

**Setup Instructions:**

1. Build or pull the Docker image: `docker pull markitdown-mcp:latest`
2. For local file access, use Option 2 and adjust the volume mount path
3. Replace `/home/user/data` with your actual data directory path

**Available Tools:**

- `markitdown_convert` - Convert files to markdown (supports: .docx, .xlsx, .pptx, .pdf, .html, .csv, .json, .xml, images)

#### 2. Mermaid Chart MCP

**Purpose:** Generate diagrams programmatically from text descriptions
**Documentation:** https://docs.mermaidchart.com/ai/mcp-server
**Use Cases:**

- Architecture diagrams in `/arch-doc` command
- Data flow visualizations
- Component relationship diagrams
- Sequence diagrams for API flows
- Entity-relationship diagrams
- Flowcharts and state diagrams

**Configuration (`.mcp.json`):**

```json
{
  "mcpServers": {
    "mermaid-mcp": {
      "url": "https://mcp.mermaidchart.com/mcp",
      "type": "http"
    }
  }
}
```

**Setup Instructions:**

1. Sign up at https://www.mermaidchart.com/ (if authentication is required)
2. Add the HTTP server configuration to your `.mcp.json`
3. No API key needed for basic usage (check documentation for authentication details)

**Available Diagram Types:**

- Flowchart
- Sequence Diagram
- Class Diagram
- State Diagram
- Entity Relationship Diagram
- User Journey
- Gantt Chart
- Pie Chart
- Quadrant Chart
- Git Graph

## Files to Create

### Commands (with $ARGUMENTS support)

- ✅ `commands/readme.md` - `/readme [project-type] [audience]`
- ✅ `commands/changelog.md` - `/changelog [version] [range]`
- ✅ `commands/arch-doc.md` - `/arch-doc [focus] [style]`
- ✅ `commands/api-docs.md` - `/api-docs [api-type] [framework]`
- 🆕 `commands/contributing.md` - `/contributing`
- 🆕 `commands/docs-all.md` - `/docs-all [options]`
- 🆕 `commands/convert-doc.md` - `/convert-doc <file-path>`
- 🆕 `commands/adr.md` - `/adr <decision-title>`
- 🆕 `commands/validate-docs.md` - `/validate-docs`
- 🆕 `commands/doc-health.md` - `/doc-health`

### Agents

- ✅ `agents/readme-generator.md` - Create README with project type awareness
- ✅ `agents/api-documenter.md` - Generate REST/GraphQL/gRPC docs
- ✅ `agents/architecture-documenter.md` - Create architecture docs with diagrams
- 🆕 `agents/contributing-generator.md` - Generate CONTRIBUTING.md
- 🆕 `agents/adr-generator.md` - Create Architecture Decision Records
- 🆕 `agents/doc-validator.md` - Validate documentation quality
- 🆕 `agents/doc-health-analyzer.md` - Analyze doc completeness and score

### Skills

- ✅ `skills/inline-doc-generator/SKILL.md` - Auto-doc for 8+ languages
- ✅ `skills/markdown-formatter/SKILL.md` - Auto-format markdown with MD rules
- ✅ `skills/changelog-tracker/SKILL.md` - Auto-suggest changelog entries

### Templates

- `templates/README-template.md` - README structure by project type
- `templates/CHANGELOG-template.md` - Keep a Changelog format
- `templates/CONTRIBUTING-template.md` - Contributing guidelines
- `templates/ADR-template.md` - Architecture Decision Record template
- `templates/API-DOCS-template.md` - API documentation structure
- `templates/mermaid-diagrams.md` - Common diagram patterns
- 🆕 `templates/DOC-HEALTH-REPORT.md` - Health report format

### Reference Files

- 🆕 `DOCUMENTATION_STANDARDS.md` - Documentation best practices
  - Markdown formatting rules
  - Code example standards
  - Diagram conventions
  - Link formatting guidelines
  - Versioning strategy
  - Multi-language support guidelines

### MCP Configuration

- ✅ `.mcp.json` - MCP server configurations
  - MarkItDown MCP (document conversion)
  - Mermaid Chart MCP (diagram generation)

## Expected Behavior

When plugin is installed:

### Core Documentation Generation

1. **README generation** (`/readme`) - Create comprehensive README.md with project type detection
2. **Changelog management** (`/changelog`) - Generate/update CHANGELOG.md with semver recommendations
3. **Architecture documentation** (`/arch-doc`) - Create architecture docs with Mermaid diagrams
4. **API documentation** (`/api-docs`) - Generate REST/GraphQL/gRPC documentation with OpenAPI specs
5. **Contributing guidelines** (`/contributing`) - Generate CONTRIBUTING.md with workflows
6. **Complete documentation suite** (`/docs-all`) - Generate all documentation at once

### Advanced Features

7. **Document conversion** (`/convert-doc`) - Convert Word/PDF/Excel to markdown (via MarkItDown MCP)
8. **ADR creation** (`/adr`) - Create Architecture Decision Records with templates
9. **Documentation validation** (`/validate-docs`) - Check for broken links, syntax errors, etc.
10. **Documentation health scoring** (`/doc-health`) - Get 0-100 score with recommendations

### Auto-Invoked Features

11. **Inline documentation** - Auto-generate docstrings/JSDoc for 8+ languages
12. **Markdown formatting** - Auto-apply consistent formatting with MD rules
13. **Changelog tracking** - Auto-suggest changelog entries on commits

### MCP Integrations

14. **Mermaid diagrams** - Programmatic diagram generation (via Mermaid Chart MCP)
15. **Document conversion** - Multi-format support (via MarkItDown MCP)

### Argument Support

All commands accept arguments for customization:

- `/readme library developers` - Generate library README for developers
- `/changelog 2.0.0` - Generate changelog for version 2.0.0
- `/arch-doc security` - Generate security architecture only
- `/api-docs rest` - Generate REST API docs only
- `/docs-all --skip-readme --force` - Generate all except README, force overwrite

### Quality Assurance

- Documentation validation before releases
- Health scoring for continuous improvement
- Link checking (internal and external)
- Code example validation
- Consistent formatting enforcement
