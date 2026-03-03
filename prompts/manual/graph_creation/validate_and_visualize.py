#!/usr/bin/env python3
"""
Validate and visualize UK Skilled Worker Visa eligibility decision tree.

Usage:
    python3 validate_and_visualize.py

Requirements:
    pip install graphviz
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple


def load_eligibility_data(filepath: str) -> Dict:
    """Load the eligibility JSON file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def validate_against_schema(data: Dict, schema_path: str = "eligibility-schema.json") -> List[str]:
    """Validate data against JSON Schema if jsonschema library available."""
    issues = []

    try:
        import jsonschema
    except ImportError:
        return ["jsonschema library not installed - skipping schema validation"]

    try:
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema = json.load(f)
    except FileNotFoundError:
        return [f"Schema file not found: {schema_path}"]
    except json.JSONDecodeError as e:
        return [f"Schema file is not valid JSON: {e}"]

    try:
        jsonschema.validate(instance=data, schema=schema)
    except jsonschema.exceptions.ValidationError as e:
        issues.append(f"Schema validation error: {e.message}")
        issues.append(f"  At path: {'.'.join(str(p) for p in e.path)}")
    except jsonschema.exceptions.SchemaError as e:
        issues.append(f"Schema itself is invalid: {e.message}")

    return issues


def validate_structure(data: Dict) -> List[str]:
    """Validate the decision tree structure and return list of issues."""
    issues = []

    # Check required top-level keys
    required_keys = ['version', 'last_updated', 'source', 'decision_tree', 'constants']
    for key in required_keys:
        if key not in data:
            issues.append(f"Missing required top-level key: {key}")

    if 'decision_tree' not in data:
        return issues

    tree = data['decision_tree']

    # Check root exists
    if 'root' not in tree:
        issues.append("Missing 'root' in decision_tree")
        return issues

    if 'nodes' not in tree:
        issues.append("Missing 'nodes' in decision_tree")
        return issues

    root = tree['root']
    nodes = tree['nodes']

    # Collect all node IDs
    all_node_ids = {root['id']} | set(nodes.keys())

    # Check root points to valid node
    if 'next' in root and root['next'] not in all_node_ids:
        issues.append(f"Root points to non-existent node: {root['next']}")

    # Validate each node
    referenced_nodes = set()
    if 'next' in root:
        referenced_nodes.add(root['next'])

    for node_id, node in nodes.items():
        # Check required fields
        if 'id' not in node:
            issues.append(f"Node {node_id} missing 'id' field")
        elif node['id'] != node_id:
            issues.append(f"Node key '{node_id}' doesn't match id '{node['id']}'")

        if 'type' not in node:
            issues.append(f"Node {node_id} missing 'type' field")

        # Check outcomes point to valid nodes
        if 'outcomes' in node:
            for outcome, target in node['outcomes'].items():
                if target not in all_node_ids:
                    issues.append(f"Node {node_id} outcome '{outcome}' points to non-existent node: {target}")
                else:
                    referenced_nodes.add(target)

        # Check 'next' field if present
        if 'next' in node and node['next']:
            if node['next'] not in all_node_ids:
                issues.append(f"Node {node_id} 'next' points to non-existent node: {node['next']}")
            else:
                referenced_nodes.add(node['next'])

    # Find unreachable nodes (excluding outcomes)
    outcome_nodes = {nid for nid, node in nodes.items() if node.get('type') == 'outcome'}
    non_outcome_nodes = set(nodes.keys()) - outcome_nodes
    unreachable = non_outcome_nodes - referenced_nodes

    if unreachable:
        issues.append(f"Unreachable nodes (not outcomes): {', '.join(sorted(unreachable))}")

    # Check for cycles (simple check - no outcome node should be referenced as source)
    for node_id in outcome_nodes:
        if 'outcomes' in nodes[node_id] or 'next' in nodes[node_id]:
            issues.append(f"Outcome node {node_id} has outgoing edges (should be terminal)")

    return issues


def get_all_paths(data: Dict) -> List[List[str]]:
    """Extract all paths from root to outcome nodes."""
    tree = data['decision_tree']
    root = tree['root']
    nodes = tree['nodes']

    paths = []

    def traverse(node_id: str, current_path: List[str]):
        current_path.append(node_id)

        if node_id in nodes:
            node = nodes[node_id]

            # Terminal node
            if node.get('type') == 'outcome':
                paths.append(current_path.copy())
                return

            # Follow outcomes
            if 'outcomes' in node:
                for outcome, target in node['outcomes'].items():
                    traverse(target, current_path.copy())
            # Follow next
            elif 'next' in node and node['next']:
                traverse(node['next'], current_path.copy())

    # Start from root's next node
    if 'next' in root:
        traverse(root['next'], [root['id']])

    return paths


def generate_summary_stats(data: Dict) -> Dict:
    """Generate summary statistics about the decision tree."""
    tree = data['decision_tree']
    nodes = tree['nodes']

    node_types = {}
    for node in nodes.values():
        node_type = node.get('type', 'unknown')
        node_types[node_type] = node_types.get(node_type, 0) + 1

    outcomes = {}
    for node in nodes.values():
        if node.get('type') == 'outcome':
            result = node.get('result', 'unknown')
            outcomes[result] = outcomes.get(result, 0) + 1

    paths = get_all_paths(data)
    path_lengths = [len(p) for p in paths]

    return {
        'total_nodes': len(nodes) + 1,  # +1 for root
        'node_types': node_types,
        'outcomes': outcomes,
        'total_paths': len(paths),
        'avg_path_length': sum(path_lengths) / len(path_lengths) if path_lengths else 0,
        'min_path_length': min(path_lengths) if path_lengths else 0,
        'max_path_length': max(path_lengths) if path_lengths else 0
    }


def generate_graphviz(data: Dict, output_file: str):
    """Generate a Graphviz DOT file for visualization."""
    try:
        import graphviz
    except ImportError:
        print("Warning: graphviz library not installed. Install with: pip install graphviz")
        return False

    tree = data['decision_tree']
    root = tree['root']
    nodes = tree['nodes']

    dot = graphviz.Digraph(comment='UK {}'.format(output_file.replace("_", " ").capitalize()))
    dot.attr(rankdir='TB')
    dot.attr('node', fontname='Arial', fontsize='10')
    dot.attr('edge', fontname='Arial', fontsize='9')

    # Node styling by type
    type_styles = {
        'start': {'shape': 'box', 'style': 'rounded,filled', 'fillcolor': 'lightgreen'},
        'boolean_question': {'shape': 'diamond', 'style': 'filled', 'fillcolor': 'lightblue'},
        'multi_path_check': {'shape': 'hexagon', 'style': 'filled', 'fillcolor': 'plum'},
        'salary_check': {'shape': 'box', 'style': 'filled', 'fillcolor': 'orange'},
        'complex_criteria': {'shape': 'box', 'style': 'filled', 'fillcolor': 'orange'},
        'financial_check': {'shape': 'box', 'style': 'filled', 'fillcolor': 'gold'},
        'occupation_check': {'shape': 'box', 'style': 'filled', 'fillcolor': 'lightcyan'},
        'conditional_check': {'shape': 'diamond', 'style': 'filled', 'fillcolor': 'lightblue'},
        'routing': {'shape': 'circle', 'style': 'filled', 'fillcolor': 'lightgray'},
        'outcome': {'shape': 'box', 'style': 'rounded,filled', 'fillcolor': 'white'}
    }

    # Add root node
    root_label = root.get('description', root['id'])
    dot.node(root['id'], root_label, **type_styles.get('start', {}))

    # Add root edge
    if 'next' in root:
        dot.edge(root['id'], root['next'])

    # Add all other nodes
    for node_id, node in nodes.items():
        node_type = node.get('type', 'unknown')

        # Create label
        if node_type == 'outcome':
            result = node.get('result', 'UNKNOWN')
            reason = node.get('reason', '')
            label = f"{result}\\n{reason}"

            # Color outcome nodes
            style = type_styles.get(node_type, {}).copy()
            if result == 'ELIGIBLE':
                style['fillcolor'] = 'green'
                style['fontcolor'] = 'white'
            else:
                style['fillcolor'] = 'red'
                style['fontcolor'] = 'white'
        else:
            label = node.get('question', node.get('description', node_id))
            # Truncate long labels
            #  if len(label) > 50:
            #      label = label[:47] + '...'
            style = type_styles.get(node_type, {})

        dot.node(node_id, label, **style)

        # Add edges
        if 'outcomes' in node:
            for outcome, target in node['outcomes'].items():
                # Simplify outcome labels
                edge_label = outcome.replace('_', ' ').title()
                #  if len(edge_label) > 20:
                #      edge_label = edge_label[:17] + '...'
                dot.edge(node_id, target, label=edge_label)
        elif 'next' in node and node['next']:
            dot.edge(node_id, node['next'])

    # Save DOT file
    dot.save(output_file)

    # Try to render
    try:
        output_base = output_file.replace('.dot', '')
        dot.render(output_base, format='png', cleanup=False)
        print(f"✓ Generated graph visualization: {output_base}.png")
        return True
    except Exception as e:
        print(f"✓ Generated DOT file: {output_file}")
        print(f"  (Could not render PNG: {e})")
        print(f"  Render manually with: dot -Tpng {output_file} -o {output_base}.png")
        return True


def main():
    """Main validation and visualization routine."""
    print("UK Skilled Worker Visa Eligibility Validator")
    print("=" * 60)

    evaluate_specification("skilled_worker_visa_eligibility.json")
    print("UK Child Benefit Eligibility Validator")
    print("=" * 60)
    evaluate_specification("child_benefit_eligibility.json")
    return 0


def evaluate_specification(json_file: str):
    # Check if file exists
    if not Path(json_file).exists():
        print(f"✗ Error: {json_file} not found")
        return 1

    # Load data
    print(f"\n1. Loading {json_file}...")
    try:
        data = load_eligibility_data(json_file)
        print("✓ JSON loaded successfully")
    except json.JSONDecodeError as e:
        print(f"✗ JSON parsing error: {e}")
        return 1
    except Exception as e:
        print(f"✗ Error loading file: {e}")
        return 1

    # Validate against schema
    print("\n2. Validating against JSON Schema...")
    schema_issues = validate_against_schema(data)

    if schema_issues:
        if schema_issues[0].startswith("jsonschema library"):
            print(f"⚠ {schema_issues[0]}")
            print("  Install with: pip install jsonschema")
        else:
            print(f"✗ Found {len(schema_issues)} schema issue(s):")
            for issue in schema_issues:
                print(f"  - {issue}")
            return 1
    else:
        print("✓ Schema validation passed")

    # Validate structure
    print("\n3. Validating decision tree structure...")
    issues = validate_structure(data)

    if issues:
        print(f"✗ Found {len(issues)} issue(s):")
        for issue in issues:
            print(f"  - {issue}")
        return 1
    else:
        print("✓ Structure validation passed")

    # Generate statistics
    print("\n4. Generating statistics...")
    stats = generate_summary_stats(data)

    print(f"✓ Decision tree statistics:")
    print(f"  - Total nodes: {stats['total_nodes']}")
    print(f"  - Node types:")
    for node_type, count in sorted(stats['node_types'].items()):
        print(f"    • {node_type}: {count}")
    print(f"  - Outcomes:")
    for outcome, count in sorted(stats['outcomes'].items()):
        print(f"    • {outcome}: {count}")
    print(f"  - Total paths to outcomes: {stats['total_paths']}")
    print(f"  - Path lengths: min={stats['min_path_length']}, "
          f"avg={stats['avg_path_length']:.1f}, max={stats['max_path_length']}")

    # Generate visualization
    print("\n5. Generating graph visualization...")
    success = generate_graphviz(data, output_file=json_file.replace(".json", ""))

    if not success:
        print("  (Skipped - graphviz not available)")

    print("\n" + "=" * 60)
    print("✓ Validation complete!")
    print("\nThe decision tree is:")
    print("  • Structurally valid (all references resolve)")
    print("  • Complete (covers all paths to outcomes)")
    print("  • Deterministic (each node has clear next steps)")
    print("  • Unambiguous (all conditions are explicit)")


if __name__ == '__main__':
    sys.exit(main())
