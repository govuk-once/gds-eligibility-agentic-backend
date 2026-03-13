# Universal Credit Eligibility Specification

**Version**: 1.0  
**Last Updated**: 2026-03-12  
**Source**: https://www.gov.uk/universal-credit  
**Schema Version**: 2.0

---

## Overview

This specification provides a machine-readable representation of UK Universal Credit eligibility criteria in JSON format, conforming to the eligibility-schema.json v2.0.

Universal Credit is a monthly payment for people who are on a low income or out of work. It replaces six older benefits (Income Support, income-based Jobseeker's Allowance, income-related Employment and Support Allowance, Housing Benefit, Child Tax Credit, and Working Tax Credit).

---

## Eligibility Summary

To be eligible for Universal Credit, you must:

✅ **Age**: Be 18 or over (16-17 under special circumstances) and under State Pension age  
✅ **Residency**: Live in the UK (England, Scotland, Wales, or Northern Ireland)  
✅ **Immigration Status**: UK citizen, or EU/EEA/Swiss citizen with settled/pre-settled status  
✅ **Capital**: Have £16,000 or less in savings, capital, and investments  
✅ **Student Status**: Not be a full-time student (unless you meet specific exceptions)  
✅ **Joint Claim**: If living with partner, must make a joint claim together

---

## Decision Tree Structure

### High-Level Flow

```
Start
  ↓
Age Check (Under 16 / 16-17 / 18-Pension / Pension+)
  ↓
UK Residency Check
  ↓
EU/EEA/Swiss Status Check (if applicable)
  ↓
Capital/Savings Limit Check (£16,000 maximum)
  ↓
Student Status Check
  ↓
Joint Claim Requirement Check
  ↓
ELIGIBLE or INELIGIBLE outcomes
```

### Node Summary

**Total Nodes**: 18  
- **Routing nodes**: 2 (age categorization, student status routing)
- **Boolean questions**: 2 (UK residency, partner under pension age)
- **Conditional checks**: 2 (EU/EEA status, joint claim requirement)
- **Criteria checks**: 1 (capital limit with tariff income calculation)
- **Multi-path checks**: 2 (youth eligibility exceptions, student eligibility exceptions)
- **Outcome nodes**: 9 (1 ELIGIBLE, 8 INELIGIBLE)

---

## Key Decision Points

### 1. Age Eligibility

**Categories**:
- **Under 16**: Not eligible
- **Age 16-17**: Eligible only under special circumstances (8 specific paths)
- **Age 18 to State Pension age**: Proceed to residency check
- **State Pension age or over**: Only eligible if partner is under State Pension age

**16-17 Year Old Exceptions** (any ONE qualifies):
- Health condition/disability with medical evidence (fit note)
- Caring for someone receiving health/disability benefit
- Nearing end of life
- Responsible for a child
- Lives with eligible partner and responsible for child
- Pregnant (baby due in next 11 weeks)
- Had baby in last 15 weeks
- No parental support (not living with parents, not in local authority care)

### 2. Capital and Savings Limit

**Maximum Capital**: £16,000

**Tariff Income Calculation** (£6,000-£16,000):
- For every £250 (or part thereof) above £6,000, payment is reduced by £4.35 per month
- Formula: `CEILING((capital - £6,000) / £250) × £4.35`
- Examples:
  - £6,300 capital: (£300 ÷ £250 = 1.2 → 2) × £4.35 = **£8.70/month reduction**
  - £14,500 capital: (£8,500 ÷ £250 = 34) × £4.35 = **£147.90/month reduction**

**What Counts as Capital**:
- Cash, bank accounts, PayPal, digital-only accounts
- Savings accounts (bank, building society, credit union)
- ISAs (all types including Lifetime ISAs)
- Premium Bonds, stocks, shares, cryptoassets
- Property you own but don't live in (with exceptions)
- Trust funds, inheritance, redundancy pay
- Unspent benefits and income

**What DOESN'T Count**:
- Your main home (property you live in)
- Personal possessions
- Life insurance policies (not yet paid out)
- Funeral plan contracts
- Children's savings (in children's names)
- Business accounts (active businesses or closed within 6 months)
- Property that is main home of retired close relatives or former partner lone parent

### 3. Student Status

**General Rule**: Full-time students are NOT eligible for Universal Credit

**Full-Time Student Exceptions** (any ONE qualifies):
1. Age 21 or under in full-time non-advanced education without parental support
2. Responsible for a child (adopted or foster)
3. Lives with partner who is eligible for Universal Credit
4. Reached State Pension age and lives with younger partner
5. Received a Migration Notice letter
6. Disabled with limited capability for work (assessed BEFORE course start) AND receiving qualifying disability benefit
7. Studying full-time non-advanced education with no student loan/grant and available for work

**Part-Time Students**: Can claim if available for work

**Advanced vs Non-Advanced Education**:

| Non-Advanced (Eligible with Exceptions) | Advanced (Generally Not Eligible) |
|---------------------------------------|-----------------------------------|
| GCSE, AS/A level, T level | University degrees |
| NVQ levels 1-3 | Postgraduate qualifications |
| BTEC up to level 3 | NVQ level 4+ |
| Access to Higher Education | HNC, HND |
| International Baccalaureate | Foundation degrees |

**Qualifying Disability Benefits** (for disabled students):
- Personal Independence Payment (PIP)
- Disability Living Allowance (DLA)
- Attendance Allowance
- Armed Forces Independence Payment
- Adult Disability Payment (ADP) - Scotland
- Child Disability Payment (CDP) - Scotland
- Pension Age Disability Payment (PADP) - Scotland
- Scottish Adult Disability Living Allowance (SADLA)

### 4. Joint Claim Requirement

**Rule**: If you live with a partner, you MUST make a joint claim

**Combined Assessment**: Both partners' income and savings are added together

**No Exceptions**: Even if one partner is not eligible individually, must claim jointly

**Consequence**: Separate claims will be rejected

---

## Constants Reference

### Age Limits
- **Minimum age**: 18 (16 with special circumstances)
- **Maximum age**: Under State Pension age (varies by date of birth)
- Check your State Pension age: https://www.gov.uk/state-pension-age

### Capital Limits
- **Maximum capital**: £16,000
- **Lower tariff threshold**: £6,000
- **Tariff income rate**: £4.35 per month per £250 band
- **Tariff band size**: £250

### Assessment Period
- **Length**: 28 days (approximately monthly)
- **Payment frequency**: Monthly based on circumstances in each assessment period

### Student Income
- **Disregard**: £110 per assessment period for full-time students
- Student loans and maintenance grants count as income (minus disregard)

---

## Validation Rules

### Capital Calculation

**Rule**: Capital between £6,000-£16,000 generates tariff income that reduces payment

**Formula**: 
```
Monthly reduction = CEILING((capital - £6,000) / £250) × £4.35
```

**Key Principle**: Any remaining amount that is not a complete £250 counts as another full band (always round up)

**Examples**:
1. **£6,300 capital**:
   - (£6,300 - £6,000) / £250 = 1.2
   - Round up to 2 bands
   - Reduction: 2 × £4.35 = **£8.70/month**

2. **£14,500 capital**:
   - (£14,500 - £6,000) / £250 = 34
   - Exactly 34 bands
   - Reduction: 34 × £4.35 = **£147.90/month**

3. **£16,000 capital**:
   - (£16,000 - £6,000) / £250 = 40
   - Maximum 40 bands
   - Reduction: 40 × £4.35 = **£174.00/month**

### Joint Claim Rule

**Assessment**: Both partners' income and savings are combined  
**Exception**: None - even if one partner is not eligible, must claim jointly  
**Consequence**: Separate claims by partners living together will be rejected

### Student Eligibility

**General Rule**: Full-time students not eligible unless meet specific exceptions

**Part-Time Rule**: Part-time students can claim if available for work

**Student Income**: Student loans and grants count as income, with £110 per assessment period disregarded for full-time students

**Limited Capability for Work**: Must be assessed BEFORE starting course to qualify as disabled student

**Qualifying Benefits**: Disabled students must receive one of the 8 qualifying disability benefits listed

### Age 16-17 Eligibility

**Rule**: 16-17 year olds can only claim under specific circumstances

**Assessment**: Any ONE of the 8 listed circumstances is sufficient

---

## Coverage Analysis

### Eligibility Scenarios Covered

✅ **Age-based routing**: Under 16, 16-17, 18-pension age, pension age+  
✅ **Youth exceptions**: 8 specific paths for 16-17 year olds  
✅ **Residency**: UK residency requirement  
✅ **Immigration status**: EU/EEA/Swiss settled status requirement  
✅ **Capital limits**: £16,000 hard limit with tariff income calculation  
✅ **Student exceptions**: 7 specific paths for full-time students  
✅ **Joint claims**: Couples must claim together  
✅ **Mixed-age couples**: One partner at pension age, other under

### Known Limitations

⚠️ **Income thresholds**: This specification covers eligibility only, not payment amount calculations based on earned/unearned income  
⚠️ **Work requirements**: Conditionality and work-related requirements not modeled (search for work, attend appointments, etc.)  
⚠️ **Additional elements**: Health conditions, disability additions, childcare costs, housing costs not in eligibility determination  
⚠️ **Advance payments**: Application process details and advance payment eligibility not covered  
⚠️ **Sanctions**: Reduction or suspension of payments due to not meeting requirements not modeled

**Rationale**: This specification focuses on *initial eligibility determination* only. Payment amounts, conditionality, and ongoing compliance are separate processes handled after eligibility is established.

---

## Test Scenarios

### Scenario 1: Standard Working-Age Applicant
- Age: 25, UK resident, British citizen
- Savings: £4,000
- Not a student
- Single
- **Result**: ELIGIBLE

### Scenario 2: High Capital Disqualification
- Age: 30, UK resident
- Savings: £20,000 in ISAs
- **Result**: INELIGIBLE (capital over £16,000)

### Scenario 3: Full-Time Student Exception (Child)
- Age: 22, UK resident
- Full-time university student
- Responsible for 2-year-old child
- Savings: £3,000
- **Result**: ELIGIBLE (meets student exception)

### Scenario 4: 17-Year-Old Without Circumstances
- Age: 17, UK resident
- Not pregnant, no child, has parental support
- Lives with parents
- **Result**: INELIGIBLE (age 16-17 without qualifying circumstances)

### Scenario 5: 17-Year-Old Carer
- Age: 17, UK resident
- Caring for disabled parent receiving PIP
- Savings: £1,000
- **Result**: ELIGIBLE (meets youth carer exception)

### Scenario 6: Capital at Tariff Threshold
- Age: 35, UK resident
- Savings: £9,750
- Not a student, single
- **Result**: ELIGIBLE with £65.25/month reduction
  - (£9,750 - £6,000) / £250 = 15 bands
  - 15 × £4.35 = £65.25/month reduction

### Scenario 7: Couple - Joint Claim Requirement
- Partner A: Age 28, eligible, £2,000 savings
- Partner B: Age 30, eligible, £8,000 savings
- Living together
- **Result**: ELIGIBLE if claiming jointly (combined savings £10,000 → £69.60/month reduction)
- **Result**: INELIGIBLE if trying to claim separately

### Scenario 8: Mixed-Age Couple
- Partner A: Age 66 (State Pension age)
- Partner B: Age 62 (under State Pension age)
- Living together, combined savings £5,000
- **Result**: ELIGIBLE (can claim UC until both reach pension age)

### Scenario 9: EU Citizen Without Settled Status
- Age: 28, EU citizen
- Living in UK, no settled/pre-settled status
- Savings: £2,000
- **Result**: INELIGIBLE (no settled status)

### Scenario 10: Disabled Student
- Age: 24, UK resident
- Full-time university student (advanced education)
- Assessed with limited capability for work BEFORE starting course
- Receiving Personal Independence Payment (PIP)
- Savings: £4,000
- **Result**: ELIGIBLE (meets disabled student exception)

---

## External References

All eligibility criteria sourced from official gov.uk pages:

| Topic | URL |
|-------|-----|
| Main Universal Credit page | https://www.gov.uk/universal-credit |
| Eligibility criteria | https://www.gov.uk/universal-credit/eligibility |
| How to claim | https://www.gov.uk/how-to-claim-universal-credit |
| Apply online | https://www.gov.uk/apply-universal-credit |
| Money, savings & investments | https://www.gov.uk/guidance/universal-credit-money-savings-and-investments |
| Students guidance | https://www.gov.uk/guidance/universal-credit-and-students |
| Education course levels | https://www.gov.uk/guidance/universal-credit-and-education-course-levels |
| Health conditions & disability | https://www.gov.uk/health-conditions-disability-universal-credit |
| End of life claims | https://www.gov.uk/health-conditions-disability-universal-credit/claiming-end-of-life |
| State Pension age calculator | https://www.gov.uk/state-pension-age |
| Pension Credit (for pension age) | https://www.gov.uk/pension-credit |
| EU Settlement Scheme | https://www.gov.uk/settled-status-eu-citizens-families/eligibility |
| Benefits calculator | https://www.gov.uk/benefits-calculators |

---

## Usage

### JSON Structure

```json
{
  "$schema": "../../schemas/eligibility-schema.json",
  "version": "1.0",
  "decision_tree": {
    "root": { ... },
    "nodes": { ... }
  },
  "constants": { ... },
  "validation_rules": { ... },
  "external_references": { ... }
}
```

### Validation

```bash
cd ancillary_functionality
python3 validate_specifications.py
```

### Visualization

```bash
cd ancillary_functionality
python3 validate_and_visualize.py
```

---

## Version History

**v1.0** (2026-03-12):
- Initial release
- 18 nodes (9 decision nodes, 9 outcome nodes)
- Covers core eligibility determination: age, residency, capital limits, student status, joint claims
- Uses abstracted schema v2.0 node types
- All validation checks pass
- Based on official gov.uk guidance as of March 2026

---

## Notes for Developers

### Schema Compliance

This specification uses **schema v2.0** abstract node types:
- `routing`: Age categorization, student status routing
- `boolean_question`: Simple yes/no decisions
- `conditional_check`: Context-dependent questions (EU status, joint claims)
- `criteria_check`: Capital limit validation with complex calculation
- `multi_path_check`: Youth exceptions (8 paths), student exceptions (7 paths)
- `outcome`: Terminal nodes (1 ELIGIBLE, 8 INELIGIBLE variations)

### Domain-Specific Extensions

**Constants**: Fully custom structure with age limits, capital limits, student criteria, assessment period details

**Validation Rules**: Detailed formulas for capital calculation, joint claim assessment, student eligibility rules

**No Schema Changes Required**: All domain logic implemented using flexible schema v2.0 structures

---

**Specification maintained by**: GDS Eligibility Graph Creation Project  
**Schema version**: 2.0  
**Last validated**: 2026-03-12  
**Status**: ✅ Production-ready
