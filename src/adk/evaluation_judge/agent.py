import os
from pathlib import Path

from google.adk.agents import LoopAgent, SequentialAgent
from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.tool_context import ToolContext

from gds_eligibility.agent import root_agent as eligibility_agent


prompts_dir = os.environ.get("PROMPTS_DIR", "../../prompts")


def get_prompt(rel_path: str) -> str:
    prompt_path = Path(prompts_dir).joinpath(rel_path)
    with prompt_path.open() as f:
        prompt_lines = f.readlines()
    return "\n".join(prompt_lines)


def exit_loop(tool_context: ToolContext):
    """Call this function ONLY when the judge indicates no further conversation is needed, signaling the iterative process should end."""
    print(f"  [Tool Call] exit_loop triggered by {tool_context.agent_name}")
    tool_context.actions.escalate = True
    # Return empty dict as tools should typically return JSON-serializable output
    return {}


evaluation_judge = Agent(
    model=LiteLlm(model="bedrock/converse/anthropic.claude-3-7-sonnet-20250219-v1:0"),
    name="evaluation_judge",
    description="When given a transcript, outputs a judgement",
    instruction=get_prompt("agents/Ancillary/EvaluationJudge-EvaluationOnly.md"),
)

def get_review_pipeline(test_case):
    actor = Agent(
        model=LiteLlm(model="bedrock/converse/anthropic.claude-3-7-sonnet-20250219-v1:0"),
        name="actor",
        description="When given a context, it will role-play as a user in order to test another agent",
        #static_instruction=get_prompt("agents/Ancillary/Actor-Humanlike.md"),
        #instruction=test_case,
        instruction=get_prompt("agents/Ancillary/Actor-Humanlike.md") + "\n" + test_case,
        tools=[exit_loop],  # Provide the exit_loop tool
    )


    conversation_pipeline = LoopAgent(
        name="Converse", sub_agents=[eligibility_agent, actor]
    )


    review_pipeline = SequentialAgent(
        name="ConverseAndEvaluate", sub_agents=[conversation_pipeline, evaluation_judge]
    )
    return review_pipeline
