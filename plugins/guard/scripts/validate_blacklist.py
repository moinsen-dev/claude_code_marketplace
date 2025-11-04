#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

"""
File Guardian - Blacklist Validator
Prevents editing of forbidden files based on project blacklist.
"""
import json
import sys
from pathlib import Path
import fnmatch
import os

def is_guardian_enabled(project_root: Path, guardian_name: str) -> bool:
    """Check if a specific guardian is enabled in overrides."""
    overrides_file = project_root / '.claude' / 'guard' / 'overrides.json'

    if not overrides_file.exists():
        return True  # Default: enabled

    try:
        with open(overrides_file) as f:
            overrides = json.load(f)
            return overrides.get(guardian_name, True)
    except:
        return True  # On error, assume enabled

def load_blacklist(project_root: Path) -> list[str]:
    """Load forbidden paths from project blacklist file."""
    blacklist_file = project_root / '.claude' / 'guard' / 'forbidden_paths.txt'

    if not blacklist_file.exists():
        # Try to create from template
        plugin_root = Path(os.getenv('CLAUDE_PLUGIN_ROOT', ''))
        template = plugin_root / 'templates' / 'default-blacklist.txt'

        if template.exists():
            # First run - create default blacklist
            blacklist_file.parent.mkdir(parents=True, exist_ok=True)
            blacklist_file.write_text(template.read_text())
            print(f"ℹ️  Created default blacklist at {blacklist_file}", file=sys.stderr)
        else:
            # No template, no blacklist - allow everything
            return []

    with open(blacklist_file) as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

def is_path_forbidden(file_path: str, forbidden_paths: list[str], project_root: Path) -> tuple[bool, str]:
    """Check if a file path matches any blacklist pattern."""
    path = Path(file_path)
    
    # Normalize to relative path
    try:
        rel_path = path.relative_to(project_root) if path.is_absolute() else path
    except ValueError:
        rel_path = path
    
    rel_path_str = str(rel_path)
    
    for pattern in forbidden_paths:
        # Directory patterns (ending with /)
        if pattern.endswith('/'):
            dir_pattern = pattern.rstrip('/')
            if rel_path_str.startswith(dir_pattern + '/') or rel_path_str == dir_pattern:
                return True, pattern
        
        # Exact match
        elif rel_path_str == pattern or path.name == pattern:
            return True, pattern
        
        # Glob pattern
        elif fnmatch.fnmatch(rel_path_str, pattern):
            return True, pattern
        
        # Filename-only pattern
        elif '/' not in pattern and fnmatch.fnmatch(path.name, pattern):
            return True, pattern
    
    return False, ""

def main():
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)
    
    tool_name = data.get('tool_name', '')
    tool_input = data.get('tool_input', {})
    
    # Only check edit operations
    if tool_name not in ['Edit', 'Write', 'MultiEdit']:
        sys.exit(0)
    
    # Get project root
    project_root = Path(os.getenv('CLAUDE_PROJECT_DIR', os.getcwd()))

    # Check if this guardian is enabled
    if not is_guardian_enabled(project_root, "file-protection"):
        sys.exit(0)  # Disabled, allow operation

    # Load blacklist
    forbidden_paths = load_blacklist(project_root)
    
    if not forbidden_paths:
        sys.exit(0)  # No restrictions
    
    # Extract file path
    file_path = tool_input.get('file_path') or tool_input.get('path')
    
    if not file_path:
        sys.exit(0)
    
    # Check if forbidden
    is_forbidden, matched_pattern = is_path_forbidden(file_path, forbidden_paths, project_root)
    
    if is_forbidden:
        print(f"🛡️  FILE GUARDIAN: Edit blocked", file=sys.stderr)
        print(f"   📄 File: {file_path}", file=sys.stderr)
        print(f"   🚫 Pattern: {matched_pattern}", file=sys.stderr)
        print(f"   💡 Use /protect list to see all protected patterns", file=sys.stderr)
        print(f"   💡 Use /unprotect \"{matched_pattern}\" to allow edits", file=sys.stderr)
        sys.exit(2)  # Block the operation
    
    sys.exit(0)  # Allow

if __name__ == '__main__':
    main()
