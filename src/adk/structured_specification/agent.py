import os
import json
from pathlib import Path
from typing import Dict, Any, Optional

from google.adk.models.lite_llm import LiteLlm
from google.adk.agents.llm_agent import Agent
from google.adk.tools.tool_context import ToolContext

# Load the child benefit eligibility specification
PROMPTS_DIR = Path(__file__).parent.parent.parent.parent / "prompts" 
SPEC_PATH = PROMPTS_DIR / "manual" / "graph_creation" / "specifications" / "child_benefit" / "child_benefit_eligibility.json"

def load_specification() -> Dict[str, Any]:
    """Load the child benefit eligibility specification."""
    with open(SPEC_PATH, 'r') as f:
        return json.load(f)

CHILD_BENEFIT_SPEC = load_specification()
prompts_dir = Path(os.environ.get("PROMPTS_DIR", PROMPTS_DIR))

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
    print(f"  [Tool Call] get_node_info triggered by {tool_context.agent_name}")
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
    print(f"  [Tool Call] navigate_to_outcome triggered by {tool_context.agent_name}")
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


def get_constants(tool_context: ToolContext) -> Dict[str, Any]:
    """
    Retrieve constant values from the specification (age limits, time limits, etc.).

    Returns:
        Dictionary containing all constants
    """
    print(f"  [Tool Call] get_constants triggered by {tool_context.agent_name}")
    return CHILD_BENEFIT_SPEC.get("constants", {})


def get_validation_rules(tool_context: ToolContext) -> Dict[str, Any]:
    """
    Retrieve validation rules from the specification.

    Returns:
        Dictionary containing validation rules
    """
    print(f"  [Tool Call] get_validation_rules triggered by {tool_context.agent_name}")
    return CHILD_BENEFIT_SPEC.get("validation_rules", {})


def start_assessment(tool_context: ToolContext) -> Dict[str, Any]:
    """
    Start a new child benefit eligibility assessment. ALWAYS CALL THIS WHEN STARTING A CONVERSATION ON CHILD BENEFIT ELIGIBILITY

    Args:
        tool_context: The tool context for state management

    Returns:
        Dictionary containing the first node information
    """
    print(f"  [Tool Call] start_assessment triggered by {tool_context.agent_name}")
    # Reset state
    tool_context.state["navigation_history"] = []

    # Get root node
    root = CHILD_BENEFIT_SPEC["decision_tree"]["root"]
    first_node_id = root["next"]
    tool_context.state["current_node"] = root

    return get_node_info(first_node_id, tool_context)


def get_specification_metadata(tool_context: ToolContext = None) -> Dict[str, Any]:
    """
    Get metadata about the child benefit specification.

    Returns:
        Dictionary containing version, source, description, etc.
    """
    if tool_context:
        print(f"  [Tool Call] get_specification_metadata triggered by {tool_context.agent_name}")
    return {
        "version": CHILD_BENEFIT_SPEC.get("version"),
        "last_updated": CHILD_BENEFIT_SPEC.get("last_updated"),
        "source": CHILD_BENEFIT_SPEC.get("source"),
        "description": CHILD_BENEFIT_SPEC.get("description"),
        "external_references": CHILD_BENEFIT_SPEC.get("external_references", {})
    }


def eligibility_judgement_outcome(
        child_names: list[str], 
        is_eligible_list: list[bool], 
        reasonings: list[str], 
        overall_reasoning: str, 
        tool_context: ToolContext
    ):
    """
    Call this function ONLY when you have an outcome to report as to eligibility.
    
    Args:
        child_names: A list of the exact names of every child discussed.
        is_eligible_list: A list of booleans (True/False) indicating if the claimant is eligible for each child. MUST be in the exact same order as child_names.
        reasonings: A list of step-by-step reasoning explaining the rules for each child. MUST be in the exact same order as child_names.
        overall_reasoning: A brief summary of the family's total situation.
    """
    print(f"  [Tool Call] eligibility_judgement_outcome triggered by {tool_context.agent_name}")
    tool_context.actions.escalate = True
    

    child_evaluations = []
    for name, is_eligible, reasoning in zip(child_names, is_eligible_list, reasonings):
        child_evaluations.append({
            "child_name": name,
            "is_eligible": is_eligible,
            "reasoning": reasoning
        })
    
    return {
        "child_evaluations": child_evaluations,
        "overall_reasoning": overall_reasoning
    }


root_agent = Agent(
    model=LiteLlm(model="bedrock/converse/eu.anthropic.claude-sonnet-4-5-20250929-v1:0"),
    name="child_benefit_eligibility_agent",
    description="A helpful assistant for UK Child Benefit eligibility questions using the official specification.",
    instruction=get_prompt("agents/TechnicalHypotheses/StructuredSpecification-ChildBenefit-v1.md").format(metadata=get_specification_metadata()),
    tools=[
        start_assessment,
        get_node_info,
        navigate_to_outcome,
        get_constants,
        get_validation_rules,
        get_specification_metadata,
        eligibility_judgement_outcome
    ]
)
