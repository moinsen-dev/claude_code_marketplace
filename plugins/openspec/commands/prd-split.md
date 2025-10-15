---
description: Split a large PRD into smaller, manageable feature specifications
allowed-tools: Read, Write, Grep, Glob
---

# OpenSpec PRD Split Command

You are an expert at breaking down complex product requirements into manageable, focused specifications. Split a large PRD into smaller feature specs that are independently understandable and implementable.

## Input Parameters

Parse the user's command for:
- `<prd_path>`: Path to PRD file to split (required)
- `--strategy <type>`: Splitting strategy: "features", "epics", "modules", "auto" (default: "auto")
- `--output <path>`: Output directory for split specs (default: "./.openspec/specs")
- `--min-size <number>`: Minimum tasks per spec (default: 3)
- `--max-size <number>`: Maximum tasks per spec (default: 15)

## Splitting Workflow

### 1. Load and Analyze PRD

Read the PRD and analyze its structure:
- Identify natural boundaries (sections, chapters, features)
- Count total requirements and complexity
- Detect logical groupings
- Map dependencies between sections

### 2. Choose Splitting Strategy

**Auto Strategy (default):**
- Analyze PRD structure automatically
- Use headers/sections as primary boundaries
- Group related functionality
- Balance spec sizes

**Features Strategy:**
- Split by feature sets (e.g., "User Authentication", "Payment Processing")
- Each spec is a complete feature
- Good for feature-based development

**Epics Strategy:**
- Split into large initiatives/epics first
- Then break epics into features
- Creates hierarchical structure
- Good for very large PRDs

**Modules Strategy:**
- Split by technical modules/components
- Each spec covers one architectural component
- Good for modular architectures

### 3. Generate Split Specifications

For each split section, create a focused spec file:

**File naming convention:**
```
.openspec/specs/
├── 01-user-authentication.md
├── 02-profile-management.md
├── 03-payment-processing.md
└── 04-admin-dashboard.md
```

**Each spec file structure:**
```markdown
# Feature: [Name]

## Overview
[What this feature does and why it matters]

## Original PRD Reference
- Source: [PRD file path]
- Sections: [Which sections from PRD this covers]

## Requirements
[Extracted requirements from PRD specific to this feature]

### Functional Requirements
- Requirement 1
- Requirement 2

### Non-Functional Requirements
- Performance expectations
- Security requirements
- Scalability needs

## User Stories
[Converted or extracted user stories]

## Acceptance Criteria
[Specific, testable criteria]

## Dependencies
- **Depends on**: [Other specs that must be completed first]
- **Depended by**: [Specs that need this one]
- **External**: [Third-party services, APIs]

## Technical Considerations
[Key technical notes, constraints, or suggestions]

## Estimated Complexity
- Size: [Small/Medium/Large]
- Tasks: [Estimated number]
- Risk Level: [Low/Medium/High]

## Open Questions
[Ambiguities or areas needing clarification]
```

### 4. Maintain Traceability

Create a mapping file showing how PRD sections map to specs:

**`.openspec/traceability.md`:**
```markdown
# PRD to Spec Traceability

## Source PRD: [path]

### Mapping

#### PRD Section 1: User Management
→ Specs: `01-user-authentication.md`, `02-profile-management.md`
→ Coverage: Complete

#### PRD Section 2: Payments
→ Specs: `03-payment-processing.md`
→ Coverage: Complete
→ Notes: Split from original section due to complexity

### Coverage Analysis
- Total PRD Requirements: 45
- Requirements Covered: 45
- Coverage: 100%
- Uncovered Requirements: None
```

### 5. Generate Cross-Reference Index

Create **`.openspec/index.md`**:
```markdown
# Specification Index

## Quick Navigation

### By Implementation Phase
**Phase 1: Foundation**
- 01-user-authentication.md (8 tasks)
- 02-database-schema.md (5 tasks)

**Phase 2: Core Features**
- 03-payment-processing.md (12 tasks)
- 04-order-management.md (10 tasks)

**Phase 3: Enhancement**
- 05-admin-dashboard.md (7 tasks)

### By Complexity
**High Complexity (>10 tasks)**
- 03-payment-processing.md
- 04-order-management.md

**Medium Complexity (5-10 tasks)**
- 01-user-authentication.md
- 05-admin-dashboard.md

**Low Complexity (<5 tasks)**
- 02-database-schema.md

### Dependency Graph
```
database-schema
    └─> user-authentication
            ├─> profile-management
            └─> order-management
                    └─> payment-processing
                            └─> admin-dashboard
```
```

## Quality Checks

Ensure each split spec:
- ✅ Is independently understandable
- ✅ Has clear scope and boundaries
- ✅ Contains 3-15 tasks (configurable)
- ✅ Has documented dependencies
- ✅ Includes acceptance criteria
- ✅ References source PRD sections
- ✅ Has no ambiguous requirements
- ✅ Is implementable without constant PRD reference

## Smart Splitting Rules

### Do Split When:
- A section has >15 tasks
- Multiple unrelated features are grouped
- Different stakeholders own different parts
- Can be independently deployed/tested
- Has clear technical boundaries

### Don't Split When:
- Features are tightly coupled
- Would create excessive dependencies
- Results in specs <3 tasks
- Breaks logical workflow
- Creates artificial boundaries

### Handle Cross-Cutting Concerns:
For concerns that span multiple specs (e.g., logging, auth, monitoring):
- Create a dedicated "cross-cutting" spec
- Reference it in dependent specs
- Implement early in the project

## Advanced Features

### Dependency Optimization
- Identify circular dependencies
- Suggest refactoring to break cycles
- Recommend implementation order
- Flag high-coupling areas

### Balance Analysis
- Ensure even distribution of complexity
- Avoid one huge spec and many tiny ones
- Suggest combining tiny specs
- Recommend further splitting of large specs

### Context Preservation
- Include relevant PRD context in each spec
- Reference related sections
- Maintain business rationale
- Keep user perspective

## Output Format

Present results as:

```markdown
# PRD Split Complete

## Summary
- **Source PRD**: ./docs/product-requirements.md
- **Specs Generated**: 6
- **Total Tasks**: 52 (avg 8.7 per spec)
- **Output Location**: ./.openspec/specs/

## Generated Specs

### 01-user-authentication.md
- **Complexity**: Medium
- **Tasks**: 8
- **Dependencies**: database-schema
- **PRD Sections**: 2.1, 2.2, 2.3

### 02-profile-management.md
- **Complexity**: Low
- **Tasks**: 5
- **Dependencies**: user-authentication
- **PRD Sections**: 2.4, 2.5

[... more specs ...]

## Quality Metrics
- ✅ All PRD requirements covered
- ✅ No orphaned requirements
- ✅ Dependency graph is acyclic
- ✅ Balanced complexity distribution

## Files Created
- `.openspec/specs/` - 6 specification files
- `.openspec/traceability.md` - PRD mapping
- `.openspec/index.md` - Navigation index

## Next Steps
1. Review generated specs for accuracy
2. Refine dependencies if needed
3. Use `/openspec:spec-review` to check completeness
4. Begin implementation with Phase 1 specs
```

## Example Usage

```bash
# Auto-split PRD
/openspec:prd-split ./PRD.md

# Split into feature-based specs
/openspec:prd-split ./requirements.md --strategy features

# Custom sizing constraints
/openspec:prd-split ./PRD.md --min-size 5 --max-size 10

# Custom output location
/openspec:prd-split ./docs/PRD.md --output ./project-specs
```

## Integration Notes

- Works standalone or after `/openspec:prd-breakdown`
- Can be run multiple times to refine splits
- Preserves existing spec customizations
- Compatible with `/openspec:proposal` workflow
- Use `/openspec:spec-review` after splitting to validate quality
- Output format is markdown for easy editing and version control
