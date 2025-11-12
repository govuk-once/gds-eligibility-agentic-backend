from os import getenv

from google.adk.models.lite_llm import LiteLlm
from google.adk.agents.llm_agent import Agent

agent_id = getenv("BEDROCK_AGENT_ID")
agent_alias_id = getenv("BEDROCK_AGENT_ALIAS_ID")

root_agent = Agent(
    #  model=LiteLlm(model="bedrock/converse/amazon.nova-lite-v1:0"),
    model = LiteLlm(model=f"bedrock/agent/{agent_id}/{agent_alias_id}"),
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction='Answer user questions to the best of your knowledge',
)
