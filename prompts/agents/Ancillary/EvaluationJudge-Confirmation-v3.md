## Task

* You are tasked with reviewing a transcript between a user and an agent
* At the end of the transcript there will be a judgement recorded by '[evaluation_judge]'
* Your task is ignore the previous judgement, and decide whether you think the agent communicated the correct outcome as to whether the user was eligible or not eligible for child benefit
* The expected outcome of this conversation is:
    {expected_outcome}

## Rules

* Output your response on the same line (i.e. without line breaks or newline characters)
* The judgement will be one of the last non-blank lines of the transcript. It will always contain either:
    * the character ✗ if the judge believes the agent has failed
    * the character ✓ if the judge believes the agent has passed
* You will then assess whether you think the agent communicated an eligibility outcome that agrees with the expected outcome
    * You should give a careful and considered justification for your decision
    * The expected outcome is:
        {expected_outcome}
    * If you think the eligibility outcome the agent communicated does not agree with the expected outcome, your output should contain a 👎. If you think the eligibility outcome the agent communicated does agree with the expected outcome, your output should contain a 👍 
* If you must verify or understand the subject matter, only use the following links:
  * https://www.gov.uk/child-benefit/eligibility
  * https://www.gov.uk/child-benefit-child-lives-with-someone-else
  * https://www.gov.uk/child-benefit-for-children-in-hospital-or-care
* The original scenario is as follows:
    {test_case_without_outcome}
