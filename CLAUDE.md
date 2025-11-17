# Documentation

Read documentation, so you produce a relevant and correct outputs for Claude Code plugins and marketplace.

## Marketplace

Documentation: https://code.claude.com/docs/en/plugin-marketplaces#plugin-marketplaces

## Plugin

Plugin manifest file: https://code.claude.com/docs/en/plugins-reference#plugin-manifest-schema

Complete schema:

```json
{
  "name": "plugin-name",
  "version": "1.2.0",
  "description": "Brief plugin description",
  "author": {
    "name": "Author Name",
    "email": "author@example.com",
    "url": "https://github.com/author"
  },
  "homepage": "https://docs.example.com/plugin",
  "repository": "https://github.com/author/plugin",
  "license": "MIT",
  "keywords": ["keyword1", "keyword2"],
  "commands": ["./custom/commands/special.md"],
  "agents": "./custom/agents/",
  "hooks": "./config/hooks.json",
  "mcpServers": "./mcp-config.json"
}
```

### Output styles

Documentation: `https://code.claude.com/docs/en/output-styles`

Output styles allow you to use Claude Code as any type of agent while keeping its core capabilities, such as running local scripts, reading/writing files, and tracking TODOs.

Output styles directly modify Claude Code’s system prompt.

- All output styles exclude instructions for efficient output (such as responding concisely).
- Custom output styles exclude instructions for coding (such as verifying code with tests), unless keep-coding-instructions is true.
- All output styles have their own custom instructions added to the end of the system prompt.
- All output styles trigger reminders for Claude to adhere to the output style instructions during the conversation.

### Commands

Documentation: `./docs/commands.md`

Ex. **Custom command that triggers script**

```
---
description: Get latest screenshot path
allowed-tools: Bash(/home/lukas/my_claude_commands/lss_command.sh)
---

!`/home/lukas/my_claude_commands/lss_command.sh`
```

### Sub-Agent

Documentation: https://code.claude.com/docs/en/sub-agents#file-format

File format:

```
---
name: your-sub-agent-name
description: Description of when this subagent should be invoked
tools: tool1, tool2, tool3  # Optional - inherits all tools if omitted
model: sonnet  # Optional - specify model alias or 'inherit'
---

Your subagent's system prompt goes here. This can be multiple paragraphs
and should clearly define the subagent's role, capabilities, and approach
to solving problems.

Include specific instructions, best practices, and any constraints
the subagent should follow.
```

### Skills

Documentation: https://code.claude.com/docs/en/skills

File format:

```
---
name: your-skill-name
description: Brief description of what this Skill does and when to use it
allowed-tools: Read, Grep, Glob # Claude can only use the specified tools (Read, Grep, Glob) without needing to ask for permission. If allowed-tools is not specified, Claude will ask for permission to use tools as normal, following the standard permission model.
---

# Your Skill Name

## Instructions
Provide clear, step-by-step guidance for Claude.

## Examples
Show concrete examples of using this Skill.
```

### Command-Agent-Skill Relationship

Understanding the architecture of this plugin:

**Commands** are user-facing entry points that:

- Parse arguments from user input ($ARGUMENTS)
- Validate inputs and context
- Invoke appropriate agents for heavy lifting
- Present results to user
- Can be invoked via `/command-name [arguments]`

**Agents** are specialized workers that:

- Perform deep codebase analysis
- Generate high-quality content
- Make complex decisions based on context
- Can be invoked by commands or used standalone
- Execute autonomously with specific expertise

**Skills** are auto-invoked assistants that:

- Trigger automatically on specific contexts
- Provide just-in-time assistance
- Maintain consistency across work
- Don't require explicit invocation

**Example flow:**

1. User runs `/readme library`
2. Command parses `library` argument
3. Command invokes `readme-generator` agent with context
4. Agent analyzes codebase with library-specific patterns
5. Agent generates library-focused README
6. Command presents result to user

## MCP

Available MCPs: `./MCP_SERVERS_LIST.md`.

You can propose your own MCP servers, but make sure they exist !!!
