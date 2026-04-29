import os
from enum import Enum
from pathlib import Path

from google.adk.models.lite_llm import LiteLlm
from google.adk.agents.llm_agent import Agent
from google.adk.tools.tool_context import ToolContext

from tools.web_scraper import read_webpage

prompts_dir = Path(os.environ.get("PROMPTS_DIR", "../../prompts"))

def get_prompt(rel_path: str) -> str:
    prompt_path = Path(prompts_dir).joinpath(rel_path)
    with prompt_path.open() as f:
        prompt_lines = f.readlines()
    return "\n".join(prompt_lines)


class Eligibility(Enum):
    ELIGIBLE = 1
    INELIGIBLE = 2
    INDETERMINATE = 3


def eligibility_judgement_outcome(
    child_names: list[str],
    is_eligible_list: list[Eligibility],
    reasonings: list[str],
    overall_reasoning: str,
    tool_context: ToolContext
):
    """
    Call this function ONLY when you have an outcome to report as to eligibility.

    Args:
        child_names: A list of the exact names of every child discussed.
        is_eligible_list: A list of type Eligibility (An enumeration with values ELIGIBLE, INELIGIBLE and INDETERMINATE) indicating if the claimant is eligible for each child.
        MUST be in the exact same order as child_names.
        reasonings: A list of step-by-step reasoning explaining the rules for each child. MUST be in the exact same order as child_names.
        overall_reasoning: A brief summary of the family's total situation.
    """
    case_name = tool_context.state.get("case_name")
    print(f"<{case_name}>  [Tool Call] eligibility_judgement_outcome triggered by {tool_context.agent_name}")
    tool_context.actions.escalate = True


    child_evaluations = {}
    for name, is_eligible, reasoning in zip(child_names, is_eligible_list, reasonings):
        child_evaluations[name] = {
            "child_name": name,
            "eligible": is_eligible,
            "reasoning": reasoning
        }

    return {
        "child_evaluations": child_evaluations,
        "overall_reasoning": overall_reasoning
    }


root_agent = Agent(
    model=LiteLlm(model="bedrock/converse/eu.anthropic.claude-sonnet-4-5-20250929-v1:0"),
    name="eligibility_agent",
    description="A helpful assistant for determining eligibility for benefits.",
    #  instruction=get_prompt( # This is now defined in the pipeline
    #      #  "agents/TechnicalHypotheses/adhoc-skilledWorkerVisa.md"
    #      #"agents/TechnicalHypotheses/Accuracy-ChildBenefit-v3.md"
    #      "agents/TechnicalHypotheses/Accuracy-ChildBenefit-structuredOutput-v1.md"
    #  ),
    tools=[eligibility_judgement_outcome, read_webpage]
)
