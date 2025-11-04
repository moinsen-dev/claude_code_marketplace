# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **Claude Code plugin marketplace** that provides specialized tools, agents, and workflows for development. The marketplace contains two main plugins:

1. **dev-tools**: Essential development utilities (code review, refactoring, debugging, social media generation)
2. **guard**: Unified guardian that protects sensitive files, enforces code quality, controls package management, and provides granular enable/disable controls

## Architecture

### Plugin Structure

Each plugin follows this standard layout:
```
plugins/<plugin-name>/
├── .claude-plugin/
│   └── plugin.json           # Plugin metadata
├── commands/                  # Slash commands (.md files)
├── agents/                    # Specialized AI agents (.md files)
├── hooks/
│   └── hooks.json            # Hook configurations
├── scripts/                   # Hook implementation scripts (Python)
├── templates/                # Default config templates
└── README.md                 # Plugin documentation
```

### Hook System Architecture

The **guard** plugin uses Claude Code's **PreToolUse hooks** to intercept file operations before they execute:

**Guard hooks:**
- Intercepts `Edit|Write|MultiEdit` → validates against `.claude/guard/forbidden_paths.txt` blacklist
- Intercepts `Write` → validates markdown files against unsolicited summary patterns
- Intercepts `Write|Edit|MultiEdit` → validates file size against `.claude/guard/quality_config.json` thresholds
- Intercepts `Write|Edit|MultiEdit` → warns about package manifest direct edits
- Intercepts `Bash` → enforces tool usage (e.g., pnpm over npm)
- Intercepts `Read|Write|Edit|MultiEdit` → protects generated files

Each hook checks `.claude/guard/overrides.json` to see if the guardian is enabled before running.

Hook scripts are Python 3.11+ using inline script metadata (PEP 723).

### Marketplace Configuration

The `.claude-plugin/marketplace.json` file registers plugins with Claude Code:
- Defines plugin metadata (name, version, author, description)
- Points to plugin source directories
- Includes keywords and categories for discoverability

## Key Development Commands

### Testing Plugins Locally

```bash
# Add marketplace to Claude Code
/plugin marketplace add /path/to/claude_code_marketplace

# Install plugins for testing
/plugin install dev-tools@claude-code-marketplace
/plugin install guard@claude-code-marketplace
```

### Plugin Commands

**guard:**
```bash
/guard:init                         # Initialize guard plugin
/guard:protect <pattern>            # Add file/pattern to blacklist
/guard:unprotect <pattern>          # Remove from blacklist
/guard:config                       # View quality thresholds
/guard:split-markdown <file>        # Split large markdown files
/guard:disable <guardian>           # Temporarily disable a guardian
/guard:enable <guardian>            # Re-enable a guardian
/guard:status                       # View guardian status
```

**dev-tools:**
```bash
/code-review                 # Comprehensive code review
/refactor                    # Intelligent refactoring assistance
/debug                       # Systematic debugging
/social-media [--platform <name>] [--language <lang>]  # Generate social posts
```

## Important Constraints

### Guard Plugin

The **guard** plugin provides multiple protection mechanisms:

**File Protection:**
- Blocks edits to sensitive files (`.env`, credentials, keys)
- Blocks edits to lock files (`package-lock.json`, `pubspec.lock`)
- Blocks edits to build artifacts (`node_modules/`, `build/`, `dist/`)
- Blocks edits to git internals (`.git/`)
- Blocks unsolicited markdown summaries (SUMMARY.md, RECAP.md)

**Code Quality:**
- Blocks files exceeding line thresholds (800 for .dart/.py/.ts/.js, 600 for .tsx/.jsx/.vue)
- Blocks TODO/FIXME/HACK/XXX/TEMP/TMP comments (when `block_todos: true`)
- Suggests splitting large markdown files (>2000 lines)

**Generated Files:**
- Warns when reading generated files (*.g.dart, localization, etc.)
- Blocks edits to generated files, redirects to source files

**Package Management:**
- Warns when editing package manifests directly (package.json, pubspec.yaml, etc.)
- Suggests using package manager commands instead

**Tool Usage:**
- Enforces preferred package managers (e.g., pnpm over npm, uv over pip)
- Configurable per project

**Temporary Disabling:**
- Use `/guard:disable <guardian>` to temporarily disable a specific guardian
- Use `/guard:enable <guardian>` to re-enable
- Use `/guard:status` to view current state

**When blocked**, suggest breaking files into smaller modules following domain-driven design principles.

## Configuration Files

User-configurable files in `.claude/guard/` directory:

- **forbidden_paths.txt**: File patterns to protect (one per line, supports globs)
- **file_guardian_config.json**: Markdown blocking settings
- **quality_config.json**: File size thresholds, TODO blocking, generated files, tool/package guardian settings
- **overrides.json**: Guardian enable/disable state (persists across sessions)

Hooks are stored at `.claude/hooks.json` for compatibility with other plugins.

## Development Workflow

When creating or modifying plugins:

1. **Test hooks locally** by triggering the operations they intercept
2. **Verify Python scripts** use PEP 723 inline metadata for dependencies
3. **Update marketplace.json** with accurate version numbers and metadata
4. **Document commands** in the plugin's README.md
5. **Keep plugin.json synchronized** with marketplace.json entries

## Philosophy

This marketplace embodies architectural best practices:
- **Prevention over correction**: Hooks stop problems before they happen
- **Guidance over restriction**: Error messages teach better patterns
- **Configuration over convention**: Users can customize thresholds
- **Automation over manual review**: Scripts enforce standards consistently
