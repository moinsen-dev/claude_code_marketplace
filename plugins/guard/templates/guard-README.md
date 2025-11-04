# Guard Plugin Configuration

This directory contains all configuration files for the Guard plugin's 7 guardians.

---

## 📁 Configuration Files

### 1. `forbidden_paths.txt`
**Guardian**: File Protection Guardian
**Purpose**: Blacklist of files and patterns that should never be edited

**Syntax:**
- `filename.ext` - Exact filename
- `directory/` - Entire directory (with trailing slash)
- `*.ext` - Glob patterns
- `**/*.g.dart` - Recursive glob patterns

**Examples:**
```
.env
secrets/
*.key
**/*.generated.ts
```

**Commands:**
```bash
/guard:protect mysecret.yaml    # Add protection
/guard:protect *.secret          # Pattern
/guard:protect list              # View all
/guard:unprotect build/          # Remove
```

---

### 2. `file_guardian_config.json`
**Guardian**: Markdown Control Guardian
**Purpose**: Control markdown file creation behavior

**Default:**
```json
{
  "block_unsolicited_markdown": true,
  "block_summary_content": true,
  "allow_patterns": [
    "docs/",
    "README.md",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "LICENSE.md"
  ]
}
```

**What it blocks:**
- `SUMMARY.md`, `RECAP.md`, `REPORT.md`
- Files with summary content patterns
- Auto-generated documentation

---

### 3. `quality_config.json`
**Guardians**: Code Quality, Generated Files, Tool, Package, Command
**Purpose**: Main configuration file for quality enforcement

**Structure:**
```json
{
  "default": 1000,
  "block_todos": true,
  "todo_patterns": ["TODO", "FIXME", "HACK", "XXX", "TEMP", "TMP"],

  "extensions": {
    ".tsx": 600,
    ".dart": 800,
    ".py": 800
  },

  "markdown_splitter": {
    "enabled": true,
    "warn_threshold": 2000,
    "split_strategy": "headers"
  },

  "generated_files": {
    "enabled": true,
    "patterns": [...]
  },

  "tool_guardian": {
    "enabled": false,
    "disallowed_tools": {
      "npm": {
        "preferred": "pnpm",
        "example": "pnpm add <package>"
      }
    }
  },

  "package_guardian": {
    "enabled": true
  },

  "command_guardian": {
    "enabled": false,
    "forbidden_commands": [
      {
        "pattern": "flutter run",
        "match_type": "exact",
        "reason": "I want to test manually in VSCode"
      }
    ]
  }
}
```

**File Size Thresholds:**
Customize per file type to enforce modular code:
- UI components (`.tsx`, `.jsx`, `.vue`): 600 lines
- General code (`.dart`, `.py`, `.ts`, `.js`): 800 lines
- System languages (`.java`, `.go`, `.rs`): 1000 lines
- Documentation (`.md`, `.txt`): 5000 lines

**TODO Blocking:**
When `block_todos: true`, files with TODO/FIXME/HACK comments are rejected.

**Generated Files:**
Protects auto-generated files (*.g.dart, *.freezed.dart, etc.) from direct edits.

**Tool Guardian:**
Enforces preferred package managers (disabled by default).

**Package Guardian:**
Warns when editing package manifests directly (enabled by default).

**Command Guardian:**
Blocks specific bash commands with custom reasons (disabled by default).

---

### 4. `overrides.json`
**Purpose**: Guardian enable/disable state (persists across sessions)

**Default (all enabled):**
```json
{
  "file-protection": true,
  "markdown-control": true,
  "code-quality": true,
  "generated-files": true,
  "tool-guardian": true,
  "package-guardian": true,
  "command-guardian": true
}
```

**Managed by commands:**
```bash
/guard:status                    # View current state
/guard:disable markdown-control  # Disable one
/guard:disable all               # Disable all
/guard:enable all                # Re-enable all
```

---

## 🛡️ The 7 Guardians

### 1. File Protection Guardian ✅ Enabled by default
Blocks edits to sensitive files using blacklist patterns.

**Protects:**
- Environment files (`.env`)
- Secrets (`*.key`, `*.pem`)
- Lock files (`package-lock.json`, `yarn.lock`)
- Git internals (`.git/`)
- Build artifacts (`node_modules/`, `dist/`)

### 2. Markdown Control Guardian ✅ Enabled by default
Blocks unsolicited markdown summary files.

**Blocks:**
- `SUMMARY.md`, `RECAP.md`, `STATUS.md`
- Files with summary content

### 3. Code Quality Guardian ✅ Enabled by default
Enforces file size limits and blocks incomplete code.

**Enforces:**
- File size thresholds per extension
- No TODO/FIXME/HACK comments

### 4. Generated File Protection Guardian ✅ Enabled by default
Prevents edits to auto-generated files.

**Protects:**
- `*.g.dart`, `*.freezed.dart` (Dart)
- `app_localizations*.dart` (Flutter)
- `*.pb.dart` (Protocol Buffers)

### 5. Tool Guardian ⚠️ Disabled by default
Enforces correct package manager usage.

**Example:**
- Blocks `npm install` → suggests `pnpm install`

**Enable:**
Set `"tool_guardian.enabled": true` in `quality_config.json`

### 6. Package Guardian ✅ Enabled by default
Warns when editing package manifests directly.

**Warns on:**
- Direct edits to `package.json`, `pubspec.yaml`
- Suggests using package manager commands

### 7. Command Guardian ⚠️ Disabled by default
Blocks specific bash commands with custom reasons.

**Example:**
Block `flutter run` with reason "I want to test manually"

**Enable:**
Set `"command_guardian.enabled": true` in `quality_config.json`

---

## 📋 Common Commands

### View Status
```bash
/guard:status        # See all guardian states
/guard:config        # View quality thresholds
```

### File Protection
```bash
/guard:protect .env.local
/guard:protect secrets/
/guard:protect *.generated.ts
/guard:protect list
/guard:unprotect build/
```

### Override System
```bash
# Temporarily disable when needed
/guard:disable markdown-control
/guard:disable all

# Always re-enable after
/guard:enable all
```

### Markdown Splitting
```bash
/guard:split-markdown large-doc.md
```

---

## 🎯 Customization Guide

### Adjust File Size Thresholds

Edit `quality_config.json`:
```json
{
  "extensions": {
    ".dart": 600,      # Stricter for Dart
    ".py": 1200,       # More relaxed for Python
    ".tsx": 400        # Very strict for components
  }
}
```

### Allow TODOs

Edit `quality_config.json`:
```json
{
  "block_todos": false
}
```

### Add Custom Protected Files

Edit `forbidden_paths.txt`:
```
my-secret-config.yaml
production/
*.private
```

### Block Specific Commands

Edit `quality_config.json`:
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
        "reason": "Dangerous command - please confirm first"
      },
      {
        "pattern": ".*production.*",
        "match_type": "regex",
        "reason": "Production commands require manual execution"
      }
    ]
  }
}
```

**Match types:**
- `exact` - Exact command match
- `starts_with` - Command starts with pattern
- `contains` - Command contains pattern
- `regex` - Regular expression match

### Enable Tool Guardian

Edit `quality_config.json`:
```json
{
  "tool_guardian": {
    "enabled": true,
    "disallowed_tools": {
      "npm": {
        "preferred": "pnpm",
        "example": "pnpm add <package>"
      },
      "pip": {
        "preferred": "uv",
        "example": "uv add <package>"
      }
    }
  }
}
```

---

## 🚨 Troubleshooting

### Guardian blocking legitimate operation?

**Option 1: Temporarily disable**
```bash
/guard:disable <guardian-name>
# Do your operation
/guard:enable <guardian-name>
```

**Option 2: Adjust configuration**
Edit the relevant config file and adjust thresholds or patterns.

**Option 3: Add exception**
- For files: Add to allow_patterns in `file_guardian_config.json`
- For patterns: Remove from `forbidden_paths.txt`

### Want to see what's protected?
```bash
/guard:protect list        # View blacklist
/guard:status              # View guardian states
/guard:config              # View thresholds
```

### Accidentally disabled all guardians?
```bash
/guard:enable all
```

### File size error but file is legitimately large?

Consider:
1. Is the file doing too many things? (Refactor recommended)
2. Is it a special case? (Adjust threshold for that extension)
3. Is it legacy code? (Temporarily disable Code Quality Guardian)

---

## 💡 Best Practices

### When to Disable Guardians

**Importing legacy code:**
```bash
/guard:disable all
# Import large files with TODOs
/guard:enable all
```

**One-time generated file edit:**
```bash
/guard:disable generated-files
# Make your edit
/guard:enable generated-files
```

**Testing new package manager:**
```bash
/guard:disable tool-guardian
# Try new tool
/guard:enable tool-guardian
```

### Always Re-enable

Never leave guardians disabled permanently. They exist to prevent common mistakes!

### Customize Per Project

Each project has different needs. Adjust thresholds based on:
- Team preferences
- Language conventions
- Project complexity
- Legacy codebase constraints

---

## 📚 More Information

- **Full documentation**: See plugin README.md
- **Commands**: `/guard:init`, `/guard:status`, `/guard:config`
- **Test results**: `test-guard-plugin/COMPREHENSIVE_TEST_REPORT.md`

---

**Guard Plugin** - Prevention over correction
Protecting your codebase since 2025 🛡️
