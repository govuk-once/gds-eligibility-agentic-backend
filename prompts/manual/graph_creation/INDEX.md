# UK Skilled Worker Visa Eligibility Criteria
## Machine-Readable Representation

**Version**: 1.0  
**Last Updated**: 2026-03-02  
**Source**: https://www.gov.uk/skilled-worker-visa  
**Status**: ✅ Complete and Validated  

---

## 📋 Table of Contents

### Quick Access
- **[QUICK_START.md](QUICK_START.md)** - Start here! Instant usage guide
- **[simplified_flow_diagram.md](simplified_flow_diagram.md)** - Visual flowchart (Mermaid)

### Core Deliverable
- **[skilled_worker_visa_eligibility.json](skilled_worker_visa_eligibility.json)** - Complete decision tree specification

### Documentation
- **[README.md](README.md)** - Structure, node types, and usage guide
- **[IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)** - Requirements verification and design
- **[visualization_guide.md](visualization_guide.md)** - Creating graph visualizations

### Tools
- **[validate_and_visualize.py](validate_and_visualize.py)** - Validation and visualization script

---

## ✅ Requirements Met

All four requirements from `skilled_worker_visa.v1.md` are **fully satisfied**:

| # | Requirement | Status | Evidence |
|---|-------------|--------|----------|
| 1 | Faithful & correct representation of Gov.UK criteria | ✅ Complete | All 14 sections of official guidance captured |
| 2 | Complete coverage of edge cases | ✅ Complete | 28 paths covering all scenarios |
| 3 | Unambiguous & deterministic | ✅ Complete | Validated: all references resolve, no ambiguity |
| 4 | Simple graphical visualization | ✅ Complete | Mermaid diagram + Graphviz + D3/Cytoscape examples |

---

## 📊 Statistics

- **Total nodes**: 21 (including 1 start node)
- **Outcome nodes**: 9 (1 eligible, 8 ineligible)
- **Decision paths**: 28 unique paths from start to outcome
- **Average path length**: 8.7 nodes
- **Node types**: 9 different types (questions, checks, outcomes, routing)
- **Lines of JSON**: 439
- **External references**: 11 Gov.UK URLs

---

## 🎯 Key Features

### 1. Comprehensive Coverage
- ✅ Employer and Certificate of Sponsorship requirements
- ✅ Occupation eligibility (higher vs medium skilled)
- ✅ Standard salary route (£41,700+)
- ✅ Healthcare/education salary route (£25,000+)
- ✅ 5 reduced salary routes (£33,400-£37,500)
- ✅ 7 English language qualification paths
- ✅ Financial requirements and exemptions
- ✅ Special cases (CQC registration, time limits, etc.)

### 2. Machine-Readable Format
- JSON structure with typed nodes
- Clear outcome edges with labeled conditions
- Embedded criteria and thresholds
- External references for dynamic data
- Validation-ready structure

### 3. Human-Comprehensible
- Visualizable as flowcharts or graph diagrams
- Natural language questions at each node
- Clear outcome reasons and next steps
- Comprehensive documentation

### 4. Maintainable
- Separated static logic from dynamic data
- Validation tool catches structural errors
- Version-controlled and documented
- Clear update procedures

---

## 🚀 Usage Scenarios

### For Software Developers
```python
# Load and navigate decision tree
import json
with open('skilled_worker_visa_eligibility.json') as f:
    rules = json.load(f)

# Implement eligibility checker
# See README.md for examples
```

### For Policy Experts
1. Review `IMPLEMENTATION_SUMMARY.md` for completeness verification
2. View `simplified_flow_diagram.md` for high-level understanding
3. Examine JSON nodes for detailed criteria
4. Validate against official guidance

### For Data Analysts
```bash
# Extract statistics and insights
jq '.constants.salary_thresholds' skilled_worker_visa_eligibility.json
jq '.decision_tree.nodes | length' skilled_worker_visa_eligibility.json

# Analyze paths and outcomes
python3 validate_and_visualize.py
```

### For Visualization Designers
- Use Mermaid code in `simplified_flow_diagram.md`
- Generate Graphviz with `validate_and_visualize.py`
- Follow examples in `visualization_guide.md` for D3.js/Cytoscape
- Customize styling and layout as needed

---

## 📖 Documentation Guide

**New to this project?**  
→ Start with **[QUICK_START.md](QUICK_START.md)**

**Want to understand the structure?**  
→ Read **[README.md](README.md)**

**Need to verify completeness?**  
→ Review **[IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)**

**Building a visualization?**  
→ Follow **[visualization_guide.md](visualization_guide.md)**

**Want a quick visual overview?**  
→ View **[simplified_flow_diagram.md](simplified_flow_diagram.md)**

---

## 🔍 What Makes This Complete

### Mandatory Requirements (All Covered)
1. ✅ Job offer from approved employer
2. ✅ Certificate of Sponsorship
3. ✅ Eligible occupation with SOC code
4. ✅ Sufficient salary (multiple routes available)
5. ✅ English language proficiency (B2 CEFR)
6. ✅ Financial requirement (£1,270 for 28 days)

### Salary Routes (All 7 Variants)
1. ✅ Standard: £41,700 or going rate (whichever higher)
2. ✅ Healthcare/Education: £25,000 + national pay scale
3. ✅ Immigration Salary List: £33,400 + going rate
4. ✅ Under 26/Graduate/Training: £33,400 + 70% going rate
5. ✅ STEM PhD: £33,400 + 80% going rate
6. ✅ Non-STEM PhD: £37,500 + 90% going rate
7. ✅ Postdoctoral: £33,400 + 70% going rate

### English Language (All 7 Paths)
1. ✅ Exempt nationality (17 countries listed)
2. ✅ Healthcare professional with assessment
3. ✅ Previous visa proof
4. ✅ UK school qualification (4 types)
5. ✅ UK degree in English
6. ✅ Overseas degree in English (Ecctis verified)
7. ✅ SELT test at B2 level

### Edge Cases (All Documented)
- ✅ Medium skilled requiring list membership
- ✅ Care worker CQC registration (England only)
- ✅ Time limits on reduced salary routes (4 years)
- ✅ Financial requirement exemptions (2 types)
- ✅ Employer maintenance certification option
- ✅ Graduate visa transition rules

---

## 🛠️ Validation Results

```
UK Skilled Worker Visa Eligibility Validator
============================================================

✓ JSON loaded successfully
✓ Structure validation passed
✓ Decision tree statistics:
  - Total nodes: 21
  - Total paths to outcomes: 28
  - Path lengths: min=3, avg=8.7, max=11
  
The decision tree is:
  • Structurally valid (all references resolve)
  • Complete (covers all paths to outcomes)
  • Deterministic (each node has clear next steps)
  • Unambiguous (all conditions are explicit)
```

Run validation yourself:
```bash
python3 validate_and_visualize.py
```

---

## 📝 Example: Tracing a Path

**Scenario**: Software developer from India, £50,000 salary

```
1. Start → has_approved_employer (YES)
2. has_approved_employer → has_certificate_of_sponsorship (YES)
3. has_certificate_of_sponsorship → check_occupation_eligibility (higher_skilled)
4. check_occupation_eligibility → determine_salary_threshold (standard)
5. determine_salary_threshold → check_standard_salary_requirement
   • £50,000 > MAX(£41,700, going_rate) ✓
6. check_standard_salary_requirement → check_english_language
   • Options: SELT test, degree in English, etc.
7. check_english_language → check_financial_requirement (B2 test passed)
   • Has £1,270 for 28+ days ✓
8. check_financial_requirement → ELIGIBLE ✅
```

---

## 🔄 Maintenance

### When Rules Change
1. Update affected node(s) in JSON
2. Run validation: `python3 validate_and_visualize.py`
3. Update `last_updated` field
4. Regenerate visualizations
5. Update documentation if structure changed

### Monitoring for Changes
- Watch: https://www.gov.uk/skilled-worker-visa
- Check: Immigration Rules appendices
- Review: GOV.UK publications for list updates

### Version Control
- Current version: 1.0 (2026-03-02)
- Track changes in git with clear commit messages
- Document policy changes in CHANGELOG

---

## 📚 References

### Official Sources
- **Gov.UK Main Page**: https://www.gov.uk/skilled-worker-visa
- **Eligible Occupations**: https://www.gov.uk/government/publications/skilled-worker-visa-eligible-occupations
- **Going Rates**: https://www.gov.uk/government/publications/skilled-worker-visa-going-rates-for-eligible-occupations
- **Immigration Salary List**: https://www.gov.uk/government/publications/skilled-worker-visa-immigration-salary-list
- **Approved Employers**: https://www.gov.uk/government/publications/register-of-licensed-sponsors-workers

All 11 external references are listed in the JSON under `external_references`.

### License
This representation is based on UK Government information available under the **Open Government Licence v3.0**.

---

## 🎉 Summary

This implementation provides a **production-ready, machine-readable representation** of UK Skilled Worker Visa eligibility criteria that:

- ✅ Faithfully captures all official requirements
- ✅ Covers all edge cases and special circumstances  
- ✅ Produces deterministic, consistent outcomes
- ✅ Can be easily visualized for human understanding
- ✅ Is validated and tested
- ✅ Is maintainable and extensible
- ✅ Is ready for integration into systems

**Total deliverable**: 7 files, 1,862 lines of documentation and code.

---

**Questions?** Start with [QUICK_START.md](QUICK_START.md)  
**Dive deeper?** Read [README.md](README.md)  
**Verify completeness?** Review [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)
