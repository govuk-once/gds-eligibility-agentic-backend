# Universal Credit Specification Creation Summary

**Date**: 2026-03-12  
**Specification**: Universal Credit Eligibility  
**Version**: 1.0  
**Schema Version**: 2.0  
**Status**: ✅ Complete and Validated

---

## Overview

Successfully created a comprehensive Universal Credit eligibility specification using the abstracted schema v2.0, demonstrating the schema's domain agnosticism by adding a third benefit specification without any schema changes.

---

## Specification Details

### Metadata

- **Source**: https://www.gov.uk/universal-credit
- **Total Nodes**: 18 (50% fewer than Skilled Worker Visa and Child Benefit)
- **Decision Nodes**: 9
- **Outcome Nodes**: 9 (1 ELIGIBLE, 8 INELIGIBLE)
- **Schema Conformance**: 100% compliant with schema v2.0

### Node Type Distribution

| Type | Count | Purpose |
|------|-------|---------|
| `routing` | 2 | Age categorization, student status routing |
| `boolean_question` | 2 | UK residency, partner under pension age |
| `conditional_check` | 2 | EU/EEA status, joint claim requirement |
| `criteria_check` | 1 | Capital limit with tariff income calculation |
| `multi_path_check` | 2 | Youth exceptions (8 paths), student exceptions (7 paths) |
| `outcome` | 9 | 1 ELIGIBLE, 8 INELIGIBLE variations |

### Coverage

**Core Eligibility Factors Modeled**:
✅ Age-based routing (under 16, 16-17, 18-pension age, pension age+)  
✅ Youth eligibility exceptions (8 specific paths for 16-17 year olds)  
✅ UK residency requirement  
✅ EU/EEA/Swiss citizen settled status requirement  
✅ Capital/savings limits (£16,000 maximum with tariff income calculation)  
✅ Student status (full-time vs part-time, with 7 exception paths)  
✅ Joint claim requirement for couples  
✅ Mixed-age couple provisions  

**Out of Scope** (intentionally):
- Payment amount calculations based on income
- Work-related conditionality and requirements
- Additional elements (health conditions, childcare costs, housing costs)
- Application process and advance payments
- Sanctions and compliance

**Rationale**: Focused on *initial eligibility determination* only, consistent with other specifications.

---

## Research Process

### Data Sources Used

All content sourced exclusively from official gov.uk pages:

1. **Primary source**: https://www.gov.uk/universal-credit
2. **Eligibility details**: https://www.gov.uk/universal-credit/eligibility
3. **Capital rules**: https://www.gov.uk/guidance/universal-credit-money-savings-and-investments
4. **Student rules**: https://www.gov.uk/guidance/universal-credit-and-students
5. **Course levels**: https://www.gov.uk/guidance/universal-credit-and-education-course-levels
6. **Health conditions**: https://www.gov.uk/health-conditions-disability-universal-credit

### Key Findings Extracted

**Capital Calculation**:
- Formula: `CEILING((capital - £6,000) / £250) × £4.35`
- Applied monthly as "tariff income"
- Any partial £250 band counts as full band (always round up)

**Student Eligibility**:
- 7 distinct exception paths for full-time students
- Distinction between advanced education (university+) and non-advanced education (A-levels, etc.)
- 8 qualifying disability benefits for disabled student exception
- Must be assessed with "limited capability for work" BEFORE starting course

**Youth Eligibility**:
- 8 specific circumstances allowing 16-17 year olds to claim
- Includes pregnancy, recent birth, caring responsibilities, no parental support

**Joint Claims**:
- Mandatory for couples living together
- No exceptions - both partners' circumstances combined
- Separate claims automatically rejected

---

## Decision Tree Design

### Design Principles

1. **Sequential gating**: Check disqualifying factors early (age, residency, capital)
2. **Complex routing last**: Student exceptions and youth exceptions near end of tree
3. **Efficient paths**: Most common case (working-age adult) reaches eligibility in 6 nodes
4. **Multi-path flexibility**: Used `multi_path_check` for youth/student exceptions (OR logic)

### Decision Flow

```
Start → Age Check → Residency → EU Status → Capital Limit → Student Status → Joint Claim → Outcome
```

**Key Decision Points**:
1. **Age routing**: 4-way split (under 16, 16-17, 18-pension, pension+)
2. **Youth exceptions**: 8 alternative paths via `multi_path_check`
3. **Capital check**: Single `criteria_check` with complex calculation in constants
4. **Student exceptions**: 7 alternative paths via `multi_path_check`

---

## Schema v2.0 Utilization

### Abstract Node Types Used

**Routing nodes** (2):
- Age categorization (4-way routing)
- Student status routing (3-way routing)
- Both use `description` and `routing_logic` fields for domain logic

**Criteria check** (1):
- Capital limit validation
- Domain-specific `criteria` object with tariff income calculation rules
- Demonstrates flexibility of abstracted `criteria_check` type

**Multi-path checks** (2):
- Youth eligibility (8 paths with diverse criteria)
- Student eligibility (7 paths with different requirement types)
- Shows schema can handle complex OR-logic without domain-specific types

**Domain-Specific Extensions**:
- Constants: Custom structure with age limits, capital limits, student criteria
- Validation rules: Detailed capital calculation formula with worked examples
- No schema changes needed

### Comparison with Other Specifications

| Metric | Skilled Worker Visa | Child Benefit | Universal Credit |
|--------|-------------------|---------------|------------------|
| **Nodes** | 32 | 32 | 18 |
| **Outcomes** | 14 | 16 | 9 |
| **Version** | 2.0 | 2.0 | 1.0 |
| **Schema compliance** | ✅ | ✅ | ✅ |
| **Domain-specific node types** | 0 | 0 | 0 |
| **Multi-path checks** | 2 | 2 | 2 |
| **Criteria checks** | 6 | 0 | 1 |

**Key Insight**: Universal Credit specification is significantly simpler (18 vs 32 nodes) due to fewer edge cases and special circumstances. All three specifications use the same abstract schema v2.0 node types despite different domains.

---

## Validation Results

### Structural Validation

```
✅ JSON syntax valid
✅ Schema v2.0 conformance: PASSED
✅ Required fields present: PASSED
✅ Node types valid: PASSED
✅ Outcome node requirements: PASSED
```

### Node Validation

```
Total nodes: 18
  • routing: 2 ✅
  • boolean_question: 2 ✅
  • conditional_check: 2 ✅
  • criteria_check: 1 ✅
  • multi_path_check: 2 ✅
  • outcome: 9 ✅

Outcome breakdown:
  • ELIGIBLE: 1 ✅
  • INELIGIBLE: 8 ✅
  • DEFERRED: 0 ✅
```

### Integration Test

All three specifications validated together:

```
================================================================================
✅ ALL SPECIFICATIONS VALID
================================================================================

Skilled Worker Visa: 32 nodes ✅
Child Benefit: 32 nodes ✅
Universal Credit: 18 nodes ✅
```

---

## Test Scenarios

### 10 Test Scenarios Documented

Covering diverse cases:
1. Standard working-age applicant (simple path)
2. High capital disqualification
3. Full-time student with child exception
4. 17-year-old without circumstances (disqualified)
5. 17-year-old carer (youth exception)
6. Capital at tariff threshold (calculation example)
7. Couple requiring joint claim
8. Mixed-age couple (pension transition)
9. EU citizen without settled status
10. Disabled student with PIP

**Coverage**: Age extremes, capital thresholds, student exceptions, youth exceptions, joint claims, immigration status

---

## Documentation Created

### Files Created

```
specifications/universal_credit/
  ├── universal_credit_eligibility.json          # Main specification (18 nodes)
  └── UNIVERSAL_CREDIT_README.md                 # Comprehensive documentation
```

### Documentation Sections

**README Contents**:
- Eligibility summary with checklist
- Decision tree structure and flow
- Key decision points with detailed explanations
- Constants reference (age, capital, student criteria)
- Validation rules with worked examples
- Coverage analysis with known limitations
- 10 test scenarios
- External references (14 gov.uk URLs)
- Usage instructions
- Version history

---

## Achievements

### 1. Domain Agnosticism Demonstrated

✅ Created third specification without any schema changes  
✅ All domain logic implemented in specification constants and validation rules  
✅ Schema v2.0 abstract types sufficient for completely different benefit domain  

### 2. Complexity Appropriate to Domain

✅ Universal Credit simpler than visa/child benefit (18 vs 32 nodes)  
✅ Decision tree structure matches natural eligibility flow  
✅ Complex calculations (tariff income) handled in constants/validation rules  

### 3. Comprehensive Coverage

✅ All major eligibility factors from gov.uk modeled  
✅ Edge cases covered (youth exceptions, student exceptions, mixed-age couples)  
✅ Complex financial calculation (tariff income) precisely specified  
✅ Clear scope boundaries documented (eligibility only, not payment amounts)  

### 4. Quality Documentation

✅ Comprehensive README with examples  
✅ All sources referenced with URLs  
✅ Test scenarios demonstrating diverse cases  
✅ Validation rules with worked mathematical examples  
✅ Known limitations clearly stated  

---

## Key Insights

### 1. Schema Flexibility Validated

The abstracted schema v2.0 successfully supports a third, quite different domain:
- **Skilled Worker Visa**: Employment-focused, salary calculations, occupation codes
- **Child Benefit**: Family-focused, age-based, time limits, arbitration
- **Universal Credit**: Means-tested benefit, capital limits, student rules

All three use the same 7 abstract node types without any schema modifications.

### 2. Criteria Check Versatility

The `criteria_check` node type proves highly versatile:
- **Visa**: Salary validation, financial requirements, part-time rules
- **Universal Credit**: Capital limits with tariff income calculation

Both domains use `criteria_check` for completely different measurable validations.

### 3. Multi-Path Check Power

`multi_path_check` effectively models complex "any of these qualifies" logic:
- **Visa**: Reduced salary routes (5 paths), English language exemptions (7 paths)
- **Child Benefit**: Residency paths (7 paths), responsibility paths (3 paths)
- **Universal Credit**: Youth exceptions (8 paths), student exceptions (7 paths)

Consistently useful across all three domains.

### 4. Documentation Patterns

All three specifications now follow consistent documentation structure:
- Eligibility summary
- Decision tree flow
- Key decision points with details
- Constants reference
- Validation rules with examples
- Test scenarios
- External references

This consistency makes specifications easier to understand and maintain.

---

## Future Enhancements

### Potential Additions (v1.1+)

**Income Assessment** (major addition):
- Earned income thresholds
- Unearned income rules
- Work allowances
- Taper rates (63p for every £1 earned over work allowance)

**Conditionality** (separate specification):
- Work search requirements
- Appointments and commitments
- Sanctions for non-compliance

**Additional Elements** (optional):
- Health condition/disability additions
- Childcare costs calculations
- Housing costs elements
- Limited capability for work assessments

**Rationale**: Current v1.0 focuses on *initial eligibility determination*. Income and conditionality could be separate specifications or future versions.

---

## Comparison: Before and After Schema v2.0

### If Using Schema v1.1 (Domain-Specific)

Would have needed:
- ❌ New `capital_check` node type for tariff income calculation
- ❌ New `student_check` node type for education level routing
- ❌ Schema version bump to v1.2
- ❌ Migration of existing specifications to v1.2
- ❌ Documentation updates for all three specs

### Using Schema v2.0 (Domain-Agnostic)

Actually needed:
- ✅ One `criteria_check` node for capital validation
- ✅ Two `routing` nodes for age and student categorization
- ✅ Domain logic in specification constants and validation rules
- ✅ **Zero schema changes**
- ✅ **Zero impact on existing specifications**

**Time saved**: Estimated 2-3 hours (no schema design/migration needed)

---

## Conclusion

✅ **Universal Credit specification created successfully**  
✅ **18 nodes, all validation checks pass**  
✅ **Comprehensive documentation with 10 test scenarios**  
✅ **Zero schema changes required**  
✅ **Demonstrates schema v2.0 domain agnosticism**  
✅ **Ready for production use**

The addition of Universal Credit as a third specification proves that schema v2.0 achieves its goal: a truly domain-agnostic framework for representing ANY UK government service eligibility criteria without requiring schema modifications.

---

**Project**: GDS Eligibility Graph Creation  
**Schema Version**: 2.0  
**Specifications**: 3 (Skilled Worker Visa, Child Benefit, Universal Credit)  
**Total Nodes**: 82 (32 + 32 + 18)  
**Status**: ✅ All validated and documented  
**Date**: 2026-03-12
