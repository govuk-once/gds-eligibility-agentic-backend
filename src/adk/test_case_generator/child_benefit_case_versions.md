# Child Benefit test case versions

The generated Child Benefit test cases may include a `content_version` field.

If `content_version` is omitted, this should be treated as version 1.

## Version 1

Version 1 refers to the original generated cases before the facts-bundle wording changes.

These cases were primarily formatted for actor-agent evaluations, where an actor agent receives a situation profile and answers questions from the eligibility agent.

## Version 2

Version 2 refers to regenerated cases where the case text has been updated to work better for facts-bundle evaluations. This means ensuring that the description of the file doesn't include the answer. For example, in v1 there were strings like:

```python
f"Child in care for {care_weeks} weeks (within 8-week limit)"
```

In v2 this has been changed to:

```python
f"Child in care for {care_weeks} weeks"
```

The purpose of this is so that the answer is not included in the description. The underlying eligibility facts and expected outcomes are intended to represent the same conceptual test cases as version 1, but the wording of the generated `agent_script` / case description may differ.

The purpose of `content_version` is to allow results from different generations to be separated in analysis.

`case_id` should continue to identify the conceptual test case. `content_version` identifies the generated wording/content version of that case.