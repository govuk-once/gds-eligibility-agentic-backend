#!/usr/bin/env python3
"""
Orphan Node Detector for Eligibility Specifications.
Identifies nodes that are defined but never referenced in the decision tree.
"""

import json
import sys
from pathlib import Path
from collections import defaultdict


def load_json(filepath):
    """Load and parse JSON file."""
    with open(filepath, 'r') as f:
        return json.load(f)


def find_orphan_nodes(spec, spec_name):
    """Find nodes that are defined but never referenced."""

    if "decision_tree" not in spec:
        return [], "Missing decision_tree"

    dt = spec["decision_tree"]

    if "nodes" not in dt:
        return [], "Missing decision_tree.nodes"

    nodes = dt["nodes"]
    all_node_ids = set(nodes.keys())
    referenced_ids = set()

    # Track which nodes reference each node (for reporting)
    referenced_by = defaultdict(list)

    # Add root's next node as referenced
    if "root" in dt and "next" in dt["root"]:
        root_next = dt["root"]["next"]
        referenced_ids.add(root_next)
        referenced_by[root_next].append("root")

    # Scan all nodes for references
    for node_id, node in nodes.items():
        node_type = node.get("type")

        # Boolean questions
        if node_type == "boolean_question":
            if "outcomes" in node:
                for outcome_key, target in node["outcomes"].items():
                    referenced_ids.add(target)
                    referenced_by[target].append(f"{node_id}.outcomes.{outcome_key}")

        # Multi-path checks
        elif node_type == "multi_path_check":
            if "outcomes" in node:
                for outcome_key, target in node["outcomes"].items():
                    referenced_ids.add(target)
                    referenced_by[target].append(f"{node_id}.outcomes.{outcome_key}")

        # Salary checks
        elif node_type == "salary_check":
            if "outcomes" in node:
                for outcome_key, target in node["outcomes"].items():
                    referenced_ids.add(target)
                    referenced_by[target].append(f"{node_id}.outcomes.{outcome_key}")

        # Financial checks
        elif node_type == "financial_check":
            if "outcomes" in node:
                for outcome_key, target in node["outcomes"].items():
                    referenced_ids.add(target)
                    referenced_by[target].append(f"{node_id}.outcomes.{outcome_key}")

        # Occupation checks
        elif node_type == "occupation_check":
            if "outcomes" in node:
                for outcome_key, target in node["outcomes"].items():
                    referenced_ids.add(target)
                    referenced_by[target].append(f"{node_id}.outcomes.{outcome_key}")

        # Conditional checks
        elif node_type == "conditional_check":
            if "outcomes" in node:
                for outcome_key, target in node["outcomes"].items():
                    referenced_ids.add(target)
                    referenced_by[target].append(f"{node_id}.outcomes.{outcome_key}")

        # Complex criteria
        elif node_type == "complex_criteria":
            if "outcomes" in node:
                for outcome_key, target in node["outcomes"].items():
                    referenced_ids.add(target)
                    referenced_by[target].append(f"{node_id}.outcomes.{outcome_key}")

        # Routing nodes
        elif node_type == "routing":
            if "outcomes" in node:
                for outcome_key, target in node["outcomes"].items():
                    referenced_ids.add(target)
                    referenced_by[target].append(f"{node_id}.outcomes.{outcome_key}")

        # Outcome nodes should not reference other nodes
        elif node_type == "outcome":
            pass  # Terminal nodes

    # Find orphans
    orphan_ids = all_node_ids - referenced_ids

    # Build detailed report
    orphan_details = []
    for orphan_id in sorted(orphan_ids):
        node = nodes[orphan_id]
        node_type = node.get("type", "unknown")

        # Get node description/question for context
        context = ""
        if "question" in node:
            context = node["question"][:60] + "..." if len(node["question"]) > 60 else node["question"]
        elif "description" in node:
            context = node["description"][:60] + "..." if len(node["description"]) > 60 else node["description"]
        elif "result" in node:
            context = f"Result: {node['result']}"

        orphan_details.append({
            "id": orphan_id,
            "type": node_type,
            "context": context
        })

    return orphan_details, referenced_by


def check_unreferenced_ids(spec, spec_name):
    """Find references to non-existent nodes."""

    if "decision_tree" not in spec:
        return []

    dt = spec["decision_tree"]

    if "nodes" not in dt:
        return []

    nodes = dt["nodes"]
    all_node_ids = set(nodes.keys())
    dangling_refs = []

    # Check root
    if "root" in dt and "next" in dt["root"]:
        root_next = dt["root"]["next"]
        if root_next not in all_node_ids:
            dangling_refs.append(f"root.next -> '{root_next}' (node does not exist)")

    # Check all node references
    for node_id, node in nodes.items():
        node_type = node.get("type")

        if "outcomes" in node and isinstance(node["outcomes"], dict):
            for outcome_key, target in node["outcomes"].items():
                if target not in all_node_ids:
                    dangling_refs.append(f"{node_id}.outcomes.{outcome_key} -> '{target}' (node does not exist)")

    return dangling_refs


def main():
    """Main orphan detection function."""
    print("=" * 80)
    print("ORPHAN NODE DETECTION")
    print("=" * 80)
    print()

    spec_files = [
        "../specifications/skilled_worker_visa/skilled_worker_visa_eligibility.json",
        "../specifications/child_benefit/child_benefit_eligibility.json"
    ]

    all_clean = True

    for spec_file in spec_files:
        print("-" * 80)
        print(f"Analyzing: {spec_file}")
        print("-" * 80)

        spec_path = Path(spec_file)
        if not spec_path.exists():
            print(f"❌ File not found: {spec_file}")
            all_clean = False
            continue

        try:
            spec = load_json(spec_path)
            print(f"✓ Loaded {spec_file} v{spec.get('version', 'unknown')}")

            # Find orphan nodes
            orphans, referenced_by = find_orphan_nodes(spec, spec_file)

            # Find dangling references
            dangling = check_unreferenced_ids(spec, spec_file)

            # Report results
            if orphans:
                print(f"\n❌ FOUND {len(orphans)} ORPHAN NODE(S):")
                print()
                for orphan in orphans:
                    print(f"  • {orphan['id']}")
                    print(f"    Type: {orphan['type']}")
                    if orphan['context']:
                        print(f"    Context: {orphan['context']}")
                    print()
                all_clean = False
            else:
                print(f"\n✅ NO ORPHAN NODES")

            if dangling:
                print(f"\n❌ FOUND {len(dangling)} DANGLING REFERENCE(S):")
                for ref in dangling:
                    print(f"  • {ref}")
                all_clean = False
            else:
                print(f"✅ NO DANGLING REFERENCES")

            # Statistics
            if "decision_tree" in spec and "nodes" in spec["decision_tree"]:
                total_nodes = len(spec["decision_tree"]["nodes"])
                referenced_count = total_nodes - len(orphans)
                print(f"\n📊 Statistics:")
                print(f"  • Total nodes: {total_nodes}")
                print(f"  • Referenced nodes: {referenced_count}")
                print(f"  • Orphan nodes: {len(orphans)}")
                print(f"  • Dangling references: {len(dangling)}")

            print()

        except json.JSONDecodeError as e:
            print(f"❌ JSON parsing error: {e}")
            all_clean = False
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            import traceback
            traceback.print_exc()
            all_clean = False

    print("=" * 80)
    if all_clean:
        print("✅ ALL SPECIFICATIONS CLEAN - NO ORPHAN NODES")
        print("=" * 80)
        return 0
    else:
        print("❌ ORPHAN NODES OR DANGLING REFERENCES DETECTED")
        print("=" * 80)
        return 1


if __name__ == "__main__":
    sys.exit(main())
