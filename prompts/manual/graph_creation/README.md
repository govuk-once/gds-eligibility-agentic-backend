# UK Skilled Worker Visa Eligibility - Machine-Readable Representation

## Overview

This directory contains a complete, machine-readable representation of the UK Skilled Worker Visa eligibility criteria based on official Gov.UK guidance.

## Files

- **`skilled_worker_visa_eligibility.json`** - Complete decision tree representation in JSON format
- **`visualization_guide.md`** - Guide for visualizing the decision tree as a graph
- **`README.md`** - This file

## Structure

The JSON file contains:

### 1. Decision Tree
A directed graph where each node represents:
- **Boolean questions** - Yes/No decisions
- **Multi-path checks** - Multiple ways to satisfy a requirement
- **Salary checks** - Complex salary threshold validations
- **Routing nodes** - Logic to direct flow based on job type
- **Outcomes** - Terminal nodes showing ELIGIBLE or INELIGIBLE results

### 2. Node Types

#### `boolean_question`
Simple yes/no decisions with two outcomes.

```json
{
  "type": "boolean_question",
  "question": "Does the applicant have X?",
  "outcomes": {
    "yes": "next_node_id",
    "no": "failure_node_id"
  }
}
```

#### `multi_path_check`
Multiple alternative paths to satisfy a requirement (OR logic).

```json
{
  "type": "multi_path_check",
  "question": "Does applicant meet requirement via any path?",
  "paths": [
    {"id": "path1", "description": "..."},
    {"id": "path2", "description": "..."}
  ],
  "outcomes": {
    "eligible_via_any_path": "next_node",
    "not_eligible": "failure_node"
  }
}
```

#### `salary_check`
Validates salary against thresholds and going rates.

```json
{
  "type": "salary_check",
  "criteria": {
    "minimum_absolute": 41700,
    "must_meet_going_rate": true,
    "comparison": "maximum"
  }
}
```

#### `outcome`
Terminal node indicating eligibility result.

```json
{
  "type": "outcome",
  "result": "ELIGIBLE" | "INELIGIBLE",
  "reason": "Description of why",
  "guidance": "What to do next"
}
```

### 3. Constants
Fixed values referenced throughout the criteria:
- Salary thresholds
- Financial requirements
- Application fees
- Processing times

### 4. Validation Rules
Business logic for complex calculations:
- Salary comparisons (must be HIGHER of multiple values)
- Time limits for certain routes
- Minimum wage requirements

### 5. External References
Links to official Gov.UK pages and resources for:
- Eligible occupation lists
- Going rates tables
- Approved employers register
- Qualification assessment services

## Key Features

### Deterministic
Given the same input, the system always produces the same output. All conditional logic is explicit.

### Complete
Covers all eligibility paths including:
- Standard salary route (£41,700+)
- Healthcare/education route (£25,000+)
- Immigration Salary List route (£33,400+)
- Under 26/graduate/training route (70% of going rate)
- PhD routes (80-90% of going rate)
- Postdoctoral route (70% of going rate)

### Edge Cases Handled
- Medium skilled occupations requiring list membership
- Care worker CQC registration requirements
- English language exemptions (multiple paths)
- Financial requirement exemptions
- Time limits on reduced salary routes

### Unambiguous
All conditions are precisely specified:
- Exact salary thresholds (not "approximately")
- Clear Boolean logic (AND/OR)
- Explicit eligibility criteria for each path
- References to authoritative sources

## Usage

### For Developers
Parse the JSON to build:
- Web-based eligibility checkers
- Automated application validators
- Decision support tools
- Compliance systems

### For Policy Experts
Review the decision tree to:
- Verify completeness of representation
- Identify policy edge cases
- Audit decision logic
- Document policy changes

### For Visualization
Use the node structure to generate:
- Flowcharts
- Interactive decision trees
- Graph diagrams (see `visualization_guide.md`)

## Validation

To validate an applicant's eligibility:

1. Start at `root` node
2. Evaluate the current node's question/criteria
3. Follow the appropriate outcome edge to next node
4. Repeat until reaching an `outcome` node
5. The outcome node's `result` field indicates eligibility

### Example Walk-through

**Applicant Profile:**
- Job offer: Yes, from approved employer
- CoS: Yes
- Occupation: Software developer (higher skilled)
- Salary: £50,000
- Going rate: £45,000
- English: Degree from US university
- Funds: £2,000 for 28+ days

**Path through tree:**
1. `start` → `has_approved_employer` (YES)
2. `has_approved_employer` → `has_certificate_of_sponsorship` (YES)
3. `has_certificate_of_sponsorship` → `check_occupation_eligibility` (higher_skilled)
4. `check_occupation_eligibility` → `determine_salary_threshold` (standard)
5. `determine_salary_threshold` → `check_standard_salary_requirement` (PASS: £50k > max(£41,700, £45k))
6. `check_standard_salary_requirement` → `check_english_language` (exempt_nationality: USA)
7. `check_english_language` → `check_financial_requirement` (meets: £2,000 > £1,270)
8. `check_financial_requirement` → `ELIGIBLE`

## Maintenance

When UK visa rules change:

1. Update the relevant node criteria in the JSON
2. Update `last_updated` date
3. Add new nodes if decision logic changes
4. Update `external_references` if URLs change
5. Document changes in version control

## Completeness Verification

This representation includes:

✅ All mandatory requirements (employer, CoS, occupation, salary, English, funds)  
✅ All salary routes (standard, healthcare/education, reduced options)  
✅ All English language paths (exemptions + proof methods)  
✅ All edge cases mentioned in official guidance  
✅ Special requirements (CQC for care workers)  
✅ Time limits for certain routes  
✅ Application fees and costs  
✅ External reference links for dynamic data (occupation lists, going rates)  

## Limitations

### Dynamic Data Not Included
The following are referenced but not embedded (they change frequently):
- List of eligible occupations (by SOC code)
- Going rates per occupation
- Immigration Salary List contents
- Temporary Shortage List contents
- List of approved employers
- Specific NHS/education pay scales

These are referenced via `external_references` URLs.

### Out of Scope
- Extension and switching criteria (briefly referenced but not fully modeled)
- Dependant eligibility (separate criteria)
- Settlement/indefinite leave requirements
- Application process details (non-eligibility)

## License

This representation is based on UK Government information available under the Open Government Licence v3.0.

## Contact

For questions about UK Skilled Worker visa policy, consult:
- https://www.gov.uk/skilled-worker-visa
- UK Visas and Immigration guidance
