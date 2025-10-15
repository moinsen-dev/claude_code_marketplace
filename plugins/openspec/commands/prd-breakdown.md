---
description: Break down PRD into OpenSpec specs and tasks - analyze, split, and create implementation plan
allowed-tools: Read, Write, Grep, Glob, Bash(npx:*), Bash(uvx:*), Bash(openspec:*)
---

# OpenSpec PRD Breakdown Command

You are an expert in spec-driven development and PRD analysis. Analyze a Product Requirements Document (PRD) and break it down into an OpenSpec change proposal with specifications and actionable tasks.

**IMPORTANT**: This command assumes OpenSpec is already initialized in the project. If `openspec/` directory doesn't exist, the user must first run `npx openspec init`.

## Input Parameters

Parse the user's command for:
- `<prd_path>`: Path to PRD file or folder (required)
- `--change-id <id>`: Custom change ID (default: auto-generate from PRD)
- `--tool <name>`: Which tool to use: "openspec" or "speckit" (default: "openspec")

## Core Workflow

### Phase 0: Prerequisites Check

1. **Verify OpenSpec is initialized**
   ```bash
   if [ ! -d "openspec" ]; then
     echo "❌ OpenSpec not initialized. Please run: npx openspec init"
     exit 1
   fi
   ```

2. **Read OpenSpec project context**
   - Read `openspec/project.md` to understand project conventions
   - Run `openspec list` to see existing changes
   - Run `openspec spec list --long` to see existing capabilities

3. **Check for conflicts**
   - Ensure change-id is unique
   - Check if similar changes already exist

### Phase 1: PRD Analysis and Understanding

1. **Load and Parse PRD**
   - Read the PRD file(s) from the specified path
   - If folder provided, search for PRD documents (*.md, *.pdf, *.docx, PRD.*, REQUIREMENTS.*)
   - Parse content to understand structure and requirements

2. **Analyze PRD Complexity**
   - Identify major features/capabilities (these become OpenSpec capabilities)
   - Extract user stories or use cases
   - Identify technical constraints and dependencies
   - Assess scope and complexity (small/medium/large/epic)
   - Detect cross-cutting concerns (auth, logging, testing, etc.)

3. **Generate Analysis Report**
   - Summary of the PRD scope
   - Identified capabilities with estimated complexity
   - Suggested breakdown strategy
   - Dependencies and sequencing recommendations

### Phase 2: Change Proposal Creation

4. **Determine Change ID**
   - If `--change-id` provided, use it
   - Otherwise, generate from PRD: `initial-<project-name>` or `add-<main-feature>`
   - Format: kebab-case, verb-led (add-, update-, initial-)
   - Ensure uniqueness

5. **Create Change Structure**
   ```bash
   mkdir -p openspec/changes/<change-id>/specs
   ```

6. **Write proposal.md**
   Create `openspec/changes/<change-id>/proposal.md` with:

   ```markdown
   ## Why
   [1-2 sentences: problem statement from PRD]

   ## What Changes
   - [List of capabilities being added]
   - [Key features and functionality]
   - [Note any cross-cutting concerns]

   ## Impact
   - Affected specs: [list capability names]
   - New capabilities: [count]
   - Dependencies: [external dependencies from PRD]
   ```

7. **Write tasks.md**
   Create `openspec/changes/<change-id>/tasks.md` with implementation checklist:

   ```markdown
   ## 1. Project Setup
   - [ ] 1.1 Initialize project structure
   - [ ] 1.2 Install dependencies
   - [ ] 1.3 Configure build tools

   ## 2. Core Implementation
   - [ ] 2.1 [Capability 1]: [key tasks]
   - [ ] 2.2 [Capability 2]: [key tasks]

   ## 3. Testing
   - [ ] 3.1 Unit tests
   - [ ] 3.2 Integration tests

   ## 4. Documentation
   - [ ] 4.1 API documentation
   - [ ] 4.2 User guides
   ```

   - Order by dependencies
   - Make tasks specific and actionable
   - Include testing and documentation tasks

8. **Create design.md (if needed)**
   Create `openspec/changes/<change-id>/design.md` ONLY if:
   - Cross-cutting architectural changes
   - New external dependencies
   - Complex data models or migrations
   - Security/performance considerations

   If created, use minimal structure:
   ```markdown
   ## Context
   [Technical background and constraints]

   ## Goals / Non-Goals
   - Goals: [what we're solving]
   - Non-Goals: [what's out of scope]

   ## Decisions
   - [Key technical decision and rationale]

   ## Risks / Trade-offs
   - [Risk] → [Mitigation]
   ```

### Phase 3: Capability Specs (Delta Format)

9. **Create Capability Specs**

   For each capability/feature identified, create:
   `openspec/changes/<change-id>/specs/<capability-name>/spec.md`

   **CRITICAL**: Use OpenSpec's delta format with proper requirement and scenario structure:

   ```markdown
   ## ADDED Requirements

   ### Requirement: [Clear requirement name]
   The system SHALL [specific behavior].

   #### Scenario: [Success case name]
   - **GIVEN** [initial state]
   - **WHEN** [action occurs]
   - **THEN** [expected outcome]

   #### Scenario: [Edge case name]
   - **GIVEN** [different state]
   - **WHEN** [action occurs]
   - **THEN** [expected outcome]

   ### Requirement: [Another requirement]
   The system SHALL [another behavior].

   #### Scenario: [Scenario name]
   - **WHEN** [condition]
   - **THEN** [result]
   ```

   **Key Rules**:
   - Every requirement MUST have at least one scenario
   - Scenarios use `#### Scenario:` format (4 hashtags)
   - Use GIVEN-WHEN-THEN or WHEN-THEN format
   - Use SHALL for normative requirements
   - Group related requirements under the same operation header

10. **Map PRD to Capabilities**

    Translate PRD structure to OpenSpec capabilities:

    - **PRD Features** → **OpenSpec Capabilities** (directory names)
    - **User Stories** → **Requirements** (### Requirement:)
    - **Acceptance Criteria** → **Scenarios** (#### Scenario:)
    - **Technical Details** → Requirement descriptions

    Example mapping:
    ```
    PRD Feature: "User Authentication"
    → openspec/changes/initial-app/specs/user-auth/spec.md
      → Requirement: User registration
        → Scenario: Successful registration
        → Scenario: Duplicate email error
      → Requirement: User login
        → Scenario: Valid credentials
        → Scenario: Invalid credentials
    ```

### Phase 4: Validation

11. **Run OpenSpec Validation**
    ```bash
    openspec validate <change-id> --strict
    ```

    - Fix any validation errors
    - Ensure all requirements have scenarios
    - Verify proper formatting

12. **Show Created Change**
    ```bash
    openspec show <change-id>
    ```

### Phase 5: Report and Next Steps

13. **Generate Completion Report**

    Present to user:
    ```markdown
    # ✅ OpenSpec Change Proposal Created

    ## Change ID: `<change-id>`

    ## Analysis Summary
    - **PRD Source**: <path>
    - **Capabilities Identified**: <count>
    - **Requirements Generated**: <count>
    - **Tasks Created**: <count>
    - **Complexity**: [Simple/Medium/Complex/Epic]

    ## Capabilities Breakdown
    1. **<capability-1>** - <complexity> - <requirement-count> requirements
       - <brief description>
    2. **<capability-2>** - <complexity> - <requirement-count> requirements
       - <brief description>

    ## Files Created
    ```
    openspec/changes/<change-id>/
    ├── proposal.md       # Change proposal
    ├── tasks.md          # Implementation checklist (<count> tasks)
    ├── design.md         # Technical decisions (if created)
    └── specs/
        ├── <capability-1>/
        │   └── spec.md   # <count> requirements
        ├── <capability-2>/
        │   └── spec.md   # <count> requirements
        └── ...
    ```

    ## Validation Status
    ✅ Passed strict validation

    ## Next Steps

    1. **Review the proposal**:
       ```bash
       openspec show <change-id>
       ```

    2. **View differences** (if modifying existing specs):
       ```bash
       openspec diff <change-id>
       ```

    3. **Read the AGENTS guide**:
       ```bash
       cat openspec/AGENTS.md
       ```

    4. **Start implementation**:
       - Review tasks in `openspec/changes/<change-id>/tasks.md`
       - Implement features following the specs
       - Check off tasks as you complete them

    5. **After deployment**:
       ```bash
       openspec archive <change-id> --yes
       ```

    ## OpenSpec Commands Reference

    ```bash
    openspec list                    # View all changes
    openspec show <change-id>        # View change details
    openspec diff <change-id>        # See spec differences
    openspec validate <change-id>    # Validate specs
    openspec archive <change-id>     # Archive after deployment
    ```
    ```

## Helper Methods

### PRD Parsing Strategies

**For Markdown PRDs:**
- Parse headers as capability boundaries
- Extract bullet points as requirements
- Look for user stories in format: "As a [user], I want [goal], so that [benefit]"

**For Large/Complex PRDs:**
- Use sections/chapters as capability boundaries
- Create hierarchical breakdown: Epic > Capability > Requirement > Scenario
- Generate separate spec files for each major capability

**For Folder of Documents:**
- Treat each document as a capability area
- Combine into cohesive proposal
- Cross-reference related requirements

### Capability Naming Guidelines

- Use kebab-case: `user-auth`, `payment-processing`
- Be specific but concise: `email-notifications` not `notifications`
- Verb-noun pattern when appropriate: `data-export`, `report-generation`
- Single purpose per capability
- If description needs "AND", consider splitting

### Requirement Writing Guidelines

- Start with "The system SHALL" for must-haves
- Use "The system SHOULD" for should-haves
- Be specific and measurable
- Include error cases and edge cases
- Reference external systems explicitly

### Scenario Writing Guidelines

- Use `#### Scenario:` format (4 hashtags) - REQUIRED
- Name scenarios descriptively: "Successful login", "Invalid credentials", etc.
- Use GIVEN-WHEN-THEN for complex flows
- Use WHEN-THEN for simple actions
- Cover success cases, error cases, and edge cases
- Make assertions specific and testable

### Quality Checks

Before finalizing, ensure:
- ✅ Every requirement from PRD is addressed
- ✅ All requirements have at least one scenario
- ✅ Scenarios use proper `#### Scenario:` format
- ✅ Tasks are specific and actionable
- ✅ Dependencies are clearly documented
- ✅ Technical considerations are noted
- ✅ Validation passes with `--strict` flag

## Error Handling

### If OpenSpec Not Initialized
```
❌ OpenSpec not initialized in this project.

Please run:
  npx openspec init

Then try the PRD breakdown again.
```

### If PRD is Unclear
1. Document assumptions made in proposal.md
2. Create `openspec/changes/<change-id>/questions.md`:
   ```markdown
   ## Open Questions

   1. [Question about unclear requirement]
   2. [Question about technical approach]
   3. [Question about priority]
   ```
3. Suggest user clarify before implementation

### If Validation Fails
- Show validation errors
- Explain how to fix (usually scenario formatting)
- Reference AGENTS.md for format requirements

## spec-kit Alternative

If `--tool speckit` is specified:

1. **Check if spec-kit is initialized**
   ```bash
   if [ ! -d ".specify" ]; then
     echo "Initializing spec-kit..."
     uvx --from git+https://github.com/github/spec-kit.git specify init <project-name>
   fi
   ```

2. **Use spec-kit workflow**
   - Suggest using `/speckit.constitution` to establish principles
   - Suggest using `/speckit.specify` to create specifications
   - Suggest using `/speckit.plan` for technical planning
   - Suggest using `/speckit.tasks` to generate tasks

   Note: spec-kit uses its own slash commands, so refer user to those.

## Example Output

```
✅ OpenSpec Change Proposal Created

Change ID: initial-reverse-planner

Analysis Summary:
- PRD Source: prd.md
- Capabilities Identified: 11
- Requirements Generated: 47
- Tasks Created: 28
- Complexity: Complex

Capabilities Breakdown:
1. reverse-planning-core - Medium - 8 requirements
2. template-management - Medium - 6 requirements
3. notification-system - Medium - 5 requirements
4. travel-time-integration - High - 7 requirements
... (7 more)

Files Created:
openspec/changes/initial-reverse-planner/
├── proposal.md
├── tasks.md
└── specs/
    ├── reverse-planning-core/spec.md
    ├── template-management/spec.md
    └── ... (9 more)

Validation: ✅ Passed strict validation

Next Steps:
  openspec show initial-reverse-planner
  openspec diff initial-reverse-planner
  Review tasks in tasks.md and start implementation
```

## Best Practices

1. **Start Simple**: Focus on MVP capabilities first
2. **One Capability, One Concern**: Don't mix authentication and payment processing
3. **Clear Naming**: Capability names should be immediately understandable
4. **Comprehensive Scenarios**: Cover success, failure, and edge cases
5. **Actionable Tasks**: Tasks should be specific enough to estimate time
6. **Validate Early**: Run validation immediately after creation

## Integration with OpenSpec Workflow

This command is the **first step** in the OpenSpec workflow:

1. **✅ Create Change** (this command) → `openspec/changes/<id>/`
2. **Implement** → Follow tasks.md checklist
3. **Archive** → Run `openspec archive <id>` after deployment

The created change proposal follows OpenSpec's three-stage workflow perfectly.
