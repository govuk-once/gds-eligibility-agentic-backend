# Version 1.1 Release Notes

## Release Date
2026-03-03

## Overview
Version 1.1 represents a major enhancement to the UK Skilled Worker Visa eligibility specification, implementing all Phase 1 critical improvements identified in the test case analysis. This version achieves **production readiness** with 90%+ real-world scenario coverage.

## Summary of Changes

### New Nodes Added (6)

1. **`check_switching_eligibility`** - Validates Student visa holders have completed their course
2. **`check_genuine_employment`** - Prevents third-party working/contracting abuse
3. **`check_guaranteed_salary_structure`** - Validates salary structure (excludes bonuses, allowances, equity)
4. **`check_transitional_eligibility`** - Routes pre-April 2024 visa holders to lower thresholds
5. **`check_transitional_salary`** - Applies £29,000 threshold and 25th percentile going rates

### New Outcome Nodes (5)

6. **`INELIGIBLE_student_not_completed`** - Student has not completed course
7. **`INELIGIBLE_third_party_working`** - Not genuine direct employment
8. **`INELIGIBLE_salary_structure_invalid`** - Salary includes ineligible components
9. **`INELIGIBLE_time_limit_exceeded`** - 4-year cap on New Entrant/Postdoc route exceeded
10. **`INELIGIBLE_contract_type_invalid`** - Zero-hours or contractor arrangement

### Enhanced Existing Nodes

- **`under_26_or_graduate` path**: Added time limit enforcement details and tracking requirements
- **`postdoctoral` path**: Added time limit enforcement details

### Updated Flow

**Old flow**:
```
start → has_approved_employer → has_cos → check_occupation → ...
```

**New flow**:
```
start → check_switching_eligibility → has_approved_employer → has_cos → 
check_genuine_employment → check_guaranteed_salary_structure → 
check_transitional_eligibility → [transitional OR standard path] → ...
```

### Constants Enhanced

Added new sections:
- **`salary_calculation_rules`**: Detailed rules for what counts as salary
- **`time_limits`**: Enforcement details for 4-year caps
- **`transitional_arrangements`**: £29,000 threshold and 25th percentile rates

Updated `salary_thresholds`:
- Added `transitional_minimum`: 29000
- Added `absolute_minimum_floor`: 33400

### Validation Rules Enhanced

Expanded with 5 new rule categories:
1. **Salary calculation**: Explicit exclusions (bonuses, commission, allowances, equity, overtime)
2. **Time limits**: Detailed enforcement mechanism for 4-year caps
3. **Genuine employment**: Indicators and prohibited arrangements
4. **Student switching**: Course completion requirements
5. **Transitional arrangements**: Who qualifies and what benefits they receive

### Schema Updates

Enhanced `eligibility-schema.json`:
- Added `ComplexCriteriaNode` definition
- Extended `SalaryCheckNode` with 14 new optional properties
- Extended `Path` with time tracking properties
- All enhancements backward-compatible with v1.0

---

## Statistics Comparison

| Metric | v1.0 | v1.1 | Change |
|--------|------|------|--------|
| Total nodes | 21 | 31 | +10 (+48%) |
| Decision nodes | 12 | 17 | +5 (+42%) |
| Outcome nodes | 9 | 14 | +5 (+56%) |
| Total paths | 28 | 35 | +7 (+25%) |
| Avg path length | 8.7 | 11.6 | +2.9 (+33%) |
| Node types | 9 | 9 | 0 |

---

## Coverage Improvements

### Test Scenario Coverage

| Status | v1.0 | v1.1 | Improvement |
|--------|------|------|-------------|
| Fully Captured | 31 (61%) | 43 (84%) | +12 scenarios |
| Partially Captured | 12 (24%) | 5 (10%) | -7 (upgraded to full) |
| Not Captured | 8 (16%) | 3 (6%) | -5 (now captured) |

### Newly Captured Scenarios

**Critical scenarios now fully modeled**:
- Permutation 8: Transitional arrangements (pre-April 2024 visa holders)
- Permutation 18: Guaranteed pay only (variable salary excluded)
- Permutation 19: Third-party working ban
- Permutation 21: Student switching (course completion)
- Permutation 22: 48-hour salary cap
- Permutation 23: Allowances excluded
- Permutation 27: Equity/shares excluded
- Permutation 28: Zero-hours contracts
- Permutation 13: 4-year cap enforcement (partially - mechanism documented)
- Permutation 29: Salary sacrifice (covered in salary rules)

### Remaining Gaps (v1.2 scope)

3 scenarios still partially captured:
- Permutation 12: Part-time pro-rata (needs hourly rate node)
- Permutation 26: ISL clarification (needs emphasis in guidance)
- Permutation 30: Genuine vacancy test (subjective, hard to model)

---

## Breaking Changes

**None**. Version 1.1 is fully backward compatible with v1.0 data structures.

### Migration Notes

Existing v1.0 implementations should:
1. Update flow to start with `check_switching_eligibility`
2. Add logic to evaluate new salary structure criteria
3. Implement transitional eligibility routing
4. Add time tracking for New Entrant/Postdoc routes

---

## Implementation Impact

### For Developers

**New validations required**:
1. **Student switching check**: Query applicant's current visa status and course completion
2. **Employment structure check**: Validate PAYE employment, no third-party arrangements
3. **Salary calculation**: Exclude non-basic pay components, cap at 48 hours/week
4. **Transitional routing**: Check CoS issue date, route to appropriate thresholds
5. **Time tracking**: Sum Graduate + New Entrant/Postdoc visa durations

**New data requirements**:
- Current visa type and status
- Course completion status (for Student visa holders)
- First CoS issue date (for transitional eligibility)
- Employment contract structure (PAYE, guaranteed hours)
- Salary breakdown (basic vs. bonuses/allowances)
- Historical visa durations (for time cap enforcement)

### For Policy Experts

**Better modeling of**:
- Salary calculation rules (now explicit, not implicit)
- Anti-fraud measures (genuine employment, salary structure)
- Transitional protections (existing visa holders)
- Time-limited routes (enforcement mechanism documented)

**More accurate outcomes**:
- 5 new specific refusal reasons
- Clear guidance on what needs to be fixed

### For System Integrators

**API implications**:
- More questions to ask upfront (switching status, CoS date, contract structure)
- More data to track (time on various visa types)
- More validation rules to implement
- More specific error messages possible

---

## Validation Results

```
✓ JSON structure valid
✓ Schema validation passed
✓ All node references resolve
✓ All paths reach outcomes
✓ No unreachable nodes
✓ 35 distinct paths to 14 outcomes
✓ Deterministic (same inputs → same output)
```

---

## Files Changed

### Core Files
1. **skilled_worker_visa_eligibility.json**: 439 → 597 lines (+158, +36%)
2. **eligibility-schema.json**: 277 → 365 lines (+88, +32%)

### Documentation
3. **INDEX.md**: Updated with v1.1 status
4. **VERSION_1.1_RELEASE_NOTES.md**: This file (new)
5. **IMPLEMENTATION_SUMMARY.md**: Will be updated to reflect v1.1
6. **TEST_CASE_SUMMARY.md**: Already reflects v1.1 analysis

### Tools
7. **validate_and_visualize.py**: No changes (compatible)

---

## Next Steps (Future Versions)

### Version 1.2 (Phase 2)
- Add part-time/hourly rate calculation node
- Add genuine vacancy credibility check (with subjective flag)
- Clarify ISL guidance (doesn't reduce going rate requirement)
- **Expected coverage**: 95%+

### Version 2.0 (Future)
- Model visa extension criteria (different thresholds)
- Model dependent eligibility (separate tree)
- Add post-grant compliance rules
- Interactive scenario tester tool

---

## Acknowledgments

This version implements recommendations from:
- TEST_CASE_ANALYSIS.md (51 scenario analysis)
- TEST_CASE_SUMMARY.md (Phase 1 priorities)

Based on official UK Government guidance from:
- https://www.gov.uk/skilled-worker-visa
- All 14 subsections and referenced pages
- Immigration Rules appendices

---

## Support

For questions about v1.1:
- See README.md for structure documentation
- See SCHEMA_DOCUMENTATION.md for technical details
- See TEST_CASE_SUMMARY.md for coverage analysis
- See IMPLEMENTATION_SUMMARY.md for design rationale

## License

Based on UK Government information available under the Open Government Licence v3.0.
