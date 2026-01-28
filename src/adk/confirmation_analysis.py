import asyncio
import re
from datetime import datetime
from subprocess import run
from pathlib import Path
from typing import TextIO

from google.genai import types
from google.adk.sessions.in_memory_session_service import InMemorySessionService
from google.adk.artifacts.in_memory_artifact_service import InMemoryArtifactService
from google.adk.auth.credential_service.in_memory_credential_service import (
    InMemoryCredentialService,
)
from google.adk.runners import Runner
from google.adk.apps.app import App
from google.adk.utils.context_utils import Aclosing

from evaluation_judge.agent import get_judge_agent


async def main():
    test_cohort = "child_benefit"
    hypothesis_name = f"{test_cohort}__stressTestAgent"
    #  test_cohort = "skilled_worker_visa"
    git_commit = 'e680f99'
    test_cases = load_and_parse_test_cases(test_cohort)
    current_datetime = datetime.now().isoformat()
    input_dirs = list(
        Path("./.testOutputs")
        .joinpath(hypothesis_name)
        #.glob("2026-01-27T17:16:06.069548__RepoCommit=ffd4b17")
        .glob(f"*__RepoCommit={git_commit}")
    )
    print('Looking in', input_dirs)
    for input_dir in input_dirs:
        print('Looking in', input_dirs)
        for input_filepath in input_dir.glob("Permutation*.out"):
            permutation_number = int(re.search(
                r"Permutation(?P<permutation>\d+).out", 
                input_filepath.name
            ).groupdict().get("permutation"))
            print("directory", input_dir, " permutation ", permutation_number)
            test_case = test_cases[permutation_number - 1]
            session_service = InMemorySessionService()
            artifact_service = InMemoryArtifactService()
            credential_service = InMemoryCredentialService()
            with (
                #input_dir.joinpath(f"Permutation{permutation_number}.out").open("r") as input_file, 
                input_filepath.open("r") as input_file, 
                input_dir.joinpath(f"Permutation{permutation_number}__rejudgement_{current_datetime}").open("a+") as output_file
            ):
                await execute_test_case(
                    permutation_number,
                    test_case,
                    session_service,
                    artifact_service,
                    credential_service,
                    input_file,
                    output_file,
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
    input_file: TextIO,
    output_file: TextIO,
    test_cohort: str,
):
    """
    This is largely inspired by/borrowed from `google.adk.cli.cli.run_interactively`
    https://github.com/google/adk-python/blob/32f2ec3a78c4ef8475b7d8a630705e4cf5ccbe50/src/google/adk/cli/cli.py#L88
    """
    app_name = "confirmation_judge"
    user_id = "test_user"
    test_case_without_outcome, expected_outcome = split_outcome_from_test_case(test_case)
    evaluation_judge = get_judge_agent(
        app_name,
        "agents/Ancillary/EvaluationJudge-confirmation-v1.md", 
        test_case_without_outcome=test_case_without_outcome,
        expected_outcome=expected_outcome
    )
    app = App(name=app_name, root_agent=evaluation_judge)
    session = await session_service.create_session(app_name=app_name, user_id=user_id)
    runner = Runner(
        app=app,
        artifact_service=artifact_service,
        session_service=session_service,
        credential_service=credential_service,
    )
    print(f"Outputting dialogue to {output_file.name}")
    async with Aclosing(
        runner.run_async(
            user_id=user_id,
            session_id=session.id,
            new_message=types.Content(
                role="user", parts=[types.Part(text=''.join(input_file.readlines()))]
            ),
        )
    ) as agen:
        async for event in agen:
            if event.actions.escalate:
                await runner.close()
            if event.content and event.content.parts:
                if text := "".join(part.text or "" for part in event.content.parts):
                    output = f"{datetime.now().isoformat()} [{event.author}]: {text}\n"
                    output_file.writelines(f"{output}\n")
                    #print(output) # Uncomment for developing against test runner


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

