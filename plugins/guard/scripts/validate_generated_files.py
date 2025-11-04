#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

"""
Guard Plugin - Generated File Validator
Prevents editing auto-generated files and redirects to source files.
"""
import json
import sys
import os
from pathlib import Path
import fnmatch
from typing import Optional, List, Tuple

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

def load_config(project_root: Path) -> dict:
    """Load generated files configuration."""
    config_file = project_root / '.claude' / 'guard' / 'quality_config.json'

    default_config = {
        "generated_files": {
            "enabled": True,
            "mappings": []
        }
    }

    if config_file.exists():
        with open(config_file) as f:
            full_config = json.load(f)
            if "generated_files" in full_config:
                config = default_config["generated_files"].copy()
                config.update(full_config["generated_files"])
                return config

    return default_config["generated_files"]

def normalize_path(file_path: str, project_root: Path) -> Tuple[Path, str]:
    """
    Normalize file path to absolute and relative forms.

    Returns: (absolute_path, relative_path_str)
    """
    path = Path(file_path)

    # Convert to absolute if needed
    if not path.is_absolute():
        abs_path = project_root / path
    else:
        abs_path = path

    # Get relative path
    try:
        rel_path = abs_path.relative_to(project_root)
    except ValueError:
        rel_path = path

    return abs_path, str(rel_path)

def matches_pattern(file_path: str, pattern: str) -> bool:
    """
    Check if file path matches a glob pattern.

    Supports:
    - Wildcards: *, **
    - Directory matching
    - Relative and absolute paths
    """
    # Normalize both for comparison
    file_path_normalized = file_path.replace('\\', '/')
    pattern_normalized = pattern.replace('\\', '/')

    # Try direct glob match
    if fnmatch.fnmatch(file_path_normalized, pattern_normalized):
        return True

    # Try matching just the filename
    file_name = Path(file_path).name
    pattern_name = Path(pattern).name
    if '*' in pattern_name and fnmatch.fnmatch(file_name, pattern_name):
        # Also check directory if pattern has directory component
        pattern_dir = str(Path(pattern).parent)
        if pattern_dir and pattern_dir != '.':
            file_dir = str(Path(file_path).parent)
            if not fnmatch.fnmatch(file_dir, pattern_dir):
                return False
        return True

    return False

def find_source_files(file_path: str, source_pattern: str, project_root: Path) -> List[str]:
    """
    Find source files based on pattern substitution.

    Examples:
    - file: lib/l10n/app_localizations_en.dart
    - pattern: lib/l10n/app_*.arb
    - result: [lib/l10n/app_en.arb]
    """
    # Extract the wildcard part from the file path
    # This is a simplified approach - matches the pattern structure

    abs_path, rel_path = normalize_path(file_path, project_root)

    # Try to find files matching the source pattern in the same directory
    file_dir = abs_path.parent
    pattern_dir = Path(source_pattern).parent
    pattern_name = Path(source_pattern).name

    # Determine search directory
    if str(pattern_dir) == '.' or not pattern_dir:
        search_dir = file_dir
    elif '**' in str(pattern_dir):
        # Glob pattern in directory - search from project root
        search_dir = project_root
    else:
        # Specific directory in pattern
        search_dir = project_root / pattern_dir

    if not search_dir.exists():
        return []

    # Search for matching files
    matches = []

    if '**' in source_pattern:
        # Recursive search
        pattern_parts = source_pattern.split('/')
        for part in search_dir.rglob('*'):
            if part.is_file() and matches_pattern(str(part.relative_to(project_root)), source_pattern):
                matches.append(str(part.relative_to(project_root)))
    else:
        # Non-recursive search
        for file in search_dir.glob(pattern_name):
            if file.is_file():
                matches.append(str(file.relative_to(project_root)))

    return matches

def find_matching_mapping(file_path: str, mappings: List[dict], project_root: Path) -> Optional[dict]:
    """
    Find the first mapping that matches the file path.

    Returns: matching mapping dict or None
    """
    abs_path, rel_path = normalize_path(file_path, project_root)

    for mapping in mappings:
        pattern = mapping.get('pattern', '')
        if not pattern:
            continue

        # Check if file matches this generated pattern
        if matches_pattern(rel_path, pattern) or matches_pattern(str(abs_path), pattern):
            return mapping

    return None

def handle_read_operation(file_path: str, mapping: dict, project_root: Path):
    """Handle read operation - warn but allow."""
    abs_path, rel_path = normalize_path(file_path, project_root)

    source_pattern = mapping.get('source', '')
    description = mapping.get('description', 'Auto-generated file')

    print(f"\nℹ️  GENERATED FILE: This is auto-generated code", file=sys.stderr)
    print(f"   📄 File: {rel_path}", file=sys.stderr)
    print(f"   📋 Description: {description}", file=sys.stderr)

    if source_pattern:
        print(f"   📝 Source pattern: {source_pattern}", file=sys.stderr)

        # Try to find actual source files
        source_files = find_source_files(file_path, source_pattern, project_root)
        if source_files:
            print(f"   📂 Source files:", file=sys.stderr)
            for src in source_files[:3]:  # Show first 3
                print(f"      • {src}", file=sys.stderr)
            if len(source_files) > 3:
                print(f"      ... and {len(source_files) - 3} more", file=sys.stderr)

    print(f"", file=sys.stderr)
    print(f"   ✓ Reading for reference is allowed", file=sys.stderr)
    print(f"   🚫 Edits to this file will be blocked", file=sys.stderr)
    print(f"", file=sys.stderr)

    sys.exit(0)  # Allow read

def handle_edit_operation(file_path: str, mapping: dict, project_root: Path):
    """Handle edit operation - block with helpful message."""
    abs_path, rel_path = normalize_path(file_path, project_root)

    source_pattern = mapping.get('source', '')
    description = mapping.get('description', 'Auto-generated file')
    generate_command = mapping.get('generate_command', '')

    print(f"\n🔒 GENERATED FILE GUARDIAN: Edit blocked!", file=sys.stderr)
    print(f"   📄 File: {rel_path}", file=sys.stderr)
    print(f"   ⚙️  This is a generated file ({description})", file=sys.stderr)
    print(f"", file=sys.stderr)

    if source_pattern:
        print(f"   💡 Edit the source file instead:", file=sys.stderr)
        print(f"      Pattern: {source_pattern}", file=sys.stderr)

        # Try to find actual source files
        source_files = find_source_files(file_path, source_pattern, project_root)
        if source_files:
            print(f"", file=sys.stderr)
            print(f"   📂 Available source files:", file=sys.stderr)
            for src in source_files[:5]:  # Show first 5
                src_path = project_root / src
                exists = "✓" if src_path.exists() else "✗"
                print(f"      {exists} {src}", file=sys.stderr)
            if len(source_files) > 5:
                print(f"      ... and {len(source_files) - 5} more", file=sys.stderr)
        else:
            print(f"      (Source files not found - may need to be created)", file=sys.stderr)

        print(f"", file=sys.stderr)

    if generate_command:
        print(f"   🔄 Regenerate after editing source:", file=sys.stderr)
        print(f"      $ {generate_command}", file=sys.stderr)
        print(f"", file=sys.stderr)

    print(f"   ℹ️  Generated files are auto-created from source files.", file=sys.stderr)
    print(f"      Editing them directly will be overwritten on next generation.", file=sys.stderr)
    print(f"", file=sys.stderr)
    print(f"   ⚙️  To disable: Set 'generated_files.enabled': false in quality_config.json", file=sys.stderr)
    print(f"", file=sys.stderr)

    sys.exit(2)  # Block operation

def main():
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)

    tool_name = data.get('tool_name', '')
    tool_input = data.get('tool_input', {})

    # Check relevant operations
    if tool_name not in ['Read', 'Write', 'Edit', 'MultiEdit']:
        sys.exit(0)

    # Get project root
    project_root = Path(os.getenv('CLAUDE_PROJECT_DIR', os.getcwd()))

    # Check if this guardian is enabled
    if not is_guardian_enabled(project_root, "generated-files"):
        sys.exit(0)  # Disabled, allow operation

    # Load configuration
    config = load_config(project_root)

    if not config.get('enabled', True):
        sys.exit(0)  # Feature disabled

    mappings = config.get('mappings', [])
    if not mappings:
        sys.exit(0)  # No mappings configured

    # Extract file path
    file_path = tool_input.get('file_path') or tool_input.get('path')

    if not file_path:
        sys.exit(0)

    # Check if file matches any generated pattern
    mapping = find_matching_mapping(file_path, mappings, project_root)

    if not mapping:
        sys.exit(0)  # Not a generated file

    # Handle based on operation type
    if tool_name == 'Read':
        handle_read_operation(file_path, mapping, project_root)
    else:
        # Write, Edit, MultiEdit - block these
        handle_edit_operation(file_path, mapping, project_root)

if __name__ == '__main__':
    main()
