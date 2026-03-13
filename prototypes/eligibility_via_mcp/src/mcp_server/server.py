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
        
if __name__ == "__main__":
    main()