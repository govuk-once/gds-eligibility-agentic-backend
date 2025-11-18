from os import getenv
from typing import AsyncGenerator

from google.adk.agents import LoopAgent, LlmAgent, BaseAgent
from google.adk.events import Event, EventActions
from google.adk.agents.invocation_context import InvocationContext
from google.adk.models.lite_llm import LiteLlm
from google.adk.agents.llm_agent import Agent

agent_id = getenv("BEDROCK_AGENT_ID")
agent_alias_id = getenv("BEDROCK_AGENT_ALIAS_ID")

#  root_agent = Agent(
#      #  model=LiteLlm(model="bedrock/converse/amazon.nova-lite-v1:0"),
#      model = LiteLlm(model=f"bedrock/agent/{agent_id}/{agent_alias_id}"),
#      name='root_agent',
#      description='A helpful assistant for user questions.',
#      instruction='Answer user questions to the best of your knowledge',
#  )

# Conceptual Response: Iterative Response Refinement

# Agent to generate/refine response based on state['current_response'] and state['requirements']
response_refiner = LlmAgent(
    model = LiteLlm(model=f"bedrock/agent/{agent_id}/{agent_alias_id}"),
    name="ResponseRefiner",
    instruction='''
        Read state['current_response'] (if exists) and state['query']. Generate/refine response according to instructions. Save to state['current_response'].
    ''',
    # ensure you've taken account of feedback provided in state['feedback'],
    output_key="current_response" # Overwrites previous response in state
)

# Agent to check if the response eeets quality standards
quality_checker = LlmAgent(
    model = LiteLlm(model=f"bedrock/agent/{agent_id}/{agent_alias_id}"),
    name="QualityChecker",
    instruction='''
        Evaluate the response in state['current_response'] against state['query']. Output 'pass' or 'fail'.
    ''',
    # Give qualitative feedback in state['feedback'],
    output_key="quality_status"
)

# Custom agent to check the status and escalate if 'pass'
class CheckStatusAndEscalate(BaseAgent):
    async def _run_async_impl(self, ctx: InvocationContext) -> AsyncGenerator[Event, None]:
        status = ctx.session.state.get("quality_status", "fail")
        should_stop = (status == "pass")
        yield Event(author=self.name, actions=EventActions(escalate=should_stop))

refinement_loop = LoopAgent(
    #  name="ResponseRefinementLoop",
    name="root_agent",
    max_iterations=5,
    sub_agents=[response_refiner, quality_checker, CheckStatusAndEscalate(name="StopChecker")]
)
root_agent = refinement_loop
# Loop runs: Refiner -> Checker -> StopChecker
# State['current_response'] is updated each iteration.
# Loop stops if QualityChecker outputs 'pass' (leading to StopChecker escalating) or after 5 iterations.

