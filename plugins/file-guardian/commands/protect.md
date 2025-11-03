---
description: Add files or patterns to the protection blacklist
---

# protect

Protect files from accidental edits by adding them to the blacklist.

## Usage

```bash
/protect <pattern>
/protect list
```

## Examples

```bash
# Protect environment files
/protect .env

# Protect entire directory
/protect secrets/

# Protect by extension
/protect *.key

# Show current protections
/protect list
```

## Implementation

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/manage_blacklist.py add {{pattern}}
```
