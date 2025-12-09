import asyncio
import uuid
from pathlib import Path

from google.genai import types
from google.adk.sessions.in_memory_session_service import InMemorySessionService
from google.adk.artifacts.in_memory_artifact_service import InMemoryArtifactService
from google.adk.auth.credential_service.in_memory_credential_service import InMemoryCredentialService
from google.adk.runners import Runner
from google.adk.apps.app import App
from google.adk.sessions.session import Session
from google.adk.utils.context_utils import Aclosing

from evaluation_judge.agent import review_pipeline


async def main():
    test_cases = load_and_parse_test_cases()
    session_service = InMemorySessionService()
    artifact_service = InMemoryArtifactService()
    credential_service = InMemoryCredentialService()
    for test_case in test_cases:
        foo = execute_test_case(
            test_case,
            session_service,
            artifact_service,
            credential_service
        )
        import pudb; pudb.set_trace()



async def execute_test_case(
    test_case,
    session_service,
    artifact_service,
    credential_service

):
    """
        This is largely inspired by/borrowed from `google.adk.cli.cli.run_interactively`
        https://github.com/google/adk-python/blob/32f2ec3a78c4ef8475b7d8a630705e4cf5ccbe50/src/google/adk/cli/cli.py#L88
    """
    app_name = "evaluation_judge"
    user_id = "test_user"
    app = App(name=app_name, root_agent=review_pipeline)
    session = await session_service.create_session(
        app_name=app_name, user_id=user_id
    )
    runner = Runner(
        app=app,
        artifact_service=artifact_service,
        session_service=session_service,
        credential_service=credential_service,
    )
    while True:
        async with Aclosing(
            runner.run_async(
                user_id=user_id,
                session_id=session.id,
                new_message=types.Content(
                    role='user', parts=[types.Part(text=test_case)]
                ),
            )
        ) as agen:
            async for event in agen:
                if event.content and event.content.parts:
                    if text := ''.join(part.text or '' for part in event.content.parts):
                        print(f'[{event.author}]: {text}')
    await runner.close()


def load_and_parse_test_cases():
    test_case_file = Path("../../prompts/manual/test_case_generation/child_benefit.md")
    with test_case_file.open() as f:
        raw_test_cases = f.readlines()
    test_cases_str = "\n".join(raw_test_cases)
    test_cases = test_cases_str.split(sep='---')
    return test_cases


if __name__ == "__main__":
    asyncio.run(main())
