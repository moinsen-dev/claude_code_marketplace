# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **Claude Code plugin marketplace** that provides specialized tools, agents, and workflows for development. The marketplace contains three main plugins:

1. **dev-tools**: Essential development utilities (code review, refactoring, debugging, social media generation)
2. **file-guardian**: Protection system preventing accidental edits to sensitive files and blocking unsolicited markdown summaries
3. **code-quality-guardian**: Architectural advisor that prevents bloated files and incomplete code (TODOs)

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

The guardian plugins use Claude Code's **PreToolUse hooks** to intercept file operations before they execute:

**file-guardian hooks:**
- Intercepts `Edit|Write|MultiEdit` → validates against `.claude/forbidden_paths.txt` blacklist
- Intercepts `Write` → validates markdown files against unsolicited summary patterns

**code-quality-guardian hooks:**
- Intercepts `Write|Edit|MultiEdit` → validates file size against `.claude/quality_config.json` thresholds
- Checks for TODO/FIXME/HACK comments if `block_todos: true`

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

# Install a specific plugin for testing
/plugin install dev-tools@claude-code-marketplace
/plugin install file-guardian@claude-code-marketplace
/plugin install code-quality-guardian@claude-code-marketplace
```

### Plugin Commands

**file-guardian:**
```bash
/protect <pattern>           # Add file/pattern to blacklist
/unprotect <pattern>         # Remove from blacklist
/protect list                # View protected files
```

**code-quality-guardian:**
```bash
/quality-config              # View current size thresholds
```

**dev-tools:**
```bash
/code-review                 # Comprehensive code review
/refactor                    # Intelligent refactoring assistance
/debug                       # Systematic debugging
/social-media [--platform <name>] [--language <lang>]  # Generate social posts
```

## Important Constraints

### File Protection (file-guardian)

The **file-guardian** plugin actively blocks edits to:
- Sensitive files (`.env`, credentials, keys)
- Lock files (`package-lock.json`, `pubspec.lock`)
- Build artifacts (`node_modules/`, `build/`, `dist/`)
- Git internals (`.git/`)

It also **blocks unsolicited markdown files** that look like summaries (SUMMARY.md, RECAP.md, CHANGES.md) unless explicitly requested.

### Code Quality Enforcement (code-quality-guardian)

The **code-quality-guardian** plugin blocks files that:
- Exceed line count thresholds (800 lines for .dart/.py/.ts/.js, 600 for .tsx/.jsx/.vue)
- Contain TODO/FIXME/HACK/XXX/TEMP/TMP comments (when `block_todos: true`)

**When blocked**, suggest breaking files into smaller modules following domain-driven design principles.

## Configuration Files

User-configurable files in `.claude/` directory:

- **forbidden_paths.txt**: File patterns to protect (one per line, supports globs)
- **file_guardian_config.json**: Markdown blocking settings
- **quality_config.json**: File size thresholds and TODO blocking settings

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
