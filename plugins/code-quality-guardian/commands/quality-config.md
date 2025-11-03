---
description: View and configure code quality thresholds
---

# quality-config

View and customize file size thresholds for different file types.

## Usage

```bash
# View current configuration
/quality-config

# Show available options
/quality-config help
```

## Configuration

Edit `.claude/quality_config.json` in your project root to customize thresholds.

## Example Configuration

```json
{
  "default": 1000,
  "extensions": {
    ".dart": 800,
    ".py": 800,
    ".ts": 800,
    ".tsx": 600,
    ".jsx": 600
  }
}
```

## Implementation

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/show_config.py
```
