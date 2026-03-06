#!/usr/bin/env python3
"""
Validation script to check the specification path and agent setup.
"""

from pathlib import Path
import json
import sys


def validate_specification_path():
    """Check if the specification file exists and is valid."""
    print("="*60)
    print("Validating Child Benefit Specification")
    print("="*60 + "\n")
    
    # Calculate the path from this script to the specification
    current_file = Path(__file__).resolve()
    print(f"Current script: {current_file}")
    
    # From src/adk/gds_eligibility to prompts/manual/graph_creation/specifications
    spec_path = current_file.parent.parent.parent.parent / "prompts" / "manual" / "graph_creation" / "specifications" / "child_benefit" / "child_benefit_eligibility.json"
    
    print(f"Specification path: {spec_path}")
    print(f"Specification exists: {spec_path.exists()}\n")
    
    if not spec_path.exists():
        print("✗ ERROR: Specification file not found!")
        print(f"  Expected at: {spec_path}")
        return False
    
    # Try to load and validate the specification
    try:
        with open(spec_path, 'r') as f:
            spec = json.load(f)
        
        print("✓ Specification loaded successfully\n")
        
        # Print metadata
        print("Specification Metadata:")
        print(f"  Version: {spec.get('version')}")
        print(f"  Last Updated: {spec.get('last_updated')}")
        print(f"  Source: {spec.get('source')}")
        print(f"  Description: {spec.get('description')}\n")
        
        # Print structure info
        print("Decision Tree Structure:")
        nodes = spec["decision_tree"]["nodes"]
        print(f"  Total nodes: {len(nodes)}")
        
        # Count node types
        node_types = {}
        outcome_nodes = {"ELIGIBLE": 0, "INELIGIBLE": 0, "DEFERRED": 0}
        
        for node_id, node in nodes.items():
            node_type = node.get("type", "unknown")
            node_types[node_type] = node_types.get(node_type, 0) + 1
            
            if node_type == "outcome":
                result = node.get("result", "UNKNOWN")
                if result in outcome_nodes:
                    outcome_nodes[result] += 1
        
        print(f"\n  Node Types:")
        for node_type, count in sorted(node_types.items()):
            print(f"    - {node_type}: {count}")
        
        print(f"\n  Outcomes:")
        for outcome, count in outcome_nodes.items():
            print(f"    - {outcome}: {count}")
        
        # Validate references
        print(f"\n  External References: {len(spec.get('external_references', {}))}")
        for ref_name, ref_url in spec.get('external_references', {}).items():
            print(f"    - {ref_name}: {ref_url}")
        
        print("\n✓ Specification validation complete!")
        return True
        
    except json.JSONDecodeError as e:
        print(f"✗ ERROR: Invalid JSON in specification file!")
        print(f"  {e}")
        return False
    except Exception as e:
        print(f"✗ ERROR: Failed to validate specification!")
        print(f"  {e}")
        return False


def validate_agent_imports():
    """Check if the agent can be imported."""
    print("\n" + "="*60)
    print("Validating Agent Imports")
    print("="*60 + "\n")
    
    try:
        # Try importing the agent
        import agent
        print("✓ Agent module imported successfully")
        
        # Check if root_agent exists
        if hasattr(agent, 'root_agent'):
            print("✓ root_agent found")
            print(f"  Agent name: {agent.root_agent.name}")
            print(f"  Agent description: {agent.root_agent.description}")
            
            # List tools
            if hasattr(agent.root_agent, 'tools'):
                print(f"\n  Tools available ({len(agent.root_agent.tools)}):")
                for tool in agent.root_agent.tools:
                    tool_name = tool.__name__ if hasattr(tool, '__name__') else str(tool)
                    print(f"    - {tool_name}")
        else:
            print("✗ ERROR: root_agent not found in agent module!")
            return False
        
        print("\n✓ Agent import validation complete!")
        return True
        
    except ImportError as e:
        print(f"✗ ERROR: Failed to import agent module!")
        print(f"  {e}")
        print("\n  Make sure you have all dependencies installed:")
        print("    - google.adk")
        print("    - google.genai")
        return False
    except Exception as e:
        print(f"✗ ERROR: Failed to validate agent!")
        print(f"  {e}")
        return False


def main():
    """Run all validations."""
    print("\nChild Benefit Eligibility Agent - Validation\n")
    
    spec_valid = validate_specification_path()
    agent_valid = validate_agent_imports()
    
    print("\n" + "="*60)
    print("Validation Summary")
    print("="*60)
    print(f"  Specification: {'✓ PASS' if spec_valid else '✗ FAIL'}")
    print(f"  Agent Import:  {'✓ PASS' if agent_valid else '✗ FAIL'}")
    print("="*60 + "\n")
    
    if spec_valid and agent_valid:
        print("✓ All validations passed!")
        print("\nNext steps:")
        print("  1. Run examples: python examples.py")
        print("  2. Run tests: python test_agent.py")
        print("  3. Try interactive mode: python test_agent.py interactive")
        return 0
    else:
        print("✗ Some validations failed. Please fix the errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
