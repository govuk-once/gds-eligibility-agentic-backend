## Goals

* Assert that the following specifications:
  * ./skilled_worker_visa_eligibility.json
  * ./child_benefit_eligibility.json
contain no orphan nodes.
* If orphan nodes are found, assess whether each of these nodes is required.
   * if an orphan node is required, then add the appropriate connections.
   * if an orphan nodes is not required, remove it
