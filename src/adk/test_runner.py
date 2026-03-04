import asyncio
from collections import defaultdict
from datetime import datetime
import json
from subprocess import run
from pathlib import Path

from google.genai import types
from google.adk.sessions.in_memory_session_service import InMemorySessionService
from google.adk.artifacts.in_memory_artifact_service import InMemoryArtifactService
from google.adk.auth.credential_service.in_memory_credential_service import (
    InMemoryCredentialService,
)
from google.adk.runners import Runner
from google.adk.apps.app import App
from google.adk.utils.context_utils import Aclosing

from evaluation_judge.agent import get_review_pipeline, get_conversation_pipeline

config = {
    "actor_model_string" : "bedrock/converse/eu.anthropic.claude-sonnet-4-5-20250929-v1:0",
    "eligibility_model_string" : "bedrock/converse/eu.anthropic.claude-sonnet-4-5-20250929-v1:0",
    "actor_prompt" : "structured_generation/child_benefit/actor_v0.1.md",
    "eligibility_prompt" : "agents/TechnicalHypotheses/Accuracy-ChildBenefit-structuredOutput-v2.md",
    "test_cohort" : "child_benefit"
}

def get_short_model_name(model_string: str) -> str:
    """
    Quick and dirty way to get a human-readable model name with no regex.
    So "bedrock/converse/eu.anthropic.claude-sonnet-4-5-20250929-v1:0" -> "claude-sonnet-4-5"
    """
    base_name = model_string.split('/')[-1].split('.')[-1]
    clean_parts = []

    for part in base_name.split('-'):
        # Stop if we hit an 8-digit date (e.g., 20250929)
        if len(part) == 8 and part.isdigit():
            break
            
        # Stop if we hit a version tag (starts with 'v' followed by a number, e.g., v1:0)
        if part.startswith('v') and part[1:2].isdigit():
            break
            
        clean_parts.append(part)    
    # Stitch it back together
    return '-'.join(clean_parts)




async def main():
    
    model_short_name = get_short_model_name(config["eligibility_model_string"])
    #hypothesis_name = f"{test_cohort}__stressTestAgent"
    #  test_cohort = "skilled_worker_visa"
    git_commit = run(
        ["git", "rev-parse", "--short", "HEAD"],
        capture_output=True,
        check=True,
        text=True,
    ).stdout.strip("\n")
    test_cases = load_and_parse_test_cases(config["test_cohort"])
    execution_datetime = datetime.now().isoformat() 
    output_dir = (
        Path("../../") # Repository root
        .joinpath("analysis/testOutputs")
        .joinpath(config["test_cohort"])
        .joinpath(f"{execution_datetime}__Model={model_short_name}__Commit={git_commit}")
    )
    
    output_dir.mkdir(parents=True)
    #test_cases = [test_cases[0]] # Uncomment this to run one test case for developing against test runner
    for test_id, test_case in enumerate(test_cases, start=1):
        meta = {
            "permutation": test_id,
            "test_case": test_case,
            "commit": git_commit,
            "hypothesis_name": config["test_cohort"],
            "test_cohort": config["test_cohort"],
            "execution_datetime":  execution_datetime,
            "run_config": {
                "actor_model_string": config["actor_model_string"],
                "eligibility_model_string" : config["eligibility_model_string"],
                "actor_prompt": config["actor_prompt"],
                "eligibility_prompt": config["eligibility_prompt"],
                "test_set_size": len(test_cases)
            }            
        }
        session_service = InMemorySessionService()
        artifact_service = InMemoryArtifactService()
        credential_service = InMemoryCredentialService()
        await execute_test_case(
            test_id,
            test_case,
            session_service,
            artifact_service,
            credential_service,
            output_dir,
            config["test_cohort"],
            meta
        )
    #run(
    #    ["rg", "✗", output_dir, "--stats"], capture_output=False, check=False, text=True
    #)  # Don't check as no results returns error


async def execute_test_case(
    test_id: int,
    test_case: dict,
    session_service: InMemorySessionService,
    artifact_service: InMemoryArtifactService,
    credential_service: InMemoryCredentialService,
    output_dir: Path,
    test_cohort: str,
    meta: dict[str, str],
):
    """
    This is largely inspired by/borrowed from `google.adk.cli.cli.run_interactively`
    https://github.com/google/adk-python/blob/32f2ec3a78c4ef8475b7d8a630705e4cf5ccbe50/src/google/adk/cli/cli.py#L88
    """
    app_name = "evaluation_judge"
    user_id = "test_user"

    app = App(
        name=app_name, 
        root_agent=get_conversation_pipeline(
            test_case["agent_script"],
            config["actor_model_string"],
            config["eligibility_model_string"],
            config["actor_prompt"],
            config["eligibility_prompt"]
        )
    )
    session = await session_service.create_session(app_name=app_name, user_id=user_id)
    runner = Runner(
        app=app,
        artifact_service=artifact_service,
        session_service=session_service,
        credential_service=credential_service,
    )
    payload = defaultdict(conversation=list())
    payload["meta"] = { "conversation": meta }
    with output_dir.joinpath(f"Permutation{test_id}.conversation.json").open("a+") as output_file:
        print(f"Outputting dialogue to {output_file.name}")
        async with Aclosing(
            runner.run_async(
                user_id=user_id,
                session_id=session.id,
                new_message=types.Content(
                    role="user", parts=[types.Part(text=f"am I eligible for {test_cohort.replace('_', ' ')}")]
                ),
            )
        ) as agen:
            try:
                async for event in agen:
                    if any([part.function_response for part in event.content.parts]):
                        assert len(event.content.parts) == 1
                        payload.update({f"{event.author}_payload": event.content.parts[0].function_response.dict()})
                    if event.actions.escalate:
                        #assert len(event.content.parts) == 1
                        #payload.update({f"{event.author}_payload": event.content.parts[0].function_response.json()})
                        await runner.close()
                    if event.content and event.content.parts:
                        if text := "".join(part.text or "" for part in event.content.parts):
                            payload['conversation'].append(
                                {
                                    'timestamp': datetime.now().isoformat(),
                                    'author': event.author,
                                    'text': text,
                                }
                            )
                            output = f"{datetime.now().isoformat()} [{event.author}]: {text}\n"
                            #print(output) # Uncomment for developing against test runner
            finally:
                json.dump(payload, output_file, indent=4)

def load_and_parse_test_cases(test_cohort: str):

    test_case_file = Path(f"../../prompts/structured_generation/{test_cohort}/test_cases.jsonl")
    
    test_cases = []
    with test_case_file.open("r") as f:
        for line in f:
            if line.strip():  # Skip empty lines (shouldn't be any though except the last perhaps)
                test_cases.append(json.loads(line))
                
    return test_cases


if __name__ == "__main__":
    asyncio.run(main())

