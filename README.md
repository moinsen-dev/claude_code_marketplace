# Claude Code Marketplace

A custom marketplace for Claude Code plugins, providing specialized tools and workflows to enhance your development experience.

## 📋 Table of Contents

- [Overview](#overview)
- [Why Use This Marketplace?](#why-use-this-marketplace)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Available Plugins](#available-plugins)
  - [🛠️ Dev Tools](#️-dev-tools)
  - [🛡️ File Guardian](#️-file-guardian)
  - [📏 Code Quality Guardian](#-code-quality-guardian)
- [How the Guardian Plugins Work](#how-the-guardian-plugins-work)
- [Creating Your Own Plugins](#creating-your-own-plugins)
- [Development](#development)

## Overview

This marketplace focuses on **quality and safety** through intelligent automation:

- 🛠️ **Dev Tools** - Essential development utilities (code review, refactoring, debugging, social media)
- 🛡️ **File Guardian** - Protect sensitive files and prevent unwanted markdown summaries
- 📏 **Code Quality Guardian** - Enforce architectural best practices and prevent bloated code

**Philosophy:** Prevention over correction. Use hooks to stop problems before they happen, not after.

## Why Use This Marketplace?

### Without These Plugins:
- ❌ Claude might accidentally edit `.env` or `package-lock.json`
- ❌ Claude creates annoying `SUMMARY.md` files after every task
- ❌ Claude generates 1000+ line monolithic files
- ❌ Claude leaves TODO comments instead of implementing features
- ❌ Mixed concerns and hard-to-maintain code

### With These Plugins:
- ✅ Sensitive files are automatically protected
- ✅ No more unnecessary summary files
- ✅ Enforced modular architecture with focused files
- ✅ Complete, production-ready implementations
- ✅ Better code quality through architectural guidance

## What are Claude Code Plugins?

Claude Code plugins are collections of:
- **Slash commands**: Custom shortcuts for frequently-used operations
- **Agents**: Purpose-built AI agents for specialized development tasks
- **MCP servers**: Connections to tools and data sources through the Model Context Protocol
- **Hooks**: Customizations of Claude Code's behavior at key workflow points

## Installation

To add this marketplace to your Claude Code installation:

```bash
/plugin marketplace add moinsen-dev/claude_code_marketplace
```

Or if you have cloned this repository locally:

```bash
/plugin marketplace add /path/to/claude_code_marketplace
```

## Quick Start

After adding the marketplace, install the plugins you need:

```bash
# Install all plugins
/plugin install dev-tools@claude-code-marketplace
/plugin install file-guardian@claude-code-marketplace
/plugin install code-quality-guardian@claude-code-marketplace

# Or install them one by one as needed
/plugin install file-guardian@claude-code-marketplace
```

Then start using them immediately:

```bash
# Protect your .env file
/protect .env

# Review your code
/code-review

# Check quality thresholds
/quality-config
```

The guardian plugins work automatically with zero configuration! 🎉

## Available Plugins

### 🛠️ Dev Tools
Essential development tools and utilities for common coding tasks.

**Commands:**
- `/code-review` - Comprehensive code review with quality, security, and best practices analysis
- `/refactor` - Intelligent code refactoring while preserving functionality
- `/debug` - Systematic debugging assistance
- `/social-media` - Generate professional social media posts for your project

**Agents:**
- `test-generator` - Generate comprehensive test suites

**Usage Example:**

```bash
# Generate a LinkedIn post in English (default)
/social-media

# Generate for a specific platform and language
/social-media --platform linkedin --language german
```

**Installation:**
```bash
/plugin install dev-tools@claude-code-marketplace
```

---

### 🛡️ File Guardian
Protect sensitive files from accidental edits and prevent unnecessary markdown summaries.

**The Problem:** Claude might accidentally edit your `.env` file, `package-lock.json`, or create annoying `SUMMARY.md` files listing what it just did.

**The Solution:** File Guardian uses hooks to intercept and block these operations before they happen.

**Features:**
- 🛡️ **Blacklist Protection** - Prevent edits to sensitive files using pattern matching
- 📝 **Markdown Control** - Block unsolicited summary/recap markdown files
- ⚡ **Automatic Blocking** - Hooks intercept operations before they happen
- 🎯 **Pattern Matching** - Support for globs, directories, and exact matches
- 📋 **Easy Management** - Slash commands to add/remove protections
- 🚀 **Zero Configuration** - Works with sensible defaults

**Commands:**
```bash
/protect list              # View protected files
/protect .env              # Protect specific file
/protect secrets/          # Protect directory
/protect *.key             # Protect by pattern
/unprotect .env.example    # Remove protection
```

**Default Protections:**
- Environment files (`.env`, `.env.*`)
- Secrets directory
- Credential files (`*.key`, `*.pem`, `*credentials*.json`)
- Lock files (`package-lock.json`, `pubspec.lock`, etc.)
- Git internals (`.git/`)
- Build artifacts (`build/`, `dist/`, `node_modules/`)

**Markdown Protection:**

File Guardian blocks unsolicited markdown files like:
- `SUMMARY.md`, `RECAP.md`, `CHANGES.md`
- `COMPLETION.md`, `OUTPUT.md`, `NOTES.md`
- Files with summary-like content ("I created the following files...")

Markdown files are **allowed** when:
- User explicitly requests them
- In documentation directories (`docs/`)
- Standard files (`README.md`, `CONTRIBUTING.md`, `CHANGELOG.md`)

**Configuration:** `.claude/forbidden_paths.txt`, `.claude/file_guardian_config.json`

**Installation:**
```bash
/plugin install file-guardian@claude-code-marketplace
```

---

### 📏 Code Quality Guardian
Prevent bloated files and enforce architectural best practices automatically.

**The Problem:** Without guidance, LLMs might create:
- Files that are too large (1000+ lines)
- Mixed concerns (data + logic + UI in one file)
- Incomplete code with TODO/FIXME comments
- Hard to maintain god objects

**The Solution:** Code Quality Guardian acts as an architectural advisor, blocking oversized files and incomplete code before they're created.

**Features:**
- 📏 **Automatic Size Checking** - Intercepts file writes before they happen
- 🚫 **TODO/FIXME Blocking** - Prevents incomplete code with TODO comments
- 🎯 **Smart Thresholds** - Different limits for different file types
- 🤖 **Refactoring Agent** - Expert guidance for breaking up large files
- ⚙️ **Configurable** - Customize thresholds per project
- 🚀 **Zero Config** - Works with sensible defaults

**Commands:**
```bash
/quality-config            # View current thresholds
```

**Default Thresholds:**

| File Type | Max Lines | Rationale |
|-----------|-----------|-----------|
| `.dart`, `.py`, `.ts`, `.js` | 800 | General code files |
| `.tsx`, `.jsx`, `.vue` | 600 | UI components (smaller = better) |
| `.java`, `.go` | 1000 | Larger files common in these langs |
| `.md`, `.txt` | 5000 | Documentation can be longer |
| `.json` | 2000 | Data files |
| Default | 1000 | Catch-all |

**What Gets Blocked:**

1. **Files exceeding size limits** with suggestions for domain-driven refactoring
2. **TODO/FIXME/HACK comments** when `block_todos: true`:
   - `TODO` - Unfinished implementations
   - `FIXME` - Known issues
   - `HACK` - Temporary solutions
   - `XXX`, `TEMP`, `TMP` - Other incomplete markers

**When Blocked:**

Claude receives guidance to:
- Break into smaller, focused modules
- Use domain-driven design principles
- Separate concerns (data, logic, UI)
- Complete implementations instead of leaving TODOs

**Configuration:** `.claude/quality_config.json`

```json
{
  "default": 1000,
  "block_todos": true,
  "todo_patterns": ["TODO", "FIXME", "HACK", "XXX", "TEMP", "TMP"],
  "extensions": {
    ".dart": 600,
    ".py": 500,
    ".tsx": 400
  }
}
```

**Philosophy:** Based on Domain-Driven Design principles - bounded contexts, single responsibility, separation of concerns, testability, and maintainability.

**Installation:**
```bash
/plugin install code-quality-guardian@claude-code-marketplace
```

## Creating Your Own Plugins

### Plugin Structure

Each plugin should follow this structure:

```
plugins/your-plugin/
├── .claude-plugin/
│   └── plugin.json          # Plugin metadata (optional)
├── commands/                 # Slash commands (markdown files)
│   ├── command1.md
│   └── command2.md
├── agents/                   # AI agents (markdown files)
│   └── agent1.md
└── hooks/                    # Event handlers (optional)
    └── hook1.md
```

### Plugin Metadata (plugin.json)

```json
{
  "name": "your-plugin",
  "version": "1.0.0",
  "description": "Plugin description",
  "author": {
    "name": "Your Name",
    "email": "[email protected]"
  },
  "keywords": ["keyword1", "keyword2"],
  "category": "development"
}
```

### Adding to Marketplace

1. Create your plugin in the `plugins/` directory
2. Update `.claude-plugin/marketplace.json` to include your plugin:

```json
{
  "name": "your-plugin",
  "source": "./plugins/your-plugin",
  "description": "Plugin description",
  "version": "1.0.0",
  "author": {
    "name": "Your Name"
  }
}
```

### Commands

Commands are markdown files that contain prompts for Claude. The file name becomes the command name.

Example `commands/hello.md`:
```markdown
# Hello Command

You are a friendly assistant. Greet the user warmly and ask how you can help them today.
```

Usage: `/hello`

### Agents

Agents are specialized AI assistants defined in markdown files with specific expertise and behaviors.

Example `agents/code-reviewer.md`:
```markdown
# Code Reviewer Agent

You are an expert code reviewer with 10+ years of experience...

## Your responsibilities:
- Review code for quality and best practices
- Identify potential bugs and security issues
- Suggest improvements
```

---

## How the Guardian Plugins Work

Both **File Guardian** and **Code Quality Guardian** use Claude Code's **hook system** to intercept operations before they execute:

### Hook Architecture

1. **PreToolUse Hooks** - Intercept `Write`, `Edit`, and `MultiEdit` operations
2. **Python Validators** - Check file content against rules (blacklist, size, TODOs)
3. **Block or Allow** - Return error message or allow operation to proceed

This means problems are **prevented** rather than **corrected** - a much better developer experience!

**Example Flow:**
```
Claude: "I'll create user_service.dart with 1200 lines..."
   ↓
Hook intercepts Write operation
   ↓
Python script checks file size (1200 > 800 line threshold)
   ↓
Hook blocks operation with helpful message
   ↓
Claude: "I'll break this into smaller modules instead..."
```

---

## Development

### Local Testing

1. Clone this repository
2. Add as a local marketplace:
   ```bash
   /plugin marketplace add /path/to/claude_code_marketplace
   ```
3. Install plugins:
   ```bash
   /plugin install dev-tools@claude-code-marketplace
   ```

### Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a new plugin or improve existing ones
3. Test your changes locally
4. Submit a pull request

## Resources

- [Claude Code Documentation](https://docs.claude.com/claude-code)
- [Plugin Development Guide](https://docs.claude.com/en/docs/claude-code/plugins)
- [Model Context Protocol](https://modelcontextprotocol.io)

## License

MIT License - see LICENSE file for details

## Support

For issues or questions:
- Open an issue on GitHub
- Visit [Claude Code Documentation](https://docs.claude.com/claude-code)

---

Built with Claude Code
