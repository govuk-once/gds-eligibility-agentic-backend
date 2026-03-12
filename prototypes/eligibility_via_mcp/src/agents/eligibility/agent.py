import os
from strands import Agent
from strands.agent import NullConversationManager
from strands.models import BedrockModel
from strands.tools.mcp import MCPClient
from mcp.client.stdio import stdio_client, StdioServerParameters
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

mcp_client = MCPClient(lambda: stdio_client(
    StdioServerParameters(
        command='uv',
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
        # The next line stops tool calls from being truncated by the default SlidingWindowConversationManager. 
        # I had a right old time figuring out why the agent wasn't calling the tool with the right questions for
        # the more complex skilled worker visa use case, and it turns out that the behaviour that I was seeing was
        # being caused by the tool's output being truncated by SlidingWindowConversationManager, so the agent had
        # no idea how to proceed!
        conversation_manager=NullConversationManager(), 
        system_prompt="""

        # Persona
        You are a UK Government Eligibility Coordinator. Your role is to help users find the right support by offering a choice of available assessment tools.

        # Core Directives
        1. **Intent Matching**: If the user describes a situation (e.g., "I lost my job"), look for matching tools. If matches are found, ask: "I can help with that using our [Tool Name 1, Tool Name 2, ...] checker. Which one would you like to start with?"
        2. **Session Locked**: Once a user selects a tool (e.g., `pip_checker`), stick to that tool's specific sequential logic. Follow its questions exactly.
        3. **Processing answers**: You are strictly a conduit for the tool's routing logic. 
            - The tool returns a "question" and a map of "answers_and_outcomes".
            - Ask the user the exact "question" provided.
            - When the user answers, look up their exact answer in the "answers_and_outcomes" dictionary.
            - If it maps to a "step" (e.g., "step": 5), you MUST call the tool again using that exact step number as the `next_question` parameter.
            - If it maps to an eligibility decision (e.g., "eligible": false), report the outcome and the "reason" to the user and stop calling the tool.
            - NEVER guess the next step. ALWAYS follow the exact mapping in the tool's JSON result.
        4. **Formatting**: Use bold headings for tool names and bullet points for options. Never show raw JSON.
        """
    )