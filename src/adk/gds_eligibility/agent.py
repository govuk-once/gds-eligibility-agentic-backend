import os
from pathlib import Path

from google.adk.models.lite_llm import LiteLlm
from google.adk.agents.llm_agent import Agent
from google.adk.tools.tool_context import ToolContext

prompts_dir = os.environ.get("PROMPTS_DIR", "../../prompts")


def get_prompt(rel_path: str) -> str:
    prompt_path = Path(prompts_dir).joinpath(rel_path)
    with prompt_path.open() as f:
        prompt_lines = f.readlines()
    return "\n".join(prompt_lines)
 
# TODO add tool for retrieving website content

def eligibility_judgement_outcome(
        would_application_be_eligible: bool, 
        would_application_be_ineligible: bool, 
        would_application_be_eligible_in_part: bool, 
        reasoning_for_eligibility_judgement: str, 
        tool_context: ToolContext
    ):
    """Call this function ONLY when you have an outcome to report as to eligibility."""
    print(f"  [Tool Call] eligibility_judgement_outcome triggered by {tool_context.agent_name}")
    tool_context.actions.escalate = True
    return {
        "would_application_be_eligible": would_application_be_eligible,
        "would_application_be_ineligible": would_application_be_ineligible,
        "would_application_be_eligible_in_part": would_application_be_eligible_in_part,
        "reasoning_for_eligibility_judgement": reasoning_for_eligibility_judgement
    }


root_agent = Agent(
    ##model=LiteLlm(model="bedrock/converse/google.gemma-3-4b-it"),  # Small model
    #model=LiteLlm(model="bedrock/converse/google.gemma-3-27b-it"), # Large model
    #model=LiteLlm(model="bedrock/converse/anthropic.claude-3-7-sonnet-20250219-v1:0"),
    model=LiteLlm(model="bedrock/converse/eu.anthropic.claude-sonnet-4-5-20250929-v1:0"),
    name="eligibility_agent",
    description="A helpful assistant for determining eligibility for benefits.",
    instruction=get_prompt(
        #  "agents/TechnicalHypotheses/adhoc-skilledWorkerVisa.md"
        #"agents/TechnicalHypotheses/Accuracy-ChildBenefit-v3.md"
        "agents/TechnicalHypotheses/Accuracy-ChildBenefit-structuredOutput-v1.md"
    ),
    tools=[eligibility_judgement_outcome]
)
