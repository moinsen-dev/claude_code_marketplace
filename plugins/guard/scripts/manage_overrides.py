#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

"""
Guard Plugin - Guardian Override Manager
Enables and disables individual guardians temporarily.
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
        "script": "validate_blacklist.py"
    },
    "markdown-control": {
        "name": "Markdown Control",
        "description": "Blocks unsolicited markdown summaries",
        "script": "validate_markdown.py"
    },
    "code-quality": {
        "name": "Code Quality",
        "description": "Enforces file size limits and TODO blocking",
        "script": "check_file_size.py"
    },
    "generated-files": {
        "name": "Generated File Protection",
        "description": "Protects auto-generated files",
        "script": "validate_generated_files.py"
    },
    "tool-guardian": {
        "name": "Tool Guardian",
        "description": "Enforces correct package manager usage",
        "script": "validate_tool_usage.py"
    },
    "package-guardian": {
        "name": "Package Guardian",
        "description": "Warns about direct package manifest edits",
        "script": "validate_package_edits.py"
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
        # Create default (all enabled)
        overrides_file.parent.mkdir(parents=True, exist_ok=True)
        default_overrides = {guardian: True for guardian in GUARDIANS.keys()}
        with open(overrides_file, 'w') as f:
            json.dump(default_overrides, f, indent=2)
        return default_overrides

    with open(overrides_file) as f:
        return json.load(f)

def save_overrides(overrides: dict):
    """Save overrides to file."""
    overrides_file = get_overrides_path()
    overrides_file.parent.mkdir(parents=True, exist_ok=True)
    with open(overrides_file, 'w') as f:
        json.dump(overrides, f, indent=2)

def set_guardian(guardian: str, enabled: bool):
    """Enable or disable a guardian."""
    if guardian not in GUARDIANS and guardian != "all":
        print(f"❌ Unknown guardian: {guardian}")
        print(f"\n📋 Available guardians:")
        for gid, info in GUARDIANS.items():
            print(f"   • {gid}: {info['description']}")
        sys.exit(1)

    overrides = load_overrides()
    action = "enabled" if enabled else "disabled"

    if guardian == "all":
        # Enable/disable all guardians
        for gid in GUARDIANS.keys():
            overrides[gid] = enabled
        save_overrides(overrides)

        print(f"✅ All guardians {action}!")
        print(f"\n📋 Guardian Status:")
        for gid, info in GUARDIANS.items():
            status = "✅" if enabled else "❌"
            print(f"   {status} {info['name']}: {action}")
    else:
        # Enable/disable specific guardian
        overrides[guardian] = enabled
        save_overrides(overrides)

        info = GUARDIANS[guardian]
        status = "✅" if enabled else "❌"
        print(f"{status} {info['name']}: {action}")
        print(f"   📋 {info['description']}")

    print(f"\n💾 Overrides saved to: {get_overrides_path().relative_to(Path(os.getenv('CLAUDE_PROJECT_DIR', os.getcwd())))}")
    print(f"\n💡 Use /guard:status to view current guardian states")

    sys.exit(0)

def main():
    if len(sys.argv) < 3:
        print("Usage: manage_overrides.py <enable|disable> <guardian-name|all>")
        print(f"\nAvailable guardians:")
        for gid, info in GUARDIANS.items():
            print(f"  • {gid}: {info['description']}")
        sys.exit(1)

    action = sys.argv[1].lower()
    guardian = sys.argv[2].lower()

    if action not in ["enable", "disable"]:
        print(f"❌ Invalid action: {action}")
        print(f"   Use 'enable' or 'disable'")
        sys.exit(1)

    enabled = (action == "enable")
    set_guardian(guardian, enabled)

if __name__ == '__main__':
    main()
