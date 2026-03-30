#!/usr/bin/env python3
"""
Manual JSON Schema validation for eligibility specifications.
Checks conformance to eligibility-schema.json without external dependencies.
"""

import json
import sys
from pathlib import Path


def load_json(filepath):
    """Load and parse JSON file."""
    with open(filepath, 'r') as f:
        return json.load(f)


def validate_specification(spec, spec_name):
    """Validate specification against schema requirements."""
    errors = []
    warnings = []

    # Check required top-level fields
    required_fields = ["version", "last_updated", "source", "description", "decision_tree", "constants"]
    for field in required_fields:
        if field not in spec:
            errors.append(f"Missing required field: {field}")

    # Validate decision_tree structure
    if "decision_tree" in spec:
        dt = spec["decision_tree"]

        # Check root node
        if "root" not in dt:
            errors.append("Missing decision_tree.root")
        else:
            root = dt["root"]
            if root.get("type") != "start":
                errors.append(f"Root node type must be 'start', got '{root.get('type')}'")
            if "next" not in root:
                errors.append("Root node missing 'next' field")

        # Check nodes
        if "nodes" not in dt:
            errors.append("Missing decision_tree.nodes")
        else:
            nodes = dt["nodes"]

            # Validate each node
            for node_id, node in nodes.items():
                # Check node has required fields
                if "id" not in node:
                    errors.append(f"Node '{node_id}' missing 'id' field")
                elif node["id"] != node_id:
                    errors.append(f"Node key '{node_id}' doesn't match node.id '{node['id']}'")

                if "type" not in node:
                    errors.append(f"Node '{node_id}' missing 'type' field")
                    continue

                node_type = node["type"]

                # Validate node types
                valid_types = [
                    "boolean_question", "multi_path_check", "salary_check",
                    "financial_check", "occupation_check", "conditional_check",
                    "complex_criteria", "routing", "outcome"
                ]

                if node_type not in valid_types:
                    errors.append(f"Node '{node_id}' has invalid type '{node_type}'")
                    continue

                # Type-specific validation
                if node_type == "outcome":
                    if "result" not in node:
                        errors.append(f"Outcome node '{node_id}' missing 'result' field")
                    else:
                        result = node["result"]
                        valid_results = ["ELIGIBLE", "INELIGIBLE", "DEFERRED"]
                        if result not in valid_results:
                            errors.append(f"Outcome node '{node_id}' has invalid result '{result}', must be one of {valid_results}")

                        # Check result-specific requirements
                        if result == "ELIGIBLE":
                            if "description" not in node:
                                errors.append(f"ELIGIBLE outcome '{node_id}' missing 'description'")
                            if "next_steps" not in node:
                                warnings.append(f"ELIGIBLE outcome '{node_id}' should have 'next_steps'")

                        elif result == "INELIGIBLE":
                            if "reason" not in node:
                                errors.append(f"INELIGIBLE outcome '{node_id}' missing 'reason'")
                            if "guidance" not in node:
                                errors.append(f"INELIGIBLE outcome '{node_id}' missing 'guidance'")

                        elif result == "DEFERRED":
                            if "reason" not in node:
                                errors.append(f"DEFERRED outcome '{node_id}' missing 'reason'")
                            if "guidance" not in node:
                                errors.append(f"DEFERRED outcome '{node_id}' missing 'guidance'")

                elif node_type == "boolean_question":
                    if "question" not in node:
                        errors.append(f"Boolean question '{node_id}' missing 'question'")
                    if "outcomes" not in node:
                        errors.append(f"Boolean question '{node_id}' missing 'outcomes'")
                    elif not isinstance(node["outcomes"], dict):
                        errors.append(f"Boolean question '{node_id}' outcomes must be object")
                    else:
                        outcomes = node["outcomes"]
                        if "yes" not in outcomes:
                            errors.append(f"Boolean question '{node_id}' missing 'yes' outcome")
                        if "no" not in outcomes:
                            errors.append(f"Boolean question '{node_id}' missing 'no' outcome")

                elif node_type == "routing":
                    if "description" not in node:
                        errors.append(f"Routing node '{node_id}' missing 'description'")
                    if "outcomes" not in node:
                        errors.append(f"Routing node '{node_id}' missing 'outcomes'")

                elif node_type in ["salary_check", "financial_check"]:
                    if "question" not in node:
                        errors.append(f"{node_type} '{node_id}' missing 'question'")
                    if "criteria" not in node:
                        errors.append(f"{node_type} '{node_id}' missing 'criteria'")
                    if "outcomes" not in node:
                        errors.append(f"{node_type} '{node_id}' missing 'outcomes'")

                elif node_type in ["multi_path_check", "occupation_check", "conditional_check", "complex_criteria"]:
                    if "question" not in node:
                        errors.append(f"{node_type} '{node_id}' missing 'question'")
                    if "outcomes" not in node:
                        errors.append(f"{node_type} '{node_id}' missing 'outcomes'")

    return errors, warnings


def main():
    """Main validation function."""
    print("=" * 80)
    print("ELIGIBILITY SPECIFICATION SCHEMA VALIDATION")
    print("=" * 80)
    print()

    # Load schema
    schema_path = Path("../schemas/eligibility-schema.json")
    if not schema_path.exists():
        print(f"❌ Schema file not found: {schema_path}")
        return 1

    print(f"✓ Schema loaded: {schema_path}")
    schema = load_json(schema_path)
    print(f"  Schema version: {schema.get('version', 'unknown')}")
    print()

    # Files to validate
    spec_files = [
        "../specifications/skilled_worker_visa/skilled_worker_visa_eligibility.json",
        "../specifications/child_benefit/child_benefit_eligibility.json"
    ]

    all_valid = True

    for spec_file in spec_files:
        print("-" * 80)
        print(f"Validating: {spec_file}")
        print("-" * 80)

        spec_path = Path(spec_file)
        if not spec_path.exists():
            print(f"❌ File not found: {spec_file}")
            all_valid = False
            continue

        try:
            spec = load_json(spec_path)
            print(f"✓ JSON parsed successfully")
            print(f"  Specification version: {spec.get('version', 'unknown')}")
            print(f"  Last updated: {spec.get('last_updated', 'unknown')}")

            # Run validation
            errors, warnings = validate_specification(spec, spec_file)

            if errors:
                print(f"\n❌ VALIDATION FAILED - {len(errors)} error(s):")
                for error in errors:
                    print(f"  • {error}")
                all_valid = False
            else:
                print(f"\n✅ VALIDATION PASSED")

            if warnings:
                print(f"\n⚠️  {len(warnings)} warning(s):")
                for warning in warnings:
                    print(f"  • {warning}")

            # Count nodes
            if "decision_tree" in spec and "nodes" in spec["decision_tree"]:
                node_count = len(spec["decision_tree"]["nodes"])
                outcome_count = sum(1 for n in spec["decision_tree"]["nodes"].values()
                                  if n.get("type") == "outcome")
                print(f"\n📊 Statistics:")
                print(f"  • Total nodes: {node_count}")
                print(f"  • Outcome nodes: {outcome_count}")
                print(f"  • Decision nodes: {node_count - outcome_count}")

                # Count outcome types
                results = {}
                for node in spec["decision_tree"]["nodes"].values():
                    if node.get("type") == "outcome":
                        result = node.get("result", "UNKNOWN")
                        results[result] = results.get(result, 0) + 1

                if results:
                    print(f"  • Outcome breakdown:")
                    for result, count in sorted(results.items()):
                        print(f"    - {result}: {count}")

            print()

        except json.JSONDecodeError as e:
            print(f"❌ JSON parsing error: {e}")
            all_valid = False
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            all_valid = False

    print("=" * 80)
    if all_valid:
        print("✅ ALL SPECIFICATIONS VALID")
        print("=" * 80)
        return 0
    else:
        print("❌ VALIDATION FAILED")
        print("=" * 80)
        return 1


if __name__ == "__main__":
    sys.exit(main())
