import json
import random
from typing import Any, Dict, List, Tuple
from pathlib import Path


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# Weekly Child Benefit rate for eldest/only child 2025/26
# If this is changed then the test cases with UPKEEP in the variant name need to be changed
# as this is a threshold which determines whether you get Child Benefit (if you don't live
# with the child and contribute less than this to their upkeep you can't get it)
CB_WEEKLY_RATE = 26.05

# Maps each fact field to a plain English description
# e.g. {"age": "The child's age in years."}
with open("data_dictionary.json", "r") as f:
    DATA_DICTIONARY = json.load(f)

OUTFILE_NAME = "../../../prompts/structured_generation/child_benefit/test_cases.jsonl"

RANDOM_GENERATION_CONFIG = {
    # Case-Level Probabilities
    "prob_claimant_uk": 0.80,  # 80% chance claimant lives in UK
    "num_children_choices": [1, 2, 3],
    "num_children_weights": [5, 3, 2],  # Mostly 1 child, rarely 3
    # For simplicity no one has more than 3 (the rules don't change at that point)
    "age_range": (2, 21),  # of children
    "prob_lives_with_claimant": 0.66,
    # 16-19 specific probabilities
    "prob_education": 0.50,
    "prob_extension": 0.50,
    # Responsibility (when living apart)
    "upkeep_amounts": [0.0, 10.0, 20.0, 26.05, 30.0, 50.0],
    "prob_another_claimant_lives_with_child": 0.33,
    "prob_another_claimant_priority": 0.10,
    # Care & Hospital
    "prob_care": 0.12,
    "care_weeks": [4, 7, 8, 9, 12, 16],
    "prob_care_home_24h": 0.50,
    "prob_hospital": 0.12,
    "hospital_weeks": [4, 8, 11, 12, 13, 18],
    "prob_hospital_spending": 0.50,
    # Fostering
    "prob_foster": 0.08,
    "prob_council_pays": 0.50,
    # Over 16 specific probabilities
    "prob_work_24_plus": 0.15,
    "prob_apprenticeship": 0.08,
    "prob_qualifying_benefits": 0.08,
    # Age Boundaries
    "min_age_post_16_rules": 16,  # Applies to education, work, apprenticeships, and benefits
    "max_age_extension": 17,  # The maximum inclusive age for the 20-week extension
    "age_education_cutoff": 20,  # The age at which ALL education eligibility strictly ends
}

# ---------------------------------------------------------------------------
# Rules
#
# Each function encodes a single eligibility criterion from the published
# Child Benefit rules (gov.uk). Each returns a Tuple[bool, str] (passed, reason).
#
# `passed` is a boolean as it's per-child. So a claimant may have two children
# and eligibility is True for child 0 and False for child 1.
#
# `reason` is why the child is eligible/ineligible e.g.
# "Someone who lives with the child is already claiming".
# You get one reason per condition and these are concatenated into
# a final free text summary,
# which sets out the entire circumstances of the child.
#
#
# The checks are deliberately simple so that correctness can be verified by
# reading the code alone
# There are also tests that they return what we expect (i.e. have been implemented correctly):
# _assert_correctness called in generate_systematic_cases().
# ---------------------------------------------------------------------------


def check_residency(facts: Dict[str, Any]) -> Tuple[bool, str]:
    """Claimant must live in the UK.
    Note that this applies to the claimant (i.e. parent/carer)
    whereas the other rules apply to the child.
    """
    if not facts["claimant_lives_in_uk"]:
        return False, "Claimant does not live in the UK"
    return True, "Claimant lives in the UK"


def check_child_age_education(child: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Child must be under 16, OR under 20 and in approved education/training,
    OR 16-17 and in the 20-week extension period (registered with a
    government careers service or armed forces).
    """
    age = child["age"]
    if age < 16:
        return True, f"Child is {age} (under 16)"
    if age >= 20:
        return False, f"Child is {age}, which is 20 or over"
    # 16-19
    if child["in_approved_education"]:
        return True, f"Child is {age} and in approved education"
    if age <= 17 and child["in_extension_period"]:
        return True, f"Child is {age} and in the 20-week extension period"
    return False, f"Child is {age} and not in approved education or extension period"


def check_responsibility(child: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Claimant must be responsible for the child: either the child lives with
    them (and no other claimant has priority), or the claimant contributes
    at least the Child Benefit rate per week to the child's upkeep.

    If someone who lives with the child is already claiming, they have
    priority over an upkeep-based claimant.
    """
    if child["lives_with_claimant"]:
        if child["another_claimant_has_priority"]:
            # Note: this is the path where they live with the child but another parent is already claiming
            return False, "Another claimant who lives with the child has priority"
        return True, "Child lives with claimant"

    # Can only get here if child does not live with claimant
    upkeep = child["upkeep_per_week"]
    if upkeep < CB_WEEKLY_RATE:
        return False, (
            f"Child does not live with claimant and weekly upkeep "
            f"(£{upkeep:.2f}) is below the Child Benefit rate (£{CB_WEEKLY_RATE})"
        )
    if child["another_claimant_lives_with_child"]:
        return False, "Someone who lives with the child is already claiming"
    return (
        True,
        f"Claimant contributes £{upkeep:.2f}/week towards child's upkeep (>= £{CB_WEEKLY_RATE}) and no other claimaint has priority",
    )


def check_care_absence(child: Dict[str, Any]) -> Tuple[bool, str]:
    """
    If the child has been in local authority care for more than 8 weeks,
    eligibility stops UNLESS the child spends at least 24 hours per week
    at home.
    """
    care_weeks = child["care_weeks"]
    if care_weeks > 8:
        if child["care_home_24h_per_week"]:
            return (
                True,
                f"Child in care for {care_weeks} weeks but spends 24+ hours/week at home",
            )
        return False, (
            f"Child in local authority care for {care_weeks} weeks "
            f"(>8) and does not spend 24+ hours/week at home"
        )
    if care_weeks > 0:
        return True, f"Child in care for {care_weeks} weeks (within 8-week limit)"
    return True, "Child is not in local authority care"


def check_hospital_absence(child: Dict[str, Any]) -> Tuple[bool, str]:
    """
    If the child has been in hospital or residential accommodation for more
    than 12 weeks, eligibility stops UNLESS the claimant regularly spends
    money on the child.
    """
    hospital_weeks = child["hospital_weeks"]
    if hospital_weeks > 12:
        if child["claimant_spends_on_child"]:
            return (
                True,
                f"Child in hospital for {hospital_weeks} weeks but claimant regularly spends on child",
            )
        return False, (
            f"Child in hospital/residential accommodation for "
            f"{hospital_weeks} weeks (>12) and claimant is not "
            f"regularly spending money on child"
        )
    if hospital_weeks > 0:
        return (
            True,
            f"Child in hospital for {hospital_weeks} weeks (within 12-week limit)",
        )
    return True, "Child is not in hospital or residential accommodation"


def check_fostering(child: Dict[str, Any]) -> Tuple[bool, str]:
    """
    A foster parent can claim Child Benefit ONLY if the local council is NOT
    paying towards the child's accommodation or maintenance.
    """
    if child["is_fostered"]:
        if child["council_pays_for_child"]:
            return (
                False,
                "Child is fostered and the council pays for their accommodation or maintenance",
            )
        return (
            True,
            "Child is fostered but the council is not paying for accommodation or maintenance",
        )
    return True, "Child is not fostered"


def check_child_work_status(child: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Eligibility stops if the child works 24 or more hours per week AND is
    no longer in approved education or training.
    """
    if child["works_24_plus_hours"]:
        if not child["in_approved_education"]:
            return False, "Child works 24+ hours/week and is not in approved education"
        return True, "Child works 24+ hours/week but is in approved education"
    return True, "Child does not work 24+ hours/week"


def check_apprenticeship(child: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Eligibility stops if the child starts an apprenticeship in England.
    """
    if child["started_apprenticeship_in_england"]:
        return False, "Child has started an apprenticeship in England"
    return True, "Child has not started an apprenticeship in England"


def check_child_benefits(child: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Eligibility stops if the child receives certain benefits in their own
    right, such as Universal Credit or Employment and Support Allowance.
    """
    if child["receives_qualifying_benefits"]:
        return (
            False,
            "Child receives qualifying benefits (e.g. UC, ESA) in their own right",
        )
    return True, "Child does not receive qualifying benefits in their own right"


# ---------------------------------------------------------------------------
# Check eligibility
# ---------------------------------------------------------------------------


def evaluate_eligibility(facts: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Evaluate eligibility for each child. Returns a list of per-child results.
    """

    child_checks = [
        check_child_age_education,
        check_responsibility,
        check_care_absence,
        check_hospital_absence,
        check_fostering,
        check_child_work_status,
        check_apprenticeship,
        check_child_benefits,
    ]

    res_ok, res_reason = check_residency(facts)

    results = []
    for child in facts["children"]:
        failed_reasons = []
        # Bit of a hack to append the residency to child but it's easiest approach
        # rather than special-casing this one reason
        all_circumstances = [res_reason]

        if not res_ok:
            failed_reasons.append(res_reason)

        # Evaluate every rule, storing the facts for the LLM script
        for fn in child_checks:
            passed, reason = fn(child)
            all_circumstances.append(reason)
            if not passed:
                failed_reasons.append(reason)

        is_eligible = len(failed_reasons) == 0

        results.append(
            {
                "child_id": child["id"],
                "eligible": is_eligible,
                # This is either a list of semicolon-separated failures, or all passes
                "reason": "; ".join(failed_reasons)
                if not is_eligible
                else "; ".join(all_circumstances),
                # The complete list of every reason regardless of pass/fail (for LLM script)
                "circumstances": all_circumstances,
            }
        )

    return results


# ---------------------------------------------------------------------------
# Case generation
# There are 49 systematic cases in systematic_cases.json.
# For these cases, we know the expected outcome and we check that we get this
# when we read it in - which is a useful confirmation that our eligibility rules
# are working.
# ---------------------------------------------------------------------------


def _generate_case_id(rule: str, variant: str, expected: List[bool]) -> str:
    """Derives a strict, predictable case ID based on the expected outcomes."""
    if all(expected):
        outcome_str = "PASS"
    elif not any(expected):
        outcome_str = "FAIL"
    else:
        outcome_str = "MIXED"

    case_id = f"{rule}_{outcome_str}"
    if variant:
        case_id += f"_{variant}"
    return case_id


def _build_child_facts(raw_children: List[Dict]) -> List[Dict]:
    """Takes raw JSON child data and returns a list of dicts.
    Assigns consecutive child_ids.
    If unspecified, specifies defaults as below (basically a simple case)
    """
    children = []
    for i, child_data in enumerate(raw_children):
        # 1. Define the complete baseline for a "standard, uncomplicated" child
        c = {
            "id": f"child_{i}",
            "age": 8,
            "lives_with_claimant": True,
            "in_approved_education": False,
            "in_extension_period": False,
            "upkeep_per_week": 0.0,
            "another_claimant_has_priority": False,
            "another_claimant_lives_with_child": False,
            "care_weeks": 0,
            "care_home_24h_per_week": False,
            "hospital_weeks": 0,
            "claimant_spends_on_child": False,
            "is_fostered": False,
            "council_pays_for_child": False,
            "works_24_plus_hours": False,
            "started_apprenticeship_in_england": False,
            "receives_qualifying_benefits": False,
        }

        # 2. Overwrite the baseline with whatever was explicitly stated in the JSON
        c.update(child_data)
        children.append(c)
    return children


def _enrich_facts(data: Any) -> Any:
    """Wraps keys with their DATA_DICTIONARY descriptions.
    So e.g. rather than output being:
    {"claimant_lives_in_uk": true}
    We have:
    {"claimant_lives_in_uk": {"description": "Whether the claimant lives in the UK.", "value": true}
    """
    if isinstance(data, dict):
        return {
            k: {
                "description": DATA_DICTIONARY[k],
                "value": _enrich_facts(v),
            }
            for k, v in data.items()
        }
    elif isinstance(data, list):
        return [_enrich_facts(item) for item in data]
    return data


def _build_preamble(facts: Dict[str, Any]) -> str:
    """Builds the factual 'Situation Profile' for the LLM."""
    lines = []

    # Claimant details
    lines.append("=== YOUR SITUATION PROFILE ===")
    lines.append(
        "You live in the UK."
        if facts["claimant_lives_in_uk"]
        else "You do not live in the UK."
    )

    # Number of children
    child_word = "child" if len(facts["children"]) == 1 else "children"
    lines.append(f"You are inquiring about your {len(facts['children'])} {child_word}:")

    # Child details
    for child in facts["children"]:
        lives_with = (
            "lives with you"
            if child["lives_with_claimant"]
            else "does not live with you"
        )
        lines.append(f"  - {child['id']} is {child['age']} years old and {lives_with}.")

    # The technical facts
    lines.append(
        "\nHere are the exact details of your circumstances to use when answering the agent's questions:"
    )

    return "\n".join(lines)


def _build_agent_script(facts: Dict[str, Any], eligibility_results: List[Dict]) -> str:
    """Formats the evaluated circumstances into a readable script for the LLM.
    For example, for the first test case it produces this:
    Regarding child_0:
    - Claimant lives in the UK
    - Child is 8 (under 16)
    - Child lives with claimant
    - Child is not in local authority care
    - Child is not in hospital or residential accommodation
    - Child is not fostered
    - Child does not work 24+ hours/week
    - Child has not started an apprenticeship in England
    - Child does not receive qualifying benefits in their own right
    """
    parts = [_build_preamble(facts)]
    for result in eligibility_results:
        facts_list = "\n".join(f"  - {c}" for c in result["circumstances"])
        parts.append(f"Regarding {result['child_id']}:\n{facts_list}")
    return "\n\n".join(parts)


def _assert_correctness(case_id: str, actual: List[bool], expected: List[bool]) -> None:
    """Verifies the rule engine's output matches the expectations specified in the json.
    For example Case 0 should return [True] (list of 1 child who is eligible).
    """
    assert actual == expected, (
        f"\nTEST FAILED: {case_id}\nExpected: {expected}\nActual:   {actual}"
    )


def generate_systematic_cases(
    json_filepath: str = "systematic_cases.json",
) -> List[Dict[str, Any]]:
    """Loads systematic test cases, evaluates them, and asserts correctness."""

    with open(json_filepath, "r") as f:
        raw_cases = json.load(f)

    cases = []

    for raw_case in raw_cases:
        # Parse the JSON inputs
        uk = raw_case.get("uk", True)  # default is lives in UK if not specified
        expected = raw_case["expected"]
        children = _build_child_facts(raw_case["children"])

        # Setup the facts and IDs
        # This is to get human-readable IDs like RESPONSIBILITY_FAIL_PRIORITY_CONFLICT
        case_id = _generate_case_id(
            raw_case.get("rule", "UNKNOWN"), raw_case.get("variant", ""), expected
        )
        facts = {"claimant_lives_in_uk": uk, "children": children}

        # Generate eligibility based on rules
        eligibility_results = evaluate_eligibility(facts)

        # Assert the engine behaved correctly
        actual_outcomes = [res["eligible"] for res in eligibility_results]
        _assert_correctness(case_id, actual_outcomes, expected)

        # Build and store the final payload
        cases.append(
            {
                "case_id": case_id,
                "facts": _enrich_facts(facts),
                "agent_script": _build_agent_script(facts, eligibility_results),
                "expected_eligibility": eligibility_results,
            }
        )

    return cases


# ---------------------------------------------------------------------------
# Random case generation
# ---------------------------------------------------------------------------


def generate_random_child(rng: random.Random, child_id: str) -> Dict[str, Any]:
    """Builds a random child profile based on RANDOM_GENERATION_CONFIG."""
    cfg = RANDOM_GENERATION_CONFIG

    age = rng.randint(cfg["age_range"][0], cfg["age_range"][1])
    lives_with = rng.random() < cfg["prob_lives_with_claimant"]

    child: Dict[str, Any] = {
        "id": child_id,
        "age": age,
        "lives_with_claimant": lives_with,
    }

    # Education / extension (16-19 only)
    if cfg["min_age_post_16_rules"] <= age < cfg["age_education_cutoff"]:
        child["in_approved_education"] = rng.random() < cfg["prob_education"]
        if not child["in_approved_education"] and age <= cfg["max_age_extension"]:
            child["in_extension_period"] = rng.random() < cfg["prob_extension"]

    # Responsibility details
    if not lives_with:
        child["upkeep_per_week"] = rng.choice(cfg["upkeep_amounts"])
        child["another_claimant_lives_with_child"] = (
            rng.random() < cfg["prob_another_claimant_lives_with_child"]
        )
    else:
        if rng.random() < cfg["prob_another_claimant_priority"]:
            child["another_claimant_has_priority"] = True

    # Care absence
    if rng.random() < cfg["prob_care"]:
        child["care_weeks"] = rng.choice(cfg["care_weeks"])
        child["care_home_24h_per_week"] = rng.random() < cfg["prob_care_home_24h"]

    # Hospital absence
    if rng.random() < cfg["prob_hospital"]:
        child["hospital_weeks"] = rng.choice(cfg["hospital_weeks"])
        child["claimant_spends_on_child"] = rng.random() < cfg["prob_hospital_spending"]

    # Fostering
    if rng.random() < cfg["prob_foster"]:
        child["is_fostered"] = True
        child["council_pays_for_child"] = rng.random() < cfg["prob_council_pays"]

    # Work, Apprenticeship, and Benefits (Older children)
    if age >= cfg["min_age_post_16_rules"]:
        if rng.random() < cfg["prob_work_24_plus"]:
            child["works_24_plus_hours"] = True

        if rng.random() < cfg["prob_apprenticeship"]:
            child["started_apprenticeship_in_england"] = True

        if rng.random() < cfg["prob_qualifying_benefits"]:
            child["receives_qualifying_benefits"] = True

    return child


def _generate_random_case_facts(rng: random.Random) -> Dict[str, Any]:
    """Generates the fully formed factual profile for a single random case."""
    cfg = RANDOM_GENERATION_CONFIG

    num_children = rng.choices(
        cfg["num_children_choices"], weights=cfg["num_children_weights"]
    )[0]
    claimant_uk = rng.random() < cfg["prob_claimant_uk"]

    raw_children = [
        generate_random_child(rng, f"child_{j}") for j in range(num_children)
    ]

    return {
        "claimant_lives_in_uk": claimant_uk,
        "children": _build_child_facts(raw_children),
    }


def generate_random_cases(count: int = 50, seed: int = 146) -> List[Dict[str, Any]]:
    """
    Generates random test cases, evaluates them, and builds the agent scripts.
    A seed of 146 happens to generate exactly 71 eligible and 71 ineligible children
    (when you have 50 random cases and the systematic ones above).
    """
    rng = random.Random(seed)
    cases = []

    for i in range(count):
        # 1. Generate the facts
        facts = _generate_random_case_facts(rng)

        # 2. Evaluate the rules
        eligibility_results = evaluate_eligibility(facts)

        # 3. Build and store the final payload
        cases.append(
            {
                "case_id": f"RND_{i + 1:03d}",
                "facts": _enrich_facts(facts),
                "agent_script": _build_agent_script(facts, eligibility_results),
                "expected_eligibility": eligibility_results,
            }
        )

    return cases


def save_cases(all_cases):

    output_path = Path(OUTFILE_NAME)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    jsonl_content = "\n".join(json.dumps(case) for case in all_cases) + "\n"
    output_path.write_text(jsonl_content, encoding="utf-8")


def main() -> None:
    systematic = generate_systematic_cases()
    random_cases = generate_random_cases(50)
    all_cases = systematic + random_cases

    save_cases(all_cases)

    # Summary
    total_children = sum(len(c["expected_eligibility"]) for c in all_cases)
    eligible = sum(
        1 for c in all_cases for r in c["expected_eligibility"] if r["eligible"]
    )
    print(
        f"Generated {len(all_cases)} cases "
        f"({len(systematic)} systematic + {len(random_cases)} random)"
    )
    print(f"Total evaluation points (children): {total_children}")
    print(f"Eligible: {eligible}, Ineligible: {total_children - eligible}")


if __name__ == "__main__":
    main()
