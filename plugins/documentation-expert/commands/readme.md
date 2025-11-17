---
description: Generate comprehensive README.md file
---

# Generate Comprehensive README.md

Generate comprehensive README.md for: $ARGUMENTS

## Arguments

- **project-type** (optional): `library`, `cli-tool`, `web-app`, `api`, `mobile-app`, or `auto` (default)
- **audience** (optional): `developers`, `users`, or `both` (default)

## Examples

- `/readme` - Auto-detect project type
- `/readme library` - Generate library-focused README
- `/readme api developers` - API README for developers
- `/readme cli-tool users` - CLI tool README for end users

## Task

You are tasked with generating a comprehensive README.md file tailored to the specified project type and target audience.

### Argument Parsing

Parse $ARGUMENTS to extract:
1. **Project type** (first argument) - defaults to `auto` if not provided
2. **Target audience** (second argument) - defaults to `both` if not provided

### Project Types

- **library**: Software library or SDK
  - Focus on API documentation, installation, usage examples
  - Target: Developers who will integrate the library

- **cli-tool**: Command-line tool
  - Focus on commands, options, usage patterns
  - Include installation and common workflows

- **web-app**: Web application
  - Focus on features, deployment, configuration
  - Include screenshots, user workflows

- **api**: API service
  - Focus on endpoints, authentication, integration
  - Link to detailed API documentation

- **mobile-app**: Mobile application
  - Focus on features, download links, screenshots
  - Platform-specific installation

- **auto**: Auto-detect from project structure

### Target Audience

- **developers**: Technical audience (API docs, architecture, contribution)
- **users**: End users (features, installation, usage)
- **both**: Balanced for developers and users

## Analysis Steps

1. **Analyze Project Structure**:
   - Examine the codebase structure
   - Identify main entry points
   - Detect technology stack
   - Find configuration files
   - Identify dependencies

2. **Extract Key Information**:
   - Project purpose and goals
   - Main features and capabilities
   - Installation requirements
   - Usage patterns
   - Configuration options

3. **Check Existing Documentation**:
   - Review existing README if present
   - Check for other documentation files
   - Identify gaps in documentation

## README Generation

Generate a README.md following the template in `templates/README-template.md` with these sections:

### Required Sections

1. **Project Title and Description**
   - Clear, concise project name
   - One-line description
   - Relevant badges (build, coverage, version, license)

2. **Table of Contents** (if README > 200 lines)
   - Links to all major sections

3. **Features**
   - Bulleted list of key capabilities
   - Brief description of each feature

4. **Installation**
   - Prerequisites with version requirements
   - Step-by-step setup instructions
   - Platform-specific notes (Linux, macOS, Windows)
   - Docker setup if applicable

5. **Quick Start**
   - Minimal example to get started
   - Expected output

6. **Usage**
   - Common use cases with code examples
   - Configuration options
   - CLI usage if applicable
   - API usage if applicable

7. **Project Structure** (for complex projects)
   - Directory structure explanation
   - Key files and their purposes

8. **Development**
   - Development setup
   - Running tests
   - Building the project
   - Contribution workflow

9. **Documentation**
   - Link to detailed documentation
   - API documentation link
   - Architecture documentation link

10. **Contributing**
    - Link to CONTRIBUTING.md
    - Brief contribution guidelines

11. **License**
    - License type
    - Link to LICENSE file

12. **Support/Contact**
    - How to get help
    - Contact information
    - Issue tracking

### Optional Sections (Include if Applicable)

- **Screenshots/Demos**: For UI projects
- **Roadmap**: Planned features
- **FAQ**: Common questions
- **Acknowledgments**: Credits
- **Badges**: Build status, coverage, etc.

## Best Practices

Follow the standards defined in `DOCUMENTATION_STANDARDS.md`:

- Use clear heading hierarchy
- Include language identifiers in code blocks
- Keep code examples working and tested
- Use relative links for internal docs
- Add badges for build status, coverage, version
- Keep it concise but complete
- Write for the intended audience (developers, users, etc.)

## Code Examples

- Ensure all code examples are working and tested
- Include expected output
- Show common use cases
- Demonstrate error handling

## Formatting

- Use Markdown best practices
- Consistent code block formatting with language specifiers
- Proper table formatting
- Clear section hierarchy
- Links that work

## Review

Before finalizing:
- [ ] All sections are complete
- [ ] Code examples work
- [ ] Links are valid
- [ ] Grammar and spelling checked
- [ ] Consistent formatting throughout
- [ ] Appropriate for target audience

Generate the README.md and save it to the project root, or update the existing one if present.
