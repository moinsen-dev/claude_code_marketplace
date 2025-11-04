# Guard Plugin

Unified guardian that protects your codebase with file protection and code quality enforcement.

## Overview

The Guard plugin combines essential protection mechanisms:
1. **File Protection** - Prevents accidental edits to sensitive files and blocks unsolicited markdown summaries
2. **Code Quality** - Enforces file size limits and prevents incomplete code with TODO comments
3. **Package Management** - Warns when package manifests are edited directly instead of using package managers
4. **Tool Enforcement** - Ensures correct development tools are used (e.g., pnpm over npm)

## Features

### 🛡️ File Protection
- **Blacklist Protection** - Prevents edits to sensitive files using pattern matching
- **Markdown Control** - Blocks unsolicited summary/recap files
- **Pattern Matching** - Supports globs, directories, and exact matches
- **Easy Management** - Simple commands to add/remove protection

### 📏 Code Quality
- **Automatic Size Checking** - Intercepts file writes before they happen
- **TODO/FIXME Blocking** - Prevents incomplete code with markers
- **Smart Thresholds** - Different limits for different file types
- **Refactoring Agent** - Expert guidance for breaking down large files

### 📄 Markdown Splitter
- **Intelligent Splitting** - Automatically splits large markdown files
- **Context-Aware** - Creates manageable sections for LLM processing
- **Navigation System** - Generates index with TOC and bidirectional links
- **Preserves Structure** - Maintains formatting, code blocks, and links
- **Auto-Suggestion** - Offers to split when threshold exceeded

### 🔒 Generated File Protection
- **Smart Detection** - Identifies auto-generated files (*.g.dart, localization, etc.)
- **Edit Blocking** - Prevents accidental edits to generated code
- **Source Redirection** - Points to editable source files instead
- **Generation Commands** - Shows how to regenerate after editing sources
- **Read Warnings** - Allows reading for reference with helpful hints

### 🛠️ Tool Guardian
- **Package Manager Enforcement** - Ensures correct tool usage (pnpm over npm, uv over pip)
- **Strict Blocking** - Prevents disallowed tool commands
- **Clear Guidance** - Shows preferred tool and example commands
- **Project-Specific** - Configure per project's tooling preferences
- **Common Presets** - Built-in patterns for npm, pip, yarn, bun, and more

### 📦 Package Guardian
- **Smart Manifest Detection** - Recognizes package.json, pubspec.yaml, pyproject.toml, etc.
- **Version Pattern Analysis** - Detects when dependencies are being added with hardcoded versions
- **Package Manager Suggestions** - Shows the correct command for each package ecosystem
- **Warning-Only Mode** - Educates without blocking (allows operation to proceed)
- **Multi-Ecosystem Support** - npm/pnpm/yarn, pip/uv/poetry, Flutter, Go, Rust, and more

## Installation

```bash
# Install the plugin
/plugin install guard@claude-code-marketplace

# Initialize (one-time setup)
/guard:init
```

## Commands

### `/guard:init`
Initialize the plugin with default configurations.

### `/guard:protect <pattern>`
Add a file or pattern to the protection blacklist.

```bash
/guard:protect .env
/guard:protect secrets/
/guard:protect *.key
/guard:protect list    # View all protected patterns
```

### `/guard:unprotect <pattern>`
Remove a file or pattern from the blacklist.

```bash
/guard:unprotect .env.example
/guard:unprotect list    # View all protected patterns
```

### `/guard:config`
View and configure code quality thresholds.

### `/guard:split-markdown <file>`
Split a large markdown file into manageable sections.

```bash
/guard:split-markdown task.md
/guard:split-markdown docs/requirements.md
```

The splitter will:
- Analyze document structure
- Propose a split plan
- Create index file (00-<basename>.md)
- Generate section files (01-, 02-, etc.)
- Add navigation links
- Backup original file

## Configuration

All guard configuration files are located in `.claude/guard/`:

```
.claude/guard/
├── forbidden_paths.txt          # File protection blacklist
├── file_guardian_config.json    # Markdown control settings
├── quality_config.json          # Unified quality settings
├── overrides.json               # Guardian enable/disable state
└── (hooks are at .claude/hooks.json for compatibility)
```

### File Protection
**Location**: `.claude/guard/forbidden_paths.txt`, `.claude/guard/file_guardian_config.json`

**Default Protected Patterns**:
- Environment files (`.env`, `.env.*`)
- Secrets directory
- Credential files (`*.key`, `*.pem`, `*credentials*.json`)
- Lock files (`package-lock.json`, `yarn.lock`, etc.)
- Git internals (`.git/`)
- Build artifacts (`build/`, `dist/`, `node_modules/`)

### Code Quality
**Location**: `.claude/guard/quality_config.json`

**Default Thresholds**:
| File Type | Max Lines | Purpose |
|-----------|-----------|---------|
| `.dart`, `.py`, `.ts`, `.js` | 800 | Code files |
| `.tsx`, `.jsx`, `.vue` | 600 | UI components |
| `.java`, `.go`, `.rs` | 1000 | Compiled languages |
| `.md`, `.txt` | 5000 | Documentation |
| `.json` | 2000 | Data files |

**Example Configuration** (`.claude/guard/quality_config.json`):
```json
{
  "default": 1000,
  "block_todos": true,
  "todo_patterns": ["TODO", "FIXME", "HACK", "XXX", "TEMP", "TMP"],
  "extensions": {
    ".dart": 800,
    ".py": 800,
    ".ts": 800,
    ".tsx": 600
  },
  "markdown_splitter": {
    "enabled": true,
    "auto_suggest_threshold": 2000,
    "target_chunk_size": 800,
    "split_strategy": "headers",
    "preserve_original": true,
    "create_index": true
  }
}
```

### Markdown Splitter
**Location**: `.claude/guard/quality_config.json` (markdown_splitter section)

**Configuration Options**:
- **`enabled`** (default: true) - Enable/disable markdown splitting suggestions
- **`auto_suggest_threshold`** (default: 2000) - Line count to trigger split suggestion
- **`target_chunk_size`** (default: 800) - Target lines per section (for "smart" strategy)
- **`split_strategy`** (default: "headers") - "headers" or "smart" splitting
- **`preserve_original`** (default: true) - Keep backup of original file
- **`create_index`** (default: true) - Generate index file with TOC

**Split Strategies**:
- **headers**: Split at each top-level header (# title) - preserves logical structure
- **smart**: Group sections to target chunk size - creates more even sections

### Generated File Protection
**Location**: `.claude/guard/quality_config.json` (generated_files section)

**Configuration Format**:
```json
{
  "generated_files": {
    "enabled": true,
    "mappings": [
      {
        "pattern": "lib/l10n/app_localizations*.dart",
        "source": "lib/l10n/app_*.arb",
        "description": "Flutter localization files",
        "generate_command": "flutter gen-l10n"
      },
      {
        "pattern": "**/*.g.dart",
        "source": "**/*.dart",
        "description": "Dart code generation (build_runner)",
        "generate_command": "dart run build_runner build"
      },
      {
        "pattern": "**/*.freezed.dart",
        "source": "**/*.dart",
        "description": "Freezed immutable models",
        "generate_command": "dart run build_runner build"
      }
    ]
  }
}
```

**Mapping Fields**:
- **`pattern`** - Glob pattern matching generated files (supports * and **)
- **`source`** - Pattern for source files to edit instead
- **`description`** - Human-readable description of what's generated
- **`generate_command`** - Command to regenerate files after editing sources

**Common Patterns**:
| Pattern | Source | Description | Command |
|---------|--------|-------------|---------|
| `lib/l10n/app_localizations*.dart` | `lib/l10n/app_*.arb` | Flutter i18n | `flutter gen-l10n` |
| `**/*.g.dart` | `**/*.dart` | build_runner | `dart run build_runner build` |
| `**/*.freezed.dart` | `**/*.dart` | Freezed models | `dart run build_runner build` |
| `**/*.gr.dart` | `**/*.dart` | Auto Route | `dart run build_runner build` |
| `**/*.pb.dart` | `**/*.proto` | Protobuf | `protoc --dart_out=. *.proto` |

### Tool Guardian
**Location**: `.claude/guard/quality_config.json` (tool_guardian section)

**Configuration Format**:
```json
{
  "tool_guardian": {
    "enabled": true,
    "tool_replacements": [
      {
        "tool_name": "npm",
        "preferred_tool": "pnpm",
        "patterns": ["npm install", "npm i ", "npm add", "npm ci", "npm run"],
        "reason": "This project uses pnpm for faster, disk-efficient package management",
        "examples": [
          "pnpm install",
          "pnpm add [package]",
          "pnpm run [script]"
        ]
      },
      {
        "tool_name": "pip",
        "preferred_tool": "uv",
        "patterns": ["pip install", "pip3 install", "python -m pip"],
        "reason": "This project uses uv for 10-100x faster Python package management",
        "examples": [
          "uv pip install [package]",
          "uv run python [script]"
        ]
      }
    ]
  }
}
```

**Configuration Fields**:
- **`enabled`** - Enable/disable tool guardian (default: false, enable per project)
- **`tool_name`** - Name of the disallowed tool (for display)
- **`preferred_tool`** - Tool that should be used instead
- **`patterns`** - List of command patterns to detect and block
- **`reason`** - Explanation why this tool is preferred
- **`examples`** - Common usage examples with the preferred tool

**Common Tool Replacements**:
| Disallowed | Preferred | Use Case |
|-----------|-----------|----------|
| npm | pnpm | Faster, disk-efficient Node.js packages |
| npm | bun | Ultra-fast JavaScript runtime & package manager |
| npm | yarn | Deterministic, reliable Node.js packages |
| pip | uv | 10-100x faster Python package management |
| pip | poetry | Python dependency management & packaging |
| python | uv run python | Managed Python environments with uv |

**Important Notes**:
- Tool Guardian is **disabled by default** - enable it per project
- Patterns use simple string matching (case-insensitive)
- Blocks commands that contain the pattern anywhere
- Set `enabled: true` in quality_config.json to activate

### Package Guardian
**Location**: `.claude/guard/quality_config.json` (package_guardian section)

**Configuration Format**:
```json
{
  "package_guardian": {
    "enabled": true,
    "package_managers": [
      {
        "name": "npm",
        "manifest_files": ["package.json"],
        "add_command": "npm install {package}",
        "add_dev_command": "npm install --save-dev {package}",
        "description": "Node.js package manager"
      },
      {
        "name": "pub",
        "manifest_files": ["pubspec.yaml"],
        "add_command": "flutter pub add {package}",
        "add_dev_command": "flutter pub add --dev {package}",
        "description": "Dart/Flutter package manager"
      }
    ],
    "detection_patterns": [
      "\"version\"\\s*:\\s*\"\\d+\\.\\d+",
      "version\\s*=\\s*\"\\d+\\.\\d+",
      "version:\\s*\\^?\\d+\\.\\d+",
      "@\\d+\\.\\d+"
    ]
  }
}
```

**Configuration Fields**:
- **`enabled`** - Enable/disable package guardian (default: true)
- **`package_managers`** - List of supported package managers
  - **`name`** - Display name of the package manager
  - **`manifest_files`** - Array of manifest file patterns to watch
  - **`add_command`** - Command template for adding packages
  - **`add_dev_command`** - Optional command for dev dependencies
  - **`description`** - Human-readable description
- **`detection_patterns`** - Regex patterns to detect version additions

**Supported Package Managers** (Built-in):
| Ecosystem | Manifest Files | Package Managers |
|-----------|---------------|------------------|
| Node.js | package.json | npm, pnpm, yarn, bun |
| Python | requirements.txt, pyproject.toml | pip, uv, poetry |
| Dart/Flutter | pubspec.yaml | pub (flutter pub) |
| Go | go.mod | go modules |
| Rust | Cargo.toml | cargo |
| Ruby | Gemfile | bundler |
| PHP | composer.json | composer |
| Java | pom.xml, build.gradle | maven, gradle |
| .NET | *.csproj | dotnet (NuGet) |

**Important Notes**:
- Package Guardian is **enabled by default**
- Issues **warnings only** - does not block operations
- Educates AI agents about best practices
- Template config includes all major package ecosystems
- Customize per project needs in `.claude/guard/quality_config.json`

## Temporarily Disabling Guardians

Each guardian can be individually enabled or disabled without modifying configuration files. Changes persist across sessions until manually reverted.

### Commands

**Disable a guardian:**
```bash
/guard:disable <guardian-name>
/guard:disable all
```

**Re-enable a guardian:**
```bash
/guard:enable <guardian-name>
/guard:enable all
```

**View current status:**
```bash
/guard:status
```

### Available Guardians

| Guardian ID | Name | What It Does |
|-------------|------|--------------|
| `file-protection` | File Protection | Prevents editing blacklisted files |
| `markdown-control` | Markdown Control | Blocks unsolicited markdown summaries |
| `code-quality` | Code Quality | Enforces file size and TODO limits |
| `generated-files` | Generated File Protection | Protects auto-generated files |
| `tool-guardian` | Tool Guardian | Enforces package manager usage |
| `package-guardian` | Package Guardian | Warns about manifest edits |

### Example Usage

```bash
# Temporarily disable package warnings while doing bulk edits
/guard:disable package-guardian

# Edit package.json directly
# ... make changes ...

# Re-enable when done
/guard:enable package-guardian

# Check current status
/guard:status
```

### How Override State Is Stored

- **Location**: `.claude/guard/overrides.json`
- **Format**: JSON with boolean flags per guardian
- **Persistence**: Survives Claude Code restarts
- **Default**: All guardians enabled

**Example overrides.json:**
```json
{
  "file-protection": true,
  "markdown-control": true,
  "code-quality": true,
  "generated-files": true,
  "tool-guardian": true,
  "package-guardian": false
}
```

## How It Works

Guard uses Claude Code's **PreToolUse hooks** to intercept file operations before they execute:

1. **File Protection Hooks**:
   - `Write|Edit|MultiEdit` → Validates against blacklist patterns
   - `Write` → Checks for unsolicited markdown summaries

2. **Code Quality Hooks**:
   - `Write|Edit|MultiEdit` → Checks file size and TODO comments
   - `Write|Edit` (markdown files) → Suggests splitting for large markdown files

3. **Generated File Hooks**:
   - `Read|Write|Edit|MultiEdit` → Detects generated files
   - `Read` → Warns with source file information (but allows)
   - `Write|Edit|MultiEdit` → Blocks with redirection to sources

4. **Tool Usage Hooks**:
   - `Bash` → Validates command-line tool usage
   - Blocks disallowed tools (npm, pip, etc.)
   - Shows preferred tool and examples

5. **Package Management Hooks**:
   - `Write|Edit|MultiEdit` → Detects package manifest edits
   - Analyzes content for dependency additions with versions
   - Warns (but allows) with proper package manager commands
   - Suggests ecosystem-appropriate tools

When a violation is detected, the operation is **blocked** with a helpful error message suggesting solutions.

For **markdown files exceeding 2000 lines**, Guard suggests splitting (but doesn't block) and offers to launch the markdown-splitter agent automatically.

For **generated files**, Guard warns on reads and blocks on edits, showing the source files to edit instead.

For **tool usage**, Guard blocks disallowed tools and shows the preferred alternative with examples.

For **package manifests**, Guard warns when dependencies are being added directly to manifest files and suggests using the appropriate package manager command instead.

## Agents

### `refactoring-architect`
Expert agent for breaking down large files into maintainable modules using domain-driven design principles.

### `markdown-splitter`
Expert agent for analyzing and splitting large markdown documents into manageable, context-friendly sections. Automatically creates:
- Index file with table of contents
- Section files with navigation
- Backups of original files
- Preserves all formatting and structure

## Philosophy

**Prevention over Correction** - Guard stops problems before they happen, not after:
- Sensitive files are never accidentally modified
- Code stays modular and maintainable
- All implementations are complete and production-ready

## Examples

### Protecting Project-Specific Files
```bash
/guard:protect config/production.yaml
/guard:protect src/secrets/
/guard:protect *credentials*.json
```

### Viewing Current Settings
```bash
/guard:protect list      # View protected files
/guard:config            # View quality thresholds
```

### Splitting Large Markdown Files
```bash
# Manual split
/guard:split-markdown task.md

# Or let Guard suggest it automatically
# When you try to write a markdown file > 2000 lines,
# Guard will ask: "Would you like me to split this file?"
# Reply "yes" to launch the markdown-splitter agent
```

**Result:**
```
task.md.backup          # Original backup
00-task.md              # Index with TOC
01-task.md              # Introduction (450 lines)
02-task.md              # Requirements (650 lines)
03-task.md              # Implementation (800 lines)
04-task.md              # Testing (550 lines)
```

### Managing Generated Files
Edit `.claude/guard/quality_config.json` to add custom generated file patterns:
```json
{
  "generated_files": {
    "enabled": true,
    "mappings": [
      {
        "pattern": "lib/models/*.g.dart",
        "source": "lib/models/*.dart",
        "description": "Custom model generation",
        "generate_command": "dart run build_runner build --delete-conflicting-outputs"
      }
    ]
  }
}
```

**Tips for Flutter Projects:**
- Default config includes common patterns (*.g.dart, *.freezed.dart, localization)
- Customize patterns to match your project structure
- Add custom code generation tools (GraphQL, JSON serialization, etc.)
- Include build commands with flags you typically use

### Configuring Package Guardian

Package Guardian is **enabled by default** and warns when package manifests are edited directly. To customize or disable:

**Example: Flutter Project**
```json
{
  "package_guardian": {
    "enabled": true,
    "package_managers": [
      {
        "name": "pub",
        "manifest_files": ["pubspec.yaml"],
        "add_command": "flutter pub add {package}",
        "add_dev_command": "flutter pub add --dev {package}",
        "description": "Dart/Flutter package manager"
      }
    ]
  }
}
```

**Example: Python Project with uv**
```json
{
  "package_guardian": {
    "enabled": true,
    "package_managers": [
      {
        "name": "uv",
        "manifest_files": ["pyproject.toml", "requirements.txt"],
        "add_command": "uv pip install {package}",
        "description": "Ultra-fast Python package manager"
      }
    ]
  }
}
```

**Disable Package Guardian:**
```json
{
  "package_guardian": {
    "enabled": false
  }
}
```

### Enabling Tool Guardian

The Tool Guardian is **disabled by default** to avoid conflicts with existing projects. Enable it per project:

```json
{
  "tool_guardian": {
    "enabled": true,
    "tool_replacements": [
      {
        "tool_name": "npm",
        "preferred_tool": "pnpm",
        "patterns": ["npm install", "npm i ", "npm add"],
        "reason": "This project uses pnpm",
        "examples": ["pnpm install", "pnpm add [package]"]
      }
    ]
  }
}
```

**Common Scenarios:**

**Use pnpm instead of npm:**
```json
{
  "tool_guardian": {
    "enabled": true,
    "tool_replacements": [
      {
        "tool_name": "npm",
        "preferred_tool": "pnpm",
        "patterns": ["npm install", "npm i ", "npm add", "npm ci", "npm run"],
        "reason": "This project uses pnpm for workspace support",
        "examples": ["pnpm install", "pnpm add [package]", "pnpm run [script]"]
      }
    ]
  }
}
```

**Use uv instead of pip:**
```json
{
  "tool_guardian": {
    "enabled": true,
    "tool_replacements": [
      {
        "tool_name": "pip",
        "preferred_tool": "uv",
        "patterns": ["pip install", "pip3 install", "python -m pip"],
        "reason": "This project uses uv for faster installs",
        "examples": ["uv pip install [package]", "uv pip sync"]
      }
    ]
  }
}
```

### Adjusting Quality Thresholds
Edit `.claude/guard/quality_config.json`:
```json
{
  "extensions": {
    ".py": 500,    # Stricter limit for Python
    ".tsx": 400    # Smaller React components
  },
  "markdown_splitter": {
    "auto_suggest_threshold": 1500,  # Suggest splitting at 1500 lines
    "split_strategy": "smart"        # Use smart chunking
  }
}
```

## Error Messages

When Guard blocks an operation, you'll see clear, actionable error messages:

**File Protection**:
```
🛡️  FILE GUARDIAN: Edit blocked
   📄 File: config/secrets.yaml
   🚫 Pattern: secrets/
   💡 Use /guard:unprotect "secrets/" to allow edits
```

**Code Quality**:
```
📏 CODE QUALITY GUARDIAN: File too large!
   📄 File: user_service.py
   📊 Size: 850 lines (threshold: 800)

   💡 Instead of creating one large file, consider:
      • Breaking into smaller, focused modules
      • Using domain-driven design principles
      • Separating concerns (data, logic, UI)
```

**Markdown Splitting**:
```
📄 MARKDOWN SPLITTER: Large markdown file detected!
   📄 File: requirements.md
   📊 Size: 2500 lines (split threshold: 2000)

   💡 This file may exceed LLM context limits.
      Large markdown files are difficult to navigate and process.

   ✨ I can split this into manageable sections:
      • Create index file (00-requirements.md)
      • Split into logical sections with navigation
      • Preserve all content and formatting
      • Backup original file

   🤖 Would you like me to split this file?
      Reply 'yes' and I'll launch the markdown-splitter agent
```

**Generated File (Read)**:
```
ℹ️  GENERATED FILE: This is auto-generated code
   📄 File: lib/l10n/app_localizations_en.dart
   📋 Description: Flutter localization files
   📝 Source pattern: lib/l10n/app_*.arb
   📂 Source files:
      • lib/l10n/app_en.arb

   ✓ Reading for reference is allowed
   🚫 Edits to this file will be blocked
```

**Generated File (Edit - Blocked)**:
```
🔒 GENERATED FILE GUARDIAN: Edit blocked!
   📄 File: lib/l10n/app_localizations_en.dart
   ⚙️  This is a generated file (Flutter localization files)

   💡 Edit the source file instead:
      Pattern: lib/l10n/app_*.arb

   📂 Available source files:
      ✓ lib/l10n/app_en.arb

   🔄 Regenerate after editing source:
      $ flutter gen-l10n

   ℹ️  Generated files are auto-created from source files.
      Editing them directly will be overwritten on next generation.
```

**Tool Guardian (Blocked)**:
```
🛠️  TOOL GUARDIAN: Disallowed tool detected!
   🚫 Command: npm install express
   ❌ Disallowed: npm

   💡 Use the preferred tool instead:
      ✓ pnpm

   📝 Example command:
      pnpm install [package]

   📋 Common usage:
      • pnpm install
      • pnpm add [package]
      • pnpm run [script]

   📋 Reason: This project uses pnpm for faster, disk-efficient package management

   ⚙️  Configure: Edit tool_guardian.tool_replacements in quality_config.json
   ⚙️  Disable: Set 'tool_guardian.enabled': false
```

**Package Guardian (Warning)**:
```
⚠️  PACKAGE GUARDIAN: Direct package manifest edit detected!
   📄 File: package.json
   📦 Package Manager: npm
   📋 Node.js package manager

   💡 Instead of editing the manifest directly, use the package manager:
   npm install {package}
   npm install --save-dev {package}  (for dev dependencies)

   ✨ Benefits of using package managers:
      • Automatic version resolution and compatibility checks
      • Updates lock files for reproducible builds
      • Handles transitive dependencies correctly
      • Prevents version conflicts and outdated packages

   ℹ️  This is a WARNING only - the operation will proceed
   ⚙️  Configure: Edit 'package_guardian' in .claude/guard/quality_config.json
   ⚙️  Disable: Set 'package_guardian.enabled': false
```

## License

MIT License - See LICENSE file for details

## Support

For issues or questions:
- GitHub: https://github.com/moinsen-dev/claude_code_marketplace
- Open an issue for bug reports or feature requests
