import os
from pathlib import Path

from google.adk.models.lite_llm import LiteLlm
from google.adk.agents.llm_agent import Agent

#  agent_id = os.getenv("BEDROCK_AGENT_ID")
#  agent_alias_id = os.getenv("BEDROCK_AGENT_ALIAS_ID")
prompts_dir = os.environ.get("PROMPTS_DIR", "../../prompts")


def get_prompt(rel_path: str) -> str:
    prompt_path = Path(prompts_dir).joinpath(rel_path)
    with prompt_path.open() as f:
        prompt_lines = f.readlines()
    return "\n".join(prompt_lines)


root_agent = Agent(
    #  model=LiteLlm(model="bedrock/converse/google.gemma-3-4b-it"), # Small model
    model=LiteLlm(model="bedrock/converse/google.gemma-3-27b-it"), # Large model
    #  model = LiteLlm(model=f"bedrock/agent/{agent_id}/{agent_alias_id}"),
    name="root_agent",
    description="A helpful assistant for user questions.",
    instruction=get_prompt(
        "agents/TechnicalHypotheses/adhoc-skilledWorkerVisa.md"
    ),
)
