from copy import deepcopy
import os
from pathlib import Path

from google.adk.agents import LoopAgent, SequentialAgent
from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.tool_context import ToolContext

from gds_eligibility.agent import root_agent as eligibility_agent


prompts_dir = os.environ.get("PROMPTS_DIR", "../../prompts")


def get_prompt(rel_path: str, **kwargs) -> str:
    prompt_path = Path(prompts_dir).joinpath(rel_path)
    with prompt_path.open() as f:
        prompt_lines = f.readlines()
    prompt_string = "\n".join(prompt_lines)
    if kwargs:
        for format_key in kwargs.keys():
            # str.format() will fail silently if args/kwargs are not present in the string templating syntax
            assert ("{" + format_key + "}") in prompt_string
        prompt_string = prompt_string.format(**kwargs)
    return prompt_string

def exit_loop(tool_context: ToolContext):
    """Call this function ONLY when the judge indicates no further conversation is needed, signaling the iterative process should end."""
    print(f"  [Tool Call] exit_loop triggered by {tool_context.agent_name}")
    tool_context.actions.escalate = True
    # Return empty dict as tools should typically return JSON-serializable output
    return {}


def get_judge_agent(name: str, prompt_filepath: str, **kwargs):
    return Agent(
        model=LiteLlm(model="bedrock/converse/anthropic.claude-3-7-sonnet-20250219-v1:0"),
        name=name,
        description="When given a transcript, outputs a judgement",
        instruction=get_prompt(prompt_filepath, **kwargs),
    )


def get_review_pipeline(test_case: str, expected_outcome: str):
    evaluation_judge = get_judge_agent("evaluation_judge", "agents/Ancillary/EvaluationJudge-EvaluationOnly-v3.md", expected_outcome=expected_outcome)

    actor = Agent(
        model=LiteLlm(model="bedrock/converse/anthropic.claude-3-7-sonnet-20250219-v1:0"),
        name="actor",
        description="When given a context, it will role-play as a user in order to test another agent",
        #static_instruction=get_prompt("agents/Ancillary/Actor-Humanlike.md"),
        #instruction=test_case,
        instruction=get_prompt("agents/Ancillary/Actor-Humanlike-v0.md") + "\n" + test_case,
        tools=[exit_loop],  # Provide the exit_loop tool
    )

    conversation_pipeline = LoopAgent(
        # Any agent instantiated outside the scope of this function should be deep-copied, as said
        # agent instance remembers its parent from previous invocations 
        name="Converse", sub_agents=[deepcopy(eligibility_agent), actor]
    )

    review_pipeline = SequentialAgent(
        name="ConverseAndEvaluate", sub_agents=[conversation_pipeline, evaluation_judge]
    )
    return review_pipeline
