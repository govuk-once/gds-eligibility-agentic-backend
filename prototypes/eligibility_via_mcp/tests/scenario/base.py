import os
import scenario
from strands import Agent
from agents.eligibility.agent import create
from abc import ABC, abstractmethod

class EligibilityAgent(scenario.AgentAdapter):
    def __init__(self):
        super().__init__()
        self.agent: Agent = create()
        
    async def call(self, input: scenario.AgentInput) -> scenario.AgentReturnTypes:
        return str(self.agent(input.last_new_user_message_str()))

class BaseScenario(ABC):
    def __init__(
        self, 
        short_description: str,
        user_should_be_eligible: bool, 
        user_intro: str,
        decision_addendum: str = "",
    ):
        self.short_description = short_description
        self.user_should_be_eligible = user_should_be_eligible
        self.decision_addendum = decision_addendum

        self.user_inputs = [user_intro]
        self.judge_criteria = [f"The agent should identify that {self._get_eligibility_name()} is the most suitable eligibility to check, and ask the user if they want to proceed"]
        self.user_inputs.append("yes, continue with check")

    @abstractmethod
    def _get_eligibility_name(self) -> str:
        ...

    @abstractmethod
    def _get_judge_criteria_for_implicated_benefits(self) -> str:
        ...

    def _add_user_input(self, value: str):
        self.user_inputs.append(value)

    def _add_judge_criteria(self, value: str):
        self.judge_criteria.append(value)

    def _user_eligibility_str(self) -> str:
        return "eligible" if self.user_should_be_eligible else "ineligible"
    
    def would_you_like_me_to_check_what_implications_there_are_with_other_benefits_if_you_were_apply_and_be_found_eligible(self, value: str) -> BaseScenario:
        self._add_user_input(value)
        self._add_judge_criteria(self._get_judge_criteria_for_implicated_benefits())
        return self

    async def run(self) -> None:
        self.judge_criteria.append(f"Finally, the agent should tell the user that they are {self._user_eligibility_str()},{ " " + self.decision_addendum + ", " if self.decision_addendum else ""} and the conversation should conclude.")

        result = await scenario.run(
            name=f"{self._get_eligibility_name()} ({self.short_description})",
            description=f"The user's situation indicates that {self._get_eligibility_name()} would be an appropriate eligibility to" \
            "investigate, so they should be assessed to see if they are eligibile. The agent should determine that the user is " \
            f"{self._user_eligibility_str()}.",
            agents=[
                EligibilityAgent(),
                scenario.UserSimulatorAgent(
                    model=os.getenv("USER_SIMULATOR_AWS_BEDROCK_MODEL_ID", "")
                ),
                scenario.JudgeAgent(
                    criteria=self.judge_criteria, 
                    model=os.getenv("JUDGE_AGENT_AWS_BEDROCK_MODEL_ID", "")
                )
            ],
            script=[
                call 
                for user_input in self.user_inputs 
                for call in (scenario.user(user_input), scenario.agent())
            ] + [scenario.judge()])

        assert result.success