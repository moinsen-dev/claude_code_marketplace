---
description: Review and validate OpenSpec specifications for completeness, consistency, and quality
allowed-tools: Read, Grep, Glob, Bash(openspec:*)
---

# OpenSpec Spec Review Command

You are a quality assurance expert for specification-driven development. Validate OpenSpec change proposals and specifications to ensure they are complete, consistent, actionable, and ready for implementation.

**IMPORTANT**: This command works with OpenSpec's structure. It validates change proposals in `openspec/changes/<change-id>/` or existing specs in `openspec/specs/`.

## Input Parameters

Parse the user's command for:
- `<target>`: Change ID, spec path, or `openspec/` directory (optional, defaults to all active changes)
- `--strict`: Enable strict validation mode with higher standards (optional flag)
- `--type <change|spec>`: Validate change proposal or source spec (default: auto-detect)

## Validation Workflow

### Phase 0: Prerequisites Check

1. **Verify OpenSpec is initialized**
   ```bash
   if [ ! -d "openspec" ]; then
     echo "❌ OpenSpec not initialized. Please run: npx openspec init"
     exit 1
   fi
   ```

2. **Determine Target**
   - If no target provided: Validate all changes in `openspec/changes/`
   - If change-id provided: Validate `openspec/changes/<change-id>/`
   - If spec path provided: Validate that specific spec
   - If `openspec/` provided: Validate all changes and specs

3. **Use OpenSpec CLI First**
   ```bash
   openspec validate <change-id> --strict
   ```
   - This handles the core OpenSpec validation (delta format, scenarios, etc.)
   - Our additional checks add value on top

### Phase 1: OpenSpec CLI Validation

1. **Run Built-in Validation**
   ```bash
   openspec validate <change-id> --strict
   ```

2. **Capture Results**
   - Parse OpenSpec's validation output
   - Identify errors and warnings
   - Extract specific line numbers and issues

3. **Report CLI Results**
   ```markdown
   ## OpenSpec Validation: [✅ Passed | ⚠️ Warnings | ❌ Failed]

   ### Core Format Validation
   [Results from openspec validate --strict]
   ```

### Phase 2: Structure Validation

4. **Check Change Proposal Structure**

   For a change in `openspec/changes/<change-id>/`:
   ```markdown
   ✅ Required Files:
     ✅ proposal.md (exists)
     ✅ tasks.md (exists)
     ✅ specs/ (directory exists, <count> capability specs)

   ⚠️ Optional Files:
     [✅|❌] design.md (recommended for architectural changes)
     [✅|❌] questions.md (if ambiguities exist)
   ```

5. **Validate proposal.md Structure**
   ```markdown
   Required sections:
   - [✅|❌] ## Why
   - [✅|❌] ## What Changes
   - [✅|❌] ## Impact
   ```

6. **Validate tasks.md Structure**
   ```markdown
   Check:
   - [✅|❌] Tasks organized by phase/category
   - [✅|❌] Each task has checkbox format `- [ ]`
   - [✅|❌] Tasks are specific and actionable
   - [✅|❌] No overly broad tasks (>1 day of work)
   ```

7. **Validate Spec Files (Delta Format)**

   For each `specs/<capability>/spec.md`:
   ```markdown
   Required delta operations:
   - [✅|❌] Has at least one operation (## ADDED/MODIFIED/REMOVED Requirements)
   - [✅|❌] Every requirement has at least one scenario
   - [✅|❌] Scenarios use proper format: `#### Scenario:`
   - [✅|❌] Requirements use SHALL/SHOULD appropriately
   ```

### Phase 3: Content Quality Validation

8. **Requirement Quality Checks**

   For each requirement:
   - ✅ **Specific**: Not vague (bad: "system should be fast", good: "API response time <200ms")
   - ✅ **Measurable**: Has clear success criteria
   - ✅ **Actionable**: Developer knows what to build
   - ✅ **Testable**: Can write tests to verify
   - ✅ **Reasonable**: Not impossible or over-complex

9. **Scenario Quality Checks**

   For each scenario:
   - ✅ **Proper Format**: Uses `#### Scenario:` (4 hashtags)
   - ✅ **Descriptive Name**: Clear what's being tested
   - ✅ **Complete Flow**: Has GIVEN/WHEN/THEN or WHEN/THEN
   - ✅ **Testable Assertions**: THEN clauses are specific
   - ✅ **Coverage**: Success, failure, and edge cases included

10. **Task Quality Checks**

    For each task:
    - ✅ **Actionable**: Starts with verb (Implement, Create, Add, Configure)
    - ✅ **Specific**: Not too broad (bad: "build feature", good: "implement user login API endpoint")
    - ✅ **Sized appropriately**: Not too large (>8 hours) or too small (<30 mins)
    - ✅ **Clear completion criteria**: Know when it's done

11. **Common Issues to Flag**

    ❌ **Vague Language:**
    - "intuitive interface"
    - "fast performance"
    - "user-friendly design"
    - "robust system"
    - "scalable architecture" (without metrics)

    ❌ **Missing Details:**
    - No error handling specified
    - No validation rules
    - No edge cases considered
    - No data models defined

    ❌ **Ambiguous Requirements:**
    - "should work on most devices"
    - "reasonable load times"
    - "appropriate security"
    - "where applicable"

### Phase 4: Consistency Validation

12. **Cross-Reference Checks**

    ```markdown
    ## Consistency Analysis

    ### Proposal vs Specs
    ✅ All capabilities in proposal.md have corresponding spec files
    ✅ All spec files are mentioned in proposal.md

    ### Tasks vs Specs
    [✅|⚠️] Tasks in tasks.md reference specific capabilities
    [✅|⚠️] All capabilities have corresponding tasks
    [❌|⚠️] <count> tasks don't reference any spec

    ### Dependencies
    ✅ All dependencies are documented
    [⚠️|❌] Circular dependencies detected: [list]
    [⚠️|❌] External dependencies without setup tasks: [list]
    ```

13. **Terminology Consistency**
    - Check for inconsistent naming across files
    - Verify technical terms used consistently
    - Flag contradictions

### Phase 5: Completeness Validation

14. **Coverage Analysis**

    ```markdown
    ## Completeness Assessment

    ### Requirements Coverage
    - Functional requirements: [percentage]
    - Error handling: [percentage]
    - Edge cases: [percentage]
    - Non-functional requirements: [percentage]

    ### Test Coverage Planning
    - Unit test approach: [specified | missing]
    - Integration test approach: [specified | missing]
    - E2E test approach: [specified | missing]

    ### Documentation Planning
    - API documentation: [planned | missing]
    - User documentation: [planned | missing]
    - Deployment docs: [planned | missing]
    ```

15. **Gap Analysis**

    Identify missing elements:
    - Capabilities mentioned but not specified
    - Tasks without corresponding specs
    - Specs without corresponding tasks
    - Dependencies not documented
    - Prerequisites not defined

### Phase 6: Actionability Assessment

16. **Implementation Readiness**

    ```markdown
    ## Readiness Assessment

    ### Can development start? [✅ Yes | ⚠️ With caveats | ❌ No]

    **Ready to Implement:**
    ✅ <capability-1> - All details present, dependencies clear
    ✅ <capability-2> - Requirements specific and testable

    **Needs Clarification:**
    ⚠️ <capability-3>
      - Missing: [specific missing information]
      - Ambiguous: [specific ambiguous requirements]

    **Blocked:**
    ❌ <capability-4>
      - Depends on: [missing dependency]
      - Missing: [critical information]
    ```

17. **Missing Prerequisites**
    - Development environment setup
    - CI/CD pipeline requirements
    - Deployment strategy
    - Database migration approach
    - External service configuration

### Phase 7: Generate Validation Report

18. **Compile Comprehensive Report**

    ```markdown
    # OpenSpec Validation Report

    Generated: [timestamp]
    Validator: spec-review command

    ## Summary
    - **Target**: openspec/changes/<change-id>/
    - **Change ID**: <change-id>
    - **Files Validated**: <count> (<breakdown>)
    - **OpenSpec CLI Validation**: [✅ Passed | ⚠️ Warnings | ❌ Failed]
    - **Overall Status**: [✅ Ready | ⚠️ Ready with recommendations | ❌ Not ready]

    ## OpenSpec CLI Validation

    ```bash
    $ openspec validate <change-id> --strict
    [Output from OpenSpec validation]
    ```

    [✅ All checks passed | ⚠️ <count> warnings | ❌ <count> errors]

    ## Critical Issues (Must Fix) 🔴

    [List of blocking issues that prevent implementation]

    ### Issue 1: [Description]
    **Location**: [file:line]
    **Impact**: [Why this blocks implementation]
    **Fix**: [How to resolve]

    ## Warnings (Should Fix) ⚠️

    [List of issues that should be addressed but don't block implementation]

    ### Warning 1: [Description]
    **Location**: [file:line]
    **Issue**: [What's wrong]
    **Fix**: [How to resolve]

    ## Quality Assessment

    ### Structure: [Score]/10 [✅|⚠️|❌]
    - File organization
    - Naming conventions
    - Delta format compliance

    ### Completeness: [Score]/10 [✅|⚠️|❌]
    - Requirements coverage
    - Task breakdown
    - Documentation planning

    ### Clarity: [Score]/10 [✅|⚠️|❌]
    - Requirement specificity
    - Scenario clarity
    - Task actionability

    ### Consistency: [Score]/10 [✅|⚠️|❌]
    - Terminology usage
    - Cross-references
    - Dependency documentation

    ### Actionability: [Score]/10 [✅|⚠️|❌]
    - Implementation readiness
    - Clear acceptance criteria
    - Testability

    ## Detailed Findings

    ### proposal.md
    [Validation results]

    ### tasks.md
    [Validation results]

    ### specs/<capability-1>/spec.md
    [Validation results for each spec]

    ## Recommendations

    ### High Priority (Fix before implementation)
    1. [Recommendation]
    2. [Recommendation]

    ### Medium Priority (Fix during implementation)
    1. [Recommendation]
    2. [Recommendation]

    ### Low Priority (Nice to have)
    1. [Recommendation]
    2. [Recommendation]

    ## Next Steps

    1. **Fix critical issues**: [List]
    2. **Run validation again**:
       ```bash
       openspec validate <change-id> --strict
       ```
    3. **After fixes, review again**:
       ```bash
       /openspec:spec-review <change-id>
       ```
    4. **Once passing, start implementation**:
       - Review tasks in tasks.md
       - Implement following the specs
       - Check off tasks as completed

    ## OpenSpec Commands Reference

    ```bash
    openspec validate <change-id>           # Validate change proposal
    openspec show <change-id>               # View change details
    openspec diff <change-id>               # See what will change
    openspec list                           # View all changes
    ```
    ```

### Phase 8: Provide Actionable Feedback

19. **Summarize Key Actions**

    ```markdown
    ## Summary

    ### Status: [✅ Ready | ⚠️ Ready with recommendations | ❌ Not ready]

    ### Critical Actions Required
    [If status is ❌]
    - [ ] Fix [issue 1]
    - [ ] Fix [issue 2]
    - [ ] Re-run validation

    ### Recommended Improvements
    [If status is ⚠️]
    - [ ] Address [warning 1]
    - [ ] Address [warning 2]
    - [ ] Consider [suggestion]

    ### Ready to Proceed
    [If status is ✅]
    ✅ All validations passed
    ✅ Ready to start implementation
    Next: Review tasks in tasks.md and begin work
    ```

## Strict Mode

When `--strict` flag is used:

- Pass `--strict` to OpenSpec CLI validation
- Apply higher standards for all checks:
  - All requirements must have measurable acceptance criteria
  - All tasks must reference specific specs
  - No vague language allowed anywhere
  - All external dependencies must have setup tasks
  - All capabilities must have error handling specified
  - All capabilities must have test strategy documented
  - All scenarios must cover success, failure, and edge cases

Strict mode is recommended for:
- Production-ready specifications
- Large or critical projects
- Teams with high quality standards

## Example Usage

```bash
# Review all active changes
/openspec:spec-review

# Review specific change
/openspec:spec-review initial-reverse-planner

# Strict validation
/openspec:spec-review initial-reverse-planner --strict

# Review source spec (after archiving)
/openspec:spec-review user-auth --type spec
```

## Integration with OpenSpec CLI

This command **complements** OpenSpec's built-in `openspec validate` command:

1. **OpenSpec CLI** (`openspec validate`):
   - Validates delta format (ADDED/MODIFIED/REMOVED)
   - Checks requirement and scenario structure
   - Ensures proper markdown formatting
   - Validates cross-references

2. **This Command** (`/openspec:spec-review`):
   - Runs OpenSpec CLI validation first
   - Adds quality checks (vague language, ambiguity)
   - Checks task quality and specificity
   - Analyzes completeness and coverage
   - Assesses implementation readiness
   - Provides detailed improvement recommendations

Always use both for comprehensive validation!

## Common Validation Errors

### Error: "Requirement must have at least one scenario"
**Fix**: Add at least one `#### Scenario:` under the requirement

### Error: "Invalid delta operation header"
**Fix**: Use exactly: `## ADDED Requirements`, `## MODIFIED Requirements`, or `## REMOVED Requirements`

### Error: "Scenario format invalid"
**Fix**: Use `#### Scenario: Name` (4 hashtags, followed by colon and name)

### Warning: "Vague requirement language"
**Fix**: Replace vague terms with specific, measurable criteria

### Warning: "Task too broad"
**Fix**: Break down large tasks into smaller, estimable subtasks

## Best Practices

1. **Run Early and Often**: Validate as you write specs, not just at the end
2. **Fix Critical Issues First**: Don't proceed with warnings until criticals are resolved
3. **Use Strict Mode for Production**: Apply higher standards for production code
4. **Validate Before Implementation**: Always run before starting development
5. **Re-validate After Changes**: Run again after addressing issues

## Integration Notes

- Run after `/openspec:prd-breakdown` to ensure quality
- Run before starting implementation
- Include in code review process
- Can be automated in CI/CD pipelines
- Compatible with OpenSpec's three-stage workflow
