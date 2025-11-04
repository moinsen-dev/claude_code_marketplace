#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

"""
Guard Plugin - Status Display
Shows the current enabled/disabled state of all guardians.
"""
import json
import sys
from pathlib import Path
import os

# Guardian identifiers and their descriptions
GUARDIANS = {
    "file-protection": {
        "name": "File Protection",
        "description": "Prevents editing forbidden files (blacklist)",
        "icon": "🛡️"
    },
    "markdown-control": {
        "name": "Markdown Control",
        "description": "Blocks unsolicited markdown summaries",
        "icon": "📄"
    },
    "code-quality": {
        "name": "Code Quality",
        "description": "Enforces file size limits and TODO blocking",
        "icon": "📏"
    },
    "generated-files": {
        "name": "Generated File Protection",
        "description": "Protects auto-generated files",
        "icon": "🔒"
    },
    "tool-guardian": {
        "name": "Tool Guardian",
        "description": "Enforces correct package manager usage",
        "icon": "🛠️"
    },
    "package-guardian": {
        "name": "Package Guardian",
        "description": "Warns about direct package manifest edits",
        "icon": "📦"
    }
}

def get_overrides_path() -> Path:
    """Get the path to the overrides file."""
    project_root = Path(os.getenv('CLAUDE_PROJECT_DIR', os.getcwd()))
    return project_root / '.claude' / 'guard' / 'overrides.json'

def load_overrides() -> dict:
    """Load current overrides or return defaults."""
    overrides_file = get_overrides_path()

    if not overrides_file.exists():
        # Return defaults (all enabled)
        return {guardian: True for guardian in GUARDIANS.keys()}

    with open(overrides_file) as f:
        overrides = json.load(f)

    # Ensure all guardians have a value
    for guardian in GUARDIANS.keys():
        if guardian not in overrides:
            overrides[guardian] = True

    return overrides

def main():
    project_root = Path(os.getenv('CLAUDE_PROJECT_DIR', os.getcwd()))
    overrides = load_overrides()

    print("\n🛡️  Guard Plugin - Guardian Status\n")
    print("=" * 60)
    print()

    enabled_count = sum(1 for v in overrides.values() if v)
    disabled_count = len(overrides) - enabled_count

    for gid, info in GUARDIANS.items():
        is_enabled = overrides.get(gid, True)
        status = "✅ enabled " if is_enabled else "❌ disabled"
        icon = info['icon']

        print(f"{icon}  {info['name']:30} {status}")
        print(f"   {info['description']}")
        print()

    print("=" * 60)
    print(f"📊 Summary: {enabled_count} enabled, {disabled_count} disabled")
    print()

    overrides_file = get_overrides_path()
    if overrides_file.exists():
        print(f"⚙️  Configuration: {overrides_file.relative_to(project_root)}")
    else:
        print(f"⚙️  Using default settings (all enabled)")

    print()
    print("💡 Commands:")
    print("   • Disable: /guard:disable <guardian-name>")
    print("   • Enable:  /guard:enable <guardian-name>")
    print("   • All:     /guard:disable all | /guard:enable all")
    print()

    sys.exit(0)

if __name__ == '__main__':
    main()
