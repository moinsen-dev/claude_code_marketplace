#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

"""
Guard Plugin - Unified Initialization
Sets up file protection and code quality features.
"""
import json
import sys
import os
from pathlib import Path
import stat
import shutil

# Default quality configuration
DEFAULT_QUALITY_CONFIG = {
    "default": 1000,
    "block_todos": True,
    "todo_patterns": ["TODO", "FIXME", "HACK", "XXX", "TEMP", "TMP"],
    "extensions": {
        ".md": 5000,
        ".json": 2000,
        ".txt": 5000,
        ".dart": 800,
        ".py": 800,
        ".ts": 800,
        ".js": 800,
        ".tsx": 600,
        ".jsx": 600,
        ".vue": 600,
        ".java": 1000,
        ".go": 1000,
        ".rs": 1000,
        ".cpp": 1000,
        ".c": 1000,
        ".cs": 1000,
        ".php": 800,
        ".rb": 800,
        ".swift": 800,
        ".kt": 800
    },
    "markdown_splitter": {
        "enabled": True,
        "auto_suggest_threshold": 2000,
        "target_chunk_size": 800,
        "split_strategy": "headers",
        "preserve_original": True,
        "create_index": True
    },
    "generated_files": {
        "enabled": True,
        "mappings": [
            {
                "pattern": "lib/l10n/app_localizations*.dart",
                "source": "lib/l10n/app_*.arb",
                "description": "Flutter localization files",
                "generate_command": "flutter gen-l10n"
            },
            {
                "pattern": "**/*.g.dart",
                "source": "**/*.dart",
                "description": "Dart code generation (build_runner)",
                "generate_command": "dart run build_runner build"
            },
            {
                "pattern": "**/*.freezed.dart",
                "source": "**/*.dart",
                "description": "Freezed immutable models",
                "generate_command": "dart run build_runner build"
            }
        ]
    },
    "tool_guardian": {
        "enabled": False,
        "tool_replacements": [
            {
                "tool_name": "npm",
                "preferred_tool": "pnpm",
                "patterns": ["npm install", "npm i ", "npm add", "npm ci", "npm run", "npm test", "npm start"],
                "reason": "This project uses pnpm for faster, disk-efficient package management",
                "examples": [
                    "pnpm install",
                    "pnpm add [package]",
                    "pnpm run [script]"
                ]
            },
            {
                "tool_name": "pip",
                "preferred_tool": "uv",
                "patterns": ["pip install", "pip3 install", "python -m pip", "python3 -m pip"],
                "reason": "This project uses uv for 10-100x faster Python package management",
                "examples": [
                    "uv pip install [package]",
                    "uv pip sync requirements.txt",
                    "uv run python [script]"
                ]
            }
        ]
    },
    "package_guardian": {
        "enabled": True,
        "package_managers": [],
        "detection_patterns": [
            "\"version\"\\s*:\\s*\"\\d+\\.\\d+",
            "version\\s*=\\s*\"\\d+\\.\\d+",
            "version:\\s*\\^?\\d+\\.\\d+",
            "@\\d+\\.\\d+"
        ]
    },
    "command_guardian": {
        "enabled": False,
        "forbidden_commands": [
            {
                "pattern": "flutter run",
                "match_type": "exact",
                "reason": "I want to test manually in VSCode or my preferred tool"
            },
            {
                "pattern": "rm -rf /",
                "match_type": "exact",
                "reason": "Destructive command - please confirm before running"
            }
        ]
    }
}

# Default overrides configuration (all guardians enabled by default)
DEFAULT_OVERRIDES = {
    "file-protection": True,
    "markdown-control": True,
    "code-quality": True,
    "generated-files": True,
    "tool-guardian": True,
    "package-guardian": True,
    "command-guardian": True
}

# Unified plugin hooks
PLUGIN_HOOKS = {
    "hooks": {
        "PreToolUse": [
            {
                "matcher": "Bash",
                "hooks": [
                    {
                        "type": "command",
                        "command": "${CLAUDE_PLUGIN_ROOT}/scripts/validate_tool_usage.py"
                    }
                ]
            },
            {
                "matcher": "Read|Write|Edit|MultiEdit",
                "hooks": [
                    {
                        "type": "command",
                        "command": "${CLAUDE_PLUGIN_ROOT}/scripts/validate_generated_files.py"
                    }
                ]
            },
            {
                "matcher": "Write|Edit|MultiEdit",
                "hooks": [
                    {
                        "type": "command",
                        "command": "${CLAUDE_PLUGIN_ROOT}/scripts/check_file_size.py"
                    },
                    {
                        "type": "command",
                        "command": "${CLAUDE_PLUGIN_ROOT}/scripts/validate_blacklist.py"
                    },
                    {
                        "type": "command",
                        "command": "${CLAUDE_PLUGIN_ROOT}/scripts/validate_package_edits.py"
                    }
                ]
            },
            {
                "matcher": "Write",
                "hooks": [
                    {
                        "type": "command",
                        "command": "${CLAUDE_PLUGIN_ROOT}/scripts/validate_markdown.py"
                    }
                ]
            }
        ]
    }
}

def normalize_matcher(matcher: str) -> str:
    """Normalize matcher by sorting tool names."""
    if not matcher:
        return ""
    tools = [t.strip() for t in matcher.split("|")]
    return "|".join(sorted(tools))

def merge_hooks(existing_hooks: dict, new_hooks: dict) -> dict:
    """Merge new hooks into existing hooks without duplication."""
    if not existing_hooks:
        return new_hooks

    result = existing_hooks.copy()

    # Ensure hooks structure exists
    if "hooks" not in result:
        result["hooks"] = {}
    if "PreToolUse" not in result["hooks"]:
        result["hooks"]["PreToolUse"] = []

    # Add new hooks
    for new_hook_group in new_hooks.get("hooks", {}).get("PreToolUse", []):
        matcher = new_hook_group.get("matcher")
        normalized_matcher = normalize_matcher(matcher)

        # Find existing hook group with same matcher (normalized)
        existing_group = None
        for group in result["hooks"]["PreToolUse"]:
            if normalize_matcher(group.get("matcher")) == normalized_matcher:
                existing_group = group
                break

        if existing_group:
            # Merge hooks into existing group
            for new_hook in new_hook_group.get("hooks", []):
                command = new_hook.get("command")
                # Check if this hook already exists
                hook_exists = any(
                    h.get("command") == command
                    for h in existing_group.get("hooks", [])
                )
                if not hook_exists:
                    existing_group.setdefault("hooks", []).append(new_hook)
        else:
            # Add new hook group
            result["hooks"]["PreToolUse"].append(new_hook_group)

    return result

def make_scripts_executable(plugin_root: Path):
    """Make all Python scripts in the scripts directory executable."""
    scripts_dir = plugin_root / "scripts"
    if scripts_dir.exists():
        for script in scripts_dir.glob("*.py"):
            st = os.stat(script)
            os.chmod(script, st.st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)

def main():
    project_dir = Path(os.getenv('CLAUDE_PROJECT_DIR', os.getcwd()))
    # Use CLAUDE_PLUGIN_ROOT to support marketplace installations
    plugin_root = Path(os.getenv('CLAUDE_PLUGIN_ROOT', project_dir / "plugins" / "guard"))

    # Create .claude/guard/ directory
    guard_dir = project_dir / ".claude" / "guard"
    guard_dir.mkdir(parents=True, exist_ok=True)

    # For backward compatibility, also maintain .claude/hooks.json at root
    claude_dir = project_dir / ".claude"

    print("\n🛡️  Guard Plugin - Initialization\n")

    # 1. Create forbidden_paths.txt if it doesn't exist
    forbidden_paths = guard_dir / "forbidden_paths.txt"
    if forbidden_paths.exists():
        print(f"✓ Blacklist file already exists: {forbidden_paths.relative_to(project_dir)}")
    else:
        template = plugin_root / "templates" / "default-blacklist.txt"
        shutil.copy(template, forbidden_paths)
        print(f"✓ Created blacklist file: {forbidden_paths.relative_to(project_dir)}")

    # 2. Create file_guardian_config.json if it doesn't exist
    file_config = guard_dir / "file_guardian_config.json"
    if file_config.exists():
        print(f"✓ File protection config already exists: {file_config.relative_to(project_dir)}")
    else:
        template = plugin_root / "templates" / "guardian-config.json"
        shutil.copy(template, file_config)
        print(f"✓ Created file protection config: {file_config.relative_to(project_dir)}")

    # 3. Create quality_config.json if it doesn't exist
    quality_config = guard_dir / "quality_config.json"
    if quality_config.exists():
        print(f"✓ Quality config already exists: {quality_config.relative_to(project_dir)}")
    else:
        with open(quality_config, 'w') as f:
            json.dump(DEFAULT_QUALITY_CONFIG, f, indent=2)
        print(f"✓ Created quality config: {quality_config.relative_to(project_dir)}")

    # 4. Create overrides.json if it doesn't exist
    overrides_file = guard_dir / "overrides.json"
    if overrides_file.exists():
        print(f"✓ Overrides file already exists: {overrides_file.relative_to(project_dir)}")
    else:
        with open(overrides_file, 'w') as f:
            json.dump(DEFAULT_OVERRIDES, f, indent=2)
        print(f"✓ Created overrides file: {overrides_file.relative_to(project_dir)}")

    # 5. Copy README.md template to guard directory
    guard_readme = guard_dir / "README.md"
    if guard_readme.exists():
        print(f"✓ Guard README already exists: {guard_readme.relative_to(project_dir)}")
    else:
        readme_template = plugin_root / "templates" / "guard-README.md"
        if readme_template.exists():
            shutil.copy(readme_template, guard_readme)
            print(f"✓ Created guard README: {guard_readme.relative_to(project_dir)}")
        else:
            print(f"⚠️  README template not found (this is okay for older installations)")

    # 6. Merge hooks into hooks.json (kept at .claude/ for compatibility)
    hooks_file = claude_dir / "hooks.json"
    existing_hooks = {}
    if hooks_file.exists():
        with open(hooks_file) as f:
            existing_hooks = json.load(f)

    merged_hooks = merge_hooks(existing_hooks, PLUGIN_HOOKS)

    with open(hooks_file, 'w') as f:
        json.dump(merged_hooks, f, indent=2)

    if existing_hooks:
        print(f"✓ Merged hooks into: {hooks_file.relative_to(project_dir)}")
    else:
        print(f"✓ Created hooks file: {hooks_file.relative_to(project_dir)}")

    # 7. Make scripts executable
    make_scripts_executable(plugin_root)
    print(f"✓ Made scripts executable")

    # 8. Success message
    print("\n✅ Guard Plugin initialized successfully!\n")
    print("Configuration Files:")
    print(f"  • README: .claude/guard/README.md")
    print(f"  • Blacklist: .claude/guard/forbidden_paths.txt")
    print(f"  • File Protection: .claude/guard/file_guardian_config.json")
    print(f"  • Code Quality: .claude/guard/quality_config.json")
    print(f"  • Overrides: .claude/guard/overrides.json")
    print(f"  • Hooks: .claude/hooks.json")

    print("\n🛡️  File Protection:")
    print(f"  • Environment files (.env, .env.*)")
    print(f"  • Secrets directory")
    print(f"  • Credential files (*.key, *.pem, *credentials*.json)")
    print(f"  • Lock files (package-lock.json, yarn.lock, etc.)")
    print(f"  • Git internals (.git/)")
    print(f"  • Build artifacts (node_modules/, build/, dist/)")
    print(f"  • Unsolicited markdown summaries (SUMMARY.md, RECAP.md)")

    print("\n📏 Code Quality:")
    print(f"  • .py, .ts, .js, .dart: 800 lines")
    print(f"  • .tsx, .jsx, .vue: 600 lines")
    print(f"  • .txt, .md: 5000 lines")
    print(f"  • TODO/FIXME blocking: Enabled")

    print("\n📄 Markdown Splitter:")
    print(f"  • Auto-suggest threshold: 2000 lines")
    print(f"  • Target chunk size: 800 lines")
    print(f"  • Split strategy: By headers")
    print(f"  • Backup original: Enabled")

    print("\n🔒 Generated File Protection:")
    print(f"  • Flutter localization files (app_localizations*.dart)")
    print(f"  • Dart code generation (*.g.dart, *.freezed.dart)")
    print(f"  • Redirects to source files with generation commands")
    print(f"  • Warns on reads, blocks on edits")

    print("\n🛠️  Tool Guardian:")
    print(f"  • Enforces correct package manager usage")
    print(f"  • Default: Disabled (enable per project)")
    print(f"  • Presets: npm→pnpm, pip→uv")
    print(f"  • Enable: Set 'tool_guardian.enabled': true")

    print("\n🚫 Command Guardian:")
    print(f"  • Blocks specific bash commands with custom reasons")
    print(f"  • Default: Disabled (enable per project)")
    print(f"  • Examples: flutter run, rm -rf /")
    print(f"  • Enable: Set 'command_guardian.enabled': true")
    print(f"  • Match types: exact, starts_with, contains, regex")

    print("\nNext Steps:")
    print(f"  • Add protection: /guard:protect <file-or-pattern>")
    print(f"  • View protected: /guard:protect list")
    print(f"  • View config: /guard:config")
    print(f"  • Split markdown: /guard:split-markdown <file>")
    print(f"  • Disable guardian: /guard:disable <guardian-name>")
    print(f"  • Enable guardian: /guard:enable <guardian-name>")
    print(f"  • View status: /guard:status")
    print(f"  • Guard is now active and protecting your codebase!")
    print()

    sys.exit(0)

if __name__ == '__main__':
    main()
