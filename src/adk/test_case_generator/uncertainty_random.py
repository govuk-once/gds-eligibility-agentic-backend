import json
import random
from copy import deepcopy
from pathlib import Path
from typing import Any

from generate_uncertainty_cases import (
    CB_WEEKLY_RATE,
    RANDOM_GENERATION_CONFIG,
    STATUS_INDETERMINATE,
    _assert_correctness,
    _build_agent_script,
    _build_child_facts,
    _enrich_facts,
    _generate_case_id,
    _validate_unspecified_case,
    evaluate_eligibility,
)

BASE_DIR = Path(__file__).resolve().parent

RANDOM_VARIANT_TARGET_TOTAL = 100
RANDOM_VARIANT_SEED = 146

RIGHT_TO_RESIDE_VARIANTS = [
    "unclear right-to-reside position",
    "right-to-reside position not yet confirmed",
    "right-to-reside position still being checked",
    "right-to-reside position is not known",
    "right-to-reside position is uncertain",
    "right-to-reside position has not been established",
    "right-to-reside position is awaiting confirmation",
    "right-to-reside position has not yet been assessed",
    "right-to-reside position is under review",
    "right-to-reside position is unclear from the information available",
    "right-to-reside position is not something the claimant can confirm",
    "right-to-reside position has not been confirmed by anyone official",
]

APPRENTICESHIP_LOCATION_VARIANTS = [
    "Wales",
    "Cardiff, Wales",
    "Swansea, Wales",
    "Newport, Wales",
    "Wrexham, Wales",
    "Scotland",
    "Edinburgh, Scotland",
    "Glasgow, Scotland",
    "Aberdeen, Scotland",
    "Dundee, Scotland",
    "Northern Ireland",
    "Belfast, Northern Ireland",
    "Derry, Northern Ireland",
    "Lisburn, Northern Ireland",
    "Newry, Northern Ireland",
]

def _assert_contains_indeterminate(case_id: str, outcomes: list[str]) -> None:
    """
    We need this because we're adding some True/False outcomes for additional children
    in with the indeterminate cases.
    """
    assert STATUS_INDETERMINATE in outcomes, (
        f"\nTEST FAILED: {case_id}\n"
        "Expected uncertainty case to contain at least one INDETERMINATE outcome\n"
        f"Actual:   {outcomes}"
    )

def _load_raw_cases_with_source() -> list[dict[str, Any]]:
    cases: list[dict[str, Any]] = []

    for filepath in ["unspecified_cases.json", "uncovered_cases.json"]:
        path = BASE_DIR / filepath
        if not path.exists():
            raise FileNotFoundError(f"Required uncertainty input file not found: {path}")

        with path.open("r", encoding="utf-8") as f:
            raw_cases = json.load(f)

        for raw_case in raw_cases:
            case_id = _base_case_id(raw_case)
            _assert_contains_indeterminate(case_id, raw_case["expected"])
            cases.append(raw_case)

    assert cases, "No uncertainty source cases were loaded"

    return cases

def _facts_from_raw_case(raw_case: dict[str, Any]) -> dict[str, Any]:
    children = _build_child_facts(raw_case["children"])

    facts = {
        "claimant_lives_in_uk": raw_case.get(
            "uk",
            raw_case.get("claimant_lives_in_uk", True),
        ),
        "children": children,
        "_unknown_descriptions": raw_case.get("_unknown_descriptions", {}),
    }

    for key, value in raw_case.items():
        if key not in {
            "case_id",
            "rule",
            "variant",
            "expected",
            "children",
            "uk",
            "_unknown_descriptions",
        }:
            facts[key] = value

    return facts


def _case_payload_from_raw_case(raw_case: dict[str, Any]) -> dict[str, Any]:
    expected = raw_case["expected"]
    facts = _facts_from_raw_case(raw_case)

    case_id = raw_case.get("case_id") or _generate_case_id(
        raw_case.get("rule", "UNKNOWN"),
        raw_case.get("variant", ""),
        expected,
    )

    _validate_unspecified_case(case_id, facts)

    eligibility_results = evaluate_eligibility(facts)
    actual_outcomes = [result["eligible"] for result in eligibility_results.values()]

    _assert_correctness(case_id, actual_outcomes, expected)
    _assert_contains_indeterminate(case_id, actual_outcomes)

    return {
        "case_id": case_id,
        "facts": _enrich_facts(facts),
        "agent_script": _build_agent_script(facts, eligibility_results),
        "expected_eligibility": eligibility_results,
    }


def _base_case_id(raw_case: dict[str, Any]) -> str:
    return raw_case.get("case_id") or _generate_case_id(
        raw_case.get("rule", "UNKNOWN"),
        raw_case.get("variant", ""),
        raw_case["expected"],
    )


def _generate_random_child(rng: random.Random) -> dict[str, Any]:
    """
    Generate a random determinate child profile.

    This mirrors the random child generation in generate_test_cases.py, but
    returns raw child facts. IDs and names are assigned later by _build_child_facts().
    """
    cfg = RANDOM_GENERATION_CONFIG

    age = rng.randint(cfg["age_range"][0], cfg["age_range"][1])
    lives_with = rng.random() < cfg["prob_lives_with_claimant"]

    child: dict[str, Any] = {
        "age": age,
        "lives_with_claimant": lives_with,
    }

    # Education / extension: only relevant for 16-19.
    if cfg["min_age_post_16_rules"] <= age < cfg["age_education_cutoff"]:
        child["in_approved_education"] = rng.random() < cfg["prob_education"]
        if not child["in_approved_education"] and age <= cfg["max_age_extension"]:
            child["in_extension_period"] = rng.random() < cfg["prob_extension"]

    # Responsibility details.
    if not lives_with:
        child["upkeep_per_week"] = rng.choice(cfg["upkeep_amounts"])
        child["another_claimant_lives_with_child"] = (
            rng.random() < cfg["prob_another_claimant_lives_with_child"]
        )
    else:
        if rng.random() < cfg["prob_another_claimant_priority"]:
            child["another_claimant_has_priority"] = True

    # Care absence.
    if rng.random() < cfg["prob_care"]:
        child["care_weeks"] = rng.choice(cfg["care_weeks"])
        child["care_home_24h_per_week"] = rng.random() < cfg["prob_care_home_24h"]

    # Hospital absence.
    if rng.random() < cfg["prob_hospital"]:
        child["hospital_weeks"] = rng.choice(cfg["hospital_weeks"])
        child["claimant_spends_on_child"] = rng.random() < cfg["prob_hospital_spending"]

    # Fostering.
    if rng.random() < cfg["prob_foster"]:
        child["is_fostered"] = True
        child["council_pays_for_child"] = rng.random() < cfg["prob_council_pays"]

    # Work, apprenticeship, and benefits: only for older children.
    if age >= cfg["min_age_post_16_rules"]:
        if rng.random() < cfg["prob_work_24_plus"]:
            child["works_24_plus_hours"] = True

        if rng.random() < cfg["prob_apprenticeship"]:
            child["started_apprenticeship_in_england"] = True
            child["in_approved_education"] = False
            child["in_extension_period"] = False

        if rng.random() < cfg["prob_qualifying_benefits"]:
            child["receives_qualifying_benefits"] = True

    return child

def _has_unknown(child: dict[str, Any], field: str) -> bool:
    return field in child and child[field] is None


def _set_under_16_eligible_age(child: dict[str, Any], rng: random.Random) -> None:
    child["age"] = rng.choice([3, 5, 8, 11, 15])
    child["in_approved_education"] = False
    child["in_extension_period"] = False
    child["works_24_plus_hours"] = False
    child["started_apprenticeship_in_england"] = False
    child["receives_qualifying_benefits"] = False
    child.pop("apprenticeship_location", None)


def _set_16_to_19_eligible_age(child: dict[str, Any], rng: random.Random) -> None:
    child["age"] = rng.choice([16, 17, 18, 19])
    child["in_approved_education"] = True
    child["in_extension_period"] = False
    child["works_24_plus_hours"] = False
    child["started_apprenticeship_in_england"] = False
    child["receives_qualifying_benefits"] = False


def _randomise_age_safely(child: dict[str, Any], rng: random.Random) -> None:
    if _has_unknown(child, "age"):
        return

    if _has_unknown(child, "in_approved_education"):
        child["age"] = rng.choice([16, 17, 18, 19])
        child["in_extension_period"] = False
        child["works_24_plus_hours"] = False
        child["started_apprenticeship_in_england"] = False
        child["receives_qualifying_benefits"] = False
        child.pop("apprenticeship_location", None)
        return

    if _has_unknown(child, "in_extension_period"):
        child["age"] = rng.choice([16, 17])
        child["in_approved_education"] = False
        child["works_24_plus_hours"] = False
        child["started_apprenticeship_in_england"] = False
        child["receives_qualifying_benefits"] = False
        child.pop("apprenticeship_location", None)
        return

    if _has_unknown(child, "works_24_plus_hours"):
        child["age"] = rng.choice([16, 17, 18, 19])
        child["in_approved_education"] = True
        child["in_extension_period"] = False
        child["started_apprenticeship_in_england"] = False
        child["receives_qualifying_benefits"] = False
        child.pop("apprenticeship_location", None)
        return

    if _has_unknown(child, "started_apprenticeship_in_england"):
        child["age"] = rng.choice([16, 17, 18, 19])
        child["in_approved_education"] = False
        child["in_extension_period"] = False
        child["works_24_plus_hours"] = False
        child["receives_qualifying_benefits"] = False
        child.pop("apprenticeship_location", None)
        return

    if _has_unknown(child, "receives_qualifying_benefits"):
        child["age"] = rng.choice([16, 17, 18, 19])
        child["in_approved_education"] = True
        child["in_extension_period"] = False
        child["works_24_plus_hours"] = False
        child["started_apprenticeship_in_england"] = False
        child.pop("apprenticeship_location", None)
        return

    if child.get("apprenticeship_location"):
        child["age"] = rng.choice([16, 17, 18, 19])
        child["in_approved_education"] = False
        child["in_extension_period"] = False
        child["works_24_plus_hours"] = False
        child["started_apprenticeship_in_england"] = False
        child["receives_qualifying_benefits"] = False
        child["apprenticeship_location"] = rng.choice(APPRENTICESHIP_LOCATION_VARIANTS)
        return

    if rng.random() < 0.75:
        _set_under_16_eligible_age(child, rng)
    else:
        _set_16_to_19_eligible_age(child, rng)


def _responsibility_is_uncertainty_trigger(child: dict[str, Any]) -> bool:
    return any(
        _has_unknown(child, field)
        for field in [
            "lives_with_claimant",
            "upkeep_per_week",
            "another_claimant_has_priority",
            "another_claimant_lives_with_child",
        ]
    )


def _has_special_relationship_trigger(child: dict[str, Any]) -> bool:
    return bool(
        child.get("informal_arrangement")
        or child.get("claimant_dispute_unresolved")
        or child.get("is_adopting")
        or child.get("is_fostered")
        or _has_unknown(child, "is_fostered")
        or _has_unknown(child, "council_pays_for_child")
    )


def _randomise_responsibility_safely(child: dict[str, Any], rng: random.Random) -> None:
    if _responsibility_is_uncertainty_trigger(child):
        return

    if _has_special_relationship_trigger(child):
        return

    if rng.random() < 0.7:
        child["lives_with_claimant"] = True
        child["upkeep_per_week"] = 0.0
        child["another_claimant_has_priority"] = False
        child["another_claimant_lives_with_child"] = False
    else:
        child["lives_with_claimant"] = False
        child["upkeep_per_week"] = rng.choice([CB_WEEKLY_RATE, 30.0, 50.0])
        child["another_claimant_lives_with_child"] = False
        child["another_claimant_has_priority"] = False


def _claimant_residency_is_unknown(raw_case: dict[str, Any]) -> bool:
    if "uk" in raw_case:
        return raw_case["uk"] is None
    if "claimant_lives_in_uk" in raw_case:
        return raw_case["claimant_lives_in_uk"] is None
    return False


def _randomise_case_level_fields_safely(
    raw_case: dict[str, Any],
    rng: random.Random,
) -> None:
    if _claimant_residency_is_unknown(raw_case):
        return

    # Keep explicit living-abroad uncovered cases as living-abroad cases.
    if raw_case.get("country"):
        return

    if raw_case.get("recently_moved_to_uk") is True:
        raw_case["claimant_lives_in_uk"] = True
        raw_case.pop("uk", None)
        raw_case["right_to_reside_status"] = rng.choice(RIGHT_TO_RESIDE_VARIANTS)
        return

    if raw_case.get("eu_status") == "pre_settled":
        raw_case["claimant_lives_in_uk"] = True
        raw_case.pop("uk", None)
        return

    raw_case["claimant_lives_in_uk"] = True
    raw_case.pop("uk", None)


def _randomise_child_fields_safely(
    raw_case: dict[str, Any],
    rng: random.Random,
) -> None:
    for i, child in enumerate(raw_case["children"]):
        _randomise_age_safely(child, rng)
        _randomise_responsibility_safely(child, rng)

        if not (
            _has_unknown(child, "care_weeks")
            or _has_unknown(child, "care_home_24h_per_week")
        ):
            child.setdefault("care_weeks", 0)
            child.setdefault("care_home_24h_per_week", False)

        if not (
            _has_unknown(child, "hospital_weeks")
            or _has_unknown(child, "claimant_spends_on_child")
            or child.get("hospital_abroad")
        ):
            child.setdefault("hospital_weeks", 0)
            child.setdefault("claimant_spends_on_child", False)


def _add_random_extra_children(
    raw_case: dict[str, Any],
    rng: random.Random,
) -> None:
    """
    Add random extra children to some variants.

    The reviewed child or children remain in place. Extra children are generated
    using the same kind of random child logic as the standard known-case generator.
    Their expected outcomes are assigned later by evaluating the full case.
    """
    cfg = RANDOM_GENERATION_CONFIG

    current_children = len(raw_case["children"])

    target_children = rng.choices(
        cfg["num_children_choices"],
        weights=cfg["num_children_weights"],
    )[0]

    if target_children <= current_children:
        return

    max_supported_children = len(cfg["names"])
    target_children = min(target_children, max_supported_children)

    while len(raw_case["children"]) < target_children:
        raw_case["children"].append(_generate_random_child(rng))

def _set_expected_outcomes_after_extra_children(
    raw_case: dict[str, Any],
    *,
    original_expected: list[str],
) -> None:
    """
    Set expected outcomes after adding random extra children.

    The original reviewed children must still produce their original expected
    outcomes. This catches mistakes where randomisation accidentally destroys
    the uncertainty trigger.

    Extra children get their expected outcomes from the uncertainty evaluator,
    because claimant-level uncertainty may affect them too.
    """
    facts = _facts_from_raw_case(raw_case)
    case_id = raw_case.get("case_id") or _generate_case_id(
        raw_case.get("rule", "UNKNOWN"),
        raw_case.get("variant", ""),
        original_expected,
    )

    _validate_unspecified_case(case_id, facts)

    eligibility_results = evaluate_eligibility(facts)
    actual_outcomes = [result["eligible"] for result in eligibility_results.values()]

    original_child_count = len(original_expected)
    actual_for_original_children = actual_outcomes[:original_child_count]

    # Non-circular check: the reviewed uncertainty child or children still
    # produce the manually specified expected outcomes.
    _assert_correctness(
        case_id,
        actual_for_original_children,
        original_expected,
    )

    # Case-level check: even after adding extra True/False children, this must
    # still be an uncertainty case overall.
    _assert_contains_indeterminate(case_id, actual_outcomes)

    raw_case["expected"] = actual_outcomes


def _make_random_variant_raw_case(
    raw_case: dict[str, Any],
    *,
    variant_number: int,
    rng: random.Random,
) -> dict[str, Any]:
    variant = deepcopy(raw_case)
    base_id = _base_case_id(raw_case)
    original_expected = list(raw_case["expected"])

    variant["case_id"] = f"{base_id}_RND_{variant_number:03d}"
    variant["expected"] = original_expected

    _randomise_case_level_fields_safely(variant, rng)
    _randomise_child_fields_safely(variant, rng)
    _add_random_extra_children(variant, rng)
    _set_expected_outcomes_after_extra_children(
        variant,
        original_expected=original_expected,
    )

    return variant

def generate_random_uncertainty_variants(
    *,
    target_total_cases: int = RANDOM_VARIANT_TARGET_TOTAL,
    seed: int = RANDOM_VARIANT_SEED,
) -> list[dict[str, Any]]:
    rng = random.Random(seed)
    raw_cases = _load_raw_cases_with_source()

    canonical_count = len(raw_cases)
    variants_needed = max(0, target_total_cases - canonical_count)

    variant_payloads: list[dict[str, Any]] = []

    for i in range(variants_needed):
        raw_case = raw_cases[i % canonical_count]
        variant_raw_case = _make_random_variant_raw_case(
            raw_case,
            variant_number=i + 1,
            rng=rng,
        )
        variant_payloads.append(_case_payload_from_raw_case(variant_raw_case))

    return variant_payloads
