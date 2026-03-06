<<<<<<< HEAD
import sys
import logging
from mcp.server.fastmcp import FastMCP

# 1. Route logging to stderr so it doesn't break the JSON-RPC stdio
logging.basicConfig(level=logging.INFO, stream=sys.stderr, format='%(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 2. Instantiate the server FIRST
mcp = FastMCP("eligibility_tools")

# 3. Import the tools AFTER the mcp object exists
# We wrap it in a try/except so the server doesn't crash if you haven't generated the files yet.
try:
    from mcp_server.registered_eligibility_checker_tools import *
    from mcp_server.registered_eligibility_implication_tools import *
    logger.info("Successfully loaded all registered tools.")
except ImportError as e:
    logger.warning(f"Could not load tools: {e}")

def main():
    logger.info("Booting FastMCP Server...")
    mcp.run(transport="stdio")
=======
from mcp.server.fastmcp import FastMCP
from tools.pip.eligibility_checker import get_next_question
from models.eligibility_check_models import Question

mcp = FastMCP("eligibility_tools")

def main():
    mcp.run(transport="stdio")

@mcp.tool(
    name="pip_checker",
    title="Personal Independence Payments eligibility checker",
    description="Get the next PIP eligibility question. Input 'next_question' as an integer (e.g., 1 for the first question).",
    structured_output=True
)
def pip_checker(next_question: int) -> Question:
    return get_next_question(next_question=next_question)
>>>>>>> 46781da (ELIG-243: complete)
        
if __name__ == "__main__":
    main()