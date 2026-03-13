from mcp_server.tools.pip.eligibility_implications import check_pip_eligibility_implications
from mcp_server.server import mcp
from mcp_server.models.eligibility_check_models import Implications
from mcp_server.tools.universal_credit.eligibility_implications import check_universal_credit_eligibility_implications

@mcp.tool(
    name="pip_implications_checker",
    title="Personal independence payments implications checker",
    description="Retrieve any benefit implications that may occur if a user applies for Personal Independence Payments and is found eligible",
    structured_output=True
)
def pip_implications_checker() -> Implications:
    return check_pip_eligibility_implications()

@mcp.tool(
    name="universal_credit_implications_checker",
    title="Universal Credit implications checker",
    description="Retrieve any benefit implications that may occur if a user applies for Universal Credit and is found eligible",
    structured_output=True
)
def universal_credit_implications_checker() -> Implications:
    return check_universal_credit_eligibility_implications()
