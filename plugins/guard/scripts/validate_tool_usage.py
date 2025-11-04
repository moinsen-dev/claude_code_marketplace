#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

"""
Guard Plugin - Tool Usage Validator
Enforces correct package manager and tool usage (e.g., pnpm over npm, uv over pip).
"""
import json
import sys
import os
import re
from pathlib import Path
from typing import Optional, List, Dict

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
    """Load tool guardian configuration."""
    config_file = project_root / '.claude' / 'guard' / 'quality_config.json'

    default_config = {
        "tool_guardian": {
            "enabled": True,
            "tool_replacements": []
        }
    }

    if config_file.exists():
        with open(config_file) as f:
            full_config = json.load(f)
            if "tool_guardian" in full_config:
                config = default_config["tool_guardian"].copy()
                config.update(full_config["tool_guardian"])
                return config

    return default_config["tool_guardian"]

def normalize_command(command: str) -> str:
    """Normalize command by removing extra whitespace."""
    return ' '.join(command.split())

def detect_disallowed_tool(command: str, replacements: List[Dict]) -> Optional[Dict]:
    """
    Detect if command uses a disallowed tool.

    Returns: matching replacement config or None
    """
    command_normalized = normalize_command(command)
    command_lower = command_normalized.lower()

    for replacement in replacements:
        tool_name = replacement.get('tool_name', '').lower()
        patterns = replacement.get('patterns', [])

        if not tool_name or not patterns:
            continue

        # Check each pattern
        for pattern in patterns:
            # Simple substring match
            if isinstance(pattern, str):
                pattern_lower = pattern.lower()

                # Check if pattern matches at word boundary
                # This prevents matching "pnpm" when looking for "npm"
                pattern_regex = r'\b' + re.escape(pattern_lower) + r'\b'

                if re.search(pattern_regex, command_lower):
                    return replacement

            # Regex pattern
            elif isinstance(pattern, dict) and 'regex' in pattern:
                regex_pattern = pattern['regex']
                try:
                    if re.search(regex_pattern, command, re.IGNORECASE):
                        return replacement
                except re.error:
                    continue

    return None

def get_command_example(command: str, preferred_tool: str, tool_name: str) -> Optional[str]:
    """
    Generate an example command using the preferred tool.

    Returns: example command or None
    """
    # Extract the action from the original command
    command_lower = command.lower()

    # Common command mappings
    if tool_name.lower() == 'npm':
        if 'install' in command_lower or ' i ' in command_lower or command_lower.endswith(' i'):
            return f"{preferred_tool} install [package]"
        elif 'add' in command_lower:
            return f"{preferred_tool} add [package]"
        elif 'run' in command_lower:
            return f"{preferred_tool} run [script]"
        else:
            return f"{preferred_tool} [command]"

    elif tool_name.lower() == 'pip':
        if 'install' in command_lower:
            return f"{preferred_tool} pip install [package]"
        else:
            return f"{preferred_tool} pip [command]"

    elif tool_name.lower() == 'python':
        if 'python -m' in command_lower:
            return f"{preferred_tool} run python -m [module]"
        else:
            return f"{preferred_tool} run python [script]"

    elif tool_name.lower() in ['yarn', 'bun']:
        return f"{preferred_tool} [command]"

    return None

def check_forbidden_command(command: str, project_root: Path) -> Optional[Dict]:
    """
    Check if command matches any forbidden commands.

    Returns: forbidden command config or None
    """
    # Load configuration
    config_file = project_root / '.claude' / 'guard' / 'quality_config.json'

    if not config_file.exists():
        return None

    try:
        with open(config_file) as f:
            full_config = json.load(f)
            command_config = full_config.get('command_guardian', {})
    except:
        return None

    if not command_config.get('enabled', False):
        return None  # Command guardian disabled

    forbidden_commands = command_config.get('forbidden_commands', [])
    if not forbidden_commands:
        return None

    command_normalized = normalize_command(command)

    for forbidden in forbidden_commands:
        pattern = forbidden.get('pattern', '')
        match_type = forbidden.get('match_type', 'exact')

        if not pattern:
            continue

        # Check match based on type
        matched = False

        if match_type == 'exact':
            matched = command_normalized == pattern or command_normalized.lower() == pattern.lower()
        elif match_type == 'starts_with':
            matched = command_normalized.startswith(pattern) or command_normalized.lower().startswith(pattern.lower())
        elif match_type == 'contains':
            matched = pattern in command_normalized or pattern.lower() in command_normalized.lower()
        elif match_type == 'regex':
            try:
                matched = bool(re.search(pattern, command, re.IGNORECASE))
            except re.error:
                continue

        if matched:
            return forbidden

    return None

def main():
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)

    tool_name = data.get('tool_name', '')
    tool_input = data.get('tool_input', {})

    # Only check Bash commands
    if tool_name != 'Bash':
        sys.exit(0)

    # Get project root
    project_root = Path(os.getenv('CLAUDE_PROJECT_DIR', os.getcwd()))

    # Extract command
    command = tool_input.get('command', '')

    if not command:
        sys.exit(0)

    # ===== COMMAND GUARDIAN CHECK =====
    # Check if command-guardian is enabled in overrides
    if is_guardian_enabled(project_root, "command-guardian"):
        forbidden = check_forbidden_command(command, project_root)

        if forbidden:
            # Block the command
            pattern = forbidden.get('pattern', '')
            reason = forbidden.get('reason', 'Command is forbidden by project configuration')
            match_type = forbidden.get('match_type', 'exact')

            print(f"\n🚫 COMMAND GUARDIAN: Command blocked!", file=sys.stderr)
            print(f"   📄 Command: {command}", file=sys.stderr)
            print(f"   🚫 Matched pattern: {pattern} (match type: {match_type})", file=sys.stderr)
            print(f"", file=sys.stderr)
            print(f"   💡 Reason:", file=sys.stderr)
            print(f"      {reason}", file=sys.stderr)
            print(f"", file=sys.stderr)
            print(f"   ⚙️  To allow this command:", file=sys.stderr)
            print(f"      • Remove from forbidden_commands in quality_config.json", file=sys.stderr)
            print(f"      • Or disable: /guard:disable command-guardian", file=sys.stderr)
            print(f"", file=sys.stderr)

            sys.exit(2)  # Block the operation

    # ===== TOOL GUARDIAN CHECK =====
    # Check if this guardian is enabled
    if not is_guardian_enabled(project_root, "tool-guardian"):
        sys.exit(0)  # Disabled, allow operation

    # Load configuration
    config = load_config(project_root)

    if not config.get('enabled', True):
        sys.exit(0)  # Feature disabled

    replacements = config.get('tool_replacements', [])
    if not replacements:
        sys.exit(0)  # No replacements configured

    # Check if command uses disallowed tool
    replacement = detect_disallowed_tool(command, replacements)

    if not replacement:
        sys.exit(0)  # No disallowed tool detected

    # Block the command
    disallowed_tool = replacement.get('tool_name', 'unknown tool')
    preferred_tool = replacement.get('preferred_tool', 'recommended tool')
    reason = replacement.get('reason', 'Project configuration')
    examples = replacement.get('examples', [])

    print(f"\n🛠️  TOOL GUARDIAN: Disallowed tool detected!", file=sys.stderr)
    print(f"   🚫 Command: {command}", file=sys.stderr)
    print(f"   ❌ Disallowed: {disallowed_tool}", file=sys.stderr)
    print(f"", file=sys.stderr)
    print(f"   💡 Use the preferred tool instead:", file=sys.stderr)
    print(f"      ✓ {preferred_tool}", file=sys.stderr)
    print(f"", file=sys.stderr)

    # Show example if available
    example = get_command_example(command, preferred_tool, disallowed_tool)
    if example:
        print(f"   📝 Example command:", file=sys.stderr)
        print(f"      {example}", file=sys.stderr)
        print(f"", file=sys.stderr)

    # Show custom examples if provided
    if examples:
        print(f"   📋 Common usage:", file=sys.stderr)
        for ex in examples[:3]:
            print(f"      • {ex}", file=sys.stderr)
        print(f"", file=sys.stderr)

    print(f"   📋 Reason: {reason}", file=sys.stderr)
    print(f"", file=sys.stderr)
    print(f"   ⚙️  Configure: Edit tool_guardian.tool_replacements in quality_config.json", file=sys.stderr)
    print(f"   ⚙️  Disable: Set 'tool_guardian.enabled': false", file=sys.stderr)
    print(f"", file=sys.stderr)

    sys.exit(2)  # Block the operation

if __name__ == '__main__':
    main()
