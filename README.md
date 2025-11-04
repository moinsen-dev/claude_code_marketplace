# Claude Code Marketplace

A custom marketplace for Claude Code plugins, providing specialized tools and workflows to enhance your development experience.

## 📋 Table of Contents

- [Overview](#overview)
- [Why Use This Marketplace?](#why-use-this-marketplace)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Available Plugins](#available-plugins)
  - [🛠️ Dev Tools](#️-dev-tools)
  - [🛡️ Guard](#️-guard)
- [How the Guard Plugin Works](#how-the-guard-plugin-works)
- [Creating Your Own Plugins](#creating-your-own-plugins)
- [Development](#development)

## Overview

This marketplace focuses on **quality and safety** through intelligent automation:

- 🛠️ **Dev Tools** - Essential development utilities (code review, refactoring, debugging, social media)
- 🛡️ **Guard** - Unified protection system with 7 guardians for code quality, security, and maintainability

**Philosophy:** Prevention over correction. Use hooks to stop problems before they happen, not after.

## Why Use This Marketplace?

### Without Guard Plugin:
- ❌ Claude might accidentally edit `.env` or `package-lock.json`
- ❌ Claude creates annoying `SUMMARY.md` files after every task
- ❌ Claude generates 1000+ line monolithic files
- ❌ Claude leaves TODO comments instead of implementing features
- ❌ Claude edits generated files (*.g.dart, *.freezed.dart) instead of source files
- ❌ Mixed concerns and hard-to-maintain code

### With Guard Plugin:
- ✅ **7 guardians** protecting your codebase automatically
- ✅ Sensitive files are automatically protected (secrets, lock files, .git/)
- ✅ No more unnecessary summary files
- ✅ Enforced modular architecture with size limits per file type
- ✅ Complete, production-ready implementations (no TODOs)
- ✅ Generated files protected with helpful redirection to source files
- ✅ Flexible override system (disable/enable guardians as needed)
- ✅ Package manager guidance (warns when editing manifests directly)

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
/plugin install guard@claude-code-marketplace

# Or install individually
/plugin install guard@claude-code-marketplace
```

Initialize Guard in your project:

```bash
# Initialize guard with default protections
/guard:init
```

Then start using guard commands:

```bash
# View all guardian statuses
/guard:status

# Check quality configuration
/guard:config

# Protect additional files
/guard:protect mysecret.yaml

# Disable a guardian when needed
/guard:disable markdown-control
```

The Guard plugin works automatically with zero configuration after `/guard:init`! 🎉

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

### 🛡️ Guard
**Unified protection system with 7 independent guardians for comprehensive codebase security and quality.**

**The Problem:** Without protection, Claude might:
- Accidentally edit `.env` files, `package-lock.json`, or other sensitive files
- Create annoying `SUMMARY.md` files after every task
- Generate 1000+ line monolithic files that are hard to maintain
- Leave TODO comments instead of implementing complete features
- Edit generated files (*.g.dart, *.freezed.dart) instead of source files
- Use wrong package managers or edit manifests directly

**The Solution:** Guard uses Claude Code's hook system with 7 specialized guardians that intercept and block problematic operations **before** they happen.

---

## The 7 Guardians

### 1️⃣ File Protection Guardian
Protects sensitive files using blacklist pattern matching.

**Blocks:**
- Environment files (`.env`, `.env.*`)
- Secrets (`*.key`, `*.pem`, `*credentials*.json`)
- Lock files (`package-lock.json`, `yarn.lock`, `pubspec.lock`, etc.)
- Git internals (`.git/`)
- Build artifacts (`node_modules/`, `build/`, `dist/`, `.dart_tool/`)
- Database files (`*.db`, `*.sqlite`)

**Commands:**
```bash
/guard:protect mysecret.yaml    # Add protection
/guard:protect *.secret          # Pattern matching
/guard:protect list              # View all protections
/guard:unprotect build/          # Remove protection
```

---

### 2️⃣ Markdown Control Guardian
Blocks unsolicited markdown summary files.

**Blocks:**
- `SUMMARY.md`, `RECAP.md`, `REPORT.md`, `STATUS.md`
- Files with summary content patterns
- Auto-generated documentation

**Allows:**
- User-requested markdown files
- Documentation in `docs/` directory
- Standard files (`README.md`, `CHANGELOG.md`)

---

### 3️⃣ Code Quality Guardian
Enforces file size limits and blocks incomplete code.

**Default Thresholds:**
| File Type | Max Lines |
|-----------|-----------|
| `.tsx`, `.jsx`, `.vue` | 600 |
| `.dart`, `.py`, `.ts`, `.js` | 800 |
| `.java`, `.go`, `.rs` | 1000 |
| `.md`, `.txt` | 5000 |

**Blocks:**
- Files exceeding size limits
- TODO/FIXME/HACK/XXX/TEMP/TMP comments
- Suggests refactoring with domain-driven design

**Commands:**
```bash
/guard:config    # View thresholds and settings
```

---

### 4️⃣ Generated File Protection Guardian
Prevents edits to auto-generated files.

**Protects:**
- Dart build_runner files (`*.g.dart`, `*.freezed.dart`, `*.gr.dart`)
- Flutter localization (`app_localizations*.dart`)
- Protocol Buffers (`*.pb.dart`, `*.pbjson.dart`)

**When Blocked:**
- Shows exact source file pattern
- Provides regeneration command
- Explains why edits will be lost

---

### 5️⃣ Tool Guardian
Enforces correct package manager usage (disabled by default).

**Example:**
- Blocks `npm install` → suggests `pnpm install`
- Blocks `pip install` → suggests `uv add`
- Word-boundary matching (won't block "npm" in strings)

**Enable:**
```json
{
  "tool_guardian": {
    "enabled": true,
    "disallowed_tools": {
      "npm": {"preferred": "pnpm"}
    }
  }
}
```

---

### 6️⃣ Package Guardian
Warns when editing package manifests directly (warning-only).

**Detects:**
- Direct edits to `package.json`, `pubspec.yaml`, `requirements.txt`
- Version patterns like `"lodash": "^4.17.21"`

**Suggests:**
- Use package manager commands instead
- `pnpm add lodash@^4.17.21`
- `dart pub add http:^1.0.0`

---

### 7️⃣ Command Guardian
Blocks specific bash commands based on project configuration (disabled by default).

**Blocks:**
- Configured commands that shouldn't run in this project
- Custom patterns: exact match, starts_with, contains, or regex
- Examples: `flutter run`, `rm -rf /`, or any other command

**When Blocked:**
- Shows the command that was blocked
- Displays the custom reason from configuration
- Provides instructions to allow or configure

**Enable & Configure:**
```json
{
  "command_guardian": {
    "enabled": true,
    "forbidden_commands": [
      {
        "pattern": "flutter run",
        "match_type": "exact",
        "reason": "I want to test manually in VSCode"
      },
      {
        "pattern": "rm -rf",
        "match_type": "starts_with",
        "reason": "Destructive command - please confirm first"
      }
    ]
  }
}
```

**Match Types:**
- `exact`: Command must match exactly
- `starts_with`: Command must start with pattern
- `contains`: Command must contain pattern
- `regex`: Custom regex pattern

---

## Guard Features

### 🎛️ Flexible Override System
Enable/disable guardians as needed:

```bash
# View status
/guard:status

# Disable individual guardian
/guard:disable markdown-control

# Disable all guardians
/guard:disable all

# Re-enable
/guard:enable markdown-control
/guard:enable all
```

**State persists** across sessions in `.claude/guard/overrides.json`

---

### 🛠️ Specialized Agents

**refactoring-architect** - Expert at breaking down large files
- Domain-driven design principles
- Separation of concerns
- Module boundaries

**markdown-splitter** - Intelligent markdown file splitting
- Creates index with table of contents
- Section files with navigation
- Preserves formatting and structure

---

### 📋 All Commands

| Command | Description |
|---------|-------------|
| `/guard:init` | Initialize guard with defaults |
| `/guard:status` | View all guardian states |
| `/guard:config` | View quality thresholds |
| `/guard:protect <pattern>` | Add file protection |
| `/guard:unprotect <pattern>` | Remove protection |
| `/guard:disable <guardian\|all>` | Disable guardian(s) |
| `/guard:enable <guardian\|all>` | Enable guardian(s) |
| `/guard:split-markdown <file>` | Split large markdown |

---

### ⚙️ Configuration Files

All configs in `.claude/guard/`:

- **`forbidden_paths.txt`** - Blacklist patterns (23+ defaults)
- **`file_guardian_config.json`** - Markdown blocking settings
- **`quality_config.json`** - Size thresholds, TODO blocking, tool/package settings
- **`overrides.json`** - Guardian enable/disable state

---

### 🎯 Error Message Quality

Guard provides **exceptional error messages** with:
- 🛡️ Clear visual indicators (emojis)
- 📄 Exact file paths and line numbers
- 💡 Actionable suggestions (commands to run)
- ⚙️ Configuration options
- Educational content (explains WHY)

**Example:**
```
🚫 CODE QUALITY GUARDIAN: TODO/FIXME comments detected!
   📄 File: user_service.ts
   ⚠️  Found 1 incomplete marker(s):
      Line 42: // TODO: Add error handling

   💡 Code should be complete and production-ready
   🤖 Try: Ask me to complete these implementations
   ⚙️  To allow TODOs: Set 'block_todos': false in quality_config.json
```

---

### 📊 Test Results

Guard has been comprehensively tested:
- ✅ **20/20 tests passed (100%)**
- ✅ All 7 guardians working perfectly
- ✅ Error message quality: 9.8/10
- ✅ Zero critical bugs
- ✅ **Overall Grade: A+ (95/100)**

See `test-guard-plugin/COMPREHENSIVE_TEST_REPORT.md` for full results.

---

**Installation:**
```bash
/plugin install guard@claude-code-marketplace
/guard:init
```

**Philosophy:** Prevention over correction. Guard stops problems before they happen through intelligent hooks and clear, educational error messages.

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

## How the Guard Plugin Works

Guard uses Claude Code's **PreToolUse hook system** to intercept file operations before they execute:

### Hook Architecture

1. **4 Hook Groups** - Different matchers for different operations:
   - `Bash` → validate_tool_usage.py (Tool Guardian)
   - `Read|Write|Edit|MultiEdit` → validate_generated_files.py (Generated Files Guardian)
   - `Write|Edit|MultiEdit` → check_file_size.py, validate_blacklist.py, validate_package_edits.py
   - `Write` → validate_markdown.py (Markdown Control Guardian)

2. **Python Validators** (3.11+, zero dependencies):
   - Check file paths against blacklist patterns
   - Validate file size against thresholds
   - Detect TODO/FIXME comments
   - Identify generated files
   - Detect markdown summaries
   - Check package manifest edits

3. **Guardian Override Check**:
   - Each validator checks `.claude/guard/overrides.json`
   - If guardian disabled, allow operation
   - If guardian enabled, enforce rules

4. **Block or Allow**:
   - Return error with helpful message (block)
   - Return success (allow)

This means problems are **prevented** rather than **corrected** - a much better developer experience!

**Example Flow:**
```
Claude: "I'll create user_service.dart with 1200 lines..."
   ↓
Hook intercepts Write operation
   ↓
check_file_size.py runs
   ↓
Checks Code Quality Guardian status (enabled)
   ↓
Counts lines (1200 > 800 threshold for .dart)
   ↓
Returns error with refactoring guidance
   ↓
Claude: "I'll break this into smaller modules instead..."
```

**Another Example:**
```
Claude: "I'll edit the .env file..."
   ↓
Hook intercepts Write operation
   ↓
validate_blacklist.py runs
   ↓
Checks File Protection Guardian status (enabled)
   ↓
Matches .env against forbidden_paths.txt
   ↓
Returns error: "🛡️ FILE GUARDIAN: Edit blocked"
   ↓
Claude: "The .env file is protected. I'll guide you instead."
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
