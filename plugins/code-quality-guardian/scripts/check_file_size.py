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

def load_config(project_root: Path) -> dict:
    """Load custom thresholds or use defaults."""
    config_file = project_root / '.claude' / 'quality_config.json'
    
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
    
    # Load configuration
    config = load_config(project_root)
    
    # Extract file path and content
    file_path = tool_input.get('file_path') or tool_input.get('path')
    
    # For Write tool
    if 'file_text' in tool_input:
        content = tool_input.get('file_text', '')
    # For Edit tool - need to check if it's a full rewrite
    elif 'new_str' in tool_input:
        # This is str_replace, we'll allow it
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
