import os
from pathlib import Path

from google.adk.models.lite_llm import LiteLlm
from google.adk.agents.llm_agent import Agent

prompts_dir = os.environ.get("PROMPTS_DIR", "../../prompts")


def get_prompt(rel_path: str) -> str:
    prompt_path = Path(prompts_dir).joinpath(rel_path)
    with prompt_path.open() as f:
        prompt_lines = f.readlines()
    return "\n".join(prompt_lines)


root_agent = Agent(
    model=LiteLlm(model="bedrock/converse/eu.anthropic.claude-sonnet-4-5-20250929-v1:0"),
    name="root_agent",
    description="A helpful assistant for user questions.",
    instruction='''
        {app:state_prompt}
    '''
    #tools=[update_question_and_answers],
)

#def update_question_and_answers(question: str, answer: str, tool_context: ToolContext ) -> Dict[str, Any]:
#    questions_and_answers = tool_context.state.setdefault("questions_and_answers", {})
#    print(questions_and_answers)
#    questions_and_answers[question] = answer
#    print(questions_and_answers)
#    tool_context.state["questions_and_answers"] = questions_and_answers
#    
#    return {
#       "state": tool_context.state.to_dict()
#    }

