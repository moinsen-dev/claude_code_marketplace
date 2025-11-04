#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

"""
Package Guardian - Package Manifest Validator
Warns when editing package manifest files and suggests using package manager tools.
"""
import json
import sys
import re
from pathlib import Path
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


def load_config(project_root: Path) -> dict:
    """Load package guardian configuration."""
    config_file = project_root / '.claude' / 'guard' / 'quality_config.json'

    if not config_file.exists():
        # Try to create from template
        plugin_root = Path(os.getenv('CLAUDE_PLUGIN_ROOT', ''))
        template = plugin_root / 'templates' / 'package-guardian-config.json'

        if template.exists():
            # Load template config
            with open(template) as f:
                template_data = json.load(f)
                return template_data.get('package_guardian', {})

        # No config available
        return {}

    # Load existing config
    with open(config_file) as f:
        config = json.load(f)
        return config.get('package_guardian', {})


def detect_package_manager(file_path: Path, config: dict) -> dict | None:
    """Detect which package manager this file belongs to."""
    if not config.get('enabled', True):
        return None

    filename = file_path.name
    package_managers = config.get('package_managers', [])

    for pm in package_managers:
        manifest_files = pm.get('manifest_files', [])

        for pattern in manifest_files:
            # Check for exact match or glob pattern
            if pattern == filename:
                return pm

            # Simple glob matching for *.csproj etc
            if '*' in pattern:
                if re.match(pattern.replace('*', '.*'), filename):
                    return pm

    return None


def detect_dependency_addition(old_content: str, new_content: str, config: dict) -> bool:
    """Detect if new content appears to add dependencies with versions."""
    if not new_content:
        return False

    # If we can't get old content, analyze new content for version patterns
    detection_patterns = config.get('detection_patterns', [])

    if not detection_patterns:
        # Default patterns for version detection
        detection_patterns = [
            r'"version"\s*:\s*"\d+\.\d+',  # JSON: "version": "1.0.0"
            r'version\s*=\s*"\d+\.\d+',    # TOML: version = "1.0.0"
            r'version:\s*\^?\d+\.\d+',     # YAML: version: ^1.0.0
            r'@\d+\.\d+'                    # npm style: package@1.0.0
        ]

    # Check if new_content contains version patterns
    for pattern in detection_patterns:
        if re.search(pattern, new_content):
            return True

    return False


def get_preferred_command(package_manager: dict, file_path: Path) -> str:
    """Get the appropriate command for adding a package."""
    pm_name = package_manager.get('name', '')
    add_command = package_manager.get('add_command', '')
    add_dev_command = package_manager.get('add_dev_command', '')

    # Check if this might be a dev dependency
    # This is a heuristic - we can't perfectly detect intent
    commands = []

    if add_command:
        commands.append(f"   {add_command}")

    if add_dev_command:
        commands.append(f"   {add_dev_command}  (for dev dependencies)")

    if not commands:
        return f"   Use {pm_name} to manage dependencies"

    return "\n".join(commands)


def main():
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)

    tool_name = data.get('tool_name', '')
    tool_input = data.get('tool_input', {})

    # Only check write/edit operations
    if tool_name not in ['Write', 'Edit', 'MultiEdit']:
        sys.exit(0)

    # Get project root
    project_root = Path(os.getenv('CLAUDE_PROJECT_DIR', os.getcwd()))

    # Check if this guardian is enabled
    if not is_guardian_enabled(project_root, "package-guardian"):
        sys.exit(0)  # Disabled, allow operation

    # Load configuration
    config = load_config(project_root)

    if not config or not config.get('enabled', True):
        sys.exit(0)  # Feature disabled

    # Extract file path
    file_path = tool_input.get('file_path') or tool_input.get('path')

    if not file_path:
        sys.exit(0)

    file_path = Path(file_path)

    # Detect package manager
    package_manager = detect_package_manager(file_path, config)

    if not package_manager:
        sys.exit(0)  # Not a package manifest file

    # Get the content being written
    new_content = tool_input.get('content') or tool_input.get('new_string') or ''
    old_content = ''

    # Try to read old content if file exists
    if file_path.exists():
        try:
            old_content = file_path.read_text()
        except:
            pass

    # Detect if this looks like a dependency addition
    is_adding_dependency = detect_dependency_addition(old_content, new_content, config)

    if not is_adding_dependency:
        sys.exit(0)  # Not adding dependencies, allow silently

    # Issue warning
    pm_name = package_manager.get('name', 'package manager')
    pm_desc = package_manager.get('description', '')
    manifest_file = file_path.name

    warning_msg = config.get('warning_message',
        '⚠️  PACKAGE GUARDIAN: Direct package manifest edit detected!')

    print(warning_msg, file=sys.stderr)
    print(f"   📄 File: {manifest_file}", file=sys.stderr)
    print(f"   📦 Package Manager: {pm_name}", file=sys.stderr)

    if pm_desc:
        print(f"   📋 {pm_desc}", file=sys.stderr)

    print(file=sys.stderr)
    print("   💡 Instead of editing the manifest directly, use the package manager:", file=sys.stderr)

    commands = get_preferred_command(package_manager, file_path)
    print(commands, file=sys.stderr)

    print(file=sys.stderr)
    print("   ✨ Benefits of using package managers:", file=sys.stderr)
    print("      • Automatic version resolution and compatibility checks", file=sys.stderr)
    print("      • Updates lock files for reproducible builds", file=sys.stderr)
    print("      • Handles transitive dependencies correctly", file=sys.stderr)
    print("      • Prevents version conflicts and outdated packages", file=sys.stderr)

    print(file=sys.stderr)
    print("   ℹ️  This is a WARNING only - the operation will proceed", file=sys.stderr)
    print("   ⚙️  Configure: Edit 'package_guardian' in .claude/guard/quality_config.json", file=sys.stderr)
    print("   ⚙️  Disable: Set 'package_guardian.enabled': false", file=sys.stderr)

    # Exit 0 to allow the operation (warning only, not blocking)
    sys.exit(0)


if __name__ == '__main__':
    main()
