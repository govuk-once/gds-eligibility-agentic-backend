import os
import json
from pathlib import Path
from typing import Dict, Any, Optional

from google.adk.models.lite_llm import LiteLlm
from google.adk.agents.llm_agent import Agent
from google.adk.tools.tool_context import ToolContext

# Load the child benefit eligibility specification
SPEC_PATH = Path(__file__).parent.parent.parent.parent / "prompts" / "manual" / "graph_creation" / "specifications" / "child_benefit" / "child_benefit_eligibility.json"

def load_specification() -> Dict[str, Any]:
    """Load the child benefit eligibility specification."""
    with open(SPEC_PATH, 'r') as f:
        return json.load(f)

CHILD_BENEFIT_SPEC = load_specification()
prompts_dir = os.environ.get("PROMPTS_DIR", "../../prompts")

def get_prompt(rel_path: str) -> str:
    prompt_path = Path(prompts_dir).joinpath(rel_path)
    with prompt_path.open() as f:
        prompt_lines = f.readlines()
    return "\n".join(prompt_lines)


def get_node_info(node_id: str, tool_context: ToolContext) -> Dict[str, Any]:
    """
    Retrieve information about a specific node in the decision tree.

    Args:
        node_id: The ID of the node to retrieve
        tool_context: The tool context for state management

    Returns:
        Dictionary containing node information
    """
    nodes = CHILD_BENEFIT_SPEC["decision_tree"]["nodes"]

    if node_id not in nodes:
        return {"error": f"Node '{node_id}' not found in specification"}

    node = nodes[node_id]

    # Store current node in context
    tool_context.state["current_node"] = node_id

    return {
        "node_id": node_id,
        "node_type": node.get("type"),
        "question": node.get("question"),
        "description": node.get("description"),
        "help_text": node.get("help_text"),
        "criteria": node.get("criteria"),
        "outcomes": node.get("outcomes"),
        "paths": node.get("paths"),
        "routing_logic": node.get("routing_logic"),
        "evaluation_logic": node.get("evaluation_logic"),
        "reference": node.get("reference"),
        "result": node.get("result"),
        "reason": node.get("reason"),
        "guidance": node.get("guidance"),
        "next_steps": node.get("next_steps")
    }


def navigate_to_outcome(outcome_key: str, tool_context: ToolContext) -> Dict[str, Any]:
    """
    Navigate to an outcome node based on the current node's outcomes.

    Args:
        outcome_key: The outcome key (e.g., 'yes', 'no', 'under_16', etc.)
        tool_context: The tool context for state management

    Returns:
        Dictionary containing the destination node information
    """
    current_node_id = tool_context.state.get("current_node")

    if not current_node_id:
        # Start from root if no current node
        root = CHILD_BENEFIT_SPEC["decision_tree"]["root"]
        next_node_id = root["next"]
    else:
        nodes = CHILD_BENEFIT_SPEC["decision_tree"]["nodes"]
        current_node = nodes.get(current_node_id)

        if not current_node:
            return {"error": f"Current node '{current_node_id}' not found"}

        outcomes = current_node.get("outcomes", {})

        if outcome_key not in outcomes:
            return {
                "error": f"Outcome '{outcome_key}' not valid for node '{current_node_id}'",
                "valid_outcomes": list(outcomes.keys())
            }

        next_node_id = outcomes[outcome_key]

    # Update navigation history
    history = tool_context.state.get("navigation_history", [])
    history.append({
        "from": current_node_id,
        "outcome": outcome_key,
        "to": next_node_id
    })
    tool_context.state["navigation_history"] = history

    # Get info about the next node
    return get_node_info(next_node_id, tool_context)


def get_constants() -> Dict[str, Any]:
    """
    Retrieve constant values from the specification (age limits, time limits, etc.).

    Returns:
        Dictionary containing all constants
    """
    return CHILD_BENEFIT_SPEC.get("constants", {})


def get_validation_rules() -> Dict[str, Any]:
    """
    Retrieve validation rules from the specification.

    Returns:
        Dictionary containing validation rules
    """
    return CHILD_BENEFIT_SPEC.get("validation_rules", {})


def start_assessment(tool_context: ToolContext) -> Dict[str, Any]:
    """
    Start a new child benefit eligibility assessment.

    Args:
        tool_context: The tool context for state management

    Returns:
        Dictionary containing the first node information
    """
    # Reset state
    tool_context.state.clear()
    tool_context.state["navigation_history"] = []

    # Get root node
    root = CHILD_BENEFIT_SPEC["decision_tree"]["root"]
    first_node_id = root["next"]

    return get_node_info(first_node_id, tool_context)


def get_specification_metadata() -> Dict[str, Any]:
    """
    Get metadata about the child benefit specification.

    Returns:
        Dictionary containing version, source, description, etc.
    """
    return {
        "version": CHILD_BENEFIT_SPEC.get("version"),
        "last_updated": CHILD_BENEFIT_SPEC.get("last_updated"),
        "source": CHILD_BENEFIT_SPEC.get("source"),
        "description": CHILD_BENEFIT_SPEC.get("description"),
        "external_references": CHILD_BENEFIT_SPEC.get("external_references", {})
    }


root_agent = Agent(
    model=LiteLlm(model="bedrock/converse/eu.anthropic.claude-sonnet-4-5-20250929-v1:0"),
    name="child_benefit_eligibility_agent",
    description="A helpful assistant for UK Child Benefit eligibility questions using the official specification.",
    instruction=get_prompt("StructuredSpecification-ChildBenefit-v1.md").format(metadata=get_specification_metadata()),
    tools=[
        start_assessment,
        get_node_info,
        navigate_to_outcome,
        get_constants,
        get_validation_rules,
        get_specification_metadata
    ]
)
