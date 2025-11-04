#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

"""
File Guardian - Blacklist Manager
Manage the project's forbidden paths blacklist.
"""
import sys
from pathlib import Path
import os

def get_blacklist_path() -> Path:
    """Get the path to the project's blacklist file."""
    project_root = Path(os.getenv('CLAUDE_PROJECT_DIR', os.getcwd()))
    return project_root / '.claude' / 'guard' / 'forbidden_paths.txt'

def ensure_blacklist_exists():
    """Ensure blacklist file exists, create from template if needed."""
    blacklist_file = get_blacklist_path()
    
    if not blacklist_file.exists():
        plugin_root = Path(os.getenv('CLAUDE_PLUGIN_ROOT', ''))
        template = plugin_root / 'templates' / 'default-blacklist.txt'
        
        blacklist_file.parent.mkdir(parents=True, exist_ok=True)
        
        if template.exists():
            blacklist_file.write_text(template.read_text())
        else:
            blacklist_file.write_text("# File Guardian - Protected Paths\n# Add patterns below (one per line)\n\n.env\n")
    
    return blacklist_file

def list_protected():
    """List all protected patterns."""
    blacklist_file = get_blacklist_path()
    
    if not blacklist_file.exists():
        print("No protected patterns configured.")
        print(f"Use /protect add <pattern> to add patterns.")
        return
    
    with open(blacklist_file) as f:
        lines = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    
    if not lines:
        print("No protected patterns configured.")
        return
    
    print("🛡️  Protected patterns:")
    for i, pattern in enumerate(lines, 1):
        print(f"  {i}. {pattern}")
    
    print(f"\n📄 Blacklist file: {blacklist_file}")

def add_pattern(pattern: str):
    """Add a pattern to the blacklist."""
    blacklist_file = ensure_blacklist_exists()
    
    # Check if already exists
    with open(blacklist_file) as f:
        existing = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    
    if pattern in existing:
        print(f"⚠️  Pattern '{pattern}' is already protected.")
        return
    
    # Add pattern
    with open(blacklist_file, 'a') as f:
        f.write(f"{pattern}\n")
    
    print(f"✅ Added '{pattern}' to protected patterns")

def remove_pattern(pattern: str):
    """Remove a pattern from the blacklist."""
    blacklist_file = get_blacklist_path()
    
    if not blacklist_file.exists():
        print("No blacklist file exists.")
        return
    
    # Read all lines
    with open(blacklist_file) as f:
        lines = f.readlines()
    
    # Filter out the pattern
    new_lines = [line for line in lines if line.strip() != pattern]
    
    if len(new_lines) == len(lines):
        print(f"⚠️  Pattern '{pattern}' not found in blacklist.")
        return
    
    # Write back
    with open(blacklist_file, 'w') as f:
        f.writelines(new_lines)
    
    print(f"✅ Removed '{pattern}' from protected patterns")

def main():
    if len(sys.argv) < 2:
        list_protected()
        return
    
    command = sys.argv[1]
    
    if command == "list":
        list_protected()
    elif command == "add" and len(sys.argv) >= 3:
        add_pattern(sys.argv[2])
    elif command == "remove" and len(sys.argv) >= 3:
        remove_pattern(sys.argv[2])
    else:
        print("Usage:")
        print("  list              - Show all protected patterns")
        print("  add <pattern>     - Add a pattern to blacklist")
        print("  remove <pattern>  - Remove a pattern from blacklist")

if __name__ == '__main__':
    main()
