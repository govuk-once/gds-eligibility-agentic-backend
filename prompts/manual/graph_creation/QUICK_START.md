# Quick Start Guide

## What's Included

This directory contains a machine-readable representation of UK Skilled Worker Visa eligibility criteria:

📄 **skilled_worker_visa_eligibility.json** - Complete decision tree (439 lines)  
📄 **README.md** - Full documentation of structure and usage  
📄 **IMPLEMENTATION_SUMMARY.md** - Requirements verification and design decisions  
📄 **visualization_guide.md** - How to create graph visualizations  
📄 **simplified_flow_diagram.md** - Mermaid flowchart summary  
🐍 **validate_and_visualize.py** - Validation and visualization tool  

## Instant Usage

### 1. View the Simplified Flowchart
Open `simplified_flow_diagram.md` in any Mermaid-compatible viewer (GitHub, VS Code with Mermaid extension, or https://mermaid.live)

### 2. Validate the JSON
```bash
python3 validate_and_visualize.py
```

Expected output:
```
✓ JSON loaded successfully
✓ Structure validation passed
✓ Decision tree statistics:
  - Total nodes: 21
  - Total paths to outcomes: 28
✓ Validation complete!
```

### 3. Generate Graph (Optional)
Install graphviz library:
```bash
pip install graphviz
python3 validate_and_visualize.py
```

This creates `visa_eligibility_graph.png`

### 4. Explore the JSON Structure
```bash
# View the decision tree root
jq '.decision_tree.root' skilled_worker_visa_eligibility.json

# List all node IDs
jq '.decision_tree.nodes | keys' skilled_worker_visa_eligibility.json

# View eligibility outcome
jq '.decision_tree.nodes.ELIGIBLE' skilled_worker_visa_eligibility.json

# View all salary thresholds
jq '.constants.salary_thresholds' skilled_worker_visa_eligibility.json
```

## Key Concepts

### Decision Tree Structure
```
Start → Check Employer → Check CoS → Check Occupation → 
Check Salary → Check English → Check Funds → Outcome
```

### Node Types
- **Questions**: Boolean yes/no or multi-path checks
- **Checks**: Salary, financial, or complex criteria validation
- **Outcomes**: ELIGIBLE or INELIGIBLE (with reason)

### Eligibility Paths
**28 total paths** through the tree, including:
- 1 path to ELIGIBLE outcome
- 27 paths to 8 different INELIGIBLE outcomes

Each path represents a unique combination of circumstances.

## Common Use Cases

### For Developers - Build an Eligibility Checker
```python
import json

# Load rules
with open('skilled_worker_visa_eligibility.json') as f:
    rules = json.load(f)

# Start at root
current = rules['decision_tree']['root']
print(current['description'])

# Navigate to first question
first_question = rules['decision_tree']['nodes'][current['next']]
print(first_question['question'])

# User answers "yes" → follow outcome
next_node_id = first_question['outcomes']['yes']
# Continue until outcome node reached
```

### For Policy Experts - Verify Completeness
1. Open `IMPLEMENTATION_SUMMARY.md`
2. Check "Comparison with Official Guidance" table
3. Review "Requirements Verification" section
4. Examine simplified_flow_diagram.md for high-level flow

### For Analysts - Extract Statistics
```bash
# Count ineligible outcomes
jq '[.decision_tree.nodes[] | select(.result == "INELIGIBLE")] | length' \
  skilled_worker_visa_eligibility.json

# List all reduced salary paths
jq '.decision_tree.nodes.check_reduced_salary_eligibility.paths[].id' \
  skilled_worker_visa_eligibility.json

# Show English language exemptions
jq '.decision_tree.nodes.check_english_language.paths[] | 
    {id, description}' skilled_worker_visa_eligibility.json
```

## Understanding the Salary Logic

The most complex part of eligibility is salary calculation. Here's the simplified logic:

```
IF job is Healthcare/Education:
    Required = MAX(£25,000, national_pay_scale_rate)
    
ELSE IF meets standard requirements:
    Required = MAX(£41,700, going_rate)
    
ELSE IF eligible for reduced salary:
    Choose applicable route:
    • Immigration Salary List: MAX(£33,400, going_rate)
    • Under 26/Graduate: MAX(£33,400, 70% × going_rate)  
    • STEM PhD: MAX(£33,400, 80% × going_rate)
    • Non-STEM PhD: MAX(£37,500, 90% × going_rate)
    • Postdoc: MAX(£33,400, 70% × going_rate)
    
ELSE:
    INELIGIBLE - salary too low
```

See `validation_rules.salary_calculation` in the JSON for the formal specification.

## Key Decision Points

### 1. Occupation Eligibility
- **Higher skilled** → Proceed to salary check
- **Medium skilled** → Must be on Immigration Salary List OR Temporary Shortage List
- **Not eligible** → Cannot apply

### 2. Salary Routes (in order of preference)
1. Try standard: £41,700 or going rate (whichever higher)
2. If below, try healthcare/education: £25,000 + national pay scale
3. If below, try reduced routes: 5 alternatives with different minimums
4. If none apply → Ineligible

### 3. English Language (any one path)
7 different ways to qualify:
- Exempt nationality (17 countries)
- Healthcare professional exemption
- Previous visa proof
- UK qualifications (4 types)
- Overseas degree in English
- SELT test

### 4. Financial Requirement
£1,270 for 28 days, OR:
- In UK 12+ months with valid visa
- Employer certifies maintenance

## Quick Reference - Constants

| Item | Value |
|------|-------|
| Standard salary threshold | £41,700 |
| Healthcare/education minimum | £25,000 |
| Reduced salary minimum (most) | £33,400 |
| Reduced salary (non-STEM PhD) | £37,500 |
| Financial requirement | £1,270 |
| Holding period | 28 days |
| CoS validity | 3 months |
| English level required | B2 CEFR |

## Troubleshooting

### JSON won't load
Check syntax: `python3 -m json.tool skilled_worker_visa_eligibility.json`

### Validation fails
Review error messages - usually indicates:
- Broken node reference
- Missing required field
- Outcome node with outgoing edges

### Can't generate visualization
Install graphviz: `pip install graphviz`  
Or use Mermaid diagram in simplified_flow_diagram.md

### Want to modify the rules
1. Edit the JSON file
2. Run validation: `python3 validate_and_visualize.py`
3. Update `last_updated` field
4. Document changes in version control

## Next Steps

- **Understand structure**: Read README.md
- **Verify requirements**: Read IMPLEMENTATION_SUMMARY.md  
- **Create visualizations**: Follow visualization_guide.md
- **Integrate into system**: Use JSON as source of truth for eligibility logic
- **Keep updated**: Monitor https://www.gov.uk/skilled-worker-visa for policy changes

## Support

This representation is based on official UK Government guidance:
- Source: https://www.gov.uk/skilled-worker-visa
- License: Open Government Licence v3.0
- Last updated: 2026-03-02

For questions about UK visa policy, consult official Gov.UK resources or immigration advisors.

For questions about this implementation, refer to:
- README.md for structure documentation
- IMPLEMENTATION_SUMMARY.md for design decisions  
- visualization_guide.md for visualization options
