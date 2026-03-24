# Introduction to Claude Code and Skills

## Table of Contents

- [What is Claude Code](#what-is-claude-code)
- [Installation and Setup](#installation-and-setup)
- [Basic Usage](#basic-usage)
- [Slash Commands](#slash-commands)
- [CLAUDE.md Files](#claudemd-files)
- [Skills](#skills)
- [Hooks](#hooks)
- [MCP Servers](#mcp-servers)
- [Permissions and Settings](#permissions-and-settings)
- [IDE Integration](#ide-integration)
- [Memory System](#memory-system)
- [Headless Mode and Automation](#headless-mode-and-automation)
- [Best Practices](#best-practices)
- [Summary](#summary)
- [Next Steps](#next-steps)
- [Additional Resources](#additional-resources)

---

## What is Claude Code

Claude Code is Anthropic's official command-line interface for AI-assisted software development. It provides an agentic coding experience where Claude can read, search, edit files, and execute commands directly in your terminal.

Key characteristics of Claude Code:

- **Agentic coding tool**: Claude operates as an autonomous agent that can explore your codebase, make changes, and run commands
- **Terminal-native**: runs directly in your shell with full access to your development environment
- **Context-aware**: understands your project structure, git history, and file contents
- **Tool use**: Claude can read files, write files, execute bash commands, search code, and more
- **Iterative**: supports multi-turn conversations to refine solutions

```bash
# Claude Code works directly in your terminal
# It can see your project, run commands, and make edits
claude

# Start with a specific prompt
claude "explain the architecture of this project"

# Pipe input for processing
cat error.log | claude "what caused this error?"
```

Claude Code differs from chat-based AI assistants because it has direct access to your filesystem and can take actions, not just provide suggestions.

---

## Installation and Setup

Claude Code requires Node.js 18+ and is installed via npm.

```bash
# Install Claude Code globally
npm install -g @anthropic-ai/claude-code

# Verify installation
claude --version

# Run initial setup and authentication
claude
```

On first run, Claude Code will guide you through authentication with your Anthropic account.

```bash
# Authentication options
# 1. Direct API key (for individual use)
export ANTHROPIC_API_KEY="sk-ant-..."

# 2. OAuth login (opens browser for Anthropic account login)
claude  # follow the prompts on first run

# 3. Enterprise SSO (for organizations)
# configured via your organization's admin settings
```

System requirements and configuration:

```bash
# Check system requirements
node --version  # must be 18+
npm --version

# Set custom configuration directory (optional)
export CLAUDE_CONFIG_DIR="$HOME/.config/claude-code"

# Set custom model (if needed)
export CLAUDE_MODEL="claude-sonnet-4-20250514"

# Increase context window usage limit (optional)
export CLAUDE_MAX_TOKENS=200000
```

You can also configure Claude Code through the settings file:

```json
{
  "apiKey": "sk-ant-...",
  "model": "claude-sonnet-4-20250514",
  "theme": "dark",
  "verbose": false
}
```

---

## Basic Usage

Claude Code runs as an interactive conversation in your terminal.

```bash
# Start an interactive session
claude

# Start with an initial prompt
claude "refactor the database module to use connection pooling"

# Resume the most recent conversation
claude --resume

# Resume a specific conversation by ID
claude --resume abc123

# Start a new conversation (don't resume)
claude --new

# Print the last response and exit
claude --print
```

Working with context and files:

```bash
# Claude automatically sees your current directory
# You can reference files in your prompts
claude "review the code in src/main.py and suggest improvements"

# Pipe file contents or command output
cat requirements.txt | claude "are there any security vulnerabilities?"

# Pass multi-line input
claude "$(cat <<'EOF'
Fix the bug where users can't log in.
The error is in auth/login.py.
Make sure to add proper error handling.
EOF
)"

# Use with specific files
claude "update tests in test_api.py to cover the new endpoint"
```

During a conversation, Claude has access to tools:

```bash
# Claude can autonomously:
# - Read files to understand your code
# - Search for patterns across your codebase
# - Edit files with precise replacements
# - Run bash commands (with your permission)
# - Use git to understand history and make commits

# Example interaction:
# You: "fix the failing tests"
# Claude: *reads test files* *reads source code* *identifies bug*
#         *edits source file* *runs tests* *confirms fix*
```

---

## Slash Commands

Slash commands are special commands you type during a conversation to control Claude Code's behavior.

```bash
# /help - Show available commands and usage
/help

# /clear - Clear the current conversation context
/clear

# /compact - Compress conversation to save context window
# Useful for long sessions approaching the context limit
/compact

# /compact [instructions] - Compact with custom focus instructions
/compact "focus on the database refactoring discussion"

# /init - Create a CLAUDE.md file for your project
# Generates project-specific instructions for Claude
/init

# /review - Review a pull request or code changes
/review

# /commit - Stage and commit changes with an AI-generated message
/commit

# /diff - Show current uncommitted changes
/diff

# /cost - Display token usage and cost for the session
/cost

# /bug - Report a bug with Claude Code
/bug

# /config - Open configuration settings
/config

# /login - Re-authenticate with Anthropic
/login

# /logout - Clear authentication credentials
/logout

# /doctor - Diagnose common issues
/doctor

# /permissions - Review and modify tool permissions
/permissions
```

Slash commands can be used at any point during a conversation:

```bash
# Typical workflow example
claude
> "Let's refactor the user authentication module"
# ... long conversation ...
> /compact  # save context space
> "Now update the tests for the changes we made"
# ... more work ...
> /commit  # commit the changes
> /clear   # start fresh for a new task
```

---

## CLAUDE.md Files

CLAUDE.md files provide project-specific instructions that Claude reads at the start of every conversation. They act as persistent context about your project's conventions, architecture, and preferences.

```bash
# Generate a CLAUDE.md file interactively
claude /init

# Claude will analyze your project and create a CLAUDE.md
# covering: tech stack, conventions, build commands, etc.
```

CLAUDE.md files can be placed at multiple levels:

```bash
# Project root (shared with the team via git)
/my-project/CLAUDE.md

# Project root (personal, git-ignored)
/my-project/.claude/CLAUDE.md

# Home directory (applies to all projects)
~/.claude/CLAUDE.md

# Parent directories are also checked
# Claude walks up from cwd to find all applicable CLAUDE.md files
```

Example CLAUDE.md content:

```text
# CLAUDE.md

## Project Overview
This is a FastAPI backend service for user management.

## Tech Stack
- Python 3.12, FastAPI, SQLAlchemy 2.0, PostgreSQL
- Testing: pytest with pytest-asyncio
- Linting: ruff

## Conventions
- Use async/await for all database operations
- Follow Google-style docstrings
- Type hints are required on all function signatures
- Database models go in src/models/
- API routes go in src/routes/
- Business logic goes in src/services/

## Build and Test Commands
- Run tests: `pytest -xvs`
- Run linter: `ruff check .`
- Run formatter: `ruff format .`
- Start dev server: `uvicorn src.main:app --reload`

## Important Patterns
- All API responses use the ResponseModel wrapper
- Database sessions are injected via FastAPI dependencies
- Migrations are managed with alembic

## Do NOT
- Do not modify alembic migration files directly
- Do not use raw SQL queries; use SQLAlchemy ORM
- Do not commit .env files
```

CLAUDE.md supports importing other instruction files:

```text
# CLAUDE.md

@docs/architecture.md
@docs/api-conventions.md
@.cursor/rules/*.md
```

---

## Skills

Skills are modular capabilities that extend what Claude Code can do. They provide specialized knowledge and tool access for specific tasks.

Built-in skills include:

```bash
# /commit - Generate commit messages and stage changes
# Claude analyzes your diff and creates descriptive commit messages
/commit

# /review - Review code changes or pull requests
# Provides detailed feedback on code quality, bugs, and improvements
/review

# /init - Initialize project configuration
/init

# Skills are invoked via slash commands
# Claude automatically detects when a skill is relevant
```

Custom skills can be defined to teach Claude project-specific workflows:

```json
{
  "skills": {
    "deploy": {
      "description": "Deploy the application to production",
      "instructions": "Run the deployment pipeline using...",
      "tools": ["bash"]
    },
    "db-migrate": {
      "description": "Create and run database migrations",
      "instructions": "Use alembic to generate migration files...",
      "tools": ["bash", "write"]
    }
  }
}
```

Skills can also be loaded from external sources:

```bash
# Skills can be distributed as packages
# and referenced in your project configuration

# Community skills extend Claude's capabilities
# for specific frameworks, languages, or workflows
```

---

## Hooks

Hooks allow you to run custom scripts before or after Claude uses a tool. They are configured in your settings and enable validation, logging, and automation.

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "bash",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'About to run bash command' >> /tmp/claude-audit.log"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "write",
        "hooks": [
          {
            "type": "command",
            "command": "ruff check $CLAUDE_FILE_PATH 2>&1 || true"
          }
        ]
      }
    ],
    "Notification": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "notify-send 'Claude Code' '$CLAUDE_NOTIFICATION'"
          }
        ]
      }
    ]
  }
}
```

Hook types and their use cases:

```bash
# PreToolUse - runs BEFORE a tool is executed
# Use cases: validation, approval gates, logging
# Return non-zero exit code to block the tool execution

# PostToolUse - runs AFTER a tool completes
# Use cases: linting after file writes, running tests, notifications

# Notification - runs when Claude wants to notify the user
# Use cases: desktop notifications, sound alerts, Slack messages

# Stop - runs when Claude finishes a turn
# Use cases: cleanup, final validation, metrics collection
```

Hook environment variables:

```bash
# Available in all hooks:
# $CLAUDE_TOOL_NAME - the tool being used (e.g., "bash", "write")
# $CLAUDE_TOOL_INPUT - JSON string of tool input parameters
# $CLAUDE_SESSION_ID - current session identifier

# Available in PostToolUse:
# $CLAUDE_TOOL_OUTPUT - the output from the tool execution

# Available in write/edit hooks:
# $CLAUDE_FILE_PATH - path of the file being written/edited
```

Practical hook example for auto-formatting:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "write|edit",
        "hooks": [
          {
            "type": "command",
            "command": "if [[ \"$CLAUDE_FILE_PATH\" == *.py ]]; then ruff format \"$CLAUDE_FILE_PATH\"; fi"
          },
          {
            "type": "command",
            "command": "if [[ \"$CLAUDE_FILE_PATH\" == *.js ]]; then prettier --write \"$CLAUDE_FILE_PATH\"; fi"
          }
        ]
      }
    ]
  }
}
```

---

## MCP Servers

Model Context Protocol (MCP) servers extend Claude Code by connecting external tools and data sources. MCP is an open standard for providing context and tools to AI assistants.

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/allowed/dir"],
      "env": {}
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_..."
      }
    },
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres", "postgresql://user:pass@localhost/mydb"],
      "env": {}
    }
  }
}
```

MCP server configuration locations:

```bash
# Project-level MCP servers (in .claude/settings.json)
/my-project/.claude/settings.json

# User-level MCP servers (applies to all projects)
~/.claude/settings.json

# MCP servers can also be configured via the CLI
claude mcp add my-server -- npx -y @some/mcp-server
claude mcp remove my-server
claude mcp list
```

Common MCP servers and their capabilities:

```bash
# @modelcontextprotocol/server-filesystem
# Provides: file read/write/search tools
# Use when: you need controlled file access with specific directory permissions

# @modelcontextprotocol/server-github
# Provides: GitHub API tools (issues, PRs, repos)
# Use when: working with GitHub repositories, reviewing PRs

# @modelcontextprotocol/server-postgres
# Provides: SQL query tools for PostgreSQL
# Use when: exploring or modifying database schemas and data

# @modelcontextprotocol/server-memory
# Provides: persistent key-value memory across sessions
# Use when: storing context that should persist between conversations

# @modelcontextprotocol/server-brave-search
# Provides: web search capabilities
# Use when: Claude needs to look up current information
```

Custom MCP server example:

```json
{
  "mcpServers": {
    "my-internal-api": {
      "command": "python",
      "args": ["/path/to/my_mcp_server.py"],
      "env": {
        "API_BASE_URL": "https://internal.api.example.com",
        "API_KEY": "..."
      }
    }
  }
}
```

---

## Permissions and Settings

Claude Code uses a permission system to control what actions Claude can take, ensuring safety while maintaining productivity.

```json
{
  "permissions": {
    "allow": [
      "bash(npm run *)",
      "bash(pytest *)",
      "bash(git *)",
      "bash(ruff *)",
      "read",
      "write(src/**)",
      "edit(src/**)"
    ],
    "deny": [
      "bash(rm -rf *)",
      "bash(sudo *)",
      "bash(curl * | bash)",
      "write(.env*)",
      "write(*.pem)"
    ]
  }
}
```

Permission levels and behavior:

```bash
# When Claude wants to use a tool:
# 1. Check deny list - if matched, block immediately
# 2. Check allow list - if matched, proceed without asking
# 3. If neither matched - prompt user for approval

# Users can approve with different scopes:
# - "Yes" - allow this one time
# - "Yes, always for this project" - add to project allow list
# - "Yes, always" - add to user-level allow list
# - "No" - deny this one time
```

Settings file locations:

```bash
# User settings (applies globally)
~/.claude/settings.json

# Project settings (shared with team, checked into git)
.claude/settings.json

# Project settings (personal, not checked in)
.claude/settings.local.json
```

Complete settings example:

```json
{
  "permissions": {
    "allow": [
      "bash(npm *)",
      "bash(git *)",
      "read",
      "write(src/**)",
      "edit(src/**)"
    ],
    "deny": [
      "bash(rm -rf /)",
      "write(.env)"
    ]
  },
  "hooks": {},
  "mcpServers": {},
  "preferences": {
    "verbose": false,
    "theme": "system"
  }
}
```

---

## IDE Integration

Claude Code integrates with VS Code through an official extension, providing a GUI experience alongside terminal access.

```bash
# Install the VS Code extension
# Search for "Claude Code" in VS Code extensions marketplace
# Or install from the command line:
code --install-extension anthropic.claude-code

# The extension provides:
# - Side panel for conversations
# - Inline code suggestions
# - File diff previews before applying changes
# - Terminal integration
```

VS Code extension features:

```bash
# Open Claude Code panel
# Keyboard shortcut: Ctrl+Shift+P -> "Claude Code: Open"

# Key features:
# 1. Chat interface within VS Code
# 2. See file changes as diffs before accepting
# 3. Navigate to files Claude references
# 4. Review tool use with visual indicators
# 5. Integrated terminal output display

# The extension uses the same configuration as CLI
# CLAUDE.md, settings.json, and permissions all apply
```

---

## Memory System

Claude Code has a memory system that persists important context across conversations through CLAUDE.md files and conversation history.

```bash
# Claude remembers context through:
# 1. CLAUDE.md files (persistent project instructions)
# 2. Conversation resume (--resume flag)
# 3. MCP memory servers (explicit key-value storage)
# 4. Git history (Claude reads commits for context)

# Resume a previous conversation
claude --resume

# List recent conversations
claude --list

# The /compact command summarizes the current conversation
# preserving key context while freeing token space
/compact
```

Memory best practices:

```bash
# Put stable project information in CLAUDE.md
# - Architecture decisions
# - Coding conventions
# - Build and test commands
# - Common gotchas

# Use /compact during long sessions to avoid context limits
# The summary preserves essential context from the conversation

# For cross-session memory, use an MCP memory server
claude mcp add memory -- npx -y @modelcontextprotocol/server-memory
```

---

## Headless Mode and Automation

Claude Code can run in non-interactive (headless) mode for CI/CD pipelines, scripts, and automation.

```bash
# Run a single prompt and exit (print mode)
claude -p "explain what this project does"

# Pipe input and get structured output
cat code.py | claude -p "review this code" --output-format json

# Use in shell scripts
REVIEW=$(claude -p "review the last commit" --output-format text)
echo "$REVIEW" > review.txt

# Run with specific allowed tools (no permission prompts)
claude -p "fix the linting errors" \
  --allowedTools "bash(ruff *)" "read" "edit(src/**)"

# Output formats
claude -p "list all TODO comments" --output-format text    # plain text
claude -p "analyze dependencies" --output-format json      # structured JSON
claude -p "summarize changes" --output-format stream-json  # streaming JSON
```

CI/CD integration example:

```bash
#!/bin/bash
# automated-review.sh - Run Claude Code in CI pipeline

# Review pull request changes
claude -p "Review the changes in this PR. \
  Focus on: security issues, performance problems, \
  and adherence to our coding standards." \
  --output-format json \
  --allowedTools "read" "bash(git diff *)" \
  > review-results.json

# Generate documentation for changed files
claude -p "Update docstrings for all modified functions" \
  --allowedTools "read" "edit(src/**)" "bash(git diff --name-only)"
```

GitHub Actions integration:

```bash
# In your GitHub Actions workflow:
# - uses: anthropic/claude-code-action@v1
#   with:
#     prompt: "Review this PR and comment on any issues"
#     anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
```

---

## Best Practices

Effective usage patterns for Claude Code:

```bash
# 1. Start with a clear, specific prompt
claude "add input validation to the /api/users POST endpoint \
  using pydantic models, return 422 for invalid data"

# 2. Use CLAUDE.md to reduce repetitive instructions
# Instead of saying "use pytest" every time, put it in CLAUDE.md

# 3. Let Claude explore before prescribing solutions
claude "there's a bug where login fails intermittently, investigate"
# Better than: "fix line 42 in auth.py"

# 4. Use /compact for long sessions
# Prevents context window exhaustion

# 5. Review changes before accepting
# Claude shows diffs - take time to review them

# 6. Use permissions to build trust gradually
# Start restrictive, add to allow list as patterns prove safe

# 7. Combine with git for safety
# Work on branches, commit frequently, easy to revert
```

Common workflows:

```bash
# Bug investigation and fix
claude "users report 500 errors on the dashboard. investigate and fix."

# Code review
claude /review

# Test writing
claude "write comprehensive tests for src/services/payment.py"

# Refactoring
claude "refactor the user module to use the repository pattern"

# Documentation
claude "add docstrings to all public functions in src/api/"

# Migration
claude "migrate from Flask to FastAPI, preserving all endpoints"
```

---

## Summary

Claude Code is Anthropic's terminal-based AI coding assistant that operates as an autonomous agent within your development environment. Key takeaways:

- **Installation**: via npm, authenticate with Anthropic account or API key
- **CLAUDE.md**: project instructions that persist across conversations
- **Slash commands**: /compact, /commit, /review, /init, and more
- **Skills**: modular capabilities for specialized tasks
- **Hooks**: pre/post tool execution scripts for validation and automation
- **MCP servers**: extend Claude with external tools and data sources
- **Permissions**: fine-grained control over what Claude can do
- **Headless mode**: run in CI/CD pipelines and automation scripts
- **IDE integration**: VS Code extension for a GUI experience

---

## Next Steps

- Create a CLAUDE.md file for your main projects using `/init`
- Configure permissions in `.claude/settings.json` for your workflow
- Explore MCP servers for your common data sources
- Set up hooks for automatic linting and formatting
- Try headless mode in a CI pipeline for automated code review
- Build custom skills for your team's specific workflows

---

## Additional Resources

- [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code)
- [Model Context Protocol Specification](https://modelcontextprotocol.io)
- [MCP Server Repository](https://github.com/modelcontextprotocol/servers)
- [Claude Code GitHub Action](https://github.com/anthropic-ai/claude-code-action)
- [Anthropic API Documentation](https://docs.anthropic.com)
- [Claude Code VS Code Extension](https://marketplace.visualstudio.com/items?itemName=anthropic.claude-code)
