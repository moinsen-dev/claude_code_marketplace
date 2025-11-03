# File Guardian Plugin

Protect sensitive files from accidental edits and prevent unnecessary markdown summaries by Claude Code.

## Features

- 🛡️ **Blacklist Protection** - Prevent edits to sensitive files
- 📝 **Markdown Control** - Block unsolicited summary/recap markdown files
- ⚡ **Automatic Blocking** - Hooks intercept operations before they happen
- 🎯 **Pattern Matching** - Support for globs, directories, and exact matches
- 📋 **Easy Management** - Slash commands to add/remove protections
- 🚀 **Zero Configuration** - Works out of the box with sensible defaults

## Installation

From the Moinsen marketplace:

```bash
claude plugin install moinsen-claude-code-marketplace
```

The file-guardian plugin will be available automatically.

## Usage

### View Protected Files

```bash
/protect list
```

### Add Protection

```bash
/protect .env              # Protect specific file
/protect secrets/          # Protect directory
/protect *.key             # Protect by pattern
```

### Remove Protection

```bash
/unprotect .env.example
```

## How It Works

**Think of it like a security bouncer for your files** 🎭:

1. You maintain a blacklist of forbidden patterns
2. When Claude tries to edit a file
3. The hook checks against the blacklist
4. If matched → blocks the edit ❌
5. If not matched → allows the edit ✅

## Markdown Protection 📝

**The Problem**: Claude often creates unnecessary summary markdown files:

```
Claude: *Creates user_service.dart, user_repository.dart, user_model.dart*
Claude: *Also creates SUMMARY.md with "I created 3 files: ..."*
You: "I can see the 3 files! Why the summary??" 😤
```

**File Guardian blocks this!**

### Blocked Patterns

**Suspicious filenames:**
- `SUMMARY.md`, `summary.md`
- `RECAP.md`, `recap.md`  
- `CHANGES.md`, `changes.md`
- `COMPLETION.md`, `report.md`
- `OUTPUT.md`, `NOTES.md`
- Any file with summary-like names

**Suspicious content:**
- "I created the following files..."
- "Here's what I generated..."
- "Task completed successfully..."
- "Changes made:"
- "Files created:"

### Example Block

```
Claude: *Tries to create SUMMARY.md*
Guardian: 🛑 BLOCKED!

🛡️  FILE GUARDIAN: Unsolicited markdown file blocked
   📄 File: SUMMARY.md
   🚫 Reason: Filename suggests auto-generated summary

   💡 Markdown files should only be created when explicitly requested:
      • User asks: "Create a README.md documenting the API"
      • User asks: "Write documentation in markdown"
      • Don't create summary files listing what you did

   ℹ️  The user can see what files were created in the output
```

**Result**: No more noise! Claude stops creating "I did this" summaries! ✅

### When Markdown IS Allowed

Markdown files are **allowed** when:
1. **User explicitly requests**: "Create a README.md"
2. **Project documentation**: docs/ folder
3. **Standard files**: CONTRIBUTING.md, CHANGELOG.md, LICENSE.md
4. **Configured patterns**: Custom allow list in config

### Configuration

Create `.claude/file_guardian_config.json`:

```json
{
  "block_unsolicited_markdown": true,
  "block_summary_content": true,
  "allow_patterns": [
    "docs/",              // Allow docs directory
    "README.md",          // Allow README
    "CONTRIBUTING.md",    // Allow contribution guide
    "api-docs.md"         // Allow specific file
  ]
}
```

**Disable completely** (not recommended):
```json
{
  "block_unsolicited_markdown": false
}
```

## Configuration

The blacklist is stored in `.claude/forbidden_paths.txt` in your project root.

On first use, File Guardian creates a default blacklist with common sensitive files.

Manual editing:

```bash
# Edit directly
vim .claude/forbidden_paths.txt

# Or use commands
/protect <pattern>
/unprotect <pattern>
```

## Pattern Examples

```txt
# Exact files
.env
config.prod.json

# Directories (trailing slash)
secrets/
.git/

# Glob patterns
*.key
*-credentials.json

# Complex patterns
src/**/*.secret.ts
```

## Default Protections

File Guardian comes with sensible defaults:

- Environment files (.env, .env.*)
- Secrets directory
- Credential files (*.key, *.pem, *credentials*.json)
- Lock files (package-lock.json, pubspec.lock, etc.)
- Git internals (.git/)
- Build artifacts (build/, dist/, node_modules/)
- Database files (*.db, *.sqlite)

## Why Use File Guardian?

**Without File Guardian**: Claude might accidentally edit your `.env` file or `package-lock.json`, causing security issues or dependency conflicts.

**With File Guardian**: These files are protected. Claude gets a clear error message and can't proceed with the edit.

## License

MIT
