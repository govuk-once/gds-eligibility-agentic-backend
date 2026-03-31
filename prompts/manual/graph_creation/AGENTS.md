# AGENTS.md

**Guide for AI agents working in the GDS Eligibility Graph Creation directory**

---

## Overview

This directory contains **machine-readable JSON specifications** of UK government service eligibility criteria. These specifications model complex eligibility decision trees in a deterministic, visualizable format using a standardized JSON Schema.

**Primary goal**: Create and maintain JSON decision trees that faithfully represent Gov.UK eligibility rules for various UK government services (visas, benefits, etc.).

---

## Project Structure

### Core Files

```
prompts/manual/graph_creation/
├── README.md                      # Main documentation - comprehensive guide
├── QUICK_START.md                 # Quick reference for getting started
├── INDEX.md                       # Project index and version history
├── Toby.Notes.md                  # Developer notes and TODOs
├── simplified_flow_diagram.md     # Mermaid flowchart examples
│
├── schemas/
│   ├── eligibility-schema.json    # JSON Schema definition (v1.1)
│   └── SCHEMA_DOCUMENTATION.md    # Schema reference guide
│
├── specifications/
│   ├── skilled_worker_visa/
│   │   ├── skilled_worker_visa_eligibility.json   # Main specification (v1.2)
│   │   ├── PHASE_1_IMPLEMENTATION_COMPLETE.md
│   │   ├── TEST_CASE_ANALYSIS.md
│   │   ├── VERSION_1.1_RELEASE_NOTES.md
│   │   └── VERSION_1.2_RELEASE_NOTES.md
│   │
│   ├── child_benefit/
│   │   ├── child_benefit_eligibility.json         # Main specification (v1.2)
│   │   ├── CHILD_BENEFIT_README.md
│   │   ├── CHILD_BENEFIT_TEST_ANALYSIS.md
│   │   ├── CHILD_BENEFIT_VERSION_1.1_RELEASE_NOTES.md
│   │   └── CHILD_BENEFIT_VERSION_1.2_RELEASE_NOTES.md
│   │
│   ├── SCHEMA_VALIDATION_REPORT.md
│   └── ORPHAN_NODE_CLEANUP_REPORT.md
│
├── ancillary_functionality/
│   ├── validate_specifications.py      # Validate JSON against schema
│   ├── check_orphan_nodes.py          # Detect orphan nodes
│   ├── validate_and_visualize.py      # Validation + visualization
│   ├── visualization_guide.md         # Guide for creating visualizations
│   ├── child_benefit_eligibility      # GraphViz DOT file
│   ├── child_benefit_eligibility.png  # Generated visualization
│   ├── skilled_worker_visa_eligibility
│   └── skilled_worker_visa_eligibility.png
│
├── summaries/
│   ├── IMPLEMENTATION_SUMMARY.md
│   ├── ORPHAN_NODES_SUMMARY.md
│   ├── README_UPDATE_SUMMARY.md
│   ├── TASK_COMPLETION_SUMMARY.md
│   └── TEST_CASE_SUMMARY.md
│
└── task_prompts/
    ├── child_benefit.v1.md
    ├── child_benefit.v2.md
    ├── child_benefit.v3.md
    ├── rehome-orphan-nodes.v1.md
    ├── schema-fix.v1.md
    ├── skilled_worker_visa.v1.md
    └── skilled_worker_visa.v2.md
```

---

## Essential Commands

### Validation

```bash
# Validate all specifications against schema
python3 ancillary_functionality/validate_specifications.py

# Check for orphan nodes and dangling references
python3 ancillary_functionality/check_orphan_nodes.py

# Validate and optionally generate visualization
python3 ancillary_functionality/validate_and_visualize.py
```

### JSON Operations

```bash
# View decision tree root
jq '.decision_tree.root' specifications/skilled_worker_visa/skilled_worker_visa_eligibility.json

# List all node IDs
jq '.decision_tree.nodes | keys' specifications/child_benefit/child_benefit_eligibility.json

# Count nodes by type
jq '[.decision_tree.nodes[].type] | group_by(.) | map({type: .[0], count: length})' specifications/child_benefit/child_benefit_eligibility.json

# View all outcome nodes
jq '.decision_tree.nodes | to_entries[] | select(.value.type == "outcome")' specifications/skilled_worker_visa/skilled_worker_visa_eligibility.json

# Check for a specific node
jq '.decision_tree.nodes.ELIGIBLE' specifications/child_benefit/child_benefit_eligibility.json
```

---

## JSON Schema Overview

### Schema Version: v1.1 (Current)

**Location**: `schemas/eligibility-schema.json`

#### Top-Level Required Fields

Every eligibility specification must have:

- `version` - Semantic version (e.g., "1.2")
- `last_updated` - ISO date (YYYY-MM-DD)
- `source` - Official Gov.UK URL
- `description` - Human-readable description
- `decision_tree` - Contains root and all nodes
- `constants` - Fixed values (thresholds, fees, etc.)

#### Optional Top-Level Fields

- `$schema` - Reference to eligibility-schema.json
- `validation_rules` - Business logic rules
- `external_references` - URLs to external data

### Node Types (10 types)

1. **`start`** - Entry point (root node only)
   - Required: `id`, `type`, `description`, `next`

2. **`boolean_question`** - Yes/No decisions
   - Required: `id`, `type`, `question`, `outcomes` (must have `yes` and `no`)
   - Optional: `help_text`, `reference`

3. **`multi_path_check`** - Multiple alternative paths (OR logic)
   - Required: `id`, `type`, `question`, `paths[]`, `outcomes`
   - Optional: `evaluation_logic`, `help_text`, `reference`

4. **`salary_check`** - Salary threshold validations
   - Required: `id`, `type`, `question`, `criteria`, `outcomes`

5. **`financial_check`** - Financial requirement validations
   - Required: `id`, `type`, `question`, `criteria`, `outcomes`

6. **`occupation_check`** - Occupation skill level checks
   - Required: `id`, `type`, `question`, `outcomes`

7. **`conditional_check`** - Questions that may not apply to all applicants
   - Required: `id`, `type`, `question`, `outcomes`

8. **`complex_criteria`** - Multi-factor criteria evaluation
   - Required: `id`, `type`, `question`, `criteria`, `outcomes`
   - Optional: `disclaimer`, `common_red_flags`

9. **`routing`** - Non-question routing logic
   - Required: `id`, `type`, `description`, `outcomes`
   - Optional: `routing_logic`

10. **`outcome`** - Terminal nodes with eligibility results
    - Required: `id`, `type`, `result` (ELIGIBLE, INELIGIBLE, or DEFERRED)
    - **ELIGIBLE**: requires `description`, `next_steps`
    - **INELIGIBLE**: requires `reason`, `guidance`
    - **DEFERRED**: requires `reason`, `guidance`; optional `hmrc_decision_criteria`, `required_evidence`

### Outcome Types

- **ELIGIBLE** - Applicant qualifies for the service
- **INELIGIBLE** - Applicant does not qualify
- **DEFERRED** - External decision required (e.g., HMRC arbitration)

---

## Code Conventions

### JSON Structure Patterns

1. **Node IDs**:
   - Use snake_case: `check_uk_residency`, `has_qualifying_child`
   - Outcome nodes: `ELIGIBLE`, `INELIGIBLE_<reason>`, `DEFERRED_<reason>`
   - Descriptive and unique

2. **Questions**:
   - Clear, complete sentences
   - Start with "Does", "Is", "Has", "Can" for boolean questions
   - Include context when needed

3. **References**:
   - Always use official Gov.UK URLs
   - Include `reference` field for nodes that reference official guidance
   - Store frequently-changing data URLs in `external_references`

4. **Help Text**:
   - Provide when question needs clarification
   - Keep concise but informative
   - Reference specific Gov.UK sections when applicable

5. **Outcomes**:
   - Use descriptive keys: `yes`/`no`, `meets_requirement`/`does_not_meet`, `eligible_via_any_path`/`not_eligible`
   - Ensure all paths lead to an outcome node (no dead ends)
   - Outcome nodes are terminal (no outgoing edges)

### Python Script Conventions

1. **Imports**: Standard library imports first, then third-party
2. **Encoding**: UTF-8 with shebang `#!/usr/bin/env python3`
3. **Functions**: Docstrings for all public functions
4. **Error Handling**: Try-except blocks with informative error messages
5. **Output**: Use ✓/✅ for success, ❌ for errors, ⚠️ for warnings, 📊 for statistics
6. **Returns**: Exit codes: 0 for success, 1 for errors

---

## Validation Requirements

### Before Committing Changes

**ALWAYS run validation tools before committing**:

```bash
# 1. Validate structure and schema conformance
python3 ancillary_functionality/validate_specifications.py

# 2. Check for orphan nodes
python3 ancillary_functionality/check_orphan_nodes.py

# 3. Verify JSON syntax
python3 -m json.tool specifications/child_benefit/child_benefit_eligibility.json > /dev/null
```

### Common Validation Errors

1. **Orphan Nodes**: Nodes defined but never referenced
   - Solution: Either connect them to the tree or remove them

2. **Dangling References**: References to non-existent nodes
   - Solution: Fix typos in node IDs or create missing nodes

3. **Missing Required Fields**: Node missing `id`, `type`, `question`, etc.
   - Solution: Add required fields per node type

4. **Outcome Node Issues**:
   - ELIGIBLE missing `next_steps`
   - INELIGIBLE missing `reason` or `guidance`
   - DEFERRED missing `reason` or `guidance`

5. **Boolean Question Issues**: Missing `yes` or `no` in outcomes
   - Solution: Add both outcome paths

---

## Making Changes

### Adding a New Node

1. **Choose the correct node type** (see Node Types above)
2. **Add the node to `nodes` object** with all required fields
3. **Update parent node** to reference the new node ID in its `outcomes`
4. **Run validation** to ensure no orphan nodes
5. **Test the path** by tracing through the decision tree

Example:
```json
"check_new_requirement": {
  "id": "check_new_requirement",
  "type": "boolean_question",
  "question": "Does the applicant meet the new requirement?",
  "help_text": "Explanation of the requirement",
  "reference": "https://www.gov.uk/...",
  "outcomes": {
    "yes": "next_node_id",
    "no": "INELIGIBLE_new_requirement_not_met"
  }
}
```

### Modifying an Existing Node

1. **Read README.md first** to understand current structure
2. **View the node** in context using `jq`
3. **Make targeted changes** to specific fields
4. **Update `last_updated`** at top level
5. **Run validation** to ensure changes don't break tree
6. **Document changes** in version notes if significant

### Adding a New Specification

1. **Copy an existing specification** as a template
2. **Update all metadata**: version, last_updated, source, description
3. **Build decision tree** following schema
4. **Define constants** (thresholds, fees, etc.)
5. **Add validation rules** if needed
6. **Add external references** for dynamic data
7. **Validate thoroughly** with all tools
8. **Create supporting documentation**:
   - README in specification directory
   - Release notes
   - Test analysis document
9. **Update `validate_specifications.py`** to include new spec in `spec_files` list

---

## Version Control

### Semantic Versioning

- **Major (X.0)**: Breaking changes to structure or schema
- **Minor (X.Y)**: New features, backward compatible additions
- **Patch (X.Y.Z)**: Bug fixes, clarifications (rarely used here)

### When to Increment Version

- **Minor version**: Add new nodes, enhance existing paths, add outcome types
- **Major version**: Change schema structure, rename node types, restructure tree

### Version Update Checklist

When updating a specification:

1. Update `version` field in JSON
2. Update `last_updated` field (YYYY-MM-DD)
3. Create/update release notes document
4. Document changes in version control commit message
5. Update README.md if structural changes
6. Update test analysis if coverage changes

---

## Testing Against Test Cases

### Test Case Files

Test cases are located in parent directories:
- `../test_cases/child_benefit.md`
- `../test_cases/skilled_worker_visa.md`

### Coverage Analysis Process

1. **Read test scenarios** from test case files
2. **Trace each scenario** through the decision tree
3. **Document coverage** in TEST_CASE_ANALYSIS.md
4. **Identify gaps** where specification doesn't cover scenario
5. **Enhance specification** to cover gaps
6. **Re-validate** to ensure changes don't break existing paths

### Coverage Metrics

Current coverage:
- **Skilled Worker Visa**: 90%+ (46 of 51 scenarios fully covered)
- **Child Benefit**: 98% (49 of 50 scenarios fully covered)

---

## Important Gotchas

### 1. Node References Must Be Exact

- Node IDs are case-sensitive
- Typos in `outcomes` create dangling references
- Always run `check_orphan_nodes.py` after changes

### 2. Outcome Nodes Are Terminal

- Outcome nodes (type: "outcome") **cannot** have outgoing edges
- They must not have a `next` field or `outcomes` field
- All paths must end at an outcome node

### 3. Root Node Is Special

- Root node lives in `decision_tree.root`, not in `nodes`
- Root node must have `type: "start"` and a `next` field
- Root node cannot be referenced by other nodes

### 4. Multi-Path Check Logic

- Multi-path checks use **OR logic** (any path satisfies)
- Each path needs clear `id` and `description`
- Outcome typically has `eligible_via_any_path` and `not_eligible`

### 5. Constants vs. Validation Rules

- **Constants**: Fixed values (£41,700, 28 days, etc.)
- **Validation Rules**: Logic for calculations (salary must be HIGHER of X or Y)
- Keep them separate in the JSON structure

### 6. External References

- **DO**: Store frequently-changing data URLs (occupation lists, going rates)
- **DO**: Reference official Gov.UK pages
- **DON'T**: Embed large lists that change often
- **DON'T**: Use unofficial sources

### 7. DEFERRED Outcome Type

- Added in schema v1.1
- Used when external decision-maker must arbitrate (e.g., HMRC)
- Requires `reason` and `guidance`
- Optional fields: `hmrc_decision_criteria`, `required_evidence`
- See Child Benefit specification for example

### 8. Help Text vs. Disclaimer

- **help_text**: Clarifies the question for the user
- **disclaimer**: Used in `complex_criteria` nodes to indicate subjective assessment
- Both are optional but help with comprehension

---

## Common Tasks

### Task: Add a New Eligibility Route

**Example**: Adding a new salary route to Skilled Worker Visa

1. Identify parent node (e.g., `check_reduced_salary_eligibility`)
2. Add new path to `paths` array:
   ```json
   {
     "id": "new_route_id",
     "description": "Clear description of route",
     "salary_minimum": 30000,
     "salary_percentage": "80% of going rate"
   }
   ```
3. If outcome differs, add new outcome node
4. Validate structure
5. Update constants if new thresholds introduced
6. Document in release notes

### Task: Fix an Orphan Node

**When `check_orphan_nodes.py` reports orphans**:

1. Read the orphan node context (type, question/description)
2. Determine if node should be connected or removed:
   - **Connect**: Find parent node and add reference in `outcomes`
   - **Remove**: Delete node from `nodes` object
3. Re-run validation to confirm fix

### Task: Update Gov.UK Reference

**When Gov.UK URLs change**:

1. Find all nodes with old URL in `reference` field:
   ```bash
   jq '.decision_tree.nodes[] | select(.reference == "old-url") | .id' spec.json
   ```
2. Update `reference` field to new URL
3. Check `external_references` object for same URL
4. Update `last_updated` date
5. Validate

### Task: Create Visualization

**Generate graph diagram**:

1. Ensure graphviz Python library is installed: `pip install graphviz`
2. Run: `python3 ancillary_functionality/validate_and_visualize.py`
3. Output: `<spec_name>_eligibility.png`
4. For custom visualizations, see `visualization_guide.md`

---

## Key Principles

### 1. Faithfulness to Official Guidance

- **Always** base specifications on official Gov.UK pages
- **Never** invent or assume rules
- **Include** references to authoritative sources
- **Document** any interpretation decisions

### 2. Determinism

- Given same inputs, always produce same output
- All conditional logic must be explicit
- No ambiguous or subjective language (except in `complex_criteria` with disclaimers)
- Clear Boolean conditions

### 3. Completeness

- Cover all paths from start to outcome
- No dead ends (all paths must reach outcome node)
- Handle edge cases documented in Gov.UK guidance
- Achieve high test scenario coverage (>90%)

### 4. Maintainability

- Separate static logic from dynamic data
- Use meaningful node IDs
- Document complex logic in node fields
- Create release notes for all versions
- Keep validation tools up to date

### 5. Human Comprehensibility

- Use natural language in questions
- Provide help text when needed
- Structure can be visualized as flowchart
- Documentation is comprehensive

---

## Documentation Standards

### README Files

- **Main README.md**: Comprehensive guide to entire project
- **Specification README**: Details for specific benefit/service
- **QUICK_START.md**: Fast entry point for new users

### Release Notes

**Required sections**:
- Version and date
- Summary of changes
- New nodes added
- Modified nodes
- Coverage improvements
- Breaking changes (if any)

**Format**: `VERSION_X.Y_RELEASE_NOTES.md`

### Test Analysis Documents

**Structure**:
- Test case ID and description
- Path through decision tree
- Coverage status (Full, Partial, Not Covered)
- Gaps identified
- Recommendations

**Format**: `TEST_CASE_ANALYSIS.md` or `<SERVICE>_TEST_ANALYSIS.md`

---

## Useful References

### External Documentation

- **Gov.UK Style Guide**: https://www.gov.uk/guidance/style-guide
- **JSON Schema Documentation**: https://json-schema.org/understanding-json-schema/
- **Open Government Licence v3.0**: https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/

### Internal Documentation

Must-read files before making changes:
1. **README.md** - Comprehensive overview
2. **SCHEMA_DOCUMENTATION.md** - Schema reference
3. **Specification README** - Service-specific details
4. **Latest VERSION_X.Y_RELEASE_NOTES.md** - Recent changes

### Tools Documentation

- **jq Manual**: https://stedolan.github.io/jq/manual/
- **GraphViz**: https://graphviz.org/documentation/
- **Python JSON**: https://docs.python.org/3/library/json.html

---

## Current State

### Active Specifications

1. **Skilled Worker Visa** (v1.2, 2026-03-03)
   - 32 nodes, 90%+ test coverage
   - 13 INELIGIBLE outcomes, 1 ELIGIBLE outcome

2. **Child Benefit** (v1.2, 2026-03-03)
   - 32 nodes, 98% test coverage
   - 14 INELIGIBLE outcomes, 1 ELIGIBLE outcome, 1 DEFERRED outcome

### Schema Version

- **Current**: v1.1 (2026-03-03)
- **Key Feature**: Added DEFERRED outcome type
- **Status**: Production-ready, validates both specifications

### Known TODOs (from Toby.Notes.md)

- [ ] Refactor domain-specific constants out of schema into specifications
- [ ] Consider MCP interface for state transition exploration
- [ ] Hook SWV instantiation into model for 51 test case handling

### Key Insights (from Toby.Notes.md)

1. **External Dependencies**: Some benefits have decisions deferred to other departments (e.g., Child Benefit → HMRC)

2. **Agent Navigation Required**: Decision trees require agent or human navigation due to nuanced terms that resist simple automation (e.g., "genuine vacancy" assessment)

3. **Third-Party Enrichment**: May need external data sources for things like "going rates" for job roles

---

## Quick Command Reference

```bash
# Validation
python3 ancillary_functionality/validate_specifications.py
python3 ancillary_functionality/check_orphan_nodes.py

# JSON Queries
jq '.decision_tree.nodes | keys' <spec>.json                    # List nodes
jq '.decision_tree.nodes[] | select(.type == "outcome")' <spec>.json  # Find outcomes
jq '.constants' <spec>.json                                      # View constants

# JSON Validation
python3 -m json.tool <spec>.json > /dev/null                     # Check syntax

# Find Files
find . -name "*.json" -type f                                    # All JSON files
find . -name "*RELEASE_NOTES.md"                                 # Release notes

# Statistics
jq '.decision_tree.nodes | length' <spec>.json                   # Count nodes
jq '[.decision_tree.nodes[].type] | group_by(.) | map({type: .[0], count: length})' <spec>.json
```

---

## When You Get Stuck

1. **Read README.md first** - It's comprehensive and well-maintained
2. **Check SCHEMA_DOCUMENTATION.md** - For node type requirements
3. **Look at existing specifications** - Use as templates/examples
4. **Run validation tools** - They provide specific error messages
5. **Check release notes** - Understand recent changes
6. **Review test analysis** - See how scenarios map to tree

---

## Contact & Contributions

### For Policy Questions

- Skilled Worker Visa: https://www.gov.uk/contact-ukvi
- Child Benefit: https://www.gov.uk/government/organisations/hm-revenue-customs/contact/child-benefit

### For Technical Changes

**Before submitting**:
- Ensure schema conformance (run validation tools)
- Document changes in release notes
- Update version numbers appropriately
- Add test scenarios for new edge cases
- Verify no orphan nodes or dangling references

---

**Last Updated**: 2026-03-12 (AGENTS.md creation)
**Schema Version**: v1.1
**Active Specifications**: Skilled Worker Visa v1.2, Child Benefit v1.2
