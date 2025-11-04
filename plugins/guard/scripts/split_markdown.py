#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

"""
Guard Plugin - Markdown Splitter
Intelligently splits large markdown files into manageable sections.
"""
import json
import sys
import os
import re
from pathlib import Path
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

@dataclass
class MarkdownSection:
    """Represents a section of markdown content."""
    title: str
    level: int
    content: str
    line_start: int
    line_end: int

    @property
    def line_count(self) -> int:
        return len(self.content.split('\n'))

class MarkdownSplitter:
    """Splits large markdown files into manageable sections."""

    def __init__(self, file_path: Path, config: dict):
        self.file_path = file_path
        self.config = config
        self.content = file_path.read_text()
        self.lines = self.content.split('\n')

    def parse_structure(self) -> List[MarkdownSection]:
        """Parse markdown structure and identify sections."""
        sections = []
        current_section = None
        current_content = []
        line_num = 0

        for i, line in enumerate(self.lines):
            # Check if this is a header
            header_match = re.match(r'^(#{1,6})\s+(.+)$', line)

            if header_match:
                # Save previous section if exists
                if current_section:
                    current_section.content = '\n'.join(current_content)
                    current_section.line_end = i - 1
                    sections.append(current_section)

                # Start new section
                level = len(header_match.group(1))
                title = header_match.group(2).strip()

                current_section = MarkdownSection(
                    title=title,
                    level=level,
                    content="",
                    line_start=i,
                    line_end=i
                )
                current_content = [line]
            else:
                # Add to current section
                if current_section:
                    current_content.append(line)
                else:
                    # Content before first header
                    if not sections:
                        current_section = MarkdownSection(
                            title="Introduction",
                            level=1,
                            content="",
                            line_start=0,
                            line_end=0
                        )
                        current_content = [line]

        # Save last section
        if current_section:
            current_section.content = '\n'.join(current_content)
            current_section.line_end = len(self.lines) - 1
            sections.append(current_section)

        return sections

    def group_sections(self, sections: List[MarkdownSection]) -> List[List[MarkdownSection]]:
        """Group sections by top-level headers for splitting."""
        target_size = self.config.get('target_chunk_size', 800)
        strategy = self.config.get('split_strategy', 'headers')

        if strategy == 'headers':
            # Group by top-level headers (level 1)
            groups = []
            current_group = []

            for section in sections:
                if section.level == 1 and current_group:
                    # Start new group
                    groups.append(current_group)
                    current_group = [section]
                else:
                    current_group.append(section)

            if current_group:
                groups.append(current_group)

            return groups

        else:  # 'smart' chunking
            # Group sections to target chunk size
            groups = []
            current_group = []
            current_size = 0

            for section in sections:
                section_size = section.line_count

                if current_size + section_size > target_size and current_group:
                    # Start new group
                    groups.append(current_group)
                    current_group = [section]
                    current_size = section_size
                else:
                    current_group.append(section)
                    current_size += section_size

            if current_group:
                groups.append(current_group)

            return groups

    def generate_index(self, groups: List[List[MarkdownSection]]) -> str:
        """Generate index file content."""
        basename = self.file_path.stem
        total_lines = len(self.lines)
        total_sections = len(groups)
        avg_lines = total_lines // total_sections if total_sections > 0 else 0

        index_content = [
            f"# {basename} - Index",
            "",
            "> This document has been split into manageable sections for better context handling.",
            "",
            "## 📑 Table of Contents",
            ""
        ]

        # Add TOC entries
        for i, group in enumerate(groups, 1):
            main_section = group[0]
            section_lines = sum(s.line_count for s in group)

            # Get title (first level-1 header or first section title)
            title = main_section.title

            # Count subsections
            subsection_count = len([s for s in group if s.level > 1])
            subsection_info = f" ({subsection_count} subsections)" if subsection_count > 0 else ""

            index_content.append(
                f"{i}. [{title}](./{i:02d}-{basename}.md) - {section_lines} lines{subsection_info}"
            )

        index_content.extend([
            "",
            "## 🔍 Quick Navigation",
            "",
            f"- **Total Sections**: {total_sections}",
            f"- **Original Size**: {total_lines} lines",
            f"- **Average Section**: {avg_lines} lines",
            f"- **Split Date**: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "",
            "## 📝 Overview",
            "",
            f"This document was automatically split because it exceeded the recommended size threshold ({self.config.get('auto_suggest_threshold', 2000)} lines).",
            "Each section can now be loaded independently, improving LLM context efficiency.",
            "",
            "To navigate:",
            "- Click any section link above to view its content",
            "- Each section includes navigation links back to this index",
            "- Sections maintain the original document structure and formatting",
            "",
            "---",
            f"*Generated by Guard Markdown Splitter on {datetime.now().strftime('%Y-%m-%d')}*"
        ])

        return '\n'.join(index_content)

    def generate_section_file(self,
                             section_num: int,
                             group: List[MarkdownSection],
                             total_sections: int) -> str:
        """Generate content for a section file."""
        basename = self.file_path.stem

        # Build navigation header
        nav_parts = [f"[← Index](./00-{basename}.md)"]

        if section_num > 1:
            nav_parts.append(f"[← Previous](./{section_num-1:02d}-{basename}.md)")

        if section_num < total_sections:
            nav_parts.append(f"[Next →](./{section_num+1:02d}-{basename}.md)")

        navigation = " | ".join(nav_parts)

        # Build content
        content_parts = [
            f"# {group[0].title}",
            "",
            f"> **Navigation**: {navigation}",
            "",
            "---",
            ""
        ]

        # Add section content (skip the first header as we already added it)
        for i, section in enumerate(group):
            section_lines = section.content.split('\n')

            if i == 0:
                # Skip the first line (header) for first section
                content_parts.extend(section_lines[1:])
            else:
                content_parts.extend(section_lines)

        # Add footer navigation
        content_parts.extend([
            "",
            "---",
            f"> **Navigation**: {navigation}"
        ])

        return '\n'.join(content_parts)

    def split(self, output_dir: Optional[Path] = None) -> dict:
        """
        Split the markdown file into sections.

        Returns:
            dict with 'files' (list of created files) and 'stats' (splitting statistics)
        """
        if output_dir is None:
            output_dir = self.file_path.parent

        basename = self.file_path.stem

        # Parse and group sections
        sections = self.parse_structure()
        groups = self.group_sections(sections)

        if not groups:
            return {
                'success': False,
                'error': 'No sections found to split'
            }

        # Backup original if configured
        if self.config.get('preserve_original', True):
            backup_path = self.file_path.parent / f"{self.file_path.name}.backup"
            backup_path.write_text(self.content)

        created_files = []

        # Generate index file
        index_path = output_dir / f"00-{basename}.md"
        index_content = self.generate_index(groups)
        index_path.write_text(index_content)
        created_files.append(str(index_path))

        # Generate section files
        for i, group in enumerate(groups, 1):
            section_path = output_dir / f"{i:02d}-{basename}.md"
            section_content = self.generate_section_file(i, group, len(groups))
            section_path.write_text(section_content)
            created_files.append(str(section_path))

        # Calculate statistics
        stats = {
            'original_file': str(self.file_path),
            'original_lines': len(self.lines),
            'sections_created': len(groups),
            'files_created': created_files,
            'backup_created': str(self.file_path.parent / f"{self.file_path.name}.backup") if self.config.get('preserve_original', True) else None
        }

        return {
            'success': True,
            'stats': stats
        }

def load_config(project_root: Path) -> dict:
    """Load markdown splitter configuration."""
    config_file = project_root / '.claude' / 'guard' / 'quality_config.json'

    default_config = {
        "markdown_splitter": {
            "enabled": True,
            "auto_suggest_threshold": 2000,
            "target_chunk_size": 800,
            "split_strategy": "headers",
            "preserve_original": True,
            "create_index": True
        }
    }

    if config_file.exists():
        with open(config_file) as f:
            full_config = json.load(f)
            if "markdown_splitter" in full_config:
                config = default_config["markdown_splitter"].copy()
                config.update(full_config["markdown_splitter"])
                return config

    return default_config["markdown_splitter"]

def main():
    """Main entry point for markdown splitting."""
    if len(sys.argv) < 2:
        print("Usage: split_markdown.py <markdown-file>", file=sys.stderr)
        sys.exit(1)

    file_path = Path(sys.argv[1])

    if not file_path.exists():
        print(f"Error: File not found: {file_path}", file=sys.stderr)
        sys.exit(1)

    if not file_path.suffix.lower() in ['.md', '.markdown']:
        print(f"Error: Not a markdown file: {file_path}", file=sys.stderr)
        sys.exit(1)

    # Load configuration
    project_root = Path(os.getenv('CLAUDE_PROJECT_DIR', os.getcwd()))
    config = load_config(project_root)

    # Create splitter and split
    splitter = MarkdownSplitter(file_path, config)
    result = splitter.split()

    if result['success']:
        stats = result['stats']
        print(f"\n✅ Markdown file split successfully!\n")
        print(f"📄 Original: {stats['original_file']} ({stats['original_lines']} lines)")
        print(f"📦 Created: {stats['sections_created']} section files\n")
        print(f"Files created:")
        for f in stats['files_created']:
            print(f"  • {Path(f).name}")

        if stats['backup_created']:
            print(f"\n💾 Backup: {Path(stats['backup_created']).name}")

        print()
    else:
        print(f"\n❌ Failed to split markdown: {result['error']}\n", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
