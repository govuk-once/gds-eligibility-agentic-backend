# Child Benefit uncertainty test cases

## Purpose

This generator creates a separate Child Benefit evaluation set for cases where the agent should not force a yes/no eligibility decision.

The existing deterministic benchmark tests cases where the supplied Child Benefit rules determine the answer. This uncertainty set tests a different behaviour: whether the agent can return `INDETERMINATE` when the available information or supplied rules are insufficient.

The goal is not to estimate real-world accuracy. The goal is to create controlled ground-truth cases that make it possible to compare models, prompts and rule-provision approaches on uncertainty handling. This benchmark tests whether an eligibility agent knows when not to decide, and instead to say that it doesn't know.

## Current output

The current generator creates three groups of cases:

1. **Canonical unspecified cases** from `unspecified_cases.json`
2. **Canonical uncovered-rule cases** from `uncovered_cases.json`
3. **Random variants** generated from those reviewed canonical cases

The intended target is **100 total cases**:

- 11 canonical unspecified cases
- 9 canonical uncovered-rule cases
- 80 random variants

Each generated case should have expected eligibility:

```python
"INDETERMINATE"
```

The generator still supports `True` and `False` internally, because the rule checks share the same broad structure as the deterministic generator, but this particular uncertainty corpus should only produce indeterminate examples.

## Overall design

The design has two layers.

### 1. Reviewed canonical cases

The canonical cases are the ground-truth examples. These are small, hand-written JSON cases where the reason for indeterminacy should be obvious by inspection.

There are two types:

- **Unspecified required information**: the rules cover the scenario, but a necessary fact is unknown.
- **Uncovered or referred-out conditions**: the fact is known, but the supplied rules do not determine the answer.

### 2. Controlled random variants

The random generator does not invent new uncertainty types. It takes the reviewed canonical cases and produces controlled variants by changing safe surrounding facts.

This is deliberately limited. The random variation is there to avoid testing one fixed vignette repeatedly, not to generate arbitrary Child Benefit cases.

The core rule is:

> The uncertainty trigger must remain the same.

For example, if the canonical case is about an apprenticeship outside England, the random generator may vary the location between Wales, Scotland, Northern Ireland and named cities in those countries. It should not turn the case into an apprenticeship in England or introduce a separate determinate failure.

## Outcome logic

The uncertainty rule engine uses a tri-state outcome:

```python
"ELIGIBLE" | "INELIGIBLE" | "INDETERMINATE"
```

The rule is:

1. If any check gives a definite failure, the child is `"INELIGIBLE"`.
2. Otherwise, if any check is indeterminate, the child is `"INDETERMINATE"`.
3. Otherwise, the child is `"ELIGIBLE"`.

This is important. It means an indeterminate case should not also contain a separate deterministic reason for ineligibility. Otherwise the final expected output would be `"INELIGIBLE"`, not `"INDETERMINATE"`.

## Uncertainty areas tested

### A. Required information is unspecified

These cases test whether the agent can avoid making a decision when the user has not provided a fact that the rules need.

| Area | Trigger | Why this is indeterminate |
|---|---|---|
| UK residence unknown | It is unknown whether the claimant lives in the UK | UK residence is a threshold condition. Without it, the rules cannot determine eligibility. |
| Child age unknown | Child age is unknown, but known to be somewhere between 15 and 19 | The answer may depend on whether the child is under 16, 16-17, or 18-19. |
| Approved education unknown | The child is 16-19, but it is unknown whether they are in approved education or training | For 16-19 year olds, education/training status can determine eligibility. |
| 20-week extension unknown | The child is 16 or 17, not in approved education, and extension status is unknown | A 16-17 year old may still qualify during the 20-week extension period. |
| Upkeep amount unknown | The child does not live with the claimant, and weekly upkeep is unknown | Eligibility may depend on whether upkeep is at least the Child Benefit rate. |
| Priority claimant unknown | The child lives with the claimant, but it is unknown whether another person living with the child has priority | Another claimant with priority can block entitlement. |
| Care-home exception unknown | The child has been in local authority care for more than 8 weeks, but it is unknown whether they spend 24+ hours per week at home | The care absence rule has an exception based on time spent at home. |
| Hospital spending exception unknown | The child has been in hospital/residential accommodation for more than 12 weeks, but it is unknown whether the claimant regularly spends money on them | The hospital/residential rule has an exception based on regular spending. |
| Foster council support unknown | The child is fostered, but it is unknown whether the council pays towards accommodation or maintenance | Foster eligibility depends on whether the council pays towards the child. |
| Apprenticeship in England status unknown | The child is 16+, but it is unknown whether they have started an apprenticeship in England | Starting an apprenticeship in England can end eligibility. |
| Child benefit status unknown | The child is 16+, but it is unknown whether they receive qualifying benefits in their own right | Receiving qualifying benefits in the child's own right can end eligibility. |

### B. Known facts are not determined by the supplied rules

These cases test situations where the user has provided a fact, but the supplied Child Benefit rules do not give enough detail to determine eligibility.

| Area | Trigger | Why this is indeterminate |
|---|---|---|
| Apprenticeship in Wales | Child has started an apprenticeship in Wales | The supplied rule covers apprenticeships in England, not Wales. |
| Apprenticeship in Scotland | Child has started an apprenticeship in Scotland | The supplied rule covers apprenticeships in England, not Scotland. |
| Apprenticeship in Northern Ireland | Child has started an apprenticeship in Northern Ireland | The supplied rule covers apprenticeships in England, not Northern Ireland. |
| Recently moved to the UK | Claimant recently moved to the UK and right-to-reside position is unclear | The supplied rules do not determine the right-to-reside issue from the case facts. |
| Informal arrangement | Claimant looks after a child through an informal arrangement | This is treated as a referred-out or insufficiently determined situation. |
| Unresolved claimant dispute | Claimant and another responsible person cannot agree who should claim | The supplied rules do not resolve the dispute directly. |
| Adoption before child moves in | Claimant is adopting the child, but the child has not yet come to live with them | This is a boundary case not directly resolved by the supplied rules. |
| Hospital abroad | Child is in hospital abroad and exception details are unknown | The hospital-abroad exception depends on further facts not supplied in the case. |
| Pre-settled status | Claimant has pre-settled status and financial-resource details are unknown | The supplied facts are not enough to determine whether the relevant conditions are met. |

Note that the current set does **not** test "no right to reside". It tests unclear or unconfirmed right-to-reside status. That distinction matters, because "no right to reside" may be a determinate exclusion, while "unclear right to reside" is an uncertainty case.

## Random variant generation

The random generator starts from the canonical cases and cycles through them until the target total number of cases is reached.

For each selected canonical case, it:

1. Deep-copies the raw JSON case.
2. Assigns a new case ID ending in `_RND_###`.
3. Preserves the expected output.
4. Applies safe random changes.
5. Rebuilds the full case payload.
6. Evaluates the case and asserts that the actual output still matches the expected output.

### What gets randomised

The randomisation is deliberately conservative.

#### Age

Age may be varied where doing so does not destroy the uncertainty trigger.

Examples:

- If the unknown field is approved education, age remains 16-19.
- If the unknown field is extension-period status, age remains 16-17.
- If the trigger is an apprenticeship or qualifying benefits issue, age remains 16-19 and the child is otherwise kept in approved education.
- For other uncertainty types, the child may be made either:
  - under 16, or
  - 16-19 and in approved education.

#### Responsibility route

Where responsibility is not itself the uncertainty trigger, the random generator may vary whether the child:

- lives with the claimant, or
- does not live with the claimant but receives sufficient upkeep.

It avoids doing this where responsibility is part of the uncertainty trigger, or where the case involves a special relationship such as fostering, adoption, informal care, or claimant dispute.

#### Right-to-reside wording

For moved-to-UK cases, the random generator varies the wording of the unclear right-to-reside position. These variants stay deliberately vague, for example:

- "right-to-reside position is not known"
- "right-to-reside position is uncertain"
- "right-to-reside position has not been established"

The wording should not imply a specific immigration status.

#### Apprenticeship location

For apprenticeship-outside-England cases, the random generator varies the location across Wales, Scotland and Northern Ireland, including named cities such as Cardiff, Glasgow and Belfast.

These variants should still clearly remain outside England.

### What does not get randomised

The random generator does not create new uncertainty concepts. It also avoids randomising fields that would create a competing deterministic answer.

In particular, it should not:

- overwrite a field that is deliberately `None`
- create an apprenticeship in England for an apprenticeship-outside-England case
- make a 16-19 education uncertainty case into an under-16 case
- add a separate ineligibility reason to an indeterminate case
- combine multiple special situations such as adoption, fostering and claimant dispute unless the canonical case already does so

## Guardrails

The generator uses several guardrails.

### Unknown means explicitly `None`

A fact is treated as unknown only if the field is present and set to `None`.

This avoids confusing "missing from JSON, so use the default" with "the user does not know this fact".

### Validation of unspecified cases

The unspecified cases are validated to catch cases where an unknown field is only meaningful under another branch.

For example:

- `in_approved_education` can only be unknown for a child aged 16-19.
- `in_extension_period` can only be unknown for a child aged 16 or 17 who is not in approved education.
- `upkeep_per_week` can only be unknown when the child does not live with the claimant.
- `care_home_24h_per_week` can only be unknown when `care_weeks > 8`.
- `claimant_spends_on_child` can only be unknown when `hospital_weeks > 12`.
- `council_pays_for_child` can only be unknown when the child is fostered.

### Assertion against expected outcome

After each case is generated, the evaluator runs and checks that the actual outcome matches the expected outcome in the JSON.

For the uncertainty corpus, that means checking the generated child-level output remains `"INDETERMINATE"`.

This is especially important for random variants, because it catches accidental changes that remove the uncertainty trigger or introduce a deterministic failure.

## What this benchmark can and cannot tell us

### It can tell us

- Whether an agent can return `INDETERMINATE` rather than force a yes/no answer.
- Whether different models or prompts handle uncertainty differently.
- Whether a model tends to hallucinate determinate eligibility decisions where the facts or rules are insufficient.
- Whether changes to the prompt or tool schema affect uncertainty handling.

### It cannot tell us

- Real-world accuracy across all Child Benefit queries.
- How often these uncertainty scenarios occur in real users' queries.
- Whether the supplied rules are legally complete.
- Whether the actor agent always avoids hallucinating missing facts.
- How the agent behaves with multiple simultaneous uncertainties unless those are explicitly generated.
- How the agent behaves with uncertainty types not included in the canonical cases.

## Adding new uncertainty types

To add a new uncertainty type:

1. Add one reviewed canonical case to either `unspecified_cases.json` or `uncovered_cases.json`.
2. Make sure the expected output is `"INDETERMINATE"`.
3. Add or update the relevant `check_*` function if the rule engine does not yet recognise the trigger.
4. Add validation if the unknown field is only meaningful under certain conditions.
5. Only then add randomisation, and only if there are safe surrounding facts to vary.

Do not start with random generation. Start with one readable canonical case.
