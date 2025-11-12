from google.adk.models.lite_llm import LiteLlm
from google.adk.agents.llm_agent import Agent

root_agent = Agent(
    #  model=LiteLlm(model="bedrock/converse/amazon.nova-lite-v1:0"),
    model = LiteLlm(model="bedrock/agent/CBVQSIPNEW/JU2SFMBBHR"),
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction='Answer user questions to the best of your knowledge',
)
