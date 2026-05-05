import json
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parent
CB_WEEKLY_RATE = 26.05
STATUS_INDETERMINATE = "INDETERMINATE"
STATUS_INELIGIBLE = "INELIGIBLE"
STATUS_ELIGIBLE = "ELIGIBLE"
OUTFILE_NAME = BASE_DIR.parent.parent.parent / "prompts/structured_generation/child_benefit/uncertainty_cases.jsonl"

CONTENT_VERSION = 2

with (BASE_DIR / "data_dictionary.json").open("r", encoding="utf-8") as f:
    DATA_DICTIONARY = json.load(f)

with (BASE_DIR / "uncertainty_data_dictionary.json").open("r", encoding="utf-8") as f:
    EXTRA_DATA_DICTIONARY = json.load(f)

FIELD_DESCRIPTIONS = DATA_DICTIONARY | EXTRA_DATA_DICTIONARY

RANDOM_GENERATION_CONFIG = {
    "prob_claimant_uk": 0.80,
    "num_children_choices": [1, 2, 3],
    "num_children_weights": [5, 3, 2],
    "age_range": (2, 21),
    "prob_lives_with_claimant": 0.66,
    "prob_education": 0.50,
    "prob_extension": 0.50,
    "upkeep_amounts": [0.0, 10.0, 20.0, 26.05, 30.0, 50.0],
    "prob_another_claimant_lives_with_child": 0.33,
    "prob_another_claimant_priority": 0.10,
    "prob_care": 0.12,
    "care_weeks": [4, 7, 8, 9, 10, 16],
    "prob_care_home_24h": 0.50,
    "prob_hospital": 0.12,
    "hospital_weeks": [4, 8, 11, 10, 13, 18],
    "prob_hospital_spending": 0.50,
    "prob_foster": 0.08,
    "prob_council_pays": 0.50,
    "prob_work_24_plus": 0.15,
    "prob_apprenticeship": 0.08,
    "prob_qualifying_benefits": 0.08,
    "min_age_post_16_rules": 16,
    "max_age_extension": 17,
    "age_education_cutoff": 20,
    "names": ["Alex", "Blake", "Charlie"],
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _field_is_unknown(obj: dict[str, Any], field: str) -> bool:
    """A field is unknown only if it is explicitly present with value None."""
    return field in obj and obj[field] is None


def _get_unknown_description(obj: dict[str, Any], field: str) -> str | None:
    return obj.get("_unknown_descriptions", {}).get(field)


def _money(amount: float | int) -> str:
    return f"£{amount:.2f}"


def _tri_state(failures: list[str], indeterminates: list[str]) -> str:
    """
    Takes the list of failures and returns a string indicating
    whether the child is eligible, ineligible or if this is indeterminate.
    """
    if failures:
        return STATUS_INELIGIBLE
    if indeterminates:
        return STATUS_INDETERMINATE
    return STATUS_ELIGIBLE

def _has_apprenticeship_issue(child: dict[str, Any]) -> bool:
    """
    This is a robustness check to make sure that someone isn't
    in approved education and also with an "unknown" apprenticeship
    as that doesn't really make sense.

    True when the case is about an actual or uncertain apprenticeship.
    """
    return (
        _field_is_unknown(child, "started_apprenticeship_in_england")
        or child.get("started_apprenticeship_in_england") is True
        or bool(child.get("apprenticeship_location"))
    )
# ---------------------------------------------------------------------------
# Case-level checks
# Each check has at most one path to STATUS_INDETERMINATE.
# ---------------------------------------------------------------------------


def check_residency(facts: dict[str, Any]) -> tuple[bool | str, str | None]:
    if _field_is_unknown(facts, "claimant_lives_in_uk"):
        return STATUS_INDETERMINATE, "It is unknown whether claimant lives in the UK"
    if not facts["claimant_lives_in_uk"]:
        return False, "Claimant does not live in the UK"
    return True, "Claimant lives in the UK"


def check_moved_to_uk(facts: dict[str, Any]) -> tuple[bool | str, str | None]:
    if facts.get("recently_moved_to_uk") is not True:
        return True, None
    right_to_reside = facts.get("right_to_reside_status", "not specified")
    return (
        STATUS_INDETERMINATE,
        f"Claimant has recently moved to the UK and their right-to-reside position is '{right_to_reside}'",
    )


def check_pre_settled_status(facts: dict[str, Any]) -> tuple[bool | str, str | None]:
    if facts.get("eu_status") != "pre_settled":
        return True, None
    return (
        STATUS_INDETERMINATE,
        "Claimant has pre-settled status and further details about their financial resources are unknown",
    )


# ---------------------------------------------------------------------------
# Child-level checks
# Each check has at most one path to STATUS_INDETERMINATE.
# ---------------------------------------------------------------------------

def check_child_age_education(child: dict[str, Any]) -> tuple[bool | str, str]:
    """
    Child must be under 16, OR under 20 and in approved education/training,
    OR 16-17 and in the 20-week extension period (registered with a
    government careers service or armed forces).

    Apprenticeship uncertainty cases are treated separately. They should not
    also say the child is in approved education, but the age/education rule
    should not turn them into determinate failures before the apprenticeship
    rule is evaluated.
    """
    if _field_is_unknown(child, "age"):
        return (
            STATUS_INDETERMINATE,
            "Child age is unknown; child is known to be somewhere between 15 and 19",
        )

    age = child["age"]
    if age < 16:
        return True, f"Child is {age} (under 16)"
    if age >= 20:
        return False, f"Child is {age}, which is 20 or over"

    # 16-19 apprenticeship cases are handled by the apprenticeship checks.
    # They must not also be described as being in approved education.
    if _has_apprenticeship_issue(child):
        return True, f"Child is {age} and not in approved education; apprenticeship status is relevant"

    # 16-19
    if _field_is_unknown(child, "in_approved_education"):
        return (
            STATUS_INDETERMINATE,
            "It is unknown whether child is in approved education or training, including the type of education or training",
        )

    if child["in_approved_education"]:
        return True, f"Child is {age} and in approved education"

    if age <= 17:
        if _field_is_unknown(child, "in_extension_period"):
            return (
                STATUS_INDETERMINATE,
                "It is unknown whether child has left education or training and has been registered with a government-sponsored careers service or the armed services for less than 20 weeks",
            )

        if child["in_extension_period"]:
            return True, f"Child is {age}, has left education or training and been registered with a government-sponsored careers service or the armed services for less than 20 weeks"

    return False, f"Child is {age} and not in approved education or extension period"

def check_lives_with_claimant(child: dict[str, Any]) -> tuple[bool | str, str | None]:
    if _field_is_unknown(child, "lives_with_claimant"):
        return STATUS_INDETERMINATE, "It is unknown whether child lives with claimant"
    if child["lives_with_claimant"]:
        return True, "Child lives with claimant"
    return True, "Child does not live with claimant"


def check_priority_when_living_with_claimant(child: dict[str, Any]) -> tuple[bool | str, str | None]:
    if child.get("lives_with_claimant") is not True:
        return True, None

    if _field_is_unknown(child, "another_claimant_has_priority"):
        return (
            STATUS_INDETERMINATE,
            "It is unknown whether another person who lives with child has priority for claiming Child Benefit",
        )

    if child["another_claimant_has_priority"]:
        return False, "Another claimant who lives with the child has priority"

    return True, "No other claimant who lives with the child has priority"


def check_upkeep_when_not_living_with_claimant(child: dict[str, Any]) -> tuple[bool | str, str | None]:
    if child.get("lives_with_claimant") is not False:
        return True, None

    if _field_is_unknown(child, "upkeep_per_week"):
        return (
            STATUS_INDETERMINATE,
            "The weekly value of claimant's upkeep for the child is unknown; it could be below or above the Child Benefit rate",
        )

    upkeep = child["upkeep_per_week"]
    if upkeep < CB_WEEKLY_RATE:
        return (
            False,
            f"Child does not live with claimant and weekly upkeep is ({_money(upkeep)})",
        )

    return True, f"Claimant contributes {_money(upkeep)}/week towards child's upkeep (>= {_money(CB_WEEKLY_RATE)})"


def check_other_claimant_when_not_living_with_claimant(child: dict[str, Any]) -> tuple[bool | str, str | None]:
    if child.get("lives_with_claimant") is not False:
        return True, None
    upkeep = child.get("upkeep_per_week")
    if not isinstance(upkeep, (int, float)) or upkeep < CB_WEEKLY_RATE:
        return True, None

    if _field_is_unknown(child, "another_claimant_lives_with_child"):
        return (
            STATUS_INDETERMINATE,
            "It is unknown whether someone who lives with child is already claiming Child Benefit for them",
        )

    if child["another_claimant_lives_with_child"]:
        return False, "Someone who lives with the child is already claiming"

    return True, "No one who lives with the child is already claiming"


def check_care_duration(child: dict[str, Any]) -> tuple[bool | str, str | None]:
    if _field_is_unknown(child, "care_weeks"):
        return STATUS_INDETERMINATE, "It is unknown how long child has been in local authority care"

    care_weeks = child["care_weeks"]
    if care_weeks > 8:
        return True, f"Child is in local authority care for {care_weeks} weeks"
    if care_weeks > 0:
        return True, f"Child in care for {care_weeks} weeks"
    return True, "Child is not in local authority care"


def check_care_home_exception(child: dict[str, Any]) -> tuple[bool | str, str | None]:
    care_weeks = child.get("care_weeks")
    if not (isinstance(care_weeks, (int, float)) and care_weeks > 8):
        return True, None

    if _field_is_unknown(child, "care_home_24h_per_week"):
        return (
            STATUS_INDETERMINATE,
            "Child has been in local authority care for more than 8 weeks, but it is unknown how many hours per week child spends at home. It could be anywhere from zero to 100 hours",
        )

    if child["care_home_24h_per_week"]:
        return True, f"Child in care for {care_weeks} weeks but spends 24+ hours/week at home"

    return (
        False,
        f"Child in local authority care for {care_weeks} weeks and does not spend 24+ hours/week at home",
    )


def check_hospital_duration(child: dict[str, Any]) -> tuple[bool | str, str | None]:
    if child.get("hospital_abroad") is True:
        return True, "Child is in hospital abroad"

    if _field_is_unknown(child, "hospital_weeks"):
        return STATUS_INDETERMINATE, "It is unknown how long child has been in hospital or residential accommodation"

    hospital_weeks = child["hospital_weeks"]
    if hospital_weeks > 12:
        return True, f"Child is in hospital/residential accommodation for {hospital_weeks} weeks (>12)"
    if hospital_weeks > 0:
        return True, f"Child in hospital for {hospital_weeks} weeks (within 12-week limit)"
    return True, "Child is not in hospital or residential accommodation"


def check_hospital_spending_exception(child: dict[str, Any]) -> tuple[bool | str, str | None]:
    if child.get("hospital_abroad") is True:
        return True, None

    hospital_weeks = child.get("hospital_weeks")
    if not (isinstance(hospital_weeks, (int, float)) and hospital_weeks > 12):
        return True, None

    if _field_is_unknown(child, "claimant_spends_on_child"):
        return (
            STATUS_INDETERMINATE,
            "Child has been in hospital or residential accommodation for more than 12 weeks, but it is unknown whether claimant regularly spends money on child",
        )

    if child["claimant_spends_on_child"]:
        return True, f"Child in hospital for {hospital_weeks} weeks but claimant regularly spends on child"

    return (
        False,
        f"Child in hospital/residential accommodation for {hospital_weeks} weeks (>12) and claimant is not regularly spending money on child",
    )


def check_hospital_abroad(child: dict[str, Any]) -> tuple[bool | str, str | None]:
    if child.get("hospital_abroad") is not True:
        return True, None
    return (
        STATUS_INDETERMINATE,
        "Child is in hospital abroad; it is unknown whether the child only went abroad to be in hospital, whether claimant is back in the UK, and whether claimant regularly spends money on child",
    )


def check_is_fostered(child: dict[str, Any]) -> tuple[bool | str, str | None]:
    if _field_is_unknown(child, "is_fostered"):
        return STATUS_INDETERMINATE, "It is unknown whether child is fostered"

    if child["is_fostered"]:
        return True, "Child is fostered"

    return True, "Child is not fostered"


def check_foster_council_support(child: dict[str, Any]) -> tuple[bool | str, str | None]:
    if child.get("is_fostered") is not True:
        return True, None

    if _field_is_unknown(child, "council_pays_for_child"):
        return (
            STATUS_INDETERMINATE,
            "Child is fostered, but it is unknown whether the local council pays towards the child's accommodation or maintenance",
        )

    if child["council_pays_for_child"]:
        return False, "Child is fostered and the council pays for their accommodation or maintenance"

    return True, "Child is fostered but the council is not paying for accommodation or maintenance"


def check_informal_arrangement(child: dict[str, Any]) -> tuple[bool | str, str | None]:
    if child.get("informal_arrangement") is not True:
        return True, None
    return STATUS_INDETERMINATE, "Claimant is not the child's parent or official carer and looks after child through an informal arrangement"


def check_claimant_dispute(child: dict[str, Any]) -> tuple[bool | str, str | None]:
    if child.get("claimant_dispute_unresolved") is not True:
        return True, None
    return (
        STATUS_INDETERMINATE,
        "Claimant and another person are both responsible for the child and cannot agree who should claim Child Benefit",
    )


def check_adoption_boundary(child: dict[str, Any]) -> tuple[bool | str, str | None]:
    if child.get("is_adopting") is True and child.get("child_has_moved_in") is False:
        return (
            STATUS_INDETERMINATE,
            "Claimant is adopting the child, but the child has not yet come to live with claimant",
        )
    if child.get("is_adopting") is True:
        return True, "Child is being adopted and has come to live with claimant"
    return True, None


def check_work_hours(child: dict[str, Any]) -> tuple[bool | str, str | None]:
    if _field_is_unknown(child, "works_24_plus_hours"):
        return STATUS_INDETERMINATE, "It is unknown whether child works 24 hours or more each week in paid employment"

    if child["works_24_plus_hours"]:
        return True, "Child works 24+ hours/week"

    return True, "Child does not work 24+ hours/week"


def check_work_education_interaction(child: dict[str, Any]) -> tuple[bool | str, str | None]:
    if child.get("works_24_plus_hours") is not True:
        return True, None

    if _field_is_unknown(child, "in_approved_education"):
        return (
            STATUS_INDETERMINATE,
            "It is unknown whether child is in approved education or training, including the type of education or training",
        )

    if not child["in_approved_education"]:
        return False, "Child works 24+ hours/week and is not in approved education"

    return True, "Child works 24+ hours/week but is in approved education"


def check_apprenticeship(child: dict[str, Any]) -> tuple[bool | str, str | None]:
    if _field_is_unknown(child, "started_apprenticeship_in_england"):
        return STATUS_INDETERMINATE, "It is unknown whether child has started an apprenticeship in England"

    if child["started_apprenticeship_in_england"]:
        return False, "Child has started an apprenticeship in England"

    return True, "Child has not started an apprenticeship in England"


def check_apprenticeship_location(child: dict[str, Any]) -> tuple[bool | str, str | None]:
    location = child.get("apprenticeship_location")
    if not location:
        return True, None
    if location == "England":
        return False, "Child has started an apprenticeship in England"
    return STATUS_INDETERMINATE, f"Child has started an apprenticeship in {location}"


def check_child_benefits(child: dict[str, Any]) -> tuple[bool | str, str | None]:
    if _field_is_unknown(child, "receives_qualifying_benefits"):
        return (
            STATUS_INDETERMINATE,
            "It is unknown whether child receives benefits in their own right, such as Universal Credit or Employment and Support Allowance",
        )
    if child["receives_qualifying_benefits"]:
        return False, "Child receives qualifying benefits (e.g. UC, ESA) in their own right"
    return True, "Child does not receive qualifying benefits in their own right"


def evaluate_eligibility(facts: dict[str, Any]) -> dict[str, dict[str, Any]]:
    case_checks = [check_residency, check_moved_to_uk, check_pre_settled_status]
    child_checks = [
        check_child_age_education,
        check_lives_with_claimant,
        check_priority_when_living_with_claimant,
        check_upkeep_when_not_living_with_claimant,
        check_other_claimant_when_not_living_with_claimant,
        check_care_duration,
        check_care_home_exception,
        check_hospital_duration,
        check_hospital_spending_exception,
        check_hospital_abroad,
        check_is_fostered,
        check_foster_council_support,
        check_informal_arrangement,
        check_claimant_dispute,
        check_adoption_boundary,
        check_work_hours,
        check_work_education_interaction,
        check_apprenticeship,
        check_apprenticeship_location,
        check_child_benefits,
    ]

    case_failures: list[str] = []
    case_indeterminates: list[str] = []
    case_circumstances: list[str] = []

    for fn in case_checks:
        status, reason = fn(facts)
        if reason:
            case_circumstances.append(reason)
        if status is False and reason:
            case_failures.append(reason)
        elif status == STATUS_INDETERMINATE and reason:
            case_indeterminates.append(reason)

    results: dict[str, dict[str, Any]] = {}
    for child in facts["children"].values():
        failures = list(case_failures)
        indeterminates = list(case_indeterminates)
        circumstances = list(case_circumstances)

        for fn in child_checks:
            status, reason = fn(child)
            if reason:
                circumstances.append(reason)
            if status is False and reason:
                failures.append(reason)
            elif status == STATUS_INDETERMINATE and reason:
                indeterminates.append(reason)

        eligibility_status = _tri_state(failures, indeterminates)
        reason = "; ".join(failures if eligibility_status == STATUS_INELIGIBLE else circumstances)

        results[child["name"]] = {
            "child_id": child["id"],
            "name": child["name"],
            "eligible": eligibility_status,
            "reason": reason,
            "circumstances": circumstances,
        }

    return results


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------


def _unknown_fields(obj: dict[str, Any]) -> set[str]:
    return {k for k, v in obj.items() if v is None}

def _validate_child_consistency(case_id: str, child: dict[str, Any]) -> None:
    """
    Catch logically inconsistent combinations in both reviewed and random cases.
    """
    name = child.get("name", "unknown child")

    def fail(message: str) -> None:
        raise ValueError(f"{case_id}: {name}: {message}")

    age = child.get("age")

    if _has_apprenticeship_issue(child):
        if not (isinstance(age, int) and age >= 16):
            fail("apprenticeship cases should only be used for a child aged 16 or over")

        if child.get("in_approved_education") is not False:
            fail(
                "apprenticeship cases must not also say the child is in approved education"
            )

        if child.get("in_extension_period") is True:
            fail(
                "apprenticeship cases must not also say the child is in the 20-week extension period"
            )

    if child.get("is_adopting") is True:
        if "child_has_moved_in" not in child:
            fail("adoption cases should specify whether the child has moved in")

        if child.get("child_has_moved_in") is False and child.get("lives_with_claimant") is not False:
            fail("adoption-before-move-in cases must not say the child lives with claimant")

        if child.get("child_has_moved_in") is True and child.get("lives_with_claimant") is not True:
            fail("adoption-after-move-in cases should say the child lives with claimant")

def _validate_unspecified_child(case_id: str, child: dict[str, Any]) -> None:
    """Catch cases where an unknown field is only relevant under another branch."""
    unknown = _unknown_fields(child)
    name = child.get("name", "unknown child")

    def fail(message: str) -> None:
        raise ValueError(f"{case_id}: {name}: {message}")

    age = child.get("age")

    if "in_approved_education" in unknown and not (isinstance(age, int) and 16 <= age < 20):
        fail("in_approved_education should only be unknown for a child aged 16 to 19")

    if "in_extension_period" in unknown:
        if not (isinstance(age, int) and age in (16, 17)):
            fail("in_extension_period should only be unknown for a child aged 16 or 17")
        if child.get("in_approved_education") is not False:
            fail("in_extension_period should only be unknown when the child is not in approved education")

    if "upkeep_per_week" in unknown and child.get("lives_with_claimant") is not False:
        fail("upkeep_per_week should only be unknown when the child does not live with the claimant")

    if "another_claimant_has_priority" in unknown and child.get("lives_with_claimant") is not True:
        fail("another_claimant_has_priority should only be unknown when the child lives with the claimant")

    if "another_claimant_lives_with_child" in unknown and child.get("lives_with_claimant") is not False:
        fail("another_claimant_lives_with_child should only be unknown when the child does not live with the claimant")

    if "care_home_24h_per_week" in unknown:
        care_weeks = child.get("care_weeks")
        if not (isinstance(care_weeks, (int, float)) and care_weeks > 8):
            fail("care_home_24h_per_week should only be unknown when care_weeks is over 8")

    if "claimant_spends_on_child" in unknown:
        hospital_weeks = child.get("hospital_weeks")
        if not (isinstance(hospital_weeks, (int, float)) and hospital_weeks > 12):
            fail("claimant_spends_on_child should only be unknown when hospital_weeks is over 12")

    if "council_pays_for_child" in unknown and child.get("is_fostered") is not True:
        fail("council_pays_for_child should only be unknown when the child is fostered")

    for field in ["works_24_plus_hours", "started_apprenticeship_in_england", "receives_qualifying_benefits"]:
        if field in unknown and not (isinstance(age, int) and age >= 16):
            fail(f"{field} should only be unknown for a child aged 16 or over")


def _validate_unspecified_case(case_id: str, facts: dict[str, Any]) -> None:
    for child in facts["children"].values():
        _validate_child_consistency(case_id, child)
        _validate_unspecified_child(case_id, child)

# ---------------------------------------------------------------------------
# Case generation
# ---------------------------------------------------------------------------


def _generate_case_id(rule: str, variant: str, expected: list[str]) -> str:
    if all(x == STATUS_ELIGIBLE for x in expected):
        outcome = "PASS"
    elif all(x == STATUS_INELIGIBLE for x in expected):
        outcome = "FAIL"
    elif all(x == STATUS_INDETERMINATE for x in expected):
        outcome = "INDET"
    else:
        outcome = "MIXED"

    return f"{rule}_{outcome}" + (f"_{variant}" if variant else "")


def _build_child_facts(raw_children: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    children: dict[str, dict[str, Any]] = {}
    for i, child_data in enumerate(raw_children):
        child: dict[str, Any] = {
            "id": f"child_{i}",
            "name": RANDOM_GENERATION_CONFIG["names"][i],
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
            "_unknown_descriptions": {},
        }
        child.update(child_data)
        if "_unknown_descriptions" not in child:
            child["_unknown_descriptions"] = {}
        children[child["name"]] = child
    return children


def _enrich_facts(data: Any) -> Any:
    if isinstance(data, dict):
        unknown_descriptions = data.get("_unknown_descriptions", {})
        enriched: dict[str, Any] = {}
        for key, value in data.items():
            if key.startswith("_"):
                continue

            enriched_value = (
                unknown_descriptions[key]
                if value is None and key in unknown_descriptions
                else _enrich_facts(value)
            )

            if key in FIELD_DESCRIPTIONS:
                enriched[key] = {
                    "description": FIELD_DESCRIPTIONS[key],
                    "value": enriched_value,
                }
            else:
                enriched[key] = enriched_value
        return enriched

    if isinstance(data, list):
        return [_enrich_facts(item) for item in data]

    return data


def _build_preamble(facts: dict[str, Any]) -> str:
    lines = ["=== YOUR SITUATION PROFILE ==="]

    if _field_is_unknown(facts, "claimant_lives_in_uk"):
        lines.append("It is unknown whether you live in the UK.")
    else:
        lines.append("You live in the UK." if facts["claimant_lives_in_uk"] else "You do not live in the UK.")

    child_word = "child" if len(facts["children"]) == 1 else "children"
    lines.append(f"You are asking about Child Benefit for {len(facts['children'])} {child_word}:")

    for child in facts["children"].values():
        if _field_is_unknown(child, "age"):
            age_desc = _get_unknown_description(child, "age") or "unknown"
            if age_desc.startswith("unknown;"):
                age_text = f"of unknown age ({age_desc.split(';', 1)[1].strip()})"
            elif age_desc == "unknown":
                age_text = "of unknown age"
            else:
                age_text = f"of unknown age ({age_desc})"
        else:
            age_text = f"{child['age']} years old"

        if child.get("is_adopting") is True and child.get("child_has_moved_in") is False:
            lives_with = "has not yet come to live with you"
        elif _field_is_unknown(child, "lives_with_claimant"):
            lives_with = "has an unknown living arrangement"
        else:
            lives_with = "lives with you" if child["lives_with_claimant"] else "does not live with you"

        lines.append(f"  - {child['name']} is {age_text} and {lives_with}.")

    lines.append("\nHere are the exact details of your circumstances to use when answering the agent's questions:")
    return "\n".join(lines)


def _build_agent_script(facts: dict[str, Any], eligibility_results: dict[str, dict[str, Any]]) -> str:
    parts = [_build_preamble(facts)]
    for result in eligibility_results.values():
        facts_list = "\n".join(f"  - {circumstance}" for circumstance in result["circumstances"])
        parts.append(f"Regarding {result['name']}:\n{facts_list}")
    return "\n\n".join(parts)


CASE_METADATA_FIELDS = {
    "case_id",
    "rule",
    "variant",
    "expected",
    "children",
    "_unknown_descriptions",
}


def _build_case_facts(raw_case: dict[str, Any], children: dict[str, dict[str, Any]]) -> dict[str, Any]:
    facts: dict[str, Any] = {
        "claimant_lives_in_uk": raw_case.get("uk", raw_case.get("claimant_lives_in_uk", True)),
        "children": children,
        "_unknown_descriptions": raw_case.get("_unknown_descriptions", {}),
    }

    for key, value in raw_case.items():
        if key == "uk" or key in CASE_METADATA_FIELDS:
            continue
        facts[key] = value

    return facts


def _assert_correctness(case_id: str, actual: list[str], expected: list[str]) -> None:
    assert actual == expected, f"\nTEST FAILED: {case_id}\nExpected: {expected}\nActual:   {actual}"


def _generate_cases_from_json(json_filepath: str, *, validate_unspecified: bool) -> list[dict[str, Any]]:
    with (BASE_DIR / json_filepath).open("r", encoding="utf-8") as f:
        raw_cases = json.load(f)

    cases: list[dict[str, Any]] = []
    for raw_case in raw_cases:
        expected = raw_case["expected"]
        children = _build_child_facts(raw_case["children"])
        facts = _build_case_facts(raw_case, children)

        case_id = raw_case.get("case_id") or _generate_case_id(
            raw_case.get("rule", "UNKNOWN"),
            raw_case.get("variant", ""),
            expected,
        )

        _validate_unspecified_case(case_id, facts)

        eligibility_results = evaluate_eligibility(facts)
        actual_outcomes = [result["eligible"] for result in eligibility_results.values()]
        _assert_correctness(case_id, actual_outcomes, expected)

        cases.append(
            {
                "case_id": case_id,
                "content_version": CONTENT_VERSION,
                "facts": _enrich_facts(facts),
                "agent_script": _build_agent_script(facts, eligibility_results),
                "expected_eligibility": eligibility_results,
            }
        )

    return cases


def generate_unspecified_cases(json_filepath: str = "unspecified_cases.json") -> list[dict[str, Any]]:
    return _generate_cases_from_json(json_filepath, validate_unspecified=True)


def generate_uncovered_cases(json_filepath: str = "uncovered_cases.json") -> list[dict[str, Any]]:
    return _generate_cases_from_json(json_filepath, validate_unspecified=False)


def save_cases(all_cases: list[dict[str, Any]], output_path: Path = OUTFILE_NAME) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        "\n".join(json.dumps(case) for case in all_cases) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    # Ugly but avoids circular import in a relatively simple way
    from uncertainty_random import generate_random_uncertainty_variants

    unspecified_cases = generate_unspecified_cases()
    uncovered_cases = generate_uncovered_cases()
    random_variant_cases = generate_random_uncertainty_variants()

    cases = unspecified_cases + uncovered_cases + random_variant_cases
    save_cases(cases)

    total_children = sum(len(case["expected_eligibility"]) for case in cases)
    status_counts = {STATUS_ELIGIBLE: 0, STATUS_INELIGIBLE: 0, STATUS_INDETERMINATE: 0}
    for case in cases:
        for result in case["expected_eligibility"].values():
            status_counts[result["eligible"]] += 1

    print(
        f"Generated {len(cases)} uncertainty cases "
        f"({len(unspecified_cases)} unspecified + "
        f"{len(uncovered_cases)} uncovered + "
        f"{len(random_variant_cases)} random variants)"
    )
    print(f"Total evaluation points (children): {total_children}")
    print(
        f"Eligible: {status_counts[STATUS_ELIGIBLE]}, "
        f"Ineligible: {status_counts[STATUS_INELIGIBLE]}, "
        f"Indeterminate: {status_counts[STATUS_INDETERMINATE]}"
    )


if __name__ == "__main__":
    main()
