---
description: Re-enable a disabled guardian
---

# enable

Re-enable specific guardians or all guardians that were previously disabled.

## Usage

```bash
/guard:enable <guardian-name>
/guard:enable all
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
# Re-enable package manifest warnings
/guard:enable package-guardian

# Re-enable all guardians
/guard:enable all

# Re-enable file protection
/guard:enable file-protection
```

## Implementation

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/manage_overrides.py enable {{guardian-name}}
```
