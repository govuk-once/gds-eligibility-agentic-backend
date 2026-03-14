import os
import httpx
from pathlib import Path
from strands import Agent, tool
from strands.models import BedrockModel
from strands.agent.a2a_agent import A2AAgent
from dotenv import load_dotenv

load_dotenv()

# 1. Load the markdown system prompt
current_dir = Path(__file__).parent
with open(current_dir / "system_prompt.md", "r") as f:
    SYSTEM_PROMPT = f.read()

# 2. Tool to fetch the dynamic catalog from the Registry
@tool
def get_available_services() -> dict[str, str]:
    """
    Fetches the catalog of all available eligibility and implication agents.
    Returns their names, descriptions, and A2A endpoint URLs.
    """
    try:
        # Calls the local registry we built in registry.py
        response = httpx.get("http://localhost:7999/catalog")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": f"Could not reach the Agent Registry: {e}"}

# 3. Tool to establish dynamic A2A communication
@tool
def route_to_service(user_message: str, endpoint_url: str) -> str | None:
    """
    Routes the user's message to a specific downstream service agent via A2A.
    Provide the exact 'endpointUrl' found in the catalog.
    """
    print(f"🔀 Orchestrator dynamically routing to: {endpoint_url}")
    try:
        # Dynamically instantiate the A2A client for the target URL
        a2a_agent = A2AAgent(endpoint=endpoint_url)
        result = a2a_agent(prompt=user_message)
        return result.message.get("content")[0].get("text")
    except Exception as e:
        return f"Error contacting the downstream agent at {endpoint_url}: {e}"

def create_orchestrator() -> Agent:
    return Agent(
        name="Eligibility_Orchestrator",
        system_prompt=SYSTEM_PROMPT,
        tools=[get_available_services, route_to_service],
        model=BedrockModel(
            model_id=os.getenv("ELIGIBILITY_AGENT_AWS_BEDROCK_MODEL_ID", ""),
            region_name="eu-west-2"
        ),
    )