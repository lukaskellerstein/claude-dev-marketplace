---
description: Generate a comprehensive README.md file for the project with installation, usage, and contribution guidelines
---

Generate a complete, production-ready README.md file for your project.

## Process

Follow these steps:

1. **Analyze Project**: Understand the project structure and purpose
   - Identify project type (library, application, CLI tool, etc.)
   - Review package.json/requirements.txt/etc. for metadata
   - Analyze main entry points and core functionality
   - Check for existing documentation
   - Review license file
   - Identify technology stack

2. **Launch Technical Writer**: Use the `technical-writer` agent to:
   - Create project overview and description
   - Write clear installation instructions
   - Document configuration options
   - Create usage examples with code
   - Write API reference (if applicable)
   - Document project structure
   - Write contributing guidelines
   - Add troubleshooting section
   - Include license and acknowledgments
   - Generate badges and shields

3. **Enhance with Diagrams**: If architecture is complex:
   - Create system architecture diagram with Mermaid
   - Add data flow diagrams
   - Include component diagrams
   - Visualize workflows

4. **Review Quality**: Ensure README is:
   - Clear and easy to understand
   - Complete with all necessary sections
   - Has working code examples
   - Includes proper formatting
   - Has table of contents for long documents
   - Appropriate for target audience

## Output

Present a comprehensive README.md including:

### Essential Sections

**Header**
- Project name and tagline
- Badges (build status, version, license, coverage)
- Brief description

**Table of Contents** (for long READMEs)
- Links to all major sections

**Overview**
- What the project does
- Why it exists
- Who it's for
- Key features

**Installation**
- Prerequisites and dependencies
- Step-by-step installation
- Platform-specific instructions
- Docker/container instructions (if applicable)
- Verification steps

**Quick Start**
- Minimal working example
- Copy-paste ready code
- Expected output

**Usage**
- Basic usage examples
- Common use cases
- Configuration options
- Advanced usage
- CLI commands (if applicable)

**API Reference** (if applicable)
- Core classes/functions
- Parameters and return values
- Examples for each API

**Configuration**
- Environment variables
- Config file format
- Configuration options table
- Default values

**Examples**
- Real-world usage scenarios
- Code samples
- Screenshots/GIFs (if applicable)

**Architecture** (if complex)
- High-level architecture diagram
- Component descriptions
- Design decisions

**Development**
- Setting up development environment
- Running tests
- Building the project
- Code style guidelines

**Contributing**
- How to contribute
- Code of conduct
- Pull request process
- Development workflow

**Testing**
- How to run tests
- Test coverage
- Testing strategy

**Deployment** (if applicable)
- Deployment instructions
- Platform-specific guides
- Environment setup

**Troubleshooting**
- Common issues and solutions
- FAQ
- Where to get help

**License**
- License type
- License text or link

**Acknowledgments**
- Credits and attributions
- Third-party libraries
- Contributors

## Best Practices Applied

- **Clarity**: Use simple, direct language
- **Completeness**: Cover all necessary topics
- **Code Examples**: Include working, tested examples
- **Visual Aids**: Use diagrams where helpful
- **Navigation**: Add table of contents for long docs
- **Badges**: Include relevant status badges
- **Accessibility**: Use descriptive link text and alt text
- **Consistency**: Follow markdown best practices
- **Mobile-Friendly**: Ensure readable on all devices

## Examples

### Generate README for Library
```
/generate-readme

Generate a README for this JavaScript library with
installation via npm, usage examples, and API documentation
```

### Generate README for CLI Tool
```
/generate-readme

Create a comprehensive README for this CLI tool with
installation instructions, command reference, and examples
```

### Generate README for Application
```
/generate-readme

Generate a README for this web application with
setup instructions, configuration guide, and deployment steps
```

## README Templates by Project Type

### Library/Package
Focus on:
- Installation via package manager
- Import/require examples
- API documentation
- Integration examples

### CLI Tool
Focus on:
- Installation methods
- Command reference
- Options and flags
- Usage examples

### Web Application
Focus on:
- Setup and installation
- Environment configuration
- Running locally
- Deployment instructions

### Framework/Boilerplate
Focus on:
- Getting started guide
- Project structure
- Customization options
- Examples and templates

## Quality Checklist

Before finalizing:
- [ ] Project name and description are clear
- [ ] Installation instructions are complete and tested
- [ ] Usage examples work and are up-to-date
- [ ] Configuration options are documented
- [ ] Code examples are properly formatted
- [ ] Links are valid and working
- [ ] Badges are accurate and functional
- [ ] Table of contents is complete (if present)
- [ ] Contributing guidelines are included
- [ ] License is specified
- [ ] Contact/support information is provided
- [ ] Troubleshooting section addresses common issues

Provide a complete, production-ready README.md that can be used immediately.
