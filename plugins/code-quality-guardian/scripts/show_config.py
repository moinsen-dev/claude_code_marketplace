#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

"""
Code Quality Guardian - Configuration Viewer
"""
import json
from pathlib import Path
import os

DEFAULT_CONFIG = {
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
    }
}

def main():
    project_root = Path(os.getenv('CLAUDE_PROJECT_DIR', os.getcwd()))
    config_file = project_root / '.claude' / 'quality_config.json'
    
    print("📏 Code Quality Guardian - Configuration")
    print("=" * 50)
    
    if config_file.exists():
        with open(config_file) as f:
            config = json.load(f)
        print(f"\n✅ Using custom configuration from:")
        print(f"   {config_file}")
    else:
        config = DEFAULT_CONFIG
        print(f"\n📋 Using default configuration")
        print(f"\n💡 To customize, create: {config_file}")
    
    print(f"\n⚙️  Current Thresholds:")
    print(f"\n   Default: {config.get('default', 1000)} lines")
    
    # TODO blocking status
    block_todos = config.get('block_todos', True)
    print(f"\n   TODO Blocking: {'✅ Enabled' if block_todos else '❌ Disabled'}")
    if block_todos and 'todo_patterns' in config:
        patterns = config['todo_patterns']
        print(f"   Blocked patterns: {', '.join(patterns)}")
    
    if 'extensions' in config:
        print(f"\n   File-Specific:")
        for ext, threshold in sorted(config['extensions'].items()):
            print(f"      {ext:10} → {threshold:4} lines")
    
    print("\n" + "=" * 50)
    print("\n💡 Tip: Files exceeding these limits will be blocked")
    print("         TODOs/FIXMEs/HACKs will also be rejected")
    print("         Use the refactoring-architect agent for help!")

if __name__ == '__main__':
    main()
