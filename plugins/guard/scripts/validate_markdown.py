#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

"""
File Guardian - Markdown Validator
Prevents unnecessary markdown file creation unless explicitly requested.
Blocks common "summary" files that Claude creates automatically.
"""
import json
import sys
from pathlib import Path
import os
import re

# Suspicious markdown filenames that suggest auto-generated summaries
SUMMARY_PATTERNS = [
    r'summary',
    r'recap',
    r'changes',
    r'completed?',
    r'completion',
    r'report',
    r'output',
    r'results?',
    r'notes',
    r'log',
    r'status',
    r'progress',
    r'update',
]

# Content patterns that suggest it's just a summary
SUMMARY_CONTENT_PATTERNS = [
    r'(?i)^#+ (summary|recap|changes|completed|report)',
    r'(?i)(i )?created? the following',
    r'(?i)(i )?generated? the following',
    r'(?i)(i )?made the following changes',
    r'(?i)(i )?modified the following',
    r'(?i)here.?s what (i|was) (created?|changed?|modified)',
    r'(?i)task completed?',
    r'(?i)files? created?:',
    r'(?i)changes made:',
]

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
    """Load markdown validation config."""
    config_file = project_root / '.claude' / 'guard' / 'file_guardian_config.json'

    default_config = {
        "block_unsolicited_markdown": True,
        "allow_patterns": [],  # Patterns to always allow
        "block_summary_content": True,
    }
    
    if config_file.exists():
        with open(config_file) as f:
            custom_config = json.load(f)
            config = default_config.copy()
            config.update(custom_config)
            return config
    
    return default_config

def is_summary_filename(filename: str) -> bool:
    """Check if filename suggests an auto-generated summary."""
    name_lower = filename.lower()
    stem = Path(filename).stem.lower()
    
    for pattern in SUMMARY_PATTERNS:
        if re.search(pattern, stem):
            return True
    
    return False

def has_summary_content(content: str) -> tuple[bool, str]:
    """Check if content looks like an auto-generated summary."""
    # Check first 500 chars (where summaries usually start)
    sample = content[:500]
    
    for pattern in SUMMARY_CONTENT_PATTERNS:
        match = re.search(pattern, sample, re.MULTILINE)
        if match:
            return True, match.group(0)
    
    return False, ""

def is_explicitly_allowed(file_path: str, config: dict) -> bool:
    """Check if file matches any allow patterns."""
    allow_patterns = config.get("allow_patterns", [])
    path = Path(file_path)
    
    for pattern in allow_patterns:
        if pattern.endswith('/'):
            # Directory pattern
            if str(path).startswith(pattern.rstrip('/')):
                return True
        elif '*' in pattern:
            # Glob pattern
            import fnmatch
            if fnmatch.fnmatch(str(path), pattern) or fnmatch.fnmatch(path.name, pattern):
                return True
        else:
            # Exact match
            if str(path) == pattern or path.name == pattern:
                return True
    
    return False

def main():
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)
    
    tool_name = data.get('tool_name', '')
    tool_input = data.get('tool_input', {})
    
    # Only check Write operations (new files)
    if tool_name != 'Write':
        sys.exit(0)
    
    # Get file path
    file_path = tool_input.get('file_path') or tool_input.get('path')
    
    if not file_path:
        sys.exit(0)
    
    # Check if it's a markdown file
    path = Path(file_path)
    if path.suffix.lower() not in ['.md', '.markdown']:
        sys.exit(0)  # Not markdown, allow
    
    # Get project root and load config
    project_root = Path(os.getenv('CLAUDE_PROJECT_DIR', os.getcwd()))

    # Check if this guardian is enabled
    if not is_guardian_enabled(project_root, "markdown-control"):
        sys.exit(0)  # Disabled, allow operation

    config = load_config(project_root)

    # If markdown blocking is disabled, allow
    if not config.get("block_unsolicited_markdown", True):
        sys.exit(0)
    
    # Check if explicitly allowed
    if is_explicitly_allowed(file_path, config):
        sys.exit(0)  # Allowed by config
    
    # Get content (Write tool uses 'content' parameter)
    content = tool_input.get('content', '')
    
    # Check filename
    is_suspicious_name = is_summary_filename(path.name)
    
    # Check content for summary patterns
    has_summary, matched_pattern = has_summary_content(content) if config.get("block_summary_content", True) else (False, "")
    
    # Block if suspicious
    if is_suspicious_name or has_summary:
        print(f"\n🛡️  FILE GUARDIAN: Unsolicited markdown file blocked", file=sys.stderr)
        print(f"   📄 File: {file_path}", file=sys.stderr)
        
        if is_suspicious_name:
            print(f"   🚫 Reason: Filename suggests auto-generated summary", file=sys.stderr)
        
        if has_summary:
            print(f"   🚫 Reason: Content looks like a summary/report", file=sys.stderr)
            if matched_pattern:
                print(f"      Pattern: \"{matched_pattern[:60]}...\"", file=sys.stderr)
        
        print(f"", file=sys.stderr)
        print(f"   💡 Markdown files should only be created when explicitly requested:", file=sys.stderr)
        print(f"      • User asks: \"Create a README.md documenting the API\"", file=sys.stderr)
        print(f"      • User asks: \"Write documentation in markdown\"", file=sys.stderr)
        print(f"      • Don't create summary files listing what you did", file=sys.stderr)
        print(f"", file=sys.stderr)
        print(f"   ℹ️  The user can see what files were created in the output", file=sys.stderr)
        print(f"   ⚙️  To allow this file: Add pattern to file_guardian_config.json", file=sys.stderr)
        
        sys.exit(2)  # Block the operation
    
    # Not suspicious, allow
    sys.exit(0)

if __name__ == '__main__':
    main()
