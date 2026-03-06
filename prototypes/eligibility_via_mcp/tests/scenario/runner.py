import os
import scenario
from strands import Agent
from agents.eligibility.agent import create

scenario.configure(default_model=os.getenv("JUDGE_AGENT_AWS_BEDROCK_MODEL_ID"))

class EligibilityAgent(scenario.AgentAdapter):
    def __init__(self):
        super().__init__()
        self.agent: Agent = create()
        
    async def call(self, input: scenario.AgentInput) -> scenario.AgentReturnTypes:
        return str(self.agent(input.last_new_user_message_str()))

async def run_scenario(
    scenario_name: str,
    scenario_description: str,
    judge_criteria: list[str],
    user_inputs: list[str]
) -> None:
    result = await scenario.run(
        name=scenario_name,
        description=scenario_description,
        agents=[
            EligibilityAgent(),
            scenario.UserSimulatorAgent(),
            scenario.JudgeAgent(criteria=judge_criteria)
        ],
        script=[
            call 
            for user_input in user_inputs 
            for call in (scenario.user(user_input), scenario.agent())
        ] + [scenario.judge()])

    assert result.success