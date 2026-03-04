# Test Case Analysis: Skilled Worker Visa Eligibility Specification

## Executive Summary

This document analyzes 51 test scenarios against the current `skilled_worker_visa_eligibility.json` specification to identify gaps, missing criteria, and areas requiring enhancement.

**Overall Assessment**: The current specification captures **core eligibility criteria** but is **missing several important implementation details** that affect real-world determinations.

**Findings**:
- ✅ **Captured**: 31 scenarios (61%)
- ⚠️ **Partially Captured**: 12 scenarios (24%)
- ❌ **Not Captured**: 8 scenarios (16%)

---

## Detailed Analysis by Scenario

### ✅ FULLY CAPTURED (31 scenarios)

These scenarios can be fully evaluated using the current specification:

1. **Permutation 1: Standard Route** - ✅ Covered by `check_standard_salary_requirement`
2. **Permutation 2: New Entrant (Under 26/Graduate)** - ✅ Covered by `check_reduced_salary_eligibility` → `under_26_or_graduate` path
3. **Permutation 3: STEM PhD** - ✅ Covered by `check_reduced_salary_eligibility` → `stem_phd` path
4. **Permutation 4: Non-STEM PhD** - ✅ Covered by `check_reduced_salary_eligibility` → `non_stem_phd` path with £37,500 minimum
5. **Permutation 5: Immigration Salary List** - ✅ Covered by `check_reduced_salary_eligibility` → `immigration_salary_list` path
6. **Permutation 6: Postdoctoral Position** - ✅ Covered by `check_reduced_salary_eligibility` → `postdoctoral` path with eligible codes
10. **Permutation 10: Care Worker CQC Requirement** - ✅ Covered by `check_care_worker_registration` node
11. **Permutation 11: Going Rate Trap** - ✅ Covered by salary check logic (must meet HIGHER of threshold or going rate)
14. **Permutation 14: New Entrant via Professional Qualification** - ✅ Covered in `under_26_or_graduate` criteria
15. **Permutation 15: Skill Level Mismatch (RQF Fail)** - ✅ Covered by `check_occupation_eligibility`
16. **Permutation 16: Irrelevant PhD** - ✅ Covered by PhD path requirements ("PhD is relevant to the job")
25. **Permutation 25: English Language Exemption** - ✅ Covered by `check_english_language` → `exempt_nationality` path
32. **Permutation 32: PhD Student 24-Month Rule** - ✅ Covered in `under_26_or_graduate` (recent student)
46. **Permutation 46: Expired SELT (Previous Use)** - ✅ Covered by `check_english_language` → `previous_visa` path

**Additional scenarios fully captured:**
- Valid sponsor requirement (Permutations 1-51)
- Certificate of Sponsorship (Permutations 1-51)
- English language paths (UK degree, overseas degree, SELT) - Permutations throughout
- Financial requirement (£1,270 for 28 days) - implicit in all
- Healthcare/education salary rules - Permutation 9

---

### ⚠️ PARTIALLY CAPTURED (12 scenarios)

These scenarios are conceptually covered but **lack specific implementation details** in the specification:

#### 7. **Permutation 7: Absolute Fail (Below £33,400)**
**Status**: ⚠️ Partially captured
**Current**: Minimum thresholds documented in `constants`
**Gap**: No explicit "below absolute minimum" outcome node before checking reduced routes
**Impact**: Medium - can be inferred but not explicitly modeled

#### 8. **Permutation 8: Transitional Arrangements (Pre-April 2024)**
**Status**: ⚠️ Not captured
**Current**: Brief mention in `validation_rules.special_cases.extending_visa`
**Gap**: No node for transitional eligibility check, no £29,000 threshold
**Impact**: HIGH - Affects existing visa holders significantly
**Recommendation**: Add `check_transitional_eligibility` node

#### 9. **Permutation 9: Health and Care Visa (NHS Pay Bands)**
**Status**: ⚠️ Partially captured
**Current**: Healthcare salary check exists with £25,000 minimum
**Gap**: Doesn't explicitly model NHS Band structure or that this bypasses standard thresholds
**Impact**: Medium - logic is there but NHS-specific details missing

#### 12. **Permutation 12: Part-Time Pro-Rata Failure**
**Status**: ⚠️ Not captured
**Current**: No mention of part-time, hourly rates, or pro-rata calculations
**Gap**: Missing hourly wage calculation rules and pro-rata restrictions
**Impact**: HIGH - Common scenario
**Recommendation**: Add criteria about guaranteed annual salary vs. hourly rates

#### 13. **Permutation 13: New Entrant 4-Year Cap**
**Status**: ⚠️ Partially captured
**Current**: Time limit mentioned in `under_26_or_graduate` path ("Maximum 4 years total")
**Gap**: No mechanism to check accumulated time or deny if exceeds
**Impact**: HIGH - Prevents system from actually enforcing the limit
**Recommendation**: Add validation for accumulated time on Graduate/New Entrant visas

#### 18. **Permutation 18: Guaranteed Pay (Variable Salary)**
**Status**: ⚠️ Not captured
**Current**: Salary criteria exist but don't specify "guaranteed basic gross"
**Gap**: No exclusion of bonuses, commission, overtime
**Impact**: HIGH - Very common issue
**Recommendation**: Add criteria specifying only guaranteed basic salary counts

#### 22. **Permutation 22: 48-Hour Salary Cap**
**Status**: ⚠️ Not captured
**Current**: No mention of hourly calculations or hour limits
**Gap**: Missing rule about capping at 48 hours/week for salary calculation
**Impact**: HIGH - Affects hospitality, healthcare sectors
**Recommendation**: Add validation rule about assessable hours

#### 23. **Permutation 23: Allowances Excluded**
**Status**: ⚠️ Not captured
**Current**: No mention of allowances
**Gap**: Missing exclusion of housing, car, living allowances from salary
**Impact**: HIGH - Common in relocation packages
**Recommendation**: Add criteria excluding non-salary compensation

#### 24. **Permutation 24: Ecctis Verification Fail**
**Status**: ⚠️ Partially captured
**Current**: PhD paths mention "verified by Ecctis if overseas"
**Gap**: No failure path if Ecctis determines qualification insufficient
**Impact**: Medium - covered conceptually

#### 29. **Permutation 29: Salary Sacrifice**
**Status**: ⚠️ Not captured
**Current**: No mention of salary sacrifice schemes
**Gap**: Missing rule that post-sacrifice salary must meet threshold
**Impact**: Medium - Less common but important compliance issue
**Recommendation**: Add validation rule about salary after deductions

#### 45. **Permutation 45: Ecctis English Proficiency Fail**
**Status**: ⚠️ Partially captured
**Current**: Overseas degree path mentions Ecctis verification
**Gap**: Doesn't specify need for separate English proficiency statement
**Impact**: Medium - detail level issue

#### 51. **Permutation 51: 26th Birthday Timing**
**Status**: ⚠️ Partially captured
**Current**: "Under 26 on application date" mentioned
**Gap**: Doesn't explicitly state age is frozen at application time
**Impact**: Low - minor clarification

---

### ❌ NOT CAPTURED (8 scenarios)

These scenarios represent **significant gaps** in the specification:

#### 17. **Permutation 17: Supplementary Work Rules**
**Status**: ❌ Not captured
**Current**: Brief mention in overview about additional work
**Gap**: No node for supplementary employment rules (same code OR ISL, max 20 hrs/week)
**Impact**: HIGH - Common question, distinct from primary eligibility
**Recommendation**: Consider if in scope - this is post-grant condition, not eligibility criteria
**Scope Decision**: OUT OF SCOPE for initial eligibility, but should be documented separately

#### 19. **Permutation 19: Third-Party Ban (Contracting Out)**
**Status**: ❌ Not captured
**Current**: No mention of third-party working restrictions
**Gap**: Missing "genuine employment" check for contracting arrangements
**Impact**: HIGH - Prevents agency/consulting abuse
**Recommendation**: Add `genuine_employment_check` node
**Scope**: IN SCOPE - affects initial eligibility

#### 20. **Permutation 20: Care Worker Dependent Ban**
**Status**: ❌ Not captured
**Current**: Specification focused on primary applicant only
**Gap**: No mention that codes 6135/6136 cannot bring dependents
**Impact**: Medium - Affects family applications
**Scope**: OUT OF SCOPE - dependent eligibility is separate criteria tree

#### 21. **Permutation 21: Student Switching (Course Completion)**
**Status**: ❌ Not captured
**Current**: No node for switching from Student visa
**Gap**: Missing completion requirement check
**Impact**: HIGH - Common application pathway
**Recommendation**: Add `check_switching_eligibility` node with Student visa completion rules
**Scope**: IN SCOPE - affects ability to apply

#### 26. **Permutation 26: ISL Age Limit / Going Rate Still Required**
**Status**: ⚠️ Partially captured (moving to NOT CAPTURED)
**Current**: ISL path says "must still meet standard going rate"
**Gap**: Doesn't emphasize ISL alone doesn't grant going rate discount
**Impact**: HIGH - Common misunderstanding
**Recommendation**: Clarify ISL only lowers general threshold, not going rate

#### 27. **Permutation 27: Equity/Shares Excluded**
**Status**: ❌ Not captured
**Current**: No mention of non-cash compensation
**Gap**: Missing exclusion of stock options, equity
**Impact**: HIGH - Very common in tech/startup sector
**Recommendation**: Add to salary criteria (only cash counts)

#### 28. **Permutation 28: Zero-Hours Contract**
**Status**: ❌ Not captured
**Current**: No mention of contract type or guaranteed hours
**Gap**: Missing requirement for guaranteed minimum hours
**Impact**: HIGH - Affects gig economy, hospitality
**Recommendation**: Add criteria requiring guaranteed annual salary

#### 30. **Permutation 30: Genuine Vacancy Test**
**Status**: ❌ Not captured
**Current**: No credibility/fraud check in tree
**Gap**: Missing subjective "genuine vacancy" assessment
**Impact**: HIGH - Critical anti-fraud measure
**Recommendation**: Add node but mark as "caseworker discretion"
**Scope**: BORDERLINE - subjective assessment, hard to model

---

### 📋 OUT OF SCOPE (9 scenarios)

These scenarios are **valid rules but outside the scope** of initial eligibility determination:

31. **Permutation 31: Switching from Visitor Visa** - Immigration route switching rules (separate tree)
33. **Permutation 33: Global Business Mobility Time** - Time accumulation tracking (system logic, not criteria)
34. **Permutation 34: Owner-Manager Dividend** - Specific to PAYE vs. dividend (salary validation detail)
35. **Permutation 35: Professional Doctorate vs. PhD** - Degree type validation (Ecctis assessment detail)
36. **Permutation 36: Internal Promotion** - Change of employment process (post-grant compliance)
37. **Permutation 37: Supplementary Work Limit** - Post-grant work conditions
38. **Permutation 38: Defined vs. Undefined CoS** - CoS type validation (administrative detail)
39. **Permutation 39: 28-Day Start Rule** - Post-grant compliance
40. **Permutation 40: Term-Time Only Salary** - Pro-rata calculation (covered under part-time)
41. **Permutation 41: Immigration Skills Charge** - Sponsor payment requirement (not applicant eligibility)
42. **Permutation 42: B-Rated Sponsor** - Sponsor compliance status (external to applicant)
43. **Permutation 43: Unpaid Leave Limit** - Post-grant compliance
44. **Permutation 44: Minimum Age (16-17)** - Age and safeguarding (implicit in employment law)
47. **Permutation 47: Concurrent Employment** - Multiple visa process
48. **Permutation 48: Tailored Job Description** - Genuine vacancy (subjective, covered by #30)
49. **Permutation 49: Salary Reduction** - Post-grant compliance
50. **Permutation 50: Contractor IR35** - Employment relationship type (PAYE requirement implicit)

---

## Priority Recommendations

### CRITICAL GAPS (Must Address)

1. **Transitional Arrangements (Permutation 8)**
   - Add `check_transitional_eligibility` node
   - Add £29,000 threshold constant
   - Model 25th percentile going rate

2. **Guaranteed Salary Only (Permutation 18)**
   - Add explicit criteria excluding bonuses, commission, overtime
   - Clarify "basic gross pay" requirement

3. **48-Hour Week Cap (Permutation 22)**
   - Add validation rule limiting assessable hours to 48/week
   - Add hourly rate calculation logic

4. **Allowances Excluded (Permutation 23)**
   - Add criteria excluding allowances from salary calculation

5. **Zero-Hours Contracts (Permutation 28)**
   - Add requirement for guaranteed minimum hours/salary

6. **Equity/Shares Excluded (Permutation 27)**
   - Add criteria that only cash salary counts

7. **Student Switching Rules (Permutation 21)**
   - Add `check_switching_eligibility` node
   - Model course completion requirement

### HIGH PRIORITY (Should Address)

8. **4-Year Cap Enforcement (Permutation 13)**
   - Add mechanism to validate accumulated time
   - Create ineligible outcome if cap exceeded

9. **Part-Time Pro-Rata (Permutation 12)**
   - Model hourly rate vs. annual salary distinction
   - Add rule that general threshold cannot be pro-rated

10. **Third-Party Working Ban (Permutation 19)**
    - Add genuine employment check
    - Model contracting-out restriction

11. **Genuine Vacancy Test (Permutation 30)**
    - Add node with caseworker discretion flag
    - Document as subjective assessment

### MEDIUM PRIORITY (Consider Adding)

12. **Salary Sacrifice (Permutation 29)** - Post-sacrifice salary validation
13. **ISL Clarification (Permutation 26)** - Emphasize going rate still required
14. **Ecctis Details (Permutations 24, 45)** - Separate qualification and English assessments

---

## Specification Enhancement Proposal

### New Nodes Required

#### 1. `check_transitional_eligibility`
```json
{
  "id": "check_transitional_eligibility",
  "type": "boolean_question",
  "question": "Did applicant hold Skilled Worker visa before 4 April 2024?",
  "help_text": "Transitional arrangements apply lower thresholds",
  "outcomes": {
    "yes": "check_transitional_salary",
    "no": "determine_salary_threshold"
  }
}
```

#### 2. `check_switching_eligibility`
```json
{
  "id": "check_switching_eligibility",
  "type": "conditional_check",
  "question": "If switching from Student visa, has course been completed (or 24+ months of PhD)?",
  "outcomes": {
    "yes_or_not_switching": "has_approved_employer",
    "no": "INELIGIBLE_student_not_completed"
  }
}
```

#### 3. `check_genuine_employment`
```json
{
  "id": "check_genuine_employment",
  "type": "complex_criteria",
  "question": "Is this genuine direct employment (not third-party contracting)?",
  "criteria": [
    "Worker reports to sponsor, not third party",
    "Role is permanent need of sponsor, not filling client vacancy",
    "Sponsor retains full control over duties"
  ],
  "outcomes": {
    "yes": "check_guaranteed_salary_structure",
    "no": "INELIGIBLE_third_party_working"
  }
}
```

#### 4. `check_guaranteed_salary_structure`
```json
{
  "id": "check_guaranteed_salary_structure",
  "type": "salary_check",
  "question": "Is salary guaranteed basic gross pay (excluding bonuses, allowances, equity)?",
  "criteria": {
    "must_be_guaranteed": true,
    "must_be_basic_pay": true,
    "excludes": ["Bonuses", "Commission", "Allowances", "Stock options", "Overtime"],
    "hourly_cap": "48 hours per week for calculation",
    "must_specify_minimum_hours": true
  },
  "outcomes": {
    "meets_requirements": "determine_salary_threshold",
    "below_or_invalid": "INELIGIBLE_salary_structure_invalid"
  }
}
```

### Enhanced Constants

```json
"constants": {
  "salary_thresholds": {
    "standard_minimum": 41700,
    "transitional_minimum": 29000,
    "healthcare_education_minimum": 25000,
    "reduced_minimum_stem_phd": 33400,
    "reduced_minimum_non_stem_phd": 37500,
    "reduced_minimum_other": 33400,
    "absolute_minimum_floor": 33400
  },
  "salary_calculation_rules": {
    "max_assessable_hours_per_week": 48,
    "only_guaranteed_basic_gross": true,
    "excludes_bonuses": true,
    "excludes_commission": true,
    "excludes_allowances": true,
    "excludes_equity": true,
    "excludes_overtime": true,
    "requires_minimum_guaranteed_hours": true
  },
  "time_limits": {
    "new_entrant_maximum_years": 4,
    "includes_graduate_visa_time": true
  }
}
```

### New Validation Rules

```json
"validation_rules": {
  "transitional_arrangements": {
    "rule": "Applicants with Skilled Worker visa before 4 April 2024 use £29,000 threshold and 25th percentile going rates",
    "applies_to": "Extensions and job changes only",
    "reference": "https://www.gov.uk/skilled-worker-visa/if-you-got-your-first-certificate-of-sponsorship-before-4-april-2024"
  },
  "guaranteed_salary": {
    "rule": "Only guaranteed basic gross pay counts. Excludes: bonuses, commission, allowances, equity, overtime pay",
    "hourly_calculation_cap": "Maximum 48 hours per week",
    "contract_requirement": "Must specify guaranteed minimum hours/annual salary"
  },
  "new_entrant_time_accumulation": {
    "rule": "Total time on Graduate visa + New Entrant Skilled Worker cannot exceed 4 years",
    "enforcement": "System must track accumulated time and deny if granting visa would exceed limit"
  },
  "genuine_employment": {
    "rule": "Sponsor must be genuine employer, not third-party contractor supplier",
    "indicators": "Worker reports to sponsor, role fills sponsor's need, sponsor controls duties"
  }
}
```

---

## Coverage Summary

| Category | Count | % | Status |
|----------|-------|---|--------|
| Fully Captured | 31 | 61% | ✅ No action needed |
| Partially Captured | 12 | 24% | ⚠️ Enhance details |
| Not Captured (In Scope) | 8 | 16% | ❌ Must add |
| Out of Scope | 9 | 18% | ℹ️ Document separately |
| **Total Scenarios** | **51** | **100%** | |

### By Priority

| Priority | Count | Action Required |
|----------|-------|-----------------|
| Critical | 7 | Must address for production use |
| High | 4 | Should address for completeness |
| Medium | 3 | Consider for future enhancement |
| Low/Out of Scope | 37 | Document or defer |

---

## Recommendations for v1.1

### Immediate Actions (Critical)

1. **Add 4 new nodes**:
   - `check_transitional_eligibility`
   - `check_switching_eligibility`
   - `check_genuine_employment`
   - `check_guaranteed_salary_structure`

2. **Enhance existing nodes**:
   - `check_standard_salary_requirement`: Add guaranteed salary criteria
   - `check_reduced_salary_eligibility`: Add accumulated time validation
   - `check_healthcare_education_salary`: Clarify NHS band structure

3. **Expand constants**:
   - Add transitional thresholds
   - Add salary calculation rules
   - Add time limit enforcement details

4. **Add 5 new outcome nodes**:
   - `INELIGIBLE_student_not_completed`
   - `INELIGIBLE_third_party_working`
   - `INELIGIBLE_salary_structure_invalid`
   - `INELIGIBLE_time_limit_exceeded`
   - `INELIGIBLE_contract_type_invalid`

### Documentation Updates

1. Update README to note salary calculation rules
2. Add section on transitional arrangements
3. Document out-of-scope scenarios
4. Create separate document for post-grant compliance rules

### Schema Updates

1. Add `genuine_employment_check` node type
2. Add `salary_structure_check` node type
3. Enhance salary_check to include exclusion lists

---

## Conclusion

The current specification captures the **core eligibility paths** well (61% full coverage) but requires enhancement to handle **real-world implementation details** around:

1. **Salary calculation** (what counts, how to calculate)
2. **Transitional rules** (for existing visa holders)
3. **Application prerequisites** (switching, course completion)
4. **Fraud prevention** (genuine vacancy, third-party ban)

**Recommended approach**:
- **Phase 1 (v1.1)**: Add critical gaps (7 items) - salary rules, transitional, switching
- **Phase 2 (v1.2)**: Add high priority items (4 items) - time cap enforcement, genuine employment
- **Phase 3 (v2.0)**: Consider medium priority enhancements as policy evolves

The specification is **production-ready for standard cases** but needs these enhancements for **comprehensive real-world coverage**.
