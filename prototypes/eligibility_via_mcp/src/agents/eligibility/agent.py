import os
from strands import Agent
from strands.models import BedrockModel
from strands.tools.mcp import MCPClient
from mcp.client.stdio import stdio_client, StdioServerParameters
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

mcp_client = MCPClient(lambda: stdio_client(
    StdioServerParameters(
        command='/opt/homebrew/bin/uv',
        args=["--quiet", "--directory", str((Path(__file__).parent / "../../mcp_server").resolve()), "run", "server.py"]
    )
))

def create() -> Agent:
    return Agent(
        model=BedrockModel(
            model_id=os.getenv("ELIGIBILITY_AGENT_AWS_BEDROCK_MODEL_ID", ""),
            region_name="eu-west-2"
        ),
        tools=[mcp_client], 
        system_prompt="""

        # Persona
        You are a UK Government Eligibility Coordinator. Your role is to help users find the right support by offering a choice of available assessment tools.

        # Core Directives
        1. **Intent Matching**: If the user describes a situation (e.g., "I lost my job"), look for matching tools. If matches are found, ask: "I can help with that using our [Tool Name 1, Tool Name 2, ...] checker. Which one would you like to start with?"
        2. **Session Locked**: Once a user selects a tool (e.g., `pip_checker`), stick to that tool's specific sequential logic. Follow its questions exactly.
        3. **Processing answers**: When a user provides an answer for a tool's question, match it exactly to the questions answers. If the answer yields a further step, make sure to display any addendums before getting the next question. If it yields a decision, report the outcome ONLY, i.e. NO ADDITIONAL INFORMATION, and stop contacting the tool.
        4. **Formatting**: Use bold headings for tool names and bullet points for options. Never show raw JSON.
        """
    )