import os
from pathlib import Path

from google.adk.agents import SequentialAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.agents.llm_agent import Agent

from gds_eligibility.agent import root_agent as eligibility_agent


prompts_dir = os.environ.get("PROMPTS_DIR", "../../prompts")

def get_prompt(rel_path: str) -> str:
    prompt_path = Path(prompts_dir).joinpath(rel_path)
    with prompt_path.open() as f:
        prompt_lines = f.readlines()
    return '\n'.join(prompt_lines)


evaluation_judge = Agent(
    model=LiteLlm(model="bedrock/converse/anthropic.claude-3-7-sonnet-20250219-v1:0"),
    name='evaluation_judge',
    description='When given a context, it will role-play as a user in order to test another agent',
    instruction=get_prompt("agents/Ancillary/EvaluationJudge.md")
)

# TODO are we making the test inauthentic by using A2A as the communication medium?
# https://google.github.io/adk-docs/agents/multi-agents/#reviewcritique-pattern-generator-critic
review_pipeline = SequentialAgent(
    name="ConverseAndEvaluate",
    sub_agents=[evaluation_judge, eligibility_agent]
)
