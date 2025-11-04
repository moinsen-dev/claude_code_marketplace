---
description: Split large markdown files into manageable sections with automatic navigation
---

# split-markdown

Intelligently split a large markdown file into context-friendly sections with automatic table of contents and navigation.

## Usage

```bash
# Split a specific markdown file
/guard:split-markdown <file-path>

# Examples
/guard:split-markdown task.md
/guard:split-markdown docs/PRD.md
/guard:split-markdown ./planning/requirements.md
```

## What It Does

When you split a markdown file, the Guard plugin will:

1. **Analyze Structure** - Parse the document to identify logical sections based on headers
2. **Propose Split** - Show you how the file will be divided before making changes
3. **Create Index** - Generate `00-<basename>.md` with table of contents and navigation
4. **Create Sections** - Generate numbered files (`01-`, `02-`, etc.) for each section
5. **Add Navigation** - Include bidirectional links between index and sections
6. **Backup Original** - Save the original file as `<filename>.backup`

## Output Structure

For a file named `task.md`, you'll get:

```
task.md.backup          # Original file (backup)
00-task.md              # Index with TOC
01-task.md              # First section
02-task.md              # Second section
03-task.md              # Third section
...
```

### Index File (00-task.md)

Contains:
- Document title
- Table of contents with links to all sections
- Quick navigation statistics (total sections, line counts)
- Overview explaining why the split was done
- Metadata (split date, strategy used)

### Section Files (01-task.md, 02-task.md, etc.)

Each section includes:
- Section title
- Navigation header (links to index, previous, next)
- Full section content (preserved formatting)
- Navigation footer (same links as header)

## Configuration

The splitting behavior is controlled by `.claude/quality_config.json`:

```json
{
  "markdown_splitter": {
    "enabled": true,
    "auto_suggest_threshold": 2000,
    "target_chunk_size": 800,
    "split_strategy": "headers",
    "preserve_original": true,
    "create_index": true
  }
}
```

### Configuration Options

- **`auto_suggest_threshold`** (default: 2000)
  - Line count threshold for automatic split suggestions
  - When a markdown file exceeds this, Guard will offer to split it

- **`target_chunk_size`** (default: 800)
  - Target lines per section (used with "smart" strategy)
  - Helps keep sections at manageable sizes

- **`split_strategy`** (default: "headers")
  - `"headers"` - Split at each top-level header (# title)
  - `"smart"` - Group sections to target chunk size while respecting boundaries

- **`preserve_original`** (default: true)
  - Keep backup of original file as `<filename>.backup`
  - Set to false to remove original after split

- **`create_index`** (default: true)
  - Generate `00-<basename>.md` index file
  - Set to false to only create section files

## Split Strategies

### Headers Strategy (Default)

Splits at every top-level header (`# Title`):

**Pros:**
- Preserves logical document structure
- Sections are semantically meaningful
- Easy to understand split points

**Cons:**
- May create uneven section sizes

**Best for:**
- Well-structured documents with clear top-level sections
- PRDs, design docs, technical specifications

### Smart Strategy

Groups sections to target chunk size while respecting header boundaries:

**Pros:**
- More consistent section sizes
- Still respects logical boundaries
- Better for documents with many small sections

**Cons:**
- May group unrelated content together

**Best for:**
- Documents with many small sections
- Task lists with many items
- API documentation with many endpoints

## Examples

### Example 1: Large PRD Document

```bash
/guard:split-markdown requirements.md
```

**Before:**
```
requirements.md (3500 lines)
  # Overview
  # User Stories
  # Technical Requirements
  # Architecture
  # Testing Strategy
```

**After:**
```
requirements.md.backup
00-requirements.md (index)
01-requirements.md (Overview - 400 lines)
02-requirements.md (User Stories - 900 lines)
03-requirements.md (Technical Requirements - 1100 lines)
04-requirements.md (Architecture - 700 lines)
05-requirements.md (Testing Strategy - 400 lines)
```

### Example 2: Implementation Task List

```bash
/guard:split-markdown tasks.md
```

**Before:**
```
tasks.md (4200 lines)
  # Backend Tasks
    ## API Endpoints (many subtasks)
    ## Database Schema (many subtasks)
  # Frontend Tasks
    ## Components (many subtasks)
    ## Pages (many subtasks)
```

**After:**
```
tasks.md.backup
00-tasks.md (index)
01-tasks.md (Backend Tasks - 2100 lines)
02-tasks.md (Frontend Tasks - 2100 lines)
```

### Example 3: API Documentation

```bash
/guard:split-markdown api-docs.md
```

With `"split_strategy": "smart"` in config:

**Before:**
```
api-docs.md (5000 lines)
  # Authentication
  # User Endpoints (50+ endpoints)
  # Data Endpoints (40+ endpoints)
  # Admin Endpoints (30+ endpoints)
```

**After:**
```
api-docs.backup
00-api-docs.md (index)
01-api-docs.md (Authentication - 600 lines)
02-api-docs.md (User Endpoints Part 1 - 800 lines)
03-api-docs.md (User Endpoints Part 2 - 850 lines)
04-api-docs.md (Data Endpoints Part 1 - 800 lines)
05-api-docs.md (Data Endpoints Part 2 - 750 lines)
06-api-docs.md (Admin Endpoints - 700 lines)
```

## When to Use

Split a markdown file when:

- 📄 **File exceeds 2000 lines** - May hit LLM context limits
- 🔍 **Hard to navigate** - Takes too long to find sections
- ⚡ **Performance issues** - Editor or tools slow down with large file
- 👥 **Team collaboration** - Easier to work on separate sections
- 📝 **Documentation** - Better organization for large docs

## Integration with Guard

The markdown splitter integrates with Guard's file size checking:

1. When you try to write a large markdown file (>2000 lines)
2. Guard detects it exceeds the threshold
3. Guard offers: "This file is large. Would you like to split it?"
4. If you say "yes", the markdown-splitter agent is automatically launched
5. The agent analyzes, proposes a split, and executes with your approval

This provides **proactive** splitting suggestions without manual command invocation.

## Implementation

This command launches the **markdown-splitter agent** with the specified file:

```bash
# The agent will:
# 1. Read and analyze the file structure
# 2. Present a proposed split plan
# 3. Ask for confirmation
# 4. Execute the split using split_markdown.py
# 5. Verify results and report success
```

## Tips

1. **Review before splitting** - Always check the proposed split plan
2. **Adjust strategy** - Switch between "headers" and "smart" for different results
3. **Update references** - If other files link to the original, update them
4. **Commit original first** - Use git to track changes before splitting
5. **Test navigation** - After splitting, click through a few section links

## Related Commands

- `/guard:config` - View and configure splitting thresholds
- `/guard:init` - Initialize Guard with default configuration

## See Also

- **markdown-splitter agent** - The AI agent that performs the analysis and splitting
- **split_markdown.py** - The underlying Python script
- `.claude/quality_config.json` - Configuration file

---

**Need help?** The markdown-splitter agent will guide you through the process and explain each step.
