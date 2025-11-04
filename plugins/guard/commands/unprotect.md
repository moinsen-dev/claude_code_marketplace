---
description: Remove files or patterns from the protection blacklist
---

# unprotect

Remove protection from files, allowing them to be edited.

## Usage

```bash
/unprotect <pattern>
/unprotect list
```

## Examples

```bash
# Unprotect a file
/unprotect .env.example

# Unprotect directory
/unprotect build/

# Show all protections
/unprotect list
```

## Implementation

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/manage_blacklist.py remove {{pattern}}
```
