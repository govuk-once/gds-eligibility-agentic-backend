# JSON Schema Documentation (v2.0)

## Overview

The `eligibility-schema.json` file provides a formal JSON Schema (draft-07) specification for UK government service eligibility decision trees. This schema enables:

- **Domain Agnosticism**: Represent eligibility criteria for ANY UK government service without schema changes
- **Validation**: Automatically verify that eligibility JSON files conform to the expected structure
- **Documentation**: Self-documenting format with descriptions for all fields
- **IDE Support**: Enable autocomplete and validation in modern code editors
- **Type Safety**: Ensure data consistency across tools and implementations

**Current Version**: 2.0 (2026-03-12)  
**Breaking Changes from v1.x**: Yes (see [SCHEMA_V2_RELEASE_NOTES.md](SCHEMA_V2_RELEASE_NOTES.md))

## Schema Reference

The main eligibility data file references the schema via:

```json
{
  "$schema": "../../schemas/eligibility-schema.json",
  "version": "2.0",
  ...
}
```

## Top-Level Structure

### Required Properties

| Property | Type | Description |
|----------|------|-------------|
| `version` | string | Specification version number (semantic versioning: X.Y or X.Y.Z) |
| `last_updated` | string | ISO date (YYYY-MM-DD) when criteria last updated |
| `source` | string (URI) | Official government source URL |
| `description` | string | Human-readable description |
| `decision_tree` | object | Contains root node and all decision nodes |
| `constants` | object | Domain-specific fixed values (fully flexible) |

### Optional Properties

| Property | Type | Description |
|----------|------|-------------|
| `$schema` | string (URI) | Reference to this JSON Schema |
| `validation_rules` | object | Domain-specific business logic rules |
| `external_references` | object | URLs to external data sources |

### Constants Object (Flexible)

In v2.0, the `constants` object has `additionalProperties: true`, meaning it can contain ANY domain-specific structure:

**Example (Visa)**:
```json
{
  "constants": {
    "salary_thresholds": {
      "standard_minimum": 41700,
      "healthcare_education_minimum": 25000
    },
    "healthcare_surcharge_per_year": 1035,
    "english_level_required": "B2_CEFR"
  }
}
```

**Example (Benefit)**:
```json
{
  "constants": {
    "age_limits": {
      "standard_maximum_age": 16,
      "extension_period_weeks": 20
    },
    "time_limits": {
      "hospital_weeks": 12,
      "care_weeks": 8
    }
  }
}
```

## Node Types

The schema defines 7 abstract node types (v2.0):

| Type | Purpose | Use Case |
|------|---------|----------|
| `start` | Root entry point | Decision tree root |
| `boolean_question` | Yes/no decisions | Simple binary choices |
| `multi_path_check` | Multiple alternative paths (OR logic) | English language exemptions, salary routes |
| `criteria_check` | Measurable criteria validation | Salary checks, financial checks, age checks |
| `conditional_check` | Context-dependent questions | Questions that may not apply to all applicants |
| `complex_criteria` | Subjective assessments | Genuine vacancy checks, discretionary decisions |
| `routing` | Non-question routing | Categorization, age-based routing |
| `outcome` | Terminal decision | ELIGIBLE, INELIGIBLE, DEFERRED results |

### 1. Start Node (`start`)

**Location**: `decision_tree.root`

**Required Properties**:
- `id` (string): Unique identifier, typically "start"
- `type` (string): Must be "start"
- `description` (string): Purpose of the decision tree
- `next` (string): ID of first decision node

**Example**:
```json
{
  "id": "start",
  "type": "start",
  "description": "UK Skilled Worker Visa Eligibility Assessment",
  "next": "has_approved_employer"
}
```

---

### 2. Boolean Question Node (`boolean_question`)

Simple yes/no decision points.

**Required Properties**:
- `id` (string): Unique node identifier
- `type` (string): Must be "boolean_question"
- `question` (string): The yes/no question
- `outcomes` (object): Must have `yes` and `no` properties pointing to next node IDs

**Optional Properties**:
- `help_text` (string): Additional guidance
- `reference` (string, URI): Link to official guidance

**Example**:
```json
{
  "id": "has_approved_employer",
  "type": "boolean_question",
  "question": "Does the applicant have a job offer from a UK employer approved by the Home Office?",
  "help_text": "Approved employers are on the register of licensed sponsors",
  "reference": "https://www.gov.uk/...",
  "outcomes": {
    "yes": "has_certificate_of_sponsorship",
    "no": "INELIGIBLE_no_approved_employer"
  }
}
```

---

### 3. Multi-Path Check Node (`multi_path_check`)

Represents multiple alternative ways to satisfy a requirement (OR logic).

**Required Properties**:
- `id`, `type`, `question`
- `paths` (array): Array of Path objects (see below)
- `outcomes` (object): Map of outcome conditions to next node IDs

**Optional Properties**:
- `help_text`, `reference`
- `evaluation_logic` (string): Explanation of OR/AND logic
- Any domain-specific fields (e.g., `required_level` for language requirements)

**Path Object Properties**:
- `id` (string, **required**): Path identifier
- `description` (string, **required**): Human-readable description
- `criteria` (array of strings): List of requirements
- `requirement` (string): Single requirement statement
- `reference` (string, URI): Path-specific guidance URL
- **Any additional domain-specific fields** (fully flexible via `additionalProperties: true`)

**Example (Language Requirements)**:
```json
{
  "id": "check_english_language",
  "type": "multi_path_check",
  "question": "Does the applicant meet English language requirements?",
  "help_text": "Must prove English to at least B2 CEFR level unless exempt",
  "paths": [
    {
      "id": "exempt_nationality",
      "description": "National of exempt country",
      "eligible_countries": ["USA", "Canada", "Australia"]
    },
    {
      "id": "english_test",
      "description": "Secure English Language Test (SELT)",
      "requirement": "Pass SELT from approved provider at B2 level or above"
    }
  ],
  "outcomes": {
    "meets_requirement": "check_financial_requirement",
    "does_not_meet": "INELIGIBLE_english_language"
  }
}
```

**Example (Residency Paths)**:
```json
{
  "id": "check_claimant_residency",
  "type": "multi_path_check",
  "question": "Does the claimant meet UK residency requirements?",
  "paths": [
    {
      "id": "normally_resident_uk",
      "description": "Normally lives in the UK",
      "requirement": "Claimant normally lives in the UK"
    },
    {
      "id": "settled_status",
      "description": "Has settled status under EU Settlement Scheme",
      "requirement": "Has settled status under EU Settlement Scheme"
    }
  ],
  "outcomes": {
    "eligible_via_any_path": "check_responsibility_for_child",
    "not_eligible": "INELIGIBLE_residency_requirements"
  }
}
```

---

### 4. Criteria Check Node (`criteria_check`)

**New in v2.0** - replaces `salary_check`, `financial_check`, and domain-specific check types.

Validates measurable criteria (numeric, temporal, categorical).

**Required Properties**:
- `id`, `type`, `question`
- `criteria` (object): Domain-specific validation criteria (fully flexible structure)
- `outcomes` (object): Result-based routing

**Optional Properties**:
- `help_text`, `reference`

**Example (Salary Validation)**:
```json
{
  "id": "check_standard_salary_requirement",
  "type": "criteria_check",
  "question": "Does the salary meet the standard requirements?",
  "help_text": "Salary must be at least £41,700 per year OR the going rate for the job, whichever is HIGHER",
  "criteria": {
    "standard_threshold": 41700,
    "must_meet_going_rate": true,
    "comparison": "maximum"
  },
  "outcomes": {
    "meets_requirement": "check_english_language",
    "below_threshold": "check_reduced_salary_eligibility"
  }
}
```

**Example (Financial Requirement)**:
```json
{
  "id": "check_financial_requirement",
  "type": "criteria_check",
  "question": "Does the applicant meet financial requirements?",
  "criteria": {
    "required_amount": 1270,
    "holding_period_days": 28,
    "recency_requirement": "Day 28 must be within 31 days of application",
    "exemptions": [
      "Been in UK with valid visa for at least 12 months",
      "Employer confirms they can cover costs"
    ]
  },
  "outcomes": {
    "meets_requirement_or_exempt": "ELIGIBLE",
    "does_not_meet": "INELIGIBLE_insufficient_funds"
  }
}
```

**Example (Age Check)**:
```json
{
  "id": "check_education_level",
  "type": "criteria_check",
  "question": "Is the child in approved (non-advanced) education or training?",
  "criteria": {
    "must_be_non_advanced": true,
    "minimum_hours_per_week": 12,
    "approved_qualifications": ["A-levels", "T-levels", "NVQ Level 3"],
    "excluded_qualifications": ["University degrees", "HNC", "HND"]
  },
  "outcomes": {
    "approved_education": "check_child_not_working_full_time",
    "advanced_education": "INELIGIBLE_advanced_education"
  }
}
```

---

### 5. Conditional Check Node (`conditional_check`)

Questions that may not apply to all applicants.

**Required Properties**:
- `id`, `type`, `question`
- `outcomes` (object): Should include "not applicable" option

**Optional Properties**:
- `help_text`, `reference`

**Example**:
```json
{
  "id": "check_switching_eligibility",
  "type": "conditional_check",
  "question": "If applicant is switching from Student visa in the UK, have they completed their course?",
  "help_text": "Not applicable if applying from outside UK",
  "outcomes": {
    "yes_or_not_applicable": "has_approved_employer",
    "no": "INELIGIBLE_student_not_completed"
  }
}
```

---

### 6. Complex Criteria Node (`complex_criteria`)

Subjective or discretionary assessments requiring human judgment.

**Required Properties**:
- `id`, `type`, `question`
- `outcomes` (object): Based on subjective assessment

**Optional Properties**:
- `help_text`, `reference`
- `criteria` (object): Factors to consider (flexible structure)
- `disclaimer` (string): Warning about discretionary nature
- `common_red_flags` (array): Warning indicators

**Example**:
```json
{
  "id": "check_genuine_vacancy",
  "type": "complex_criteria",
  "question": "Is this a genuine vacancy that meets credibility requirements?",
  "criteria": {
    "genuine_business_need": "Role must fill an actual business need",
    "credible_job_description": "Duties must be substantive and specific",
    "appropriate_for_business_size": "Role must be proportionate to sponsor's size"
  },
  "disclaimer": "This is a discretionary check. Even if all measurable criteria are met, applications can be refused on credibility grounds.",
  "common_red_flags": [
    "Small business suddenly creating high-level role",
    "Vague or generic job description",
    "Role appears tailored to specific individual"
  ],
  "outcomes": {
    "appears_genuine": "check_genuine_employment",
    "credibility_concerns": "INELIGIBLE_not_genuine_vacancy"
  }
}
```

---

### 7. Routing Node (`routing`)

Flow control without asking a question (categorization logic).

**Required Properties**:
- `id`, `type`
- `description` (string): Routing logic explanation
- `outcomes` (object): Routing conditions to target nodes

**Optional Properties**:
- `routing_logic` (string): Detailed routing algorithm

**Example**:
```json
{
  "id": "determine_salary_threshold",
  "type": "routing",
  "description": "Determine which salary rules apply based on job type",
  "routing_logic": "If occupation is in healthcare/education list, go to healthcare_education_salary, else go to standard",
  "outcomes": {
    "healthcare_education": "check_healthcare_education_salary",
    "standard": "check_standard_salary_requirement"
  }
}
```

---

### 8. Outcome Node (`outcome`)

Terminal nodes representing eligibility determination.

**Required Properties**:
- `id`, `type`
- `result` (string): Must be "ELIGIBLE", "INELIGIBLE", or "DEFERRED"

**Conditional Requirements**:

**If `result` is "ELIGIBLE"**:
- `description` (string, required)
- `next_steps` (array of strings, required)

**If `result` is "INELIGIBLE"**:
- `reason` (string, required): Why applicant is ineligible
- `guidance` (string, required): What to do next

**If `result` is "DEFERRED"**:
- `reason` (string, required): Why external decision is needed
- `guidance` (string, required): What to do next

**Optional Properties** (domain-specific extensions allowed):
- `reference` (string, URI): Official guidance URL
- `processing_time` (object): For ELIGIBLE outcomes (visa applications)
- `hmrc_decision_criteria` (array): For DEFERRED outcomes (benefit disputes)
- `required_evidence` (array): For DEFERRED outcomes
- Any other domain-specific metadata

**Example (Eligible)**:
```json
{
  "id": "ELIGIBLE",
  "type": "outcome",
  "result": "ELIGIBLE",
  "description": "Applicant meets all criteria for Skilled Worker visa",
  "next_steps": [
    "Apply online within 3 months of Certificate of Sponsorship date",
    "Pay application fee (£769-£1,751 depending on circumstances)",
    "Pay healthcare surcharge (£1,035 per year)"
  ],
  "processing_time": {
    "outside_uk": "3 weeks",
    "inside_uk": "8 weeks"
  }
}
```

**Example (Ineligible)**:
```json
{
  "id": "INELIGIBLE_salary_too_low",
  "type": "outcome",
  "result": "INELIGIBLE",
  "reason": "Salary does not meet minimum requirements for this visa",
  "guidance": "Check if eligible for reduced salary requirements or another visa type"
}
```

**Example (Deferred)**:
```json
{
  "id": "DEFERRED_TO_HMRC",
  "type": "outcome",
  "result": "DEFERRED",
  "reason": "Multiple people claim responsibility for the child and cannot agree",
  "guidance": "HMRC will make the decision based on evidence of circumstances",
  "hmrc_decision_criteria": [
    "Primary residence (where child spends most nights)",
    "Main contributor to child's upkeep and care",
    "Stability and continuity for the child"
  ],
  "required_evidence": [
    "Proof of residence (utility bills, rental agreement)",
    "School registration and correspondence",
    "Financial contribution evidence (bank statements, receipts)"
  ],
  "reference": "https://www.gov.uk/child-benefit-child-lives-with-someone-else"
}
```

---

## Validation

### Using Python Validation Script

```bash
cd ancillary_functionality
python3 validate_specifications.py
```

**Output**:
```
================================================================================
ELIGIBILITY SPECIFICATION SCHEMA VALIDATION
================================================================================

✓ Schema loaded: ../schemas/eligibility-schema.json
  Schema version: 2.0

--------------------------------------------------------------------------------
Validating: ../specifications/skilled_worker_visa/skilled_worker_visa_eligibility.json
--------------------------------------------------------------------------------
✓ JSON parsed successfully
  Specification version: 2.0

✅ VALIDATION PASSED

📊 Statistics:
  • Total nodes: 32
  • Outcome nodes: 14
  • Decision nodes: 18
```

### Using JSON Schema Validator Library

```python
import json
import jsonschema

# Load files
with open('specifications/skilled_worker_visa/skilled_worker_visa_eligibility.json') as f:
    data = json.load(f)

with open('schemas/eligibility-schema.json') as f:
    schema = json.load(f)

# Validate
try:
    jsonschema.validate(instance=data, schema=schema)
    print("✓ Valid")
except jsonschema.ValidationError as e:
    print(f"✗ Invalid: {e.message}")
```

Install jsonschema: `pip install jsonschema`

### Using Online Tools

1. Go to https://www.jsonschemavalidator.net/
2. Paste schema in left panel
3. Paste data in right panel
4. See validation results instantly

---

## Migration from v1.x to v2.0

See [SCHEMA_V2_RELEASE_NOTES.md](SCHEMA_V2_RELEASE_NOTES.md) for detailed migration guide.

**Quick summary**:
1. Update `version` to "2.0" in specification files
2. Change `salary_check` → `criteria_check`
3. Change `financial_check` → `criteria_check`
4. Change `occupation_check` → `routing` (with `description` field)
5. All other node types remain unchanged
6. All domain-specific fields are now allowed and preserved

---

## IDE Integration

### VS Code

Install the JSON Language Features extension (built-in). The `$schema` reference enables:
- Autocomplete for properties
- Inline documentation on hover
- Real-time validation errors
- Schema-aware navigation

### IntelliJ IDEA / WebStorm

1. Settings → Languages & Frameworks → Schemas and DTDs → JSON Schema Mappings
2. Add schema file and associate with data file pattern
3. IDE will validate automatically

### Other Editors

Most modern editors support JSON Schema via plugins:
- Atom: linter-jsonschema
- Sublime Text: LSP-json
- Vim/Neovim: coc-json

---

## Best Practices

### 1. Always Reference Schema
Include `$schema` property in all specification files:
```json
{
  "$schema": "../../schemas/eligibility-schema.json",
  "version": "2.0",
  ...
}
```

### 2. Validate Before Commit
Run validation as part of development workflow:
```bash
cd ancillary_functionality
python3 validate_specifications.py || exit 1
```

### 3. Use Descriptive IDs
Node IDs should be:
- Lowercase with underscores (snake_case)
- Descriptive of their purpose
- Unique across the entire tree

Examples:
- ✅ `check_standard_salary_requirement`
- ✅ `INELIGIBLE_salary_too_low`
- ❌ `node1`, `check`, `outcome_a`

### 4. Document Complex Logic
Use `help_text`, `description`, `evaluation_logic`, and `routing_logic` fields to explain:
- Why a question is asked
- How multiple criteria combine
- What external data is needed
- Edge cases and special circumstances

### 5. Separate Domain Logic from Structure
- **Schema**: Defines structural patterns (node types, required fields)
- **Specification**: Implements domain logic (salary thresholds, age limits, specific rules)

---

## Troubleshooting

### "Invalid node type"
Ensure node `type` is one of: `start`, `boolean_question`, `multi_path_check`, `criteria_check`, `conditional_check`, `complex_criteria`, `routing`, `outcome`.

**v1.x node types removed in v2.0**: `salary_check`, `financial_check`, `occupation_check`

### "Property X is required"
Check conditional requirements:
- Boolean questions must have `yes` and `no` in `outcomes`
- ELIGIBLE outcomes must have `description` and `next_steps`
- INELIGIBLE outcomes must have `reason` and `guidance`
- DEFERRED outcomes must have `reason` and `guidance`

### "Type mismatch"
Verify property types match schema:
- Numbers should be numeric, not strings (e.g., `1270`, not `"1270"`)
- URIs should be valid URLs
- Arrays should use `[...]` syntax
- Objects should use `{...}` syntax

### "Node ID mismatch"
The node's `id` field must match its key in the `nodes` object:
```json
{
  "nodes": {
    "check_salary": {
      "id": "check_salary",  // Must match key above
      ...
    }
  }
}
```

---

## Version History

- **v2.0** (2026-03-12): **Major refactoring for domain agnosticism**
  - Removed domain-specific node types (`salary_check`, `financial_check`, `occupation_check`)
  - Introduced abstract `criteria_check` node type
  - Made `constants` fully flexible (`additionalProperties: true`)
  - Made `Path` objects fully flexible
  - Made outcome nodes extensible
  - Both specifications migrated and validated successfully

- **v1.1** (2026-03-03): Added DEFERRED outcome type
  - Support for external decision-making scenarios (HMRC arbitration)
  - Optional fields for DEFERRED outcomes

- **v1.0** (2026-03-02): Initial schema release
  - 9 node types (10 including start)
  - Complete validation for UK Skilled Worker Visa criteria
  - JSON Schema draft-07 compliant

---

## Related Files

- **eligibility-schema.json**: The JSON Schema file (this is what you're documenting)
- **SCHEMA_V2_RELEASE_NOTES.md**: Detailed v2.0 migration guide and changelog
- **specifications/skilled_worker_visa/**: Skilled Worker Visa specification (v2.0)
- **specifications/child_benefit/**: Child Benefit specification (v2.0)
- **ancillary_functionality/validate_specifications.py**: Validation script
- **ancillary_functionality/check_orphan_nodes.py**: Orphan node detection
- **README.md**: Project overview
- **AGENTS.md**: Guide for AI agents working on this project
