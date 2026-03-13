import asyncio
from datetime import datetime
import time
import json
from subprocess import run
from pathlib import Path
import argparse
import random

from google.genai import types
from google.adk.sessions.in_memory_session_service import InMemorySessionService
from google.adk.artifacts.in_memory_artifact_service import InMemoryArtifactService
from google.adk.auth.credential_service.in_memory_credential_service import (
    InMemoryCredentialService,
)
from google.adk.runners import Runner
from google.adk.apps.app import App
from google.adk.utils.context_utils import Aclosing

from deterministic_evals.child_benefit import run_evaluation

from evaluation_judge.agent import get_conversation_pipeline

config = {
    "hypothesis_name": "structured_specification",
    "actor_model_string": "bedrock/converse/eu.anthropic.claude-sonnet-4-5-20250929-v1:0",
    "eligibility_model_string": "bedrock/converse/eu.anthropic.claude-sonnet-4-5-20250929-v1:0",
    "actor_prompt": "structured_generation/child_benefit/actor_v0.1.md",
    "eligibility_prompt": "agents/TechnicalHypotheses/StructuredSpecification-ChildBenefit-v1.md",
    "test_cohort": "child_benefit",
    "output_path": "analysis/testOutputs",
    "app_name" : "evaluation_judge",
    "app_user_id" : "test_user",
    "url_tool_call_allowed" : True,
    "eligibility_agent": 'structured_specification',
    "max_concurrent_cases" : 20,
    # 20 is fine for Sonnet (limits: requests/min 10k, tokens/min 5m)
    # 30 is too too many.
    # For Opus the requests/min are 10k and tokens/min 2m
    # other models may vary.
    # check quotas: https://eu-west-2.console.aws.amazon.com/servicequotas/home/services/bedrock/quotas
    "max_retries" : 3,
    "base_delay" : 5 # seconds (if request fails)
}

def get_short_model_name(model_string: str) -> str:
    """
    Quick and dirty way to get a human-readable model name with no regex.
    So "bedrock/converse/eu.anthropic.claude-sonnet-4-5-20250929-v1:0" -> "claude-sonnet-4-5"
    """
    base_name = model_string.split("/")[-1].split(".")[-1]
    clean_parts = []

    for part in base_name.split("-"):
        # Stop if we hit an 8-digit date (e.g., 20250929)
        if len(part) == 8 and part.isdigit():
            break

        # Stop if we hit a version tag (starts with 'v' followed by a number, e.g., v1:0)
        if part.startswith("v") and part[1:2].isdigit():
            break

        clean_parts.append(part)
    # Stitch it back together
    return "-".join(clean_parts)

def get_or_create_output_directory(resume_val: str | None, execution_datetime: str, git_commit: str) -> Path:
    """
    This is basically to handle the --resume flag, which was necessary because of timeouts.
    Three options:
    1. Don't pass --resume. Default behaviour is to create a new directory and start from first case.
    2. Pass --resume with no args. Default behaviour is to resume from most recent directory.
    3. Pass --resume with args e.g. '--resume "2026-03-04T17:22:27.476356__Model=claude-sonnet-4-5__Commit=cce7a2c"'
       This will resume from the last case in that directory.
       Note: if doing this make sure to set the config params to whatever they were that time. 
    """
    base_path = Path("../../").joinpath(config["output_path"]).joinpath(config["test_cohort"])
    
    # Default behaviour (No ---resume flag): Create a new directory
    if not resume_val:
        model_short_name = get_short_model_name(config["eligibility_model_string"])
        output_dir = base_path.joinpath(f"{execution_datetime}__Model={model_short_name}__Commit={git_commit}")
        output_dir.mkdir(parents=True, exist_ok=True)
        print(f"STARTING NEW RUN: {output_dir.name}")
        return output_dir

    # Default resume (--resume with no folder name passed)
    if resume_val == "LATEST":
        if not base_path.exists():
            raise FileNotFoundError("Cannot resume. Base output directory does not exist yet.")
            
        directories = [d for d in base_path.iterdir() if d.is_dir() and d.name != "eval_reports"]
        if not directories:
            raise FileNotFoundError("Cannot resume. No previous runs found.")
            
        latest_dir = max(directories, key=lambda d: d.name)
        print(f"RESUMING LATEST RUN: {latest_dir.name}")
        return latest_dir

    # Explicit resume (--resume specific_folder_name)
    output_dir = base_path.joinpath(resume_val)
    if not output_dir.exists():
        raise FileNotFoundError(f"Cannot resume. Directory does not exist: {output_dir}")
    print(f"RESUMING SPECIFIC RUN: {output_dir.name}")
    return output_dir

def check_and_clean_existing_output(output_file_path: Path, case_name: str) -> bool:
    """
    Checks if an output file exists and is completely written.
    If it is incomplete or corrupted, it deletes the file so it can be re-run.
    This is for the --resume case. If it was interruped then we get a corrupted json
    which causes problems later.
    
    Returns:
        bool: True if the file is fully complete (meaning the case should be skipped).
              False if the file doesn't exist or was deleted (meaning the case needs to run).
    """
    if not output_file_path.exists():
        return False

    is_complete = False
    try:
        with open(output_file_path, 'r') as f:
            data = json.load(f)
            
            # Check 1: Did the file write successfully to the end?
            if "performance" in data and "duration_seconds" in data["performance"]:
                
                # Check 2: Did the agent actually finish the task before the file was saved?
                # A successful run MUST have the final judgement payload or tool call
                tool_activity = data.get("tool_activity", [])
                
                # Look for the final tool call that proves the agent didn't crash mid-conversation
                has_final_judgement = any(
                    activity.get("tool_name") in ["eligibility_judgement_outcome", "child_benefit_eligibility_agent_payload"]
                    for activity in tool_activity
                )
                
                if has_final_judgement:
                    is_complete = True
                    
    except json.JSONDecodeError:
        pass # File is half-written and corrupted

    if is_complete:
        print(f"Skipping {case_name} (Already complete)")
        return True
    
    # If we get here, the file exists but crashed/timed out before finishing the task
    print(f"Deleting incomplete/crashed file for {case_name}")
    output_file_path.unlink() 
    return False

async def main(resume_val: str | None = None, n_cases: int | None = None):

    git_commit = run(
        ["git", "rev-parse", "--short", "HEAD"],
        capture_output=True,
        check=True,
        text=True,
    ).stdout.strip("\n")
    execution_datetime = datetime.now().isoformat()

    output_dir = get_or_create_output_directory(resume_val, execution_datetime, git_commit)
    test_cases = load_and_parse_test_cases(config["test_cohort"])
    if n_cases:
        test_cases = test_cases[:n_cases]
        print(f"Limiting execution to the first {n_cases} test cases.")

    # Concurrency. max_concurrent_cases = 20 reduced a 2 hour Sonnet run to about 6 mins
    semaphore = asyncio.Semaphore(config["max_concurrent_cases"])

    async def run_case_concurrently(test_id, test_case):
        async with semaphore:
            
            # For --resume case. Can't just check if it exists, need to make sure it's written fully (with judgment playload).
            expected_filename = f"Permutation{test_id}.conversation.json" 
            output_file_path = output_dir / expected_filename
            case_name = test_case.get('case_id', f"Permutation {test_id}")
            if check_and_clean_existing_output(output_file_path, case_name):
                return

            meta = {
                "permutation": test_id,
                "test_case": test_case,
                "execution_datetime": execution_datetime,
                "run_config": {
                    "actor_model_string": config["actor_model_string"],
                    "test_cohort": config["test_cohort"],
                    "commit": git_commit,
                    "hypothesis_name": config["hypothesis_name"],
                    "eligibility_model_string": config["eligibility_model_string"],
                    "actor_prompt": config["actor_prompt"],
                    "eligibility_prompt": config["eligibility_prompt"],
                    "test_set_size": len(test_cases),
                    "url_tool_call_allowed" : config.get("url_tool_call_allowed", True),
                    "max_concurrent_cases" : config["max_concurrent_cases"]
                },
            }
            

            for attempt in range(config["max_retries"]):
                try:
                    # Instantiate services inside the execution block so they are totally isolated
                    session_service = InMemorySessionService()
                    artifact_service = InMemoryArtifactService()
                    credential_service = InMemoryCredentialService()
                    
                    print(f"▶️ Starting {case_name}...")
                    await execute_test_case(
                        test_id,
                        test_case,
                        session_service,
                        artifact_service,
                        credential_service,
                        output_dir,
                        config["test_cohort"],
                        meta,
                    )
                    break # Success! Break out of the retry loop.
                    
                except Exception as e:
                    error_str = str(e).lower()
                    # Pretty quick and dirty test for hitting API limits...
                    if "throttl" in error_str or "rate limit" in error_str or "429" in error_str:
                        if attempt < config["max_retries"] - 1:
                            # Exponential backoff with a random jitter
                            sleep_time = (config["base_delay"] * (2 ** attempt)) + random.uniform(0, 1)
                            print(f"⚠️ Rate limited on {case_name}. Retrying in {sleep_time:.1f}s...")
                            await asyncio.sleep(sleep_time)
                        else:
                            print(f"❌ Failed {case_name} after {config["max_retries"]} attempts due to rate limits.")
                            raise e
                    else:
                        # If it's a normal code bug or framework error, crash so we can fix it
                        print(f"❌ Fatal Error in {case_name}: {e}")
                        raise e

    # This prepares all cases, and the semaphore above ensures only config["max_concurrent_cases"] run at once
    tasks = []
    for test_id, test_case in enumerate(test_cases, start=1):
        tasks.append(run_case_concurrently(test_id, test_case))
        
    await asyncio.gather(*tasks)

    # Auto-evaluate only on full funs
    if n_cases is None:    
        print(f"\nTest execution complete! Triggering deterministic evaluator for {output_dir.name}...")
        try:
            run_evaluation(output_dir.name) 
            print("Evaluation complete. Summary report generated.")
        except Exception as e:
            print(f"Run finished, but evaluator failed to execute: {e}")
    else:
        print("\nSkipping automatic evaluation because --n_cases was used.")

def update_token_usage(event, usage_dict: dict) -> None:
    """Extracts token metrics from an ADK event and updates the usage tracker in place."""
    usage = getattr(event, "usage_metadata", None)
    if not usage:
        return

    # Safely handle both dict and object access depending on the ADK version/model
    if isinstance(usage, dict):
        p_tokens = usage.get("prompt_token_count", usage.get("prompt_tokens", 0))
        c_tokens = usage.get("candidates_token_count", usage.get("completion_tokens", 0))
    else:
        p_tokens = getattr(usage, "prompt_token_count", getattr(usage, "prompt_tokens", 0))
        c_tokens = getattr(usage, "candidates_token_count", getattr(usage, "completion_tokens", 0))
    
    # Update global totals
    usage_dict["total_prompt_tokens"] += p_tokens
    usage_dict["total_completion_tokens"] += c_tokens
    usage_dict["total_overall_tokens"] += (p_tokens + c_tokens)
    
    # Update per-agent breakdown
    author = getattr(event, "author", "unknown_agent")
    if author not in usage_dict["breakdown_by_agent"]:
        usage_dict["breakdown_by_agent"][author] = {
            "prompt_tokens": 0, "completion_tokens": 0, "total": 0
        }
    
    usage_dict["breakdown_by_agent"][author]["prompt_tokens"] += p_tokens
    usage_dict["breakdown_by_agent"][author]["completion_tokens"] += c_tokens
    usage_dict["breakdown_by_agent"][author]["total"] += (p_tokens + c_tokens)

async def execute_test_case(
    test_id: int,
    test_case: dict,
    session_service: InMemorySessionService,
    artifact_service: InMemoryArtifactService,
    credential_service: InMemoryCredentialService,
    output_dir: Path,
    test_cohort: str,
    meta: dict,
):
    """
    This is largely inspired by/borrowed from `google.adk.cli.cli.run_interactively`
    https://github.com/google/adk-python/blob/32f2ec3a78c4ef8475b7d8a630705e4cf5ccbe50/src/google/adk/cli/cli.py#L88
    """

    app = App(
        name=config["app_name"],
        root_agent=get_conversation_pipeline(
            test_case["agent_script"],
            config["actor_model_string"],
            config["eligibility_model_string"],
            config["actor_prompt"],
            config["eligibility_prompt"],
            config["eligibility_agent"],
            config.get("url_tool_call_allowed", True)
        ),
    )

    session = await session_service.create_session(app_name=config["app_name"], user_id=config["app_user_id"])
    runner = Runner(
        app=app,
        artifact_service=artifact_service,
        session_service=session_service,
        credential_service=credential_service,
    )

    payload = {
        "case_id": test_case["case_id"],
        "meta": meta,
        "usage": {
            "total_prompt_tokens": 0,
            "total_completion_tokens": 0,
            "total_overall_tokens": 0,
            "breakdown_by_agent": {} # We'll track actor vs eligibility_agent tokens here
        },
        "performance" : {},
        "conversation": [],
        "tool_activity": [],
        "tool_response": []
    }

    # Start the stopwatch
    start_time = time.perf_counter()

    with output_dir.joinpath(f"Permutation{test_id}.conversation.json").open(
        "a+"
    ) as output_file:
        print(f"Outputting dialogue to {output_file.name}")
        async with Aclosing(
            runner.run_async(
                user_id=config["app_user_id"],
                session_id=session.id,
                new_message=types.Content(
                    role="user",
                    parts=[
                        types.Part(
                            text=f"am I eligible for {test_cohort.replace('_', ' ')}"
                        )
                    ],
                ),
            )
        ) as agen:
            try:
                async for event in agen:
                    # Count tokens
                    update_token_usage(event, payload["usage"])
                    if event.content and event.content.parts:
                        for part in event.content.parts:
                            
                            # A. Track the LLM's raw requests (Keeps our URL logging working!)
                            if getattr(part, "function_call", None):
                                tool_args = getattr(part.function_call, "args", {})

                                # Safely convert to dictionary if the framework returned a Pydantic object
                                if hasattr(tool_args, "dict"):
                                    tool_args = tool_args.dict()
                                elif not isinstance(tool_args, dict):
                                    tool_args = dict(tool_args)

                                payload["tool_activity"].append(
                                    {
                                        "timestamp": datetime.now().isoformat(),
                                        "tool_name": part.function_call.name,
                                        "arguments": tool_args,
                                        "author": event.author,
                                    }
                                )

                            # B. Catch the framework's response (This contains your zip() output!)
                            if getattr(part, "function_response", None):
                                # We only want to save the final judgement to the root payload, 
                                # not the giant text dumps from the web scraper.
                                if part.function_response.name == "eligibility_judgement_outcome":
                                    payload[f"{event.author}_payload"] = {
                                        "response": part.function_response.dict()
                                    }
                                elif part.function_response.name in [
                                    "start_assessment",
                                    "get_node_info",
                                    "navigate_to_outcome",
                                    "get_constants",
                                    "get_validation_rules",
                                    "get_specification_metadata",
                                ]:
                                    payload["tool_response"].append({
                                        "response": part.function_response.dict()
                                    })

                        # Log the standard text conversation
                        if text := "".join(p.text or "" for p in event.content.parts):
                            payload["conversation"].append(
                                {
                                    "timestamp": datetime.now().isoformat(),
                                    "author": event.author,
                                    "text": text,
                                }
                            )

                    if getattr(event.actions, "escalate", False):
                        await runner.close()
                        
            finally:
                # Stop the stopwatch and record the duration
                end_time = time.perf_counter()
                payload["performance"]["duration_seconds"] = round(
                    end_time - start_time, 2
                )

                json.dump(payload, output_file, indent=4)


def load_and_parse_test_cases(test_cohort: str):

    test_case_file = Path(
        f"../../prompts/structured_generation/{test_cohort}/test_cases.jsonl"
    )

    test_cases = []
    with test_case_file.open("r") as f:
        for line in f:
            if (
                line.strip()
            ):  # Skip empty lines (shouldn't be any though except the last perhaps)
                test_cases.append(json.loads(line))

    return test_cases


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the Eligibility Agent evaluation.")
    
    parser.add_argument(
        "--resume", 
        nargs="?", # 0 or 1 arguments. 
        const="LATEST", # if --resume present but no args then resume from latest folder
        default=None, # if no --resume flag start a new run
        help="Resume a run. Omit to start new. Pass --resume to use the latest folder, or --resume <folder_name> for a specific one."
    )

    parser.add_argument(
        "--n_cases", 
        type=int, 
        default=None, 
        help="Limit the number of test cases to run (e.g., 1 for debugging)."
    )
    args = parser.parse_args()    
    asyncio.run(main(args.resume, args.n_cases))
