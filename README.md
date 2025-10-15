# Claude Code Marketplace

A custom marketplace for Claude Code plugins, providing specialized tools and workflows to enhance your development experience.

## What are Claude Code Plugins?

Claude Code plugins are collections of:
- **Slash commands**: Custom shortcuts for frequently-used operations
- **Agents**: Purpose-built AI agents for specialized development tasks
- **MCP servers**: Connections to tools and data sources through the Model Context Protocol
- **Hooks**: Customizations of Claude Code's behavior at key workflow points

## Installation

To add this marketplace to your Claude Code installation:

```bash
/plugin marketplace add moinsen-dev/claude_code_marketplace
```

Or if you have cloned this repository locally:

```bash
/plugin marketplace add /path/to/claude_code_marketplace
```

## Available Plugins

### Dev Tools
Essential development tools and utilities for common coding tasks.

**Commands:**
- `/code-review` - Comprehensive code review with quality checks
- `/refactor` - Intelligent code refactoring while preserving functionality
- `/debug` - Systematic debugging assistance
- `/social-media` - Generate professional social media posts for your project (supports `--platform` and `--language` options)

**Agents:**
- `test-generator` - Generate comprehensive test suites

**Usage Examples:**

Generate a LinkedIn post in English (default):
```bash
/social-media
```

Generate for a specific platform and language:
```bash
/social-media --platform linkedin --language german
```

**Installation:**
```bash
/plugin install dev-tools@claude-code-marketplace
```

### OpenSpec
Spec-driven development plugin for breaking down PRDs into actionable specifications and tasks. Complements the existing OpenSpec commands (`/openspec:proposal`, `/openspec:apply`, `/openspec:archive`) with PRD analysis and breakdown capabilities.

**Commands:**
- `/openspec:prd-breakdown` - Break down PRD into specs and tasks with full implementation plan
- `/openspec:prd-split` - Split large PRDs into smaller, manageable feature specifications
- `/openspec:prd-analyze` - Analyze PRD complexity and suggest breakdown strategies
- `/openspec:spec-review` - Review and validate specs for completeness and quality

**Features:**
- Intelligent PRD analysis and complexity assessment
- Automatic breakdown of large PRDs into manageable specs
- Support for both OpenSpec CLI and GitHub's spec-kit
- Dependency graph analysis and critical path identification
- Quality validation with actionable recommendations and auto-fix
- Seamless integration with OpenSpec workflow

**Complete Workflow:**
1. Analyze PRD → `/openspec:prd-analyze`
2. Break down → `/openspec:prd-breakdown`
3. Review quality → `/openspec:spec-review`
4. Create proposal → `/openspec:proposal` (existing)
5. Implement → `/openspec:apply` (existing)
6. Archive → `/openspec:archive` (existing)

**Usage Examples:**

Analyze PRD complexity first:
```bash
/openspec:prd-analyze ./requirements.md --detailed
```

Break down PRD into specs and tasks:
```bash
/openspec:prd-breakdown ./docs/PRD.md
```

Split a large PRD into feature specs:
```bash
/openspec:prd-split ./PRD.md --strategy features
```

Review and validate specifications:
```bash
/openspec:spec-review --strict --fix
```

Use spec-kit instead of OpenSpec CLI:
```bash
/openspec:prd-breakdown ./PRD.md --tool speckit
```

**Installation:**
```bash
/plugin install openspec@claude-code-marketplace
```

**Recommended Dependencies:**
```bash
# Install OpenSpec CLI (optional but recommended)
npm install -g @fission-ai/openspec@latest

# Or use spec-kit (alternative)
uvx --from git+https://github.com/github/spec-kit.git specify
```

## Creating Your Own Plugins

### Plugin Structure

Each plugin should follow this structure:

```
plugins/your-plugin/
├── .claude-plugin/
│   └── plugin.json          # Plugin metadata (optional)
├── commands/                 # Slash commands (markdown files)
│   ├── command1.md
│   └── command2.md
├── agents/                   # AI agents (markdown files)
│   └── agent1.md
└── hooks/                    # Event handlers (optional)
    └── hook1.md
```

### Plugin Metadata (plugin.json)

```json
{
  "name": "your-plugin",
  "version": "1.0.0",
  "description": "Plugin description",
  "author": {
    "name": "Your Name",
    "email": "[email protected]"
  },
  "keywords": ["keyword1", "keyword2"],
  "category": "development"
}
```

### Adding to Marketplace

1. Create your plugin in the `plugins/` directory
2. Update `.claude-plugin/marketplace.json` to include your plugin:

```json
{
  "name": "your-plugin",
  "source": "./plugins/your-plugin",
  "description": "Plugin description",
  "version": "1.0.0",
  "author": {
    "name": "Your Name"
  }
}
```

### Commands

Commands are markdown files that contain prompts for Claude. The file name becomes the command name.

Example `commands/hello.md`:
```markdown
# Hello Command

You are a friendly assistant. Greet the user warmly and ask how you can help them today.
```

Usage: `/hello`

### Agents

Agents are specialized AI assistants defined in markdown files with specific expertise and behaviors.

Example `agents/code-reviewer.md`:
```markdown
# Code Reviewer Agent

You are an expert code reviewer with 10+ years of experience...

## Your responsibilities:
- Review code for quality and best practices
- Identify potential bugs and security issues
- Suggest improvements
```

## MCP Servers

This marketplace includes MCP server configurations in `.mcp.json`:

- **sequential-thinking**: Advanced reasoning with chain-of-thought
- **package-hero**: Package version management and quality ratings

## Development

### Local Testing

1. Clone this repository
2. Add as a local marketplace:
   ```bash
   /plugin marketplace add /path/to/claude_code_marketplace
   ```
3. Install plugins:
   ```bash
   /plugin install dev-tools@claude-code-marketplace
   ```

### Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a new plugin or improve existing ones
3. Test your changes locally
4. Submit a pull request

## Resources

- [Claude Code Documentation](https://docs.claude.com/claude-code)
- [Plugin Development Guide](https://docs.claude.com/en/docs/claude-code/plugins)
- [Model Context Protocol](https://modelcontextprotocol.io)

## License

MIT License - see LICENSE file for details

## Support

For issues or questions:
- Open an issue on GitHub
- Visit [Claude Code Documentation](https://docs.claude.com/claude-code)

---

Built with Claude Code
