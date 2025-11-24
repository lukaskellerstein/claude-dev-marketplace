# Documentation Plugin

Comprehensive documentation toolkit for Claude Code that helps you generate, review, and maintain high-quality documentation across your entire project.

## Overview

The Documentation Plugin provides specialized agents, commands, and skills for creating and maintaining professional documentation including README files, changelogs, API documentation, architecture diagrams, ADRs (Architecture Decision Records), and code documentation.

## Features

- **README Generation**: Create comprehensive README files with installation, usage, and contribution guidelines
- **Changelog Management**: Maintain changelogs following Keep a Changelog format and Semantic Versioning
- **Architecture Documentation**: Generate architecture docs with Mermaid diagrams, component descriptions, and ADRs
- **Documentation Review**: Assess documentation quality with detailed scoring and improvement recommendations
- **Code Documentation**: Write clear docstrings, JSDoc, and inline comments following best practices
- **Diagram Generation**: Create system architecture, sequence, data flow, and deployment diagrams using Mermaid
- **Documentation Standards**: Enforce consistent markdown, writing style, and documentation patterns

## Agents

### 1. Technical Writer
Expert technical writer specialized in creating clear, comprehensive documentation.

**Capabilities:**
- README documentation
- API documentation (REST, GraphQL, gRPC)
- Architecture documentation
- Code documentation (docstrings, comments)
- Process documentation (ADRs, design docs)
- Diagram generation with Mermaid

**Best for:** Creating any type of technical documentation from scratch

### 2. Documentation Reviewer
Quality assurance expert for comprehensive documentation review and scoring.

**Capabilities:**
- Documentation quality assessment across 8 dimensions
- Quantitative scoring (0-10 scale)
- Gap analysis and recommendations
- Comparison to industry standards
- Prioritized improvement plans

**Best for:** Evaluating documentation health and identifying improvements

### 3. Changelog Maintainer
Expert in maintaining changelogs following Keep a Changelog format.

**Capabilities:**
- Generate changelog entries from git commits
- Categorize changes (Added, Changed, Fixed, etc.)
- Determine semantic version bumps
- Format according to Keep a Changelog
- Handle breaking changes and deprecations

**Best for:** Keeping CHANGELOG.md up-to-date with releases

### 4. Architecture Documenter
Specialist in creating architecture documentation with diagrams and ADRs.

**Capabilities:**
- System architecture diagrams
- Component diagrams (C4 model)
- Sequence diagrams
- Data flow diagrams
- Deployment diagrams
- ADR (Architecture Decision Record) creation
- System design documentation

**Best for:** Documenting system architecture and design decisions

## Commands

### `/generate-readme`
Generate a comprehensive README.md file for your project.

**Usage:**
```
/generate-readme

Create a complete README for this library with installation,
usage examples, and API documentation
```

**Generates:**
- Project overview and features
- Installation instructions
- Quick start guide
- Usage examples
- Configuration options
- API reference
- Contributing guidelines
- License information

### `/update-changelog`
Update CHANGELOG.md with recent changes.

**Usage:**
```
/update-changelog

Add entries for the last 2 weeks of changes and determine
appropriate version bump
```

**Generates:**
- Categorized change entries
- Semantic version number
- Breaking change notifications
- Migration guides
- Version comparison links

### `/document-architecture`
Generate comprehensive architecture documentation.

**Usage:**
```
/document-architecture

Create architecture documentation for this microservices
application with diagrams and ADRs
```

**Generates:**
- System architecture diagrams
- Component descriptions
- Sequence diagrams for key flows
- Data flow diagrams
- Deployment architecture
- ADRs for major decisions

### `/review-docs`
Review and score documentation quality.

**Usage:**
```
/review-docs

Perform comprehensive review of all project documentation
with scoring and recommendations
```

**Provides:**
- Overall documentation health score (0-10)
- Detailed scores across 8 dimensions
- Critical issues and improvements
- Prioritized action plan
- Comparison to best practices

## Skills

### 1. Documentation Standards
Auto-invoked when writing or reviewing documentation to ensure best practices.

**Enforces:**
- Markdown formatting standards
- Writing style guidelines (active voice, clarity)
- Consistent terminology
- Proper heading hierarchy
- Code block formatting
- Link and image best practices

**Active when:**
- Writing documentation
- Creating README or CHANGELOG
- Generating any .md files

### 2. Code Documentation
Auto-invoked when writing code comments or docstrings.

**Provides guidance on:**
- Language-specific documentation (JSDoc, Python docstrings, Go comments, Rust docs)
- When to document vs. self-documenting code
- Inline comment best practices
- Function/class/module documentation
- Documentation anti-patterns to avoid

**Active when:**
- Writing code documentation
- Adding comments or docstrings
- Documenting APIs

## MCP Servers

This plugin integrates with:

### Mermaid MCP
- Create and render Mermaid diagrams
- Generate architecture diagrams
- Create sequence, component, and data flow diagrams

### Markitdown MCP
- Convert various formats to Markdown (PDF, Word, PowerPoint, Excel)
- Process images with OCR
- Extract text from audio and video
- Parse HTML and text-based formats

## Installation

This plugin is part of the Claude Code marketplace. To use it:

1. Install Claude Code
2. Add this plugin from the marketplace
3. The plugin will be available with all commands and agents

## Quick Start

### Generate a README
```
/generate-readme

Create a comprehensive README for my Node.js library
```

### Update Changelog
```
/update-changelog

Add all changes since version 1.2.0 and determine next version
```

### Review Documentation
```
/review-docs

Perform a quality review of all documentation with scoring
```

### Document Architecture
```
/document-architecture

Create architecture documentation with system diagrams and ADRs
```

## Documentation Quality Dimensions

When reviewing documentation, the plugin assesses:

1. **Coverage (20%)**: Are all necessary topics documented?
2. **Accuracy (20%)**: Is information correct and up-to-date?
3. **Clarity (15%)**: Is it easy to understand?
4. **Examples (15%)**: Are examples sufficient and working?
5. **Structure (10%)**: Is it well-organized?
6. **Completeness (10%)**: Are edge cases covered?
7. **Accessibility (5%)**: Is it inclusive and readable?
8. **Maintainability (5%)**: Is it easy to keep updated?

Overall scores are weighted and graded A+ to F.

## Best Practices

### README Files
- Clear project name and description
- Installation and setup instructions
- Usage examples with code
- API reference or link
- Contributing guidelines
- License information

### Changelogs
- Follow Keep a Changelog format
- Use Semantic Versioning
- Categorize changes (Added, Changed, Fixed, etc.)
- Mark breaking changes clearly
- Include migration guides
- Date entries with ISO 8601

### Architecture Documentation
- Start with high-level overview
- Use diagrams extensively (Mermaid)
- Document major components
- Create ADRs for key decisions
- Explain integration patterns
- Include deployment architecture

### Code Documentation
- Write self-documenting code first
- Document public APIs comprehensively
- Explain "why" not "what"
- Provide usage examples
- Keep documentation close to code
- Update with code changes

## Examples

### Generate Complete Documentation Suite

```bash
# 1. Generate README
/generate-readme

# 2. Create architecture documentation
/document-architecture

# 3. Update changelog for release
/update-changelog

# 4. Review everything
/review-docs
```

### Create ADR for Decision

```
/document-architecture

Create an ADR documenting our decision to use PostgreSQL
over MongoDB for the primary database, including rationale,
alternatives considered, and consequences
```

### Fix Documentation Issues

```
# First, identify issues
/review-docs

# Then address specific issues based on review
- Fix broken links
- Update outdated examples
- Add missing troubleshooting section
```

## Supported Documentation Types

- **README.md**: Project overview and getting started
- **CHANGELOG.md**: Version history and changes
- **API Documentation**: REST, GraphQL, gRPC endpoints
- **Architecture Docs**: System design and diagrams
- **ADRs**: Architecture Decision Records
- **Code Comments**: Inline documentation
- **Docstrings**: Function/class documentation
- **Design Docs**: Technical proposals and RFCs
- **Runbooks**: Operational procedures
- **Contributing Guides**: Development workflows

## Diagram Types

Using Mermaid, the plugin can generate:

- **System Architecture**: Overall system structure
- **Component Diagrams**: C4 model components
- **Sequence Diagrams**: Interaction flows
- **Data Flow Diagrams**: Data movement and transformation
- **Deployment Diagrams**: Infrastructure topology
- **State Machines**: State transitions
- **Entity Relationship Diagrams**: Data models

## Integration with Development Workflow

### Pre-commit
- Review code documentation
- Enforce documentation standards
- Validate examples

### During Development
- Document as you code
- Create ADRs for decisions
- Maintain changelog

### Pre-release
- Update changelog
- Review all documentation
- Generate release notes
- Verify examples work

### Post-release
- Update version numbers
- Archive old documentation
- Plan documentation improvements

## Contributing

When contributing to this plugin:

1. Follow the documentation standards enforced by the plugin itself
2. Test all commands and examples
3. Update README with new features
4. Maintain consistency with existing patterns
5. Ensure all Mermaid diagrams render correctly

## License

MIT License - See LICENSE file for details

## Support

For issues, questions, or contributions:
- GitHub Issues: Report bugs or request features
- Documentation: See `/docs` directory
- Examples: See `/examples` directory

## Version History

See [CHANGELOG.md](CHANGELOG.md) for version history and changes.

---

**Made with the Documentation Plugin** - A comprehensive documentation toolkit for Claude Code.
