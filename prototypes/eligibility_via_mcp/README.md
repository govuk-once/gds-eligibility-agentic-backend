# Eligibility via MCP

## What are you?

Hi! I'm a prototype that shows how eligibility functionality required to service user requirements can
be provided via [MCP](https://modelcontextprotocol.io/docs/getting-started/intro) tools that are used 
by an eligibility agent.

## How do I run you?

To run me, you'll first need to ensure that you:

1. have access to AWS Bedrock since that is where my scripts expect to access foundational 
models for my agents. 
1. have set-up [AWS vault](https://github.com/ByteNess/aws-vault) and created an appropriate profile
to store the crendtials to access the AWS Bedrock foundational models mentioned in step 1. 
1. copy the `.env_example` file, name it `.env`, and insert the relevant environment variable values.
1. create and/or activate a `uv` virtual environment (see 
[here](https://docs.astral.sh/uv/pip/environments/) for instructions). I have a `pyproject.toml` that
can be used by `uv`.

Now, to run my tests, run the following from my root directory in a terminal:

`$ chmod+x run_tests.sh && ./run_tests.sh <AWS-VAULT-PROFILE-THAT-CAN-ACCESS-AGENT-FOUNDATIONAL-MODELS>`

