# Analysis

This directory contains Jupyter notebooks that analyse the accuracy and reliability of a Child Benefit eligibility agent (claude-sonnet-4-5) on test cases involving **indeterminate** outcomes — situations where the correct answer cannot be determined from the information provided.

Each eligibility assessment is per-child (a family can have multiple children, each potentially with a different eligibility status). The three possible outcomes are:

- **ELIGIBLE** — the child is eligible for Child Benefit
- **INELIGIBLE** — the child is not eligible for Child Benefit
- **INDETERMINATE** — eligibility cannot be determined from the available information (e.g. a required fact is unknown)

The least desirable failure mode in all experiments is classifying an `ELIGIBLE` or `INDETERMINATE` child as `INELIGIBLE`, as this would discourage genuine applicants from claiming. The most common (and more acceptable) failure mode is classifying an `INDETERMINATE` child as `ELIGIBLE`, as the outcome is merely that someone applies and is then denied.

Test cases are categorised into three reliability buckets across repeated runs:

- **Always Passes** — the agent gives the correct answer on every run
- **Flaky** — the agent gives the correct answer on some runs but not all
- **Systematic Fail** — the agent never gives the correct answer

---

## Notebooks

### `explore_reliability-indeterminacy.ipynb` — Conversational pipeline, free-text rules

**Hypothesis:** `indeterminacy_concat_cases_reruns`
**Model:** claude-sonnet-4-5
**Prompt:** `Accuracy-ChildBenefit-indeterminacy-v3.md` (Combined indeterminacy cohort)
**Runs:** 6 runs × 199 test cases = 1,742 per-child assessments

**Overall accuracy:** ~89.9%

**Reliability summary (199 test cases):**

| Category        | Cases |
|-----------------|-------|
| Always Passes   | 78    |
| Flaky           | 99    |
| Systematic Fail | 22    |

**Key findings:**

- The most common failure mode is classifying `INDETERMINATE` children as `ELIGIBLE`. This is considered the more acceptable failure mode, as it leads to an application being made and then denied rather than discouraging a potentially eligible applicant.
- 100 out of 1,742 per-child assessments fell into the least desirable category (`ELIGIBLE` or `INDETERMINATE` classified as `INELIGIBLE`).
- A relatively high flakiness rate (99 flaky cases vs 78 always-passing cases) suggests significant non-determinism in the pipeline.

**Next steps identified:**

- Further analysis to identify commonalities amongst failure modes.
- Control for "actor hallucination" by running the facts-bundle approach (without an actor agent).
- Investigate the effect of providing rules in a structured manner.

---

### `explore_reliability-indeterminacy-factsBundle.ipynb` — Facts-bundle pipeline, free-text rules

**Hypothesis:** `facts_bundle_indeterminacy_concat_cases`
**Model:** claude-sonnet-4-5
**Prompt:** `Accuracy-ChildBenefit-factsBundle-indeterminacy-v1.md` (Other Prompt)
**Runs:** 6 runs × 199 test cases = 1,742 per-child assessments

**Overall accuracy:** ~89.9%

**Reliability summary (199 test cases):**

| Category        | Cases |
|-----------------|-------|
| Always Passes   | 145   |
| Flaky           | 43    |
| Systematic Fail | 11    |

**Key findings:**

- The overall accuracy is the same as the conversational pipeline (~89.9%), but the reliability profile is substantially better: 145 cases always pass vs 78 in the conversational pipeline.
- The facts-bundle approach (bypassing the actor agent and presenting facts directly) significantly reduces flakiness and systematic failures.
- This suggests that many failures in the conversational pipeline were due to **elicitation failure** or **actor hallucination** rather than the judge/evaluator agent itself misidentifying eligibility.
- The remaining failures (11 systematic, 43 flaky) are more likely due to the agent genuinely misidentifying or hallucinating on the underlying eligibility rules.
- The least desirable failure mode (`ELIGIBLE`/`INDETERMINATE` classified as `INELIGIBLE`) accounts for 45 out of 1,742 per-child assessments — a notable improvement over the conversational pipeline.

**Next steps identified:**

- Further analysis to identify commonalities amongst failure modes.
- Investigate the effect of providing rules in a structured manner.

---

### `explore_reliability-indeterminacy-structuredRules.ipynb` — Conversational pipeline, structured rules

**Hypothesis:** `structured_spec_conversational_reruns`
**Model:** claude-sonnet-4-5
**Prompt:** `StructuredSpecification-ChildBenefit-v2.md` (Structured spec with indeterminacy)
**Runs:** 6 runs × 199 test cases = 1,742 per-child assessments

**Overall accuracy:** ~73.2%

**Reliability summary (199 test cases):**

| Category        | Cases |
|-----------------|-------|
| Always Passes   | 87    |
| Flaky           | 77    |
| Systematic Fail | 35    |

**Key findings:**

- The overall accuracy is significantly lower than the free-text rule conversational pipeline (~73.2% vs ~89.9%).
- The structured rules conversational approach also has a worse reliability profile, with more systematic failures (35 vs 22) and a higher flaky rate relative to always-passing cases.
- A notable and **less desirable** failure mode emerges: cases that should be `INDETERMINATE` are classified as `INELIGIBLE` by the agent. This is worse than the free-text failure mode (which tends towards over-classifying as `ELIGIBLE`) because it could discourage potentially eligible applicants from applying.
- Further analysis of agent reasoning in the raw data is needed to establish why structured rules perform worse than free-text rules in the conversational setting.

**Next steps identified:**

- Further analysis to identify commonalities amongst failure modes.
- Control for actor hallucination by running the structured rules in a facts-bundle setting.

---

### `explore_reliability-indeterminacy-structuredRules-factBundle.ipynb` — Facts-bundle pipeline, structured rules

**Hypothesis:** `structured_spec_factBundle_reruns`
**Model:** claude-sonnet-4-5
**Prompt:** `StructuredSpecification-ChildBenefit-v2.md` (Structured spec with indeterminacy)
**Runs:** 6 runs × 199 test cases = 1,746 per-child assessments

**Overall accuracy:** ~82.2%

**Reliability summary (199 test cases):**

| Category        | Cases |
|-----------------|-------|
| Always Passes   | 120   |
| Flaky           | 56    |
| Systematic Fail | 23    |

**Key findings:**

- The overall accuracy (~82.2%) is an improvement over the structured rules conversational pipeline (~73.2%), as expected when removing actor hallucination as a variable.
- However, the accuracy is still notably lower than the free-text rules facts-bundle pipeline (~89.9%). This suggests that **free-text rules are both easier for the agent to use and more accurate than the current structured specification**.
- The reliability of the free-text facts-bundle approach is also higher (145 always-passing vs 120 here), which is surprising: structured rules were expected to produce more consistent results than free-text rules. The opposite was observed.
- This indicates that the current structured specification format may introduce ambiguity or complexity that degrades agent performance.

**Next steps identified:**

- Further iteration on the structured specification format.
- Investigate whether the structured rules can be reformulated to match or exceed the accuracy and reliability of the free-text approach.

---

## Summary comparison

| Pipeline | Rules format | Accuracy | Always Passes | Flaky | Systematic Fail |
|----------|-------------|----------|---------------|-------|-----------------|
| Conversational | Free text | ~89.9% | 78 / 199 | 99 / 199 | 22 / 199 |
| Facts bundle | Free text | ~89.9% | **145 / 199** | **43 / 199** | **11 / 199** |
| Conversational | Structured | ~73.2% | 87 / 199 | 77 / 199 | 35 / 199 |
| Facts bundle | Structured | ~82.2% | 120 / 199 | 56 / 199 | 23 / 199 |

**Key conclusions:**

1. **The facts-bundle pipeline is more reliable than the conversational pipeline** at the same accuracy level for free-text rules, strongly suggesting that a significant portion of conversational pipeline failures are caused by elicitation failure or actor hallucination rather than the judge agent.
2. **Free-text rules outperform structured rules** in both accuracy and reliability across both pipeline types. This is counter-intuitive and warrants further investigation into the structured specification format.
3. **The best performing configuration overall** is the facts-bundle pipeline with free-text rules: ~89.9% accuracy with 145/199 cases always passing, only 43 flaky, and 11 systematic failures.
