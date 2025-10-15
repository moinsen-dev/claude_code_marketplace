# Quick Start Guide

Get up and running with the Claude Code Marketplace in minutes.

## For Users

### 1. Add the Marketplace

```bash
# From GitHub (when published)
/plugin marketplace add moinsen-dev/claude_code_marketplace

# From local directory
/plugin marketplace add /path/to/claude_code_marketplace
```

### 2. Browse Available Plugins

```bash
/plugin list
```

### 3. Install a Plugin

```bash
/plugin install dev-tools@claude-code-marketplace
```

### 4. Use Plugin Commands

```bash
# Run a code review
/code-review

# Get refactoring help
/refactor

# Debug assistance
/debug
```

### 5. Manage Plugins

```bash
# List installed plugins
/plugin list

# Uninstall a plugin
/plugin uninstall dev-tools

# Update marketplace
/plugin marketplace update claude-code-marketplace
```

## For Plugin Creators

### 1. Create Plugin Structure

```bash
mkdir -p plugins/my-plugin/{.claude-plugin,commands,agents,hooks}
```

### 2. Create Plugin Manifest

`plugins/my-plugin/.claude-plugin/plugin.json`:
```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "What your plugin does",
  "author": {
    "name": "Your Name",
    "email": "[email protected]"
  },
  "keywords": ["keyword1", "keyword2"],
  "category": "development"
}
```

### 3. Create a Command

`plugins/my-plugin/commands/hello.md`:
```markdown
# Hello Command

You are a friendly assistant. Greet the user and offer help.
```

### 4. Add to Marketplace

Update `.claude-plugin/marketplace.json`:
```json
{
  "plugins": [
    {
      "name": "my-plugin",
      "source": "./plugins/my-plugin",
      "description": "What your plugin does",
      "version": "1.0.0"
    }
  ]
}
```

### 5. Test Locally

```bash
# Add marketplace
/plugin marketplace add /path/to/claude_code_marketplace

# Install your plugin
/plugin install my-plugin@claude-code-marketplace

# Test command
/hello
```

### 6. Submit Plugin

1. Fork the repository
2. Add your plugin
3. Update README.md
4. Create pull request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## Plugin Components

### Commands (Slash Commands)
- Location: `plugins/your-plugin/commands/*.md`
- Usage: `/command-name`
- Purpose: Quick, reusable prompts for common tasks

### Agents
- Location: `plugins/your-plugin/agents/*.md`
- Usage: Through Task tool or workflows
- Purpose: Specialized AI assistants with expertise

### Hooks
- Location: `plugins/your-plugin/hooks/*.md`
- Types: `user-prompt-submit.md`, `tool-call-before.md`, `tool-call-after.md`
- Purpose: Customize Claude Code behavior at key points

### MCP Servers
- Location: `plugins/your-plugin/.mcp.json`
- Purpose: Connect external tools and data sources

## Common Tasks

### Adding MCP Servers

In your plugin directory or project root `.mcp.json`:
```json
{
  "mcpServers": {
    "server-name": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-name"]
    }
  }
}
```

### Setting Plugin Categories

Available categories:
- `development` - General dev tools
- `testing` - Testing and QA
- `documentation` - Docs generation
- `productivity` - Workflow enhancements
- `analysis` - Code analysis
- `deployment` - CI/CD tools
- `security` - Security scanning

### Versioning Plugins

Follow semantic versioning (semver):
- **1.0.0** - Initial release
- **1.0.1** - Bug fixes (patch)
- **1.1.0** - New features (minor)
- **2.0.0** - Breaking changes (major)

### Making Commands Accept Parameters

While commands are typically fixed prompts, you can design them to work with context:

```markdown
# Analyze Command

You are a code analyst.

If the user has selected code, analyze that.
If they mention a file, analyze that file.
Otherwise, ask what they want analyzed.

[Rest of command...]
```

## Troubleshooting

### Plugin Not Found
- Verify marketplace is added: `/plugin marketplace list`
- Check plugin name matches marketplace entry
- Try updating: `/plugin marketplace update name`

### Command Not Working
- Ensure plugin is installed: `/plugin list`
- Check command file exists in `commands/` directory
- Verify markdown syntax is correct

### MCP Server Not Loading
- Check `.mcp.json` syntax
- Verify command is available (e.g., `npx` or `uvx`)
- Check server logs in Claude Code settings

### Permission Issues
- Check `.claude/settings.local.json` for required permissions
- Some operations require explicit permission grants

## Resources

- **Full Documentation**: [README.md](README.md)
- **Contributing Guide**: [CONTRIBUTING.md](CONTRIBUTING.md)
- **Claude Code Docs**: https://docs.claude.com/claude-code
- **MCP Documentation**: https://modelcontextprotocol.io
- **Example Plugins**: `plugins/` directory

## Examples

### Example 1: Simple Command Plugin

```bash
mkdir -p plugins/greeter/commands
```

`plugins/greeter/commands/greet.md`:
```markdown
# Greet Command

You are a cheerful greeter. Say hello to the user and ask how you can help with their coding today.
```

Add to marketplace.json and test:
```bash
/plugin install greeter@claude-code-marketplace
/greet
```

### Example 2: Agent Plugin

```bash
mkdir -p plugins/reviewers/agents
```

`plugins/reviewers/agents/security-reviewer.md`:
```markdown
# Security Reviewer

You are a security expert. Review code for vulnerabilities, focusing on:
- Input validation
- Authentication/authorization
- Data exposure
- Injection attacks

Provide specific, actionable recommendations.
```

### Example 3: Hook Plugin

```bash
mkdir -p plugins/safety-checks/hooks
```

`plugins/safety-checks/hooks/user-prompt-submit.md`:
```markdown
# Safety Check Hook

Before executing commands, check:
1. If deleting files, confirm with user
2. If accessing production, add warning
3. If running destructive commands, suggest testing first
```

## Tips

- **Start Simple**: Begin with a single command plugin
- **Test Thoroughly**: Test in different project types
- **Clear Names**: Use descriptive, intuitive command names
- **Document Well**: Users should understand immediately
- **Be Specific**: Focused plugins are better than general ones
- **Share Examples**: Include usage examples in descriptions

## Next Steps

1. Explore the `dev-tools` plugin for real examples
2. Read [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guides
3. Check existing plugins for inspiration
4. Create your first plugin
5. Share with the community!

---

Need help? Open an issue or check the [Claude Code Documentation](https://docs.claude.com/claude-code).
