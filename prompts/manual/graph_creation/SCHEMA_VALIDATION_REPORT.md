# Schema Validation Report

**Date:** 2026-03-03  
**Schema Version:** v1.1  
**Validator:** validate_specifications.py

---

## Executive Summary

✅ **ALL SPECIFICATIONS CONFORM TO SCHEMA**

Both eligibility specifications successfully validate against `eligibility-schema.json` v1.1:

- ✅ `skilled_worker_visa_eligibility.json` v1.2
- ✅ `child_benefit_eligibility.json` v1.2

No schema enhancements were required. The schema v1.1 successfully models both specifications.

---

## Validation Results

### Skilled Worker Visa Eligibility v1.2

**Status:** ✅ PASSED

**Statistics:**
- Total nodes: 34
- Decision nodes: 18
- Outcome nodes: 16
  - ELIGIBLE: 1
  - INELIGIBLE: 15

**Schema Coverage:**
- ✅ All required top-level fields present
- ✅ Root node correctly typed as "start"
- ✅ All node IDs match their keys
- ✅ All node types are valid
- ✅ All outcome results are valid (ELIGIBLE, INELIGIBLE)
- ✅ Boolean questions have yes/no outcomes
- ✅ Routing nodes have descriptions and outcomes
- ✅ Salary/financial checks have criteria and outcomes
- ✅ ELIGIBLE outcomes have descriptions and next_steps
- ✅ INELIGIBLE outcomes have reasons and guidance

---

### Child Benefit Eligibility v1.2

**Status:** ✅ PASSED

**Statistics:**
- Total nodes: 33
- Decision nodes: 16
- Outcome nodes: 17
  - ELIGIBLE: 1
  - INELIGIBLE: 15
  - DEFERRED: 1 *(HMRC arbitration case)*

**Schema Coverage:**
- ✅ All required top-level fields present
- ✅ Root node correctly typed as "start"
- ✅ All node IDs match their keys
- ✅ All node types are valid
- ✅ All outcome results are valid (ELIGIBLE, INELIGIBLE, DEFERRED)
- ✅ Boolean questions have yes/no outcomes
- ✅ Routing nodes have descriptions and outcomes
- ✅ Complex criteria nodes have questions and outcomes
- ✅ ELIGIBLE outcomes have descriptions and next_steps
- ✅ INELIGIBLE outcomes have reasons and guidance
- ✅ DEFERRED outcome has reason and guidance

**Notable Feature:**
- First specification to use the **DEFERRED** outcome type
- DEFERRED outcome (`DEFERRED_TO_HMRC`) includes:
  - `hmrc_decision_criteria` array (5 criteria)
  - `required_evidence` array (6 evidence types)
  - Comprehensive guidance for disputed claims

---

## Schema v1.1 Features Successfully Validated

### Core Structure
- ✅ Required top-level fields (version, last_updated, source, description, decision_tree, constants)
- ✅ Root node structure
- ✅ Node map structure
- ✅ Optional validation_rules and external_references

### Node Types (9 types)
1. ✅ `start` - Root node
2. ✅ `boolean_question` - Yes/no questions
3. ✅ `multi_path_check` - Multiple alternative paths (OR logic)
4. ✅ `salary_check` - Salary validation with complex criteria
5. ✅ `financial_check` - Financial requirement validation
6. ✅ `occupation_check` - Occupation skill level checks
7. ✅ `conditional_check` - Questions that may not apply
8. ✅ `complex_criteria` - Multi-factor criteria evaluation
9. ✅ `routing` - Non-question routing logic
10. ✅ `outcome` - Terminal nodes with results

### Outcome Result Types (3 types)
1. ✅ `ELIGIBLE` - Applicant qualifies
2. ✅ `INELIGIBLE` - Applicant does not qualify
3. ✅ `DEFERRED` - External decision required (e.g., HMRC arbitration)

### Validation Rules
- ✅ ELIGIBLE outcomes require `description` and `next_steps`
- ✅ INELIGIBLE outcomes require `reason` and `guidance`
- ✅ DEFERRED outcomes require `reason` and `guidance`
- ✅ Boolean questions require `yes` and `no` outcomes
- ✅ All nodes require `id` and `type` fields
- ✅ Node IDs must match their object keys

---

## Schema Enhancements in v1.1 (Previously Applied)

The schema was previously enhanced to support both specifications:

### 1. DEFERRED Result Type
```json
"result": {
  "enum": ["ELIGIBLE", "INELIGIBLE", "DEFERRED"]
}
```

### 2. Enhanced OutcomeNode Properties
- `hmrc_decision_criteria` array - For DEFERRED outcomes
- `required_evidence` array - For DEFERRED outcomes
- `reference` field - Optional URI for all outcomes

### 3. DEFERRED Validation Rule
```json
{
  "if": {"properties": {"result": {"const": "DEFERRED"}}},
  "then": {
    "required": ["reason", "guidance"],
    "description": "DEFERRED outcomes must explain why external decision is needed"
  }
}
```

### 4. Generalized Schema Metadata
- Title: "UK Government Eligibility Criteria Decision Tree Schema"
- Description: Explicitly supports multiple services
- No longer Skilled Worker Visa specific

---

## Validator Tool

A custom Python validator was created: `validate_specifications.py`

**Features:**
- ✅ No external dependencies (pure Python 3)
- ✅ Validates required fields at all levels
- ✅ Type-specific validation for all 10 node types
- ✅ Outcome result validation (ELIGIBLE, INELIGIBLE, DEFERRED)
- ✅ Result-specific requirement checks
- ✅ Comprehensive statistics reporting
- ✅ Human-readable error messages

**Usage:**
```bash
python3 validate_specifications.py
```

**Output:**
- Per-specification validation results
- Error and warning lists
- Node count statistics
- Outcome type breakdown

---

## Conclusion

✅ **Schema v1.1 is sufficient to describe both specifications**

The eligibility schema successfully models:
- UK Skilled Worker Visa eligibility (immigration)
- UK Child Benefit eligibility (welfare)

Both specifications demonstrate:
- Complete conformance to schema structure
- Proper use of all required fields
- Correct node type usage
- Valid outcome result types
- Appropriate use of advanced features (DEFERRED outcomes)

**No further schema enhancements required at this time.**

---

## Next Steps (If Needed)

If future specifications require new features, consider:

1. **New node types** - For specialized decision logic
2. **New outcome types** - Beyond ELIGIBLE/INELIGIBLE/DEFERRED
3. **Enhanced metadata** - Service-specific constants or rules
4. **Versioning requirements** - Backward compatibility tracking

Current schema is production-ready and flexible enough for diverse government services.
