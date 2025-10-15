# Contributing to Claude Code Marketplace

Thank you for your interest in contributing! This guide will help you create and submit plugins to this marketplace.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Plugin Development](#plugin-development)
3. [Testing Your Plugin](#testing-your-plugin)
4. [Submission Process](#submission-process)
5. [Best Practices](#best-practices)

## Getting Started

### Prerequisites

- Claude Code installed and configured
- Basic understanding of markdown
- Familiarity with the tools/languages your plugin will support

### Fork and Clone

1. Fork this repository
2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR-USERNAME/claude_code_marketplace.git
   cd claude_code_marketplace
   ```

## Plugin Development

### 1. Create Plugin Structure

Create a new directory in `plugins/` with your plugin name (use kebab-case):

```bash
mkdir -p plugins/my-plugin/{.claude-plugin,commands,agents,hooks}
```

### 2. Create Plugin Manifest

Create `plugins/my-plugin/.claude-plugin/plugin.json`:

```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "Brief description of what your plugin does",
  "author": {
    "name": "Your Name",
    "email": "[email protected]"
  },
  "homepage": "https://github.com/your-username/project",
  "license": "MIT",
  "keywords": ["keyword1", "keyword2", "keyword3"],
  "category": "development"
}
```

**Available Categories:**
- `development` - General development tools
- `testing` - Testing and QA tools
- `documentation` - Documentation generators
- `productivity` - Workflow and productivity enhancements
- `analysis` - Code analysis and linting
- `deployment` - Deployment and CI/CD
- `security` - Security tools and scanners

### 3. Create Commands

Commands are markdown files in the `commands/` directory. The filename (without .md) becomes the command name.

**Example:** `commands/analyze-code.md`

```markdown
# Analyze Code Command

You are an expert code analyst specialized in [LANGUAGE/FRAMEWORK].

## Your Task:

Analyze the provided code for:
1. Code quality and maintainability
2. Performance issues
3. Security vulnerabilities
4. Best practice violations

## Analysis Steps:

1. **Read and understand** the code structure
2. **Identify issues** with clear explanations
3. **Prioritize findings** by severity (Critical/High/Medium/Low)
4. **Suggest improvements** with code examples
5. **Provide metrics** (complexity, maintainability score, etc.)

## Output Format:

### Summary
Brief overview of the code quality

### Findings
- **[Severity]** Issue description
  - Location: file:line
  - Impact: What problems this causes
  - Solution: How to fix it

### Metrics
- Lines of Code: X
- Cyclomatic Complexity: Y
- Maintainability Index: Z

### Recommendations
Prioritized list of improvements
```

**Command Best Practices:**
- Use clear, descriptive filenames
- Start with a role definition ("You are an expert...")
- Provide clear instructions and expected output
- Include examples when helpful
- Keep scope focused on one task

### 4. Create Agents

Agents are specialized AI assistants. Create them in the `agents/` directory.

**Example:** `agents/security-auditor.md`

```markdown
# Security Auditor Agent

You are a security expert specializing in application security audits and vulnerability assessment.

## Expertise Areas:
- OWASP Top 10 vulnerabilities
- Secure coding practices
- Authentication and authorization
- Data protection and privacy
- Input validation and sanitization
- Cryptography best practices

## Your Approach:

1. **Reconnaissance**
   - Understand the application architecture
   - Identify attack surfaces
   - Map data flows

2. **Vulnerability Assessment**
   - Check for common vulnerabilities
   - Test input validation
   - Review authentication mechanisms
   - Assess authorization controls

3. **Risk Analysis**
   - Evaluate severity of findings
   - Consider exploit likelihood
   - Assess business impact

4. **Recommendations**
   - Provide specific fixes
   - Include code examples
   - Prioritize by risk level
   - Suggest preventive measures

## Output Format:

### Executive Summary
High-level overview of security posture

### Vulnerabilities
For each finding:
- **Title**: Clear vulnerability name
- **Severity**: Critical/High/Medium/Low/Info
- **Description**: What the vulnerability is
- **Location**: Where it exists
- **Proof of Concept**: How to reproduce
- **Impact**: Potential consequences
- **Remediation**: How to fix it
- **References**: Related CWEs, CVEs, or standards

### Security Metrics
- Total Vulnerabilities: X
- Critical: Y
- High: Z
- Risk Score: N/100

### Recommendations
Prioritized remediation roadmap
```

**Agent Best Practices:**
- Define clear expertise and scope
- Establish a consistent approach/methodology
- Specify output format
- Include severity/priority frameworks
- Make them reusable across projects

### 5. Create Hooks (Optional)

Hooks allow you to customize Claude Code's behavior at key points. Create them in the `hooks/` directory.

**Available Hook Types:**
- `user-prompt-submit.md` - Runs before user prompts are processed
- `tool-call-before.md` - Runs before tool calls
- `tool-call-after.md` - Runs after tool calls

**Example:** `hooks/user-prompt-submit.md`

```markdown
# User Prompt Submit Hook

Before processing user input, validate and enhance it.

## Actions:

1. Check if the prompt contains file paths - verify they exist
2. If the prompt asks for code changes, remind about writing tests
3. If the prompt mentions deployment, add a safety checklist
4. Expand ambiguous requests with clarifying questions
```

### 6. Add MCP Servers (Optional)

If your plugin needs external tools or data sources, add MCP server configurations.

Create or update `.mcp.json` in your plugin directory:

```json
{
  "mcpServers": {
    "your-server": {
      "command": "node",
      "args": ["path/to/server.js"]
    }
  }
}
```

## Testing Your Plugin

### Local Testing

1. Add this marketplace locally:
   ```bash
   /plugin marketplace add /path/to/claude_code_marketplace
   ```

2. Install your plugin:
   ```bash
   /plugin install my-plugin@claude-code-marketplace
   ```

3. Test all commands:
   ```bash
   /my-command
   ```

4. Test agents through the Task tool or relevant workflows

### Validation Checklist

- [ ] All commands execute without errors
- [ ] Commands produce expected outputs
- [ ] Agents behave as intended
- [ ] Documentation is clear and complete
- [ ] Plugin metadata is accurate
- [ ] No hardcoded paths or sensitive data
- [ ] Works across different project types

## Submission Process

### 1. Update Marketplace

Add your plugin to `.claude-plugin/marketplace.json`:

```json
{
  "name": "my-plugin",
  "source": "./plugins/my-plugin",
  "description": "Brief description of what your plugin does",
  "version": "1.0.0",
  "author": {
    "name": "Your Name",
    "email": "[email protected]"
  },
  "keywords": ["keyword1", "keyword2"],
  "category": "development"
}
```

### 2. Update README

Add your plugin to the "Available Plugins" section in README.md:

```markdown
### My Plugin
Brief description of what your plugin does.

**Commands:**
- `/command-1` - Description
- `/command-2` - Description

**Agents:**
- `agent-1` - Description

**Installation:**
\`\`\`bash
/plugin install my-plugin@claude-code-marketplace
\`\`\`
```

### 3. Create Pull Request

1. Commit your changes:
   ```bash
   git add .
   git commit -m "Add my-plugin: brief description"
   ```

2. Push to your fork:
   ```bash
   git push origin main
   ```

3. Create a Pull Request on GitHub with:
   - Clear title: "Add [plugin-name] plugin"
   - Description of what your plugin does
   - List of commands and agents included
   - Any special requirements or dependencies

### 4. Review Process

Your PR will be reviewed for:
- Code quality and security
- Documentation completeness
- Functionality and usefulness
- Compatibility with Claude Code
- Adherence to guidelines

## Best Practices

### General

1. **Keep it focused** - One plugin should do one thing well
2. **Clear documentation** - Users should understand what it does instantly
3. **Descriptive naming** - Use clear, descriptive names for commands/agents
4. **Error handling** - Guide users when things go wrong
5. **Examples** - Include examples in your documentation

### Command Design

- Make commands reusable across projects
- Avoid hardcoding project-specific details
- Accept parameters where appropriate
- Provide clear output format
- Handle edge cases gracefully

### Agent Design

- Give agents clear expertise domains
- Define consistent methodologies
- Make output actionable
- Include severity/priority frameworks
- Provide specific, implementable recommendations

### Security

- Never include credentials or secrets
- Don't execute arbitrary code without validation
- Validate all file paths and user inputs
- Document security considerations
- Follow least privilege principle

### Performance

- Keep prompts concise and focused
- Avoid redundant instructions
- Use efficient tool calls
- Consider token limits
- Test with real-world scenarios

## Questions?

- Open an issue for discussion
- Check existing plugins for examples
- Review [Claude Code Documentation](https://docs.claude.com/claude-code)

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to the Claude Code Marketplace!
