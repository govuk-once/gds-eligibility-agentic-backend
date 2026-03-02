# UK Skilled Worker Visa Eligibility - Simplified Flow

```mermaid
graph TB
    Start([Start: Skilled Worker Visa<br/>Eligibility Assessment])
    
    %% Employer & CoS checks
    Start --> HasEmployer{Has job offer from<br/>approved UK employer?}
    HasEmployer -->|Yes| HasCoS{Has Certificate<br/>of Sponsorship?}
    HasEmployer -->|No| IneligEmployer[❌ INELIGIBLE<br/>No approved employer]
    
    HasCoS -->|Yes| CheckOcc[Check if occupation<br/>is eligible]
    HasCoS -->|No| IneligCoS[❌ INELIGIBLE<br/>No Certificate of Sponsorship]
    
    %% Occupation eligibility
    CheckOcc -->|Higher Skilled| DetermineSalary((Determine<br/>salary route))
    CheckOcc -->|Medium Skilled| CheckLists{On Immigration Salary List<br/>OR Temporary Shortage List?}
    CheckOcc -->|Not Eligible| IneligOcc[❌ INELIGIBLE<br/>Occupation not eligible]
    
    CheckLists -->|Yes| DetermineSalary
    CheckLists -->|No| IneligMedium[❌ INELIGIBLE<br/>Medium skilled not on lists]
    
    %% Salary determination
    DetermineSalary -->|Healthcare/Education| HealthcareSal[Healthcare/Education Salary<br/>Min £25,000 + national pay scale]
    DetermineSalary -->|Standard| StandardSal[Standard Salary<br/>Min £41,700 or going rate,<br/>whichever is HIGHER]
    
    %% Healthcare path
    HealthcareSal -->|Meets| CareWorkerCheck{Care worker 6135/6136<br/>in England?}
    HealthcareSal -->|Below| IneligSal[❌ INELIGIBLE<br/>Salary too low]
    
    CareWorkerCheck -->|Yes, CQC registered<br/>OR Not applicable| CheckEng
    CareWorkerCheck -->|No, not registered| IneligCQC[❌ INELIGIBLE<br/>Not CQC registered]
    
    %% Standard salary path
    StandardSal -->|Meets| CheckEng
    StandardSal -->|Below| ReducedSalary{{Check reduced<br/>salary eligibility}}
    
    %% Reduced salary options
    ReducedSalary -->|Immigration Salary List:<br/>£33,400 + going rate| CheckEng
    ReducedSalary -->|Under 26/Graduate/Training:<br/>£33,400 + 70% going rate| CheckEng
    ReducedSalary -->|STEM PhD:<br/>£33,400 + 80% going rate| CheckEng
    ReducedSalary -->|Non-STEM PhD:<br/>£37,500 + 90% going rate| CheckEng
    ReducedSalary -->|Postdoctoral role:<br/>£33,400 + 70% going rate| CheckEng
    ReducedSalary -->|None apply| IneligSal
    
    %% English language
    CheckEng{{English language<br/>requirement}}
    CheckEng -->|Exempt nationality| CheckFin
    CheckEng -->|Healthcare professional<br/>with English assessment| CheckFin
    CheckEng -->|Previously proved<br/>in visa application| CheckFin
    CheckEng -->|UK school qualification| CheckFin
    CheckEng -->|UK degree in English| CheckFin
    CheckEng -->|Overseas degree in English<br/>verified by Ecctis| CheckFin
    CheckEng -->|SELT test at B2 level| CheckFin
    CheckEng -->|Does not meet| IneligEng[❌ INELIGIBLE<br/>English language requirement]
    
    %% Financial requirement
    CheckFin[Financial Requirement<br/>£1,270 for 28 days]
    CheckFin -->|Meets OR employer certifies<br/>OR in UK 12+ months| Eligible
    CheckFin -->|Does not meet| IneligFin[❌ INELIGIBLE<br/>Insufficient funds]
    
    %% Final outcome
    Eligible[✅ ELIGIBLE<br/>Can apply for Skilled Worker visa]
    
    %% Styling
    classDef eligible fill:#228B22,stroke:#000,stroke-width:2px,color:#fff
    classDef ineligible fill:#DC143C,stroke:#000,stroke-width:2px,color:#fff
    classDef check fill:#87CEEB,stroke:#000,stroke-width:2px
    classDef multi fill:#DDA0DD,stroke:#000,stroke-width:2px
    classDef salary fill:#FFA500,stroke:#000,stroke-width:2px
    classDef start fill:#90EE90,stroke:#000,stroke-width:2px
    
    class Start start
    class Eligible eligible
    class IneligEmployer,IneligCoS,IneligOcc,IneligMedium,IneligSal,IneligCQC,IneligEng,IneligFin ineligible
    class HasEmployer,HasCoS,CheckLists,CareWorkerCheck check
    class CheckEng,ReducedSalary multi
    class StandardSal,HealthcareSal salary
```

## Summary of Eligibility Criteria

### 1. Mandatory Requirements (All Must Be Met)
- ✓ Job offer from Home Office approved employer
- ✓ Certificate of Sponsorship from employer
- ✓ Eligible occupation (on approved list)
- ✓ Sufficient salary (various routes available)
- ✓ English language proficiency (B2 CEFR or exempt)
- ✓ Financial requirement (£1,270 for 28 days or exempt)

### 2. Salary Routes (One Must Be Met)

#### Standard Route
- £41,700 per year OR going rate for job, whichever is **HIGHER**

#### Healthcare/Education Route
- £25,000 per year AND national pay scale going rate
- Special: Care workers in England must have CQC-registered employer

#### Reduced Salary Routes (at least £33,400 unless stated)
1. **Immigration Salary List**: £33,400 + going rate
2. **Under 26/Graduate/Training**: £33,400 + 70% going rate (max 4 years)
3. **STEM PhD**: £33,400 + 80% going rate
4. **Non-STEM PhD**: £37,500 + 90% going rate
5. **Postdoctoral**: £33,400 + 70% going rate (specific codes only, max 4 years)

### 3. English Language (One Must Be Met)
1. National of exempt country (USA, Canada, Australia, etc.)
2. Healthcare professional with English assessment
3. Previously proved in UK visa application
4. UK school qualification (GCSE, A Level, etc.)
5. UK degree taught in English
6. Overseas degree taught in English (Ecctis verified)
7. SELT test at B2 CEFR level

### 4. Financial Requirement
- £1,270 held for 28 consecutive days, within 31 days of application
- **OR** exempt if: in UK 12+ months with valid visa, or employer certifies maintenance

## Key Decision Points

### Occupation Classification
- **Higher skilled**: Can apply directly
- **Medium skilled**: Must be on Immigration Salary List OR Temporary Shortage List
- **Not eligible**: Cannot apply for Skilled Worker visa

### Salary Comparison Logic
```
Required Salary = MAX(
    Threshold (£41,700 or reduced),
    Going Rate for occupation,
    Percentage of Going Rate (if using reduced route)
)
```

### Time Limits
- Graduate/Under 26/Postdoc reduced routes: **Maximum 4 years total** (including Graduate visa time)
- Standard/other routes: Can extend indefinitely as long as requirements met
- Settlement eligibility: After 5 years continuous residence

## External Data Sources

These lists are maintained by UK Government and change periodically:

- [Eligible occupations](https://www.gov.uk/government/publications/skilled-worker-visa-eligible-occupations)
- [Going rates by occupation](https://www.gov.uk/government/publications/skilled-worker-visa-going-rates-for-eligible-occupations)
- [Immigration Salary List](https://www.gov.uk/government/publications/skilled-worker-visa-immigration-salary-list)
- [Temporary Shortage List](https://www.gov.uk/government/publications/skilled-worker-visa-temporary-shortage-list)
- [Approved employers register](https://www.gov.uk/government/publications/register-of-licensed-sponsors-workers)
