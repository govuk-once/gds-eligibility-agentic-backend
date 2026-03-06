<<<<<<< HEAD
# Eligibility via MCP
=======
# Providing Eligibility Functionality via MCP tools
>>>>>>> 46781da (ELIG-243: complete)

## What are you?

Hi! I'm a prototype that shows how eligibility functionality required to service user requirements can
<<<<<<< HEAD
be provided via [MCP](https://modelcontextprotocol.io/docs/getting-started/intro) tools that are used 
by an eligibility agent.
=======
be provided via MCP tools that are used by an eligibility agent.
>>>>>>> 46781da (ELIG-243: complete)

## How do I run you?

To run me, you'll first need to ensure that you:
<<<<<<< HEAD

=======
>>>>>>> 46781da (ELIG-243: complete)
1. have access to AWS Bedrock since that is where my scripts expect to access foundational 
models for my agents. 
1. have set-up [AWS vault](https://github.com/ByteNess/aws-vault) and created an appropriate profile
to store the crendtials to access the AWS Bedrock foundational models mentioned in step 1. 
1. copy the `.env_example` file, name it `.env`, and insert the relevant environment variable values.
1. create and/or activate a `uv` virtual environment (see 
[here](https://docs.astral.sh/uv/pip/environments/) for instructions). I have a `pyproject.toml` that
can be used by `uv`.

<<<<<<< HEAD
### Tests

To run my tests, run the following from my root directory in a terminal:

`$ chmod+x run_tests.sh && ./run_tests.sh <AWS-VAULT-PROFILE-THAT-CAN-ACCESS-AGENT-FOUNDATIONAL-MODELS>`

### Eligibility Service Generator

I contain an agent that takes a URL to a public Government web page containing eligibility criteria for
a particular government service, scrapes its content and content from other pages that are related, before
it produces 3 Python files:

1. An MCP tool that can be used by an agent to walk a user through an eligibility check for that
particular criteria 
2. A test file that defines all paths through the eligibility criteria check
3. A file containing "glue" code that allows the test file to be executed

To run this agent, run the following from my root directory in a terminal:

`$ chmod+x generate_eligibility_service.sh && ./generate_eligibility_service.sh <AWS-VAULT-PROFILE-THAT-CAN-ACCESS-AGENT-FOUNDATIONAL-MODELS>`
=======
Now, to run my tests, run the following from my root directory in a terminal:

`$ chmod+x run_tests.sh && ./run_tests.sh <AWS-VAULT-PROFILE-THAT-CAN-ACCESS-AGENT-FOUNDATIONAL-MODELS>`

>>>>>>> 46781da (ELIG-243: complete)
