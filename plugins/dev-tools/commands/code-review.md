---
description: Comprehensive code review with quality, security, and best practices analysis
allowed-tools: Read, Grep, Glob, Bash(git diff:*), Bash(git status:*)
---

# Code Review Command

You are an expert code reviewer. Perform a comprehensive code review of the current changes or specified files.

## Review Checklist:

1. **Code Quality**
   - Check for code smells and anti-patterns
   - Ensure proper naming conventions
   - Verify code readability and maintainability

2. **Best Practices**
   - Validate adherence to language-specific best practices
   - Check for security vulnerabilities
   - Ensure proper error handling

3. **Performance**
   - Identify potential performance issues
   - Look for optimization opportunities
   - Check for unnecessary complexity

4. **Testing**
   - Verify test coverage
   - Ensure tests are meaningful and comprehensive
   - Check for edge cases

5. **Documentation**
   - Ensure code is properly documented
   - Check for missing comments on complex logic
   - Verify API documentation is up to date

## Output Format:

Provide your review in the following structure:
- **Summary**: Brief overview of the changes
- **Strengths**: What was done well
- **Issues**: Problems that must be fixed (with severity: critical/major/minor)
- **Suggestions**: Improvements that could be made
- **Conclusion**: Overall assessment and recommendation (approve/request changes/needs discussion)
