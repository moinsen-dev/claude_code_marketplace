---
description: View guardian status
---

# status

Display the current enabled/disabled state of all guardians.

## Usage

```bash
/guard:status
```

## What It Shows

For each guardian:
- Current status (enabled/disabled)
- Guardian name and description
- Configuration file location

## Example Output

```
🛡️  Guard Plugin - Guardian Status

🛡️  File Protection              ✅ enabled
   Prevents editing forbidden files (blacklist)

📄  Markdown Control             ❌ disabled
   Blocks unsolicited markdown summaries

📏  Code Quality                 ✅ enabled
   Enforces file size limits and TODO blocking

...
```

## Implementation

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/show_status.py
```
