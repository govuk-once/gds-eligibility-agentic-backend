# UK Government Service Eligibility - Machine-Readable Specifications

## Overview

This directory contains complete, machine-readable representations of UK government service eligibility criteria based on official Gov.UK guidance. The specifications use a standardized JSON Schema to model complex eligibility decision trees in a deterministic, visualizable format.

## Project Contents

### Eligibility Specifications

1. **[Skilled Worker Visa](./skilled_worker_visa_eligibility.json)** (v1.2)
   - Immigration eligibility criteria
   - 32 nodes, 90%+ coverage
   - 13 INELIGIBLE outcomes, 1 ELIGIBLE outcome
   - [Release Notes](./VERSION_1.2_RELEASE_NOTES.md)

2. **[Child Benefit](./child_benefit_eligibility.json)** (v1.2)
   - Welfare benefit eligibility criteria
   - 32 nodes, 98% coverage (49/50 test scenarios)
   - 14 INELIGIBLE outcomes, 1 ELIGIBLE outcome, 1 DEFERRED outcome
   - [Detailed README](./CHILD_BENEFIT_README.md) | [Release Notes](./CHILD_BENEFIT_VERSION_1.2_RELEASE_NOTES.md)

### JSON Schema

**[eligibility-schema.json](./eligibility-schema.json)** (v1.1)
- Defines structure for all eligibility specifications
- 10 node types: start, boolean_question, multi_path_check, salary_check, financial_check, occupation_check, conditional_check, complex_criteria, routing, outcome
- 3 outcome result types: ELIGIBLE, INELIGIBLE, DEFERRED
- Supports multiple UK government services

### Validation & Analysis Tools

**Python Tools:**
- **[validate_specifications.py](./validate_specifications.py)** - Validates specifications against schema
- **[check_orphan_nodes.py](./check_orphan_nodes.py)** - Detects orphan nodes and dangling references

**Reports:**
- [Schema Validation Report](./SCHEMA_VALIDATION_REPORT.md)
- [Orphan Node Cleanup Report](./ORPHAN_NODE_CLEANUP_REPORT.md)

### Documentation

**Process Documentation:**
- [INDEX.md](./INDEX.md) - Project index and version history
- [visualization_guide.md](./visualization_guide.md) - Guide for creating visual representations

**Test Analysis:**
- [Child Benefit Test Analysis](./CHILD_BENEFIT_TEST_ANALYSIS.md) - Coverage analysis against 50 test scenarios

---

## Specification Structure

Each specification contains:

### 1. Decision Tree

A directed graph where each node represents a decision point or outcome:

**Node Types:**
- **start** - Entry point (root node)
- **boolean_question** - Yes/No decisions
- **multi_path_check** - Multiple alternative paths (OR logic)
- **salary_check** - Complex salary threshold validations
- **financial_check** - Financial requirement validations
- **occupation_check** - Occupation skill level checks
- **conditional_check** - Questions that may not apply to all applicants
- **complex_criteria** - Multi-factor criteria evaluation
- **routing** - Non-question routing logic
- **outcome** - Terminal nodes with eligibility results

### 2. Outcome Types

**ELIGIBLE** - Applicant qualifies for the service
- Requires: `description`, `next_steps`
- Example: Successfully meets all Child Benefit criteria

**INELIGIBLE** - Applicant does not qualify
- Requires: `reason`, `guidance`
- Example: Salary below threshold for Skilled Worker Visa

**DEFERRED** - External decision required
- Requires: `reason`, `guidance`
- Optional: `hmrc_decision_criteria`, `required_evidence`
- Example: Disputed Child Benefit claim requiring HMRC arbitration

### 3. Constants

Fixed values referenced throughout the criteria:
- Salary thresholds (Skilled Worker Visa)
- Time limits (hospital/care duration for Child Benefit)
- Financial requirements
- Application fees

### 4. Validation Rules

Business logic for complex calculations:
- Salary comparisons (must be HIGHER of multiple values)
- Time limits for certain routes
- Regional variations (e.g., apprenticeship rules by country)
- Age and education requirements

### 5. External References

Links to official Gov.UK pages and resources:
- Eligible occupation lists
- Going rates tables
- Approved employers register
- Qualification assessment services

---

## Node Type Examples

### Boolean Question
Simple yes/no decisions with two outcomes.

```json
{
  "id": "has_approved_employer",
  "type": "boolean_question",
  "question": "Does the applicant have a job offer from a UK employer approved by the Home Office?",
  "help_text": "Approved employers are on the register of licensed sponsors",
  "reference": "https://www.gov.uk/government/publications/register-of-licensed-sponsors-workers",
  "outcomes": {
    "yes": "has_certificate_of_sponsorship",
    "no": "INELIGIBLE_no_approved_employer"
  }
}
```

### Multi-Path Check
Multiple alternative paths to satisfy a requirement (OR logic).

```json
{
  "id": "check_reduced_salary_eligibility",
  "type": "multi_path_check",
  "question": "Is the applicant eligible for reduced salary requirements?",
  "evaluation_logic": "Check each path in any order. If ANY path is satisfied, outcome is 'eligible_via_any_path'.",
  "paths": [
    {
      "id": "immigration_salary_list",
      "description": "Job is on the Immigration Salary List",
      "salary_minimum": 33400,
      "salary_percentage": "100% of going rate"
    },
    {
      "id": "under_26_or_graduate",
      "description": "Under 26, recent graduate, or in professional training",
      "salary_minimum": 33400,
      "salary_percentage": "70% of going rate"
    }
  ],
  "outcomes": {
    "eligible_via_any_path": "check_english_language",
    "not_eligible": "INELIGIBLE_salary_too_low"
  }
}
```

### Routing Node
Non-question routing based on categories.

```json
{
  "id": "has_qualifying_child",
  "type": "routing",
  "description": "Determine child's age category for eligibility",
  "routing_logic": "Under 16: automatic qualification. 16-19: check education/training. 20+: not eligible",
  "outcomes": {
    "under_16": "check_child_not_working_full_time",
    "16_to_19": "check_education_or_extension",
    "20_or_over": "INELIGIBLE_no_qualifying_child"
  }
}
```

### Complex Criteria
Multi-factor criteria requiring subjective assessment.

```json
{
  "id": "check_genuine_vacancy",
  "type": "complex_criteria",
  "question": "Is this a genuine vacancy that meets credibility requirements?",
  "criteria": {
    "genuine_business_need": "Role must fill an actual business need, not created solely for sponsorship",
    "credible_job_description": "Duties must be substantive, specific, and match the SOC code",
    "appropriate_for_business_size": "Role must be proportionate to the sponsor's size and operations"
  },
  "disclaimer": "This is a discretionary check based on the totality of circumstances.",
  "common_red_flags": [
    "Small business suddenly creating high-level role",
    "Vague or generic job description",
    "Business financials don't support the salary level"
  ],
  "outcomes": {
    "appears_genuine": "check_genuine_employment",
    "credibility_concerns": "INELIGIBLE_not_genuine_vacancy"
  }
}
```

### Outcome Node
Terminal node indicating eligibility result.

```json
{
  "id": "ELIGIBLE",
  "type": "outcome",
  "result": "ELIGIBLE",
  "description": "Applicant meets all Skilled Worker Visa eligibility criteria",
  "next_steps": [
    "Complete online application form",
    "Pay application fee and healthcare surcharge",
    "Provide biometric information",
    "Submit required documents"
  ],
  "processing_time": {
    "outside_uk": "3 weeks",
    "inside_uk": "8 weeks"
  }
}
```

```json
{
  "id": "DEFERRED_TO_HMRC",
  "type": "outcome",
  "result": "DEFERRED",
  "reason": "Multiple people claim responsibility for the child and cannot agree who should claim",
  "guidance": "HMRC will decide who is entitled to claim based on the circumstances. Submit evidence to support your claim.",
  "hmrc_decision_criteria": [
    "Who the child primarily lives with (or spends most time with)",
    "Who contributes most to the child's upbringing financially",
    "Who provides day-to-day care"
  ],
  "required_evidence": [
    "Proof of residence (utility bills, tenancy agreement)",
    "School registration documents",
    "Medical registration documents",
    "Financial contribution records"
  ]
}
```

---

## Key Features

### Deterministic
Given the same input, the system always produces the same output. All conditional logic is explicit.

### Complete Coverage

**Skilled Worker Visa (90%+):**
- Standard salary route (£41,700+)
- Healthcare/education route (£25,000+)
- Immigration Salary List route (£33,400+, 100% going rate)
- Under 26/graduate/training route (70% of going rate)
- PhD routes (80-90% of going rate)
- Postdoctoral route (70% of going rate)
- Part-time worker special rules
- Genuine vacancy assessment

**Child Benefit (98%):**
- 8 residency paths (UK resident, settled status, Crown servant, etc.)
- 3 responsibility paths (living with child, contributing, maintenance)
- Hospital/care time limits (12-week, 8-week with linking rules)
- Education requirements (approved vs. advanced)
- Apprenticeship regional variations
- 20-week extension rules
- HMRC arbitration for disputes

### Unambiguous
All conditions are precisely specified:
- Exact salary thresholds (not "approximately")
- Clear Boolean logic (AND/OR)
- Explicit eligibility criteria for each path
- References to authoritative sources

### Visualizable
Node structure supports generation of:
- Flowcharts
- Interactive decision trees
- Graph diagrams (see [visualization_guide.md](./visualization_guide.md))

---

## Usage

### For Developers

Parse the JSON specifications to build:
- **Web-based eligibility checkers** - Interactive tools for applicants
- **Automated application validators** - Pre-submission verification
- **Decision support tools** - Caseworker assistance systems
- **Compliance systems** - Policy adherence monitoring
- **API services** - Eligibility-as-a-service

**Example: Walking the Decision Tree**

```javascript
function checkEligibility(spec, applicantData) {
  let currentNode = spec.decision_tree.root;
  
  while (currentNode.type !== 'outcome') {
    const node = spec.decision_tree.nodes[currentNode.next];
    
    // Evaluate node based on type
    const nextNodeId = evaluateNode(node, applicantData);
    currentNode = spec.decision_tree.nodes[nextNodeId];
  }
  
  return currentNode.result; // ELIGIBLE, INELIGIBLE, or DEFERRED
}
```

### For Policy Experts

Review the decision trees to:
- **Verify completeness** of representation
- **Identify policy edge cases** not yet covered
- **Audit decision logic** for correctness
- **Document policy changes** with version control
- **Compare implementations** across services

### For Validation

**Run schema validation:**
```bash
python3 validate_specifications.py
```

**Check for orphan nodes:**
```bash
python3 check_orphan_nodes.py
```

### For Visualization

Use the node structure to generate visual representations:
1. Extract nodes and edges from JSON
2. Render as directed graph (see [visualization_guide.md](./visualization_guide.md))
3. Create interactive web-based explorers

---

## Validation Walk-through

### Example 1: Skilled Worker Visa (Eligible)

**Applicant Profile:**
- Job offer: Yes, from approved employer
- CoS: Yes, valid
- Genuine vacancy: Yes
- Genuine employment: Yes (not third-party)
- Occupation: Software developer (higher skilled)
- Salary: £50,000
- Going rate: £45,000
- Part-time: No
- First CoS: After April 4, 2024
- English: Degree from US university
- Funds: £2,000 for 28+ days

**Path through tree:**
1. `start` → `check_switching_eligibility` (not applicable)
2. `has_approved_employer` (YES)
3. `has_certificate_of_sponsorship` (YES)
4. `check_genuine_vacancy` (appears_genuine)
5. `check_genuine_employment` (yes)
6. `check_guaranteed_salary_structure` (meets_requirement)
7. `check_part_time_eligibility` (meets_requirement)
8. `check_transitional_eligibility` (no - new applicant)
9. `check_occupation_eligibility` (higher_skilled)
10. `check_standard_salary_requirement` (PASS: £50k > max(£41,700, £45k))
11. `check_english_language` (exempt_nationality: USA)
12. `check_financial_requirement` (meets: £2,000 > £1,270)
13. **Result: ELIGIBLE**

### Example 2: Child Benefit (Deferred)

**Applicant Profile:**
- Child age: 10 (under 16)
- Child working: No
- Child receiving benefits: No
- Child not apprentice: Correct
- Claimant UK resident: Yes
- Claimant responsible: Yes (living with child)
- Other claimant: Yes, disputed (parents separated, both claim responsibility)

**Path through tree:**
1. `start` → `has_qualifying_child` (under_16)
2. `check_child_not_working_full_time` (yes)
3. `check_child_not_receiving_benefits` (yes)
4. `check_child_not_apprentice` (yes)
5. `check_uk_residency` (eligible_via_any_path)
6. `check_responsibility` (eligible_via_any_path)
7. `check_no_other_claimant` (disputed_multiple_claimants)
8. **Result: DEFERRED_TO_HMRC** (HMRC will arbitrate)

---

## Schema Version History

### v1.1 (Current - 2026-03-03)

**Enhancements:**
- Added `DEFERRED` result type for outcomes requiring external decision-making
- Enhanced `OutcomeNode` properties:
  - `hmrc_decision_criteria` array (for DEFERRED outcomes)
  - `required_evidence` array (for DEFERRED outcomes)
  - `reference` field (optional URI for all outcomes)
- Generalized schema title and description to support multiple government services
- Added validation rule requiring `reason` and `guidance` for DEFERRED outcomes

**Validated Specifications:**
- ✅ Skilled Worker Visa v1.2 (32 nodes)
- ✅ Child Benefit v1.2 (32 nodes)

### v1.0 (Initial Release)

**Features:**
- Core node types (9 types: boolean_question through outcome)
- Result types: ELIGIBLE, INELIGIBLE
- Required top-level fields: version, last_updated, source, description, decision_tree, constants
- Optional sections: validation_rules, external_references
- Path structures for multi_path_check nodes
- Result-specific validation (ELIGIBLE requires next_steps, INELIGIBLE requires reason/guidance)

---

## Specification Version History

### Skilled Worker Visa

**v1.2** (2026-03-03)
- Added part-time worker eligibility rules
- Clarified ISL salary requirements (100% going rate, no 80% discount)
- Added genuine vacancy assessment criteria
- **Stats:** 32 nodes, 90%+ coverage

**v1.1** (Previous)
- Added ISL route clarifications
- Enhanced PhD routes

**v1.0** (Initial)
- Complete basic eligibility criteria

### Child Benefit

**v1.2** (2026-03-03)
- Added DEFERRED outcome for HMRC arbitration
- Enhanced HICBC documentation (not an eligibility criterion)
- Documented unequal contribution allocation rules
- **Stats:** 32 nodes, 98% coverage (49/50 scenarios)

**v1.1** (Previous)
- Added education level definitions (approved vs. advanced)
- Enhanced apprenticeship regional rules
- Added 20-week extension logic
- Improved hospital linking rules

**v1.0** (Initial)
- Complete basic eligibility criteria
- 26 nodes, 64% coverage

---

## Maintenance

### When UK Policy Changes

**For Specification Updates:**
1. Identify affected nodes in the decision tree
2. Update node criteria, questions, or outcomes
3. Add new nodes if decision logic changes
4. Update `last_updated` date
5. Update `version` number (semantic versioning)
6. Create release notes documenting changes
7. Run validation tools to ensure schema conformance
8. Update test scenarios if needed

**For Schema Updates:**
1. Assess if new node types or outcome types are needed
2. Update schema version
3. Validate all existing specifications against new schema
4. Document breaking vs. non-breaking changes
5. Update this README with schema changes

**Version Control:**
- Use semantic versioning (major.minor.patch)
- Major: Breaking changes to structure
- Minor: New features, backward compatible
- Patch: Bug fixes, clarifications

### Quality Checks

**Before Release:**
```bash
# Validate against schema
python3 validate_specifications.py

# Check for orphan nodes
python3 check_orphan_nodes.py

# Verify test coverage
# (See test_cases directory)

# Review release notes
# Ensure all changes documented
```

---

## Completeness Verification

### Skilled Worker Visa v1.2

✅ All mandatory requirements (employer, CoS, occupation, salary, English, funds)  
✅ All salary routes (standard, healthcare/education, reduced options)  
✅ All English language paths (exemptions + proof methods)  
✅ Part-time worker rules (pro-rated going rate, non-pro-ratable threshold)  
✅ Genuine vacancy and employment checks  
✅ Special requirements (CQC for care workers)  
✅ Time limits documented for certain routes  
✅ Application fees and costs  
✅ External reference links for dynamic data  

### Child Benefit v1.2

✅ All child eligibility criteria (age, education, work status)  
✅ All residency paths (8 variations including Crown servants)  
✅ All responsibility paths (living with, contributing, maintenance)  
✅ Hospital and care time limits (12-week, 8-week with linking)  
✅ Education level definitions (approved vs. advanced)  
✅ Regional apprenticeship rules (England, Scotland, Wales variations)  
✅ 20-week extension rules for 16-17 year olds  
✅ HMRC arbitration for disputed claims  
✅ HICBC documentation (administrative, not eligibility)  

---

## Limitations

### Dynamic Data Not Included

The following are referenced but not embedded (they change frequently):

**Skilled Worker Visa:**
- List of eligible occupations (by SOC code)
- Going rates per occupation
- Immigration Salary List contents
- List of approved employers
- Specific NHS/education pay scales

**Child Benefit:**
- Current payment rates (£26.05/week eldest, £17.25/week additional)
- HICBC income thresholds (£60k-£80k)
- Country-specific residency agreements

These are referenced via `external_references` URLs or documented in `constants`.

### Out of Scope

**Skilled Worker Visa:**
- Extension and switching criteria (briefly referenced but not fully modeled)
- Dependant eligibility (separate criteria)
- Settlement/indefinite leave requirements
- Application process details (non-eligibility)

**Child Benefit:**
- Payment calculation (beyond basic rates)
- Tax Credit interactions
- Universal Credit interactions
- Child maintenance service coordination

---

## Tools & Utilities

### validate_specifications.py

**Purpose:** Validate specifications against schema

**Features:**
- Validates required top-level fields
- Checks decision_tree structure (root, nodes)
- Validates node types and required fields per type
- Validates outcome results (ELIGIBLE, INELIGIBLE, DEFERRED)
- Checks result-specific requirements (e.g., ELIGIBLE needs next_steps)
- Provides detailed error messages and warnings
- Statistics reporting (node counts, outcome breakdown)

**Usage:**
```bash
python3 validate_specifications.py
```

**Output:**
- ✅ VALIDATION PASSED / ❌ VALIDATION FAILED
- List of errors and warnings
- Node statistics per specification

### check_orphan_nodes.py

**Purpose:** Detect orphan nodes and dangling references

**Features:**
- Scans all node types for outgoing references
- Tracks root.next reference
- Identifies nodes defined but never referenced (orphans)
- Detects references to non-existent nodes (dangling references)
- Provides context for each orphan (type, question/description)
- Statistics reporting

**Usage:**
```bash
python3 check_orphan_nodes.py
```

**Output:**
- ✅ NO ORPHAN NODES / ❌ ORPHAN NODES DETECTED
- List of orphan nodes with context
- List of dangling references
- Node statistics (total, referenced, orphans)

---

## Project Reports

### Schema Validation Report
[SCHEMA_VALIDATION_REPORT.md](./SCHEMA_VALIDATION_REPORT.md)
- Comprehensive validation results for both specifications
- Schema feature coverage
- Node type usage analysis
- Outcome type breakdown

### Orphan Node Cleanup Report
[ORPHAN_NODE_CLEANUP_REPORT.md](./ORPHAN_NODE_CLEANUP_REPORT.md)
- Initial orphan detection (3 nodes found)
- Analysis of why nodes were orphaned
- Cleanup actions taken
- Final validation results

### Test Analysis Reports
- [Child Benefit Test Analysis](./CHILD_BENEFIT_TEST_ANALYSIS.md) - Coverage analysis for 50 test scenarios

---

## Additional Resources

### Specification-Specific Documentation

- **Child Benefit:** [CHILD_BENEFIT_README.md](./CHILD_BENEFIT_README.md) - Detailed guide to Child Benefit specification
- **Skilled Worker Visa:** This README (above sections cover SWV comprehensively)

### Release Notes

- [Skilled Worker Visa v1.2](./VERSION_1.2_RELEASE_NOTES.md)
- [Skilled Worker Visa v1.1](./VERSION_1.1_RELEASE_NOTES.md)
- [Child Benefit v1.2](./CHILD_BENEFIT_VERSION_1.2_RELEASE_NOTES.md)
- [Child Benefit v1.1](./CHILD_BENEFIT_VERSION_1.1_RELEASE_NOTES.md)

### Official Sources

**Skilled Worker Visa:**
- https://www.gov.uk/skilled-worker-visa
- https://www.gov.uk/skilled-worker-visa/eligibility
- https://www.gov.uk/government/publications/register-of-licensed-sponsors-workers

**Child Benefit:**
- https://www.gov.uk/child-benefit
- https://www.gov.uk/child-benefit/eligibility
- https://www.gov.uk/child-benefit-16-19

---

## Future Expansion

### Potential Additional Services

This schema and tooling can model other UK government services:

**Benefits:**
- Universal Credit
- Personal Independence Payment (PIP)
- State Pension
- Pension Credit

**Immigration:**
- Family Visa
- Student Visa
- Global Talent Visa
- Settlement/ILR

**Education:**
- Student Finance
- Free School Meals
- Education Maintenance Allowance (EMA)

**Housing:**
- Right to Buy
- Help to Buy
- Council Housing Priority

### Schema Extensions Needed

For future services, may require:
- New node types (e.g., `means_test`, `priority_scoring`)
- New outcome types (e.g., `PARTIAL`, `CONDITIONAL`)
- Enhanced path structures (weighted paths, priority ordering)
- Time-series support (eligibility windows, review dates)

---

## License

These specifications are based on UK Government information available under the **Open Government Licence v3.0**.

---

## Contact & Contributions

**For UK Policy Questions:**
- Skilled Worker Visa: https://www.gov.uk/contact-ukvi
- Child Benefit: https://www.gov.uk/government/organisations/hm-revenue-customs/contact/child-benefit

**For Technical Questions:**
- Review existing documentation in this directory
- Check release notes for recent changes
- Validate specifications using provided tools

**For Contributions:**
- Ensure all changes maintain schema conformance
- Run validation tools before submitting
- Document changes in release notes
- Update version numbers appropriately
- Add test scenarios for new edge cases
