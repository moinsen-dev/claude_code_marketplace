# Code Quality Guardian Plugin

Prevent bloated files and enforce architectural best practices by automatically detecting oversized files and guiding Claude toward better code organization.

## The Problem 🤔

Without guidance, LLMs might create files that are:
- **Too large** (1000+ lines)
- **Mixed concerns** (data + logic + UI in one file)
- **Hard to maintain** (god objects, spaghetti code)
- **Difficult to test** (tightly coupled dependencies)

## The Solution 💡

**Code Quality Guardian** acts like an **architectural advisor**:

1. **Detects** when Claude tries to create files exceeding size limits
2. **Blocks** the operation with helpful guidance
3. **Suggests** better architectural approaches
4. **Provides** a refactoring agent to help restructure code

Think of it as: **"An experienced architect looking over Claude's shoulder"** 🏗️

## Features

- 📏 **Automatic Size Checking** - Intercepts file writes before they happen
- 🚫 **TODO/FIXME Blocking** - Prevents incomplete code with TODO comments
- 🎯 **Smart Thresholds** - Different limits for different file types
- 🤖 **Refactoring Agent** - Expert guidance for breaking up large files
- ⚙️ **Configurable** - Customize thresholds per project
- 🚀 **Zero Config** - Works out of the box with sensible defaults

## Installation

From the Moinsen marketplace:

```bash
claude plugin install moinsen-claude-code-marketplace
```

## Default Thresholds

| File Type | Max Lines | Rationale |
|-----------|-----------|-----------|
| `.dart`, `.py`, `.ts`, `.js` | 800 | General code files |
| `.tsx`, `.jsx`, `.vue` | 600 | UI components (smaller = better) |
| `.java`, `.go` | 1000 | Larger files common in these langs |
| `.md`, `.txt` | 5000 | Documentation can be longer |
| `.json` | 2000 | Data files |
| Default | 1000 | Catch-all |

## How It Works

### When Claude Tries to Create a Large File:

```
Claude: "I'll create user_service.dart with all the logic..."
Guardian: 🛑 BLOCKED!

📏 CODE QUALITY GUARDIAN: File too large!
   📄 File: user_service.dart  
   📊 Size: 1200 lines (threshold: 800)

   💡 Instead of creating one large file, consider:
      • Breaking into smaller, focused modules
      • Using domain-driven design principles
      • Separating concerns (data, logic, UI)

   🤖 Try: Ask me to refactor this into multiple files
   🤖 Or use: /refactor to get architectural guidance
```

Claude sees this, adjusts approach, creates multiple focused files instead! ✅

## TODO/FIXME Blocking 🚫

**The Problem**: LLMs often leave TODO comments instead of completing implementations:

```dart
// TODO: Add error handling
// FIXME: This needs optimization  
// HACK: Temporary solution
// XXX: Not thread-safe
```

**Code Quality Guardian blocks this!**

```
Claude: "I'll add this feature with a TODO for error handling..."
Guardian: 🛑 BLOCKED!

🚫 CODE QUALITY GUARDIAN: TODO/FIXME comments detected!
   📄 File: user_service.dart
   ⚠️  Found 3 incomplete marker(s):

      Line   42: // TODO: Add error handling here
      Line   87: // FIXME: Optimize this query
      Line  112: // HACK: Temporary workaround for API issue

   💡 Code should be complete and production-ready:
      • Implement the missing functionality instead
      • Don't leave breadcrumbs for later
      • If you can't implement it, discuss limitations

   🤖 Try: Ask me to complete these implementations
   ⚙️  To allow TODOs: Set 'block_todos': false in quality_config.json
```

**Result**: Claude implements the error handling, optimizes the query, and finds a proper solution instead of leaving TODOs! ✅

**Blocked patterns**: TODO, FIXME, HACK, XXX, TEMP, TMP

## The Refactoring Agent

Included: A specialized **Refactoring Architect** agent that helps break down large files.

### Invoke the Agent:

```
"Help me refactor this into proper modules"
"Split this following domain-driven design"
"Break this into data, logic, and UI layers"
```

### Agent's Approach:

1. **Analyze** the file's responsibilities
2. **Identify** natural domain boundaries
3. **Propose** modular architecture
4. **Create** focused, single-responsibility files
5. **Set up** proper dependencies

### Example Refactoring:

**Before:**
```
user_service.dart (1200 lines)
├── User model
├── User repository
├── API client
├── Validation
├── UI widgets
└── State management
```

**After:**
```
models/user.dart (50 lines)
repositories/user_repository.dart (120 lines)  
services/user_api_client.dart (100 lines)
validators/user_validator.dart (80 lines)
ui/user_profile_widget.dart (150 lines)
state/user_state.dart (100 lines)
```

## Configuration

### View Current Config

```bash
/quality-config
```

### Customize Thresholds

Create `.claude/quality_config.json` in your project:

```json
{
  "default": 1000,
  "block_todos": true,
  "todo_patterns": ["TODO", "FIXME", "HACK", "XXX", "TEMP", "TMP"],
  "extensions": {
    ".dart": 600,    // Stricter for Flutter
    ".py": 500,      // Very strict Python
    ".tsx": 400      // Tiny React components
  }
}
```

**Configuration options:**
- `default`: Default line limit for all files
- `block_todos`: Enable/disable TODO blocking (default: true)
- `todo_patterns`: List of patterns to block (case-insensitive in comments)
- `extensions`: File-type-specific line limits

## Real-World Usage

### Scenario 1: Flutter App Development

```
Claude tries: Create lib/main.dart with app + routing + state
Guardian blocks: File would be 1500 lines
Claude adjusts: Creates:
  - lib/main.dart (50 lines - app entry)
  - lib/routing/app_router.dart (200 lines)
  - lib/state/app_state.dart (150 lines)
```

### Scenario 2: Backend API

```
Claude tries: Create api/server.py with all endpoints
Guardian blocks: File would be 2000 lines  
Claude adjusts: Creates:
  - api/server.py (100 lines - setup)
  - api/routes/users.py (300 lines)
  - api/routes/products.py (250 lines)
  - api/middleware/auth.py (150 lines)
```

## Why This Matters

### Without Code Quality Guardian:
- ❌ Monolithic files
- ❌ Mixed responsibilities  
- ❌ Incomplete code with TODOs
- ❌ Hard to test
- ❌ Difficult to maintain
- ❌ Poor reusability

### With Code Quality Guardian:
- ✅ Focused modules
- ✅ Clear separation of concerns
- ✅ Complete, production-ready code
- ✅ Easy to test
- ✅ Maintainable architecture
- ✅ Reusable components

## Philosophy

Based on **Domain-Driven Design** principles:
- **Bounded Contexts**: Clear module boundaries
- **Single Responsibility**: Each file does one thing well
- **Separation of Concerns**: Data, logic, and UI separated
- **Testability**: Small files are easier to test
- **Maintainability**: Easy to understand and modify

## Commands

| Command | Description |
|---------|-------------|
| `/quality-config` | View current thresholds |
| "refactor this" | Invoke refactoring agent |

## Integration with Other Plugins

Works great with:
- **File Guardian**: Protects sensitive files
- **Dev Tools**: Code review and debugging
- **OpenSpec**: Spec-driven development

## Tips for Success

1. **Trust the Guardian** - If it blocks, there's probably a better way
2. **Use the Agent** - The refactoring agent is your friend
3. **Think Domains** - Organize by business domain, not technical layers
4. **Start Small** - Better to split early than merge later
5. **Embrace Modules** - More files ≠ more complexity

## The Architect's Wisdom 🏛️

> "A system is maintainable not because it's small, but because each piece is small."

> "If your file does more than one thing, it should be multiple files."

> "Good architecture isn't about fewer files—it's about focused files."

## License

MIT
