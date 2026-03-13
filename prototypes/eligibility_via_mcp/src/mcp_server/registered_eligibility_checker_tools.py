from mcp_server.tools.pip.eligibility_checker import get_next_question_for_pip_eligibility_check
from mcp_server.tools.skilled_worker_visa.eligibility_checker import get_next_question_for_skilled_worker_visa_eligibility_check
from mcp_server.server import mcp
from mcp_server.models.eligibility_check_models import Question
from mcp_server.tools.universal_credit.eligibility_checker import get_next_question_for_universal_credit_eligibility_check

@mcp.tool(
    name="pip_eligibility_checker",
    title="Personal Independence Payments eligibility checker",
    description="Get the next Personal Independence Payments eligibility question. Input 'next_question' as an integer (e.g., 1 for the first question).",
    structured_output=True
)
def check_pip_eligibility(next_question: int) -> Question:
    return get_next_question_for_pip_eligibility_check(next_question)

@mcp.tool(
    name="skilled_worker_visa_eligibility_checker",
    title="Skilled worker visa eligibility checker",
    description="Get the next skilled worker visa eligibility question. Input 'next_question' as an integer (e.g., 1 for the first question).",
    structured_output=True
)
def check_skilled_worker_visa_eligibility(next_question: int) -> Question:
    return get_next_question_for_skilled_worker_visa_eligibility_check(next_question)

@mcp.tool(
    name="universal_credit_eligibility_checker",
    title="Universal Credit eligibility checker",
    description="Get the next Universal Credit eligibility question. Input 'next_question' as an integer (e.g., 1 for the first question).",
    structured_output=True
)
def check_universal_credit_eligibility(next_question: int) -> Question:
    return get_next_question_for_universal_credit_eligibility_check(next_question)
