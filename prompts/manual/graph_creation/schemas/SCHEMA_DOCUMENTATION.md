# JSON Schema Documentation

## Overview

The `eligibility-schema.json` file provides a formal JSON Schema (draft-07) specification for the UK Skilled Worker Visa eligibility decision tree format. This schema enables:

- **Validation**: Automatically verify that eligibility JSON files conform to the expected structure
- **Documentation**: Self-documenting format with descriptions for all fields
- **IDE Support**: Enable autocomplete and validation in modern code editors
- **Type Safety**: Ensure data consistency across tools and implementations

## Schema Reference

The main eligibility data file references the schema via:

```json
{
  "$schema": "./eligibility-schema.json",
  ...
}
```

## Top-Level Structure

### Required Properties

| Property | Type | Description |
|----------|------|-------------|
| `version` | string | Version number (semantic versioning: X.Y or X.Y.Z) |
| `last_updated` | string | ISO date (YYYY-MM-DD) when criteria last updated |
| `source` | string (URI) | Official government source URL |
| `description` | string | Human-readable description |
| `decision_tree` | object | Contains root node and all decision nodes |
| `constants` | object | Fixed values (salary thresholds, fees, etc.) |

### Optional Properties

| Property | Type | Description |
|----------|------|-------------|
| `$schema` | string (URI) | Reference to this JSON Schema |
| `validation_rules` | object | Business logic rules for complex validations |
| `external_references` | object | URLs to external data sources |

## Node Types

The schema defines 9 distinct node types, each with specific required and optional properties:

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

### 3. Multi-Path Check Node (`multi_path_check`)

Represents multiple alternative ways to satisfy a requirement (OR logic).

**Required Properties**:
- `id`, `type`, `question`
- `paths` (array): Array of Path objects (see below)
- `outcomes` (object): Map of outcome conditions to next node IDs

**Optional Properties**:
- `help_text`, `reference`
- `evaluation_logic` (string): Explanation of OR/AND logic
- `required_level` (string): For English language nodes
- `minimum_salary_for_reduction` (number): For salary nodes

**Path Object Properties**:
- `id` (string, required): Path identifier
- `description` (string, required): Human-readable description
- `salary_minimum` (number): Minimum salary for this path
- `salary_percentage` (string): Percentage of going rate
- `criteria` (array of strings): List of requirements
- `requirement` (string): Single requirement statement
- `qualifications` (array): Acceptable qualifications
- `eligible_countries` (array): Exempt countries
- `eligible_professions` (array): Eligible professions
- `eligible_occupation_codes` (array): SOC codes
- `occupation_descriptions` (object): Code to description map
- `time_limit` (string): Maximum time limit
- `benefits` (array): Additional benefits
- `reference` (string, URI): Path-specific guidance URL

**Example**:
```json
{
  "id": "check_english_language",
  "type": "multi_path_check",
  "question": "Does the applicant meet English language requirements?",
  "required_level": "B2 CEFR",
  "paths": [
    {
      "id": "exempt_nationality",
      "description": "National of exempt country",
      "eligible_countries": ["USA", "Canada", "Australia", ...]
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

### 4. Salary Check Node (`salary_check`)

Validates salary against thresholds and going rates.

**Required Properties**:
- `id`, `type`, `question`
- `criteria` (object): Salary validation criteria
  - `minimum_absolute` (number): Absolute minimum in GBP
  - `standard_threshold` (number): Standard threshold
  - `must_meet_going_rate` (boolean): Whether going rate applies
  - `going_rate_source` (string): Source for going rate
  - `comparison` (string): "minimum" or "maximum"
- `outcomes` (object): Result-based routing

**Example**:
```json
{
  "id": "check_standard_salary_requirement",
  "type": "salary_check",
  "question": "Does the salary meet the standard requirements?",
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

### 5. Financial Check Node (`financial_check`)

Validates financial requirements.

**Required Properties**:
- `id`, `type`, `question`
- `criteria` (object):
  - `required_amount` (number): Required GBP amount
  - `holding_period_days` (integer): Days funds must be held
  - `recency_requirement` (string): Recency constraint
  - `exemptions` (array of strings): Exemption conditions
- `outcomes` (object)

### 6. Occupation Check Node (`occupation_check`)

Checks job eligibility based on skill level.

**Required Properties**:
- `id`, `type`, `question`
- `outcomes` (object): Must include `higher_skilled`, `medium_skilled`, `not_eligible`

### 7. Conditional Check Node (`conditional_check`)

Questions that may not apply to all applicants.

**Required Properties**:
- `id`, `type`, `question`
- `outcomes` (object): Should include "not applicable" option

### 8. Routing Node (`routing`)

Flow control based on job/applicant type.

**Required Properties**:
- `id`, `type`
- `description` (string): Routing logic explanation
- `outcomes` (object): Routing conditions to target nodes

**Optional Properties**:
- `routing_logic` (string): Detailed routing algorithm

### 9. Outcome Node (`outcome`)

Terminal nodes representing eligibility determination.

**Required Properties**:
- `id`, `type`
- `result` (string): Must be "ELIGIBLE" or "INELIGIBLE"

**Conditional Requirements**:
- If `result` is "ELIGIBLE":
  - `description` (string, required)
  - `next_steps` (array of strings, required)
  - `processing_time` (object, optional): `outside_uk` and `inside_uk` times
  
- If `result` is "INELIGIBLE":
  - `reason` (string, required): Why applicant is ineligible
  - `guidance` (string, required): What to do next

**Example (Eligible)**:
```json
{
  "id": "ELIGIBLE",
  "type": "outcome",
  "result": "ELIGIBLE",
  "description": "Applicant meets all criteria",
  "next_steps": [
    "Apply online within 3 months",
    "Pay fees",
    ...
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
  "reason": "Salary does not meet minimum requirements",
  "guidance": "Check if eligible for reduced salary requirements"
}
```

## Validation

### Using Python

```python
import json
import jsonschema

# Load files
with open('skilled_worker_visa_eligibility.json') as f:
    data = json.load(f)

with open('eligibility-schema.json') as f:
    schema = json.load(f)

# Validate
try:
    jsonschema.validate(instance=data, schema=schema)
    print("✓ Valid")
except jsonschema.ValidationError as e:
    print(f"✗ Invalid: {e.message}")
```

Install jsonschema: `pip install jsonschema`

### Using validate_and_visualize.py

The validation script automatically checks against the schema:

```bash
python3 validate_and_visualize.py
```

Output includes schema validation step:
```
2. Validating against JSON Schema...
✓ Schema validation passed
```

### Using Online Tools

1. Go to https://www.jsonschemavalidator.net/
2. Paste schema in left panel
3. Paste data in right panel
4. See validation results instantly

## Schema Extensions

To extend the schema for new node types:

1. Add new enum value to `Node.type`
2. Create new definition (e.g., `MyNewNodeType`)
3. Add conditional to `Node.allOf` array:

```json
{
  "if": {
    "properties": {"type": {"const": "my_new_type"}}
  },
  "then": {
    "$ref": "#/definitions/MyNewNodeType"
  }
}
```

4. Define the new node type in `definitions`:

```json
"MyNewNodeType": {
  "type": "object",
  "required": ["id", "type", ...],
  "properties": {
    "id": {"type": "string"},
    "type": {"const": "my_new_type"},
    ...
  }
}
```

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

## Best Practices

### 1. Always Reference Schema
Include `$schema` property in all data files:
```json
{
  "$schema": "./eligibility-schema.json",
  ...
}
```

### 2. Validate Before Commit
Run validation as part of CI/CD pipeline:
```bash
python3 validate_and_visualize.py || exit 1
```

### 3. Keep Schema and Data in Sync
When updating data structure:
1. Update schema first
2. Validate existing data against new schema
3. Fix any validation errors
4. Update documentation

### 4. Use Descriptive IDs
Node IDs should be:
- Lowercase with underscores
- Descriptive of their purpose
- Unique across the entire tree

### 5. Document Complex Logic
Use `help_text`, `description`, and `evaluation_logic` fields to explain:
- Why a question is asked
- How multiple criteria combine
- What external data is needed

## Troubleshooting

### "Property X is not allowed"
The schema uses `additionalProperties: false` for some node types. Check that all properties are defined in the schema.

### "Property X is required"
Ensure all required fields are present. Check conditional requirements for outcome nodes.

### "Type mismatch"
Verify property types match schema:
- Numbers should be numeric, not strings
- URIs should be valid URLs
- Enums must match exactly

### "Invalid $schema reference"
Ensure:
- Schema file exists at referenced path
- Path is relative or absolute URL
- File is valid JSON

## Version History

- **v1.0** (2026-03-02): Initial schema release
  - 9 node types
  - Complete validation for UK Skilled Worker Visa criteria
  - JSON Schema draft-07 compliant

## Related Files

- **skilled_worker_visa_eligibility.json**: Main data file validated by this schema
- **validate_and_visualize.py**: Validation script with schema checking
- **README.md**: General documentation
- **IMPLEMENTATION_SUMMARY.md**: Design decisions and requirements verification
