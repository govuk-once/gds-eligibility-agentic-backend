# Personal Independence Payment (PIP) Eligibility Specification

## Overview

This directory contains the machine-readable JSON specification for **Personal Independence Payment (PIP)** eligibility criteria. PIP is a UK government benefit that helps with extra living costs for people aged 16 or over who have long-term physical or mental health conditions or disabilities.

## Specification Details

- **Version**: 1.0
- **Last Updated**: 2026-03-13
- **Official Source**: https://www.gov.uk/pip
- **Geographic Coverage**: England and Wales only (Scotland has Adult Disability Payment; Northern Ireland has separate PIP administration)

## What is PIP?

Personal Independence Payment (PIP) is a tax-free benefit designed to help people with:
- Long-term health conditions or disabilities
- Difficulties with daily living activities
- Difficulties with mobility

PIP has **two components**, each with two rates:

### Daily Living Component
- **Standard rate**: £73.90/week (8-11 points)
- **Enhanced rate**: £110.40/week (12+ points)

Covers 10 activities: preparing food, eating and drinking, managing medicines, washing and bathing, using toilet, dressing and undressing, reading, managing money, socialising, talking/listening/understanding.

### Mobility Component
- **Standard rate**: £29.20/week (8-11 points)
- **Enhanced rate**: £77.05/week (12+ points)

Covers 2 activities: planning and following journeys, moving around physically.

**Key Feature**: You can receive one component, both components, or neither depending on your assessment scores.

## Eligibility Overview

To qualify for PIP, you must meet ALL of these criteria:

1. **Age**: 16+ and under State Pension age (exception: can claim over SPA if received PIP/ADP in last 12 months)
2. **Geography**: Living in England or Wales when applying (different systems for Scotland and Northern Ireland)
3. **Health Condition**: Have long-term physical or mental health condition or disability
4. **Duration**: Condition expected to last at least 12 months
5. **Difficulty Frequency**: Have difficulty with daily living or mobility more than 50% of days over 12 months
6. **Presence Test**: Present in Great Britain for 104 weeks out of last 156 weeks (exemptions available)
7. **Habitual Residence**: Habitually resident in Common Travel Area with settled intention
8. **Immigration Status**: Not subject to immigration control (unless sponsored immigrant with permission)
9. **No Conflicting Benefits**: Not receiving DLA, Attendance Allowance, or AFIP
10. **Not in Excluded Circumstances**: Not in certain institutional settings (prison, detention, residential education, foster care, etc.)

## Decision Tree Structure

The specification models PIP eligibility as a decision tree with 42 nodes:

- **19 decision nodes**: Route applicants through eligibility checks
- **23 outcome nodes**: 6 ELIGIBLE outcomes (different component combinations) + 17 INELIGIBLE outcomes

### Key Decision Points

1. **Geographic Eligibility**: Routes to Scotland (ADP) or Northern Ireland systems if applicable
2. **Abroad Eligibility**: Handles temporary absence, EU/EEA living, and Armed Forces
3. **Age Check**: Validates age requirements with State Pension age exception
4. **Health Condition & Duration**: Confirms long-term condition exists and meets 12-month threshold
5. **Difficulty Frequency**: Ensures difficulties occur >50% of the time
6. **Presence Test**: Checks 2 out of 3 years presence with 10 exemption categories
7. **Habitual Residence**: Validates settled intention in Common Travel Area
8. **Immigration Status**: Confirms right to claim public funds
9. **Benefit Conflicts**: Checks for mutually exclusive benefits
10. **Institutional Circumstances**: Handles hospital, care home, prison, education, etc.
11. **Daily Living Assessment**: Evaluates 10 activities against reliability criteria
12. **Mobility Assessment**: Evaluates 2 activities against reliability criteria

### Assessment Criteria (Complex)

PIP uses a **points-based assessment** with **reliability criteria**. For each activity, assessors check if the claimant can perform the task:

- **Safely**: Without likelihood of harm to self or others
- **To Acceptable Standard**: Good enough quality/outcome
- **Repeatedly**: As often as reasonably required, within and across days
- **In Reasonable Time**: No more than twice as long as non-disabled person

Each activity has descriptors with point values (0, 2, 4, 6, 8, 10, or 12 points). The descriptor that applies on **>50% of days** is chosen.

### Outcome Variations

The specification includes **6 ELIGIBLE outcomes** to handle all component combinations:

1. Both components at standard rate (£103.10/week)
2. Both components at enhanced rate (£187.45/week)
3. Daily living standard + mobility enhanced (£150.95/week)
4. Daily living enhanced + mobility standard (£139.60/week)
5. Mobility standard only (£29.20/week)
6. Mobility enhanced only (£77.05/week)

Additionally, **2 institutional ELIGIBLE outcomes** for mobility-only awards when in hospital/care home 28+ days.

## Key Features of PIP Specification

### 1. **Complex Multi-Component Structure**

Unlike binary benefits (eligible/not eligible), PIP can award:
- Neither component (ineligible)
- One component (daily living OR mobility)
- Both components (daily living AND mobility)
- Each component at two rates (standard or enhanced)

This creates **routing complexity** that required dedicated routing nodes (`route_daily_living_standard`, `route_daily_living_enhanced`, `route_mobility_standard`, `route_mobility_enhanced`) to correctly combine assessment results.

### 2. **Points-Based Assessment Cannot Be Fully Automated**

The specification includes `complex_criteria` nodes for daily living and mobility assessments. However, these nodes describe the **framework** rather than implementing the full assessment:

- **10 daily living descriptors** × multiple point values each = hundreds of possible paths
- **2 mobility descriptors** × multiple point values each = dozens of possible paths
- **Subjective judgment required**: Health professionals assess reliability criteria (safely, acceptable standard, repeatedly, reasonable time)

**Design Decision**: The specification represents the assessment as a single complex criteria check, with outcomes representing point bands (8-11 points, 12+ points, <8 points). Full descriptor-level modeling would require 100+ additional nodes and still couldn't capture subjective assessment.

### 3. **Institutional Circumstances Complexity**

PIP has **time-based rules** for institutional stays:
- Hospital/care home: Daily living component stops after 28 days, mobility continues
- Prison/detention: All PIP stops immediately
- Residential education/foster care: All PIP stops immediately
- **Linking rules**: Multiple stays within 4 weeks count toward 28-day limit

The specification uses:
- `check_institutional_circumstances` to filter applicants in institutions
- `check_institutional_details` routing node with 9 outcomes to handle variations
- Separate eligibility pathway (`check_mobility_difficulties_only`) for those only eligible for mobility component

### 4. **Geographic and Immigration Complexity**

PIP availability varies by location:
- **England/Wales**: PIP available
- **Scotland**: Adult Disability Payment (ADP) instead
- **Northern Ireland**: Separate PIP administration
- **Abroad**: Limited availability (temporary absence, EU/EEA with work connection for daily living only, Armed Forces)

Immigration status has **6 qualifying paths** (British/Irish, settled status, pre-settled status, refugee/humanitarian, right of abode, sponsored immigrant).

### 5. **Exemptions and Special Rules**

The specification models **10 exemption categories** for the presence test:
1. Terminal illness
2. Refugee/humanitarian protection
3. Ukraine evacuation
4. Afghanistan evacuation
5. Sudan evacuation
6. Middle East conflict evacuation
7. UK government evacuation advice
8. Humanitarian immigration route
9. Armed Forces connection

These exemptions are implemented as a `multi_path_check` node with OR logic (meeting any one exemption satisfies the requirement).

## Schema Compatibility Evaluation

### ✅ Schema Handles PIP Well

The current schema (v2.0) successfully models PIP eligibility with the following node types:

1. **`routing`**: Used for geographic determination, institutional details, and component combination routing
2. **`multi_path_check`**: Perfect for abroad eligibility (3 paths) and presence test exemptions (10 paths)
3. **`boolean_question`**: Used for straightforward yes/no checks (health condition, difficulty frequency, habitual residence, benefit conflicts, institutional circumstances)
4. **`conditional_check`**: Used for age eligibility (handles State Pension age exception)
5. **`complex_criteria`**: Used for daily living and mobility assessments (describes framework without full descriptor implementation)
6. **`outcome`**: 23 outcome nodes cover all ineligibility reasons and 6 component combination variants

### ⚠️ Limitations Encountered

#### 1. **Points-Based Assessment Not Fully Representable**

The schema cannot fully represent the PIP descriptor scoring system within the decision tree structure. Each of the 12 activities (10 daily living + 2 mobility) has 4-8 descriptors with point values, creating a combinatorial explosion:

- **Daily living**: ~60 descriptors total across 10 activities
- **Mobility**: ~12 descriptors total across 2 activities
- **Theoretical paths**: Hundreds of combinations

**Current approach**: Use `complex_criteria` node with `disclaimer` field to indicate that assessment is conducted by DWP health professionals. The decision tree represents **assessment categories** (8-11 points, 12+ points, <8 points) rather than **full descriptor evaluation**.

**Impact**: The specification is **navigable by humans/agents** but requires **external assessment** to determine point scores. This aligns with the real-world process (PIP claims require professional assessment).

#### 2. **Temporal/Time-Based Rules**

PIP has time-based eligibility rules:
- **28-day institutional rule**: Component suspension after consecutive days
- **Linking rules**: Multiple stays within 4-week gap count together
- **Temporary absence**: 13 weeks (or 26 weeks for medical treatment)

**Current schema handling**: These rules are documented in:
- `constants.institutional_time_limits` for threshold values
- `validation_rules.institutional_rules` for logic description
- Node `help_text` fields for user-facing explanations

**Limitation**: The schema doesn't have node types specifically for **time-based conditional logic**. Handled using `routing` nodes with `routing_logic` field, but this requires prose description rather than structured temporal logic.

**Impact**: Acceptable for current use case. Time tracking would be external system concern (claim management system would track admission dates).

#### 3. **Multi-Dimensional Outcome Space**

Most benefits have simple outcomes: ELIGIBLE or INELIGIBLE. PIP has:
- **2 components** (daily living, mobility)
- **2 rates each** (standard, enhanced)
- **= 9 possible outcomes** (neither, DL only standard, DL only enhanced, M only standard, M only enhanced, both standard, both enhanced, DL standard + M enhanced, DL enhanced + M standard)

**Current schema handling**: Created separate outcome nodes for each combination. Required intermediate `routing` nodes to combine component assessment results.

**Limitation**: The schema treats multi-component benefits as **multiple sequential decisions** rather than **parallel independent assessments**. This creates routing complexity.

**Alternative approach considered**: Add `components` field to outcome nodes with array of awarded components. Would reduce 6 ELIGIBLE outcomes to 1 ELIGIBLE outcome with component details in structured field. However, this would make outcome nodes **less human-readable** and would require custom logic to extract awarded amounts.

**Decision**: Kept separate outcome nodes for **clarity and human comprehension**. The slight routing complexity is acceptable trade-off.

## Schema Amendment Recommendations

Based on PIP modeling experience, consider these optional enhancements:

### 1. **Add `assessment` Node Type (Optional)**

For benefits with complex professional assessments (PIP, ESA, UC health assessments):

```json
{
  "type": "assessment",
  "id": "pip_daily_living_assessment",
  "description": "Professional assessment of daily living difficulties",
  "assessment_framework": {
    "activities": [...],
    "scoring_method": "descriptor_based_points",
    "reliability_criteria": ["safely", "acceptable_standard", "repeatedly", "reasonable_time"],
    "assessor": "DWP health professional"
  },
  "outcome_thresholds": {
    "standard_rate": {"min_points": 8, "max_points": 11},
    "enhanced_rate": {"min_points": 12}
  },
  "outcomes": {
    "standard_rate": "route_daily_living_standard",
    "enhanced_rate": "route_daily_living_enhanced",
    "below_threshold": "check_mobility_difficulties"
  }
}
```

**Benefit**: Explicitly flags nodes that require external professional assessment rather than applicant self-assessment.

**Trade-off**: Adds complexity for benefits that don't need it. Current `complex_criteria` with `disclaimer` field achieves similar purpose.

### 2. **Add `components` Field to Outcome Nodes (Optional)**

For multi-component benefits like PIP:

```json
{
  "type": "outcome",
  "result": "ELIGIBLE",
  "components": [
    {
      "name": "daily_living",
      "rate": "standard",
      "weekly_amount": 73.90
    },
    {
      "name": "mobility", 
      "rate": "enhanced",
      "weekly_amount": 77.05
    }
  ],
  "total_weekly_amount": 150.95,
  "next_steps": [...]
}
```

**Benefit**: Reduces 6 ELIGIBLE outcomes to 1 with structured component data. Easier to programmatically extract awarded amounts.

**Trade-off**: Less human-readable. Outcome descriptions become generic. Loses clarity about which specific combination was awarded.

### 3. **Add `temporal_condition` Field (Optional)**

For time-based eligibility rules:

```json
{
  "type": "conditional_check",
  "temporal_condition": {
    "type": "duration_threshold",
    "event": "hospital_admission",
    "threshold_days": 28,
    "linking_rule": "gaps_under_4_weeks_linked"
  }
}
```

**Benefit**: Structures time-based rules that currently live in prose descriptions.

**Trade-off**: Adds complexity. Would require specification of temporal logic grammar. Most benefits don't need this.

## Recommendation: **No Schema Changes Needed**

After modeling PIP, the **current schema v2.0 is sufficient** for the following reasons:

1. **`complex_criteria` node type** adequately handles assessment frameworks with disclaimers
2. **Multiple outcome nodes** maintain human readability for multi-component benefits
3. **Prose fields** (`help_text`, `routing_logic`, `disclaimer`, `criteria`) provide flexibility for edge cases
4. **`validation_rules` and `constants`** top-level objects handle complex business logic and time-based rules

**The schema achieves its goal**: Model eligibility decision trees that are **machine-readable, human-comprehensible, and faithful to official guidance**, while acknowledging that some decisions (like PIP assessment scoring) require **external professional judgment**.

### When Schema Changes Would Be Warranted

Consider amendments if:
1. **5+ specifications** need professional assessment nodes (not just PIP, ESA, UC - but also DLA, AA, Carer's Allowance assessments)
2. **3+ specifications** have multi-component award structures (PIP, UC - need more examples)
3. **Temporal logic patterns** repeat across many benefits (institutional stays, temporary absences, linking rules)

For now: **Schema v2.0 is production-ready for PIP and similar complex benefits**.

## Next Steps for Implementation

1. **Test Case Development**: Create test scenarios covering:
   - All 6 component combinations
   - Presence test exemptions (10 categories)
   - Institutional circumstances (9 variations)
   - Abroad eligibility paths
   - Immigration status paths

2. **Visualization**: Generate decision tree diagram (will be large due to 42 nodes)

3. **Integration Testing**: Validate that routing logic correctly combines daily living and mobility assessments

4. **Coverage Analysis**: Ensure all ineligibility reasons are captured with appropriate guidance

## Files in This Directory

- `personal_independence_payment_eligibility.json` - Main specification (v1.0)
- `PIP_README.md` - This file
- (Future) `PIP_TEST_ANALYSIS.md` - Test case coverage analysis
- (Future) `VERSION_1.1_RELEASE_NOTES.md` - When updates occur

## Contact & Resources

- **Official PIP Information**: https://www.gov.uk/pip
- **Citizens Advice PIP Guide**: https://www.citizensadvice.org.uk/benefits/sick-or-disabled-people-and-carers/pip/
- **PIP Assessment Guide (Official)**: https://www.gov.uk/government/publications/personal-independence-payment-assessment-guide-for-assessment-providers

## License

This specification is derived from official UK Government guidance published under the Open Government Licence v3.0.

---

**Document Version**: 1.0  
**Last Updated**: 2026-03-13
