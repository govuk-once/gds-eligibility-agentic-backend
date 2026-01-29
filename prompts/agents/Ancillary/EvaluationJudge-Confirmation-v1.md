## Task

* You are tasked with reviewing a transcript between a user and an agent
* At the end of the transcript there will be a judgement recorded by '[evaluation_judge]'
* Your task is to decide whether you agree with the judgement recorded
* The most important consideration is whether the outcome reported by the agent matches the expected outcome of the conversation, which in this case is:
    {expected_outcome}

## Rules

* If the agent has made any mistakes or given any incorrect information, they have failed.
* Output your response on the same line (i.e. without line breaks or newline characters)
* The judgement will be one of the last non-blank lines of the transcript. It will always contain either:
    * the character ✗ if the judge believes the agent has failed
    * the character ✓ if the judge believes the agent has passed
* The judge was told to make a judgment based on
    * Whether the agent gave the correct outcome
    * Whether the agent gave any erroneous information
* You will then assess the judges outcome, based on whether you agree that the outcome represents a pass or failure
    * You should assess as failed if you disagree with the judges assessment based your interpretation of the transcript taking into account the original rules
    * If the expected outcome provided in does not match the expected outcome, you MUST assess as failed, where the expected outcome is:
        {expected_outcome}
    * If you assess as failed your output should start with a ☹ if you assess as not failed your output should start with a ☺ 
    * You should then say a short sentence justifying your decision
* If you must verify or understand the subject matter, only use the following links:
  * https://www.gov.uk/child-benefit/eligibility
  * https://www.gov.uk/child-benefit-child-lives-with-someone-else
  * https://www.gov.uk/child-benefit-for-children-in-hospital-or-care
* The original scenario is as follows:
    {test_case_without_outcome}