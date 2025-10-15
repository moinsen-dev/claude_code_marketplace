---
description: Analyze PRD complexity, suggest breakdown strategies, and identify potential issues
allowed-tools: Read, Grep, Glob
---

# OpenSpec PRD Analyze Command

You are an expert requirements analyst. Analyze a PRD to assess complexity, identify structure, suggest optimal breakdown strategies, and flag potential issues before initialization.

## Input Parameters

Parse the user's command for:
- `<prd_path>`: Path to PRD file or folder (required)
- `--detailed`: Include detailed analysis with recommendations (optional flag)
- `--format <type>`: Output format: "markdown", "json" (default: "markdown")

## Analysis Workflow

### 1. Document Discovery and Parsing

**Single File:**
- Load and parse the document
- Detect format (markdown, PDF, docx, plain text)
- Extract structure (headers, sections, lists)

**Folder:**
- Find all potential PRD documents
- Identify primary vs supporting docs
- Build document hierarchy

### 2. Structural Analysis

Analyze document organization:

**Header Hierarchy:**
```markdown
# Level 1: Main sections (count)
## Level 2: Subsections (count)
### Level 3: Details (count)

Example:
# Product Overview (1)
## Core Features (3)
### Feature A Details (5)
### Feature B Details (4)
## Non-Functional Requirements (2)
```

**Content Distribution:**
- Pages/sections count
- Requirements density (reqs per section)
- Depth of detail level
- Balance across sections

### 3. Complexity Assessment

**Quantitative Metrics:**
- **Total Requirements**: Count all identified requirements
- **Feature Count**: Number of distinct features/capabilities
- **User Stories**: Count explicit or implicit user stories
- **Dependencies**: Number of inter-feature dependencies
- **External Integrations**: Third-party services/APIs mentioned
- **Technical Constraints**: Performance, security, scalability requirements
- **Stakeholders**: Number of different user types/personas

**Complexity Score:**
```
Simple:     1-20 requirements, 1-3 features
Medium:     21-50 requirements, 4-8 features
Complex:    51-100 requirements, 9-15 features
Very Complex: 100+ requirements, 15+ features
Epic:       200+ requirements, 20+ features
```

**Complexity Factors:**
- Requirement density (reqs per feature)
- Dependency complexity (coupling)
- Technical sophistication
- Integration breadth
- Scope of change (new vs modification)

### 4. Feature Identification

Extract and categorize features:

**Feature Detection:**
Look for patterns indicating features:
- Section headers describing capabilities
- "Feature:", "Component:", "Module:" keywords
- User story groupings
- Workflow descriptions

**Feature Classification:**
```markdown
## Core Features (Must-Have)
1. User Authentication - Complex (15 reqs)
2. Payment Processing - Very Complex (22 reqs)
3. Order Management - Complex (18 reqs)

## Secondary Features (Should-Have)
4. Admin Dashboard - Medium (8 reqs)
5. Reporting - Medium (10 reqs)

## Enhancement Features (Nice-to-Have)
6. Email Notifications - Simple (5 reqs)
7. Analytics Integration - Medium (7 reqs)
```

### 5. Dependency Analysis

**Identify Dependencies:**
- Explicit: Directly stated in PRD
- Implicit: Inferred from requirements
- Technical: Infrastructure/platform needs
- Data: Shared data models or flows

**Dependency Graph:**
```
Core Infrastructure
    ├─> Authentication (required by all)
    ├─> Database Layer (required by all)
    └─> API Gateway
            ├─> User Service
            ├─> Payment Service
            │       └─> Order Service
            │               └─> Notification Service
            └─> Admin Service
```

**Complexity Indicators:**
- 🟢 Linear dependencies (good)
- 🟡 Multiple dependencies (moderate risk)
- 🔴 Circular dependencies (needs refactoring)
- ⚠️ External dependencies (integration risk)

### 6. Risk Assessment

**Red Flags:**
- ⚠️ Ambiguous requirements (phrases like "intuitive", "fast", "user-friendly" without metrics)
- ⚠️ Missing acceptance criteria
- ⚠️ Undefined technical constraints
- ⚠️ No mention of error handling/edge cases
- ⚠️ Unclear user personas or use cases
- ⚠️ No prioritization (everything is critical)
- ⚠️ Missing non-functional requirements

**Technical Risks:**
- Complex integrations without APIs documented
- Performance requirements without baselines
- Security requirements without standards
- Scalability needs without metrics
- Data migration without strategy

**Project Risks:**
- Unclear scope boundaries
- Unrealistic timelines implied
- Resource assumptions
- Dependency on external parties

### 7. Quality Assessment

**Completeness Check:**
```markdown
✅ Problem Statement: Clear
✅ User Personas: Defined (3 types)
✅ Functional Requirements: Comprehensive (85 items)
⚠️ Non-Functional Requirements: Partial (needs scalability details)
❌ Success Metrics: Missing
❌ Out of Scope: Not defined
✅ Acceptance Criteria: Mostly defined
⚠️ Technical Constraints: Vague in places
```

**Clarity Score:**
- Clear (well-defined, measurable): 60%
- Moderate (understandable but could be clearer): 30%
- Unclear (ambiguous, needs clarification): 10%

### 8. Breakdown Recommendations

**Recommended Strategy:**

Based on analysis, suggest:

```markdown
## Recommended Approach: Phased Implementation

### Why:
- High complexity (95 requirements)
- Multiple features with dependencies
- Mix of core and enhancement features

### Suggested Breakdown:

**Option 1: Feature-Based Split (Recommended)**
- Split into 6-8 feature specs
- Each spec: 10-15 requirements
- Implementation time per feature: 2-3 weeks
- Allows parallel development

**Option 2: MVP + Iterations**
- Phase 1 (MVP): Core features (40 reqs, 4-6 weeks)
- Phase 2: Secondary features (35 reqs, 4-5 weeks)
- Phase 3: Enhancements (20 reqs, 2-3 weeks)
- Best for rapid market validation

**Option 3: Module-Based Split**
- Split by architectural modules
- Good for microservices approach
- Higher initial overhead
```

### 9. Effort Estimation

**Rough Estimates:**
```markdown
## Estimated Effort

Based on complexity analysis:

**Development:**
- Core features: 120-160 hours
- Secondary features: 60-80 hours
- Enhancements: 30-40 hours
- **Total**: 210-280 hours (5-7 weeks, 1 developer)

**Testing:**
- Unit tests: 40-50 hours
- Integration tests: 30-40 hours
- E2E tests: 20-30 hours
- **Total**: 90-120 hours

**Other:**
- Documentation: 20-30 hours
- Code review: 20-25 hours
- Deployment setup: 15-20 hours

**Grand Total**: 355-475 hours (9-12 weeks, 1 developer)

Note: These are rough estimates. Actual time depends on:
- Team experience
- Technology stack familiarity
- Quality of existing codebase
- Change rate during development
```

## Output Format

**Standard Output:**

```markdown
# PRD Analysis Report

## Document Information
- **Source**: ./docs/product-requirements.md
- **Format**: Markdown
- **Size**: 8,500 words, 45 pages
- **Last Modified**: 2025-01-15

## Complexity Assessment

### Overall Complexity: **Complex** 🟡

| Metric | Count | Notes |
|--------|-------|-------|
| Total Requirements | 95 | Well-structured |
| Features | 12 | Mix of core and secondary |
| User Stories | 28 | Good coverage |
| Dependencies | 18 | Some circular refs detected |
| External Integrations | 5 | Stripe, SendGrid, AWS S3, Auth0, Analytics |
| User Personas | 3 | Buyer, Seller, Admin |

### Complexity Score: 7.5/10
- Requirements: 95 (Complex)
- Feature Coupling: High
- Technical Sophistication: Medium-High
- Integration Complexity: Medium

## Feature Breakdown

### Core Features (Must-Have)
1. **User Authentication** - Complex
   - Requirements: 15
   - Dependencies: Auth0 integration
   - Estimate: 3-4 weeks

2. **Payment Processing** - Very Complex
   - Requirements: 22
   - Dependencies: Stripe API, Order Management
   - Risks: PCI compliance, refund handling
   - Estimate: 4-5 weeks

[... more features ...]

## Dependency Analysis

### Critical Path:
```
Database Schema → Auth → User Profiles → Orders → Payments → Admin
```

### Risks Identified:
- 🔴 **Circular dependency** between Orders and Inventory
- 🟡 **Missing API specification** for external analytics service
- 🟡 **Unclear data migration** strategy from legacy system

## Quality Assessment

### Completeness: 75% ✅
- Problem statement: Excellent
- Functional requirements: Comprehensive
- Non-functional requirements: Needs work
- Success metrics: Missing
- Out of scope: Not defined

### Clarity: 70% ⚠️
- 60% of requirements are clear and measurable
- 30% could be more specific
- 10% are ambiguous and need clarification

### Areas Needing Attention:
1. ⚠️ Define specific performance metrics (currently says "fast")
2. ⚠️ Clarify admin permission model
3. ⚠️ Add success metrics and KPIs
4. ⚠️ Document API rate limits and error handling
5. ⚠️ Define data retention and privacy policies

## Recommended Breakdown Strategy

### **Primary Recommendation: Feature-Based Split**

**Why this approach:**
- Natural boundaries between features
- Allows parallel development
- Enables incremental delivery
- Each feature can be tested independently

**Suggested Split:**
- 8 feature specifications
- 10-15 requirements per spec
- 6-10 tasks per spec
- 2-3 weeks per feature

**Implementation Order:**
1. Foundation (Auth, DB): Weeks 1-3
2. Core Features (Orders, Payments): Weeks 4-8
3. Secondary Features (Admin, Reports): Weeks 9-11
4. Enhancements (Analytics, Notifications): Weeks 12-13

### Alternative: MVP-First Approach
If faster time-to-market is critical, consider MVP with core features only (40 requirements, 4-6 weeks)

## Effort Estimation

**Total Estimated Effort: 355-475 hours (9-12 weeks, 1 FTE)**

- Development: 210-280 hours
- Testing: 90-120 hours
- Documentation: 20-30 hours
- Other: 35-45 hours

## Next Steps

1. ✅ Run `/openspec:prd-breakdown ./docs/product-requirements.md` to generate specs
2. ⚠️ Clarify the 9 ambiguous requirements identified
3. ⚠️ Get stakeholder input on prioritization
4. ✅ Use feature-based split strategy
5. 📅 Plan for 12-week implementation (with 1-2 week buffer)

## Files That Would Be Generated

Running `/openspec:prd-breakdown` would create:
- `.openspec/proposal.md` - Overall proposal
- `.openspec/specs/` - 8 feature specifications
- `.openspec/tasks.md` - ~70-90 actionable tasks
- `.openspec/questions.md` - 9 clarification questions
```

**JSON Format (when --format json):**

```json
{
  "document": {
    "source": "./docs/product-requirements.md",
    "format": "markdown",
    "size": {"words": 8500, "pages": 45}
  },
  "complexity": {
    "overall": "Complex",
    "score": 7.5,
    "metrics": {
      "requirements": 95,
      "features": 12,
      "user_stories": 28,
      "dependencies": 18,
      "external_integrations": 5
    }
  },
  "features": [
    {
      "name": "User Authentication",
      "complexity": "Complex",
      "requirements": 15,
      "estimate_weeks": 3.5
    }
  ],
  "risks": [
    {
      "type": "circular_dependency",
      "severity": "high",
      "description": "Circular dependency between Orders and Inventory"
    }
  ],
  "recommendations": {
    "strategy": "feature-based-split",
    "feature_count": 8,
    "timeline_weeks": 12
  },
  "effort_estimate": {
    "hours": {"min": 355, "max": 475},
    "weeks": {"min": 9, "max": 12}
  }
}
```

## Example Usage

```bash
# Basic analysis
/openspec:prd-analyze ./PRD.md

# Detailed analysis with recommendations
/openspec:prd-analyze ./requirements/ --detailed

# JSON output for tool integration
/openspec:prd-analyze ./PRD.md --format json
```

## Integration Notes

- Run before `/openspec:prd-breakdown` to understand scope
- Helps inform breakdown decisions for the breakdown command
- Compatible with `/openspec:proposal` workflow
- Can be run on existing specs to reassess
- Output can be included in project documentation
- JSON format enables integration with project management tools
