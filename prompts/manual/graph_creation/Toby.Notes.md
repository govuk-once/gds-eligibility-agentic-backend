# TODO
* [x] Break this out into schema, plug other benefits into it
* [x] Compare specifications against tests cases and see if any modification needed to account for edge cases
* [ ] Refactor individual domain-specific constants out of schema into specifications
* [ ] Consider how the schema/specifications might be exposed as an MCP interface for exploration of state transitions

* [ ] Hook SWV instantiation into model and try to see if it can handle our 51 test cases

## Key Takeaways
* Some benefits have dependencies from outside departments
    * An example would be a decision on Child Benefit being deferred to HMRC
* The decision trees that have been produced require an agent (or a human) to navigate them, as they contain terms which are nuanced enough to resist clarification by a non-agent
    * An example might be whether a job offer meets the contractual conditions set out under the Skilled Worker Visa criteria
* There will likely need to be enrichment sources that come from third-party services outside of government
    * An example would be assessing the "going rate" for a particular job role (or the closest known job role)
