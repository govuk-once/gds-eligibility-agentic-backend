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

from evaluation_judge.agent import get_review_pipeline


async def main():
    test_cohort = "child_benefit"
    hypothesis_name = test_cohort
    #hypothesis_name = f"{test_cohort}__stressTestAgent"
    #  test_cohort = "skilled_worker_visa"
    git_commit = run(
        ["git", "rev-parse", "--short", "HEAD"],
        capture_output=True,
        check=True,
        text=True,
    ).stdout.strip("\n")
    test_cases = load_and_parse_test_cases(test_cohort)
    output_dir = (
        Path("../../") # Repository root
        .joinpath("analysis/.testOutputs")
        .joinpath(hypothesis_name)
        .joinpath(datetime.now().isoformat() + f"__RepoCommit={git_commit}")
    )
    output_dir.mkdir(parents=True)
    #  test_cases = [test_cases[0]] # Uncomment this to run one test case for developing against test runner
    for test_id, test_case in enumerate(test_cases, start=1):
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
            test_cohort,
        )
    #run(
    #    ["rg", "✗", output_dir, "--stats"], capture_output=False, check=False, text=True
    #)  # Don't check as no results returns error


async def execute_test_case(
    test_id: int,
    test_case: str,
    session_service: InMemorySessionService,
    artifact_service: InMemoryArtifactService,
    credential_service: InMemoryCredentialService,
    output_dir: Path,
    test_cohort: str,
):
    """
    This is largely inspired by/borrowed from `google.adk.cli.cli.run_interactively`
    https://github.com/google/adk-python/blob/32f2ec3a78c4ef8475b7d8a630705e4cf5ccbe50/src/google/adk/cli/cli.py#L88
    """
    app_name = "evaluation_judge"
    user_id = "test_user"
    test_case_without_outcome, expected_outcome = split_outcome_from_test_case(test_case)
    app = App(
        name=app_name, 
        root_agent=get_review_pipeline(test_case_without_outcome, expected_outcome=expected_outcome)
    )
    session = await session_service.create_session(app_name=app_name, user_id=user_id)
    runner = Runner(
        app=app,
        artifact_service=artifact_service,
        session_service=session_service,
        credential_service=credential_service,
    )
    payload = defaultdict(conversation=list())
    with output_dir.joinpath(f"Permutation{test_id}.json").open("a+") as output_file:
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
                            print(output) # Uncomment for developing against test runner
            finally:
                json.dump(payload, output_file, indent=4)


def load_and_parse_test_cases(test_cohort: str):
    test_case_file = Path(f"../../prompts/manual/test_cases/{test_cohort}.md")
    with test_case_file.open() as f:
        raw_test_cases = f.readlines()
    test_cases_str = "\n".join(raw_test_cases)
    test_cases = test_cases_str.split(sep="---")
    return test_cases


def split_outcome_from_test_case(test_case: str) -> str:
    outcome_index = test_case.lower().find("outcome")
    truncated_test_case = test_case[:outcome_index]
    outcome = test_case[outcome_index:]
    assert "outcome" not in truncated_test_case.lower()
    assert "outcome" in outcome.lower()
    return truncated_test_case, outcome


if __name__ == "__main__":
    asyncio.run(main())
