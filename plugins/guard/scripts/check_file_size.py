#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

"""
Code Quality Guardian - File Size Checker
Prevents creation of oversized files and suggests refactoring.
"""
import json
import sys
from pathlib import Path
import os

# Default configuration
DEFAULT_THRESHOLDS = {
    "default": 1000,  # Default max lines
    "block_todos": True,  # Block TODO/FIXME/HACK comments
    "todo_patterns": ["TODO", "FIXME", "HACK", "XXX", "TEMP", "TMP"],
    "extensions": {
        ".md": 5000,     # Markdown can be longer (documentation)
        ".json": 2000,   # JSON can be data-heavy
        ".txt": 5000,    # Text files can be longer
        ".dart": 800,    # Flutter/Dart files
        ".py": 800,      # Python files
        ".ts": 800,      # TypeScript files
        ".js": 800,      # JavaScript files
        ".tsx": 600,     # React components should be smaller
        ".jsx": 600,     # React components should be smaller
        ".vue": 600,     # Vue components should be smaller
        ".java": 1000,   # Java files
        ".go": 1000,     # Go files
    }
}

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
    """Load custom thresholds or use defaults."""
    config_file = project_root / '.claude' / 'guard' / 'quality_config.json'

    if config_file.exists():
        with open(config_file) as f:
            custom_config = json.load(f)
            # Merge with defaults
            config = DEFAULT_THRESHOLDS.copy()
            config.update(custom_config)
            return config
    
    return DEFAULT_THRESHOLDS

def get_threshold_for_file(file_path: str, config: dict) -> int:
    """Get the line threshold for a specific file."""
    path = Path(file_path)
    ext = path.suffix.lower()
    
    # Check for extension-specific threshold
    if ext in config.get("extensions", {}):
        return config["extensions"][ext]
    
    # Return default
    return config.get("default", 1000)

def count_lines(content: str) -> int:
    """Count non-empty lines in content."""
    return len([line for line in content.split('\n') if line.strip()])

def detect_todos(content: str, config: dict) -> list[dict]:
    """
    Detect TODO/FIXME/HACK comments in content.
    
    Returns: List of {line_number, line_content, pattern} for each TODO found
    """
    if not config.get("block_todos", True):
        return []
    
    patterns = config.get("todo_patterns", ["TODO", "FIXME", "HACK", "XXX", "TEMP", "TMP"])
    todos = []
    
    for line_num, line in enumerate(content.split('\n'), 1):
        line_upper = line.upper()
        for pattern in patterns:
            # Check for pattern in comments (common formats)
            if any(marker in line_upper for marker in [
                f"// {pattern}",      # C-style single line
                f"# {pattern}",       # Python/Shell style
                f"/* {pattern}",      # C-style multi-line
                f"* {pattern}",       # Inside multi-line comment
                f"<!-- {pattern}",    # HTML/XML
                f"//{pattern}",       # No space variant
                f"#{pattern}",        # No space variant
            ]):
                todos.append({
                    "line_number": line_num,
                    "line_content": line.strip(),
                    "pattern": pattern
                })
                break  # Only report first pattern match per line
    
    return todos

def should_block_file(file_path: str, content: str, config: dict) -> tuple[bool, int, int]:
    """
    Check if file should be blocked due to size.

    Returns: (should_block, line_count, threshold)
    """
    threshold = get_threshold_for_file(file_path, config)
    line_count = count_lines(content)

    return line_count > threshold, line_count, threshold

def should_suggest_markdown_split(file_path: str, line_count: int, config: dict) -> bool:
    """
    Check if markdown file should be suggested for splitting.

    Returns: True if file is markdown and exceeds split threshold
    """
    path = Path(file_path)
    ext = path.suffix.lower()

    # Only for markdown files
    if ext not in ['.md', '.markdown']:
        return False

    # Check if markdown splitter is enabled
    md_config = config.get("markdown_splitter", {})
    if not md_config.get("enabled", True):
        return False

    # Check if exceeds split threshold
    split_threshold = md_config.get("auto_suggest_threshold", 2000)
    return line_count > split_threshold

def main():
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)
    
    tool_name = data.get('tool_name', '')
    tool_input = data.get('tool_input', {})
    
    # Only check write operations
    if tool_name not in ['Write', 'Edit', 'MultiEdit']:
        sys.exit(0)
    
    # Get project root
    project_root = Path(os.getenv('CLAUDE_PROJECT_DIR', os.getcwd()))

    # Check if this guardian is enabled
    if not is_guardian_enabled(project_root, "code-quality"):
        sys.exit(0)  # Disabled, allow operation

    # Load configuration
    config = load_config(project_root)
    
    # Extract file path and content
    file_path = tool_input.get('file_path') or tool_input.get('path')

    # For Write tool (uses 'content' parameter)
    if 'content' in tool_input:
        content = tool_input.get('content', '')
    # For Edit tool - need to check the result after edit
    elif 'new_string' in tool_input:
        old_string = tool_input.get('old_string', '')
        new_string = tool_input.get('new_string', '')

        # Read current file content and apply the replacement
        file_path_obj = Path(file_path)
        if not file_path_obj.exists():
            # New file, use new_string as content
            content = new_string
        else:
            # Apply the string replacement to get resulting content
            try:
                current_content = file_path_obj.read_text()
                content = current_content.replace(old_string, new_string, 1)
            except Exception:
                # Can't read file, allow the operation
                sys.exit(0)
    else:
        # Unknown format, allow it
        sys.exit(0)
    
    if not file_path or not content:
        sys.exit(0)
    
    # Check for TODO comments first (higher priority)
    todos = detect_todos(content, config)

    if todos:
        print(f"\n🚫 CODE QUALITY GUARDIAN: TODO/FIXME comments detected!", file=sys.stderr)
        print(f"   📄 File: {file_path}", file=sys.stderr)
        print(f"   ⚠️  Found {len(todos)} incomplete marker(s):", file=sys.stderr)
        print(f"", file=sys.stderr)

        # Show first 5 TODOs
        for todo in todos[:5]:
            print(f"      Line {todo['line_number']:4}: {todo['line_content'][:80]}", file=sys.stderr)

        if len(todos) > 5:
            print(f"      ... and {len(todos) - 5} more", file=sys.stderr)

        print(f"", file=sys.stderr)
        print(f"   💡 Code should be complete and production-ready:", file=sys.stderr)
        print(f"      • Implement the missing functionality instead", file=sys.stderr)
        print(f"      • Don't leave breadcrumbs for later", file=sys.stderr)
        print(f"      • If you can't implement it, discuss limitations", file=sys.stderr)
        print(f"", file=sys.stderr)
        print(f"   🤖 Try: Ask me to complete these implementations", file=sys.stderr)
        print(f"   ⚙️  To allow TODOs: Set 'block_todos': false in quality_config.json", file=sys.stderr)

        sys.exit(2)  # Block the operation

    # Check if file is too large
    should_block, line_count, threshold = should_block_file(file_path, content, config)

    # Check if markdown file should be suggested for splitting (before blocking)
    if should_suggest_markdown_split(file_path, line_count, config):
        md_config = config.get("markdown_splitter", {})
        split_threshold = md_config.get("auto_suggest_threshold", 2000)

        print(f"\n📄 MARKDOWN SPLITTER: Large markdown file detected!", file=sys.stderr)
        print(f"   📄 File: {file_path}", file=sys.stderr)
        print(f"   📊 Size: {line_count} lines (split threshold: {split_threshold})", file=sys.stderr)
        print(f"", file=sys.stderr)
        print(f"   💡 This file may exceed LLM context limits.", file=sys.stderr)
        print(f"      Large markdown files are difficult to navigate and process.", file=sys.stderr)
        print(f"", file=sys.stderr)
        print(f"   ✨ I can split this into manageable sections:", file=sys.stderr)
        print(f"      • Create index file (00-{Path(file_path).stem}.md)", file=sys.stderr)
        print(f"      • Split into logical sections with navigation", file=sys.stderr)
        print(f"      • Preserve all content and formatting", file=sys.stderr)
        print(f"      • Backup original file", file=sys.stderr)
        print(f"", file=sys.stderr)
        print(f"   🤖 Would you like me to split this file?", file=sys.stderr)
        print(f"      Reply 'yes' and I'll launch the markdown-splitter agent", file=sys.stderr)
        print(f"", file=sys.stderr)
        print(f"   🔧 Manual split: /guard:split-markdown {file_path}", file=sys.stderr)
        print(f"   ⚙️  Adjust threshold: Edit markdown_splitter.auto_suggest_threshold in quality_config.json", file=sys.stderr)
        print(f"", file=sys.stderr)

        # Don't block - just warn and allow
        # User can respond to the suggestion
        sys.exit(0)
    
    if should_block:
        path = Path(file_path)
        ext = path.suffix.lower()
        
        print(f"\n📏 CODE QUALITY GUARDIAN: File too large!", file=sys.stderr)
        print(f"   📄 File: {file_path}", file=sys.stderr)
        print(f"   📊 Size: {line_count} lines (threshold: {threshold})", file=sys.stderr)
        print(f"", file=sys.stderr)
        print(f"   💡 Instead of creating one large file, consider:", file=sys.stderr)
        print(f"      • Breaking into smaller, focused modules", file=sys.stderr)
        print(f"      • Using domain-driven design principles", file=sys.stderr)
        print(f"      • Separating concerns (data, logic, UI)", file=sys.stderr)
        print(f"", file=sys.stderr)
        print(f"   🤖 Try: Ask me to refactor this into multiple files", file=sys.stderr)
        print(f"   🤖 Or use: /refactor to get architectural guidance", file=sys.stderr)
        print(f"", file=sys.stderr)
        print(f"   ⚙️  Adjust thresholds: /quality-config", file=sys.stderr)
        
        sys.exit(2)  # Block the operation
    
    # File size is acceptable
    sys.exit(0)

if __name__ == '__main__':
    main()
