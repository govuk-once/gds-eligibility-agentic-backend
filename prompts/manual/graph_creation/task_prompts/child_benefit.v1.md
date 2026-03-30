## Goal

Adapt ./eligibility-schema.json so that it can also be used to create a machine-readable, unambiguous representation of the criteria for eligibility of a family for UK Child Benefit

## Requirements
1. The representation should faithfully and correctly represent the eligibility criteria for all relevant eligibility services in scope, described by the following websites, or links from the following websites:
  * Skilled Worker Visa:
    * https://www.gov.uk/skilled-worker-visa
  * Child Benefit:
    * https://www.gov.uk/child-benefit/eligibility
    * https://www.gov.uk/child-benefit-child-lives-with-someone-else
    * https://www.gov.uk/child-benefit-for-children-in-hospital-or-care
2. The representation should be complete enough that it covers all possible edge cases contained within the eligibility criteria for all eligibility services in scope
3. The representation should be unambiguous enough that the outcome (for a particular eligibility service) is deterministic, and consistent for multiple people with the same personal circumstances
4. The representation should be capable of being visualised in a simple graphical form that it can be easily understood by someone with subject matter expertise of the rules of the eligibility domain
