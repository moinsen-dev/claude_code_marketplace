---
description: Initialize Guard plugin with file protection and code quality features
---

# init

Initialize the Guard plugin by:
- Creating `.claude/forbidden_paths.txt` with default protected patterns
- Creating `.claude/file_guardian_config.json` with markdown blocking settings
- Creating `.claude/quality_config.json` with code quality thresholds
- Setting up hooks in `.claude/hooks.json`
- Making scripts executable

## Usage

```bash
/guard:init
```

## What Gets Created

1. **Blacklist File** (`.claude/forbidden_paths.txt`)
   - Default patterns for sensitive files (.env, secrets/, *.key, etc.)
   - Lock files (package-lock.json, yarn.lock, etc.)
   - Git internals and build artifacts

2. **File Guardian Configuration** (`.claude/file_guardian_config.json`)
   - Markdown blocking settings
   - Allowed patterns for documentation

3. **Quality Configuration** (`.claude/quality_config.json`)
   - Default file size thresholds for different extensions
   - TODO/FIXME blocking settings

4. **Hooks** (`.claude/hooks.json`)
   - PreToolUse hooks for Write/Edit/MultiEdit operations
   - Merges with existing hooks from other plugins

5. **Script Permissions**
   - Makes all hook scripts executable

## Default Protections

### File Protection
After initialization, Guard will automatically protect:
- Environment files (`.env`, `.env.*`)
- Secrets directory
- Credential files (`*.key`, `*.pem`, `*credentials*.json`)
- Lock files (`package-lock.json`, `pubspec.lock`, etc.)
- Git internals (`.git/`)
- Build artifacts (`build/`, `dist/`, `node_modules/`)
- Unsolicited markdown summaries (`SUMMARY.md`, `RECAP.md`)

### Code Quality
Guard will enforce:
- File size limits (800 lines for code, 600 for components, 5000 for docs)
- TODO/FIXME/HACK comment blocking
- Architectural best practices

## Implementation

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/init_plugin.py
```
