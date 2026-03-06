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
        
if __name__ == "__main__":
    main()