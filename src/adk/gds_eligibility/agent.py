import os
from pathlib import Path

from google.adk.models.lite_llm import LiteLlm
from google.adk.agents.llm_agent import Agent

#  agent_id = os.getenv("BEDROCK_AGENT_ID")
#  agent_alias_id = os.getenv("BEDROCK_AGENT_ALIAS_ID")
prompts_dir = os.environ.get("PROMPTS_DIR", "../../prompts")


def get_prompt() -> str:
    prompt_path = Path(prompts_dir).joinpath("agents/TechnicalHypotheses/Accuracy-ChildBenefit-SmallModel.md")
    with prompt_path.open() as f:
        prompt_lines = f.readlines()
    return '\n'.join(prompt_lines)


root_agent = Agent(
    model=LiteLlm(model="bedrock/converse/anthropic.claude-3-7-sonnet-20250219-v1:0"),
    #  model = LiteLlm(model=f"bedrock/agent/{agent_id}/{agent_alias_id}"),
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction=get_prompt()
)
