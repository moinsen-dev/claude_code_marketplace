---
description: Temporarily disable a guardian
---

# disable

Temporarily disable specific guardians or all guardians. Changes persist until explicitly re-enabled.

## Usage

```bash
/guard:disable <guardian-name>
/guard:disable all
```

## Available Guardians

- `file-protection` - File blacklist protection
- `markdown-control` - Unsolicited markdown blocking
- `code-quality` - File size and TODO enforcement
- `generated-files` - Generated file protection
- `tool-guardian` - Package manager enforcement
- `package-guardian` - Package manifest warnings

## Examples

```bash
# Disable package manifest warnings
/guard:disable package-guardian

# Disable all guardians
/guard:disable all

# Disable file protection temporarily
/guard:disable file-protection
```

## Implementation

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/manage_overrides.py disable {{guardian-name}}
```
